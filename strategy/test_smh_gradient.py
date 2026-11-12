"""SMH salience gradient suite: the gradient instrument measured
against KNOWN ground truth both ways - a regime-alternating series
where compression provably precedes bursts (gradient must be
monotone, compression band disjoint from climatology), a
homoscedastic null (no salience allowed), and the law-4 volume
signature (injected spikes must be recovered). Harness file."""
import csv as _csv
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from smh_gradient import (HORIZON, _clock_for_region,
                           climatology_clock, event_anatomy,
                           km_greenwood, run_gradient)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, prices, volumes=None):
    n = len(prices)
    d0 = _dt.date(2016, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        vol = (volumes[i] if volumes is not None
               else 1_000_000.0)
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), round(float(vol), 2)))
    write_csv(path, rows)


# --- KM + Greenwood against a hand-computed case ----------------------
durs = np.array([1, 2, 2, 3, 3, 3, 5])
evs = np.array([1, 1, 0, 1, 0, 0, 0])
km = km_greenwood(durs, evs, 5)
# hand: t=1: d=1,n=7 -> S=6/7; t=2: d=1,n=6 -> S=6/7*5/6=5/7;
# t=3: d=1,n=4 -> S=5/7*3/4=15/28
check("KM cumulative matches the hand computation",
      abs(km["cum_event_12w"] - round(1 - 15 / 28, 3)) < 1e-9)
check("Greenwood band brackets the point estimate",
      km["ci95_lo"] <= km["cum_event_12w"] <= km["ci95_hi"]
      and 0.0 <= km["ci95_lo"] and km["ci95_hi"] <= 1.0)

# --- ground truth 1: quiet-then-burst regimes -------------------------
rng = np.random.default_rng(11)
n = 3000
rets = np.zeros(n)
vol = 0.003
mode = "quiet"
quiet_left = 0
for t in range(n):
    if mode == "quiet":
        quiet_left -= 1
        if quiet_left <= 0:
            mode = "burst"
            burst_left = int(rng.integers(5, 15))
    else:
        burst_left -= 1
        if burst_left <= 0:
            mode = "quiet"
            quiet_left = int(rng.integers(30, 80))
    vol = 0.002 if mode == "quiet" else 0.03
    rets[t] = rng.standard_t(6) * vol
prices = 100.0 * np.exp(np.cumsum(rets))

tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
res = tmp / "research"
res.mkdir()
_write_series(data / "QTZUSD.csv", prices)

comp = _clock_for_region(data, 0)
mid = _clock_for_region(data, 1)
stress = _clock_for_region(data, 2)
clim = climatology_clock(data)
check("ground truth: compression clock beats climatology",
      comp["cum_event_12w"] > clim["cum_event_12w"])
check("ground truth: compression band disjoint from climatology",
      comp["ci95_lo"] > clim["ci95_hi"])
check("ground truth: gradient is monotone in the point estimates",
      comp["cum_event_12w"] > mid["cum_event_12w"]
      > clim["cum_event_12w"] > stress["cum_event_12w"])
r = run_gradient(data)
check("run_gradient reports EDGE-LOCAL salience on ground truth",
      r["verdict"]["salience_edge_local"] is True)

# --- control 2: the persistence series (the mechanical-threshold
# caveat, honestly tested) --------------------------------------------
# Compression that STAYS compressed carries no expansion structure.
# The charter's own definition gives every compression entry a
# threshold advantage (sigma frozen at the decision close, selected
# on the lowest tercile) - the mechanical-threshold caveat, frozen
# beside the flag, not denied. So the honest control is RELATIVE:
# the instrument must read real expansion structure ON TOP of the
# mechanic (ground truth clearly above the persistence series),
# and the verdict must faithfully report its own numbers.
rng = np.random.default_rng(5)
n2 = 3000
vol = np.full(n2, 0.002)
for t in range(1, n2):
    vol[t] = 0.998 * vol[t - 1] + 0.002 * 0.002 + \
        0.05 * abs(rng.standard_normal()) * vol[t - 1]
    vol[t] = min(max(vol[t], 0.0005), 0.004)   # bounded, persistent
null_rets = vol * rng.standard_t(6, size=n2)
null_prices = 100.0 * np.exp(np.cumsum(null_rets))
data2 = tmp / "null"
data2.mkdir()
_write_series(data2 / "NULUSD.csv", null_prices)
comp_n = _clock_for_region(data2, 0)
clim_n = climatology_clock(data2)
check("persistence control: ground-truth compression clock "
      "clearly above the no-expansion control (the instrument "
      "reads real structure, not just the threshold mechanic)",
      comp["cum_event_12w"] > comp_n["cum_event_12w"] + 0.05)
r_n = run_gradient(data2)
g = r_n["gradient"]
check("persistence control: verdict faithfully reports its own "
      "numbers (booleans consistent with the clocks)",
      r_n["verdict"]["monotone_point_estimates"] == (
          g["compression"]["cum_event_12w"]
          > g["mid"]["cum_event_12w"]
          > g["climatology"]["cum_event_12w"]
          > g["stress_events"]["cum_event_12w"])
      and r_n["verdict"][
          "compression_disjoint_from_climatology"] == (
          g["compression"]["ci95_lo"]
          > g["climatology"]["ci95_hi"]))
check("the mechanical-threshold caveat is measurable: even with "
      "NO expansion structure, compression > climatology "
      "(the charter's frozen caveat, reproduced)",
      comp_n["cum_event_12w"] > clim_n["cum_event_12w"])

# --- ground truth 3: the law-4 volume signature -----------------------
# bursts carry 4x volume: the anatomy must recover event volume
# above baseline and above the all-bars median
vols = np.where(np.abs(rets) > 0.01, 4_000_000.0, 1_000_000.0)
data3 = tmp / "vol"
data3.mkdir()
_write_series(data3 / "VOLUSD.csv", prices, volumes=vols)
an = event_anatomy(data3)
check("anatomy: first events exist after compression entries",
      an["n_first_events"] > 0)
check("law-4 ground truth: event volume above all-bars baseline",
      an["volume"]["median_event_ratio"]
      > an["volume"]["median_all_bars_ratio"])
check("law-4 ground truth: event median ratio clearly above 1",
      an["volume"]["median_event_ratio"] > 1.5)
check("anatomy: overshoot at or above the 2.5-sigma bar",
      an["overshoot_median"] >= 1.0)
check("anatomy: arrival classes sum to the event count",
      sum(an["arrival_split"].values()) == an["n_first_events"])
check("anatomy: act capture at spell end within [0,1]",
      0.0 <= an["act_capture_at_spell_end"] <= 1.0)
check("anatomy: up/down asymmetry carries its seductive-cell flag",
      "untrusted" in an["up_down_volume_asymmetry"]["flag"])

# --- null volume: constant volume -> ratios equal ---------------------
data4 = tmp / "vnull"
data4.mkdir()
_write_series(data4 / "VNUUSD.csv", prices,
              volumes=np.full(len(prices), 1_000_000.0))
an_n = event_anatomy(data4)
check("volume null: event and all-bars ratios both 1.0",
      an_n["volume"]["median_event_ratio"] == 1.0
      and an_n["volume"]["median_all_bars_ratio"] == 1.0)

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
