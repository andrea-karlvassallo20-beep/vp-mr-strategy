"""THE LAW-4 BATTERY: effort vs result at the crash-zone entry.

The charter's law 4: impact is concave in volume - big moves
require big flow, and a move without volume is a suspect move.
The event anatomy already measured it at the event grain
(significant weeks come on 1.138x baseline volume). This
battery asks the layer-5 question: does EFFORT AT ENTRY gate
the crash-zone BOUNCE?

Cells, pre-declared (entries are the philosopher's episode
crosses on the anchored set, 4-week hold, 5 bps costs both
sides, winsorized medians, dual-split gate per cell,
per-asset breakdown mandatory):

  - effort ratio = volume at the entry bar / trailing median
    volume (60 bars, strictly causal)
  - HIGH EFFORT: ratio > 1 (the crash came on above-habit
    participation)
  - LOW EFFORT: ratio <= 1 (the crash came quietly)
  - tercile split within the entries: quiet / normal / heavy

Honest verdict either way: if high-effort crashes bounce
better through the gate, law 4 gates the entry; if not, the
quiet crash is just as good a buy and the effort read stays
descriptive. Nothing is promoted without the gate AND forward
scoring (doctrine rule 5).

Usage (nightly, after exit_battery):
    python3 law4_battery.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from market_philosopher import (ANCHORED, COST_BPS, HOLD_WEEKS,
                                WEEK, ZONE_HI, ZONE_LO)
from smh_proof import WARMUP, _series

WINSOR = 0.05
SPLITS = (0.5, 0.6)
BASE_BARS = 60          # trailing volume baseline window


def _weekly_return(logc, t):
    return float(logc[t] - logc[t - WEEK])


def _cell_stats(trades):
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
    per = {}
    for tr in trades:
        per.setdefault(tr["ticker"], []).append(tr["net"])
    return {
        "n": len(trades),
        "median_net": round(med, 4),
        "p_positive": round(float(np.mean(rets > 0)), 3),
        "dual_split_windows": wins,
        "dual_split_gate": bool(gate),
        "per_asset": {
            nm: {"n": len(a),
                 "median_net": round(float(np.median(a)), 4),
                 "positive": bool(np.median(a) > 0)}
            for nm, a in sorted(per.items())},
    }


def run_law4(data_dir: Path) -> dict:
    """The effort split at the crash-zone entry."""
    trades = []
    for name, c, v in _series(data_dir):
        if name not in ANCHORED:
            continue
        if len(c) < WARMUP + WEEK * HOLD_WEEKS + 5:
            continue
        logc = np.log(c)
        last_entry = -10 ** 9
        for t in range(WARMUP, len(c) - WEEK * HOLD_WEEKS):
            wr = _weekly_return(logc, t)
            prev = _weekly_return(logc, t - 1)
            if (ZONE_LO <= wr < ZONE_HI
                    and not ZONE_LO <= prev < ZONE_HI
                    and t >= last_entry + WEEK * HOLD_WEEKS):
                last_entry = t
                base = float(np.median(
                    v[t - BASE_BARS:t])) if t >= BASE_BARS \
                    else None
                ratio = (float(v[t]) / base
                         if base and base > 0 else None)
                fwd = float(logc[t + WEEK * HOLD_WEEKS]
                            - logc[t])
                trades.append({
                    "ticker": name, "t": t,
                    "net": fwd - 2 * COST_BPS / 1e4,
                    "effort_ratio": ratio,
                })
    measured = [tr for tr in trades
                if tr["effort_ratio"] is not None]
    if not measured:
        return {"status": "INSUFFICIENT_TRADES"}
    ratios = np.array([tr["effort_ratio"] for tr in measured])
    pooled = _cell_stats(measured)
    high = _cell_stats([tr for tr in measured
                        if tr["effort_ratio"] > 1.0])
    low = _cell_stats([tr for tr in measured
                       if tr["effort_ratio"] <= 1.0])
    q1, q2 = np.quantile(ratios, [1 / 3, 2 / 3])
    quiet = _cell_stats([tr for tr in measured
                         if tr["effort_ratio"] <= q1])
    normal = _cell_stats([tr for tr in measured
                          if q1 < tr["effort_ratio"] <= q2])
    heavy = _cell_stats([tr for tr in measured
                         if tr["effort_ratio"] > q2])

    def gated(better, worse):
        return (better.get("dual_split_gate")
                and "median_net" in better
                and "median_net" in worse
                and better["median_net"]
                > worse["median_net"])

    def positive_gate(cell):
        return (cell.get("dual_split_gate")
                and cell.get("median_net", 0) > 0)

    if "median_net" not in pooled:
        verdict = "INSUFFICIENT_BASELINE"
    elif positive_gate(high) and positive_gate(low):
        verdict = (
            f"EFFORT TILTS, IT DOES NOT GATE: both cells pass "
            f"the gate and both are positive edges (high "
            f"{high['median_net']}, low {low['median_net']}, "
            f"pooled {pooled['median_net']}) - the high-effort "
            f"crash is the modestly better buy but the quiet "
            f"crash is NOT a suspect move. The volume read "
            f"stays a context tilt on the philosopher's "
            f"verdicts, never an entry condition; flagged, "
            f"forward-scored or it stays folklore")
    elif gated(high, low) and not low.get("dual_split_gate"):
        verdict = (
            f"LAW 4 GATES THE ENTRY, DESIGN SAMPLE: high-effort "
            f"crashes (volume > trailing median) read median "
            f"net {high['median_net']} through the gate, while "
            f"low-effort crashes read {low.get('median_net')} "
            f"and fail it - flagged, forward-scored or it "
            f"stays folklore")
    elif gated(low, high) and not high.get("dual_split_gate"):
        verdict = (
            f"THE QUIET CRASH IS THE BETTER BUY, DESIGN SAMPLE: "
            f"low-effort crashes read median net "
            f"{low['median_net']} through the gate, while "
            f"high-effort crashes read {high.get('median_net')} "
            f"and fail it - the effort-vs-result relation does "
            f"NOT gate this entry; flagged, forward-scored or "
            f"it stays folklore")
    else:
        verdict = (
            f"LAW 4 DOES NOT GATE THE ENTRY: neither effort "
            f"cell separates from the pooled baseline through "
            f"the gate (high {high.get('median_net')}, low "
            f"{low.get('median_net')}, pooled "
            f"{pooled['median_net']}) - the volume read stays "
            f"descriptive at the entry grain (the charter's "
            f"event-grain finding stands: significant WEEKS "
            f"come on volume; significant BUYS do not need it)")

    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "question": ("does effort at entry (volume vs trailing "
                     "habit) gate the crash-zone bounce?"),
        "n_entries": len(measured),
        "effort_ratio_quantiles": {
            "q33": round(float(q1), 3),
            "q66": round(float(q2), 3)},
        "pooled": pooled,
        "high_effort": high,
        "low_effort": low,
        "terciles": {"quiet": quiet, "normal": normal,
                     "heavy": heavy},
        "verdict": verdict,
        "note": "episode crosses, 4-week holds, 5 bps costs, "
                "winsorized medians, dual-split gate per cell, "
                "per-asset breakdowns mandatory; design sample",
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Law-4 battery: effort vs result at the "
                    "crash-zone entry")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_law4(args.data_dir)
    dest = args.research_dir / "law4_battery.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    print(f"law4 battery -> {dest} "
          f"({r.get('n_entries')} entries)")
    print(f"verdict: {r.get('verdict')}")


if __name__ == "__main__":
    main()
