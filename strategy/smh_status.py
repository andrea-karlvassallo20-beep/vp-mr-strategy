"""THE MACHINE'S LIVE POSITION (charter v3, section 6): the
status reading - the operational replacement for counting waves.

The charter's instrument: 'the status command reports the current
clock region, the current spell's age in weeks against the measured
dwell distribution (median, mean, max), and the current state
spell's age.' What it does NOT do is convert spell age into a
forecast: age is descriptive context; rows are logged only at clock
entries, per the protocol (doctrine rule 2). This module enforces
that boundary structurally - it outputs no probability, no forecast,
no ranking by age. It reads position only.

Dwell distributions are measured from the full pooled history:
every completed spell of each region, in weeks. The live spell's
age is placed against its own region's distribution - strictly
causal (trailing spells and the running spell's age to date).

Usage (nightly, after smh_gradient):
    python3 smh_status.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import WEEK, _tercile_states
from smh_proof import WARMUP, _series, _weekly_sigma

REGIONS = {0: "compression", 1: "mid", 2: "stress"}


def _spells(states: np.ndarray) -> list:
    """Completed spells as (region, length_bars) from the state
    series, plus the running spell at the data edge. Unassigned
    bars (-1) are gaps: a gap ends the running spell and the next
    assigned bar starts a new one."""
    out = []
    start = None
    region = None
    for t in range(WARMUP, len(states)):
        if states[t] < 0:                  # gap: close any spell
            if start is not None and t > start:
                out.append((int(region), t - start))
            start = region = None
            continue
        if start is None:
            start, region = t, states[t]
        elif states[t] != region:
            out.append((int(region), t - start))
            start, region = t, states[t]
    running = ((int(region), len(states) - start)
               if start is not None else None)
    return out, running


def run_status(data_dir: Path) -> dict:
    dwell = {0: [], 1: [], 2: []}
    rows = []
    counts = {"compression": 0, "mid": 0, "stress": 0,
              "unassigned": 0}
    for name, c, v in _series(data_dir):
        sig = _weekly_sigma(np.log(c))
        states = _tercile_states(sig)
        completed, running = _spells(states)
        for region, length in completed:
            dwell[region].append(length)
        if running is None:
            counts["unassigned"] += 1
            continue
        region, age_bars = running
        counts[REGIONS[region]] += 1
        rows.append({
            "ticker": name,
            "region": REGIONS[region],
            "spell_age_weeks": round(age_bars / WEEK, 1),
        })
    dist = {}
    for r, lens in dwell.items():
        if lens:
            dist[REGIONS[r]] = {
                "n_spells": len(lens),
                "median_weeks": round(float(
                    np.median(lens)) / WEEK, 1),
                "mean_weeks": round(float(
                    np.mean(lens)) / WEEK, 1),
                "max_weeks": round(float(
                    np.max(lens)) / WEEK, 1),
            }
    region_order = {"compression": 0, "mid": 1, "stress": 2}
    rows.sort(key=lambda x: (region_order[x["region"]],
                             -x["spell_age_weeks"]))
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "doctrine_note": "spell age is descriptive context, not a "
            "forecast: rows are logged only at clock entries, and "
            "this reading converts age into no probability at all",
        "counts": counts,
        "dwell_distribution_weeks": dist,
        "positions": rows,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH machine live position (status reading)")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_status(args.data_dir)
    dest = args.research_dir / "smh_status.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    c = r["counts"]
    print(f"smh status -> {dest} "
          f"(compression {c['compression']}, mid {c['mid']}, "
          f"stress {c['stress']}, unassigned {c['unassigned']})")


if __name__ == "__main__":
    main()
