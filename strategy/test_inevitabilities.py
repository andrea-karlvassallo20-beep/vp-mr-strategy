"""Structural inevitabilities suite: verdict logic, ground truth
on synthetic series with KNOWN structure, and honest reporting
fields. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from inevitabilities import run_inevitabilities

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()

# empty dir grace
r0 = run_inevitabilities(data)
check("empty data dir reports honestly",
      r0["n_series"] == 0 and len(r0["claims"]) == 5)

# ground truth 1: impulsive series - 3% of bars carry huge moves
for i in range(4):
    rng = np.random.default_rng(10 + i)
    p = np.zeros(900)
    lvl = 100.0
    for t in range(1, 900):
        shock = 0.30 if rng.random() < 0.03 else 0.004
        lvl *= (1 + shock * rng.standard_normal())
        p[t] = lvl
    p = np.abs(p) + 1.0
    rows = [(f"2022-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 10000)
            for j in range(900)]
    write_csv(data / f"imp{i}usd.csv", rows)

r = run_inevitabilities(data)
check("impulsive synthetic series reads STRUCTURAL concentration",
      r["claims"]["impulse_concentration"]["verdict"] == "STRUCTURAL"
      and r["claims"]["impulse_concentration"]
      ["concentration_ratio_top5"] > 3.0)
check("every claim carries a verdict and a description",
      all(set(("description", "verdict")) <= set(v)
          for v in r["claims"].values()))

# ground truth 2: calm anchored series with engineered crash bounces
data2 = tmp / "anchored"
data2.mkdir()
for i in range(4):
    rng = np.random.default_rng(50 + i)
    p = np.zeros(900)
    lvl = 100.0
    last_crash = -100
    for t in range(1, 900):
        r_ = rng.standard_normal()
        if r_ < -2.4 and t - last_crash > 40:
            last_crash = t            # engineered crash bar...
            lvl *= (1 - 0.08)
            p[t] = lvl
            lvl *= (1 + 0.06)         # ...that BOUNCES next bars
            continue
        lvl *= (1 + 0.002 + 0.004 * r_)
        p[t] = lvl
    p = np.abs(p) + 1.0
    rows = [(f"2022-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 10000)
            for j in range(900)]
    write_csv(data2 / f"an{i}f.csv", rows)
r2 = run_inevitabilities(data2)
check("engineered crash-bounce series reads STRUCTURAL_ON_ANCHORED",
      r2["claims"]["crash_bounce"]["verdict"]
      == "STRUCTURAL_ON_ANCHORED"
      and r2["claims"]["crash_bounce"]["anchored_p_positive"] > 0.55)

# untestable-here note is honest
check("intraday rules recorded as out of scope",
      "intraday" in r["untestable_on_dailies"])

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
