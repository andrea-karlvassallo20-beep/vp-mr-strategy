"""SMH proof battery suite: structure, and ground truth both ways -
GARCH-like series must PROVE the laws, Gaussian iid must fail them.
Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from smh_proof import run_smh_proof

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def garch_series(n, seed):
    """Volatility clustering + heavy tails + calm/compressed starts:
    the laws 1, 2, 5 ground truth."""
    rng = np.random.default_rng(seed)
    rets = np.zeros(n)
    var = 0.0004
    for t in range(n):
        var = 0.95 * var + 0.05 * rets[t - 1] ** 2 if t else var
        rets[t] = math_sqrt(var) * rng.standard_t(5) / np.sqrt(5 / 3)
    return 100.0 * np.exp(np.cumsum(rets))


def math_sqrt(x):
    return float(np.sqrt(max(x, 0.0)))


def gaussian_series(n, seed):
    rng = np.random.default_rng(seed)
    return 100.0 * np.exp(np.cumsum(0.02 * rng.standard_normal(n)))


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()

# empty dir grace
r0 = run_smh_proof(data)
check("empty data dir reports honestly",
      r0["n_series"] == 0 and len(r0["laws"]) == 7)

# GROUND TRUTH: GARCH-like series must PROVE the vol laws
for i in range(4):
    p = garch_series(1200, 20 + i)
    rows = [(f"2020-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 10000)
            for j in range(1200)]
    write_csv(data / f"g{i}usd.csv", rows)
r = run_smh_proof(data)
check("GARCH ground truth: law 1 (vol persists) PROVEN",
      r["laws"]["law1_vol_persists"]["verdict"] == "PROVEN")
check("GARCH ground truth: law 2 (heavy tails) PROVEN",
      r["laws"]["law2_tails_heavy"]["verdict"] == "PROVEN")
check("GARCH ground truth: law 5 (self-excitation) PROVEN",
      r["laws"]["law5_self_excitation"]["verdict"] == "PROVEN")

# NEGATIVE control: Gaussian iid must NOT PROVE the heavy-tail and
# clustering laws
data2 = tmp / "gauss"
data2.mkdir()
for i in range(4):
    p = gaussian_series(1200, 60 + i)
    rows = [(f"2020-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 10000)
            for j in range(1200)]
    write_csv(data2 / f"n{i}usd.csv", rows)
r2 = run_smh_proof(data2)
check("Gaussian control: law 2 NOT PROVEN on iid normal",
      r2["laws"]["law2_tails_heavy"]["verdict"] == "NOT_PROVEN")
check("Gaussian control: law 5 weak or not proven on iid",
      r2["laws"]["law5_self_excitation"]["verdict"] in
      ("NOT_PROVEN",))

check("every law carries claim and verdict",
      all(set(("claim", "verdict")) <= set(v)
          for v in r["laws"].values()))
check("out-of-scope intraday items recorded honestly",
      "intraday" in r["untestable_here"])

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
