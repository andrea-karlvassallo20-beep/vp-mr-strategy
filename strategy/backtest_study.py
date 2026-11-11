"""Hypothesis validation + robustness study for VP-MR-ETF-D1-001.
Deterministic; numpy only. MTM equity reconstructed from exact post-fill
positions recorded by the harness loop (engine Portfolio equivalent)."""
import math
import numpy as np
from vp_mr_strategy import StrategyParameters, VolatilityParityMeanReversionStrategy


def ou_prices(n, seed, s0=450.0, theta=0.05, mu=450.0, sigma=1.2):
    rng = np.random.default_rng(seed)
    p = np.empty(n); p[0] = s0
    for i in range(1, n):
        p[i] = p[i-1] + theta * (mu - p[i-1]) + rng.normal(0, sigma)
    return p


def rw_prices(n, seed, s0=450.0, sigma=1.2):
    rng = np.random.default_rng(seed)
    return s0 + np.cumsum(rng.normal(0, sigma, n))


def scaled_params(cost_mult):
    p = StrategyParameters()
    return StrategyParameters(
        half_spread_bps=p.half_spread_bps * cost_mult,
        commission_bps=p.commission_bps * cost_mult,
        impact_coeff=p.impact_coeff * cost_mult)


def backtest(prices_dict, params=None):
    if params is None:
        params = StrategyParameters()
    strat = VolatilityParityMeanReversionStrategy(
        params, list(prices_dict.keys()), initial_equity=1_000_000.0)
    strat.deploy()
    n = len(next(iter(prices_dict.values())))
    insts = list(prices_dict.keys())
    pos_hist = {s: np.zeros(n) for s in insts}
    for t in range(n):
        if t % 252 == 0:
            strat.on_session_start()
        for s in insts:
            c = float(prices_dict[s][t])
            strat.on_bar_close(s, t, c, c * 1.002, c * 0.998, c, 1e6)
            if s in strat._pending and t + 1 < n:
                strat.on_order_fill(s, float(prices_dict[s][t + 1]))
            pos_hist[s][t] = strat.position[s]  # exact post-fill position
        if t % 252 == 251:
            strat.on_session_end()
    return strat, metrics(strat, prices_dict, pos_hist)


def metrics(strat, prices_dict, pos_hist):
    n = len(next(iter(prices_dict.values())))
    pnl = np.zeros(n)
    for s, px in prices_dict.items():
        pnl[1:] += pos_hist[s][:-1] * np.diff(px)
    cum_pnl = np.cumsum(pnl)
    cum_cost = strat.initial_equity - np.array(strat.equity_curve)[::len(prices_dict)]
    eq = strat.initial_equity + cum_pnl - cum_cost[:n]
    rets = np.diff(eq) / eq[:-1]
    ann_ret = float(rets.mean() * 252)
    ann_vol = float(rets.std(ddof=1) * math.sqrt(252))
    sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0
    peak = np.maximum.accumulate(eq)
    max_dd = float(((peak - eq) / peak).max())
    fills = [o for o in strat.order_log if o.get("state") == "FILLED"]
    gross_pnl = float(cum_pnl[-1])
    return {"final_equity": round(float(eq[-1]), 2),
            "gross_pnl": round(gross_pnl, 2),
            "total_costs": round(float(cum_cost[-1]), 2),
            "ann_return_pct": round(ann_ret * 100, 3),
            "ann_vol_pct": round(ann_vol * 100, 3),
            "sharpe": round(sharpe, 3),
            "max_dd_pct": round(max_dd * 100, 3),
            "round_trips": len(fills) // 2}


def show(title, m):
    print(f"  --- {title} ---")
    for k, v in m.items():
        print(f"  {k:>16}: {v}")


if __name__ == "__main__":
    n = 1260
    print("=" * 72)
    print("STUDY 1: HYPOTHESIS VALIDATION (5y, 2 assets)")
    print("=" * 72)
    data_ou = {"SPY": ou_prices(n, 101), "QQQ": ou_prices(n, 202, s0=380.0, mu=380.0)}
    data_rw = {"SPY": rw_prices(n, 101), "QQQ": rw_prices(n, 202, s0=380.0)}
    show("OU mean-reverting (hypothesis TRUE)", backtest(data_ou)[1])
    print()
    show("Random walk (hypothesis FALSE, control)", backtest(data_rw)[1])
    
    print()
    print("=" * 72)
    print("STUDY 2: PARAMETER ROBUSTNESS GRID (OU data; pre-deployment only)")
    print("=" * 72)
    print(f"  {'z_entry':>8} {'lookback':>9} {'sharpe':>8} {'ann_ret%':>9} {'maxDD%':>7} {'trips':>6}")
    shs = []
    for z_e in (1.5, 2.0, 2.5):
        for lb in (60, 100, 150):
            m = backtest(data_ou, StrategyParameters(zscore_entry=z_e,
                                                     lookback_zscore=lb))[1]
            shs.append(m["sharpe"])
            print(f"  {z_e:>8} {lb:>9} {m['sharpe']:>8} {m['ann_return_pct']:>9} "
                  f"{m['max_dd_pct']:>7} {m['round_trips']:>6}")
    print(f"\n  Sharpe: min={min(shs)}, max={max(shs)}, mean={round(float(np.mean(shs)),3)}")
    
    print()
    print("=" * 72)
    print("STUDY 3: COST SENSITIVITY (OU data, default params)")
    print("=" * 72)
    print(f"  {'cost_mult':>9} {'sharpe':>8} {'ann_ret%':>9} {'gross_pnl':>11} {'costs':>10}")
    for cm in (0.25, 0.5, 1.0, 2.0):
        m = backtest(data_ou, scaled_params(cm))[1]
        print(f"  {cm:>9} {m['sharpe']:>8} {m['ann_return_pct']:>9} "
              f"{m['gross_pnl']:>11} {m['total_costs']:>10}")
