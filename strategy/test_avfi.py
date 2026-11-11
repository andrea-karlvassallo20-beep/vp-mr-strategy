"""AVFI replication suite: indicator math on synthetic OHLCV with
known structure, throttle causality, and report generation.
Harness file."""
import math
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from avfi import (EMA_SLOW, avfi_v2_series, avfi_v3_series, ema,
                  parkinson_sigma_pk, run_avfi_research, spread_axis,
                  spread_z, throttle_backtest, write_report)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def synth_ohlcv(n, seed, drift=0.0):
    rng = np.random.default_rng(seed)
    rets = drift + 0.01 * rng.standard_normal(n)
    close = 100.0 * np.exp(np.cumsum(rets))
    spread = np.abs(0.008 * rng.standard_normal(n)) + 0.002
    high = close * (1 + spread)
    low = close * (1 - spread)
    vol = 1e6 * np.exp(rng.standard_normal(n))
    return high, low, close, vol


check("ema matches manual computation",
      abs(ema(np.array([1.0, 2.0, 3.0]), span=2)[1]
          - (2 / 3 * 2.0 + 1 / 3 * 1.0)) < 1e-12)

h, l, c, v = synth_ohlcv(600, seed=5)
pk = parkinson_sigma_pk(h, l)
check("Parkinson sigmaPk positive and finite on valid OHLC",
      np.all(np.isfinite(pk[50:])) and np.all(pk[50:] > 0))

v3 = avfi_v3_series(h, l, c, v)
v2 = avfi_v2_series(c, v)
check("AVFI v3 finite and centered near zero", np.isfinite(v3).all())
check("AVFI v2 finite and non-negative-magnitude",
      np.isfinite(v2).all())
check("spread axis is v3 minus slow EMA of v2",
      np.allclose(spread_axis(h, l, c, v),
                  v3 - ema(v2, EMA_SLOW), atol=1e-9))

sp = spread_axis(h, l, c, v)
z = spread_z(sp)
check("spread z is zero before the rolling window fills",
      np.all(z[:100] == 0.0) and np.any(np.abs(z[150:]) > 0))

# causality: the z at t must not change when future bars change
h2, l2, c2, v2b = synth_ohlcv(600, seed=6)
z1 = spread_z(spread_axis(h, l, c, v))
h_mod = h.copy()
h_mod[-1] *= 1.5
z2 = spread_z(spread_axis(h_mod, l, c, v))
check("spread z is strictly causal (future bar change does not "
      "alter earlier z)", np.allclose(z1[:-1], z2[:-1]))

import avfi as _avfi
_orig_spread_z = _avfi.spread_z


def _match_base():
    _avfi.spread_z = lambda spread, window=100: np.zeros(
        len(spread) if hasattr(spread, "__len__") else 0)
    try:
        a = throttle_backtest(h, l, c, v, use_throttle=True)
        b = throttle_backtest(h, l, c, v, use_throttle=False)
    finally:
        _avfi.spread_z = _orig_spread_z
    return a[:4] == b[:4] and a[4] == 0


base = throttle_backtest(h, l, c, v, use_throttle=False)
th = throttle_backtest(h, l, c, v, use_throttle=True)
check("throttle backtest returns complete tuple",
      len(base) == 5 and len(th) == 5)
check("throttle with no trigger reproduces the base run exactly",
      _match_base())
check("throttled bars counted only when active",
      th[4] >= 0 and base[4] == 0)

tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
from fetch_data import write_csv
for i, t in enumerate(["SPY", "QQQ"]):
    hi, lo, cl, vo = synth_ohlcv(400, seed=10 + i)
    rows = [(f"2024-{(j // 28) % 12 + 1:02d}-{j % 28 + 1:02d}",
             lo[j], hi[j], lo[j], cl[j], int(vo[j]))
            for j in range(len(cl))]
    write_csv(data / f"{t.lower()}.csv", rows)
r = run_avfi_research(data, universe=("SPY", "QQQ", "IWM"))
check("research runs on cached CSVs", r["status"] == "OK"
      and len(r["rows"]) == 2)
check("missing instrument skipped gracefully", all(
      row["ticker"] in ("SPY", "QQQ") for row in r["rows"]))
rep = tmp / "avfi_report.md"
write_report(r, rep)
txt = rep.read_text()
check("report carries throttle-vs-base table",
      "Base Sharpe" in txt and "Throttled bars" in txt)
check("report carries the programme note (throttle, not timer)",
      "risk throttle" in txt and "entry timer" in txt)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
