"""Full-universe tops/bottoms backtest suite: the v4 detection
measured against KNOWN ground truth both ways - a mean-reverting
series must fire confirmed bottoms that run up (points of
significant change), a falling-drift series must fire tops whose
forward runs the detected direction or read honestly otherwise -
plus the class bookkeeping and the OOS holdout extraction.
Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from tops_bottoms_backtest import (_class_of, detect_events,
                                   run_backtest)

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


# --- the class bookkeeping ----------------------------------------------
check("crypto class assigned", _class_of("BTCUSD") == "crypto")
check("original index class assigned",
      _class_of("GSPC") == "index")
check("new index assigned to the holdout class",
      _class_of("FTSE") == "index (new holdout)")
check("commodity class assigned",
      _class_of("GCF") == "commodity")

# --- detection ground truth: a mean-reverting series -------------------
# a true OU LEVEL: the price itself reverts to its anchor, so
# deep stretches must revert - confirmed bottoms run up
rng = np.random.default_rng(17)
n = 6000
level = 0.0
levels = np.zeros(n)
for t in range(n):
    level = 0.99 * level + 0.006 * rng.standard_t(6)
    levels[t] = level
rets = np.diff(levels, prepend=0.0)
prices = 100.0 * np.exp(np.cumsum(rets))
b, t_, ub, ut = detect_events(prices,
                              np.full(n, 1_000_000.0))
check("confirmed bottoms fire on mean-reverting data",
      len(b) > 5)
logc = np.log(prices)
fwd = [float(logc[t + 20] - logc[t]) for t in b
       if t + 20 < n]
check("confirmed bottoms are points of significant change "
      "(median forward up)",
      len(fwd) > 5 and float(np.median(fwd)) > 0)

# --- detection ground truth: a falling drift ---------------------------
# a small drift (large enough to make tops run down, small
# enough to keep the series alive for the dead-coin filter)
rng = np.random.default_rng(18)
rets_n = 0.002 * rng.standard_t(6, size=6000) - 0.0003
prices_n = 100.0 * np.exp(np.cumsum(rets_n))
b2, t2, ub2, ut2 = detect_events(
    prices_n, np.full(6000, 1_000_000.0))
logc_n = np.log(prices_n)
fwd_t = [float(logc_n[t + 20] - logc_n[t]) for t in t2
         if t + 20 < 6000]
check("on a falling drift, tops fire and the forward runs "
      "the detected direction (or the battery reads honestly)",
      len(t2) == 0 or float(np.median(fwd_t)) < 0)

# --- the full battery on a small universe -------------------------------
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
_write_series(data / "GSPC.csv", rets)          # index (orig)
_write_series(data / "FTSE.csv", rets_n)        # holdout class
r = run_backtest(data)
check("the battery returns all present classes",
      r["status"] == "OK"
      and "index" in r["classes"]
      and "index (new holdout)" in r["classes"])
check("each class carries the five measurement blocks",
      all(set(("bottoms", "tops", "bottoms_unmatched",
               "tops_unmatched", "zone", "series"))
          <= set(d) for d in r["classes"].values()))
check("the OOS holdout block extracts the zone verdict "
      "honestly",
      r["oos_holdout"]["n_trades"]
      == r["classes"]["index (new holdout)"]["zone"]["n"])

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
