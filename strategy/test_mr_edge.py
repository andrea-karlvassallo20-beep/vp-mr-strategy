"""MR-coin edge suite: causality of the z-core, the dead-coin filter,
control-group honesty, and ground truth on synthetic OU vs random
walk coins. Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from mr_edge import (causal_z, run_mr_edge_study, zscore_long_backtest)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def ou_coin(n, seed, kappa=0.05, sigma=0.02):
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = x[t - 1] * (1 - kappa) + sigma * rng.standard_normal()
    return 100.0 * np.exp(x - x.min())


def rw_coin(n, seed, drift=0.0005):
    rng = np.random.default_rng(seed)
    return 100.0 * np.exp(np.cumsum(drift
                                    + 0.02 * rng.standard_normal(n)))


# --- causality ---------------------------------------------------------
c = ou_coin(600, 1)
z = causal_z(c)
z_shift = causal_z(np.concatenate([c, [c[-1] * 1.5]]))[:600]
check("causal z is untouched by future bars (Gate 1)",
      np.allclose(z, z_shift, atol=1e-12))

# --- the z-core backtest ------------------------------------------------
b = zscore_long_backtest(c)
check("z-long backtest produces trades and finite returns",
      b["trades"] > 0 and np.isfinite(b["rets"]).all()
      and len(b["rets"]) == len(c) - 1)

# --- ground truth: OU coins vs random walks -----------------------------
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
for i in range(6):
    rows = [(f"2023-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             ou_coin(800, 10 + i)[j] * 1.01,
             ou_coin(800, 10 + i)[j] * 1.01,
             ou_coin(800, 10 + i)[j] * 0.99,
             ou_coin(800, 10 + i)[j], 1_000_000)
            for j in range(800)]
    write_csv(data / f"ou{i}usd.csv", rows)
for i in range(6):
    p = rw_coin(800, 50 + i)
    rows = [(f"2023-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 1_000_000)
            for j in range(800)]
    write_csv(data / f"rw{i}usd.csv", rows)

r = run_mr_edge_study(data)
check("study separates OU coins from random walks by t-stat",
      len([x for x in r["mr_runs"]
           if x["ticker"].startswith("OU")]) >= 4
      and len([x for x in r["control_runs"]
               if x["ticker"].startswith("RW")]) >= 4)
check("study reports pooled stats, edge and verdict fields",
      all(k in r for k in
          ("mr_pooled_oos_sharpe", "control_pooled_oos_sharpe",
           "edge_differential", "verdict", "deflated_sharpe",
           "confirmed_fwd_median", "plain_fwd_median")))
check("OU group beats the random-walk control group",
      r["mr_pooled_oos_sharpe"] > r["control_pooled_oos_sharpe"])
check("verdict is a bool and DSR carries trial context",
      isinstance(r["verdict"], bool)
      and r["deflated_sharpe"]["n_trials"] >= 12)

# --- the dead-coin filter ------------------------------------------------
dead = ou_coin(400, 99)
dead[-1] = dead.max() / 5000.0   # terminal collapse
rows = [(f"2023-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
         dead[j] * 1.01, dead[j] * 1.01, dead[j] * 0.99, dead[j],
         1_000_000) for j in range(400)]
write_csv(data / "deadusd.csv", rows)
r2 = run_mr_edge_study(data)
check("dead coin (priced 1000x below peak) is excluded",
      all(x["ticker"] != "DEADUSD"
          for x in r2["mr_runs"] + r2["control_runs"]))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
