"""Alert suite: every condition triggers (and none false-positives) on
synthetic states. Issue creation is only formatted, never called.
Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from alert import check_alerts, issue_title, issue_body
from vp_mr_strategy import StrategyParameters

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def make_state(tmp, seed, universe=("SPY",), mutate=None):
    data_dir = tmp / f"data_{seed}"; data_dir.mkdir(parents=True)
    state_dir = tmp / f"state_{seed}"
    for t in universe:
        write_csv(data_dir / f"{t.lower()}.csv",
                  fetch_synthetic(t, 200, seed=seed))
    params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                                vol_est_lookback=30)
    r = PaperTradingRunner(data_dir, state_dir, params=params,
                           universe=list(universe))
    r.run_session()
    if mutate:
        mutate(state_dir / "session_state.json")
    return data_dir, state_dir


tmp = Path(tempfile.mkdtemp())

def mutate_kill_switch(p):
    s = json.load(open(p))
    for rec in s["decision_log"]:
        rec["kill_switch"] = True
    json.dump(s, open(p, "w"))

def mutate_spi(p):
    s = json.load(open(p))
    for rec in s["decision_log"]:
        rec["signal"] = 99  # breaks parity recomputation
    json.dump(s, open(p, "w"))

def mutate_dup(p):
    s = json.load(open(p))
    for rec in s["decision_log"]:
        rec["blocked_at_decision"] = True
        rec["signal"] = 1
    json.dump(s, open(p, "w"))


# clean session -> no alerts
d, s = make_state(tmp, 1)
check("clean session produces no alerts", check_alerts(d, s) == [])

# kill-switch trips -> critical alert
d, s = make_state(tmp, 2, mutate=mutate_kill_switch)
alerts = check_alerts(d, s)
check("kill-switch trips detected",
      any(a["condition"] == "KILL_SWITCH_TRIPPED" and
          a["severity"] == "critical" for a in alerts))

# SPI degradation -> critical alert
d, s = make_state(tmp, 3, mutate=mutate_spi)
alerts = check_alerts(d, s)
check("SPI degradation detected",
      any(a["condition"] == "SPI_DEGRADED" for a in alerts))

# duplicate fires -> critical alert
d, s = make_state(tmp, 4, mutate=mutate_dup)
alerts = check_alerts(d, s)
check("duplicate fires detected",
      any(a["condition"] == "DUPLICATE_ORDER_FIRES" for a in alerts))

# race report PROPOSE_REDEPLOY -> notice
d, s = make_state(tmp, 5)
(s.parent / "challenger_report.md").write_text(
    "# Challenger report\n\n**Recommendation: PROPOSE_REDEPLOY**\n")
alerts = check_alerts(d, s)
check("redeploy proposal notice detected",
      any(a["condition"] == "REDEPLOY_PROPOSAL_PENDING" and
          a["severity"] == "notice" for a in alerts))

# title and body formatting
fake = [{"condition": "X", "severity": "critical", "evidence": "ev"}]
check("critical title", "[ALERT]" in issue_title(fake))
check("notice title without criticals",
      "[NOTICE]" in issue_title(
          [{"condition": "Y", "severity": "notice", "evidence": "e"}]))
body = issue_body(fake)
check("body carries condition and evidence", "X" in body and "ev" in body)
check("body points to audit trail", "paper/" in body)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
