"""Edge-seeker test: honest walk-forward proposal machinery on synthetic
data. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_synthetic, write_csv
from edge_seeker import seek, to_markdown, CANDIDATES

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
for i, t in enumerate(["SPY", "QQQ"]):
    write_csv(data_dir / f"{t.lower()}.csv", fetch_synthetic(t, 400, seed=99 + i))

r = seek(data_dir, ["SPY", "QQQ"])
check("seek returns OK", r["status"] == "OK")
check("full grid evaluated", len(r["grid"]) == len(CANDIDATES))
check("recommendation is a valid action",
      r["recommendation"] in ("KEEP_PRODUCTION", "PROPOSE_REDEPLOY"))
check("OOS windows actually scored (warm-up fix)",
      r["oos_selected"]["sharpe"] != 0.0 or r["oos_production"]["sharpe"] != 0.0)
check("selected candidate comes from the grid",
      (r["selected_candidate"]["z_entry"], r["selected_candidate"]["lookback"])
      in CANDIDATES)

md = to_markdown(r)
check("markdown carries recommendation",
      r["recommendation"] in md)
check("markdown carries Gate 3 freeze note", "frozen" in md)
check("markdown carries the full grid table", md.count("| 1.5 |") >= 3)

# empty data dir handled
r2 = seek(tmp / "empty", ["SPY"])
check("missing data returns NO_DATA", r2["status"] == "NO_DATA")
check("NO_DATA markdown is graceful", "No data" in to_markdown(r2))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
