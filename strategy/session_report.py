"""Session performance report for the VP-MR paper-trading state.

Reads the runner's persisted session state + feed CSVs and produces a
decision-grade report: MTM equity curve, Sharpe/max-DD, realized vs
expected costs, SPI status, and open-position risk. Harness file.

Usage:
    python3 session_report.py --data-dir ./paper/data --state-dir ./paper/state
    python3 session_report.py --data-dir ./paper/data --state-dir ./paper/state --markdown report.md
"""
import argparse
import json
import math
from pathlib import Path
from typing import Dict, List

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import load_bars
from vp_mr_strategy import StrategyParameters, VolatilityParityMeanReversionStrategy
import spi_monitor


def restore_strategy(state: dict) -> VolatilityParityMeanReversionStrategy:
    """Rebuild the deployed strategy from persisted state (read-only)."""
    params = StrategyParameters()
    strat = VolatilityParityMeanReversionStrategy(
        params, state["universe"], state["initial_equity"])
    strat.deploy()
    for s in state["universe"]:
        strat.position[s] = state["positions"][s]
        for c in state["close_buf"][s]:
            strat._close[s].append(c)
        for h in state["high_buf"][s]:
            strat._high[s].append(h)
        for l in state["low_buf"][s]:
            strat._low[s].append(l)
        if state.get("entry_px", {}).get(s) is not None:
            strat._entry_px[s] = state["entry_px"][s]
        if state.get("trail_stop", {}).get(s) is not None:
            strat._trail_stop[s] = state["trail_stop"][s]
    strat.equity = state["equity"]
    strat.decision_log = state["decision_log"]
    strat.order_log = state["order_log"]
    return strat


def build_report(data_dir: Path, state_dir: Path) -> dict:
    state = json.load(open(state_dir / "session_state.json"))
    strat = restore_strategy(state)
    universe = state["universe"]

    # MTM equity: replay positions (from decision log) against feed prices
    bars = {s: load_bars(data_dir / f"{s.lower()}.csv") for s in universe}
    dates = sorted({b["date"] for s in universe for b in bars[s]})
    pos = {s: {} for s in universe}
    for rec in strat.decision_log:
        pos[rec["instrument"]][rec["ts"]] = rec["position"]
    px = {s: {b["date"]: b["close"] for b in bars[s]} for s in universe}

    equity = []
    for d in dates:
        pnl = 0.0
        for s in universe:
            p = pos[s].get(d)
            if p is None:
                continue
            prev_dates = [x for x in px[s] if x < d]
            if not prev_dates:
                continue
            prev_d = max(prev_dates)
            pnl += p * (px[s][d] - px[s][prev_d])
        equity.append(state["initial_equity"] + pnl)
    eq = np.array(equity) if equity else np.array([state["initial_equity"]])

    rets = np.diff(eq) / eq[:-1] if len(eq) > 1 else np.array([0.0])
    ann_ret = float(rets.mean() * 252)
    ann_vol = float(rets.std(ddof=1) * math.sqrt(252)) if len(rets) > 1 else 0.0
    peak = np.maximum.accumulate(eq)
    max_dd = float(((peak - eq) / peak).max()) if len(eq) else 0.0

    audit = spi_monitor.audit_parity(strat)
    fills = [o for o in strat.order_log if o.get("state") == "FILLED"]
    expected_costs = sum(o.get("expected_cost", 0.0) for o in fills)

    open_risk = {}
    for s in universe:
        q = strat.position[s]
        if q != 0.0 and s in strat._trail_stop and strat._close[s]:
            stop = strat._trail_stop[s]
            last = strat._close[s][-1]
            open_risk[s] = {"qty": q, "last_close": last, "stop": stop,
                            "risk_to_stop": round(abs(q * (last - stop)), 2)}

    return {
        "sessions_bars": len(dates),
        "final_equity_mtm": round(float(eq[-1]), 2),
        "equity_internal_cost_only": round(state["equity"], 2),
        "ann_return_pct": round(ann_ret * 100, 3),
        "ann_vol_pct": round(ann_vol * 100, 3),
        "sharpe": round(ann_ret / ann_vol, 3) if ann_vol > 0 else 0.0,
        "max_dd_pct": round(max_dd * 100, 3),
        "spi": audit["spi"],
        "duplicate_fires": audit["duplicate_fires"],
        "fills": audit["fills"],
        "expected_costs_total": round(expected_costs, 2),
        "order_reasons": audit["order_reasons"],
        "kill_switch_events": audit["kill_switch_events"],
        "audit_status": audit["status"],
        "open_positions": {s: q for s, q in strat.position.items() if q != 0.0},
        "open_risk_to_stop": open_risk,
    }


def to_markdown(rep: dict) -> str:
    lines = ["# VP-MR-ETF-D1-001 paper-trading session report", ""]
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    for k, v in rep.items():
        if isinstance(v, dict):
            continue
        lines.append(f"| {k} | {v} |")
    if rep["open_risk_to_stop"]:
        lines += ["", "## Open position risk", "",
                  "| Instrument | Qty | Last close | Stop | Risk to stop |",
                  "|---|---|---|---|---|"]
        for s, r in rep["open_risk_to_stop"].items():
            lines.append(f"| {s} | {r['qty']} | {r['last_close']} | "
                         f"{r['stop']} | {r['risk_to_stop']} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--state-dir", required=True, type=Path)
    ap.add_argument("--markdown", type=Path, default=None)
    args = ap.parse_args()
    rep = build_report(args.data_dir, args.state_dir)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(to_markdown(rep))
        print(f"report written -> {args.markdown}")
    for k, v in rep.items():
        print(f"  {k:>28}: {v}")


if __name__ == "__main__":
    main()
