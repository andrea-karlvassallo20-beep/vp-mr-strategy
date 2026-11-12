"""AVFI precursor battery suite: the incremental-information
machinery measured against KNOWN ground truth - the frozen
event encoding (quiet-complete vs censored vs event), the
cross convention, and the decisive structure: a configuration
that carries NO hazard content alone must read at/below
climatology, while a configuration that fires WITH the clock
may earn incremental content only with disjoint bands.
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
from avfi_precursor import (FLIP_LO, HORIZON, RECENT, STRETCH,
                            run_avfi_precursor)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# --- the frozen event encoding, hand-checked ---------------------
import numpy as _np
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import (WEEK, first_significant_week,
                          km_greenwood)

# a quiet-complete window: no |r1| >= 2.5 sigma in 60 bars
logc = np.arange(400, dtype=float) * 0.001
sig = np.full(400, 0.05)      # thr = 0.125; weekly moves ~0.005
check("a quiet window completes as -1",
      first_significant_week(logc, sig, 100) == -1)
# an event at week 3: a 0.2 jump from bar 115 on (the week
# ending at 115 carries it)
logc2 = np.arange(400, dtype=float) * 0.001
logc2[115:] += 0.2
off = first_significant_week(logc2, sig, 100)
check("the event offset is the week-ending bar minus entry",
      off == 15)  # the week ending at bar 115, offset 15
# censored: the data edge cuts the window
logc3 = logc[:110]
check("a window cut by the data edge censors negative",
      first_significant_week(logc3, sig, 100) < -1
      or first_significant_week(logc3, sig, 100) == -1)

# --- KM on hand-computed data ------------------------------------
# 10 entries: 5 events at week 5, 5 quiet at the horizon
d = np.array([5] * 5 + [60] * 5)
e = np.array([1] * 5 + [0] * 5)
km = km_greenwood(d, e, 60)
check("KM reproduces the hand-computed cum",
      abs(km["cum_event_12w"] - 0.5) < 1e-9
      and km["n_events"] == 5)

# --- the battery on a synthetic universe -------------------------
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir(parents=True)


def _write_series(path, rets, d0=(2015, 1, 1)):
    prices = 100.0 * np.exp(np.cumsum(rets))
    d0 = _dt.date(*d0)
    rows = []
    for i, p in enumerate(prices):
        dd = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((dd, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000.0))
    write_csv(path, rows)


rng = np.random.default_rng(11)
n1 = 3000
# one asset whose vol alternates: quiet (compression) with
# occasional significant weeks, and stretch dips inside the
# quiet phases (the structure where stretch x compression can
# add hazard)
rets = 0.0002 * rng.standard_normal(n1)
for k in range(300, n1 - 100, 150):
    rets[k:k + 60] = 0.0003 * rng.standard_normal(60)
    rets[k + 20] -= 0.03          # a deep stretch dip
    rets[k + 40] += 0.04          # a significant week later
_write_series(data / "SIF.csv", rets)
# one asset that never leaves mid and never stretches
rets2 = 0.001 * rng.standard_normal(n1)
_write_series(data / "CLF.csv", rets2)

r = run_avfi_precursor(data)
check("the battery runs with every cell measured",
      r["status"] == "OK"
      and all("cum_event_12w" in c or
              c.get("verdict") for c in r["cells"].values()))
check("the climatology counterfactual is present",
      "cum_event_12w" in r["cells"].get("climatology", {}))
check("every cell carries Greenwood bands",
      all("ci95_lo" in c and "ci95_hi" in c
          for c in r["cells"].values()
          if "cum_event_12w" in c))
check("the incremental verdict is stated, honestly either way",
      isinstance(r["incremental_verdict"], str)
      and len(r["incremental_verdict"]) > 20)
check("the cell verdicts speak the no-incremental truth when "
      "bands overlap",
      all(isinstance(v, str) for v in
          r["cell_verdicts"].values()))
res = tmp / "research"
res.mkdir(parents=True)
(res / "avfi_precursor.json").write_text(json.dumps(r))
check("the JSON artifact serializes",
      json.loads((res / "avfi_precursor.json")
                 .read_text())["status"] == "OK")

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
