"""THE SMH FORWARD SCORING PROTOCOL (charter v3, sections 9, 12, 14).

The framework is design-complete; what remains is episodes. This
module is the instrument that produces them:

  DRAFT:   at each nightly decision close, every market that CROSSES
           into compression (or into stress, the mirror edge) gets
           one forecast row, logged in advance: the probability of
           the anticipated event - THE CHARTER'S FROZEN EVENT: a
           significant week, |r1| >= 2.5 sigma_w at entry, within 12
           weeks (de-stress within 12 weeks on the stress side) -
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

CORRECTION RECORD (doctrine rule 6, dated 12 Nov 2026): the first
draft of this instrument defined the event as a cumulative 60-bar
move from the entry close. The charter's frozen event is a
SIGNIFICANT WEEK (|r1| >= 2.5 sigma_w). The definition was corrected
before any row resolved; the correction is recorded in the log, and
the 30 open rows drafted under the old definition carry their
re-based forecast under the corrected one.

Usage (nightly, after smh_gradient):
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
from smh_gradient import (HORIZON, _clock_for_region,
                          _tercile_states,
                          first_significant_week)
from smh_hazard import MOM_BARS, cox_fit
from smh_proof import WARMUP, _series, _weekly_sigma

KILL_LINES = {10: 3, 20: 8, 40: 19, 60: 31}

CORRECTIONS = [{
    "date": "2026-11-12",
    "note": "Event definition corrected to the charter's frozen "
            "form (a significant week, |r1| >= 2.5 sigma_w at "
            "entry, within 12 weeks) from the earlier cumulative "
            "60-bar move. Corrected before any row resolved; open "
            "rows re-based under the corrected definition.",
}]


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
    from smh_hazard import kaplan_meier
    km = kaplan_meier(episodes)
    s = 1.0
    for row in km:
        if row["t"] <= horizon:
            s = row["survival"]
        else:
            break
    return s


def build_compression_episodes(data_dir: Path) -> list:
    """Compression-entry episodes under the charter's frozen event
    (first significant week within 12), entry-anchored: the armed
    clock keeps running after the region read changes. Censoring at
    the data edge only. Covariates strictly causal at entry."""
    eps = []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        for t in range(WARMUP + 1, len(c) - 1):
            if states[t] == 0 and states[t - 1] != 0:
                o = first_significant_week(logc, sig, t)
                if o > 0:
                    dur, ev = o, 1
                elif o == -1:
                    dur, ev = HORIZON, 0
                elif o < 0:
                    dur, ev = -o, 0
                else:
                    continue
                mom = float(logc[t]
                            - logc[max(0, t - MOM_BARS)])
                hist = sig[WARMUP:t + 1][
                    sig[WARMUP:t + 1] > 0]
                sig_pct = (float(np.mean(hist <= sig[t]))
                           if len(hist) else 0.5)
                eps.append({
                    "ticker": name,
                    "momentum": mom,
                    "sigma_pct": sig_pct,
                    "duration": int(dur),
                    "event": ev,
                })
    return eps


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
    corrections = log.get("corrections", [])

    # frozen baselines from the full history (recomputed nightly,
    # definitions frozen: the charter's significant-week event)
    comp_eps = build_compression_episodes(data_dir)
    stress_eps = build_stress_episodes(data_dir)
    comp_clock = _clock_for_region(data_dir, 0)
    p_base_comp = comp_clock["cum_event_12w"]
    s0_stress = _baseline_surv(stress_eps, HORIZON)
    cox = cox_fit(comp_eps) if len(comp_eps) >= 200 else None

    open_rows = [r for r in rows if r["status"] == "open"]
    still_open_keys = set()

    # --- RESOLVE (fill outcomes; never revise the forecast) -------
    snapshots = {}
    for name, c, v in _series(data_dir):
        sig = _weekly_sigma(np.log(c))
        snapshots[name] = (
            np.log(c), sig, _tercile_states(sig))
    for r in open_rows:
        key = (r["ticker"], r["kind"])
        if r["ticker"] not in snapshots:
            r["status"] = "ORPHANED"
            continue
        # the dated correction: rows drafted under the old
        # cumulative-move definition are re-based (pre-resolution)
        # to the charter's significant-week forecast, once, on
        # record (doctrine rule 6)
        if r.get("definition") != "sigweek":
            if r["kind"] == "compression":
                rel = 1.0
                if cox is not None:
                    z = (np.array([r["momentum_20"],
                                   r["sigma_pct"]])
                         - np.array(cox["_mu"])) \
                        / np.array(cox["_sd"])
                    rel = float(np.exp(np.clip(
                        float(np.array(cox["_beta_raw"]) @ z),
                        -5, 5)))
                r["forecast_p"] = round(min(max(
                    1.0 - (1.0 - p_base_comp) ** rel,
                    1e-4), 0.9999), 4)
            else:
                r["forecast_p"] = round(min(max(
                    1.0 - s0_stress, 1e-4), 0.9999), 4)
            r["definition"] = "sigweek"
            r["rebased_utc"] = datetime.now(timezone.utc).isoformat(
                timespec="seconds")
        logc, sig, states = snapshots[r["ticker"]]
        n = len(logc)
        e = r["entry_index"]
        if r["kind"] == "compression":
            o = first_significant_week(logc, sig, e)
            if o > 0:
                r["outcome"] = 1
                r["resolved_index"] = e + o
                r["status"] = "resolved"
            elif o == -1:
                r["outcome"] = 0      # 12 quiet weeks
                r["resolved_index"] = e + HORIZON
                r["status"] = "resolved"
            elif o < 0:
                # censored: data edge inside the window; also check
                # the quiet spell-end abort before the edge
                spell_end = None
                for k in range(e + 1, min(e + 1 + HORIZON, n)):
                    if states[k] != 0:
                        spell_end = k
                        break
                if spell_end is not None:
                    r["outcome"] = 0
                    r["resolved_index"] = spell_end
                    r["status"] = "resolved"
                else:
                    still_open_keys.add(key)
            else:
                # no window exists yet (entry at the data edge):
                # the row stays open - the window has not begun
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
            p = float(1.0 - (1.0 - p_base_comp) ** rel)
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
            "definition": "sigweek",
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
        "protocol": "SMH charter v3 sections 9/12/14: rows logged "
            "in advance at clock entries only; the event is the "
            "charter's frozen significant week (|r1| >= 2.5 "
            "sigma_w at entry, within 12 weeks); resolved against "
            "outcomes; Brier/log-scored; kill lines pre-declared.",
        "corrections": corrections + CORRECTIONS
        if not corrections else corrections,
        "baseline": {
            "n_compression_episodes": len(comp_eps),
            "n_stress_episodes": len(stress_eps),
            "p_significant_week_12w_compression": p_base_comp,
            "compression_ci95": [comp_clock["ci95_lo"],
                                 comp_clock["ci95_hi"]],
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
