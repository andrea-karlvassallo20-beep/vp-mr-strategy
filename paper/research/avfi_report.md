# AVFI v3 risk-throttle research

Python replication of the Pine v5 'AVFI v3 vs v2 [spread axis]' indicator (Parkinson-style sigmaPk vol floor, log-volume normalization, spread vs slow EMA of v2, sigma-normalized z). AVFI is evaluated ONLY as a risk throttle, never as an entry timer.

| Ticker | Base Sharpe | Base MaxDD % | Throttle Sharpe | Throttle MaxDD % | Throttled bars |
|---|---|---|---|---|---|
| SPY | +0.11 | 77.2 | +0.09 | 69.0 | 134 |
| QQQ | -0.06 | 119.4 | +0.01 | 115.1 | 138 |
| IWM | +0.38 | 64.2 | +0.40 | 52.5 | 89 |
| XLF | +0.30 | 86.7 | +0.22 | 86.7 | 146 |
| XLE | +0.72 | 34.6 | +0.78 | 31.6 | 109 |

## Iteration ledger

Iteration 1 (2026-11-11) — params: {'vol_window': 20, 'pk_window': 20, 'ema_slow': 26, 'sp_z_window': 100, 'trigger': -1.0, 'throttle': 0.5}
OOS drawdown reduction: 3.39% at Sharpe delta -0.096
Best candidate: {'params': {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.25}, 'oos_dd_reduction_pct': np.float64(4.45), 'oos_sharpe_delta': np.float64(-0.021)}
Advanced: True -> next params: {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.25}

Per the AVFI-NQ programme (KNOWLEDGE (1).md): AVFI is a slow regime descriptor, not an entry timer; only the risk-throttle use is evaluated. Research parameters iterate nightly with train/OOS honesty; the deployed strategy stays frozen (Gate 3).
