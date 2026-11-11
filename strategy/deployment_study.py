"""Study 6: Deployment envelope for VP-MR-ETF-D1-001.
(a) Edge threshold: sweep OU reversion strength theta -> find Sharpe break-even.
(b) Full run-card universe: 5 tickers, correlated + idiosyncratic components.
Deterministic."""
import math
import numpy as np
from vp_mr_strategy import StrategyParameters
from backtest_study import backtest

def ou(n, seed, s0, theta, sigma=1.2, mu=None):
    rng = np.random.default_rng(seed)
    mu = s0 if mu is None else mu
    p = np.empty(n); p[0] = s0
    for i in range(1, n):
        p[i] = p[i-1] + theta * (mu - p[i-1]) + rng.normal(0, sigma)
    return p

N = 1260
BASE = {"SPY": 450.0, "QQQ": 380.0, "IWM": 200.0, "XLF": 38.0, "XLE": 88.0}

print("=" * 72)
print("STUDY 6a: EDGE THRESHOLD (2 assets, sweep OU reversion strength theta)")
print("=" * 72)
print(f"  {'theta':>7} {'half_life':>10} {'sharpe':>8} {'ann_ret%':>9} {'trips':>6}")
prev = None
be_low = be_high = None
for theta in (0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20):
    hl = round(math.log(2) / theta, 1) if theta > 0 else float("inf")
    data = {s: ou(N, 101 + i * 7, px0, theta)
            for i, (s, px0) in enumerate(BASE.items()) if s in ("SPY", "QQQ")}
    m = backtest(data, StrategyParameters())[1]
    tag = ""
    if prev is not None and prev < 0 <= m["sharpe"] and be_low is None:
        be_low, be_high = last_theta, theta
    prev = m["sharpe"]; last_theta = theta
    print(f"  {theta:>7} {hl:>10} {m['sharpe']:>8} {m['ann_return_pct']:>9} "
          f"{m['round_trips']:>6}")
if be_low is not None:
    print(f"\n  Break-even theta in ({be_low}, {be_high}] "
          f"(half-life ~{round(math.log(2)/be_high,1)} bars)")

print()
print("=" * 72)
print("STUDY 6b: FULL RUN-CARD UNIVERSE (5 ETFs, factor + idio structure)")
print("=" * 72)
rng = np.random.default_rng(2024)
factor = rng.normal(0, 0.8, N)          # common market factor
theta = 0.05
data = {}
for i, (s, px0) in enumerate(BASE.items()):
    idio = rng.normal(0, 0.7, N)
    rng2 = np.random.default_rng(900 + i)
    p = np.empty(N); p[0] = px0
    for t in range(1, N):
        p[t] = p[t-1] + theta * (px0 - p[t-1]) + factor[t] * 0.3 + idio[t]
    data[s] = p
m = backtest(data, StrategyParameters())[1]
print("  5-asset result (default frozen params):")
for k, v in m.items():
    print(f"  {k:>16}: {v}")

print()
print("=" * 72)
print("STUDY 6c: UNIVERSE SCALING (2 -> 3 -> 5 assets, theta=0.05)")
print("=" * 72)
print(f"  {'n_assets':>9} {'sharpe':>8} {'ann_ret%':>9} {'maxDD%':>7} {'trips':>6}")
for k in (2, 3, 5):
    syms = list(BASE.keys())[:k]
    data = {s: ou(N, 101 + j * 7, BASE[s], theta)
            for j, s in enumerate(syms)}
    m = backtest(data, StrategyParameters())[1]
    print(f"  {k:>9} {m['sharpe']:>8} {m['ann_return_pct']:>9} "
          f"{m['max_dd_pct']:>7} {m['round_trips']:>6}")
