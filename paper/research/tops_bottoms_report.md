# Tops-and-bottoms detection study

Two strictly-trailing detectors — RSI divergence and VSA volume climax — checked against the plain z-score entries: do confirmed entries forward-perform better than unconfirmed ones? Honest by design.

| Ticker | div bot | div top | clim bot | clim top | z entries | confirmed | unconfirmed | long fwd (conf) | long fwd (unconf) | short fwd (conf) | short fwd (unconf) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SPY | 6 | 25 | 3 | 2 | 140 | 21 | 119 | +0.0354 | +0.0242 | -0.0032 | +0.0075 |
| QQQ | 9 | 40 | 4 | 2 | 180 | 30 | 147 | +0.0390 | +0.0343 | -0.0018 | +0.0068 |
| IWM | 20 | 12 | 4 | 2 | 141 | 33 | 107 | +0.0340 | +0.0185 | -0.0133 | -0.0132 |
| XLF | 4 | 21 | 5 | 0 | 167 | 22 | 144 | +0.0167 | +0.0172 | +0.0026 | -0.0010 |
| XLE | 3 | 29 | 1 | 3 | 152 | 27 | 125 | +0.0444 | +0.0451 | +0.0085 | +0.0088 |

Reading: a detector helps only if confirmed entries forward-outperform unconfirmed ones on the correct side. Anything else is reported as a null result.
