# AVFI v3 risk-throttle research

Python replication of the Pine v5 'AVFI v3 vs v2 [spread axis]' indicator (Parkinson-style sigmaPk vol floor, log-volume normalization, spread vs slow EMA of v2, sigma-normalized z). AVFI is evaluated ONLY as a risk throttle, never as an entry timer.

| Ticker | Base Sharpe | Base MaxDD % | Throttle Sharpe | Throttle MaxDD % | Throttled bars |
|---|---|---|---|---|---|
| SPY | +0.11 | 77.2 | +0.08 | 74.6 | 38 |
| QQQ | -0.03 | 119.4 | -0.04 | 110.2 | 43 |
| IWM | +0.39 | 64.2 | +0.43 | 64.2 | 34 |
| XLF | +0.29 | 86.7 | +0.23 | 86.7 | 45 |
| XLE | +0.72 | 34.6 | +0.77 | 30.7 | 48 |

## Iteration ledger

Iteration 1 (2026-11-11) — params: {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.25}
OOS drawdown reduction: 4.43% at Sharpe delta -0.017
Best candidate: {'params': {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.25}, 'oos_dd_reduction_pct': np.float64(4.43), 'oos_sharpe_delta': np.float64(-0.017)}
Advanced: False -> next params: {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.25}

Per the AVFI-NQ programme (KNOWLEDGE (1).md): AVFI is a slow regime descriptor, not an entry timer; only the risk-throttle use is evaluated. Research parameters iterate nightly with train/OOS honesty; the deployed strategy stays frozen (Gate 3).
