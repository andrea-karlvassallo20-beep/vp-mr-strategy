"""The surprise ledger - sealed scores vs realized jumps, over time.

Directive (Andrea, Nov 2026): the board is scored, and then over time we
track what surprises and we study it. This module is the time half of the
heat map: an append-only, hash-chained JSONL ledger (the same discipline
as forward_log.py) with two record types on one SHA-256 chain:

  snapshot   - sealed at t0, BEFORE any outcome can exist. Carries the
               top-k eligible candidates per class with their full
               priming feature vector (score, comp_days, rvol_pct,
               range_pos, vol_ratio, evr_m, last_date) and the data
               file the resolution must be read from. No outcome field
               may exist on a snapshot.
  resolution - appended only once the horizon has strictly passed.
               Carries the realized jump: the max |close move| over the
               horizon bars after t0, read from the SAME cached klines,
               never mutated. Never touches the snapshot line.

Binding rules (the same spine as forward_log):
  1. Strict monotonicity: a snapshot is refused if its timestamp is not
     strictly greater than the last record's timestamp.
  2. Never label at or before observation: a resolution is refused
     unless strictly more than horizon_bars bars exist past the
     snapshot's last_date in the cached klines.
  3. The chain is verified before any append; a broken or tampered
     ledger refuses all writes.

The study (study()) is descriptive: Spearman rank correlation between
the sealed primed_score and the realized jump, top-k vs rest mean jump,
per class and overall. Candidates, not claims; C7 stays sealed. The
multiplicity caveat binds: the sealed top-k are extremes by construction,
so the study asks whether the RANKING carried information, never whether
one winner proves anything.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

LEDGER = Path("logs/board_surprise_ledger.jsonl")
STUDY_MD = Path("paper/research/clue_scan/surprise_study.md")
GENESIS_PREV_SHA256 = "0" * 64
SNAPSHOT_RECORD = "snapshot"
RESOLUTION_RECORD = "resolution"
HORIZON_BARS = 10

ENTRY_FIELDS = (
    "series", "class", "primed_score", "comp_days", "rvol_pct",
    "range_pos", "vol_ratio", "evr_m", "last_date", "data_file",
)


class LedgerError(Exception):
    pass


MEGA_CSV = Path("paper/research/clue_scan/mega_dormancy_table.csv")
BINANCE_KLINES = Path("data/raw/top500_klines")
YAHOO_KLINES = Path("data/raw/mega_klines")


def _mega_data_file(series, venue):
    """The cached klines CSV for a mega-board series (None if unknown)."""
    if venue in ("perp", "spot"):
        p = BINANCE_KLINES / f"{series}.csv"
    elif venue == "yahoo":
        p = YAHOO_KLINES / f"{series.replace('=', '_').replace('^', '')}.csv"
    else:
        return None
    return str(p) if p.exists() else None


def _mega_last_date(data_file):
    if not data_file:
        return None
    try:
        df = pd.read_csv(data_file, usecols=["date"])
        return str(df["date"].iloc[-1]) if len(df) else None
    except Exception:
        return None


def seal_from_mega(mega_csv=MEGA_CSV, k_per_class=20,
                   ledger_path=LEDGER, timestamp_utc_us=None,
                   horizon_bars=HORIZON_BARS):
    """Seal the LIVING board (mega dormancy table) at t0.

    The mega table is what the nightly board_refresh maintains; this
    adapter maps it onto the ledger's entry schema so the sealed-score-
    vs-realized-jump record accumulates EVERY NIGHT while the L2 phase
    waits on data. dormancy_score is sealed as the primed_score field
    (it is the same coil logic, dormancy-weighted); evr_m/vol_ratio are
    absent from the mega schema and sealed as null rather than invented.
    last_date is read from the cached klines (the bar the score was
    computed on) so the horizon gate stays strict.
    """
    mega = pd.read_csv(mega_csv)
    mega["primed"] = mega["primed"].astype(bool)
    entries = []
    for cls, sub in mega[mega["primed"]].groupby("class"):
        top = sub.sort_values(
            "dormancy_score", ascending=False).head(k_per_class)
        for _, r in top.iterrows():
            data_file = _mega_data_file(r["series"], r.get("venue", ""))
            entries.append({
                "series": r["series"], "class": cls,
                "primed_score": float(r["dormancy_score"]),
                "comp_days": int(r["comp_days"]),
                "rvol_pct": float(r["rvol_pct"]),
                "range_pos": float(r["range_pos"]),
                "vol_ratio": None, "evr_m": None,
                "last_date": _mega_last_date(data_file),
                "data_file": data_file,
            })
    entries = [e for e in entries if e["last_date"] and e["data_file"]]
    if not entries:
        raise LedgerError("no primed candidates with resolvable klines")
    record = {
        "type": SNAPSHOT_RECORD,
        "timestamp_utc_us": timestamp_utc_us or _now_us(),
        "horizon_bars": horizon_bars,
        "n_series_on_board": int(len(mega)),
        "board_source": "mega_dormancy_table.csv",
        "entries": entries,
    }
    return _append(record, ledger_path)


def _canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, default=float)


def _record_sha256(record) -> str:
    body = {k: v for k, v in record.items() if k != "sha256"}
    return hashlib.sha256(_canonical_json(body).encode()).hexdigest()


def _now_us():
    return int(time.time() * 1_000_000)


def read_ledger(ledger_path=LEDGER):
    path = Path(ledger_path)
    records = []
    if not path.exists():
        return records
    for line in path.read_text().splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def verify_chain(ledger_path=LEDGER):
    prev = GENESIS_PREV_SHA256
    for rec in read_ledger(ledger_path):
        if rec.get("prev_sha256") != prev:
            raise LedgerError(f"broken chain at record {rec.get('sha256')}")
        if _record_sha256(rec) != rec.get("sha256"):
            raise LedgerError(f"tampered record {rec.get('sha256')}")
        prev = rec["sha256"]
    return True


def _append(record, ledger_path):
    verify_chain(ledger_path)
    records = read_ledger(ledger_path)
    if records:
        if record["timestamp_utc_us"] <= records[-1]["timestamp_utc_us"]:
            raise LedgerError(
                "monotonicity violated: timestamp not strictly greater "
                "than the last record's")
        record["prev_sha256"] = records[-1]["sha256"]
    else:
        record["prev_sha256"] = GENESIS_PREV_SHA256
    record["sha256"] = _record_sha256(record)
    path = Path(ledger_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(_canonical_json(record) + "\n")
    return record


def seal_snapshot(board, k_per_class=20, ledger_path=LEDGER,
                  timestamp_utc_us=None, horizon_bars=HORIZON_BARS):
    """Seal the current top-k eligible candidates per class at t0."""
    entries = []
    for cls, sub in board[board["eligible"]].groupby("class"):
        top = sub.sort_values("primed_score", ascending=False).head(k_per_class)
        for _, r in top.iterrows():
            entries.append({f: (None if pd.isna(r[f]) else r[f])
                            for f in ENTRY_FIELDS})
    if not entries:
        raise LedgerError("no eligible candidates to seal")
    record = {
        "type": SNAPSHOT_RECORD,
        "timestamp_utc_us": timestamp_utc_us or _now_us(),
        "horizon_bars": horizon_bars,
        "n_series_on_board": int(len(board)),
        "entries": entries,
    }
    return _append(record, ledger_path)


def _realized_jump(entry, horizon_bars):
    """Max |close move| over the horizon bars after last_date, or None."""
    path = Path(entry["data_file"])
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "date" not in df.columns or "close" not in df.columns:
        return None
    df = df.dropna(subset=["close"])
    future = df[df["date"] > entry["last_date"]]
    if len(future) < horizon_bars:
        return None
    base = df[df["date"] <= entry["last_date"]]["close"]
    if not len(base):
        return None
    base = float(base.iloc[-1])
    if base <= 0:
        return None
    window = future["close"].to_numpy(float)[:horizon_bars]
    moves = window / base - 1.0
    i = int(np.argmax(np.abs(moves)))
    return {
        "realized_jump": float(abs(moves[i])),
        "jump_direction": "up" if moves[i] > 0 else "down",
    }


def resolve_pending(ledger_path=LEDGER, timestamp_utc_us=None):
    """Append resolutions for every sealed entry whose horizon has passed."""
    verify_chain(ledger_path)
    records = read_ledger(ledger_path)
    resolved_keys = {
        (r.get("snapshot_sha256"), r.get("series"))
        for r in records if r["type"] == RESOLUTION_RECORD}
    out = []
    ts = timestamp_utc_us or _now_us()
    for rec in records:
        if rec["type"] != SNAPSHOT_RECORD:
            continue
        for entry in rec["entries"]:
            key = (rec["sha256"], entry["series"])
            if key in resolved_keys:
                continue
            res = _realized_jump(entry, rec["horizon_bars"])
            if res is None:
                continue
            out.append(_append({
                "type": RESOLUTION_RECORD,
                "timestamp_utc_us": ts,
                "snapshot_sha256": rec["sha256"],
                "series": entry["series"],
                "class": entry["class"],
                "primed_score": float(entry["primed_score"]),
                **res,
            }, ledger_path))
            ts += 1
    return out


def study(ledger_path=LEDGER, study_md=STUDY_MD):
    """Descriptive surprise study: sealed score vs realized jump."""
    verify_chain(ledger_path)
    records = read_ledger(ledger_path)
    rows = [r for r in records if r["type"] == RESOLUTION_RECORD]
    if not rows:
        return {"n_resolved": 0}
    df = pd.DataFrame(rows)
    out = {"n_resolved": len(df), "per_class": {}, "overall": {}}

    def _block(sub):
        rho, p = stats.spearmanr(sub["primed_score"], sub["realized_jump"])
        top5 = sub.nlargest(5, "primed_score")["realized_jump"]
        rest = sub.nsmallest(len(sub) - 5, "primed_score")["realized_jump"]
        return {
            "n": int(len(sub)),
            "spearman_rho": float(rho) if len(sub) >= 3 else None,
            "p_value": float(p) if len(sub) >= 3 else None,
            "mean_jump_top5": float(top5.mean()) if len(top5) else None,
            "mean_jump_rest": float(rest.mean()) if len(rest) else None,
            "median_jump": float(sub["realized_jump"].median()),
        }

    for cls, sub in df.groupby("class"):
        out["per_class"][cls] = _block(sub)
    out["overall"] = _block(df)
    biggest = df.nlargest(10, "realized_jump")[
        ["series", "class", "primed_score", "realized_jump",
         "jump_direction"]]
    out["biggest_surprises"] = biggest.to_dict("records")

    if study_md:
        lines = [
            "# Surprise study - sealed priming scores vs realized jumps",
            "",
            "Descriptive only. The sealed top-k are extremes by construction;",
            "the study asks whether the RANKING carried information.",
            "C7 stays sealed. WHICH WAY is refused by the score; the resolved",
            "direction is recorded, not predicted.",
            "",
            f"Resolved entries: **{len(df)}**",
            "",
            "## Per class",
            "",
            "| class | n | Spearman rho (score vs jump) | p | median jump | mean jump top-5 | mean jump rest |",
            "|---|---|---|---|---|---|---|",
        ]
        for cls, b in out["per_class"].items():
            rho = b["spearman_rho"]
            rho_s = "n/a" if rho is None else f"{rho:.3f}"
            p_s = ("n/a" if b["p_value"] is None
                   else f"{b['p_value']:.3f}")
            top5_s = ("n/a" if b["mean_jump_top5"] is None
                      else f"{b['mean_jump_top5']:.4f}")
            rest_s = ("n/a" if b["mean_jump_rest"] is None
                      else f"{b['mean_jump_rest']:.4f}")
            lines.append(
                f"| {cls} | {b['n']} | {rho_s} | {p_s} | "
                f"{b['median_jump']:.4f} | {top5_s} | {rest_s} |")
        o = out["overall"]
        lines += [
            "",
            "## Whole board",
            "",
            f"n={o['n']}  rho={o['spearman_rho']:.3f} (p={o['p_value']:.4f})  "
            f"median jump={o['median_jump']:.4f}",
            "",
            "## Biggest surprises (realized jump, sealed score)",
            "",
            "| series | class | sealed score | realized jump | direction |",
            "|---|---|---|---|---|",
        ]
        for r in out["biggest_surprises"]:
            lines.append(
                f"| {r['series']} | {r['class']} | {r['primed_score']:.3f} | "
                f"{r['realized_jump']:.4f} | {r['jump_direction']} |")
        Path(study_md).parent.mkdir(parents=True, exist_ok=True)
        Path(study_md).write_text("\n".join(lines) + "\n")
    return out


def main():
    if MEGA_CSV.exists():
        rec = seal_from_mega()
    else:
        from board_heatmap import build_board, save_board
        board = build_board()
        save_board(board)
        rec = seal_snapshot(board)
    print(f"sealed snapshot {rec['sha256'][:12]}: "
          f"{len(rec['entries'])} candidates, "
          f"horizon {rec['horizon_bars']} bars")
    n = resolve_pending()
    print(f"resolved {len(n)} entries past horizon")
    s = study()
    if s.get("n_resolved"):
        o = s["overall"]
        print(f"study: n={o['n']} rho={o['spearman_rho']:.3f} "
              f"(p={o['p_value']:.4f})")


if __name__ == "__main__":
    main()
