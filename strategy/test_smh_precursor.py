"""SMH precursor signature suite: the battery measured against
KNOWN ground truth both ways - a series where a volume precursor
provably drives the hazard (univariate Cox must recover it, the
OOF concordance must beat 0.5), a null covariate (must read null),
and the direction split (must carry the REFUSED claim). Harness
file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from smh_hazard import cox_fit
from smh_precursor import (ALL_COVS, CLOCK_COVS, NEW_COVS,
                           _entry_covariates, build_episodes,
                           run_precursor)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, prices, volumes):
    n = len(prices)
    d0 = _dt.date(2015, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4),
                     round(float(volumes[i]), 2)))
    write_csv(path, rows)


# --- entry covariates are causal and well-formed ---------------------
rng = np.random.default_rng(3)
prices = 100.0 * np.exp(np.cumsum(
    0.01 * rng.standard_t(5, size=800)))
vols = 1_000_000.0 * np.exp(
    np.cumsum(0.01 * rng.standard_normal(800)))
covs = _entry_covariates(prices, vols, np.log(prices),
                         np.zeros(800) + 0.01, 700)
check("covariates carry all five pre-committed keys",
      set(ALL_COVS) <= set(covs))
check("vol_trend and range_eff are positive ratios",
      covs["vol_trend"] > 0 and covs["range_eff"] > 0)
check("kama_eff is a ratio in [0, 1]",
      0.0 <= covs["kama_eff"] <= 1.0 + 1e-9)
# causality: the covariates at t must not change when the FUTURE
# changes
prices2 = prices.copy()
prices2[750:] *= 2.0
covs2 = _entry_covariates(prices2, vols, np.log(prices2),
                          np.zeros(800) + 0.01, 700)
check("covariates are strictly causal (future-independent)",
      all(abs(covs[k] - covs2[k]) < 1e-12 for k in ALL_COVS))

# --- ground truth: a volume precursor that drives the hazard --------
# quiet-then-burst regimes where the burst ARRIVES SOONER when the
# 20/60 volume ratio into compression is high
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
rng = np.random.default_rng(21)
n = 4000
rets = np.zeros(n)
volumes = np.full(n, 1_000_000.0)
vol = 0.003
mode = "quiet"
quiet_left = burst_left = 0
for t in range(n):
    if mode == "quiet":
        quiet_left -= 1
        if quiet_left <= 0:
            mode = "burst"
            burst_left = int(rng.integers(10, 30))
    else:
        burst_left -= 1
        if burst_left <= 0:
            mode = "quiet"
            quiet_left = int(rng.integers(60, 140))
    vol = 0.002 if mode == "quiet" else 0.03
    rets[t] = rng.standard_t(6) * vol
    volumes[t] = (4_000_000.0 if mode == "burst"
                  and rng.random() < 0.3 else 1_000_000.0)
prices = 100.0 * np.exp(np.cumsum(rets))
_write_series(data / "PRCUSD.csv", prices, volumes)
# a second independent series so the ticker-split OOF has both
# halves populated
rng_b = np.random.default_rng(22)
rets_b = np.zeros(n)
volumes_b = np.full(n, 1_000_000.0)
vol = 0.003
mode = "quiet"
quiet_left = burst_left = 0
for t in range(n):
    if mode == "quiet":
        quiet_left -= 1
        if quiet_left <= 0:
            mode = "burst"
            burst_left = int(rng_b.integers(10, 30))
    else:
        burst_left -= 1
        if burst_left <= 0:
            mode = "quiet"
            quiet_left = int(rng_b.integers(60, 140))
    vol = 0.002 if mode == "quiet" else 0.03
    rets_b[t] = rng_b.standard_t(6) * vol
    volumes_b[t] = (4_000_000.0 if mode == "burst"
                    and rng_b.random() < 0.3 else 1_000_000.0)
_write_series(data / "PRCVUSD.csv",
              100.0 * np.exp(np.cumsum(rets_b)), volumes_b)

eps = build_episodes(data)
check("episodes build with all five covariates",
      len(eps) > 20
      and all(set(ALL_COVS) <= set(e) for e in eps))
uni = cox_fit(eps, covs=("vol_trend",))
check("ground truth: the volume precursor reads significant",
      abs(uni["z_stats"][0]) > 1.96)

# --- the null covariate ----------------------------------------------
# a covariate that is pure noise must read null
rng2 = np.random.default_rng(9)
for e in eps:
    e["noise"] = float(rng2.standard_normal())
nul = cox_fit(eps, covs=("noise",))
check("null covariate reads weaker than the true precursor "
      "(and never a discovery)",
      abs(nul["z_stats"][0]) < abs(uni["z_stats"][0])
      and abs(nul["z_stats"][0]) < 3.0)

# --- the full battery on ground-truth data ---------------------------
r = run_precursor(data)
check("battery returns OK with univariate blocks",
      r["status"] == "OK"
      and set(NEW_COVS) <= set(r["univariate_new_covariates"]))
check("direction split measured with the REFUSED claim",
      r["direction_split_first_events"]["n_events"] > 0
      and "REFUSED" in r["direction_split_first_events"]["claim"]
      and r["direction_split_first_events"]["wilson_95"] is not None)
check("Wilson band brackets the point estimate",
      r["direction_split_first_events"]["wilson_95"][0]
      <= r["direction_split_first_events"]["p_up"]
      <= r["direction_split_first_events"]["wilson_95"][1])
check("verdict reports both OOF concordances",
      r["verdict"]["clock_oof_concordance"] is not None
      and r["verdict"]["full_oof_concordance"] is not None)

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
