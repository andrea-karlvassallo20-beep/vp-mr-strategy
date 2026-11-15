"""Forward-scoring calibration log: append-only, hash-chained, sealed at
decision moments.

The ledger is `logs/forward_calibration.jsonl`, one JSON object per line.
Two record types share a single SHA-256 chain:

  decision    — sealed at t_0, BEFORE any outcome can exist. Carries the
                Layer 1 phase, Layer 2 direction probability, Layer 3
                hazard ratio, the horizon end, and a SHA-256 of the causal
                feature vector X(t_0). Every label field must be absent.
  resolution  — appended only once current time is strictly past the
                horizon end. Never mutates the decision line.

Binding rules:
  1. Strict monotonicity: a decision is refused if its timestamp_utc_us is
     not strictly greater than the last record's timestamp in the ledger.
  2. Rule 3 (never label at or before observation): any populated label
     field at creation time refuses the entry outright.
  3. The chain is verified before any resolution is appended; a broken or
     tampered ledger refuses all writes.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

GENESIS_PREV_SHA256 = "0" * 64
DECISION_RECORD = "decision"
RESOLUTION_RECORD = "resolution"

DECISION_FIELDS = (
    "entry_id",
    "timestamp_utc_us",
    "instrument",
    "layer1_phase",
    "layer2_p_up",
    "layer2_ci_95",
    "layer3_hazard_ratio",
    "horizon_end_utc_us",
    "feature_vector_sha256",
)
LABEL_FIELDS = (
    "resolved_outcome_up",
    "realized_return",
    "resolution_timestamp_utc_us",
    "hit_direction",
)


def _canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, default=_jsonable)


def _jsonable(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    return o


def _record_sha256(record: dict) -> str:
    body = {k: v for k, v in record.items() if k != "entry_sha256"}
    return hashlib.sha256(_canonical_json(body).encode("utf-8")).hexdigest()


def now_utc_us() -> int:
    return int(time.time() * 1_000_000)


def _read_records(ledger_path) -> list:
    path = Path(ledger_path)
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"ledger line {lineno} is not valid JSON: {exc}") from exc
    return records


def verify_hash_chain(ledger_path) -> dict:
    """Verify the full SHA-256 chain and record-type structure.

    Returns {"n_records", "n_decisions", "n_resolutions", "head_sha256"}.
    Raises ValueError on any tamper, break, or structural violation.
    """
    records = _read_records(ledger_path)
    prev = GENESIS_PREV_SHA256
    last_ts = None
    n_dec = n_res = 0
    resolved_ids = set()
    for i, rec in enumerate(records, 1):
        if rec.get("record_type") not in (DECISION_RECORD, RESOLUTION_RECORD):
            raise ValueError(f"record {i}: unknown record_type "
                             f"{rec.get('record_type')!r}")
        if rec.get("prev_entry_sha256") != prev:
            raise ValueError(
                f"record {i}: hash chain broken (prev_entry_sha256 mismatch)")
        recomputed = _record_sha256(rec)
        if rec.get("entry_sha256") != recomputed:
            raise ValueError(f"record {i}: entry_sha256 does not match "
                             "its own content (tampered line)")
        ts = rec.get("timestamp_utc_us")
        if not isinstance(ts, int):
            raise ValueError(f"record {i}: missing/invalid timestamp_utc_us")
        if last_ts is not None and ts <= last_ts:
            raise ValueError(f"record {i}: timestamp_utc_us is not strictly "
                             "monotonic")
        last_ts = ts
        if rec["record_type"] == DECISION_RECORD:
            for field in LABEL_FIELDS:
                if rec.get(field) is not None:
                    raise ValueError(f"record {i}: decision carries label "
                                     f"field {field!r} (Rule 3 violation)")
            missing = [f for f in DECISION_FIELDS if f not in rec]
            if missing:
                raise ValueError(f"record {i}: decision missing fields "
                                 f"{missing}")
            if rec["horizon_end_utc_us"] <= rec["timestamp_utc_us"]:
                raise ValueError(f"record {i}: horizon_end_utc_us must be "
                                 "strictly after timestamp_utc_us")
            n_dec += 1
        else:
            entry_id = rec.get("entry_id")
            if entry_id in resolved_ids:
                raise ValueError(f"record {i}: duplicate resolution for "
                                 f"entry {entry_id!r}")
            resolved_ids.add(entry_id)
            if rec.get("resolved_outcome_up") is None:
                raise ValueError(f"record {i}: resolution without outcome")
            n_res += 1
        prev = recomputed
    return {
        "n_records": len(records),
        "n_decisions": n_dec,
        "n_resolutions": n_res,
        "head_sha256": prev if records else GENESIS_PREV_SHA256,
    }


def _append_record(ledger_path, record: dict) -> dict:
    path = Path(ledger_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = verify_hash_chain(ledger_path)
    record["entry_sha256"] = _record_sha256(record)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True,
                            separators=(",", ":")) + "\n")
    return record


def feature_vector_sha256(feature_vector) -> str:
    """SHA-256 of the causal feature vector X(t_0), canonically encoded."""
    return hashlib.sha256(
        _canonical_json(_jsonable(feature_vector)).encode("utf-8")
    ).hexdigest()


def append_decision_entry(
    ledger_path,
    *,
    entry_id,
    timestamp_utc_us,
    instrument,
    layer1_phase,
    layer2_p_up,
    layer2_ci_95,
    layer3_hazard_ratio,
    horizon_end_utc_us,
    feature_vector,
    **extra,
) -> dict:
    """Seal one decision at moment t_0. Refuses non-monotonic timestamps and
    any populated label field (Rule 3: never label at or before observation).
    """
    for field in LABEL_FIELDS:
        if extra.get(field) is not None:
            raise ValueError(
                f"refused: label field {field!r} populated at decision "
                "moment (Rule 3: never label an event before or at "
                "observation)")
    if not isinstance(timestamp_utc_us, int) or timestamp_utc_us <= 0:
        raise ValueError("timestamp_utc_us must be a positive integer "
                         "(microseconds since epoch)")
    if not isinstance(horizon_end_utc_us, int) \
            or horizon_end_utc_us <= timestamp_utc_us:
        raise ValueError("horizon_end_utc_us must be an integer strictly "
                         "after timestamp_utc_us")
    if not (0.0 <= float(layer2_p_up) <= 1.0):
        raise ValueError("layer2_p_up must lie in [0, 1]")
    ci = [float(x) for x in layer2_ci_95]
    if len(ci) != 2 or not (0.0 <= ci[0] <= ci[1] <= 1.0):
        raise ValueError("layer2_ci_95 must be a [lo, hi] pair in [0, 1]")

    state = verify_hash_chain(ledger_path)
    records = _read_records(ledger_path)
    if records:
        last_ts = records[-1]["timestamp_utc_us"]
        if timestamp_utc_us <= last_ts:
            raise ValueError(
                f"refused: timestamp_utc_us {timestamp_utc_us} is not "
                f"strictly greater than the ledger head {last_ts}")

    record = {
        "record_type": DECISION_RECORD,
        "entry_id": str(entry_id),
        "prev_entry_sha256": state["head_sha256"],
        "timestamp_utc_us": timestamp_utc_us,
        "instrument": str(instrument),
        "layer1_phase": str(layer1_phase),
        "layer2_p_up": float(layer2_p_up),
        "layer2_ci_95": ci,
        "layer3_hazard_ratio": float(layer3_hazard_ratio),
        "horizon_end_utc_us": horizon_end_utc_us,
        "feature_vector_sha256": feature_vector_sha256(feature_vector),
    }
    return _append_record(ledger_path, record)


def _outcome_column(df: pd.DataFrame) -> str:
    for col in ("outcome_up", "realized_outcome_up", "direction_up"):
        if col in df.columns:
            return col
    raise ValueError("realized_trades_df needs an outcome column: "
                     "'outcome_up' (1 = up, 0 = down)")


def _entry_ts_column(df: pd.DataFrame) -> str:
    for col in ("entry_timestamp_utc_us", "timestamp_utc_us",
                "decision_timestamp_utc_us"):
        if col in df.columns:
            return col
    raise ValueError("realized_trades_df needs an entry timestamp column: "
                     "'entry_timestamp_utc_us'")


def resolve_matured_entries(ledger_path, realized_trades_df,
                            current_utc_us=None) -> dict:
    """Resolve entries whose horizon has matured and compute calibration.

    Only entries with current_utc_us > horizon_end_utc_us are scored; each
    resolution is appended as a new chained line (historical lines are never
    touched). The hash chain is verified before and after.

    Returns a summary dict with cumulative out-of-sample Brier score,
    Brier skill score vs rolling climatology, and exact Clopper-Pearson
    95% bounds on the directional hit rate.
    """
    if current_utc_us is None:
        current_utc_us = now_utc_us()
    verify_hash_chain(ledger_path)
    records = _read_records(ledger_path)

    decisions = [r for r in records if r["record_type"] == DECISION_RECORD]
    resolved_ids = {r["entry_id"] for r in records
                    if r["record_type"] == RESOLUTION_RECORD}
    matured = [d for d in decisions
               if d["entry_id"] not in resolved_ids
               and current_utc_us > d["horizon_end_utc_us"]]
    if not matured:
        return calibration_metrics(ledger_path) | {
            "n_newly_resolved": 0,
            "n_unresolved_missing_outcome": 0,
        }

    df = realized_trades_df
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    ts_col = _entry_ts_column(df)
    out_col = _outcome_column(df)
    if "instrument" not in df.columns:
        raise ValueError("realized_trades_df needs an 'instrument' column")
    lookup = {
        (str(row["instrument"]), int(row[ts_col])): row[out_col]
        for _, row in df.iterrows()
    }

    missing = 0
    newly = 0
    head = _record_sha256(records[-1]) if records else GENESIS_PREV_SHA256
    lines = []
    for d in matured:
        key = (d["instrument"], d["timestamp_utc_us"])
        if key not in lookup:
            missing += 1
            continue
        outcome = lookup[key]
        if pd.isna(outcome):
            missing += 1
            continue
        outcome = int(bool(outcome))
        record = {
            "record_type": RESOLUTION_RECORD,
            "entry_id": d["entry_id"],
            "prev_entry_sha256": head,
            "timestamp_utc_us": current_utc_us + len(lines),
            "ref_decision_timestamp_utc_us": d["timestamp_utc_us"],
            "instrument": d["instrument"],
            "resolved_outcome_up": outcome,
        }
        record["entry_sha256"] = _record_sha256(record)
        lines.append(record)
        head = record["entry_sha256"]
        newly += 1

    if lines:
        path = Path(ledger_path)
        with path.open("a", encoding="utf-8") as fh:
            for record in lines:
                fh.write(json.dumps(record, sort_keys=True,
                                    separators=(",", ":")) + "\n")
    verify_hash_chain(ledger_path)

    summary = calibration_metrics(ledger_path)
    summary["n_newly_resolved"] = newly
    summary["n_unresolved_missing_outcome"] = missing
    return summary


def calibration_metrics(ledger_path, climatology_window: int | None = None,
                        cp_alpha: float = 0.05) -> dict:
    """Cumulative out-of-sample calibration metrics over resolved pairs.

    Brier score: mean((layer2_p_up - outcome)^2) over resolved entries.
    Brier skill score: 1 - BS / BS_clim, where the climatology for each
    entry is the mean outcome of the preceding resolved entries (expanding
    window, or the last `climatology_window` resolved entries when given;
    0.5 until the first resolution exists).
    Directional hit rate: share of resolved entries where the realized
    direction was UP, with exact Clopper-Pearson 95% bounds.
    """
    verify_hash_chain(ledger_path)
    records = _read_records(ledger_path)
    by_id = {r["entry_id"]: r for r in records
             if r["record_type"] == DECISION_RECORD}
    pairs = [
        (d["layer2_p_up"], int(r["resolved_outcome_up"]))
        for r in records if r["record_type"] == RESOLUTION_RECORD
        for d in [by_id[r["entry_id"]]]
    ]
    n = len(pairs)
    if n == 0:
        return {
            "n_scored": 0,
            "brier_score": None,
            "brier_skill_score_vs_rolling_climatology": None,
            "hit_rate_up": None,
            "hit_rate_up_cp95_low": None,
            "hit_rate_up_cp95_high": None,
        }

    p = np.array([q for q, _ in pairs], dtype=float)
    y = np.array([o for _, o in pairs], dtype=float)
    brier = float(np.mean((p - y) ** 2))

    clim_sq = np.empty(n)
    prior = [0.5]
    for i in range(n):
        hist = prior[:-1] if climatology_window is None \
            else prior[-(climatology_window + 1):-1]
        clim = float(np.mean(hist)) if hist else 0.5
        clim_sq[i] = (clim - y[i]) ** 2
        prior.append(y[i])
    brier_clim = float(np.mean(clim_sq))
    skill = 1.0 - brier / brier_clim if brier_clim > 0 else None

    k = int(y.sum())
    lo = float(stats.beta.ppf(cp_alpha / 2.0, k, n - k + 1)) if k > 0 else 0.0
    hi = float(stats.beta.ppf(1.0 - cp_alpha / 2.0, k + 1, n - k)) \
        if k < n else 1.0
    return {
        "n_scored": n,
        "brier_score": brier,
        "brier_climatology_score": brier_clim,
        "brier_skill_score_vs_rolling_climatology": skill,
        "hit_rate_up": k / n,
        "hit_rate_up_n_up": k,
        "hit_rate_up_cp95_low": lo,
        "hit_rate_up_cp95_high": hi,
    }
