# Cross-asset edge research

Does the mean-reversion edge exist outside the deployed
universe? Each series: OU half-life estimate and a
production-style z-score backtest vs buy-and-hold.
The deployed champion stays frozen (Gate 3); this is
research toward future challenger candidates.

| Class | Ticker | Bars | OU half-life | MR Sharpe | MR trades | MR return | B&H Sharpe | Mean-reverting? |
|---|---|---|---|---|---|---|---|---|
| commodity | CL=F | 1257 | 53.7 | +0.35 | 44 | +237.6% | +0.03 | no |
| commodity | GC=F | 1258 | 2119.2 | -0.57 | 35 | -89.3% | +0.79 | no |
| commodity | SI=F | 1257 | 510.9 | -0.25 | 37 | -63.1% | +0.35 | no |
| crypto | BTC-USD | 1827 | 695.3 | -0.54 | 57 | -94.7% | +0.04 | no |
| crypto | ETH-USD | 1827 | 106.5 | -0.66 | 55 | -97.2% | -0.20 | no |
| index | ^DJI | 1255 | 1153.6 | +0.75 | 44 | +1138.9% | +0.51 | no |
| index | ^GSPC | 1255 | 3879.3 | +0.32 | 37 | +204.6% | +0.58 | no |
| index | ^IXIC | 1255 | 1618.9 | +0.00 | 39 | +1.5% | +0.43 | no |

Best mean-reversion candidate: **^DJI** (index) with MR Sharpe +0.75 vs buy-and-hold +0.51.

Series where mean reversion beats buy-and-hold: ^DJI, CL=F.
