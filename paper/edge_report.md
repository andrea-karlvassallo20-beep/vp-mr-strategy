# Edge-seeker research report

Data: 1254 bars (selection window 752, OOS 502)

**Recommendation: PROPOSE_REDEPLOY**

## Out-of-sample comparison (last 40% of data)

| Variant | z_entry | lookback | vol model | VSA filter | exit z | ATR mult | OOS Sharpe | OOS Ann Ret % | OOS Max DD % | Fills |
|---|---|---|---|---|---|---|---|---|---|---|
| Selected candidate | 2.5 | 60 | garch | False | 0.25 | 3.0 | 0.392 | 1.77 | 4.95 | 128 |
| Production (frozen) | 2.0 | 100 | realized | False | 0.25 | 3.0 | -0.365 | -0.39 | 1.9 | 128 |

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
| 1.5 | 100 | garch | False | 0.25 | 3.0 | -0.421 |
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
| 2.0 | 100 | realized | False | 0.25 | 3.0 | 0.311 |
| 2.0 | 100 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | ewma | False | 0.25 | 3.0 | 0.303 |
| 2.0 | 100 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | garch | False | 0.25 | 3.0 | 0.227 |
| 2.0 | 100 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | realized | False | 0.25 | 3.0 | -0.077 |
| 2.0 | 150 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | ewma | False | 0.25 | 3.0 | -0.071 |
| 2.0 | 150 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | garch | False | 0.25 | 3.0 | -0.051 |
| 2.0 | 150 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | realized | False | 0.25 | 3.0 | 1.008 |
| 2.5 | 60 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | ewma | False | 0.25 | 3.0 | 1.016 |
| 2.5 | 60 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | garch | False | 0.25 | 3.0 | 1.037 |
| 2.5 | 60 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 100 | realized | False | 0.25 | 3.0 | 0.919 |
| 2.5 | 100 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 100 | ewma | False | 0.25 | 3.0 | 0.901 |
| 2.5 | 100 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 100 | garch | False | 0.25 | 3.0 | 0.876 |
| 2.5 | 100 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 150 | realized | False | 0.25 | 3.0 | 0.014 |
| 2.5 | 150 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 150 | ewma | False | 0.25 | 3.0 | -0.01 |
| 2.5 | 150 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 150 | garch | False | 0.25 | 3.0 | -0.007 |
| 2.5 | 150 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | realized | False | 0.0 | 3.0 | 0.232 |
| 2.0 | 100 | realized | False | 0.0 | 5.0 | 0.292 |
| 2.0 | 100 | realized | False | -0.5 | 3.0 | 0.276 |
| 2.0 | 100 | realized | False | -0.5 | 5.0 | 0.356 |
| 2.0 | 100 | realized | False | 0.25 | 5.0 | 0.38 |

## Gate 3

Deployed parameters remain frozen; any change requires a human-reviewed PR.
