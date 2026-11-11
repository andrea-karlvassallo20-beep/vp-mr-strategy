# Edge-seeker research report

Data: 1254 bars (selection window 752, OOS 502)

**Recommendation: PROPOSE_REDEPLOY**

## Out-of-sample comparison (last 40% of data)

| Variant | z_entry | lookback | vol model | VSA filter | exit z | ATR mult | OOS Sharpe | OOS Ann Ret % | OOS Max DD % | Fills |
|---|---|---|---|---|---|---|---|---|---|---|
| Selected candidate | 2.5 | 60 | garch | False | 0.25 | 3.0 | 0.469 | 2.11 | 4.95 | 130 |
| Production (frozen) | 2.0 | 100 | realized | False | 0.25 | 3.0 | -0.199 | -0.2 | 2.05 | 130 |

## Selection-window grid (train Sharpe)

| z_entry | lookback | vol model | VSA | exit z | ATR mult | train Sharpe |
|---|---|---|---|---|---|---|
| 1.5 | 60 | realized | False | 0.25 | 3.0 | -0.084 |
| 1.5 | 60 | realized | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 60 | ewma | False | 0.25 | 3.0 | -0.186 |
| 1.5 | 60 | ewma | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 60 | garch | False | 0.25 | 3.0 | -0.402 |
| 1.5 | 60 | garch | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 100 | realized | False | 0.25 | 3.0 | -0.501 |
| 1.5 | 100 | realized | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 100 | ewma | False | 0.25 | 3.0 | -0.483 |
| 1.5 | 100 | ewma | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 100 | garch | False | 0.25 | 3.0 | -0.412 |
| 1.5 | 100 | garch | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 150 | realized | False | 0.25 | 3.0 | -0.372 |
| 1.5 | 150 | realized | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 150 | ewma | False | 0.25 | 3.0 | -0.302 |
| 1.5 | 150 | ewma | True | 0.25 | 3.0 | 0.0 |
| 1.5 | 150 | garch | False | 0.25 | 3.0 | -0.584 |
| 1.5 | 150 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 60 | realized | False | 0.25 | 3.0 | 0.034 |
| 2.0 | 60 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 60 | ewma | False | 0.25 | 3.0 | 0.042 |
| 2.0 | 60 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 60 | garch | False | 0.25 | 3.0 | 0.228 |
| 2.0 | 60 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | realized | False | 0.25 | 3.0 | 0.302 |
| 2.0 | 100 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | ewma | False | 0.25 | 3.0 | 0.298 |
| 2.0 | 100 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 100 | garch | False | 0.25 | 3.0 | 0.223 |
| 2.0 | 100 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | realized | False | 0.25 | 3.0 | -0.071 |
| 2.0 | 150 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | ewma | False | 0.25 | 3.0 | -0.062 |
| 2.0 | 150 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.0 | 150 | garch | False | 0.25 | 3.0 | -0.039 |
| 2.0 | 150 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | realized | False | 0.25 | 3.0 | 0.968 |
| 2.5 | 60 | realized | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | ewma | False | 0.25 | 3.0 | 0.981 |
| 2.5 | 60 | ewma | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 60 | garch | False | 0.25 | 3.0 | 1.002 |
| 2.5 | 60 | garch | True | 0.25 | 3.0 | 0.0 |
| 2.5 | 100 | realized | False | 0.25 | 3.0 | 0.889 |
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
| 2.0 | 100 | realized | False | 0.0 | 3.0 | 0.225 |
| 2.0 | 100 | realized | False | 0.0 | 5.0 | 0.288 |
| 2.0 | 100 | realized | False | -0.5 | 3.0 | 0.27 |
| 2.0 | 100 | realized | False | -0.5 | 5.0 | 0.353 |
| 2.0 | 100 | realized | False | 0.25 | 5.0 | 0.372 |

## Gate 3

Deployed parameters remain frozen; any change requires a human-reviewed PR.
