# Order-Flow / Liquidity Research Program — Falsification First

Status: PROGRAM DECLARATION, updated after C1 (see `c1_hazard_report.md` and
`l2_data_acquisition_spec.md`). The daily-resolution program is CLOSED.

CLOSURE RECORD (2026-11): C1 tested-fail on BTC and ETH daily, both specs, all
substantive kill lines fired (vol-tautology 4/4, block-temporal placebo 4/4,
scale-invariance whole-layer null 4/4). The daily hazard layer is demoted to a
descriptive volatility clock; a vol clock at RR ~1.4 is not a timing edge.
C2 is DEAD BY DEPENDENCY, not by its own test: it was conditioned on C1 being
alive, and it is an increment over a base hazard that failed the vol-tautology
test on data with the same vol clustering. Recorded as dead-by-dependency;
never tested. C3/C4 were never run (they condition on the same dead base) and
are closed with the daily program. C5/C6 remain blocked and unproxied. No
further daily-resolution tests. If the demoted vol clock is ever cited as a
descriptive finding, cite the STRATIFIED version (the pooled lrvol HR 0.68
violates PH and averages two different clocks), with the PH violation stated.

Methodological note carried forward to the L2 phase: the day-spell design does
not carry forward. The L2-phase hazard must be on event clock (state-change
rows), not daily rows, or the microstructure signal will be smoothed into the
same artifact. First L2 test when data arrives and passes verification: C1
re-run at L2 resolution — does the compression effect exist when the state is
measured from the book rather than from daily bars? That decides whether the
daily null was a resolution artifact or a real absence.

Epistemic rule: no claim is "proven". Every claim is a conditional probability with
a sample size and a kill line declared before testing.

---

## (a) Data actually available (verified in this repo, not assumed)

| Dataset | Resolution | Span | Genuine / synthetic | Order-flow content |
|---|---|---|---|---|
| 5 US ETFs (SPY, QQQ, IWM, XLE, XLF) | Daily OHLCV | 2021-11 → present | Genuine consolidated volume | None |
| ~156 crypto pairs (TradingView-contracted symbols, `paper/research/data/*.csv`) | Daily OHLCV | 2021-11-12 → present (~326k rows) | Volume heterogeneous, frequently synthetic, unverifiable per pair | None |
| Engine | NautilusTrader adapter with backtest-live parity for daily-bar signals (`strategy/nautilus_adapter.py`, `test_engine_parity.py`) | — | — | No L2 replay, no queue modeling. hftbacktest not present. |

Known gaps, stated explicitly:

1. **No incremental L2 / depth data of any kind.** No bid/ask, no cancellations,
   no queue, no book snapshots. Layer 0 (book reconstruction) cannot even be
   started, let alone verified.
2. **No trades (time & sales) feed.** Trade-sign-based features (VPIN on
   volume buckets, Hawkes excitation between buy/sell trades, absorption
   asymmetry) are uncomputable.
3. **Daily bars destroy intra-bar sequencing.** A bar-based engine is invalid
   for the stated mechanism; we do not have a valid engine for it.
4. **Crypto volume is synthetic or unreliable on an unknown subset of the 156
   contracted pairs and cannot be audited pair-by-pair from the CSVs alone.**
   All volume-derived features on the panel are flagged proxies.
5. What we DO have that survives scrutiny: a daily-bar hazard framework
   (`smh_hazard.py`), purged walk-forward machinery, DSR/overfit tooling
   (`overfit_stats.py`), and a prior direction study (n=15,386 directional
   episodes) establishing the boundary P(up)=0.505 [0.497, 0.513] from
   price-derived compression features. That boundary is treated as binding:
   **no direction claim will be made from price-derived features.**

Consequence: with current data, only WHEN (hazard) questions are answerable,
only on daily resolution, and only with price-derived (plus flagged volume
proxy) covariates. WHICH WAY and HOW MUCH are blocked, not merely unmodeled.

---

## (b) Claims to be tested (kill lines pre-declared)

### C1 — Hazard, compression duration (Layer 3, testable now)

- **CLAIM:** Conditional on entering a compression state (ATR-scaled range with
  duration >= d), the hazard of a volatility-scaled breakout within the next k
  days is duration-dependent (non-constant hazard), and time-in-state carries
  timing information beyond the baseline rate.
- **MECHANISM:** Duration dependence: liquidity inside the range is progressively
  consumed/resting at the boundaries; as resting orders age, the marginal order
  required to breach the barrier gets smaller, so breach probability per unit
  time rises (or saturates) with time-in-state. This is a liquidity-redistribution
  claim, not a momentum claim.
- **TEST:** Cox proportional hazards with time-varying covariates on daily bars;
  triple-barrier labels with ATR-scaled barriers fixed at decision time; censored
  (no-break) observations retained. Combinatorial purged CV (purge on label
  horizon, embargo after). Statistic: out-of-fold concordance index and
  likelihood-ratio vs. constant-hazard null.
- **KILL LINE:** Out-of-fold concordance <= 0.52, OR the LR test fails to reject
  constant hazard in >= 30% of purged folds, OR the sign-shuffled placebo
  reproduces >= 50% of the effect size. Any one kills the claim.
- **STATUS:** untested
- **WHAT IT CANNOT TELL YOU:** Direction of the breakout (two-sided hazard only);
  anything about intra-day timing; whether the mechanism is liquidity aging or
  mere volatility clustering — daily data cannot separate them.

### C2 — Hazard, volume dry-up conditioning (Layer 3, proxy-flagged)

- **CLAIM:** Within compression states, declining effort-vs-result (accumulated
  volume per unit of realized price change, daily proxy) raises the conditional
  breakout hazard relative to high-effort compression episodes.
- **MECHANISM:** Flow toxicity/duration: when volume produces no price change,
  aggressive flow is being absorbed by resting liquidity; depletion of the
  absorbing side shortens time-to-break.
- **TEST:** Add the daily effort-vs-result ratio as a time-varying covariate to
  the C1 model; compare nested models by out-of-fold partial likelihood.
- **KILL LINE:** Fails to improve out-of-fold partial likelihood in >= 50% of
  folds, OR the placebo with volume series permuted per-pair (preserving price
  path) reproduces the improvement. On synthetic-volume pairs specifically:
  if the effect is present ONLY where volume is likely synthetic, the claim is
  dead on this data and reverts to blocked-on-data.
- **STATUS:** untested
- **WHAT IT CANNOT TELL YOU:** The daily volume proxy cannot measure absorption.
  It measures coarsely aggregated activity vs. displacement. On synthetic-volume
  pairs it may measure nothing at all — flagged as a proxy, and the panel-wide
  version of this claim is not a unifying claim, it is a sub-population claim
  until volume provenance is known per pair.

### C3 — Hazard, spring/upthrust breach-and-recover (Layer 1, price-only, WHEN only)

- **CLAIM:** A deterministic spring (breach of range low by <= s ATR units followed
  by close back inside within m days) raises the hazard of leaving the range
  (either side) relative to matched no-spring compression episodes.
- **MECHANISM:** The breach consumed sell-side liquidity at the boundary; the
  recovery shows the marginal seller failed; remaining path resistance is thinner.
- **TEST:** Deterministic, reproducible rule (parameters fixed in advance: s, m,
  ATR window). Matched-cohort comparison of breakout hazard, spring vs. no-spring,
  purged CV, censored obs retained.
- **KILL LINE:** Hazard ratio confidence interval includes 1.0 in the pooled
  out-of-fold estimate, OR the effect flips sign across folds more often than
  chance. No rescue by re-tuning s or m — re-tuning after failure is a new claim.
- **STATUS:** untested
- **WHAT IT CANNOT TELL YOU:** Direction. A spring raising the hazard of an
  UPWARD break is a direction claim and is forbidden by the 0.505 boundary
  unless it comes from data that study did not use. This claim is strictly
  two-sided (WHEN, not WHICH WAY). It also cannot distinguish Wyckoff narrative
  from simple volatility clustering — the operationalization is the claim, not
  the label.

### C4 — Hazard heterogeneity across structural phase (Layer 1)

- **CLAIM:** Breakout hazard is stratified by the operationalized phase label
  (Hurst-classified impulsive vs. mean-reverting regime, ATR-scaled swing state);
  a single pooled Cox coefficient misdescribes at least one stratum.
- **MECHANISM:** Duration dependence and liquidity provisioning differ by regime:
  in mean-reverting states, range boundaries are defended (lower hazard);
  in impulsive states, boundaries are traversed (higher hazard).
- **TEST:** Test the proportional hazards assumption (Schoenfeld residuals) on
  the C1 model; if violated, refit stratified by phase label; compare
  stratified vs. pooled out-of-fold.
- **KILL LINE:** If PH holds and stratification does not improve out-of-fold
  partial likelihood, the phase label adds nothing to timing and the Layer 1
  output is demoted to descriptive. If PH fails AND stratification also fails
  to stabilize, the phase operationalization itself is dead — do not average
  the failure into a pooled coefficient.
- **STATUS:** untested
- **WHAT IT CANNOT TELL YOU:** The daily phase label cannot supply the
  directional prior with any measurable skill (rule 4 boundary). It can only
  modulate timing. Any use of it as a "directional prior" is blocked until
  non-price data exists.

### C5 — Absorption asymmetry (Layer 2) — BLOCKED

- **CLAIM (untestable now):** While price is flat, an elevated buy-side
  trade-to-trade excitation vs. sell-side (Hawkes diagonal asymmetry) raises
  the hazard of an upward break within the next interval.
- **MECHANISM:** Aggressive buyers are absorbed by a passive seller; absorption
  exhaustion precedes the break in the absorbed-against direction.
- **TEST:** Requires trades feed with signs and timestamps +intrabar mid. None exists here.
- **KILL LINE (pre-declared for when data arrives):** Out-of-fold hazard-ratio
  CI includes 1.0, OR OFI/VPIN correlation > 0.8 collapsing it into one
  measured layer, OR placebo (shuffled trade signs, book preserved) reproduces
  >= 50% of the effect.
- **STATUS:** blocked-on-data
- **WHAT IT CANNOT TELL YOU:** Everything — it cannot be tested, so it tells
  you nothing. It is listed so it is on record as blocked, not as evidence.

### C6 — Depth-OFI timing increment (Layer 2) — BLOCKED

- **CLAIM (untestable now):** Multi-depth OFI adds out-of-fold timing information
  beyond the best price-derived covariates of C1-C4.
- **MECHANISM:** Liquidity redistribution at depth leads the touch.
- **TEST:** Requires incremental L2. None exists here.
- **KILL LINE (pre-declared):** No out-of-fold increment over C1-C4 in purged CV
  on the single clean instrument (BTC or ETH perp) — the claim dies there and
  the panel is never attempted.
- **STATUS:** blocked-on-data
- **WHAT IT CANNOT TELL YOU:** As above; no proxy substitution is permitted.
  Daily "OFI" proxies computed from close-to-close price and volume are
  explicitly refused — they measure neither orders nor flow.

### Direction (WHICH WAY) — pre-declared dead on current data

The prior study's boundary (P(up)=0.505 [0.497, 0.513], n=15,386) is treated as
established: price-derived features carry no measurable direction information
at this resolution. No direction claim will be made from the available data.
HOW MUCH (sizing) is downstream of a direction posterior and is therefore also
blocked. Position sizing without a direction posterior is decoration.

---

## (c) Blocked layer and unblocking data

**Blocked layer: Layer 0 — the entire engine.** Not merely unimplemented:
unimplementable, because the raw feed does not exist in this environment.
Consequently Layers 2 (micro state) and the order-flow half of Layer 1 are
blocked, and the panel question (contracted pairs, synthetic volume) is doubly
blocked — it cannot even be screened (cancellation fraction, depth-within-10bps,
OFI autocorrelation are uncomputable without a book).

**What would unblock it, in order:**

1. One instrument only: BTC or ETH perpetual on a major venue, two datasets:
   (i) full-depth incremental book updates (depth diff stream or ~100ms
   snapshots), and (ii) signed trades (aggTrades or equivalent), 2-4 weeks
   minimum. This unblocks Layer 0 verification (book reconstruction vs.
   snapshots at 20 random timestamps, one-tick tolerance), the data-quality
   screen, and C5/C6.
2. hftbacktest (or an equivalent queue-aware replay) installed in the sandbox,
   or the NautilusTrader adapter extended to event-driven book replay.
3. Only after C5/C6 survive on that one instrument: extend to the panel with
   group-aware purging, and only for pairs that pass the cancellation-fraction
   screen. Pairs excluded by the screen will be listed by name with the
   failing metric — a theory of 12 of 500 pairs will be reported as a theory
   of those 12 pairs.

**What can proceed meanwhile:** C1-C4 on daily bars, hazard-only, with the
purged-CV + placebo + DSR protocol already present in this repo. These are the
only testable claims in the building, and they are WHEN-claims only.
