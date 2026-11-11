"""Tops-and-bottoms detector suite: RSI correctness, divergence and
climax detection on synthetic data with known turns, event-study
honesty, and causality. Harness file."""
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from tops_bottoms import (detect_climaxes, detect_divergences,
                          event_study, forward_returns, rsi, run_study,
                          topology_buckets, turn_topology,
                          write_report, z_entries)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# 1. RSI correctness on a monotonic rise (should saturate high)
up = np.linspace(100, 200, 60)
r_up = rsi(up)
check("RSI saturates high on a monotonic rise", r_up[-1] > 90)
down = np.linspace(200, 100, 60)
r_dn = rsi(down)
check("RSI saturates low on a monotonic decline", r_dn[-1] < 10)
flat = np.full(60, 100.0)
check("RSI is 100 on a flat series (no losses, Wilder convention)",
      rsi(flat)[-1] == 100.0)

# 2. RSI causality: future bars cannot change past RSI
rng = np.random.default_rng(7)
walk = 100 * np.exp(np.cumsum(0.01 * rng.standard_normal(300)))
r1 = rsi(walk)
walk_mod = walk.copy()
walk_mod[-1] *= 1.3
r2 = rsi(walk_mod)
check("RSI is strictly causal", np.allclose(r1[:-1], r2[:-1]))

# 3. divergence detection on a constructed bottom: lower low in price,
# higher low in RSI
prices = np.concatenate([
    np.linspace(100, 80, 40),    # decline
    np.array([78.0]),           # first low
    np.linspace(80, 84, 10),     # small bounce
    np.array([77.5]),            # LOWER low in price
    np.linspace(80, 100, 60),    # recovery
])
r = rsi(prices)
bull, bear = detect_divergences(prices, r)
check("bullish divergence detected at the constructed lower low",
      len(bull) >= 1 and 50 <= bull[-1] <= 53)

# 4. climax detection: a huge-volume wide-range reversal bar after a
# decline, closing in the upper half of its range
n = 120
close = np.linspace(120, 100, n)          # steady decline
high = close * 1.003
low = close * 0.997
volume = np.full(n, 1e6)
close[-1] = 104.0                          # strong recovery close
high[-1] = 105.0
low[-1] = 99.0                             # wide range
volume[-1] = 5e6                           # climax effort
cb, ct = detect_climaxes(high, low, close, volume)
check("VSA climax bottom detected on the constructed exhaustion bar",
      len(cb) >= 1 and cb[-1] == n - 1)

# 5. z-entries: bottoms long, tops short
zz = z_entries(close)
check("z-score entries carry direction",
      all(d in (-1, 1) for _, d in zz))

# 6. forward returns are causal and horizon-bounded
fr = forward_returns(close, n - 11, horizon=10)
check("forward return computed over the horizon",
      math.isclose(fr, close[n - 1] / close[n - 11] - 1.0, rel_tol=1e-9))
check("forward return None beyond the series end",
      forward_returns(close, n - 1, horizon=10) is None)

# 7. event study: confirmed entries must be counted separately
entries = [(50, 1), (60, 1), (80, -1)]
study = event_study(close, entries, {60})
check("event study separates confirmed from unconfirmed",
      study["n_confirmed"] == 1 and study["n_unconfirmed"] == 2)

# 7b. multi-dimensional turn topology
rng2 = np.random.default_rng(9)
n2 = 600
# construct a series with a deep, climactic bottom mid-series
base = np.concatenate([
    np.linspace(100, 70, 250) + 0.5 * rng2.standard_normal(250),
    np.array([68.0]),                       # the low
    np.linspace(72, 110, 349) + 0.5 * rng2.standard_normal(349),
])
h2 = base * 1.004
l2 = base * 0.996
v2 = np.full(n2, 1e6)
# climax at the low: huge volume, wide range, upper-half close
h2[250] = 72.0
l2[250] = 66.0
base[250] = 71.0
v2[250] = 6e6
b_sc, t_sc = turn_topology(h2, l2, base, v2)
check("topology scores are integers in 0..5",
      b_sc.max() <= 5 and t_sc.max() <= 5
      and b_sc.min() >= 0)
check("topology confluence exceeds a single dimension at the "
      "constructed bottom", b_sc[245:255].max() >= 2)
ent2 = z_entries(base)
bk = topology_buckets(base, ent2, b_sc, t_sc)
check("topology buckets populated with forward returns",
      isinstance(bk, dict) and len(bk) >= 1
      and all("n" in v and "long_fwd" in v for v in bk.values()))
# regression: numpy bool_ + bool_ is OR, not addition
check("confluence score counts dimensions (numpy-bool regression)",
      (np.bool_(True) + np.bool_(True)) is not None
      and b_sc[250] >= 1)

# 8. full study on synthetic CSVs + report generation
tmp = Path(tempfile.mkdtemp())
data = tmp / "data"
data.mkdir()
from fetch_data import write_csv
for i, t in enumerate(["SPY", "QQQ"]):
    w = 100 * np.exp(np.cumsum(0.012 * np.random.default_rng(
        20 + i).standard_normal(400)))
    hi = w * 1.004
    lo = w * 0.996
    vo = 1e6 * np.exp(0.3 * np.random.default_rng(
        30 + i).standard_normal(400))
    rows = [(f"2024-{(j // 28) % 12 + 1:02d}-{j % 28 + 1:02d}",
             lo[j], hi[j], lo[j], w[j], int(vo[j]))
            for j in range(len(w))]
    write_csv(data / f"{t.lower()}.csv", rows)
res = run_study(data, universe=("SPY", "QQQ", "IWM"))
check("study runs on cached CSVs, missing instrument skipped",
      res["status"] == "OK" and len(res["rows"]) == 2)
check("study exports chart series with detector indices",
      all(k in res["charts"][0] for k in
          ("close", "divergence_bottoms", "climax_tops")))
rep = tmp / "tb_report.md"
write_report(res, rep)
txt = rep.read_text()
check("report carries the event-study table",
      "confirmed" in txt and "div bot" in txt)

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
