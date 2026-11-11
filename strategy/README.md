# VP-MR-ETF-D1-001 — Volatility-Parity Mean-Reversion Strategy

Deterministic, event-driven daily mean-reversion strategy for liquid US equity
ETFs, targeting NautilusTrader. All decision logic lives in an engine-agnostic,
AST-sandboxed core; the engine adapter is a thin event translator.

## Safety gates
- **G1 zero-lookahead:** signals at bar t use data strictly <= t-1; bounded
  trailing deques only; verified by future-perturbation audit.
- **G2 AST sandbox:** imports limited to numpy/math/typing/dataclasses/enum
  (+ nautilus_trader in the adapter, allow-listed).
- **G3 parameter freezing:** frozen dataclass params; post-deploy writes raise.
- **G4 order state machine:** explicit states with illegal-transition guard and
  per-instrument duplicate-fire protection.

## Files
| File | Purpose |
|---|---|
| `vp_mr_strategy.py` | Core strategy + offline validation harness |
| `test_gates.py` | 26-assertion gate suite (G1-G4 + modules) |
| `nautilus_adapter.py` | NautilusTrader Strategy/config adapter |
| `test_adapter_wiring.py` | 9-assertion stubbed-engine wiring suite |
| `backtest_study.py` | Hypothesis validation, robustness grid, cost stress |
| `walkforward_study.py` | Walk-forward + 40-seed Monte Carlo significance |
| `deployment_study.py` | Edge threshold + universe scaling envelope |
| `spi_monitor.py` | Live paper-trading SPI / duplicate-fire auditor |
| `papertrading_runner.py` | Incremental CSV paper-trading runner with state persistence |
| `fetch_data.py` | Daily bar fetcher (yfinance real mode / deterministic synthetic mode) |
| `session_report.py` | Session performance report (MTM equity, Sharpe, SPI, open risk) |
| `test_session_report.py` | 11-assertion report consistency suite |
| `test_runner.py` | 12-assertion runner suite (idempotency, restarts, SPI) |
| `generate_run_card.py` | Emits `run_card.json` from frozen params |
| `run_card.json` | Validated strategy run card (generated) |

## Usage
```
python3 vp_mr_strategy.py        # smoke validation (SPI, determinism)
python3 test_gates.py            # gate suite
python3 test_adapter_wiring.py   # adapter wiring (stubbed engine)
python3 backtest_study.py        # studies 1-3
python3 walkforward_study.py     # studies 4-5
python3 spi_monitor.py           # SPI audit demo
python3 generate_run_card.py     # regenerate run_card.json
```

## Offline evidence summary
- Gate suite 26/26; adapter wiring 9/9; SPI 1.000; byte-identical replays.
- OU hypothesis test: Sharpe +1.36 vs random-walk control -0.69.
- Parameter grid (9 pts): all positive, mean 1.08.
- Cost stress: Sharpe ~1.0 at 2x modeled frictions.
- Walk-forward: OOS Sharpe 0.81 on frozen params (IS 2.38).
- Monte Carlo (40 seeds): OU-vs-RW t = 24.1, P(OU>0) = 100%.
- Deployment envelope: Sharpe > 0 for any mean reversion with half-life
  <= ~69 bars; random-walk floor Sharpe -0.26; 5-asset universe Sharpe 1.02
  (with factor structure); universe scaling 2->5 assets: Sharpe 1.64 -> 2.50
  with max DD still < 2%.

## Caveats
- Statistical evidence is on synthetic data; live-data behavior (real spreads,
  halts, regime shifts) is closed only by the >= 20-day paper-trading gate.
- Adapter wiring was verified against a framework stub; run one smoke test
  against the installed nautilus_trader version before going live.
