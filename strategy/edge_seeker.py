"""Autonomous edge-seeking research trainer for VP-MR-ETF-D1-001.

Nightly research loop: walk-forwards candidate parameter variants on the
fetched market data and writes a proposal report. STRICTLY respects
Gate 3: the deployed strategy's parameters remain frozen; this module
never mutates session state or live parameters. Proposals are research
output only — any redeployment requires a human-reviewed PR.

Method (honest, no in-sample selection):
  1. Split fetched bars: first 60% = selection window, last 40% = OOS window.
  2. Grid candidates (z_entry x lookback); backtest each on the selection
     window; pick the best by Sharpe.
  3. Evaluate ONLY the selected candidate on the OOS window, alongside the
     frozen production parameters.
  4. Report: if a candidate beats production OOS Sharpe by a margin,
     propose it with evidence; else propose keeping production params.

Usage:
    python3 edge_seeker.py --data-dir ./paper/data --markdown ./paper/edge_report.md
"""
import argparse
import math
from pathlib import Path
from typing import Dict, List

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import load_bars
from vp_mr_strategy import StrategyParameters, VolatilityParityMeanReversionStrategy
from vol_models import VariantStrategy

# candidate space: (z_entry, lookback, vol_model, volume_filter,
#                   exit_z, atr_mult)
# vol_model: realized (production) | ewma (Levy/RiskMetrics) | garch (Levy)
# volume_filter: VSA weak-effort entry filter (Williams)
# exit_z / atr_mult: holding-period variants — a deeper z-score exit and a
# wider ATR trailing stop both lengthen the average hold
CANDIDATES = [
    (z, lb, vm, vf, 0.25, 3.0)
    for z in (1.5, 2.0, 2.5)
    for lb in (60, 100, 150)
    for vm in ("realized", "ewma", "garch")
    for vf in (False, True)
] + [
    (2.0, 100, "realized", False, ez, am)
    for ez in (0.0, -0.5)
    for am in (3.0, 5.0)
] + [(2.0, 100, "realized", False, 0.25, 5.0)]
MARGIN = 0.10   # candidate must beat production OOS Sharpe by this


def run_equity(prices: Dict[str, np.ndarray],
               params: StrategyParameters,
               variant: tuple = ("realized", False, 0.25, 3.0)) -> tuple:
    """Full-length backtest; returns (equity_curve, fills). Signals use only
    trailing data throughout, so scoring any later window is leakage-free.
    variant: (vol_model, volume_filter, exit_z, atr_mult) research
    extension; ("realized", False, 0.25, 3.0) is production."""
    vm, vf, ez, am = variant
    if vm == "realized" and not vf and ez == 0.25 and am == 3.0:
        strat = VolatilityParityMeanReversionStrategy(
            params, list(prices.keys()), 1_000_000.0)
    else:
        strat = VariantStrategy(params, list(prices.keys()), 1_000_000.0,
                                vol_model=vm, volume_filter=vf,
                                exit_z=ez, atr_mult=am)
    strat.deploy()
    n = len(next(iter(prices.values())))
    pos_hist = {s: np.zeros(n) for s in prices}
    for t in range(n):
        for s, px in prices.items():
            c = float(px[t])
            strat.on_bar_close(s, t, c, c * 1.002, c * 0.998, c, 1e6)
            if s in strat._pending and t + 1 < n:
                strat.on_order_fill(s, float(px[t + 1]))
            pos_hist[s][t] = strat.position[s]
    pnl = np.zeros(n)
    for s, px in prices.items():
        pnl[1:] += pos_hist[s][:-1] * np.diff(px)
    cum_cost = 1_000_000.0 - np.array(strat.equity_curve)[::len(prices)][:n]
    eq = 1_000_000.0 + np.cumsum(pnl) - cum_cost
    fills = sum(1 for o in strat.order_log if o.get("state") == "FILLED")
    return eq, fills


def score_window(eq: np.ndarray, lo: int, hi: int) -> dict:
    """Score a slice of the equity curve (warm-up happened before lo)."""
    seg = eq[lo:hi]
    if len(seg) < 2:
        return {"sharpe": 0.0, "ann_ret_pct": 0.0, "max_dd_pct": 0.0}
    base = seg[0]
    rets = np.diff(seg) / seg[:-1]
    ann_ret = float(rets.mean() * 252)
    ann_vol = float(rets.std(ddof=1) * math.sqrt(252)) if len(rets) > 1 else 0.0
    sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0
    peak = np.maximum.accumulate(seg)
    max_dd = float(((peak - seg) / peak).max())
    return {"sharpe": round(sharpe, 3), "ann_ret_pct": round(ann_ret * 100, 2),
            "max_dd_pct": round(max_dd * 100, 2)}


def seek(data_dir: Path, universe: List[str]) -> dict:
    prices = {}
    for s in universe:
        f = data_dir / f"{s.lower()}.csv"
        if not f.exists():
            continue
        prices[s] = np.array([b["close"] for b in load_bars(f)])
    if not prices:
        return {"status": "NO_DATA"}
    n = len(next(iter(prices.values())))
    split = int(n * 0.6)
    train = {s: px[:split] for s, px in prices.items()}
    test = {s: px[split:] for s, px in prices.items()}

    prod_params = StrategyParameters()

    # full-length runs per candidate; scored on the train window ONLY
    # (signals remain trailing, so OOS scoring later is leakage-free, and
    # the warm-up happens inside the train window instead of eating OOS)
    best = None
    grid_results = []
    equities = {}
    for cand in CANDIDATES:
        z, lb, vm, vf, ez, am = cand
        p = StrategyParameters(zscore_entry=z, lookback_zscore=lb)
        eq, _ = run_equity(prices, p, variant=(vm, vf, ez, am))
        equities[cand] = eq
        m = score_window(eq, 0, split)
        grid_results.append({"z_entry": z, "lookback": lb,
                             "vol_model": vm, "volume_filter": vf,
                             "exit_z": ez, "atr_mult": am,
                             "train_sharpe": m["sharpe"]})
        if best is None or m["sharpe"] > best[1]:
            best = (cand, m["sharpe"])
    (z_star, lb_star, vm_star, vf_star, ez_star, am_star), train_sharpe = best

    # OOS evaluation on the untouched last 40%: selected vs production
    oos_sel = score_window(equities[(z_star, lb_star, vm_star, vf_star,
                                     ez_star, am_star)], split, n)
    eq_prod, fills_prod = run_equity(prices, prod_params)
    oos_prod = score_window(eq_prod, split, n)
    oos_sel["fills"] = fills_prod  # fills reported from the full runs
    oos_prod["fills"] = fills_prod

    propose = (oos_sel["sharpe"] - oos_prod["sharpe"]) > MARGIN
    return {
        "status": "OK",
        "bars": n, "split": split,
        "selected_candidate": {"z_entry": z_star, "lookback": lb_star,
                               "vol_model": vm_star,
                               "volume_filter": vf_star,
                               "exit_z": ez_star, "atr_mult": am_star,
                               "train_sharpe": train_sharpe},
        "oos_selected": oos_sel,
        "oos_production": oos_prod,
        "grid": grid_results,
        "recommendation": ("PROPOSE_REDEPLOY" if propose else "KEEP_PRODUCTION"),
        "gate3_note": ("Deployed parameters remain frozen; any change "
                       "requires a human-reviewed PR."),
    }


def to_markdown(r: dict) -> str:
    if r.get("status") != "OK":
        return "# Edge-seeker report\n\nNo data available yet.\n"
    lines = ["# Edge-seeker research report", ""]
    lines.append(f"Data: {r['bars']} bars "
                f"(selection window {r['split']}, OOS {r['bars'] - r['split']})")
    lines.append("")
    lines.append(f"**Recommendation: {r['recommendation']}**")
    lines.append("")
    lines.append("## Out-of-sample comparison (last 40% of data)")
    lines.append("")
    lines.append("| Variant | z_entry | lookback | vol model | VSA filter "
                 "| exit z | ATR mult | OOS Sharpe | OOS Ann Ret % | "
                 "OOS Max DD % | Fills |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    c = r["selected_candidate"]
    o = r["oos_selected"]
    lines.append(f"| Selected candidate | {c['z_entry']} | {c['lookback']} | "
                 f"{c['vol_model']} | {c['volume_filter']} | {c['exit_z']} | "
                 f"{c['atr_mult']} | "
                 f"{o['sharpe']} | {o['ann_ret_pct']} | {o['max_dd_pct']} | {o['fills']} |")
    o = r["oos_production"]
    pp = StrategyParameters()
    lines.append(f"| Production (frozen) | {pp.zscore_entry} | "
                 f"{pp.lookback_zscore} | realized | False | "
                 f"{pp.zscore_exit} | {pp.atr_stop_multiple} | "
                 f"{o['sharpe']} | {o['ann_ret_pct']} | {o['max_dd_pct']} | {o['fills']} |")
    lines += ["", "## Selection-window grid (train Sharpe)", "",
              "| z_entry | lookback | vol model | VSA | exit z | ATR mult "
              "| train Sharpe |",
              "|---|---|---|---|---|---|---|"]
    for g in r["grid"]:
        lines.append(f"| {g['z_entry']} | {g['lookback']} | {g['vol_model']} | "
                     f"{g['volume_filter']} | {g['exit_z']} | "
                     f"{g['atr_mult']} | {g['train_sharpe']} |")
    lines += ["", f"## Gate 3", "", r["gate3_note"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--universe", default="SPY,QQQ,IWM,XLF,XLE")
    ap.add_argument("--markdown", type=Path, default=None)
    args = ap.parse_args()
    r = seek(args.data_dir, [t.strip() for t in args.universe.split(",")])
    md = to_markdown(r)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(md)
        print(f"edge report written -> {args.markdown}")
    print(f"recommendation: {r.get('recommendation', r.get('status'))}")


if __name__ == "__main__":
    main()
