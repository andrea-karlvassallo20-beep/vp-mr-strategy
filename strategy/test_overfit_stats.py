"""Overfitting-statistics suite: PSR, DSR, PBO on synthetic
strategies with KNOWN ground truth (pure noise must fail, a real
edge must pass). Harness file."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from overfit_stats import (deflated_sharpe, expected_max_sharpe,
                           pbo_cscv, probabilistic_sharpe,
                           sharpe_stats)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


rng = np.random.default_rng(42)

# --- moments -----------------------------------------------------------
r = rng.normal(0.001, 0.01, 2000)
s = sharpe_stats(r)
check("sharpe stats on iid normal are sane",
      abs(s["sr"]) < 1.0 and abs(s["skew"]) < 0.2
      and abs(s["kurt"] - 3.0) < 0.3 and s["n"] == 2000)

# --- PSR ----------------------------------------------------------------
check("PSR of a positive-mean series vs 0 benchmark is high",
      probabilistic_sharpe(r, 0.0) > 0.95)
check("PSR of a series vs its OWN sample sharpe is exactly 0.5",
      abs(probabilistic_sharpe(r, s["sr"]) - 0.5) < 1e-6)

# --- expected max sharpe -------------------------------------------------
noise_sharpes = [sharpe_stats(rng.normal(0, 0.01, 1000))["sr"]
                 for _ in range(100)]
emax = expected_max_sharpe(noise_sharpes)
check("E[max SR] of 100 zero-skill trials is meaningfully positive",
      0.5 < emax < 3.0)
check("E[max SR] grows with more trials",
      expected_max_sharpe(noise_sharpes + noise_sharpes)
      > expected_max_sharpe(noise_sharpes[:10]))

# --- DSR: the ground-truth tests ---------------------------------------
# 100 pure-noise strategies, the best is the luckiest coin-flip
noise_strats = [rng.normal(0, 0.01, 1000) for _ in range(100)]
best_noise = max(noise_strats, key=lambda x: x.mean())
d_noise = deflated_sharpe(best_noise,
                          [sharpe_stats(x)["sr"]
                           for x in noise_strats])
check("DSR CONVICTS the best of 100 noise strategies",
      not d_noise["passes_95"] and d_noise["dsr"] < 0.95)

# one true edge among noise (annual Sharpe ~3, above the
# ~1.3 the 100-trial search would manufacture from pure luck)
edge = rng.normal(0.002, 0.01, 1000)
d_edge = deflated_sharpe(edge, [sharpe_stats(x)["sr"]
                                for x in noise_strats])
check("DSR PASSES a genuine edge searched alongside noise",
      d_edge["passes_95"])

# --- PBO ----------------------------------------------------------------
# identical-skill configs (shared noise + tiny idiosyncratic
# jitter): the IS winner is pure luck, so PBO scatters around
# the coin-flip level with sampling noise
base = rng.normal(0, 0.01, (2000, 1))
m_same = base + rng.normal(0, 0.001, (2000, 50))
p_same = pbo_cscv(m_same, n_blocks=10)
check("PBO of identical-skill configs is a noisy coin flip",
      p_same["pbo"] is not None and 0.1 < p_same["pbo"] < 0.9)

# one persistent edge: the IS winner keeps winning OOS on every
# split, so PBO collapses to 0
m_edge = m_same.copy()
m_edge[:, 0] += 0.003
p_edge = pbo_cscv(m_edge, n_blocks=10)
check("PBO collapses to 0 when a real edge is present",
      p_edge["pbo"] is not None and p_edge["pbo"] < 0.05)
check("PBO discriminates edge from luck",
      p_edge["pbo"] < p_same["pbo"])

check("PBO handles degenerate input",
      pbo_cscv(np.ones((5, 1)), n_blocks=8)["pbo"] is None)

print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
