"""Gate-check test: verify PROMOTE/HOLD verdicts fire correctly for
short (immature) and long (mature) paper sessions. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from gate_check import evaluate, to_markdown

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def run_session(n_bars, seed, universe=("SPY", "QQQ")):
    tmp = Path(tempfile.mkdtemp())
    data_dir = tmp / "data"; data_dir.mkdir()
    state_dir = tmp / "state"
    for i, t in enumerate(universe):
        write_csv(data_dir / f"{t.lower()}.csv",
                  fetch_synthetic(t, n_bars, seed=seed + i * 11))
    runner = PaperTradingRunner(data_dir, state_dir, universe=list(universe))
    runner.run_session()
    return tmp, data_dir, state_dir


# --- immature session: 10 days -> HOLD ---
tmp1, d1, s1 = run_session(10, 700)
v1 = evaluate(d1, s1)
check("10-day session verdict HOLD", v1["verdict"] == "HOLD")
check("sessions counted = 10", v1["sessions_completed"] == 10)
check("sessions_required from run card = 20",
      v1["sessions_required"] == 20)
check("SPI criterion passes even while HOLD",
      any(c["criterion"] == "signal_parity_index" and c["pass"]
          for c in v1["criteria"]))
shutil.rmtree(tmp1)

# --- mature session: 60 days, criteria should pass -> PROMOTE ---
tmp2, d2, s2 = run_session(60, 800)
v2 = evaluate(d2, s2)
check("60-day session verdict PROMOTE", v2["verdict"] == "PROMOTE")
check("all criteria pass on mature session",
      all(c["pass"] for c in v2["criteria"]))
check("SPI >= 0.98 on mature session",
      v2["report_summary"]["audit_status"] == "PASS")
md = to_markdown(v2)
check("markdown shows PROMOTE", "PROMOTE" in md)
check("markdown lists all criteria", md.count("| YES |") == len(v2["criteria"]))
shutil.rmtree(tmp2)

print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
