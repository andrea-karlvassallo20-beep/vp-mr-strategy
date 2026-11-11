# Tops-and-bottoms detection study

Two strictly-trailing detectors — RSI divergence and VSA volume climax — checked against the plain z-score entries: do confirmed entries forward-perform better than unconfirmed ones? Honest by design.

| Ticker | div bot | div top | clim bot | clim top | z entries | confirmed | unconfirmed | long fwd (conf) | long fwd (unconf) | short fwd (conf) | short fwd (unconf) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SPY | 6 | 25 | 3 | 2 | 140 | 21 | 119 | +0.0354 | +0.0242 | -0.0032 | +0.0075 |
| QQQ | 9 | 40 | 4 | 2 | 180 | 30 | 147 | +0.0390 | +0.0343 | -0.0018 | +0.0068 |
| IWM | 19 | 12 | 4 | 2 | 141 | 33 | 107 | +0.0340 | +0.0185 | -0.0133 | -0.0132 |
| XLF | 4 | 21 | 5 | 0 | 167 | 22 | 144 | +0.0167 | +0.0172 | +0.0026 | -0.0010 |
| XLE | 3 | 29 | 1 | 3 | 152 | 27 | 125 | +0.0444 | +0.0451 | +0.0085 | +0.0088 |

## Multi-dimensional turn topology (confluence score)

Forward returns by number of aligned dimensions (price stretch, momentum, divergence, effort, AVFI regime)
at the entry bar. Monotonicity across buckets is the honest test.

| Ticker | score | n | long fwd | short fwd (neg) |
|---|---|---|---|---|
| SPY | 1 | 4 | +0.0448 | - |
| SPY | 2 | 110 | +0.0225 | -0.0075 |
| SPY | 3 | 26 | +0.0304 | +0.0032 |
| QQQ | 1 | 5 | +0.0657 | - |
| QQQ | 2 | 142 | +0.0289 | -0.0063 |
| QQQ | 3 | 30 | +0.0439 | -0.0016 |
| IWM | 1 | 2 | +0.0515 | - |
| IWM | 2 | 106 | +0.0163 | +0.0132 |
| IWM | 3 | 27 | +0.0285 | +0.0133 |
| IWM | 4 | 5 | +0.0557 | - |
| XLF | 1 | 1 | +0.0830 | - |
| XLF | 2 | 146 | +0.0142 | +0.0001 |
| XLF | 3 | 19 | +0.0256 | +0.0056 |
| XLE | 1 | 2 | +0.0967 | -0.0719 |
| XLE | 2 | 125 | +0.0419 | -0.0103 |
| XLE | 3 | 25 | +0.0482 | +0.0029 |

Reading: a detector helps only if confirmed entries forward-outperform unconfirmed ones on the correct side. Anything else is reported as a null result.
