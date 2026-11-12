"""THE TRADE-INEVITABLES: the additions to the rule set, measured -
the structural conditions that construct the lowest-drawdown,
highest risk-reward exposures the data permits.

Three new rules, each oriented at trade construction, each
measured with the programme's honesty conventions (medians,
winsorized tails, STRUCTURAL/FOLKLORE verdicts):

  T1. THE ARMED CLOCK'S DRAWDOWN PROFILE: while the 12-week armed
      window runs after a compression entry, what is the WORST
      adverse excursion (in entry-sigma_w units) before the event
      arrives - versus the size of the event itself (median
      first-event overshoot ~1.4x the 2.5-sigma bar)? If the
      median waiting drawdown is a small fraction of the median
      event size, the event-capture structure is high-RR BY
      CONSTRUCTION: risk a little, wait for the inevitable
      expansion. This is the measured form of "the lowest
      drawdown trade the hypothesis permits."

  T2. THE CRASH-DEPTH GRADIENT (the nuclear-red rule, measured):
      on ANCHORED assets (the majors that cannot go to zero and
      mean-revert after panics), the forward 4-week return after
      a weekly crash, bucketed by depth: -5..-7.5%, -7.5..-10%,
      -10..-15%, and the nuclear-red -15% and worse. If deeper
      crashes buy higher forward medians, the depth gradient is
      STRUCTURAL and the nuclear-red buy is the highest-RR
      defined-risk entry the daily grain can measure.

  T3. THE POST-EVENT CALM: after a significant week (>= 2.5
      sigma_w), the measured probability that the FOLLOWING week
      is quieter than baseline - the stress clock's "decay by
      calm" at the entry grain. This is the re-entry window: the
      market's recovery is in its boredom, and the measured
      calm probability is what makes the post-event re-entry a
      low-drawdown one.

Usage (nightly, after smh_bayes):
    python3 trade_inevitables.py --data-dir ../paper/research/data \\
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import (HORIZON, _tercile_states,
                          first_significant_week)
from smh_proof import (EVENT_SIG, WARMUP, _series,
                       _weekly_sigma)

WEEK = 5
ANCHORED = ("BTCUSD", "ETHUSD", "GCF", "CLF", "HGF", "SIF",
            "GSPC", "DJI", "IXIC", "RUT")
CRASH_BUCKETS = ((-0.075, -0.05), (-0.10, -0.075),
                 (-0.15, -0.10), (-1.0, -0.15))
FWD_WEEKS = 4          # forward window in weeks
WINSOR = 0.05          # winsorize forward returns at 5%/95%


def _winsorize(x):
    x = np.asarray(x, dtype=float)
    if not len(x):
        return x
    lo, hi = np.quantile(x, [WINSOR, 1 - WINSOR])
    return np.clip(x, lo, hi)


def claim_t1(data_dir: Path) -> dict:
    """The armed clock's drawdown profile: waiting MAE vs event
    size, in entry-sigma_w units."""
    maes, ev_sizes = [], []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        for t in range(WARMUP + 1, len(c) - 1):
            if states[t] == 0 and states[t - 1] != 0:
                thr = EVENT_SIG * sig[t]
                if thr <= 0:
                    continue
                o = first_significant_week(logc, sig, t)
                if o <= 0:
                    continue
                k = t + o
                # the WAITING drawdown: worst adverse excursion
                # from the entry close during the bars BEFORE the
                # event week begins (the event's own path is the
                # payoff, not the risk)
                wait_end = max(t + 1, k - WEEK + 1)
                seg = logc[t:wait_end]
                mae = max(0.0,
                          float(np.max(seg) - logc[t]),
                          float(logc[t] - np.min(seg)))
                maes.append(mae / thr)
                ev_sizes.append(
                    abs(logc[k] - logc[k - WEEK]) / thr)
    if not maes:
        return {"verdict": "INSUFFICIENT_DATA"}
    med_mae = float(np.median(maes))
    med_ev = float(np.median(ev_sizes))
    rr = med_ev / med_mae if med_mae > 0 else None
    return {
        "n_events": len(maes),
        "median_waiting_mae_sigma_bars": round(med_mae, 3),
        "p75_waiting_mae": round(float(
            np.quantile(maes, 0.75)), 3),
        "median_event_size_sigma_bars": round(med_ev, 3),
        "rr_by_construction": (round(rr, 2)
                              if rr is not None else None),
        "verdict": ("STRUCTURAL - the waiting drawdown is a "
                    "small fraction of the event size: the "
                    "event-capture structure is high-RR by "
                    "construction" if rr is not None and rr >= 2
                    else "FOLKLORE - the waiting drawdown eats "
                    "the event"),
    }


def claim_t2(data_dir: Path) -> dict:
    """The crash-depth gradient on anchored assets: forward
    4-week return by crash depth bucket."""
    buckets = {f"{hi:.3f}_{lo:.3f}": []
               for hi, lo in CRASH_BUCKETS}
    for name, c, v in _series(data_dir):
        if name not in ANCHORED:
            continue
        logc = np.log(c)
        wr = np.zeros(len(logc))
        wr[WEEK:] = logc[WEEK:] - logc[:-WEEK]
        for t in range(WARMUP, len(logc) - WEEK * FWD_WEEKS):
            r = wr[t]
            if r >= 0:
                continue
            fwd = logc[t + WEEK * FWD_WEEKS] - logc[t]
            for hi, lo in CRASH_BUCKETS:
                key = f"{hi:.3f}_{lo:.3f}"
                if lo > r >= hi:
                    buckets[key].append(float(fwd))
                    break
    out = {}
    medians = []
    for key, rets in buckets.items():
        if len(rets) < 10:
            out[key] = {"n": len(rets)}
            continue
        w = _winsorize(rets)
        med = float(np.median(w))
        out[key] = {
            "n": len(rets),
            "depth": key.replace("_", " to "),
            "median_fwd_4w": round(med, 4),
            "p_positive": round(float(np.mean(
                np.array(rets) > 0)), 3),
        }
        medians.append(med)
    monotone = all(medians[i] <= medians[i + 1]
                   for i in range(len(medians) - 1)) \
        and len(medians) >= 3
    deep = out.get("-1.000_-0.150", {})
    return {
        "buckets": out,
        "gradient_monotone_deeper_is-better": bool(monotone),
        "nuclear_red": {
            "n": deep.get("n"),
            "median_fwd_4w": deep.get("median_fwd_4w"),
            "p_positive": deep.get("p_positive"),
        },
        "verdict": ("STRUCTURAL - deeper crashes buy higher "
                    "forward medians: the nuclear-red buy is the "
                    "highest-RR defined-risk entry the daily "
                    "grain measures" if monotone and
                    deep.get("median_fwd_4w", 0) > 0
                    else "FOLKLORE - the depth gradient is not "
                    "measured on these assets"),
    }


def claim_t3(data_dir: Path) -> dict:
    """The post-event calm: after a significant week, is the
    following week quieter than the asset's baseline?"""
    quieter = tot = 0
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        wr = np.zeros(len(logc))
        wr[WEEK:] = logc[WEEK:] - logc[:-WEEK]
        base = np.zeros(len(logc))
        for t in range(WARMUP, len(logc)):
            h = wr[t - 40:t + 1]
            h = h[np.abs(h) > 0]
            base[t] = np.abs(h).mean() if len(h) else 0
        for t in range(WARMUP + WEEK, len(logc) - WEEK):
            if sig[t] <= 0:
                continue
            if abs(wr[t]) >= EVENT_SIG * sig[t]:
                tot += 1
                nxt = abs(wr[t + WEEK])
                if base[t] > 0 and nxt < base[t]:
                    quieter += 1
    if not tot:
        return {"verdict": "INSUFFICIENT_DATA"}
    p = quieter / tot
    return {
        "n_significant_weeks": tot,
        "p_next_week_quiet": round(float(p), 3),
        "verdict": ("STRUCTURAL - the market's recovery is in "
                    "its boredom: the week after the event is "
                    "calmer than baseline, the measured re-entry "
                    "window" if p > 0.55 else
                    "FOLKLORE - no measured post-event calm"),
    }


def run_trade_inevitables(data_dir: Path) -> dict:
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "protocol": "the trade-inevitables: additions to the "
            "rule set, measured with the programme's honesty "
            "conventions - the drawdown profile of the armed "
            "clock, the crash-depth gradient on anchored "
            "assets, and the post-event calm",
        "t1_armed_clock_drawdown": claim_t1(data_dir),
        "t2_crash_depth_gradient": claim_t2(data_dir),
        "t3_post_event_calm": claim_t3(data_dir),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Trade inevitables (the rule additions)")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_trade_inevitables(args.data_dir)
    dest = args.research_dir / "trade_inevitables.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    t1 = r["t1_armed_clock_drawdown"]
    t2 = r["t2_crash_depth_gradient"]
    t3 = r["t3_post_event_calm"]
    print(f"trade inevitables -> {dest} "
          f"(T1 {t1.get('verdict', '')[:12]} "
          f"RR {t1.get('rr_by_construction')}, "
          f"T2 {t2.get('verdict', '')[:12]}, "
          f"T3 {t3.get('verdict', '')[:12]} "
          f"p {t3.get('p_next_week_quiet')})")


if __name__ == "__main__":
    main()
