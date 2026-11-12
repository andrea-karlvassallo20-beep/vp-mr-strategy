"""SMH Bayesian forecaster suite: the blend measured against
KNOWN ground truth both ways - a human who is genuinely better
calibrated than the model must earn weight and the blend must
beat the model; a human who is noise must earn zero weight (the
shrinkage protects the record); and a young record (under the
pre-declared minimum) must earn zero weight however good the
early numbers look. Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from smh_bayes import (MIN_SCORED, W_CAP, _logit, _sigmoid,
                       human_weight, run_bayes)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# --- the logit helpers round-trip -------------------------------------
check("logit/sigmoid round-trip",
      abs(_sigmoid(_logit(0.7)) - 0.7) < 1e-9)

# --- the weight rule, pre-declared -------------------------------------
rng = np.random.default_rng(1)
good_human = [{"brier_human": 0.10, "brier_model": 0.20}
              ] * MIN_SCORED
noise_human = [{"brier_human": 0.20, "brier_model": 0.20}
               ] * MIN_SCORED
worse_human = [{"brier_human": 0.30, "brier_model": 0.20}
               ] * MIN_SCORED
young = good_human[:MIN_SCORED - 1]
check("a good record earns positive weight",
      0.4 < human_weight(good_human) <= W_CAP)
check("a noise record earns exactly zero",
      human_weight(noise_human) == 0.0)
check("a worse-than-model record earns exactly zero",
      human_weight(worse_human) == 0.0)
check("a young record earns zero however good it looks",
      human_weight(young) == 0.0)
check("the human never owns more than half the blend",
      W_CAP == 0.5 and human_weight(
          [{"brier_human": 0.0, "brier_model": 0.5}] * 100)
      <= W_CAP)

# --- end-to-end: the three-way scoreboard on synthetic rows -----------
tmp = Path(tempfile.mkdtemp())
res = tmp / "research"
res.mkdir()
# 30 resolved rows: the model forecasts 0.6; the human is
# genuinely sharper (calls the events at 0.8 when they happen,
# 0.3 when they do not)
rows = []
judgments = []
for i in range(30):
    y = 1 if i % 2 == 0 else 0
    rows.append({"ticker": f"T{i}", "kind": "compression",
                 "entry_index": i, "forecast_p": 0.6,
                 "status": "resolved", "outcome": y})
    judgments.append({
        "ticker": f"T{i}", "kind": "compression",
        "entry_index": i, "model_p": 0.6,
        "human_p": 0.8 if y else 0.3,
        "note": "synthetic", "logged_utc": "x",
        "outcome": y,
        "brier_human": round((0.8 if y else 0.3 - 0) ** 2
                             - ((0.8 if y else 0.3) - y) ** 2
                             + ((0.8 if y else 0.3) - y) ** 2, 4),
        "brier_model": round((0.6 - y) ** 2, 4),
    })
# fix brier_human properly (the expression above is deliberately
# the plain squared error)
for j in judgments:
    j["brier_human"] = round((j["human_p"] - j["outcome"]) ** 2, 4)
(res / "smh_forward.json").write_text(json.dumps({"rows": rows}))
(res / "smh_judgment.json").write_text(
    json.dumps({"judgments": judgments}))

r = run_bayes(res)
sb = r["scoreboard"]
check("30 scored judgments clear the pre-declared minimum",
      r["n_scored_judgments"] >= MIN_SCORED)
check("the good human earns weight",
      r["human_weight"] > 0.3)
check("the blend beats the model on the scoreboard",
      sb["blend_brier"] is not None
      and sb["blend_brier"] < sb["model_brier"])
check("the blend sits between the human and the model "
      "(logit-space averaging)",
      all(min(b["human_p"], b["model_p"]) - 1e-6
          <= b["blend_p"]
          <= max(b["human_p"], b["model_p"]) + 1e-6
          for b in r["blends"]))
check("the blend is a separate track: the forward row's "
      "logged forecast is untouched",
      all(b["model_p"] == 0.6 for b in r["blends"]))

# --- the young-record control: blend = model ---------------------------
j2 = judgments[:5]
(res / "smh_judgment.json").write_text(
    json.dumps({"judgments": j2}))
r2 = run_bayes(res)
check("a young record: the blend collapses to the model "
      "(shrinkage protects the record)",
      r2["human_weight"] == 0.0
      and all(abs(b["blend_p"] - b["model_p"]) < 1e-9
              for b in r2["blends"]))

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
