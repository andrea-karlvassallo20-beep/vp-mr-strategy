"""Timing battery suite: the WHEN prediction measured against
KNOWN ground truth - episodes whose bounce peaks at a known
week must read that week, the realization fractions must match
the hand computation, and the region conditioning must report
its verdict honestly whatever the data says. Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from market_philosopher import HOLD_WEEKS, WEEK
from timing_battery import _episodes, _path_stats, run_timing

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, rets):
    prices = 100.0 * np.exp(np.cumsum(rets))
    d0 = _dt.date(2010, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000.0))
    write_csv(path, rows)


# --- episodes: the cross rule, once per episode -------------------------
rng = np.random.default_rng(7)
n = 4000
rets = 0.001 * rng.standard_t(6, size=n)
# one crash episode: the week 100-104 falls ~ -7%, then a bounce
rets[300:305] = -0.014
logc = np.cumsum(rets)
eps = _episodes(logc, n)
check("the episode fires at the cross, exactly once",
      len(eps) == 1 and 300 <= eps[0] <= 304)

# --- the path stats: a known recovery shape -----------------------------
# shape the bounce: +2% in week 1, +1% week 2, flat weeks 3-4
# -> peak at week 2, total +3%
t = eps[0]
for j in range(WEEK):
    rets[t + 1 + j] += 0.02 / WEEK
for j in range(WEEK):
    rets[t + 6 + j] += 0.01 / WEEK
logc = np.cumsum(rets)
run, peak_week, realized = _path_stats(logc, t)
check("the peak lands in the known week",
      peak_week == 2)
check("the weekly running returns rise then hold",
      run[0] > 0 and run[1] > run[0]
      and abs(run[2] - run[1]) < 0.005)
check("the realization fractions match the hand computation",
      realized[0] is not None
      and abs(realized[0] - run[0] / run[-1]) < 0.02)

# --- the full battery on a synthetic anchored universe ------------------
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
rng2 = np.random.default_rng(3)
n2 = 12000
base = 0.0015 * rng2.standard_t(6, size=n2)
# many crash episodes, each bouncing front-loaded
t2 = 200
while t2 < n2 - 60:
    if rng2.random() < 0.15:
        for j in range(5):
            base[t2 + j] = -0.015
        for j in range(10):
            base[t2 + 5 + j] += 0.004
        t2 += 60
    else:
        t2 += 1
_write_series(data / "BTCUSD.csv", base)
r = run_timing(data)
check("the battery returns the pooled card and the regions",
      r["status"] == "OK" and r["pooled"]["n"] > 20
      and set(r["by_region"]) == {"compression", "mid",
                                  "stress"})
check("the pooled card carries the timing prediction fields",
      set(("median_peak_week", "p_positive_week1",
           "p_positive_week4", "median_fraction_realized_"
           "by_week2")) <= set(r["pooled"]))
check("the region verdict is stated honestly either way",
      "validated" in r["region_verdict"]["statement"]
      or "unproven" in r["region_verdict"]["statement"])
check("the candidate timing card names its purpose",
      "prediction on timing" in
      r["candidate_timing_card"]["statement"])

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
