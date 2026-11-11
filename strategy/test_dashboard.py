"""Dashboard test: generation from a synthetic session + empty-state
grace. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from dashboard import build_html

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
for i, t in enumerate(["SPY", "QQQ"]):
    write_csv(data_dir / f"{t.lower()}.csv", fetch_synthetic(t, 300, seed=7 + i))
runner = PaperTradingRunner(data_dir, tmp / "state", universe=["SPY", "QQQ"])
runner.run_session()

html = build_html(tmp / "state" and tmp)
check("html generated", len(html) > 4000)
check("metric cards present", html.count('class="card"') == 8)
check("equity curve SVG rendered", "<svg" in html and "polyline" in html)
check("verification matrix present", "Cross-engine parity" in html)
check("autonomous loop section present", "edge-seeker" in html)
check("work log timeline present", "Work log" in html and "False PROMOTE" in html)
check("no unescaped script injection", "<script" not in html)

empty = build_html(tmp / "nonexistent")
check("empty state graceful", "no session data yet" in empty)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
