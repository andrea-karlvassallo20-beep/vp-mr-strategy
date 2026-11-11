# VP-MR-ETF-D1-001 dashboard

Volatility-parity mean reversion on US equity ETFs, paper-trading autonomously since 2026-11-11.

| Metric | Value |
|---|---|
| Sessions (forward) | 2 / 20 |
| Gate verdict | **HOLD** |
| SPI | 1.0 |
| Sharpe (MTM, net of costs) | 0.044 |
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

## Work log

— VP-MR-ETF-D1-001

- **2026-11-11 — Strategy core built and gated.** Volatility-parity mean-reversion strategy (z-score entry/exit, vol-parity x 0.25 Kelly sizing, 3x ATR trailing stop, daily-DD kill-switch). Four safety gates enforced in code: zero-lookahead, AST sandbox, parameter freezing, order state machine. 26-assertion gate suite; SPI 1.000; deterministic replays. (PR #1)
- **2026-11-11 — Statistical validation.** Six studies on deterministic synthetic data: hypothesis test (OU Sharpe +1.36 vs random-walk -0.69), 9-point robustness grid (all positive), cost stress (survives 2x frictions), walk-forward (OOS 0.81 on frozen params), 40-seed Monte Carlo (t = 24.1), deployment envelope (profitable at mean-reversion half-life <= ~69 bars). (PR #1)
- **2026-11-11 — NautilusTrader adapter.** Stub wiring suite 9/9, then real-engine verification: installed nautilus_trader, ran the adapter through a genuine BacktestEngine (bars + quote ticks, real matching engine). Six API incompatibilities found and fixed. Real-engine suite 7/7. (PR #1)
- **2026-11-11 — Paper-trading stack.** Incremental CSV runner with JSON state persistence (idempotent, restart-safe), yfinance/synthetic fetcher, session performance reports (MTM equity, Sharpe, open risk), promotion gate emitting PROMOTE/HOLD from the run card's acceptance criteria. Runner 12/12, report 11/11, gate 9/9. (PR #1)
- **2026-11-11 — CI + scheduled autonomy.** CI runs all suites plus determinism and run-card consistency; scheduled workflow runs the paper session after each US close (21:30 UTC Mon-Fri) and commits state + reports. (PR #1, merged 15:36 UTC)
- **2026-11-11 — First real-market session.** 502 real bars x 5 ETFs, 2,510 decisions, SPI 1.000, zero duplicate fires, zero kill-switch trips, 78 fills through the full order state machine. MTM +0.43% net of costs. (committed to main by the workflow)
- **2026-11-11 — Live-data hardening.** Kill-switch was being reset per-instrument mid-session (fixed: once per session). Session-close flatten orders were submitted but never filled (fixed: paper-filled at last close). Fetcher hardened for cloud-IP throttling: retries with backoff, loud empty-frame failures, MultiIndex schema handling. (PRs #2, #3, merged)
- **2026-11-11 — False PROMOTE caught and fixed.** The first real session exposed the gate counting 502 historical backfill bars as 502 "sessions", declaring PROMOTE on day one. Fixed with an invocation counter (a backfill is ONE session); legacy fallback made conservative; stale verdict regenerated to an honest HOLD 1/20. Workflow concurrency race also fixed. (PR #4, merged; PR #5, merged)
- **2026-11-11 — Session monitor.** One-command forward-test status from committed artifacts. (PR #5, merged)
- **2026-11-11 — Edge-seeker research trainer.** Nightly walk-forward over real fetched data: candidate grid, selection on first 60%, OOS scoring on untouched last 40% (warm-up methodology bug found on real data and fixed). First real recommendation: PROPOSE_REDEPLOY (z=1.5/lb=60, OOS Sharpe -0.52 vs production -1.16 in the current adverse regime). Strictly Gate 3-safe: deployed params stay frozen; proposals require human-reviewed redeployment. 10/10 suite. (PR #6)
- **2026-11-11 — Knowledge base incorporated.** Studied the uploaded KNOWLEDGE.md (13 books: Elliott Wave base, VSA, five microstructure layers, quant history, Bjork, Javaheri, Levy). Implemented the knowledge-grounded candidates: EWMA (lambda=0.97) and GARCH(1,1) (persistence 0.95) sizing-vol models plus the VSA weak-volume entry filter, as research variants in the edge-seeker's 54-candidate nightly grid. First honest evaluation on real data: variants did not beat the selected candidate — documented in KNOWLEDGE_APPLIED.md. 13-assertion variant suite.
- **2026-11-11 — Champion/challenger self-learning loop.** The edge-seeker's winning candidate now runs as a CHALLENGER in shadow paper-trading on the same real bars every night (own persisted state), while the deployed CHAMPION stays frozen so its 20-session forward test stays honest. Nightly race report compares live paper equity, Sharpe, and drawdown; a challenger beating the champion by the margin triggers PROPOSE_REDEPLOY with full evidence — applied only via human-reviewed PR (Gate 3). First real-data race: KEEP_CHAMPION. Salient shows the race. 12-assertion suite.
- **2026-11-11 — Dashboard.** Self-contained HTML dashboard: metric cards, inline-SVG equity curve, verification matrix, edge-seeker recommendation, and this work log. Regenerated by every nightly session. 7/7 suite. (PR #6)
- **2026-11-11 — Session journal.** Append-only per-date history of every paper session (sessions count, verdict, SPI, Sharpe, max DD, race verdict, equity), idempotent per date. 10-assertion suite. (PR #15, merged)
- **2026-11-11 — Incident alerts.** The system files its own anomaly reports as GitHub issues: kill-switch trips, SPI below 0.98, duplicate fires, or a pending redeploy proposal each open a labeled issue, idempotent by title. 9-assertion suite. (PR #16, merged)
- **2026-11-11 — Auto-redeploy proposal.** When the challenger clears the promotion margin, propose_redeploy.py patches the core parameters, regenerates the frozen run card, and opens a PR with full evidence — the human merge IS the review (Gate 3). Applied only from the nightly race report. 13-assertion suite. (PR #14, merged after a full union re-integration with journal+alerts)
- **2026-11-11 — Salient goes live.** GitHub Pages enabled; deploy workflow publishes docs/index.html on every push and after every nightly session. A trigger-path gap (workflow-only changes did not fire deploys) and a token limitation (GITHUB_TOKEN cannot create the Pages site first time) were both diagnosed and fixed. (PRs #17, #18, #19, #20)
- **2026-11-11 — Salient redesign.** Full site rebuild: sticky nav with eight anchored sections, structured knowledge base (13 concept-to-design mappings plus the 14-book studied library parsed live from KNOWLEDGE.md), latest reports as collapsible sections, the full build log as a timeline, a repository map, and upgraded charts (gradient fills, gridlines with value labels, date axes, entry tooltips, race legend with returns). 15-assertion dashboard suite. (PR #20, merged)
- **2026-11-11 — Cross-asset edge research.** Extended research universe beyond the deployed ETFs: crypto (BTC, ETH), main indices (S&P 500, Nasdaq, Dow), commodities (gold, crude, silver). Per series: OU half-life, Dickey-Fuller-style mean-reversion t-test (fixes a real finite-sample AR(1) bias the synthetic tests caught — random walks show spurious half-lives), and a causal z-score backtest vs buy-and-hold. First real findings: crude oil is the standout mean-reverter (half-life ~54 bars, MR Sharpe +0.35 vs B&H +0.03); crypto and gold honestly negative. Nightly workflow, CI and Salient section wired. 15-assertion suite. (PR #21, merged)
- **2026-11-11 — Framing made explicit.** The project is a hobby research pursuit: it will never trade live, and the enjoyment comes from solving and finding the edge, not financial gain. The site carries no personal name in its visible content — only Salient.
