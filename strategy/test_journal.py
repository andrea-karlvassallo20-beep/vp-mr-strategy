"""Journal suite: append, idempotent same-day update, new-day append,
header bootstrap. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from journal import journal_entry, update_journal, HEADER
from vp_mr_strategy import StrategyParameters

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
state_dir = tmp / "state"
journal = tmp / "journal.md"

for i, t in enumerate(["SPY"]):
    write_csv(data_dir / f"{t.lower()}.csv", fetch_synthetic(t, 200, seed=5))
params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                           vol_est_lookback=30)
runner = PaperTradingRunner(data_dir, state_dir, params=params,
                            universe=["SPY"])
runner.run_session()

e1 = journal_entry(data_dir, state_dir, date="2026-01-01")
check("entry is a table row", e1.startswith("| 2026-01-01 |"))
check("bootstrap creates header", update_journal(journal, e1))
text = journal.read_text()
check("header present", HEADER in text and "# Paper-trading session journal" in text)

# same-day re-run with CHANGED metrics: row updated, not duplicated
sessions_cell = e1.split("|")[2].strip()
e1_changed = e1.replace(f"| {sessions_cell} |", "| 5/20 |")
assert e1_changed != e1, "mutation must change the entry"
check("same-day update applied", update_journal(journal, e1_changed))
text_now = journal.read_text()
check("no duplicate rows", text_now.count("| 2026-01-01 |") == 1)
check("row reflects the new value", "| 5/20 |" in text_now)

# idempotent: identical entry -> no change
check("identical entry is a no-op",
      not update_journal(journal, e1_changed))

# new day appends
e2 = journal_entry(data_dir, state_dir, date="2026-01-02")
check("new day appended", update_journal(journal, e2))
lines = [l for l in journal.read_text().splitlines() if l.startswith("| 2026")]
check("two dated rows in order", len(lines) == 2 and
      lines[0].startswith("| 2026-01-01") and lines[1].startswith("| 2026-01-02"))

# date auto-derived from state when not given
e3 = journal_entry(data_dir, state_dir)
check("date auto-derived", e3.split("|")[1].strip().startswith("20"))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
