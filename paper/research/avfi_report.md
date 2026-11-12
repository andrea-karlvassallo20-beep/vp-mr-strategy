# AVFI v3 risk-throttle research

Python replication of the Pine v5 'AVFI v3 vs v2 [spread axis]' indicator (Parkinson-style sigmaPk vol floor, log-volume normalization, spread vs slow EMA of v2, sigma-normalized z). AVFI is evaluated ONLY as a risk throttle, never as an entry timer.

| Ticker | Base Sharpe | Base MaxDD % | Throttle Sharpe | Throttle MaxDD % | Throttled bars |
|---|---|---|---|---|---|
| SPY | +0.58 | 35.4 | +0.57 | 35.4 | 16 |
| QQQ | +0.51 | 45.4 | +0.49 | 45.4 | 19 |
| IWM | +0.64 | 49.1 | +0.68 | 49.1 | 20 |
| XLF | +0.27 | 65.9 | +0.24 | 69.2 | 20 |
| XLE | +0.11 | 62.7 | +0.15 | 57.1 | 13 |

## Iteration ledger

Iteration 2 (2026-11-12) — params: {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.25, 'vol_estimator': 'parkinson', 'volume_mode': 'shares', 'entry_mode': 'detector'}
OOS drawdown reduction: 0.5% at Sharpe delta -0.005
Best candidate: {'params': {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.5, 'vol_estimator': 'parkinson', 'volume_mode': 'shares', 'entry_mode': 'detector', 'z_entry': 2.5}, 'oos_dd_reduction_pct': np.float64(17.35), 'oos_sharpe_delta': np.float64(0.144)}
Advanced: True -> next params: {'vol_window': 20, 'pk_window': 10, 'ema_slow': 13, 'sp_z_window': 100, 'trigger': -1.5, 'throttle': 0.5, 'vol_estimator': 'parkinson', 'volume_mode': 'shares', 'entry_mode': 'detector', 'z_entry': 2.5}

Per the AVFI-NQ programme (KNOWLEDGE (1).md): AVFI is a slow regime descriptor, not an entry timer; only the risk-throttle use is evaluated. Research parameters iterate nightly with train/OOS honesty; the deployed strategy stays frozen (Gate 3).
