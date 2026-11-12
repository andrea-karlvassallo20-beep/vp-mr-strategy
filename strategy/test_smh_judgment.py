"""SMH judgment log suite: the human inside the protocol, tested
against the doctrine rules - advance or not at all (rule 2),
never revised (rule 2), append-only (rule 6), and the scoring
machinery (the human's Brier next to the model's, hand-checked).
Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from smh_judgment import record_judgment, resolve_judgments

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
res = tmp / "research"
res.mkdir()
fw = {
    "rows": [
        {"ticker": "BTCUSD", "kind": "compression",
         "entry_index": 1000, "forecast_p": 0.65,
         "status": "open", "outcome": None},
        {"ticker": "ETHUSD", "kind": "compression",
         "entry_index": 900, "forecast_p": 0.60,
         "status": "resolved", "outcome": 1},
    ],
}
(res / "smh_forward.json").write_text(json.dumps(fw))

# --- rule 2: advance or not at all ------------------------------------
r = record_judgment(res, "ETHUSD", 0.9, "too late")
check("a judgment against a RESOLVED row is rejected",
      r["status"] == "REJECTED")
r = record_judgment(res, "NOPEUSD", 0.9, "no such row")
check("a judgment against a nonexistent row is rejected",
      r["status"] == "REJECTED")
r = record_judgment(res, "BTCUSD", 1.5, "not a probability")
check("a non-probability is rejected",
      r["status"] == "REJECTED")

# --- a valid judgment records with the model's p beside it ------------
r = record_judgment(res, "BTCUSD", 0.7, "coiling since October")
check("a valid judgment against an OPEN row is recorded",
      r["status"] == "RECORDED" and r["model_p"] == 0.65
      and r["human_p"] == 0.7)
r = record_judgment(res, "BTCUSD", 0.8, "changed my mind")
check("a second judgment on the same row is rejected "
      "(never revised)",
      r["status"] == "REJECTED")

# --- the nightly pass scores nothing while the row is open -----------
rp = resolve_judgments(res)
check("no scoring while the row is open",
      rp["n_scored"] == 0 and rp["human_brier"] is None)

# --- resolution: the human's Brier next to the model's ---------------
fw["rows"][0]["status"] = "resolved"
fw["rows"][0]["outcome"] = 1
(res / "smh_forward.json").write_text(json.dumps(fw))
rp = resolve_judgments(res)
check("the resolved row scores the judgment",
      rp["n_scored"] == 1 and rp["scored_tonight"] == 1)
check("human Brier matches the hand computation",
      abs(rp["human_brier"] - round((0.7 - 1) ** 2, 4)) < 1e-9)
check("model Brier matches the hand computation",
      abs(rp["model_brier"] - round((0.65 - 1) ** 2, 4)) < 1e-9)

# --- append-only: outcomes fill in, nothing rewritten ------------------
log = json.loads((res / "smh_judgment.json").read_text())
check("the judgment keeps its logged prior and note",
      log["judgments"][0]["human_p"] == 0.7
      and log["judgments"][0]["note"] == "coiling since October")
rp2 = resolve_judgments(res)
check("re-running the pass is idempotent (append-only)",
      rp2["n_scored"] == 1 and rp2["scored_tonight"] == 0)

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
