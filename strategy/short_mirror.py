"""THE SHORT MIRROR: is there a measured SHORT edge at the
euphoria zone, or is the long-only philosophy a measurement?

The crash-zone long is the programme's one measured edge
(206 episode trades, +1.69% median net, gate-passing,
OOS-replicated). The mirror question completes the symmetry
and must be asked honestly: does a SHORT at the cross into
the moderate euphoria zone (+5% to +10% weekly) earn its keep
under the same machinery?

Entries: the CROSS into the zone (one per episode, the same
cooldown convention), 4-week holds, 5 bps costs both sides,
winsorized medians, dual-split gate, per-asset breakdown
mandatory. A short's net return is the NEGATIVE of the
forward move, minus costs.

Honest expectation, stated in advance: the tops data already
hints negative (confirmed v4 tops on indexes read +1.46%
median forward 4w - shorting a confirmed top LOSES on
median), and law 3 says up-markets drift. If the mirror
reads negative, the finding is doctrine-grade: the long-only
philosophy is not a choice, it is a measurement.

Usage (nightly, after law4_battery):
    python3 short_mirror.py --data-dir ../paper/research/data \
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
                                WEEK)
from smh_proof import WARMUP, _series

WINSOR = 0.05
SPLITS = (0.5, 0.6)
EUPH_LO = 0.05        # the moderate euphoria zone: the mirror
EUPH_HI = 0.10        # of the measured best-buy zone
NUC_HI = 0.15         # the nuclear-red euphoria, measured too


def _weekly_return(logc, t):
    return float(logc[t] - logc[t - WEEK])


def _entries(logc, n, lo, hi, cooldown):
    out = []
    last_entry = -10 ** 9
    for t in range(WARMUP, n - WEEK * HOLD_WEEKS):
        wr = _weekly_return(logc, t)
        prev = _weekly_return(logc, t - 1)
        if (lo <= wr < hi
                and not lo <= prev < hi
                and t >= last_entry + cooldown):
            last_entry = t
            out.append(t)
    return out


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
                 "median_net": round(float(np.median(a)), 4)}
            for nm, a in sorted(per.items())},
    }


def run_short_mirror(data_dir: Path) -> dict:
    """The euphoria-zone short, measured on the anchored set."""
    trades_mod = []
    trades_nuc = []
    for name, c, v in _series(data_dir):
        if name not in ANCHORED:
            continue
        if len(c) < WARMUP + WEEK * HOLD_WEEKS + 5:
            continue
        logc = np.log(c)
        for t in _entries(logc, len(c), EUPH_LO, EUPH_HI,
                          WEEK * HOLD_WEEKS):
            fwd = float(logc[t + WEEK * HOLD_WEEKS] - logc[t])
            trades_mod.append({
                "ticker": name, "t": t,
                "net": -fwd - 2 * COST_BPS / 1e4})
        for t in _entries(logc, len(c), EUPH_HI, NUC_HI,
                          WEEK * HOLD_WEEKS):
            fwd = float(logc[t + WEEK * HOLD_WEEKS] - logc[t])
            trades_nuc.append({
                "ticker": name, "t": t,
                "net": -fwd - 2 * COST_BPS / 1e4})
    mod = _cell_stats(trades_mod)
    nuc = _cell_stats(trades_nuc)

    if "median_net" not in mod:
        verdict = "INSUFFICIENT_TRADES"
    elif mod["dual_split_gate"] and mod["median_net"] > 0:
        verdict = (
            f"A MEASURED SHORT EDGE EXISTS, DESIGN SAMPLE: the "
            f"moderate euphoria short reads median net "
            f"{mod['median_net']} through the gate - flagged, "
            f"forward-scored or it stays folklore")
    else:
        nuclear_line = ""
        if "median_net" in nuc \
                and nuc.get("dual_split_gate") \
                and nuc["median_net"] > 0:
            nuclear_line = (
                f" One seductive cell is flagged beside it, "
                f"never hidden: the NUCLEAR euphoria short "
                f"(+10..15% weekly, n={nuc['n']}) reads "
                f"{nuc['median_net']} through the gate - small "
                f"sample, seductive, carries its flag forever "
                f"(doctrine rule 5) until forward-scored.")
        verdict = (
            f"THE MIRROR IS NEGATIVE: the moderate euphoria "
            f"short reads median net {mod['median_net']} "
            f"(P(+) {mod['p_positive']}, gate "
            f"{'passes' if mod['dual_split_gate'] else 'FAILS'}"
            f") - there is NO measured short edge at the "
            f"mirror of the best-buy zone. The long-only "
            f"philosophy is not a choice, it is a MEASUREMENT: "
            f"the market takes the stairs up and the elevator "
            f"down, and only the elevator side pays the "
            f"philosopher." + nuclear_line)

    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "question": ("is there a measured SHORT edge at the "
                     "euphoria zone, the mirror of the "
                     "crash-zone long?"),
        "moderate_euphoria_short": mod,
        "nuclear_euphoria_short": nuc,
        "verdict": verdict,
        "note": "episode crosses, 4-week holds, 5 bps costs "
                "both sides, winsorized medians, dual-split "
                "gate, per-asset breakdowns; design sample",
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="The short mirror: the euphoria-zone "
                    "short, measured")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_short_mirror(args.data_dir)
    dest = args.research_dir / "short_mirror.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    print(f"short mirror -> {dest}")
    for k in ("moderate_euphoria_short",
              "nuclear_euphoria_short"):
        c = r[k]
        print(f"  {k}: n={c.get('n')} "
              f"median={c.get('median_net')} "
              f"gate={c.get('dual_split_gate')}")
    print(f"verdict: {r['verdict']}")


if __name__ == "__main__":
    main()
