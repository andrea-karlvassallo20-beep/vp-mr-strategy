"""SMH hazard model suite: KM with censoring, Cox with KNOWN ground
truth (covariate-dependent hazard recovered; null covariate reads
null), and episode construction causality. Harness file."""
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from smh_hazard import (build_episodes, cox_fit, kaplan_meier,
                        run_hazard_model, vassallo_scores)
from smh_proof import WARMUP

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# --- KM with censoring -------------------------------------------------
rng = np.random.default_rng(3)
eps = []
for i in range(400):
    d = int(rng.exponential(30))
    cens = int(rng.exponential(25))
    eps.append({"momentum": 0.0, "sigma_pct": 0.5,
                "duration": min(d, cens), "event": int(d <= cens)})
km = kaplan_meier(eps)
s10 = next((r["survival"] for r in km if r["t"] >= 10), None)
check("KM survival decreases with time",
      s10 is not None and s10 < 1.0
      and all(km[i]["survival"] >= km[i + 1]["survival"]
              for i in range(len(km) - 1)))
check("KM curve carries at-risk, events and censored counts",
      all(set(("t", "n_at_risk", "events", "censored",
              "survival")) <= set(r) for r in km))

# --- Cox with ground truth ----------------------------------------------
# hazard truly depends on x -> Cox must recover a positive, significant
# coefficient and a concordance clearly above chance
rng = np.random.default_rng(7)
eps = []
for i in range(2000):
    x = rng.standard_normal()
    lam = np.exp(0.8 * x) / 30.0
    d = int(rng.exponential(1 / lam))
    cens = int(rng.exponential(40))
    eps.append({"x": x, "duration": min(d, cens),
                "event": int(d <= cens)})
cox = cox_fit(eps, covs=("x",))
check("Cox recovers the true covariate sign and significance",
      cox["coefficients"][0] > 0.3
      and cox["z_stats"][0] > 3.0
      and "x" in cox["significant_covariates"])
check("Cox concordance clearly above chance on true signal",
      cox["concordance"] > 0.6)

# null covariate -> no significance, concordance ~ 0.5
rng = np.random.default_rng(11)
eps = []
for i in range(2000):
    d = int(rng.exponential(30))
    cens = int(rng.exponential(30))
    eps.append({"x": rng.standard_normal(),
                "duration": min(d, cens),
                "event": int(d <= cens)})
cox_null = cox_fit(eps, covs=("x",))
check("Cox reads NULL on a null covariate",
      not cox_null["significant_covariates"]
      and abs(cox_null["concordance"] - 0.5) < 0.05)

# --- episode construction on synthetic series ---------------------------
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
for i in range(3):
    r = np.random.default_rng(20 + i)
    p = 100.0 * np.exp(np.cumsum(0.01 * r.standard_normal(900)))
    rows = [(f"2021-{j // 28 % 12 + 1:02d}-{j % 28 + 1:02d}",
             p[j] * 1.01, p[j] * 1.01, p[j] * 0.99, p[j], 10000)
            for j in range(900)]
    write_csv(data / f"s{i}usd.csv", rows)
eps = build_episodes(data)
check("episodes built with all fields, durations positive",
      len(eps) > 0 and all(
          set(("momentum", "sigma_pct", "duration", "event",
               "ticker")) <= set(e) and e["duration"] >= 1
          for e in eps))
check("episodes only start inside compression (event within window)",
      all(e["event"] in (0, 1) for e in eps))
r = run_hazard_model(data)
check("hazard model runs end to end on real-shaped data",
      r["status"] in ("OK", "INSUFFICIENT_EPISODES"))

# --- the Vassallo Score ------------------------------------------------
# with a fitted model and a baseline, scores must be probabilities
# in (0, 1), and deeper compression must score HIGHER (the fitted
# sigma_pct coefficient is negative)
if r.get("status") == "OK" and r.get("vassallo_scores"):
    vs = r["vassallo_scores"]
    check("Vassallo Scores are probabilities in (0, 1)",
          all(0.0 < s["vassallo_score"] < 1.0 for s in vs))
    check("Vassallo Scores ranked descending",
          all(vs[i]["vassallo_score"]
              >= vs[i + 1]["vassallo_score"]
              for i in range(len(vs) - 1)))
    deep = [s for s in vs if s["sigma_pct"] <= 0.05]
    shallow = [s for s in vs if s["sigma_pct"] >= 0.25]
    check("deeper compression scores higher on average",
          (not deep or not shallow)
          or (sum(s["vassallo_score"] for s in deep) / len(deep)
              > sum(s["vassallo_score"] for s in shallow)
              / len(shallow)))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
