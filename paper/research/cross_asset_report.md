# Cross-asset edge research

Does the mean-reversion edge exist outside the deployed
universe? Each series: OU half-life estimate and a
production-style z-score backtest vs buy-and-hold.
The deployed champion stays frozen (Gate 3); this is
research toward future challenger candidates.

## Commoditys

| Class | Ticker | Bars | OU half-life | MR Sharpe | MR trades | MR return | B&H Sharpe | Mean-reverting? |
|---|---|---|---|---|---|---|---|---|
| commodity | BZ=F | 1258 | 57.3 | +0.47 | 46 | +441.7% | +0.06 | no |
| commodity | CC=F | 1257 | 286.6 | -0.43 | 45 | -76.8% | +0.28 | no |
| commodity | CL=F | 1257 | 53.6 | +0.35 | 44 | +237.6% | +0.03 | no |
| commodity | CT=F | 1258 | 136.5 | +0.61 | 46 | +556.0% | -0.24 | no |
| commodity | GC=F | 1258 | 2092.3 | -0.57 | 35 | -89.4% | +0.79 | no |
| commodity | HG=F | 1258 | 205.1 | +0.43 | 47 | +427.1% | +0.25 | no |
| commodity | KC=F | 1258 | 206.4 | +0.17 | 46 | +82.7% | +0.12 | no |
| commodity | NG=F | 1258 | 73.4 | +0.21 | 43 | +95.7% | -0.11 | no |
| commodity | PA=F | 1256 | 125.3 | +0.31 | 41 | +202.5% | -0.30 | no |
| commodity | PL=F | 1257 | 240.0 | +0.56 | 53 | +658.3% | +0.19 | no |
| commodity | SB=F | 1258 | 146.0 | +0.15 | 40 | +64.2% | -0.06 | no |
| commodity | SI=F | 1257 | 506.6 | -0.25 | 37 | -63.6% | +0.35 | no |
| commodity | ZC=F | 1256 | 229.8 | -0.12 | 40 | -33.2% | -0.19 | no |
| commodity | ZS=F | 1256 | 217.3 | +0.58 | 47 | +538.4% | +0.01 | no |
| commodity | ZW=F | 1256 | 112.9 | +0.58 | 51 | +714.4% | -0.17 | no |

## Cryptos

| Class | Ticker | Bars | OU half-life | MR Sharpe | MR trades | MR return | B&H Sharpe | Mean-reverting? |
|---|---|---|---|---|---|---|---|---|
| crypto | AAVE-USD | 1827 | 114.0 | +0.33 | 64 | +471.3% | -0.16 | no |
| crypto | ADA-USD | 1827 | 143.4 | +0.01 | 63 | +3.9% | -0.48 | no |
| crypto | ALGO-USD | 1827 | 145.3 | -0.43 | 60 | -90.9% | -0.58 | yes |
| crypto | APT-USD | - | - | - | - | - | - | NO DATA (yfinance fetch failed for APT-USD after 3 attempts: empty frame for APT-USD) |
| crypto | ARB-USD | 1827 | 63.5 | +0.37 | 44 | +145.8% | -0.06 | yes |
| crypto | ATOM-USD | 1827 | 423.8 | -0.39 | 49 | -86.5% | -0.61 | no |
| crypto | AVAX-USD | 1827 | 210.2 | -0.61 | 52 | -96.2% | -0.41 | no |
| crypto | BCH-USD | 1827 | 186.5 | +0.32 | 58 | +426.6% | -0.22 | no |
| crypto | BNB-USD | 1827 | 340.2 | -0.16 | 59 | -59.7% | +0.02 | no |
| crypto | BTC-USD | 1827 | 694.2 | -0.54 | 57 | -94.7% | +0.04 | no |
| crypto | DOGE-USD | 1827 | 138.0 | -0.26 | 53 | -76.5% | -0.25 | no |
| crypto | DOT-USD | 1827 | 303.6 | -0.24 | 57 | -73.1% | -0.81 | no |
| crypto | ETC-USD | 1827 | 152.5 | +0.19 | 56 | +162.1% | -0.43 | no |
| crypto | ETH-USD | 1827 | 106.6 | -0.66 | 55 | -97.2% | -0.20 | no |
| crypto | FIL-USD | 1827 | 214.8 | +0.23 | 61 | +204.3% | -0.73 | no |
| crypto | HBAR-USD | 1827 | 136.0 | -0.28 | 52 | -80.0% | -0.33 | no |
| crypto | ICP-USD | 1827 | 134.8 | -0.29 | 46 | -78.0% | -0.49 | no |
| crypto | LINK-USD | 1827 | 93.2 | +0.03 | 58 | +15.4% | -0.23 | yes |
| crypto | LTC-USD | 1827 | 61.5 | +0.19 | 68 | +162.6% | -0.37 | yes |
| crypto | NEAR-USD | 1827 | 153.9 | -0.11 | 60 | -46.2% | -0.18 | no |
| crypto | OP-USD | 1704 | 168.2 | -0.27 | 54 | -34.5% | +0.22 | no |
| crypto | SOL-USD | 1827 | 323.9 | -0.56 | 55 | -95.8% | -0.18 | no |
| crypto | UNI-USD | - | - | - | - | - | - | NO DATA (yfinance fetch failed for UNI-USD after 3 attempts: empty frame for UNI-USD) |
| crypto | XLM-USD | 1827 | 146.8 | -0.22 | 55 | -71.2% | -0.20 | no |
| crypto | XRP-USD | 1827 | 374.9 | -0.12 | 53 | -47.2% | -0.03 | no |

## Indexs

| Class | Ticker | Bars | OU half-life | MR Sharpe | MR trades | MR return | B&H Sharpe | Mean-reverting? |
|---|---|---|---|---|---|---|---|---|
| index | ^DJI | 1254 | 1181.6 | +0.75 | 44 | +1137.9% | +0.50 | no |
| index | ^GSPC | 1254 | 3803.7 | +0.31 | 37 | +199.4% | +0.57 | no |
| index | ^IXIC | 1254 | 1545.1 | -0.00 | 39 | -1.2% | +0.41 | no |
| index | ^RUT | 1254 | 235.7 | +0.35 | 38 | +211.1% | +0.15 | no |


Best mean-reversion candidate: **^DJI** (index) with MR Sharpe +0.75 vs buy-and-hold +0.50.

Series where mean reversion beats buy-and-hold: ADA-USD, LINK-USD, LTC-USD, BCH-USD, ARB-USD, FIL-USD, ETC-USD, AAVE-USD, ^DJI, ^RUT, PL=F, PA=F, CL=F, NG=F, BZ=F, HG=F, KC=F, SB=F, CT=F, ZS=F, ZW=F.
