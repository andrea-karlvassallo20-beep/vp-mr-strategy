"""Commodity edge battery suite: structure, ground truth (OU futures
pass), and the honest verdict fields. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from commodity_edge import run_commodity_edge_study

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def ou_futures(n, seed, kappa=0.06, sigma=0.015):
    r = np.random.default_rng(seed)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = x[t - 1] * (1 - kappa) + sigma * r.standard_normal()
    return 100.0 * np.exp(x - x.min())


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()

# empty dir grace
r0 = run_commodity_edge_study(data)
check("empty data dir reports honestly",
      r0["status"] == "NO_DATA")

# ground truth: OU futures should PASS the battery
for i in range(8):
    p = ou_futures(900, 30 + i)
    rows = [(f"2022-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 10000)
            for j in range(900)]
    write_csv(data / f"cm{i}f.csv", rows)

r = run_commodity_edge_study(data)
check("battery carries every gate metric",
      all(k in r["battery"] for k in
          ("pooled_oos_worse_window", "time_split_first_half",
           "time_split_second_half", "cost_stress_2x_pooled_oos",
           "positive_markets", "top5_concentration",
           "deflated_sharpe")))
check("OU futures PASS the battery (ground truth)",
      r["verdict"] is True
      and r["battery"]["pooled_oos_worse_window"] > 1.0
      and r["battery"]["cost_stress_2x_pooled_oos"] > 0
      and r["battery"]["positive_markets"] == "8/8")
check("DSR context deflates by the number of markets",
      r["battery"]["deflated_sharpe"]["n_trials"] == 8)
check("markets carry per-attribution fields",
      all(set(("ticker", "mr_t_stat", "half_life", "trades",
               "full", "oos_40", "first_half", "second_half"))
          <= set(m) for m in r["markets"]))
check("next step recorded for the pass case",
      "challenger" in r["next_step_if_pass"])

# random-walk futures should FAIL
data2 = tmp / "rw"
data2.mkdir()
for i in range(8):
    p = 100.0 * np.exp(np.cumsum(
        0.0005 + 0.015 * np.random.default_rng(
            70 + i).standard_normal(900)))
    rows = [(f"2022-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 10000)
            for j in range(900)]
    write_csv(data2 / f"rw{i}f.csv", rows)
r2 = run_commodity_edge_study(data2)
check("random-walk futures FAIL the battery (ground truth)",
      r2["verdict"] is False)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
