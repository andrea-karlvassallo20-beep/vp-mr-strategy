# Salient / vp-mr-strategy — A Falsification-First Market Research Programme

**The one-line summary:** a research knowledge base and falsification lab for
one primary question — *out of the whole universe of markets, WHAT has become
structurally primed to make the next significant move?* — with WHEN as the
supporting clock and WHICH WAY explicitly refused by measurement. It is run
under adversarial falsification: every claim is declared with its kill line
before it is tested, and when a claim dies, the dead mechanism is named.
Nothing here will ever trade live; the asset is the method.

**The main premise (v2):** knowing WHAT will move is the primary object of
prediction. If the primed state is correctly identified, the significant move
is actuarially inevitable across the cycle — no death dated, death certain —
and the trade needs no daily probabilities, only the capital to survive the
wait. This is why 99.9999% lose: they trade probabilities in everything
instead of inevitabilities in one thing. The premise is falsifiable as claim
C7 (cross-sectional priming), the program's primary claim; "surety" itself
cannot be claimed — what can be measured is conditional probability
approaching certainty as the horizon lengthens, with the drawdown constraint
that inevitability-without-a-date imposes. The "look at EVERYTHING" directive
is adopted with one binding constraint: the wider the clue-search, the harder
the Deflated Sharpe correction, and every variable admitted to the priming
score must survive the vol-tautology check that killed C1.

**Status: FROZEN in a strict holding pattern.** The daily-resolution program
is closed (its central claim was falsified). The next phase — C1 re-run at L2
resolution on full-depth order-book data — is fully specified, kill lines
pre-declared, and blocked solely on procurement of Tardis full-depth L2 data
that must pass the verification gate. No further model code will be written
until then.

---

## 1. The Salient Market Hypothesis (SMH)

The theoretical framework, named by Andrea, built and measured in public. It
is a direct replacement for Elliott Wave: it keeps what Elliott got right
(impulse/correction alternation, scale self-similarity, crowd footprints),
discards what Elliott got wrong (the fixed 5-3 cage, Fibonacci targets,
unfalsifiability), and adds the dimension Elliott never had: **time**.
State instead of count. Clock instead of prophecy. Calibration instead of
belief.

### The six axioms (the unconditional laws)

1. **Volatility persists, then mean-reverts** — the clock itself.
2. **Tails are heavy** — thresholds live in sigma units, never points.
3. **Autocorrelation has horizon structure** — a directional prior exists
   only inside trend states.
4. **Impact is concave in volume** — a significant event must be confirmed
   by volume (effort vs result).
5. **Events self-excite** — hazard is state-dependent, never constant.
6. **Every edge decays** — every rule carries a forward score and a decay
   watch.

Not on the list, by measurement: the direction of the next impulse at a
chosen time.

### The mechanism

The measurable core of SMH is the **salience gradient**: markets in a
compressed, quiet state have a materially higher conditional probability of a
significant move within a fixed horizon than the climatology. Measured
(design-sample): compression entries read P(significant week within 12
weeks) = 0.639 vs climatology 0.437, disjoint bands; the forecast carries
pre-scored walk-forward Brier skill (0.2374 vs climatology 0.2642); the one
measured long edge (the crash-zone cross: 206 episodes, median +1.69% over 4
weeks, 57.3% positive) replicated on 11 global indexes the design never
touched (+3.07% median, 71.4% positive). Every number carries the design-sample
caveat; the forward calibration record (33 scoreboard rows logged in advance)
is the only judge with zero selection bias.

### The Certainty-Timing-Direction Triangle

A public rule that is certain, timed, AND directional cannot exist: anyone who
sees it trades it, and the event no longer happens as forecast. So the claims
are separated, and no single model may answer two:

- **CERTAINTY** lives at the distribution (the six laws).
- **PROBABILITY** lives at the event (conditional rates by state).
- **HAZARD** lives at the timing (the clock).
- **DIRECTION** is refused by measurement: a study of n=15,386 directional
  episodes found P(up) = 0.505 [0.497, 0.513] from price-derived features — a
  coin flip. This boundary is binding on everything downstream: direction, if
  it ever exists, must come from data that study did not use — order flow,
  book dynamics, cancellations.

---

## 2. The Falsification Record

The programme's discipline is that claims die in public, with the mechanism
named. The record so far:

**C1 (compression duration-dependence on daily data): tested-fail, and the
death is the pivot point of this repository.**

- CLAIM: after a compression state forms, time-in-state carries timing
  information about the breakout (hazard rises as resting boundary liquidity
  ages).
- TEST: Cox proportional hazards with triple-barrier ATR-scaled labels on
  BTC and ETH daily bars (1,826 days each, 2021-11 → 2026-11), purged 6-fold
  CV, block-temporal placebo, and a scale-invariance whole-layer null — all
  kill lines declared before running (`paper/research/orderflow_program.md`).
- RESULT: all substantive kill lines fired, on both instruments, both specs
  (k=1.0/h=28 and k=2.5/h=84):
  1. **Vol-tautology (the decisive death):** after conditioning on the
     realized-volatility level alone, the compression flag's hazard-ratio CI
     included 1.0 in 4/4 cells. Compression was volatility wearing a costume.
  2. **Block-temporal placebo:** a null that preserves volatility clustering
     but destroys state-event alignment reproduced the entire "effect" in
     4/4 cells.
  3. **Scale-invariance null:** a synthetic series with volatility clustering
     but no liquidity mechanism reproduced the observed gap within its 95%
     band in 4/4 cells.
- VERDICT (pre-declared, not post-hoc): the daily hazard layer is falsified
  as a flow-duration theory and demoted to a **descriptive volatility clock**.
  A volatility clock at RR ~1.4 is not a timing edge. The daily-resolution
  program is CLOSED.
- **Why the pivot to L2:** the daily null leaves one live alternative — the
  effect may be a *resolution artifact*: daily aggregation destroys the
  intra-bar sequence of order flow, exactly the mechanism the theory needs.
  The deciding test is C1 re-run at L2 resolution: does the compression
  effect exist when the state is measured from the book rather than from
  daily bars? That is the next experiment, and it is fully specified.

Also dead, recorded honestly: C2 (volume dry-up) — **dead by dependency**,
never tested (it was an increment over the falsified base, on data with the
same vol clustering); C3 (springs) and C4 (phase stratification) — closed
with the daily program, never run; the short mirror (−0.02% median, a coin
flip before costs); the commodity z-score edge (dies at 2× costs, DSR 0.38);
the 3D state-space region hypothesis; detector confirmation as a strategy
improvement.

Blocked, unproxied: C5 (absorption asymmetry) and C6 (depth OFI) — they
require full-depth incremental L2 and signed trades, which do not exist in
this repository yet. No proxy substitution is permitted.

---

## 3. The Architecture

The path from raw data to a hazard claim, each stage gated on the previous:

```
data ingestion                     src/binance_ingest.py
  raw Binance public archives (aggTrades; bookTicker when available) ->
  normalized Parquet. Strict rules: UTC int64 microsecond timestamps
  (exact ms*1000, no float intermediates, coercion failure kills the file),
  binary int8 aggressor_buy flag, bid<=ask, monotone timestamps.

verification gate (runs FIRST on any L2 data)   src/verify_l2_gate.py
  reconstruct the book from sequence-numbered diffs (U/u/pu); a gap
  (pu != last u) is logged to gaps.log and invalidates the book until
  resync — never patched. Compare mid (one tick) and depth within 10bps
  at 100 random timestamps against snapshots. FAILS LOUDLY (exit 1,
  'GATE FAILED') if: sequence gap rate >= 0.01%, or mid agreement < 99%,
  or depth agreement < 99%. Nothing downstream may run until it passes.

event clock                       src/event_clock.py
  state-change rows, not calendar rows: one row per BBBA change (or trade
  state change on the free data). The clock self-thins dead sessions —
  no events, no rows, no hazard estimated from frozen liquidity. Validated
  on 8.8M real BTCUSDT trades: 914k-4.9M rows/day, 10-58x hourly spread.

CPCV + embargo                     src/event_clock.py::purged_cpcv_splits
  purged combinatorial cross-validation with purge on the LABEL horizon
  (wall-clock) and embargo after the test window. Leakage-proven: on 6.8M
  real event-clock rows, zero index intersections and zero label-window
  overlaps across all splits (enforced by assert, not by convention).

Cox hazard model                   src/c1_l2_test.py (harness, awaiting data)
  competing-risks survival with time-varying covariates on the event
  clock; labels are trade-touch triple barriers (quote flicker never
  counts) with a spread-based noise floor; hour-of-day stratification is
  a mandatory control. All kill lines are raising asserts.
```

Supporting machinery, already validated descriptively on real ticks
(`src/features.py`, `src/dry_run.py`): VPIN on trade-count buckets, a
2-dim (buy/sell trade) Hawkes estimator with bounded MLE and optimizer
fallback, top-of-book OFI (Cont-Kukanov-Stoikov at the touch). Honest
capability statement: the free Binance archives contain **no full-depth
L2** — bookTicker is not publicly archived and bookDepth is 5-second
band snapshots, which destroy the update sequence. The free data supports
trade-flow analysis only; every book-based claim (C5/C6) stays blocked
until the Tardis data passes the gate.

---

## 4. The Pre-Declared Kill Lines for the L2 Test

Public and immutable, declared in `paper/research/c1_l2_test_spec.md` and
physically enforced as asserts in `src/c1_l2_test.py`. The test dies if:

1. **Concordance floor:** pooled out-of-fold concordance <= 0.52.
2. **Vol-tautology:** the compression hazard-ratio CI includes 1.0 in a
   model containing only compression and the sigma_H level — compression
   adds nothing beyond the volatility it was built from.
3. **Constant-hazard null, powered folds only:** the LR test fails to
   reject constant hazard in >= 30% of folds holding >= 50 events (folds
   under 50 events are merged or flagged insufficient-power —
   non-rejection in an underpowered fold is a power failure, not evidence).
4. **Diurnal artifact check (L2-specific):** the compression effect dies
   under hour-of-day stratification — it was session timing, not liquidity.
5. **Scale-invariance whole-layer null:** a block bootstrap of
   sigma-standardized mid returns (1h blocks, preserving diurnal structure)
   reproduces the observed compression gap within its 95% band — the same
   death as daily, and the resolution-artifact hypothesis is dead: the
   absence is real at both resolutions.

If all five pass, the bounded conclusion is pre-committed: a WHEN clock
measured from the book, with measured hazard ratio, survival gap, and
economic effect at the vertical barrier — no direction claimed (the 0.505
boundary stands), C5/C6 next on the same single instrument. If any fires,
the dead mechanism is named and no pivot to a nearby surviving claim is
permitted.

---

## 5. The Macro Timeline

`data/macro_timeline.csv` (schema in `docs/data_dictionary.md`; population
checklist in `docs/macro_timeline_checklist.md`) is a hand-curated calendar
of structural events: FOMC decisions, CPI releases, and crypto-specific
events (ETF approvals, halvings, exchange failures, regulatory actions),
each with UTC timestamps, an expected resolution time, and a confidence flag.

Its role is **interpretive and structural, never predictive**: macro events
define the regime context in which hazard estimates are read — event-window
stratification (is the compression clock measuring liquidity aging, or is it
accidentally measuring proximity to a scheduled announcement?), censoring
decisions around known release times, and the honest separation of
"endogenous market structure" from "scheduled information arrival." Two
binding rules: times are UTC only, and the `surprise_note` field is filled
AFTER the event — it is look-ahead by construction and can never be a model
input.

---

## Repository Map

| Path | What it is |
|---|---|
| `paper/research/orderflow_program.md` | The constitution: data inventory, claims ledger, kill lines, blocked-on-data record |
| `paper/research/c1_hazard_report.md` | The C1 experiment and its verdict (FAILED, all kill lines) |
| `paper/research/c1_l2_test_spec.md` | The next experiment, fully specified, not run |
| `paper/research/l2_data_acquisition_spec.md` | Exactly what data must arrive and pass the gate |
| `paper/research/LEARNING_NOTES.md` | Plain-language guide: the book knowledge base and the lab |
| `KNOWLEDGE.md`, `KNOWLEDGE_SMH.md` | The Market Studies knowledge base (13 books studied; the source of the ideas) |
| `src/` | Ingestion, verification gate, event clock, CPCV, feature calculators, C1-L2 harness |
| `tests/` | 27 tests, all green, including failure-path tests (gap, leakage, kill lines) |
| `docs/` | Data dictionary, macro checklist, the thesis presentation |
| `strategy/`, `paper/` | The earlier Salient system: gated strategy core, nightly paper-trading loop, research batteries |

## The Epistemic Contract (why this can be trusted)

1. Never "prove" — every claim is a conditional probability with a
   confidence interval and a sample size.
2. WHEN / WHICH WAY / HOW MUCH are separate questions; no model answers two.
3. Labels are computable at the decision moment from strictly earlier data.
4. Direction never comes from price-derived features (the measured 0.505
   boundary).
5. Kill lines are declared before testing and never moved after.
6. A failed test names the dead mechanism; no pivoting to a nearby survivor.
7. If it cannot be tested with available data, say so and stop — no silent
   proxy substitution.
8. One instrument survives before any panel is attempted.

**Frozen pending data acquisition.** The next commit that touches the model
should be the gate report on real Tardis data.
