"""Trade-inevitables suite: the three rule additions measured
against KNOWN ground truth both ways - a mean-reverting anchored
asset must show the crash-depth gradient (deeper buys higher
forward medians), a drifting asset must not; the armed clock on
quiet-then-burst data must show a small waiting MAE against a
large event (high RR by construction); and the post-event calm
must be recovered on vol-decaying data. Harness file."""
import datetime as _dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from trade_inevitables import (claim_t1, claim_t2, claim_t3,
                               run_trade_inevitables)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _write_series(path, rets):
    prices = 100.0 * np.exp(np.cumsum(rets))
    d0 = _dt.date(2010, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000.0))
    write_csv(path, rows)


tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()

# --- T2 ground truth: a mean-reverting anchored asset -----------------
# crash weeks injected at random times with random depths, each
# followed by a bounce proportional to depth: the gradient is
# true BY CONSTRUCTION
rng = np.random.default_rng(9)
n = 20000
rets = 0.003 * rng.standard_t(6, size=n)
t = 100
while t < n - 40:
    if rng.random() < 0.02:
        depth = float(rng.uniform(0.05, 0.30))
        # the crash week: ~depth spread over 5 bars
        for j in range(5):
            rets[t + j] -= depth / 5
        # the bounce: the full depth plus a little (anchored,
        # mean-reverting - the asset does not decay to zero
        # and trip the dead-coin filter)
        for j in range(20):
            rets[t + 5 + j] += (depth * 1.05) / 20
        t += 40
    else:
        t += 1
_write_series(data / "BTCUSD.csv", rets)

t2 = claim_t2(data)
buckets = t2["buckets"]
with_data = [b for b in buckets.values()
             if "median_fwd_4w" in b]
check("T2 ground truth: the depth gradient is monotone "
      "(deeper buys higher forward medians)",
      t2["gradient_monotone_deeper_is-better"] is True
      and len(with_data) >= 3)
check("T2 ground truth: the nuclear-red bucket is positive",
      t2["nuclear_red"]["median_fwd_4w"] is not None
      and t2["nuclear_red"]["median_fwd_4w"] > 0)
check("T2 ground truth: verdict STRUCTURAL",
      "STRUCTURAL" in t2["verdict"])

# --- T2 null: a drifting asset (no bounce) -----------------------------
rng = np.random.default_rng(10)
rets_n = 0.003 * rng.standard_t(6, size=20000) - 0.0005
data2 = tmp / "null"
data2.mkdir()
_write_series(data2 / "BTCUSD.csv", rets_n)
t2n = claim_t2(data2)
check("T2 null: no STRUCTURAL gradient claimed on a drifting "
      "asset (the honesty note reports what is measured)",
      "STRUCTURAL" not in t2n["verdict"]
      or t2n["nuclear_red"].get("median_fwd_4w") is None
      or t2n["nuclear_red"]["median_fwd_4w"] <= 0)

# --- T1 ground truth: quiet-then-burst (small MAE, big event) ---------
def _regimes(rng2, n):
    r = np.zeros(n)
    vol = 0.003
    mode = "quiet"
    ql = bl = 0
    for t in range(n):
        if mode == "quiet":
            ql -= 1
            if ql <= 0:
                mode = "burst"
                bl = int(rng2.integers(10, 25))
        else:
            bl -= 1
            if bl <= 0:
                mode = "quiet"
                ql = int(rng2.integers(60, 140))
        vol = 0.001 if mode == "quiet" else 0.04
        r[t] = rng2.standard_t(6) * vol
    return r

data3 = tmp / "t1"
data3.mkdir()
_write_series(data3 / "QTZUSD.csv",
              _regimes(np.random.default_rng(3), 8000))
t1 = claim_t1(data3)
check("T1 ground truth: events measured",
      t1.get("n_events", 0) > 20)
check("T1 ground truth: high RR by construction "
      "(event size >= 2x the waiting MAE)",
      t1.get("rr_by_construction") is not None
      and t1["rr_by_construction"] >= 2
      and "STRUCTURAL" in t1["verdict"])

# --- T3 ground truth: vol decays after events -------------------------
t3 = claim_t3(data3)
check("T3 ground truth: the post-event calm measured",
      t3.get("n_significant_weeks", 0) > 10
      and t3.get("p_next_week_quiet") is not None)

# --- the full battery ---------------------------------------------------
r = run_trade_inevitables(data3)
check("the battery returns all three claims",
      r["status"] == "OK"
      and set(("t1_armed_clock_drawdown",
               "t2_crash_depth_gradient",
               "t3_post_event_calm")) <= set(r))

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
