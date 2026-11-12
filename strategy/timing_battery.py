"""THE TIMING BATTERY: the prediction work on WHEN - the right
side of the chart only.

Fewer trades, better timing: the crash-zone guideline already
proposes once per episode; this battery measures WHEN the
proposed trade pays, so every candidate can carry a predicted
timing card instead of just an entry:

  TIME-TO-PEAK: after every crash-zone episode entry on
  anchored assets, the week (1..4) in which the forward window's
  maximum favorable point lands - the measured shape of the
  bounce. The candidate card says: "median peak at week X;
  P(positive by week 1) = Y".

  THE REALIZATION CURVE: the fraction of the 4-week move
  realized by each week - does the bounce pay early (front-
  loaded, like the SMH hazard) or late?

  REGION-CONDITIONED TIMING: the same statistics conditioned on
  the SMH region at entry (compression / mid / stress). If
  stress-region crashes pay worse or later, the philosopher's
  stress flag is validated BY MEASUREMENT; if not, the flag is
  honest noise and says so.

Everything strictly causal: entries at the episode cross, the
path measured forward from the entry only - the right side of
the chart, never the left.

Usage (nightly, after market_philosopher):
    python3 timing_battery.py --data-dir ../paper/research/data \\
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from market_philosopher import (ANCHORED, HOLD_WEEKS, WEEK,
                                 ZONE_HI, ZONE_LO,
                                 _weekly_return)
from smh_gradient import _tercile_states
from smh_proof import WARMUP, _series, _weekly_sigma


def _episodes(logc, n):
    """Crash-zone episode entries: the cross into the zone, no
    re-entry while the hold runs (the philosopher's rule)."""
    out = []
    last_entry = -10 ** 9
    for t in range(WARMUP, n - WEEK * HOLD_WEEKS):
        wr = _weekly_return(logc, t)
        prev = _weekly_return(logc, t - 1)
        if (ZONE_LO <= wr < ZONE_HI
                and not ZONE_LO <= prev < ZONE_HI
                and t >= last_entry + WEEK * HOLD_WEEKS):
            last_entry = t
            out.append(t)
    return out


def _path_stats(logc, t):
    """The forward path from the entry, in weekly steps: the
    running return each week, the week of the peak, and the
    realization fractions."""
    entry = float(logc[t])
    run = []
    for w in range(1, HOLD_WEEKS + 1):
        run.append(float(logc[t + WEEK * w] - entry))
    peak_week = int(np.argmax(run)) + 1
    total = run[-1]
    realized = [round(r / total, 3) if abs(total) > 1e-9
                else None for r in run[:-1]]
    return run, peak_week, realized


def run_timing(data_dir: Path) -> dict:
    by_region = {"compression": [], "mid": [], "stress": []}
    for name, c, v in _series(data_dir):
        if name not in ANCHORED:
            continue
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        for t in _episodes(logc, len(logc)):
            region = ("compression" if states[t] == 0
                      else "mid" if states[t] == 1 else "stress")
            run, peak_week, realized = _path_stats(logc, t)
            by_region[region].append({
                "run": run, "peak_week": peak_week,
                "realized": realized})

    def block(rows):
        if not rows:
            return {"n": 0}
        peaks = [r["peak_week"] for r in rows]
        wk1 = [r["run"][0] for r in rows]
        wk4 = [r["run"][-1] for r in rows]
        real2 = [r["realized"][1] for r in rows
                 if r["realized"][1] is not None]
        return {
            "n": len(rows),
            "median_peak_week": round(float(
                np.median(peaks)), 1),
            "p_positive_week1": round(float(np.mean(
                np.array(wk1) > 0)), 3),
            "p_positive_week4": round(float(np.mean(
                np.array(wk4) > 0)), 3),
            "median_week4": round(float(np.median(wk4)), 4),
            "median_fraction_realized_by_week2": (round(float(
                np.median(real2)), 3) if real2 else None),
        }

    pooled = block([r for rs in by_region.values() for r in rs])
    regional = {k: block(v) for k, v in by_region.items()}

    # the region verdict, pre-declared: the stress flag is
    # validated only if stress reads clearly worse than the
    # pooled (lower p_positive_week4 by a margin), else honest
    # noise
    stress = regional.get("stress", {})
    comp = regional.get("compression", {})
    stress_ok = stress.get("n", 0) >= 20
    stress_worse = (stress_ok and
                    stress.get("p_positive_week4", 1.0)
                    < pooled.get("p_positive_week4", 1.0) - 0.05)
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "protocol": "the timing prediction for the crash-zone "
            "guideline: time-to-peak, the realization curve, and "
            "the region conditioning - strictly forward from the "
            "entry, the right side of the chart only",
        "pooled": pooled,
        "by_region": regional,
        "region_verdict": {
            "stress_flag_validated": bool(stress_worse),
            "statement": ("stress-region crash episodes pay "
                          "clearly worse: the philosopher's "
                          "stress flag is validated by "
                          "measurement" if stress_worse else
                          "the stress flag is NOT validated by "
                          "the timing data at this sample - it "
                          "stays a context flag, honestly "
                          "unproven"),
        },
        "candidate_timing_card": {
            "median_peak_week": pooled.get("median_peak_week"),
            "p_positive_week1": pooled.get("p_positive_week1"),
            "statement": ("every LONG_CANDIDATE carries this "
                          "card: when the measured record says "
                          "the bounce pays, and with what "
                          "probability - the prediction on "
                          "timing, on the record"),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="The timing battery (the WHEN prediction)")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_timing(args.data_dir)
    dest = args.research_dir / "timing_battery.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    p = r["pooled"]
    print(f"timing battery -> {dest} "
          f"(pooled n {p.get('n')}, median peak week "
          f"{p.get('median_peak_week')}, "
          f"P(+ by week 1) {p.get('p_positive_week1')}, "
          f"P(+ by week 4) {p.get('p_positive_week4')}; "
          f"stress flag validated: "
          f"{r['region_verdict']['stress_flag_validated']})")


if __name__ == "__main__":
    main()
