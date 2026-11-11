# Cross-asset edge research

Does the mean-reversion edge exist outside the deployed
universe? Each series: OU half-life estimate and a
production-style z-score backtest vs buy-and-hold.
The deployed champion stays frozen (Gate 3); this is
research toward future challenger candidates.

## Commoditys

| Class | Ticker | Bars | OU half-life | MR Sharpe | MR trades | MR return | B&H Sharpe | Mean-reverting? |
|---|---|---|---|---|---|---|---|---|
| commodity | BZ=F | 1258 | 57.3 | +0.47 | 46 | +441.7% | +0.05 | no |
| commodity | CC=F | 1257 | 286.6 | -0.43 | 45 | -76.8% | +0.28 | no |
| commodity | CL=F | 1257 | 53.6 | +0.35 | 44 | +237.6% | +0.03 | no |
| commodity | CT=F | 1258 | 136.5 | +0.61 | 46 | +556.0% | -0.24 | no |
| commodity | GC=F | 1258 | 2076.8 | -0.57 | 35 | -89.5% | +0.79 | no |
| commodity | GF=F | 1256 | 490.4 | -0.41 | 36 | -79.9% | +0.88 | no |
| commodity | HE=F | 1256 | 59.8 | +0.19 | 29 | +101.6% | -0.16 | no |
| commodity | HG=F | 1258 | 204.3 | +0.43 | 47 | +424.2% | +0.25 | no |
| commodity | HO=F | 1258 | 105.1 | +0.29 | 39 | +195.9% | +0.24 | no |
| commodity | KC=F | 1258 | 206.4 | +0.17 | 46 | +82.7% | +0.12 | no |
| commodity | LBS=F | - | - | - | - | - | - | NO DATA (yfinance fetch failed for LBS=F after 3 attempts: empty frame for LBS=F) |
| commodity | LE=F | 1256 | 311.5 | +0.53 | 40 | +628.9% | +0.67 | no |
| commodity | NG=F | 1258 | 73.4 | +0.21 | 43 | +96.0% | -0.11 | no |
| commodity | OJ=F | 1258 | 185.7 | +0.63 | 44 | +698.3% | +0.05 | no |
| commodity | PA=F | 1256 | 125.3 | +0.31 | 41 | +202.2% | -0.30 | no |
| commodity | PL=F | 1257 | 239.1 | +0.55 | 53 | +650.9% | +0.19 | no |
| commodity | RB=F | 1258 | 82.8 | -0.20 | 41 | -48.8% | +0.05 | no |
| commodity | SB=F | 1258 | 146.0 | +0.15 | 40 | +64.2% | -0.06 | no |
| commodity | SI=F | 1257 | 504.2 | -0.26 | 37 | -63.9% | +0.35 | no |
| commodity | ZC=F | 1256 | 229.8 | -0.12 | 40 | -33.2% | -0.19 | no |
| commodity | ZO=F | 1256 | 90.4 | +0.65 | 48 | +758.1% | -0.36 | no |
| commodity | ZR=F | 1256 | 167.7 | +0.46 | 37 | +259.9% | +0.21 | no |
| commodity | ZS=F | 1256 | 217.3 | +0.58 | 47 | +538.4% | +0.01 | no |
| commodity | ZW=F | 1256 | 112.9 | +0.58 | 51 | +714.4% | -0.17 | no |

## Cryptos

| Class | Ticker | Bars | OU half-life | MR Sharpe | MR trades | MR return | B&H Sharpe | Mean-reverting? |
|---|---|---|---|---|---|---|---|---|
| crypto | AAVE-USD | 1827 | 113.9 | +0.33 | 64 | +471.3% | -0.16 | no |
| crypto | ADA-USD | 1827 | 144.4 | +0.00 | 63 | +1.3% | -0.49 | no |
| crypto | ALGO-USD | 1827 | 145.8 | -0.43 | 60 | -90.9% | -0.58 | yes |
| crypto | APT-USD | - | - | - | - | - | - | NO DATA (yfinance fetch failed for APT-USD after 3 attempts: empty frame for APT-USD) |
| crypto | ARB-USD | 1827 | 63.5 | +0.37 | 44 | +145.8% | -0.06 | yes |
| crypto | ATOM-USD | 1827 | 425.6 | -0.39 | 49 | -86.6% | -0.62 | no |
| crypto | AVAX-USD | 1827 | 211.1 | -0.61 | 52 | -96.2% | -0.41 | no |
| crypto | BCH-USD | 1827 | 186.7 | +0.32 | 58 | +426.6% | -0.22 | no |
| crypto | BNB-USD | 1827 | 338.5 | -0.16 | 59 | -60.6% | +0.02 | no |
| crypto | BTC-USD | 1827 | 691.2 | -0.55 | 57 | -94.8% | +0.04 | no |
| crypto | DOGE-USD | 1827 | 138.7 | -0.26 | 53 | -77.1% | -0.26 | no |
| crypto | DOT-USD | 1827 | 306.5 | -0.25 | 57 | -73.8% | -0.81 | no |
| crypto | ETC-USD | 1827 | 154.1 | +0.19 | 56 | +162.1% | -0.44 | no |
| crypto | ETH-USD | 1827 | 106.7 | -0.66 | 55 | -97.2% | -0.20 | no |
| crypto | FIL-USD | 1827 | 216.1 | +0.22 | 61 | +197.5% | -0.73 | no |
| crypto | HBAR-USD | 1827 | 136.3 | -0.28 | 52 | -80.0% | -0.33 | no |
| crypto | ICP-USD | 1827 | 135.2 | -0.29 | 46 | -78.0% | -0.49 | no |
| crypto | LINK-USD | 1827 | 93.3 | +0.03 | 58 | +15.4% | -0.24 | no |
| crypto | LTC-USD | 1827 | 61.6 | +0.19 | 68 | +162.5% | -0.37 | yes |
| crypto | NEAR-USD | 1827 | 153.7 | -0.11 | 60 | -46.2% | -0.19 | no |
| crypto | OP-USD | 1704 | 168.2 | -0.27 | 54 | -34.5% | +0.22 | no |
| crypto | SOL-USD | 1827 | 323.7 | -0.57 | 55 | -95.9% | -0.19 | no |
| crypto | UNI-USD | - | - | - | - | - | - | NO DATA (yfinance fetch failed for UNI-USD after 3 attempts: empty frame for UNI-USD) |
| crypto | XLM-USD | 1827 | 147.0 | -0.23 | 55 | -72.0% | -0.20 | no |
| crypto | XRP-USD | 1827 | 374.3 | -0.12 | 53 | -48.2% | -0.03 | no |

## Indexs

| Class | Ticker | Bars | OU half-life | MR Sharpe | MR trades | MR return | B&H Sharpe | Mean-reverting? |
|---|---|---|---|---|---|---|---|---|
| index | ^DJI | 1254 | 1181.6 | +0.75 | 44 | +1137.9% | +0.50 | no |
| index | ^GSPC | 1254 | 3803.7 | +0.31 | 37 | +199.4% | +0.57 | no |
| index | ^IXIC | 1254 | 1545.1 | -0.00 | 39 | -1.2% | +0.41 | no |
| index | ^RUT | 1254 | 235.7 | +0.35 | 38 | +211.1% | +0.15 | no |


Best mean-reversion candidate: **^DJI** (index) with MR Sharpe +0.75 vs buy-and-hold +0.50.

Series where mean reversion beats buy-and-hold: LINK-USD, LTC-USD, BCH-USD, ARB-USD, FIL-USD, ETC-USD, AAVE-USD, ^DJI, ^RUT, PL=F, PA=F, CL=F, BZ=F, NG=F, HO=F, HG=F, ZS=F, ZW=F, ZO=F, ZR=F, KC=F, SB=F, CT=F, OJ=F, HE=F.
