# VP-MR-ETF-D1-001 — Volatility-Parity Mean-Reversion Strategy

Deterministic, event-driven daily mean-reversion strategy for liquid US equity
ETFs, targeting NautilusTrader. All decision logic lives in an engine-agnostic,
AST-sandboxed core; the engine adapter is a thin event translator; the
paper-trading stack runs the strategy against real data with persistence,
reporting, and an automated promotion verdict.

```
hypothesis -> gated strategy -> statistical validation -> engine adapter
           -> CI (81 assertions) -> daily scheduled paper session
           -> performance report -> automated PROMOTE/HOLD verdict
```

## Quickstart

```bash
pip install numpy                      # core + fast suites
bash strategy/run_checks.sh           # full verification program (81 assertions)

# real-engine suites (optional, also run in the CI engine job):
pip install nautilus_trader
bash strategy/run_checks.sh

# paper trading (any environment with network):
pip install yfinance
python3 strategy/fetch_data.py --data-dir ./paper/data
python3 strategy/papertrading_runner.py --data-dir ./paper/data --state-dir ./paper/state --report
python3 strategy/session_report.py --data-dir ./paper/data --state-dir ./paper/state --markdown ./paper/performance_report.md
python3 strategy/gate_check.py --data-dir ./paper/data --state-dir ./paper/state --markdown ./paper/gate_verdict.md
```

## Safety gates
- **G1 zero-lookahead:** signals at bar t use data strictly <= t-1; bounded
  trailing buffers only; verified by future-perturbation audit.
- **G2 AST sandbox:** core imports limited to numpy/math/typing/dataclasses/enum
  (+ nautilus_trader in the adapter, allow-listed).
- **G3 parameter freezing:** frozen dataclass params; post-deploy writes raise.
- **G4 order state machine:** explicit states with illegal-transition guard and
  per-instrument duplicate-fire protection.

## Progress

| # | Milestone | Status | Evidence |
|---|---|---|---|
| 1 | Strategy core with G1-G4 gates | done | 26/26 gate suite; SPI 1.000; byte-identical replays |
| 2 | Hypothesis validation | done | OU Sharpe +1.36 vs random-walk control -0.69 |
| 3 | Robustness + cost stress | done | 9-pt grid all positive (mean 1.08); Sharpe ~1.0 at 2x costs |
| 4 | Walk-forward + Monte Carlo | done | OOS Sharpe 0.81 frozen params; 40 seeds, t = 24.1 |
| 5 | Deployment envelope | done | profitable at half-life <= ~69 bars; 2->5 assets Sharpe 1.64 -> 2.50 |
| 6 | NautilusTrader adapter | done | stub suite 9/9; real BacktestEngine suite 7/7 |
| 7 | CI pipeline | done | 2 jobs (fast + engine), all green on every push |
| 8 | Paper-trading runner | done | 12/12: idempotent, persisted, restart-safe |
| 9 | Session reporting | done | 11/11: MTM equity, Sharpe, SPI, open risk |
| 10 | Promotion gate | done | 9/9: PROMOTE/HOLD from run-card criteria |
| 11 | Cross-engine parity | done | 7/7: signals byte-identical runner vs real engine |
| 12 | Scheduled paper sessions | ready | activates on merge (cron 21:30 UTC Mon-Fri) |
| 13 | >= 20 paper sessions on live data | pending | requires merge + calendar time |
| 14 | PROMOTE verdict on live data | pending | automated by gate_check after 20 sessions |

## Files
| File | Purpose |
|---|---|
| `vp_mr_strategy.py` | Core strategy + offline validation harness |
| `nautilus_adapter.py` | NautilusTrader Strategy/config adapter |
| `run_checks.sh` | One-command full verification program |
| `test_gates.py` | 26-assertion gate suite (G1-G4 + modules) |
| `test_adapter_wiring.py` | 9-assertion stubbed-engine wiring suite |
| `test_nautilus_engine.py` | 7-assertion real BacktestEngine suite |
| `test_engine_parity.py` | 7-assertion cross-engine parity suite |
| `test_runner.py` | 12-assertion runner suite (idempotency, restarts, SPI) |
| `test_session_report.py` | 11-assertion report consistency suite |
| `test_gate_check.py` | 9-assertion promotion gate suite |
| `backtest_study.py` | Studies 1-3: hypothesis, robustness, cost stress |
| `walkforward_study.py` | Studies 4-5: walk-forward + Monte Carlo |
| `deployment_study.py` | Study 6: edge threshold + universe scaling |
| `spi_monitor.py` | Live paper-trading SPI auditor |
| `papertrading_runner.py` | Incremental paper-trading runner with state persistence |
| `fetch_data.py` | Daily bar fetcher (yfinance / deterministic synthetic) |
| `session_report.py` | Session performance report (MTM equity, Sharpe, open risk) |
| `gate_check.py` | Forward-test promotion gate (PROMOTE/HOLD verdict) |
| `generate_run_card.py`, `run_card.json` | Generated run card (single source of truth) |
| `../.github/workflows/ci.yml` | CI: fast suites + determinism + run-card consistency + engine job |
| `../.github/workflows/paper-trading.yml` | Scheduled session: fetch -> run -> report -> verdict -> commit |

## Caveats
- Statistical evidence is on deterministic synthetic data; live-data behavior
  (real spreads, halts, regime shifts) is exactly what the scheduled paper
  sessions measure — and what the promotion gate requires before live review.
- Adapter wiring is verified two ways: a stubbed-engine suite in the fast CI
  job, and a real `nautilus_trader` BacktestEngine suite in the dedicated
  `engine` CI job (bars + quote ticks, real matching engine, fill and
  rejection reconciliation into the core order state machine).

## License
MIT — see `LICENSE` in the repository root.
