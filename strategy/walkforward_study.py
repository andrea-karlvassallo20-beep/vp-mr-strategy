"""Walk-forward + Monte Carlo significance study for VP-MR-ETF-D1-001.
WF: select params on bars 0..629, freeze, evaluate untouched on 630..1259.
MC: 40 seeds x {OU, RW} to get Sharpe distributions. Deterministic."""
import math
import numpy as np
from vp_mr_strategy import StrategyParameters
from backtest_study import ou_prices, rw_prices, backtest

N = 1260
HALF = N // 2

print("=" * 72)
print("STUDY 4: WALK-FORWARD (select on 0..629, evaluate frozen on 630..1259)")
print("=" * 72)

GRID = [(z, lb) for z in (1.5, 2.0, 2.5) for lb in (60, 100, 150)]

def two_assets(gen, seed):
    if gen is rw_prices:
        return {"SPY": rw_prices(N, seed), "QQQ": rw_prices(N, seed + 1000, s0=380.0)}
    return {"SPY": ou_prices(N, seed), "QQQ": ou_prices(N, seed + 1000, s0=380.0, mu=380.0)}

def run_half(prices, params, lo, hi):
    """Run strategy on bars [lo, hi) only, with warm-up inside the window."""
    sub = {s: px[lo:hi] for s, px in prices.items()}
    return backtest(sub, params)[1]

# --- in-sample selection (first half) ---
best = None
print("  IN-SAMPLE grid (bars 0..629):")
print(f"  {'z':>5} {'lb':>4} {'sharpe':>7}")
for z, lb in GRID:
    prices = two_assets(ou_prices, 101)
    m = run_half(prices, StrategyParameters(zscore_entry=z, lookback_zscore=lb,
                                            min_history_bars=250), 0, HALF)
    print(f"  {z:>5} {lb:>4} {m['sharpe']:>7}")
    if best is None or m["sharpe"] > best[2]:
        best = (z, lb, m["sharpe"])
z_star, lb_star, is_sharpe = best
print(f"\n  SELECTED (frozen): z_entry={z_star}, lookback={lb_star} "
      f"[in-sample Sharpe {is_sharpe}]")

# --- out-of-sample evaluation (second half, frozen params) ---
prices = two_assets(ou_prices, 101)
oos = run_half(prices, StrategyParameters(zscore_entry=z_star,
                                          lookback_zscore=lb_star,
                                          min_history_bars=250), HALF, N)
print(f"  OUT-OF-SAMPLE (bars {HALF}..{N-1}, frozen params):")
for k, v in oos.items():
    print(f"  {k:>16}: {v}")
print(f"\n  WF verdict: in-sample {is_sharpe} -> out-of-sample {oos['sharpe']} "
      f"(decay ratio {round(oos['sharpe']/is_sharpe, 2) if is_sharpe else 'n/a'})")

print()
print("=" * 72)
print("STUDY 5: MONTE CARLO SIGNIFICANCE (40 seeds, default frozen params)")
print("=" * 72)
res = {"OU": [], "RW": []}
for k in range(40):
    seed = 5000 + k * 37
    res["OU"].append(backtest(two_assets(ou_prices, seed),
                              StrategyParameters())[1]["sharpe"])
    res["RW"].append(backtest(two_assets(rw_prices, seed),
                              StrategyParameters())[1]["sharpe"])
for name, arr in res.items():
    arr = np.array(arr)
    print(f"  {name:>3}: n={len(arr)}  mean={arr.mean():.3f}  "
          f"median={np.median(arr):.3f}  p5={np.percentile(arr,5):.3f}  "
          f"p95={np.percentile(arr,95):.3f}  P(Sharpe>0)={np.mean(arr>0)*100:.0f}%")
ou, rw = np.array(res["OU"]), np.array(res["RW"])
diff = ou - rw
se = diff.std(ddof=1) / math.sqrt(len(diff))
t = diff.mean() / se if se > 0 else 0.0
print(f"\n  OU vs RW Sharpe differential: mean={diff.mean():.3f}, "
      f"t-stat={t:.2f} ({'SIGNIFICANT' if abs(t) > 2.0 else 'NOT SIGNIFICANT'} at 5%)")
