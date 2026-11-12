"""THE AVFI PRECURSOR BATTERY: incremental information, the
decisive test.

The charter's layer-3 question, asked the only way it can be
answered: does ANY AVFI v4 configuration raise the hazard of
the charter's significant week (|r1| >= 2.5 sigma_w within 12
weeks) BEYOND the SMH clock's own compression table?

AVFI must demonstrate INCREMENTAL information beyond the SMH
state before it earns a role in the strategy (the standing
rule). This battery measures, per configuration, with the
same Kaplan-Meier + Greenwood machinery as the clock study:

  CELLS (all causal, all at CROSSES into the condition, the
  charter's entry convention - never every in-condition bar):
    - deep_stretch_down: causal stretch-z <= -2 (the v4
      bottom stretch condition)
    - deep_stretch_up: z >= +2 (the v4 top stretch condition)
    - confirmed_bottom_recent: a v4 confirmed bottom fired
      within the last 3 bars
    - confirmed_top_recent: a v4 confirmed top within 3 bars
    - z_flip_up: z crossed from <= -1 to > 0 (a transition)
    - compression: the clock baseline (state 0, the
      measured champion)
    - compression_and_stretch: state 0 AND z <= -1 - THE
      INCREMENTAL QUESTION: does adding AVFI stretch to the
      clock raise the hazard beyond the clock alone?
    - climatology: the do-nothing counterfactual (any week)

  VERDICTS, honest either way:
    - each cell vs climatology (band overlap)
    - THE INCREMENTAL VERDICT: compression_and_stretch vs
      compression, bands must be disjoint for AVFI to earn
      hazard content beyond the clock - and even then it is
      design-sample, flagged until forward-scored (doctrine
      rule 5)

Usage (nightly, after smh_gradient):
    python3 avfi_precursor.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import (HORIZON, WEEK, _tercile_states,
                          climatology_clock,
                          first_significant_week, km_greenwood,
                          _weekly_sigma)
from smh_proof import WARMUP, _series
from tops_bottoms_backtest import detect_events
from v4_study import causal_z

STRETCH = 2.0            # the v4 deep-stretch threshold
RECENT = 3               # bars for "confirmed event fired recently"
FLIP_LO = -1.0           # the z-flip transition threshold


def run_avfi_precursor(data_dir: Path) -> dict:
    """All cells, measured against the clock and the
    counterfactual."""
    cells = {}
    for name, c, v in _series(data_dir):
        if len(c) < WARMUP + HORIZON + WEEK + 5:
            continue
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        z = causal_z(c)
        _, _, bottoms, tops = detect_events(c, v)
        bset = set(int(b) for b in bottoms)
        tset = set(int(x) for x in tops)
        universe = cells.setdefault(
            name, (logc, sig, states, z, bset, tset))

    def pooled_clock(condition) -> dict:
        durations, events = [], []
        for name, (logc, sig, states, z, bset, tset) \
                in cells.items():
            prev = False
            for t in range(WARMUP + 1,
                           len(logc) - WEEK):
                cur = condition(t, logc=logc, sig=sig,
                                states=states, z=z,
                                bset=bset, tset=tset)
                if cur and not prev and sig[t] > 0:
                    off = first_significant_week(
                        logc, sig, t)
                    # the frozen encoding: >0 = event at
                    # that offset; -1 = window completed
                    # quietly; <0 (not -1) = censored at the
                    # data edge; 0 = no window (excluded)
                    if off > 0:
                        durations.append(off)
                        events.append(1)
                    elif off == -1:
                        durations.append(HORIZON)
                        events.append(0)
                    elif off < 0:
                        durations.append(-off)
                        events.append(0)
                prev = cur
        d = np.array(durations, dtype=int)
        e = np.array(events, dtype=int)
        if len(d) < 10:
            return {"n": int(len(d)),
                    "verdict": "INSUFFICIENT_ENTRIES"}
        return km_greenwood(d, e, HORIZON)

    conds = {
        "deep_stretch_down":
            lambda t, **kw: kw["z"][t] <= -STRETCH,
        "deep_stretch_up":
            lambda t, **kw: kw["z"][t] >= STRETCH,
        "confirmed_bottom_recent":
            lambda t, **kw: any(t - RECENT <= b <= t
                                for b in kw["bset"]),
        "confirmed_top_recent":
            lambda t, **kw: any(t - RECENT <= x <= t
                                for x in kw["tset"]),
        "z_flip_up":
            lambda t, **kw: (kw["z"][t] > 0
                             and t >= WEEK
                             and kw["z"][t - WEEK]
                             <= FLIP_LO),
        "compression":
            lambda t, **kw: kw["states"][t] == 0,
        "compression_and_stretch":
            lambda t, **kw: (kw["states"][t] == 0
                             and kw["z"][t] <= FLIP_LO),
    }
    measured = {k: pooled_clock(fn) for k, fn in
                 conds.items()}
    measured["climatology"] = climatology_clock(data_dir)

    comp = measured.get("compression", {})
    incr = measured.get("compression_and_stretch",
                        {})

    def cell_verdict(key):
        c = measured.get(key, {})
        if "cum_event_12w" not in c:
            return "INSUFFICIENT_ENTRIES"
        cl = measured.get("climatology", {})
        if "cum_event_12w" not in cl:
            return "INSUFFICIENT_CLIMATOLOGY"
        disjoint = (c["ci95_lo"]
                    > cl.get("ci95_hi", 1.0))
        above = c["cum_event_12w"] > \
            cl.get("cum_event_12w", 1.0)
        if disjoint and above:
            return (f"SEPARATES FROM CLIMATOLOGY "
                    f"(cum {c['cum_event_12w']} "
                    f"[{c['ci95_lo']}, {c['ci95_hi']}] vs "
                    f"climatology {cl['cum_event_12w']} "
                    f"[{cl['ci95_lo']}, {cl['ci95_hi']}]) - "
                    f"design-sample, flagged until "
                    f"forward-scored")
        if above:
            return (f"READS ABOVE CLIMATOLOGY BUT THE BANDS "
                    f"OVERLAP (cum {c['cum_event_12w']} "
                    f"[{c['ci95_lo']}, {c['ci95_hi']}] vs "
                    f"climatology {cl['cum_event_12w']} "
                    f"[{cl['ci95_lo']}, {cl['ci95_hi']}]) - "
                    f"no separation claim")
        return (f"DOES NOT BEAT CLIMATOLOGY (cum "
                f"{c['cum_event_12w']} vs "
                f"{cl.get('cum_event_12w')}) - no "
                f"event-hazard information")

    incremental = "INSUFFICIENT_ENTRIES"
    if "cum_event_12w" in incr \
            and "cum_event_12w" in comp:
        disjoint = (incr["ci95_lo"] > comp["ci95_hi"])
        if disjoint:
            incremental = (
                f"AVFI EARNS INCREMENTAL HAZARD CONTENT, "
                f"DESIGN SAMPLE: compression AND stretch "
                f"give cum {incr['cum_event_12w']} "
                f"[{incr['ci95_lo']}, {incr['ci95_hi']}] "
                f"vs the clock alone "
                f"{comp['cum_event_12w']} "
                f"[{comp['ci95_lo']}, {comp['ci95_hi']}] - "
                f"the bands are disjoint; flagged until "
                f"forward-scored (doctrine rule 5)")
        elif incr["cum_event_12w"] > comp["cum_event_12w"]:
            incremental = (
                f"NO INCREMENTAL CLAIM: adding AVFI stretch "
                f"to the clock reads higher ({incr['cum_event_12w']} "
                f"vs {comp['cum_event_12w']}) but the bands "
                f"OVERLAP - the clock already carries the "
                f"hazard; AVFI stays the read, not the "
                f"trigger")
        else:
            incremental = (
                f"AVFI ADDS NOTHING TO THE CLOCK: "
                f"compression AND stretch reads "
                f"{incr['cum_event_12w']} vs the clock alone "
                f"{comp['cum_event_12w']} - the standing "
                f"verdict stands: AVFI describes regimes, "
                f"it does not predict the event")

    result = {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "question": ("does any AVFI v4 configuration "
                     "raise the event hazard BEYOND the SMH "
                     "clock? (entries at crosses into each "
                     "condition, the charter's convention)"),
        "cells": measured,
        "cell_verdicts": {k: cell_verdict(k)
                          for k in conds
                          if k != "compression"},
        "incremental_verdict": incremental,
        "note": "KM+Greenwood, the charter's frozen event, "
                "all cells at crosses; Bonferroni honesty: "
                "seven cells at 95% each, no promotion "
                "without band disjointness AND forward "
                "scoring; design sample",
    }
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="AVFI precursor battery: incremental "
                    "information beyond the clock")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_avfi_precursor(args.data_dir)
    dest = args.research_dir / "avfi_precursor.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    print(f"avfi precursor battery -> {dest}")
    for k, v in r["cells"].items():
        print(f"  {k}: n={v.get('n')} "
              f"cum={v.get('cum_event_12w')} "
              f"[{v.get('ci95_lo')}, {v.get('ci95_hi')}]")
    print(f"incremental: {r['incremental_verdict']}")


if __name__ == "__main__":
    main()
