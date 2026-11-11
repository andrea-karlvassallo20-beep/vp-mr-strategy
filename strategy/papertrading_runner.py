"""Paper-trading runner for VP-MR-ETF-D1-001.

Incrementally feeds bars from CSV files into the deployed strategy, persists
session state between invocations (so it can run once per bar / once per
close), and emits a daily SPI audit report via spi_monitor.

Feed contract: one CSV per instrument, columns
    date,open,high,low,close,volume
Only NEW rows (date > last processed) are consumed per invocation — the
runner is idempotent and safe to re-run on the same data.

This is an operational harness, not strategy code: it uses stdlib (csv,
json, argparse, pathlib) for I/O, which is outside the strategy AST sandbox
by design. The strategy core remains sandbox-clean.

Usage:
    python3 papertrading_runner.py --data-dir ./data --state-dir ./state
    python3 papertrading_runner.py --data-dir ./data --state-dir ./state --report
"""
import argparse
import csv
import json
import math
from pathlib import Path
from typing import Dict, List

import numpy as np

from vp_mr_strategy import (OrderState, StrategyParameters,
                            VolatilityParityMeanReversionStrategy)
import spi_monitor


def load_bars(csv_path: Path) -> List[dict]:
    bars = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            bars.append({
                "date": row["date"],
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row["volume"]),
            })
    return bars


class PaperTradingRunner:
    """Stateful wrapper: one strategy instance per state-dir, persisted as
    JSON after every invocation. Positions/order state survive restarts."""

    STATE_FILE = "session_state.json"

    def __init__(self, data_dir: Path, state_dir: Path,
                 params: StrategyParameters = None,
                 universe: List[str] = None,
                 initial_equity: float = 1_000_000.0) -> None:
        self.data_dir = data_dir
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.params = params or StrategyParameters()
        self.universe = universe or ["SPY", "QQQ", "IWM", "XLF", "XLE"]
        self.strat = VolatilityParityMeanReversionStrategy(
            self.params, self.universe, initial_equity)
        self.last_date: Dict[str, str] = {}
        self._load_state()

    # ---------------- persistence ----------------
    def _load_state(self) -> None:
        p = self.state_dir / self.STATE_FILE
        if not p.exists():
            return
        with open(p) as f:
            state = json.load(f)
        self.strat = VolatilityParityMeanReversionStrategy(
            self.params, state["universe"], state["initial_equity"])
        self.strat.deploy()
        for s in state["universe"]:
            self.strat.position[s] = state["positions"][s]
            self.last_date[s] = state["last_date"][s]
            for c in state["close_buf"][s]:
                self.strat._close[s].append(c)
            for h in state["high_buf"][s]:
                self.strat._high[s].append(h)
            for l in state["low_buf"][s]:
                self.strat._low[s].append(l)
        self.strat.equity = state["equity"]
        for s in state["universe"]:
            if state["entry_px"].get(s) is not None:
                self.strat._entry_px[s] = state["entry_px"][s]
            if state["trail_stop"].get(s) is not None:
                self.strat._trail_stop[s] = state["trail_stop"][s]
        self.strat.decision_log = state["decision_log"]
        self.strat.order_log = state["order_log"]

    def _save_state(self) -> None:
        state = {
            "universe": self.universe,
            "initial_equity": self.strat.initial_equity,
            "equity": self.strat.equity,
            "positions": {s: self.strat.position[s] for s in self.universe},
            "last_date": dict(self.last_date),
            "close_buf": {s: list(self.strat._close[s]) for s in self.universe},
            "high_buf": {s: list(self.strat._high[s]) for s in self.universe},
            "low_buf": {s: list(self.strat._low[s]) for s in self.universe},
            "entry_px": {s: self.strat._entry_px.get(s) for s in self.universe},
            "trail_stop": {s: self.strat._trail_stop.get(s) for s in self.universe},
            "decision_log": self.strat.decision_log,
            "order_log": self.strat.order_log,
        }
        tmp = self.state_dir / (self.STATE_FILE + ".tmp")
        with open(tmp, "w") as f:
            json.dump(state, f)
        tmp.replace(self.state_dir / self.STATE_FILE)

    # ---------------- session run ----------------
    def run_session(self) -> Dict[str, int]:
        """Consume all new bars for every instrument. Returns per-instrument
        bar counts processed this invocation."""
        processed = {}
        last_close: Dict[str, float] = {}
        self.strat.on_session_start()  # once per session, not per instrument:
        # a daily kill-switch trip must not be reset by the next instrument
        for s in self.universe:
            csv_path = self.data_dir / f"{s.lower()}.csv"
            if not csv_path.exists():
                processed[s] = 0
                continue
            bars = load_bars(csv_path)
            new = [b for b in bars
                   if s not in self.last_date or b["date"] > self.last_date[s]]
            for i, b in enumerate(new):
                self.strat.on_bar_close(s, b["date"], b["open"], b["high"],
                                        b["low"], b["close"], b["volume"])
                # paper fills: pending order fills at this bar's close
                if s in self.strat._pending:
                    self.strat.on_order_fill(s, b["close"])
                self.last_date[s] = b["date"]
                last_close[s] = b["close"]
            processed[s] = len(new)
        self.strat.on_session_end()
        # execute the session-close flatten rule: fill pending flatten
        # tickets at each instrument's last close (previously dropped)
        for s, ticket in list(self.strat._pending.items()):
            if s in last_close:
                self.strat.on_order_fill(s, last_close[s])
        self._save_state()
        return processed

    def report(self) -> dict:
        return spi_monitor.audit_parity(self.strat)


def main() -> None:
    ap = argparse.ArgumentParser(description="VP-MR paper-trading runner")
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--state-dir", required=True, type=Path)
    ap.add_argument("--report", action="store_true",
                    help="print SPI audit report after the session")
    args = ap.parse_args()

    runner = PaperTradingRunner(args.data_dir, args.state_dir)
    processed = runner.run_session()
    print("bars processed:", processed)
    print("positions:", {s: runner.strat.position[s]
                          for s in runner.universe})
    print("equity (cost-adjusted):", round(runner.strat.equity, 2))
    if args.report:
        for k, v in runner.report().items():
            print(f"  {k:>18}: {v}")


if __name__ == "__main__":
    main()
