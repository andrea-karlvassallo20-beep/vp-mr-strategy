"""Nightly pre-flight: simulates exactly what the scheduled session does,
end-to-end, on top of a persisted state — so tonight's run is de-risked
before it happens.

Simulates: session 1 (historical backfill) -> commit state -> session 2
(one new forward bar, exactly what the cron does each night) -> SPI audit
-> performance report -> promotion gate -> edge-seeker -> dashboards.
Harness file."""
import datetime
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np

from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from session_report import build_report
from gate_check import evaluate, to_markdown
from edge_seeker import CANDIDATES, seek, to_markdown as edge_md
from dashboard import build_html, build_markdown, build_site
from vp_mr_strategy import StrategyParameters

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
state_dir = tmp / "state"
params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                            vol_est_lookback=30)

# --- session 1: historical backfill (like the first real run) ---
for i, t in enumerate(["SPY", "QQQ"]):
    write_csv(data_dir / f"{t.lower()}.csv",
              fetch_synthetic(t, 300, seed=31 + i))
r1 = PaperTradingRunner(data_dir, state_dir, params=params,
                        universe=["SPY", "QQQ"])
r1.run_session()
check("session 1 (backfill) completes", r1.invocations == 1)

# --- session 2: exactly what the cron does — one new bar per instrument ---
for i, t in enumerate(["SPY", "QQQ"]):
    bars = fetch_synthetic(t, 300, seed=31 + i)
    last_date = datetime.date.fromisoformat(bars[-1][0])
    c = float(bars[-1][4]) * 1.001
    new_bar = ((last_date + datetime.timedelta(days=1)).isoformat(),
               c, c * 1.002, c * 0.998, c, 1e6)
    write_csv(data_dir / f"{t.lower()}.csv", bars + [new_bar])

r2 = PaperTradingRunner(data_dir, state_dir, params=params,
                        universe=["SPY", "QQQ"])
processed = r2.run_session()
check("session 2 consumes the new forward bar",
      processed["SPY"] == 1 and processed["QQQ"] == 1)
check("invocations increment to 2 (forward session counted)",
      r2.invocations == 2)

# --- downstream artifacts, exactly as the nightly workflow runs them ---
rep = build_report(data_dir, state_dir)
check("performance report builds from persisted state",
      rep["sessions_bars"] == 301 and rep["spi"] >= 0.98)

v = evaluate(data_dir, state_dir)
check("promotion gate reads invocation counter: HOLD at 2/20",
      v["verdict"] == "HOLD" and v["sessions_completed"] == 2)
check("gate markdown renders", "HOLD" in to_markdown(v))

r = seek(data_dir, ["SPY", "QQQ"])
check("edge-seeker research pass completes on the grown window",
      r["status"] == "OK" and len(r["grid"]) == len(CANDIDATES))
check("edge report renders", "Recommendation" in edge_md(r))

html = build_html(state_dir and tmp)
md = build_markdown(state_dir and tmp)
site = build_site(state_dir and tmp)
check("dashboard.html regenerates", "<svg" in html)
check("DASHBOARD.md regenerates", "Gate verdict" in md)
check("Salient site regenerates", "Salient" in site)

# --- idempotency: a same-day re-run must not double-count ---
r3 = PaperTradingRunner(data_dir, state_dir, params=params,
                        universe=["SPY", "QQQ"])
processed = r3.run_session()
check("re-run on same data consumes nothing and does not increment",
      processed["SPY"] == 0 and r3.invocations == 2)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
