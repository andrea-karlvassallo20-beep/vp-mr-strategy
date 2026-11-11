"""Runner test: incremental CSV sessions, state persistence across
restarts, idempotent re-runs, SPI gate. Harness file (stdlib I/O allowed)."""
import datetime
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import PaperTradingRunner
from vp_mr_strategy import StrategyParameters

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def write_csv(path, bars):
    with open(path, "w", newline="") as f:
        f.write("date,open,high,low,close,volume\n")
        for b in bars:
            f.write(f"{b[0]},{b[1]},{b[2]},{b[3]},{b[4]},{b[5]}\n")


def ou_bars(n, seed, s0=450.0, theta=0.05, sigma=1.2, start_day=0):
    """Monotonic ISO dates: one bar per calendar day from start_day."""
    rng = np.random.default_rng(seed)
    p = np.empty(n); p[0] = s0
    for i in range(1, n):
        p[i] = p[i-1] + theta * (s0 - p[i-1]) + rng.normal(0, sigma)
    bars = []
    for i in range(n):
        c = float(p[i])
        d = (datetime.date(2024, 1, 1) +
             datetime.timedelta(days=start_day + i)).isoformat()
        bars.append((d, c, c*1.002, c*0.998, c, 1e6))
    return bars


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
state_dir = tmp / "state"

params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                            vol_est_lookback=30)
bars = ou_bars(400, 42)
write_csv(data_dir / "spy.csv", bars)

# --- invocation 1: first 400 bars ---
r1 = PaperTradingRunner(data_dir, state_dir, params=params, universe=["SPY"])
processed = r1.run_session()
check("first invocation processes 400 bars", processed["SPY"] == 400)
check("backfill counts as ONE session invocation", r1.invocations == 1)
pos_after_1 = dict(r1.strat.position)
eq_after_1 = r1.strat.equity
log_after_1 = len(r1.strat.decision_log)
check("state file created", (state_dir / "session_state.json").exists())

# --- invocation 2: re-run same data (idempotency) ---
r2 = PaperTradingRunner(data_dir, state_dir, params=params, universe=["SPY"])
processed = r2.run_session()
check("re-run consumes 0 new bars (idempotent)", processed["SPY"] == 0)
check("positions unchanged on re-run", r2.strat.position == pos_after_1)
check("equity unchanged on re-run", r2.strat.equity == eq_after_1)
check("decision log not duplicated", len(r2.strat.decision_log) == log_after_1)

# --- invocation 3: append 100 new bars, restart from persisted state ---
bars += ou_bars(100, 43, start_day=400)
write_csv(data_dir / "spy.csv", bars)
r3 = PaperTradingRunner(data_dir, state_dir, params=params, universe=["SPY"])
processed = r3.run_session()
check("restart consumes only 100 new bars", processed["SPY"] == 100)
check("second forward session increments invocations", r3.invocations == 2)
check("bounded trailing buffer restored at capacity",
      len(r3.strat._close["SPY"]) == 65)  # min_history(60) + 5, by design
check("session-close flatten executed (positions flat)",
      all(q == 0.0 for q in r3.strat.position.values()))
check("flatten fills recorded in order log",
      any(o.get("reason") == "SESSION_CLOSE_FLATTEN"
          for o in r3.strat.order_log))
check("no pending tickets left after session", not r3.strat._pending)

# --- SPI gate on the combined session ---
rep = r3.report()
check("SPI >= 0.98 across restarts", rep["spi"] >= 0.98)
check("no duplicate fires", rep["duplicate_fires"] == 0)
check("audit status PASS", rep["status"] == "PASS")

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
