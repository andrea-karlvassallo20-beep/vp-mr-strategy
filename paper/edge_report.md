# Edge-seeker research report

Data: 1255 bars (selection window 753, OOS 502)

**Recommendation: PROPOSE_REDEPLOY**

## Out-of-sample comparison (last 40% of data)

| Variant | z_entry | lookback | vol model | VSA filter | exit z | ATR mult | OOS Sharpe | OOS Ann Ret % | OOS Max DD % | Fills |
|---|---|---|---|---|---|---|---|---|---|---|
| Selected candidate | 2.5 | 60 | garch | False | 0.25 | 3.0 | 0.472 | 2.12 | 4.95 | 128 |
| Production (frozen) | 2.0 | 100 | realized | False | 0.25 | 3.0 | -0.12 | -0.12 | 1.9 | 128 |

## Selection-window grid (train Sharpe)

| z_entry | lookback | vol model | VSA | exit z | ATR mult | train Sharpe |
|---|---|---|---|---|---|---|
| 1.5 | 60 | realized | False | 0.25 | 3.0 | -0.129 |
| 1.5 | 60 | realized | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 60 | ewma | False | 0.25 | 3.0 | -0.214 |
| 1.5 | 60 | ewma | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 60 | garch | False | 0.25 | 3.0 | -0.429 |
| 1.5 | 60 | garch | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 100 | realized | False | 0.25 | 3.0 | -0.512 |
| 1.5 | 100 | realized | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 100 | ewma | False | 0.25 | 3.0 | -0.493 |
| 1.5 | 100 | ewma | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 100 | garch | False | 0.25 | 3.0 | -0.42 |
| 1.5 | 100 | garch | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 150 | realized | False | 0.25 | 3.0 | -0.384 |
| 1.5 | 150 | realized | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 150 | ewma | False | 0.25 | 3.0 | -0.314 |
| 1.5 | 150 | ewma | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 150 | garch | False | 0.25 | 3.0 | -0.596 |
| 1.5 | 150 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 60 | realized | False | 0.25 | 3.0 | 0.045 |
| 2.0 | 60 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 60 | ewma | False | 0.25 | 3.0 | 0.067 |
| 2.0 | 60 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 60 | garch | False | 0.25 | 3.0 | 0.26 |
| 2.0 | 60 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | realized | False | 0.25 | 3.0 | 0.275 |
| 2.0 | 100 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | ewma | False | 0.25 | 3.0 | 0.271 |
| 2.0 | 100 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | garch | False | 0.25 | 3.0 | 0.195 |
| 2.0 | 100 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | realized | False | 0.25 | 3.0 | -0.095 |
| 2.0 | 150 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | ewma | False | 0.25 | 3.0 | -0.086 |
| 2.0 | 150 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | garch | False | 0.25 | 3.0 | -0.065 |
| 2.0 | 150 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | realized | False | 0.25 | 3.0 | 0.967 |
| 2.5 | 60 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | ewma | False | 0.25 | 3.0 | 0.98 |
| 2.5 | 60 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | garch | False | 0.25 | 3.0 | 1.002 |
| 2.5 | 60 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 100 | realized | False | 0.25 | 3.0 | 0.888 |
| 2.5 | 100 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 100 | ewma | False | 0.25 | 3.0 | 0.874 |
| 2.5 | 100 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 100 | garch | False | 0.25 | 3.0 | 0.85 |
| 2.5 | 100 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 150 | realized | False | 0.25 | 3.0 | -0.03 |
| 2.5 | 150 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 150 | ewma | False | 0.25 | 3.0 | -0.047 |
| 2.5 | 150 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 150 | garch | False | 0.25 | 3.0 | -0.04 |
| 2.5 | 150 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | realized | False | 0.0 | 3.0 | 0.199 |
| 2.0 | 100 | realized | False | 0.0 | 5.0 | 0.261 |
| 2.0 | 100 | realized | False | -0.5 | 3.0 | 0.244 |
| 2.0 | 100 | realized | False | -0.5 | 5.0 | 0.326 |
| 2.0 | 100 | realized | False | 0.25 | 5.0 | 0.346 |

## Gate 3

Deployed parameters remain frozen; any change requires a human-reviewed PR.
