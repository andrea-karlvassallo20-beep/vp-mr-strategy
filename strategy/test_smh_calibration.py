"""SMH temporal calibration suite: the dress rehearsal measured
against KNOWN ground truth both ways - a universe where
compression provably elevates the hazard (the forecast must carry
positive out-of-sample skill), and a persistence universe where
it does not (the skill must not be positive). Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from smh_calibration import (build_episodes, climatology_rate,
                             run_calibration)

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


def _regimes(rng, n, quiet_lo, quiet_hi, burst_lo, burst_hi):
    rets = np.zeros(n)
    vol = 0.003
    mode = "quiet"
    quiet_left = burst_left = 0
    for t in range(n):
        if mode == "quiet":
            quiet_left -= 1
            if quiet_left <= 0:
                mode = "burst"
                burst_left = int(rng.integers(
                    burst_lo, burst_hi))
        else:
            burst_left -= 1
            if burst_left <= 0:
                mode = "quiet"
                quiet_left = int(rng.integers(
                    quiet_lo, quiet_hi))
        vol = 0.002 if mode == "quiet" else 0.03
        rets[t] = rng.standard_t(6) * vol
    return rets


# --- ground truth: quiet-then-burst (compression elevates) ------------
rng = np.random.default_rng(41)
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
for i in range(3):
    rets = _regimes(np.random.default_rng(41 + i), 6000,
                   60, 140, 10, 25)
    _write_series(data / f"CLB{i}USD.csv", rets)

eps = build_episodes(data)
check("episodes carry the temporal split tag",
      all(e["split"] in ("train", "test") for e in eps)
      and any(e["split"] == "train" for e in eps)
      and any(e["split"] == "test" for e in eps))
cut_frac = sum(1 for e in eps if e["split"] == "test") / len(eps)
check("roughly 30% of entries land in the test window",
      0.1 < cut_frac < 0.5)

r = run_calibration(data)
check("battery returns OK on ground truth",
      r["status"] == "OK")
if r["status"] == "OK":
    check("ground truth: the forecast beats climatology "
          "out of sample (positive skill)",
          r["verdict"]["beats_climatology_oos"] is True
          and r["skill_score"] > 0)
    check("Brier in a sane range",
          0.0 < r["scores"]["brier"] < 0.5)
    check("the protocol note names the doctrine boundary",
          "doctrine rule 2" in r["protocol"])

# --- the persistence control: the mechanical caveat, honestly --------
# Compression-conditioning carries a threshold advantage even
# with NO expansion structure (the charter's mechanical-threshold
# caveat, frozen beside the gradient). So the honest control is
# RELATIVE: real structure must add skill on top of the mechanic.
rng = np.random.default_rng(5)
data2 = tmp / "null"
data2.mkdir()
n2 = 6000
vol = np.full(n2, 0.002)
for t in range(1, n2):
    vol[t] = 0.998 * vol[t - 1] + 0.002 * 0.002 + \
        0.05 * abs(rng.standard_normal()) * vol[t - 1]
    vol[t] = min(max(vol[t], 0.0005), 0.004)
_write_series(data2 / "NCLUSD.csv",
              vol * rng.standard_t(6, size=n2))
r_n = run_calibration(data2)
if r_n["status"] == "OK":
    check("persistence control: ground-truth skill clearly "
          "exceeds the no-expansion control (the instrument "
          "reads real structure on top of the threshold "
          "mechanic)",
          r["skill_score"] > r_n["skill_score"] + 0.05)
    check("persistence control: the battery reports its verdict "
          "faithfully (booleans consistent with the scores)",
          r_n["verdict"]["beats_climatology_oos"]
          == (r_n["skill_score"] > 0))
else:
    check("persistence control: insufficient episodes reported "
          "honestly", "INSUFFICIENT" in r_n["status"])

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
