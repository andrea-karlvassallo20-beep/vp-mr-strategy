# VP-MR-ETF-D1-001 dashboard

Volatility-parity mean reversion on US equity ETFs, paper-trading autonomously since 2026-11-11.

| Metric | Value |
|---|---|
| Sessions (forward) | 1 / 20 |
| Gate verdict | **HOLD** |
| SPI | 1.0 |
| Sharpe (MTM, net of costs) | 0.066 |
| Max drawdown | 3.811% |
| Fills | 78 (156 orders) |
| Edge-seeker recommendation | PROPOSE_REDEPLOY |
| Open positions | flat |

## Verification program (all green in CI)

| Suite | Assertions |
|---|---|
| Gate suite (G1-G4) | 26 |
| Adapter wiring (stub) | 9 |
| Runner suite | 16 |
| Session report suite | 11 |
| Promotion gate suite | 11 |
| Fetcher hardening | 9 |
| Edge-seeker suite | 10 |
| Dashboard suite | 8 |
| Real NautilusTrader engine | 7 |
| Cross-engine parity | 7 |
