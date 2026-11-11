"""Session report test: run a runner session on synthetic data, then verify
the report generated from the persisted state is consistent with the live
strategy instance. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from session_report import build_report, to_markdown
from vp_mr_strategy import StrategyParameters

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
state_dir = tmp / "state"

for i, t in enumerate(["SPY", "QQQ"]):
    write_csv(data_dir / f"{t.lower()}.csv",
              fetch_synthetic(t, 400, seed=555 + i * 11))

params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                            vol_est_lookback=30)
runner = PaperTradingRunner(data_dir, state_dir, params=params,
                            universe=["SPY", "QQQ"])
processed = runner.run_session()
check("session ran over 400 bars", processed["SPY"] == 400)

rep = build_report(data_dir, state_dir)
check("report generated", isinstance(rep, dict))
check("sessions_bars matches feed", rep["sessions_bars"] == 400)
check("SPI consistent with live instance",
      rep["spi"] == runner.strat.signal_parity_index())
check("audit status PASS", rep["audit_status"] == "PASS")
check("fills consistent with live order log",
      rep["fills"] == sum(1 for o in runner.strat.order_log
                          if o.get("state") == "FILLED"))
check("positions consistent",
      rep["open_positions"] == {s: q for s, q in runner.strat.position.items()
                                 if q != 0.0})
check("equity internal consistent",
      rep["equity_internal_cost_only"] == round(runner.strat.equity, 2))
check("MTM equity finite and positive", rep["final_equity_mtm"] > 0)

md = to_markdown(rep)
check("markdown renders", "| Metric | Value |" in md and "session report" in md)
check("markdown written", len(md.splitlines()) > 10)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
