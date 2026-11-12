# C1 at L2 Resolution — Test Specification (DRAFTED, NOT RUN)

Blocked on: Tardis.dev Binance USDT-M BTCUSDT incremental_book_L2 + aggTrade
(2-4 weeks, spanning a regime change), passing the 100-timestamp verification
gate and the cancellation-fraction screen in `l2_data_acquisition_spec.md`.
Nothing below runs until that gate passes. No model, no panel, no daily tests.

The question this test decides: was the daily C1 null a resolution artifact, or a
real absence? If the compression effect exists when the state is measured from
the book, the daily null was an artifact of daily aggregation. If it dies here
too, the absence is real and the compression-as-flow-duration theory is dead
at both resolutions.

---

## Resolution of the four transition problems (pre-declared, binding)

### 1. Labels: economic barriers in wall-clock, covariates on event clock

Two time axes, decoupled on purpose.

- **Survival/label axis: wall-clock.** The claim is about the timing of MAJOR
  moves, which are economic (wall-clock) events, not microstructure events.
  A pure event-count survival axis would let a frozen book fake survival
  (nothing happens, no events, "hazard" undefined) and would let a burst of
  churny updates fake event density. Labels stay in wall-clock.
- **Covariate update grid: event clock.** Covariates are refreshed at
  state-change events (see #3), not on a fixed grid — this is what "event
  clock" means here: the model *learns* at the moments the book changes state,
  and the *duration* variable is measured in book-update counts.
- **Barrier widths: macro-volatility units, with a noise floor.** Barrier =
  k x sigma_H, where sigma_H is the realized volatility of the mid over the
  label horizon H (primary spec: H = 24h, k = 1.0; secondary: H = 72h, k = 2.5),
  estimated from the trailing window at t0. HARD FLOOR: barrier >= 10 x the
  median bid-ask spread over the trailing window. If the floor binds in > 5%
  of spells, the barriers are noise-dominated at that k: report the binding
  rate and STOP that spec rather than testing noise-touching.
- **Microstructure-noise rejection:** a touch counts only if it is a TRADE
  through the barrier level (last trade price beyond the barrier), not a
  quote touch. Quote flicker through a level is microstructure noise; a
  traded print is an economic event. Both are logged; the trade-touch rule is
  the label, the quote-touch rate is a reported diagnostic.

### 2. Purge and embargo: wall-clock on the label horizon, not event counts

- Purge is on the LABEL horizon, and the label horizon is wall-clock (H
  hours). A training spell at t0 with label window [t0, t0+H] is purged if
  that window intersects the test window extended by the embargo. Embargo =
  H after the test window end. This is unchanged from daily C1 because the
  leak channel is the label, and labels are wall-clock.
- The director's concern (10s of gap ≠ 10s of dead session) is real but is a
  FEATURE-sampling concern, not a label concern. It is handled by the
  covariate grid: in dead sessions there are no state-change events, so no
  rows are emitted, so no hazard is estimated from frozen liquidity — the
  event clock self-thins. We do NOT purge or embargo in event counts, because
  overlap is defined by label windows; and we do NOT purge in volume,
  because volume-denominated time imports the very quantity whose
  information content is under test.
- Folds: contiguous wall-clock blocks (6-fold), so activity regimes are
  distributed across folds by calendar, not by activity rank. Sessions with
  unresolvable sequence gaps are dropped entirely and reported by timestamp.

### 3. State definition: compression measured FROM THE BOOK

Operationalized, deterministic, computable at the decision moment:

- **Mid series:** mid of the reconstructed book, sampled at every book event
  that changes the best bid or best ask (BBBA-change events). This is the
  event-clock price series.
- **Compression flag:** trailing realized range of mid over W = 4h of
  wall-clock, expressed in sigma_H units, percentile-ranked against the
  trailing 5-day pool OF THE SAME HOUR-OF-DAY bucket (6 buckets of 4h).
  Hour-of-day benchmarking is mandatory: without it, "compression" just
  labels the Asian session and the effect is diurnal seasonality wearing a
  liquidity costume. Compression = percentile <= 33.
- **Time-in-compression (the duration variable):** counted in BBBA-change
  events since compression began (event clock) AND in wall-clock hours.
  Both are recorded; the primary duration covariate is the event count,
  the wall-clock version is the secondary. If the two disagree about the
  effect, that disagreement is itself a reported result, not a nuisance.
- **L2-native covariates (measured, not yet trusted):** depth within 10bps,
  cancellation fraction, OFI at top-3 levels — recorded from t0 forward but
  NOT in the primary C1-L2 model. The primary model is compression +
  time-in-compression + sigma_H level + hour-of-day strata, the direct
  analogue of daily C1. L2 features enter only at C5/C6, after C1-L2 passes
  or fails on its own terms. No layer stacking on an untested base.
- **Decision rows:** transitions into compression, plus a refresh row every
  1h of wall-clock while the state persists (so long compressions contribute
  time-varying duration information). Rows are irregular; the Cox long format
  (start, stop] intervals in wall-clock hours carries this exactly.

### 4. The scale-invariance null at L2: standardized-mid block bootstrap

The daily null block-bootstrapped r/sigma. The L2 translation:

- Residuals: BBBA-change mid returns standardized by local sigma (the same
  sigma_H field used for barriers — the null must neutralize exactly the
  scaling the test uses).
- Blocks: 1h wall-clock blocks, resampled with replacement, 100 reps. 1h
  blocks preserve intraday/diurnal volatility structure; standardization
  imposes scale invariance; resampling destroys event alignment while
  preserving the marginal and serial structure of volatility.
- Reconstruction: synthetic mid path = sigma_t x bootstrapped residual,
  re-run the ENTIRE pipeline on the synthetic mid (states, barriers,
  trade-touch labels, Cox, CV). The book's own trade prints for label
  purposes are re-derived from the synthetic mid's barrier crossings by the
  trade-touch rule applied to the synthetic path.
- **Companion null (book placebo):** real mid path and real states, but the
  L2-native timelines (depth, cancels, OFI) circularly shifted by a random
  multiple of 24h. This is the L2 analogue of the daily block-temporal
  placebo and preserves diurnal structure exactly. It matters only once L2
  features enter the model (C5/C6); it is pre-declared here so it cannot be
  invented after seeing results.

---

## C1-L2 kill lines (restated, pre-declared before any run)

1. **Concordance floor:** pooled out-of-fold concordance <= 0.52 kills.
2. **Vol-tautology:** if the compression hazard-ratio CI includes 1.0 in a
   model containing only compression and the sigma_H level, compression adds
   nothing beyond the volatility it was built from — killed.
3. **Constant-hazard null, powered folds only:** unrejection of the LR test
   in >= 30% of folds holding >= 50 events kills. Folds under 50 events are
   merged with a neighbor or flagged insufficient-power and excluded from the
   count — non-rejection in an underpowered fold is a power failure, not
   evidence.
4. **Diurnal artifact check (new, L2-specific):** refit with hour-of-day
   strata AND with hour-of-day as a covariate; if the compression effect
   dies under stratification, the effect was session timing, not liquidity.
   Killed.
5. **Scale-invariance whole-layer null:** if the standardized-mid block
   bootstrap reproduces the observed compression gap within its 95% band,
   the L2 compression effect is a volatility-clustering artifact — the same
   death as daily, and the resolution-artifact hypothesis is dead: the
   absence is real at both resolutions.

If C1-L2 passes all five: the bounded conclusion is a WHEN clock measured
from the book, with measured HR, survival gap, and economic effect at the
vertical barrier; no direction is claimed (the 0.505 boundary stands), and
C5/C6 — the order-flow claims — are the next tests, on this same single
instrument, with their own pre-declared kill lines. If C1-L2 fails: name the
dead mechanism, do not pivot, and the compression theory is closed at both
resolutions; the program proceeds directly to C5/C6 (which never depended on
compression) once their kill lines are restated for the verified data.
