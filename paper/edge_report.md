# Edge-seeker research report

Data: 502 bars (selection window 301, OOS 201)

**Recommendation: PROPOSE_REDEPLOY**

## Out-of-sample comparison (last 40% of data)

| Variant | z_entry | lookback | OOS Sharpe | OOS Ann Ret % | OOS Max DD % | Fills |
|---|---|---|---|---|---|---|
| Selected candidate | 1.5 | 60 | -0.517 | -4.53 | 7.79 | 95 |
| Production (frozen) | 2.0 | 100 | -1.162 | -8.4 | 8.37 | 95 |

## Selection-window grid (train Sharpe)

| z_entry | lookback | train Sharpe |
|---|---|---|
| 1.5 | 60 | 0.502 |
| 1.5 | 100 | 0.477 |
| 1.5 | 150 | -0.428 |
| 2.0 | 60 | 0.306 |
| 2.0 | 100 | -0.503 |
| 2.0 | 150 | -0.558 |
| 2.5 | 60 | -0.483 |
| 2.5 | 100 | -0.568 |
| 2.5 | 150 | -0.454 |

## Gate 3

Deployed parameters remain frozen; any change requires a human-reviewed PR.
