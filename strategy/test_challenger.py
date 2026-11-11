"""Challenger suite: shadow session persistence, race evaluation,
Gate 3 honesty. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np

from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from challenger import (run_challenger_session, evaluate_race, to_markdown)
from vp_mr_strategy import StrategyParameters

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
champ_state = tmp / "champion"
chall_state = tmp / "challenger"

params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                            vol_est_lookback=30)
for i, t in enumerate(["SPY", "QQQ"]):
    write_csv(data_dir / f"{t.lower()}.csv",
              fetch_synthetic(t, 300, seed=17 + i))

# champion: the deployed strategy
champ = PaperTradingRunner(data_dir, champ_state, params=params,
                           universe=["SPY", "QQQ"])
champ.run_session()

# challenger: a candidate variant, shadow-traded on the same bars
candidate = {"z_entry": 1.5, "lookback": 60, "vol_model": "garch",
             "volume_filter": True, "train_sharpe": 0.0}
runner = run_challenger_session(data_dir, chall_state, candidate)
check("challenger shadow session completed",
      (chall_state / "session_state.json").exists())
check("challenger processed all bars",
      len(runner.strat.decision_log) == 600)

# idempotent re-run
runner2 = run_challenger_session(data_dir, chall_state, candidate)
check("challenger re-run idempotent (no new bars)",
      len(runner2.strat.decision_log) == 600)

# race evaluation
race = evaluate_race(data_dir, champ_state, chall_state, candidate)
check("race status OK on common window", race["status"] == "OK")
check("race window matches feed", race["bars"] == 300)
check("race verdict is a valid action",
      race["recommendation"] in ("PROPOSE_REDEPLOY", "KEEP_CHAMPION"))
check("champion metrics present",
      {"ret_pct", "sharpe", "max_dd_pct"} <= set(race["champion"]))
check("challenger metrics present",
      {"ret_pct", "sharpe", "max_dd_pct"} <= set(race["challenger"]))

md = to_markdown(race)
check("race markdown carries verdict", race["recommendation"] in md)
check("race markdown carries Gate 3 note", "frozen" in md)

# warming-up grace
empty_state = tmp / "empty"; empty_state.mkdir()
(empty_state / "session_state.json").write_text(
    '{"universe": [], "initial_equity": 1000000.0, "equity": 1000000.0,'
    '"positions": {}, "last_date": {}, "close_buf": {}, "high_buf": {},'
    '"low_buf": {}, "decision_log": [], "order_log": []}')
race2 = evaluate_race(data_dir, empty_state, chall_state, candidate)
check("degenerate state handled gracefully",
      race2["status"] in ("WARMING_UP", "OK"))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
