"""Structural inevitabilities: the market facts that hold without
prediction.

The framework (from the project's own research notes): true
direction prediction is impossible - but markets have INEVITABLE
occurrences and drawdown-hostile conditions that can be catalogued
and measured:

  1. IMPULSE/NOISE STRUCTURE: markets range most of the time; a
     small fraction of bars carries most of the movement. If true,
     the top 1%/5% of bars must carry a hugely disproportionate
     share of total absolute movement.
  2. THE CRASH BOUNCE: a best-buy condition at -7% or worse (the
     notes' "nuclear red day -15%"). Measured: forward 10-day
     distribution after crash days vs the unconditional baseline -
     median, probability of positive, and the worst tail.
  3. TIME-AT-PRICE LEVELS: prices where the market spent unusual
     time become levels it will not quickly revisit (the daily-
     bar approximation of the "last orderbook low"). Measured:
     after multi-bar congestion at a level, how often does price
     return within 60 bars?
  4. COMPRESSION -> IMPULSE: "a long time horizontally is
     inevitably needed for a significant change." Measured: after
     the tightest trailing ranges, is the next move larger than
     baseline?
  5. IMPULSE FOLLOW-THROUGH: impulse/correction alternation. After
     a large bar, does the move continue (trend) or revert
     (exhaustion)?

Every claim is measured across the whole extended universe with
honest statistics (medians, own-scale beats, tails) and a verdict:
STRUCTURAL (inevitable) or FOLKLORE (the data disagrees). The
5/15-minute max-hold rules from the framework need intraday data
and are honestly recorded as untestable on daily bars.

Usage (nightly):
    python3 inevitabilities.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import load_bars

HORIZON = 10
CRASH_DAY = -0.07
NUCLEAR_DAY = -0.15
CONGESTION_BARS = 5
CONGESTION_RET = 0.002
RETURN_WINDOW = 60
COMP_RANGE_PCT = 0.2
IMPULSE_DAY = 0.03


def _fwd(c, t, h=HORIZON):
    if t + h >= len(c):
        return None
    return float(c[t + h] / c[t] - 1.0)


def run_inevitabilities(data_dir: Path) -> dict:
    series = []
    for f in sorted(data_dir.glob("*.csv")):
        bars = load_bars(f)
        if len(bars) < 400:
            continue
        c = np.array([b["close"] for b in bars], dtype=float)
        mask = np.isfinite(c) & (c > 0)
        c = c[mask]
        if len(c) < 400 or (c.max() > 0 and c[-1] < c.max() / 1000.0):
            continue
        series.append({"ticker": f.stem.upper(),
                       "cls": ("crypto" if f.stem.lower().endswith("usd")
                               else "other"),
                       "c": c})

    out = {"n_series": len(series), "claims": {}}

    # --- 1. impulse/noise structure ---------------------------------
    shares = {1: [], 5: [], 10: []}
    for s in series:
        rets = np.abs(np.diff(np.log(s["c"])))
        tot = rets.sum()
        if tot <= 0:
            continue
        srt = np.sort(rets)[::-1]
        for pct in (1, 5, 10):
            k = max(1, int(len(srt) * pct / 100))
            shares[pct].append(float(srt[:k].sum() / tot))
    top5 = float(np.median(shares[5]))
    out["claims"]["impulse_concentration"] = {
        "description": ("share of total absolute movement carried "
                        "by the top 1% / 5% / 10% of bars - if "
                        "markets are noise most of the time with "
                        "distinct impulse points, these must be "
                        "hugely disproportionate. The verdict uses "
                        "the concentration RATIO: top-5% share "
                        "divided by 5% (uniform = 1.0)"),
        "top1_median": round(float(np.median(shares[1])), 3),
        "top5_median": round(top5, 3),
        "top10_median": round(float(np.median(shares[10])), 3),
        "concentration_ratio_top5": round(top5 / 0.05, 1),
        "verdict": ("STRUCTURAL" if top5 / 0.05 >= 3.0
                    else "FOLKLORE"),
    }

    # --- 2. the crash bounce ------------------------------------------
    # split by class: a dying crypto crashes repeatedly (terminal
    # collapse contaminates the crash sample), while anchored
    # assets (commodities, indices) are where the bounce claim
    # actually means something
    crash_by_cls = {"crypto": [], "other": []}
    nuclear_fwd, base_fwd = [], []
    crash_worst = []
    for s in series:
        c = s["c"]
        rets = np.diff(np.log(c))
        for t in range(len(c) - HORIZON - 1):
            fr = _fwd(c, t)
            if fr is None:
                continue
            base_fwd.append(fr)
            # rets[t] is the move INTO bar t+1: the crashed close is
            # bar t+1, so the bounce is measured FROM the crashed
            # close, never including the crash itself
            if rets[t] <= CRASH_DAY:
                frc = _fwd(c, t + 1)
                if frc is not None:
                    crash_by_cls[s["cls"]].append(frc)
            if rets[t] <= NUCLEAR_DAY:
                frn = _fwd(c, t + 1)
                if frn is not None:
                    nuclear_fwd.append(frn)
    crash_fwd = crash_by_cls["crypto"] + crash_by_cls["other"]
    crash_med = (round(float(np.median(crash_fwd)), 4)
                 if crash_fwd else None)
    base_med = round(float(np.median(base_fwd)), 4)
    out["claims"]["crash_bounce"] = {
        "description": ("forward 10-day return after a <= -7% day "
                        "(and <= -15% nuclear day) vs the "
                        "unconditional baseline"),
        "n_crashes": len(crash_fwd),
        "crash_fwd_median": crash_med,
        "crash_fwd_p_positive": (round(float(np.mean(
            np.array(crash_fwd) > 0)), 3) if crash_fwd else None),
        "crash_fwd_p10": (round(float(np.quantile(
            crash_fwd, 0.10)), 4) if crash_fwd else None),
        "n_nuclear": len(nuclear_fwd),
        "nuclear_fwd_median": (round(float(np.median(nuclear_fwd)), 4)
                               if nuclear_fwd else None),
        "baseline_median": base_med,
        "crash_fwd_median_crypto": (
            round(float(np.median(crash_by_cls["crypto"])), 4)
            if crash_by_cls["crypto"] else None),
        "n_crashes_crypto": len(crash_by_cls["crypto"]),
        "crash_fwd_median_anchored": (
            round(float(np.median(crash_by_cls["other"])), 4)
            if crash_by_cls["other"] else None),
        "n_crashes_anchored": len(crash_by_cls["other"]),
        "anchored_p_positive": (
            round(float(np.mean(np.array(
                crash_by_cls["other"]) > 0)), 3)
            if crash_by_cls["other"] else None),
        "verdict": ("STRUCTURAL_ON_ANCHORED"
                    if crash_by_cls["other"]
                    and np.median(crash_by_cls["other"]) > 0
                    and np.mean(np.array(
                        crash_by_cls["other"]) > 0) > 0.55
                    else "FOLKLORE"),
    }

    # --- 3. time-at-price levels ---------------------------------------
    returned, total_levels = 0, 0
    for s in series:
        c = s["c"]
        rets = np.abs(np.diff(np.log(c)))
        t = CONGESTION_BARS
        while t < len(c) - RETURN_WINDOW:
            window = rets[t - CONGESTION_BARS:t]
            if np.all(window <= CONGESTION_RET):
                level = c[t]
                lo_lvl, hi_lvl = level * 0.995, level * 1.005
                later = c[t + 1:t + 1 + RETURN_WINDOW]
                total_levels += 1
                if np.any((later >= lo_lvl) & (later <= hi_lvl)):
                    returned += 1
                t += RETURN_WINDOW      # non-overlapping samples
            else:
                t += 1
    p_return = (round(returned / total_levels, 3)
                if total_levels else None)
    out["claims"]["time_at_price"] = {
        "description": ("after >= 5 bars of congestion at one "
                        "price, how often does price RETURN to that "
                        "level (within 0.5%) within 60 bars? - the "
                        "daily-bar approximation of the last-"
                        "orderbook-low idea"),
        "n_levels": total_levels,
        "p_return_within_60": p_return,
        "verdict": ("STRUCTURAL" if p_return is not None
                    and p_return < 0.35 else "FOLKLORE"),
    }

    # --- 4. compression -> impulse --------------------------------------
    comp_moves, base_moves = [], []
    for s in series:
        c = s["c"]
        rets = np.diff(np.log(c))
        rng10 = np.convolve(np.abs(rets), np.ones(10), "valid") / 10
        for t in range(20, len(rng10) - 20):
            hist = rng10[max(0, t - 500):t + 1]
            if len(hist) < 50:
                continue
            pct = float(np.mean(hist <= rng10[t]))
            move = float(np.abs(np.log(c[t + 20]) - np.log(c[t])))
            if pct <= COMP_RANGE_PCT:
                comp_moves.append(move)
            else:
                base_moves.append(move)
    comp_med = (round(float(np.median(comp_moves)), 4)
                if comp_moves else None)
    base_move_med = (round(float(np.median(base_moves)), 4)
                     if base_moves else None)
    out["claims"]["compression_impulse"] = {
        "description": ("after the tightest trailing 10-bar ranges "
                        "(bottom 20% of their trailing history), is "
                        "the next 20-bar move larger than baseline? "
                        "- the horizontal-time-before-impulse claim"),
        "n_compressed": len(comp_moves),
        "compressed_move_median": comp_med,
        "baseline_move_median": base_move_med,
        "verdict": ("STRUCTURAL" if comp_med and base_move_med
                    and comp_med > base_move_med else "FOLKLORE"),
    }

    # --- 5. impulse follow-through --------------------------------------
    cont, rev, tot_i = 0, 0, 0
    for s in series:
        c = s["c"]
        rets = np.diff(np.log(c))
        for t in range(len(rets) - 5):
            if abs(rets[t]) >= IMPULSE_DAY:
                tot_i += 1
                fwd5 = float(np.log(c[t + 6]) - np.log(c[t + 1]))
                if np.sign(fwd5) == np.sign(rets[t]):
                    cont += 1
                elif fwd5 != 0:
                    rev += 1
    p_cont = round(cont / tot_i, 3) if tot_i else None
    out["claims"]["impulse_follow_through"] = {
        "description": ("after a >= 3% impulse bar, does the next "
                        "5-day move continue (trend) or revert "
                        "(exhaustion)? - the impulse/correction "
                        "alternation claim"),
        "n_impulses": tot_i,
        "p_continuation": p_cont,
        "verdict": ("STRUCTURAL_CONTINUATION" if p_cont
                    and p_cont > 0.55 else
                    "STRUCTURAL_REVERSION" if p_cont
                    and p_cont < 0.45 else "NO_STRUCTURE"),
    }

    out["untestable_on_dailies"] = (
        "the framework's 5/15-minute max-hold and fast-fail rules "
        "require intraday (orderbook / minute-bar) data; recorded "
        "honestly as out of scope for daily bars")
    out["generated_utc"] = datetime.now(timezone.utc).isoformat(
        timespec="seconds")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Structural inevitabilities, measured")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_inevitabilities(args.data_dir)
    dest = args.research_dir / "inevitabilities.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    verdicts = {k: v["verdict"] for k, v in r["claims"].items()}
    print(f"inevitabilities -> {dest} ({r['n_series']} series)")
    for k, v in verdicts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
