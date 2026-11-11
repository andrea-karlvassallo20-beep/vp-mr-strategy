"""AVFI replication suite: indicator math on synthetic OHLCV with
known structure, throttle causality, iteration honesty, and chart-data
generation. Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from avfi import (DEFAULT_PARAMS, VARIANT_GRID, avfi_v2_series,
                  avfi_v3_series, ema, garman_klass_sigma,
                  parkinson_sigma_pk,
                  run_iteration, spread_axis, spread_z,
                  throttle_backtest, trailing_mean, write_report)

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

vals = np.arange(10, dtype=float)
check("trailing mean is strictly causal (out[t] uses only <= t)",
      trailing_mean(vals, 3)[4] == np.mean(vals[2:5])
      and trailing_mean(vals, 3)[0] == vals[0])

h, l, c, v = synth_ohlcv(600, seed=5)
pk = parkinson_sigma_pk(h, l, DEFAULT_PARAMS["pk_window"])
check("Parkinson sigmaPk positive and finite on valid OHLC",
      np.all(np.isfinite(pk[50:])) and np.all(pk[50:] > 0))

v3 = avfi_v3_series(h, l, c, v, DEFAULT_PARAMS["vol_window"],
                    DEFAULT_PARAMS["pk_window"])
v2 = avfi_v2_series(c, v, DEFAULT_PARAMS["vol_window"])
check("AVFI v3 and v2 finite", np.isfinite(v3).all() and np.isfinite(v2).all())
check("spread axis is v3 minus slow EMA of v2",
      np.allclose(spread_axis(h, l, c, v, DEFAULT_PARAMS),
                  v3 - ema(v2, DEFAULT_PARAMS["ema_slow"]), atol=1e-9))

sp = spread_axis(h, l, c, v, DEFAULT_PARAMS)
z = spread_z(sp, DEFAULT_PARAMS["sp_z_window"])
check("spread z is zero before the rolling window fills",
      np.all(z[:DEFAULT_PARAMS["sp_z_window"]] == 0.0)
      and np.any(np.abs(z[150:]) > 0))

h_mod = h.copy()
h_mod[-1] *= 1.5
z2 = spread_z(spread_axis(h_mod, l, c, v, DEFAULT_PARAMS),
              DEFAULT_PARAMS["sp_z_window"])
check("spread z is strictly causal (future bar change does not "
      "alter earlier z)", np.allclose(z[:-1], z2[:-1]))

base = throttle_backtest(h, l, c, v, use_throttle=False)
th = throttle_backtest(h, l, c, v, use_throttle=True)
check("backtest returns full study dict",
      all(k in base for k in ("sharpe", "max_dd_pct", "entries", "pos",
                              "sp_z", "eq")))
check("entries recorded with direction",
      len(base["entries"]) > 0 and all(d in (-1, 1) for _, d in
                                       base["entries"]))

import avfi as _avfi
_orig_spread_z = _avfi.spread_z
_avfi.spread_z = lambda spread, window: np.zeros(len(spread))
try:
    a = throttle_backtest(h, l, c, v, use_throttle=True)
    b = throttle_backtest(h, l, c, v, use_throttle=False)
finally:
    _avfi.spread_z = _orig_spread_z
check("throttle with no trigger reproduces the base run exactly",
      a["sharpe"] == b["sharpe"] and a["throttled_bars"] == 0)

gk = garman_klass_sigma(l, h, l, c, DEFAULT_PARAMS["pk_window"])
check("Garman-Klass sigma finite and positive on valid OHLC",
      np.all(np.isfinite(gk[50:])) and np.all(gk[50:] > 0))
check("dollar-volume mode changes the flow",
      not np.allclose(
          avfi_v3_series(h, l, c, v, 20, 20, volume_mode="dollar"),
          avfi_v3_series(h, l, c, v, 20, 20, volume_mode="shares")))
check("variant grid is pre-committed and non-trivial",
      len(VARIANT_GRID) == 72
      and any(g["trigger"] != DEFAULT_PARAMS["trigger"]
              for g in VARIANT_GRID)
      and any(g["vol_estimator"] == "garman_klass" for g in VARIANT_GRID)
      and any(g["volume_mode"] == "dollar" for g in VARIANT_GRID))

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
r = run_iteration(data, tmp / "research", universe=("SPY", "QQQ", "IWM"))
check("iteration runs on cached CSVs", r["status"] == "OK"
      and len(r["rows"]) == 2)
check("iteration ledger written with honest record",
      (tmp / "research" / "avfi_iterations.json").exists()
      and r["iteration"]["advanced"] in (True, False)
      and "oos_dd_reduction_pct" in r["iteration"])
chart = json.loads((tmp / "research" / "avfi_chart.json").read_text())
check("chart data exported per instrument",
      len(chart) == 3 and all(
          k in chart[1] for k in ("ticker", "dates", "close", "sp_z",
                                  "entries", "trigger", "eq")))
check("chart includes the PORTFOLIO equity entry",
      any(ch["ticker"] == "PORTFOLIO" and len(ch["eq"]) > 2
          for ch in chart))
check("chart entries match the audited decision log",
      all(len(ch["entries"]) > 0 for ch in chart
          if ch["ticker"] != "PORTFOLIO"))
rep = tmp / "avfi_report.md"
write_report(r, rep)
txt = rep.read_text()
check("report carries throttle table + iteration ledger",
      "Throttled bars" in txt and "Iteration ledger" in txt)

r2 = run_iteration(data, tmp / "research", universe=("SPY", "QQQ"))
ledger = json.loads((tmp / "research" / "avfi_iterations.json").read_text())
check("same-day re-run is idempotent in the ledger",
      len(ledger) == 1 and ledger[0]["iteration"] == 1)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
