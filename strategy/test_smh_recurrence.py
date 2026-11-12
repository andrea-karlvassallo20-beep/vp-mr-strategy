"""SMH recurrence suite: the long-run lemma's preconditions
measured against KNOWN ground truth both ways - a fully cycling
regime chain must read irreducible with a positive trigger rate,
and a chain with an absorbing state must read NOT irreducible
(the verdict is mechanical, not narrative). Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from smh_recurrence import run_recurrence

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, rets):
    prices = 100.0 * np.exp(np.cumsum(rets))
    d0 = _dt.date(2012, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000.0))
    write_csv(path, rows)


# --- ground truth: a fully cycling chain -----------------------------
# three vol levels cycling: quiet -> moderate -> hot -> quiet ...
# every directed link fires, none absorbing
rng = np.random.default_rng(4)
n = 9000
rets = np.zeros(n)
levels = [0.0015, 0.006, 0.03]
for t in range(n):
    rets[t] = levels[(t // 300) % 3] * rng.standard_t(6)
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
_write_series(data / "CYCUSD.csv", rets)

r = run_recurrence(data)
tm = r["transition_matrix"]
check("transition matrix carries all nine cells",
      len(tm) == 9 and all(
          v["count"] >= 0 for v in tm.values()))
row_sums = {}
for key, v in tm.items():
    a = key.split("->")[0]
    row_sums[a] = row_sums.get(a, 0) + (v["probability"] or 0)
check("each region's exit probabilities sum to ~1",
      all(abs(s - 1.0) < 0.02 for s in row_sums.values()
          if s > 0))
check("ground truth: the cycling chain reads irreducible",
      r["irreducibility"]["irreducible"] is True
      and r["irreducibility"]["all_six_directed_links_observed"])
check("ground truth: trigger recurrence is positive",
      r["trigger_recurrence"]["triggers_per_market_year"] > 0)
check("the irreducible verdict carries the actuarial statement",
      "actuarially inevitable" in
      r["irreducibility"]["statement"])

# --- ground truth 2: an absorbing state ------------------------------
# the chain cycles only between quiet and mid (stress never
# entered), then a long hot tail to the data edge: stress is
# entered exactly once and never left - absorbing, and the
# verdict must fail mechanically
rng = np.random.default_rng(4)
rets_a = np.zeros(n)
for t in range(n):
    lvl = (levels[(t // 300) % 2] if t < 6000 else 0.3)
    rets_a[t] = lvl * rng.standard_t(6)
data2 = tmp / "absorb"
data2.mkdir()
_write_series(data2 / "ABSUSD.csv", rets_a)
r_a = run_recurrence(data2)
check("absorbing control: stress never exits (count 0 out)",
      all(v["count"] == 0 for k, v in
          r_a["transition_matrix"].items()
          if k.startswith("stress->") and not
          k.endswith("->stress")))
check("absorbing control: the chain reads NOT irreducible "
      "(the verdict is mechanical, not narrative)",
      r_a["irreducibility"]["irreducible"] is False
      and r_a["irreducibility"]["all_six_directed_links_observed"]
      is False)

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
