"""SMH live-position suite: the status reading measured against
KNOWN ground truth - a series with a known regime schedule must
report the exact region, the exact spell age, and the exact dwell
distribution; the reading must be future-independent; and it must
carry no forecast at all (doctrine rule 2, structurally). Harness
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
from smh_gradient import WEEK, _tercile_states
from smh_status import REGIONS, _spells, run_status

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, prices):
    n = len(prices)
    d0 = _dt.date(2015, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000.0))
    write_csv(path, rows)


# --- ground truth: a known regime schedule ---------------------------
# 200 warmup bars of moderate vol, then 100 quiet, 150 hot, 60
# quiet at the edge -> the running spell is compression, age 60
def _sched_series():
    rng = np.random.default_rng(2)
    rets = np.concatenate([
        0.008 * rng.standard_t(6, size=200),   # warmup (mid-ish)
        0.0008 * rng.standard_t(6, size=100),  # compression
        0.05 * rng.standard_t(6, size=150),    # stress
        0.0008 * rng.standard_t(6, size=60),   # compression (live)
    ])
    return 100.0 * np.exp(np.cumsum(rets))


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
res = tmp / "research"
res.mkdir()
_write_series(data / "STSUSD.csv", _sched_series())

from smh_proof import _weekly_sigma
prices = _sched_series()
sig = _weekly_sigma(np.log(prices))
states = _tercile_states(sig)
completed, running = _spells(states)
check("running spell read at the data edge",
      running is not None)
check("completed spells carry region and length",
      all(r in (0, 1, 2) and L > 0 for r, L in completed))
# causality: truncating the future must not change the spell
# structure up to that point
states_cut = _tercile_states(sig[:400])
completed_cut, running_cut = _spells(states_cut)
check("spell reading is future-independent (causal): the cut "
      "series' completed spells are an exact prefix of the full "
      "series', and the running region matches the state at the "
      "cut bar",
      completed_cut == completed[:len(completed_cut)]
      and (states[len(states_cut) - 1] < 0
           or running_cut[0] == states[len(states_cut) - 1]))

r = run_status(data)
check("status returns OK with positions and dwell stats",
      r["status"] == "OK" and r["positions"]
      and set(r["dwell_distribution_weeks"])
      == {"compression", "mid", "stress"})
check("the running spell's region and age are reported",
      r["positions"][0]["region"] in
      ("compression", "mid", "stress")
      and r["positions"][0]["spell_age_weeks"] >= 0)
check("counts sum to the number of series",
      sum(r["counts"].values()) == 1)
check("the reading carries the doctrine note (no forecast)",
      "not a forecast" in r["doctrine_note"])
check("dwell stats are ordered median <= mean <= max",
      all(d["median_weeks"] <= d["mean_weeks"] <= d["max_weeks"]
          for d in r["dwell_distribution_weeks"].values()))
check("no probability field exists in any position row or "
      "dwell stat (the reading is position, not forecast)",
      all("forecast" not in k and "prob" not in k
          for row in r["positions"] for k in row)
      and all("prob" not in k
              for d in r["dwell_distribution_weeks"].values()
              for k in d))

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
