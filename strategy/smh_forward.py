"""THE SMH FORWARD SCORING PROTOCOL (charter v2, sections 9, 12, 14).

The framework is design-complete; what remains is episodes. This
module is the instrument that produces them:

  DRAFT:   at each nightly decision close, every market that CROSSES
           into compression (or into stress, the mirror edge) gets
           one forecast row, logged in advance: the probability of
           the anticipated event (a >= 2.5 sigma_w week within 12
           weeks; de-stress within 12 weeks on the stress side),
           computed from the frozen KM baseline and the Cox model.
  RESOLVE: as windows complete, each row is scored against the
           outcome - event (1), quiet spell end or 12 quiet weeks
           (0), or still open at the data edge.
  SCORE:   Brier, log score, reliability bins on every resolved row.
  KILL:    the charter's pre-declared kill lines (section 14.6):
           the occurrence claim dies in public if, at 10/20/40/60
           scored compression rows, the event count is at or below
           3/8/19/31.

Doctrine rules enforced structurally (rule 2): rows exist only at
clock entries, only on the decision cadence, never twice for the
same entry, never revised after the fact - resolution only fills
the outcome a row already declared.

Usage (nightly, after smh_hazard):
    python3 smh_forward.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_hazard import (EVENT_SIG, MOM_BARS, build_episodes,
                        cox_fit, kaplan_meier)
from smh_proof import WARMUP, _series, _weekly_sigma

HORIZON = 60          # 12 weeks of daily bars (charter section 14)
KILL_LINES = {10: 3, 20: 8, 40: 19, 60: 31}


def _tercile_states(sig: np.ndarray) -> np.ndarray:
    """Expanding-tercile clock states: 0 compression, 1 mid,
    2 high - strictly causal, identical to the hazard battery."""
    n = len(sig)
    states = np.full(n, -1, dtype=int)
    for t in range(WARMUP, n):
        hist = sig[WARMUP:t + 1][sig[WARMUP:t + 1] > 0]
        if len(hist) < 60 or sig[t] <= 0:
            continue
        q1, q2 = np.quantile(hist, [1 / 3, 2 / 3])
        states[t] = 0 if sig[t] <= q1 else (
            1 if sig[t] <= q2 else 2)
    return states


def build_stress_episodes(data_dir: Path) -> list:
    """Stress-entry episodes for the mirror clock: entry on the
    cross above the frozen high cut; the EVENT is de-stress (state
    exit); censoring at data end."""
    eps = []
    for name, c, v in _series(data_dir):
        sig = _weekly_sigma(np.log(c))
        states = _tercile_states(sig)
        n = len(c)
        t = WARMUP
        while t < n - 1:
            if states[t] == 2 and states[t - 1] != 2:
                k = t + 1
                event = 0
                while k < n:
                    if states[k] != 2:
                        event = 1
                        break
                    k += 1
                eps.append({
                    "ticker": name,
                    "momentum": 0.0,
                    "sigma_pct": 0.5,
                    "duration": int(min(k - t, n - 1 - t)),
                    "event": event,
                })
                t = k + 1
            else:
                t += 1
    return eps


def _baseline_surv(episodes: list, horizon: int) -> float:
    """KM baseline survival at the horizon (probability the event
    has NOT yet happened by `horizon` bars after entry)."""
    km = kaplan_meier(episodes)
    s = 1.0
    for row in km:
        if row["t"] <= horizon:
            s = row["survival"]
        else:
            break
    return s


def _entry_covariates(logc: np.ndarray, sig: np.ndarray,
                      t: int) -> tuple:
    mom = float(logc[t] - logc[max(0, t - MOM_BARS)])
    hist = sig[WARMUP:t + 1][sig[WARMUP:t + 1] > 0]
    sig_pct = (float(np.mean(hist <= sig[t]))
               if len(hist) else 0.5)
    return mom, sig_pct


def draft_and_resolve(data_dir: Path, research_dir: Path) -> dict:
    """One nightly pass: load the log, resolve open rows against
    the updated data, draft new rows at tonight's clock entries,
    score everything resolved, and read the kill lines. The log is
    append-only: existing rows keep their logged probability and
    gain only their outcome."""
    dest = research_dir / "smh_forward.json"
    log = json.loads(dest.read_text()) if dest.exists() else {
        "rows": []}
    rows = log.get("rows", [])

    # frozen baselines from the full history (recomputed nightly,
    # definitions frozen: KM on compression / stress episodes)
    comp_eps = build_episodes(data_dir)
    stress_eps = build_stress_episodes(data_dir)
    s0_comp = _baseline_surv(comp_eps, HORIZON)
    s0_stress = _baseline_surv(stress_eps, HORIZON)
    cox = cox_fit(comp_eps) if len(comp_eps) >= 200 else None

    open_rows = [r for r in rows if r["status"] == "open"]
    still_open_keys = set()

    # --- RESOLVE (fill outcomes; never revise the forecast) -------
    snapshots = {}
    for name, c, v in _series(data_dir):
        snapshots[name] = (
            np.log(c),
            _weekly_sigma(np.log(c)),
            _tercile_states(_weekly_sigma(np.log(c))),
        )
    for r in open_rows:
        key = (r["ticker"], r["kind"])
        if r["ticker"] not in snapshots:
            r["status"] = "ORPHANED"
            continue
        logc, sig, states = snapshots[r["ticker"]]
        n = len(logc)
        e = r["entry_index"]
        thr = EVENT_SIG * r["entry_sigma_w"]
        if r["kind"] == "compression":
            outcome = None
            for k in range(e + 1, min(e + 1 + HORIZON, n)):
                if abs(logc[k] - logc[e]) >= thr:
                    outcome = 1
                    r["resolved_index"] = k
                    break
                if states[k] != 0:
                    outcome = 0          # spell ended, quiet
                    r["resolved_index"] = k
                    break
            if outcome is None and e + HORIZON < n - 1:
                outcome = 0              # 12 quiet weeks
                r["resolved_index"] = e + HORIZON
            if outcome is not None:
                r["outcome"] = outcome
                r["status"] = "resolved"
            else:
                still_open_keys.add(key)
        else:  # stress mirror: event = de-stress
            outcome = None
            for k in range(e + 1, min(e + 1 + HORIZON, n)):
                if states[k] != 2:
                    outcome = 1
                    r["resolved_index"] = k
                    break
            if outcome is None and e + HORIZON < n - 1:
                outcome = 0
                r["resolved_index"] = e + HORIZON
            if outcome is not None:
                r["outcome"] = outcome
                r["status"] = "resolved"
            else:
                still_open_keys.add(key)

    # --- DRAFT (tonight's clock entries; one row per entry) --------
    drafted = 0
    for name, c, v in _series(data_dir):
        logc, sig, states = snapshots[name]
        t = len(logc) - 1
        if t < WARMUP + 1 or states[t] < 0 or states[t - 1] < 0:
            continue
        kind = None
        if states[t] == 0 and states[t - 1] != 0:
            kind = "compression"
        elif states[t] == 2 and states[t - 1] != 2:
            kind = "stress"
        if kind is None:
            continue
        if (name, kind) in still_open_keys:
            continue                    # never twice for one entry
        if any(r["ticker"] == name and r["kind"] == kind
               and r["entry_index"] == t for r in rows):
            continue                    # idempotent on re-run
        mom, sig_pct = _entry_covariates(logc, sig, t)
        if kind == "compression":
            rel = 1.0
            if cox is not None:
                z = (np.array([mom, sig_pct])
                     - np.array(cox["_mu"])) / np.array(cox["_sd"])
                rel = float(np.exp(np.clip(
                    float(np.array(cox["_beta_raw"]) @ z), -5, 5)))
            p = float(1.0 - s0_comp ** rel)
        else:
            p = float(1.0 - s0_stress)
        rows.append({
            "ticker": name,
            "kind": kind,
            "entry_index": int(t),
            "entry_close": round(float(c[t]), 6),
            "entry_sigma_w": round(float(sig[t]), 6),
            "momentum_20": round(mom, 4),
            "sigma_pct": round(sig_pct, 4),
            "forecast_p": round(min(max(p, 1e-4), 0.9999), 4),
            "logged_utc": datetime.now(timezone.utc).isoformat(
                timespec="seconds"),
            "status": "open",
            "outcome": None,
        })
        drafted += 1

    # --- SCORE every resolved row ----------------------------------
    resolved = [r for r in rows if r["status"] == "resolved"]
    comp_res = [r for r in resolved if r["kind"] == "compression"]
    n_events = sum(r["outcome"] for r in comp_res)
    brier = logscore = None
    reliability = []
    if resolved:
        ps = np.array([r["forecast_p"] for r in resolved])
        ys = np.array([r["outcome"] for r in resolved], dtype=float)
        brier = float(np.mean((ps - ys) ** 2))
        logscore = float(np.mean(
            ys * np.log(ps) + (1 - ys) * np.log(1 - ps)))
        for lo in [0.0, 0.2, 0.4, 0.6, 0.8]:
            m = (ps >= lo) & (ps < lo + 0.2)
            if m.sum() >= 3:
                reliability.append({
                    "bin": f"{lo:.1f}-{lo + 0.2:.1f}",
                    "n": int(m.sum()),
                    "mean_p": round(float(ps[m].mean()), 3),
                    "observed": round(float(ys[m].mean()), 3),
                })

    # --- KILL LINES (pre-declared, charter section 14.6) -----------
    n_comp = len(comp_res)
    kill_status = "ALIVE"
    triggered = None
    for n_rows, min_events in sorted(KILL_LINES.items()):
        if n_comp >= n_rows and n_events <= min_events:
            kill_status = "DEAD"
            triggered = {"at_rows": n_rows,
                         "events": int(n_events),
                         "line": min_events}
            break
    next_line = next(
        ({"at_rows": k, "line": v} for k, v in sorted(
            KILL_LINES.items()) if k > n_comp), None)

    result = {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "protocol": "SMH charter v2 sections 9/12/14: rows logged "
            "in advance at clock entries only; resolved against "
            "outcomes; Brier/log-scored; kill lines pre-declared.",
        "baseline": {
            "n_compression_episodes": len(comp_eps),
            "n_stress_episodes": len(stress_eps),
            "survival_12w_compression": round(s0_comp, 4),
            "survival_12w_stress": round(s0_stress, 4),
            "cox_used": cox is not None,
        },
        "rows": rows,
        "counts": {
            "drafted_tonight": drafted,
            "open": sum(1 for r in rows if r["status"] == "open"),
            "resolved": len(resolved),
            "compression_scored": n_comp,
            "compression_events": int(n_events),
        },
        "scores": {
            "brier": round(brier, 4) if brier is not None else None,
            "log_score": (round(logscore, 4)
                          if logscore is not None else None),
            "reliability": reliability,
        },
        "kill_lines": {
            "status": kill_status,
            "triggered": triggered,
            "next_line": next_line,
            "table": {str(k): v for k, v in KILL_LINES.items()},
        },
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH forward scoring protocol")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = draft_and_resolve(args.data_dir, args.research_dir)
    dest = args.research_dir / "smh_forward.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    c = r["counts"]
    print(f"smh forward -> {dest} "
          f"(drafted {c['drafted_tonight']}, open {c['open']}, "
          f"resolved {c['resolved']}, "
          f"kill-line status {r['kill_lines']['status']})")


if __name__ == "__main__":
    main()
