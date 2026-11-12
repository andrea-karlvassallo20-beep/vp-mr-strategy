"""THE EXIT BATTERY: entry exits and fewer trades, measured.

The timing battery measured the WHEN (median bounce peak at
week 3, ~47% realized by week 2). This battery asks the two
questions that follow, on the same episode entries, with every
cell reported and none cherry-picked:

  1. THE HOLD LADDER: what does each fixed hold give up?
     1/2/3/4 weeks, net of costs, with the trade count, the
     positive rate, and the exposure (bars in the market) per
     cell. The 4-week cell IS the production baseline.

  2. THE PROFIT-TAKE EXITS: exit at the first week whose
     cumulative return clears +2% / +4%, else the time exit at
     4 weeks. Right-side exits, measured against the ladder.

  3. FEWER TRADES, ENTRY FILTERS: each filter must EARN its
     trades back with a better median net and must still pass
     the dual-split gate, or it is refused:
       - v4_confirmed: a v4 confirmed bottom within +/-3 bars
         of the cross (the AVFI layer as an entry condition)
       - compression_at_entry: the region is compression at
         the cross (the clock layer as an entry condition)
       - no_consecutive_crash: the week BEFORE the cross was
         not itself a crash week (the falling-knife filter)

Honesty rules, unchanged: winsorized medians, 5 bps costs both
sides, per-asset breakdown mandatory for any promoted cell,
dual-split gate on last-40% and last-50% windows, negative
results are rules too, and every number is design-sample until
the forward log scores it.

Usage (nightly, after timing_battery):
    python3 exit_battery.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from market_philosopher import ANCHORED, HOLD_WEEKS, WEEK, \
    ZONE_HI, ZONE_LO, COST_BPS
from smh_gradient import _tercile_states
from smh_proof import WARMUP, _series, _weekly_sigma
from tops_bottoms_backtest import detect_events
from v4_study import causal_z

WINSOR = 0.05
SPLITS = (0.5, 0.6)
V4_WINDOW = 3          # bars around the cross for a confirmed bottom
PROFIT_TAKES = (0.02, 0.04)
HOLDS = (1, 2, 3, 4)


def _weekly_return(logc, t):
    return float(logc[t] - logc[t - WEEK])


def _entries(logc, n, cooldown_bars):
    """Episode entries: the cross into the crash zone, one per
    episode, cooldown = the bars the tested rule spends in the
    market."""
    out = []
    last_entry = -10 ** 9
    for t in range(WARMUP, n - WEEK * HOLD_WEEKS):
        wr = _weekly_return(logc, t)
        prev = _weekly_return(logc, t - 1)
        if (ZONE_LO <= wr < ZONE_HI
                and not ZONE_LO <= prev < ZONE_HI
                and t >= last_entry + cooldown_bars):
            last_entry = t
            out.append(t)
    return out


def _exit_return(logc, t, hold, profit_take=None):
    """The net return of one entry under an exit rule: the fixed
    hold, or the first week that clears the profit take (then
    the time exit at the full hold)."""
    entry = float(logc[t])
    cost = 2 * COST_BPS / 1e4
    for w in range(1, hold + 1):
        run = float(logc[t + WEEK * w] - entry)
        if profit_take is not None and run >= profit_take:
            return run, w, True
    return float(logc[t + WEEK * hold] - entry), hold, False


def _cell_stats(trades):
    """Winsorized median, positive rate, dual-split gate."""
    if len(trades) < 10:
        return {"n": len(trades),
                "verdict": "INSUFFICIENT_TRADES"}
    rets = np.array([tr["net"] for tr in trades])
    w = np.clip(rets, *np.quantile(
        rets, [WINSOR, 1 - WINSOR]))
    med = float(np.median(w))

    def window_stats(lo):
        seg = rets[int(len(rets) * lo):]
        if len(seg) < 10:
            return None
        ws = np.clip(seg, *np.quantile(
            seg, [WINSOR, 1 - WINSOR]))
        return {"n": len(seg),
                "median_net": round(float(np.median(ws)), 4),
                "p_positive": round(float(np.mean(seg > 0)), 3)}

    wins = [window_stats(lo) for lo in SPLITS]
    gate = all(x is not None and x["median_net"] > 0
               for x in wins)
    return {
        "n": len(trades),
        "median_net": round(med, 4),
        "p_positive": round(float(np.mean(rets > 0)), 3),
        "mean_net": round(float(np.mean(w)), 4),
        "dual_split_windows": wins,
        "dual_split_gate": bool(gate),
    }


def run_exit_battery(data_dir: Path) -> dict:
    """All cells, measured. The baseline is the production rule:
    4-week hold, no filter."""
    universe = []
    for name, c, v in _series(data_dir):
        if name not in ANCHORED:
            continue
        if len(c) < WARMUP + WEEK * HOLD_WEEKS + 5:
            continue
        logc = np.log(c)
        states = _tercile_states(_weekly_sigma(logc))
        z = causal_z(c)
        _, _, bottoms, _ = detect_events(c, v)
        bset = set(int(b) for b in bottoms)
        universe.append((name, c, logc, states, bset))

    def collect(hold, profit_take=None, filt=None):
        trades = []
        for name, c, logc, states, bset in universe:
            ents = _entries(logc, len(c), WEEK * hold)
            for t in ents:
                if filt == "v4_confirmed":
                    if not any(t - V4_WINDOW <= b <= t + V4_WINDOW
                               for b in bset):
                        continue
                elif filt == "compression_at_entry":
                    if states[t] != 0:
                        continue
                elif filt == "no_consecutive_crash":
                    prev = _weekly_return(logc, t - 1)
                    if ZONE_LO <= prev < ZONE_HI:
                        continue
                r, w, took = _exit_return(
                    logc, t, hold, profit_take)
                trades.append({
                    "ticker": name, "t": t,
                    "net": r - 2 * COST_BPS / 1e4,
                    "exit_week": w, "profit_take_hit": took,
                })
        return trades

    def cell(hold, profit_take=None, filt=None):
        trades = collect(hold, profit_take, filt)
        st = _cell_stats(trades)
        st["hold_weeks"] = hold
        st["exposure_bars"] = int(sum(
            WEEK * tr["exit_week"] for tr in trades))
        if profit_take is not None:
            st["profit_take"] = profit_take
            st["profit_take_hit_rate"] = round(float(
                np.mean([tr["profit_take_hit"]
                         for tr in trades])), 3) \
                if trades else None
        if filt is not None:
            st["entry_filter"] = filt
        per = {}
        for tr in trades:
            a = per.setdefault(tr["ticker"], [])
            a.append(tr["net"])
        st["per_asset"] = {
            nm: {"n": len(a),
                 "median_net": round(float(np.median(a)), 4),
                 "positive": bool(np.median(a) > 0)}
            for nm, a in sorted(per.items())}
        return st, trades

    baseline = None
    ladder = []
    for hold in HOLDS:
        st, trades = cell(hold)
        ladder.append(st)
        if hold == HOLD_WEEKS:
            baseline = st

    profit_cells = []
    for pt in PROFIT_TAKES:
        st, _ = cell(HOLD_WEEKS, profit_take=pt)
        profit_cells.append(st)

    filter_cells = []
    for filt in ("v4_confirmed", "compression_at_entry",
                 "no_consecutive_crash"):
        st, trades = cell(HOLD_WEEKS, filt=filt)
        filter_cells.append(st)

    # the fewer-trades candidate: the best gate-passing filter
    # crossed with the realization-curve hold (2 weeks)
    combos = []
    for filt in ("v4_confirmed", "compression_at_entry",
                 "no_consecutive_crash"):
        st, trades = cell(2, filt=filt)
        st["note"] = ("filter + the 2-week hold the "
                      "realization curve suggests")
        combos.append(st)

    def verdict_line():
        if baseline is None or "median_net" not in baseline:
            return "INSUFFICIENT_BASELINE"
        better = [x for x in ladder
                  if x["hold_weeks"] < HOLD_WEEKS
                  and x.get("dual_split_gate")
                  and x.get("median_net", 0)
                  > baseline["median_net"]]
        if better:
            b = max(better, key=lambda x: x["median_net"])
            return (f"EARLY EXIT EARNS ITS KEEP: the "
                    f"{b['hold_weeks']}-week hold beats the "
                    f"4-week baseline median net "
                    f"({b['median_net']} vs "
                    f"{baseline['median_net']}) AND passes the "
                    f"dual-split gate")
        return ("NO EARLY TIME EXIT EARNS ITS KEEP: no shorter "
                "hold beats the 4-week baseline median net "
                "while passing the dual-split gate - the "
                "realization curve does not license a shorter "
                "hold, and the 4-week hold stands")

    def pt_verdict_line():
        if baseline is None or "median_net" not in baseline:
            return "INSUFFICIENT_BASELINE"
        better = [x for x in profit_cells
                  if x.get("dual_split_gate")
                  and x.get("median_net", 0)
                  > baseline["median_net"]]
        if better:
            b = max(better, key=lambda x: x["median_net"])
            return (f"THE PROFIT TAKE EARNS ITS KEEP, DESIGN "
                    f"SAMPLE: exit at first week >= "
                    f"{b['profit_take'] * 100:.0f}% gives "
                    f"median net {b['median_net']} vs the "
                    f"baseline {baseline['median_net']} "
                    f"(gate passes, hit rate "
                    f"{b['profit_take_hit_rate']}), at "
                    f"{b['exposure_bars'] / max(1, WEEK * HOLD_WEEKS * b['n']) * 100:.0f}% "
                    f"of the baseline exposure - flagged, "
                    f"forward-scored or it stays folklore")
        return ("NO PROFIT TAKE EARNS ITS KEEP: neither take "
                "level beats the baseline median net while "
                "passing the gate")

    def filter_verdict_line():
        if baseline is None or "median_net" not in baseline:
            return "INSUFFICIENT_BASELINE"
        earned = [x for x in filter_cells
                  if x.get("dual_split_gate")
                  and x.get("median_net", 0)
                  > baseline["median_net"]
                  and x.get("n", 0) < baseline["n"]]
        if earned:
            b = max(earned, key=lambda x: x["median_net"])
            return (f"FEWER TRADES, BETTER TRADES, DESIGN "
                    f"SAMPLE: the {b['entry_filter']} filter "
                    f"cuts the book to {b['n']} trades "
                    f"({100 * (1 - b['n'] / baseline['n']):.0f}% "
                    f"fewer) with median net {b['median_net']} "
                    f"vs the baseline {baseline['median_net']} "
                    f"(gate passes) - flagged, forward-scored "
                    f"or it stays folklore")
        return ("NO ENTRY FILTER EARNS ITS KEEP: no filter "
                "cuts trades while beating the baseline "
                "median net through the gate - the unfiltered "
                "zone cross stands")

    result = {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "question": ("does the timing curve justify an exit "
                     "rule, and can fewer, better entries beat "
                     "the production rule?"),
        "baseline_4w": baseline,
        "hold_ladder": ladder,
        "profit_take_cells": profit_cells,
        "entry_filter_cells": filter_cells,
        "filter_plus_2w_combos": combos,
        "verdict": verdict_line(),
        "profit_take_verdict": pt_verdict_line(),
        "entry_filter_verdict": filter_verdict_line(),
        "note": "every cell reported, none cherry-picked; "
                "winsorized medians, 5 bps costs both sides; "
                "design sample - forward-scored or it stays "
                "flagged",
    }
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="The exit battery: entry exits, fewer trades")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_exit_battery(args.data_dir)
    dest = args.research_dir / "exit_battery.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    b = r["baseline_4w"] or {}
    print(f"exit battery -> {dest} "
          f"(baseline n={b.get('n')} "
          f"median={b.get('median_net')} "
          f"gate={b.get('dual_split_gate')})")
    print(f"verdict: {r['verdict']}")


if __name__ == "__main__":
    main()
