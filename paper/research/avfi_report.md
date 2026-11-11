# AVFI v3 risk-throttle research

Python replication of the Pine v5 'AVFI v3 vs v2 [spread axis]' indicator (Parkinson-style sigmaPk vol floor, log-volume normalization, spread vs slow EMA of v2, sigma-normalized z). Per the programme's evidence, AVFI is evaluated ONLY as a risk throttle (halve exposure when sp_z <= -1), never as an entry timer.

| Ticker | Base Sharpe | Base MaxDD % | Throttle Sharpe | Throttle MaxDD % | Throttled bars |
|---|---|---|---|---|---|
| SPY | +0.11 | 77.2 | +0.09 | 69.0 | 134 |
| QQQ | -0.06 | 119.4 | +0.01 | 115.1 | 138 |
| IWM | +0.38 | 64.2 | +0.40 | 52.5 | 89 |
| XLF | +0.30 | 86.7 | +0.22 | 86.7 | 146 |
| XLE | +0.72 | 34.6 | +0.78 | 31.6 | 109 |

Per the AVFI-NQ programme (KNOWLEDGE (1).md): AVFI is a slow regime descriptor, not an entry timer; only the risk-throttle use is evaluated here.

Honest reading: the throttle is judged on drawdown reduction at preserved Sharpe (the programme's U2 result), not on Sharpe improvement. Negative results are reported.
