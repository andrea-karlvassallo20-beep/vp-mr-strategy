# Salient — an autonomous quantitative trading system

**What this is:** a complete, self-running quantitative trading pipeline — a
mean-reversion strategy for US equity ETFs, wrapped in hard safety gates,
statistically validated, connected to a real execution engine, and currently
**paper-trading itself against live market data every night** — auditing its
own decisions, seeking a better edge, and reporting everything to a dashboard.

**The goal:** find the edge, through evidence, not enthusiasm. This is a
hobby research project — it will never trade live, and the enjoyment comes
from solving, not financial gain. The promotion gate still matters: the
system must complete 20 forward paper-trading sessions with a Signal Parity
Index >= 0.98, zero duplicate order fires, and zero risk-kill-switch trips —
and it judges itself. Beyond the deployed universe, a nightly research pass
studies 188 series — 156 verified crypto spot pairs, 29 commodity futures and
the main indices — hunting for mean-reversion structure, testing every
hypothesis against control groups, dual out-of-sample windows, cost stress and
the Deflated Sharpe Ratio, and reporting the falsifications as prominently as
the findings.

## The strategy in one paragraph
Each trading day, after the US market close, the strategy computes a 100-day
z-score of each ETF's price against its trailing window. When price stretches
2 standard deviations below the rolling mean (and the market is mean-reverting),
it buys; 2 above, it sells. Position size is volatility parity scaled by a
quarter-Kelly haircut, capped at 0.5% equity risk per trade. A 3x-ATR trailing
stop exits losers, a 2% daily drawdown kill-switch halts everything, and all
positions flatten at session close. Parameters are frozen at deployment.

## Backtesting results (the evidence so far)

All studies ran on deterministic synthetic data with known ground truth,
then were re-verified on real fetched bars. Every number below is
reproducible from the committed test suites.

| Study | Result |
|---|---|
| Hypothesis test (does mean reversion pay?) | OU-process Sharpe **+1.36** vs random-walk control **-0.69** — the edge exists exactly when the market mean-reverts |
| Robustness grid (9 parameter points) | all 9 positive — the edge is not a parameter artifact |
| Cost stress (2x frictions) | strategy survives doubled spreads/commissions/impact |
| Walk-forward (train 60% / OOS 40%) | OOS Sharpe **0.81** on frozen parameters — no re-fitting |
| Monte Carlo (40 seeds) | t = **24.1** — the edge is not a lucky seed |
| Deployment envelope | profitable while mean-reversion half-life <= ~69 bars |
| Cross-engine parity | sandboxed runner vs real NautilusTrader engine: signal streams **identical**; z-scores agree to 3.5e-3 (price-quantization tolerance) |
| First real-market session | 2,510 decisions, SPI 1.000, zero duplicate fires, zero kill-switch trips, 78 fills, MTM +0.43% net of costs |
| Champion/challenger race (nightly) | edge-seeker candidates must beat the live champion by 10% out-of-sample on the same real data — first verdict KEEP_CHAMPION |

## The current honest state (updated after the research battery)

The method is the asset; the edge has not been found yet. What the accumulated
studies have established — and killed:

**Falsified, with the evidence committed:** the 3D state-space region
hypothesis (322 pooled events, 17/40 own-scale beats); both single axes as
entry filters; mid-vol regime gating (null when made causal); detector
confirmation as a strategy improvement (−0.12 pooled premium across 174
series — the forward-return tripling is real but unconditional, and the
exit rule never collects it); and the commodity z-score edge (+0.37 pooled
OOS, but it dies at 2x costs and its Deflated Sharpe at 32 trials is 0.38).

**What stands:** deep stretch alone is the one supported entry signal, and
deeper pays with no falling knife; the AVFI spread axis works as a risk
throttle, never an entry timer (AVFI v4 Pine encodes exactly this); mean
reversion needs an anchor — commodities have one, crypto does not (the same
core: +0.37 pooled OOS on commodities vs −0.31 on crypto); and the live
forward test is the only judge with zero selection bias.

**The direction:** depth-first. One lead at a time, through every gate, and
no new universes until a battery-passing edge exists. The ten evidence-
forced lessons live in `strategy/lessons.py` and render on Salient, each tied
to the data that forced it.

## Why it can be trusted (the four safety gates)
| Gate | Guarantee |
|---|---|
| **G1 zero-lookahead** | Signals at bar t use only data <= t-1. Verified by future-perturbation audit: mutating future bars cannot change past decisions. |
| **G2 AST sandbox** | The strategy core imports only numpy/math/typing/dataclasses/enum. No OS, network, or eval — enforced by static analysis in CI. |
| **G3 parameter freezing** | Hyperparameters are immutable after deployment; mid-run re-optimization raises an exception. The edge-seeker may *propose* changes; only a human can apply them. |
| **G4 order state machine** | Every order walks an explicit state graph with illegal-transition guards and duplicate-fire protection. |

## The autonomous loop (runs nightly, 21:30 UTC Mon-Fri)
```
fetch real bars (SPY QQQ IWM XLF XLE)
  -> run the persisted paper session
  -> SPI audit (decision-time signal parity)
  -> performance report (MTM equity, Sharpe, drawdown)
  -> edge-seeker research pass (walk-forward candidate proposals)
  -> promotion gate verdict (PROMOTE / HOLD vs run-card criteria)
  -> cross-asset research (188 series: MR stats, detections, state space)
  -> honesty studies (MR-coin control group, v4 confirmation premium,
     commodity edge battery, stretch-depth, lessons synthesis)
  -> ingest uploaded research PDFs (the alternative knowledge path)
  -> regenerate dashboard + Salient site + work log
  -> commit everything to main
```

## Website
**Salient** — the live site: <https://andrea-karlvassallo20-beep.github.io/vp-mr-strategy/>
(source: `docs/index.html`), served by GitHub Pages,
regenerated after every paper-trading session. It shows the equity curve,
drawdown curve, per-instrument price charts with trade entries, the
champion-vs-challenger race, and the session journal.

## Current status
See **[DASHBOARD.md](DASHBOARD.md)** — the live, GitHub-renderable dashboard.
Raw artifacts accumulate under [`paper/`](paper/); every session commits its
state, reports, and verdict. The engagement work log lives in
[`strategy/WORKLOG.md`](strategy/WORKLOG.md).

## Repository layout
| Path | What it is |
|---|---|
| `strategy/vp_mr_strategy.py` | The gated strategy core |
| `strategy/nautilus_adapter.py` | NautilusTrader engine adapter |
| `strategy/papertrading_runner.py` | Persisted paper-trading runner |
| `strategy/edge_seeker.py` | Nightly research trainer (Gate 3-safe proposals) |
| `strategy/gate_check.py` | Promotion gate (PROMOTE/HOLD verdict) |
| `strategy/spi_monitor.py`, `strategy/session_report.py`, `strategy/monitor.py` | Audit and reporting |
| `strategy/dashboard.py` | Generates `dashboard.html` and `DASHBOARD.md` |
| `strategy/test_*.py` | 10 suites, 113+ assertions, all green in CI |
| `strategy/backtest_study.py` etc. | The six statistical validation studies |
| `paper/` | The live paper-trading journal (state, reports, verdicts) |
| `.github/workflows/` | CI + the nightly session workflow |

## Quickstart
```bash
pip install numpy
bash strategy/run_checks.sh        # full verification program
```

## Honest caveats
- All statistical evidence to date is on deterministic synthetic data plus one
  real-market backfill; the forward paper sessions are the actual test.
- The edge-seeker's proposals are research output — deployment changes are
  human-reviewed PRs, always.
- This is a research system, not investment advice.

## License
MIT
