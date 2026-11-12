# C7-L2 Integration Specification — The Filter and the Trigger

Status: ARCHITECTURE, declared before the Tardis data arrives. No code run.
The C7 record is sealed (verdict: PASS, dataset closed); this document defines
how that sealed edge connects to the L2 layer. New claims introduced here
(C8) are declared untested, with kill lines pre-declared below.

## 1. The doctrine: two layers, two clocks, two assets

- **C7 is the macro trap layer.** It measures, on daily data, whether a
  market is structurally primed: coiled ≥ 20 days, quiet, forgotten (low in
  its yearly range). Its clock is the day. Its verdict is a CONDITIONING
  STATE, not a trade.
- **L2 is the micro trigger layer.** It measures, on the event clock of one
  instrument's book, when the coiled market begins to release. Its clock is
  the trade and the quote. Its verdict is a TIMING.
- **The asset separation (binding):** the L2 book measures its own asset.
  C7 measures the macro trap. The L2 test runs on BTC (or ETH) regardless of
  that instrument's C7 status, and the C7 state of THAT instrument becomes a
  conditioning covariate in the survival model. The book is the asset: an
  altcoin's primed state is never timed by BTC's book. Cross-asset
  interpretation is refused, not proxied.

## 2. How the C7 signal reaches the L2 hazard model

1. **The primed registry (nightly, causal).** At each UTC close, the C7
   scanner emits a dated artifact — one row per panel series: primed flag,
   comp_days, rvol_pct, range_pos, frustration_score where perp data exists.
   Computed strictly from data ≤ close. Persisted, versioned, immutable
   (the registry is an audit trail, not a scratchpad).
2. **The L2 model consumes the registry as time-varying covariates:**
   - `primed_lag1` — the binary C7 flag, lagged one full day (the L2 event
     clock never sees same-day C7 state; causality is enforced by lag, not
     by convention).
   - `comp_days_lag1`, `rvol_pct_lag1`, `range_pos_lag1` — the continuous
     components. The binary flag is the filter; the continuous values are
     the conditioning. A 60-day coil and a 143-day coil are not the same
     macro state, and the model is allowed to know that.
3. **Interaction structure (the C8 claim, declared here, untested):** the
   scientifically decisive term is the INTERACTION — does microstructure
   hazard (OFI, Hawkes, absorption) carry more timing information when the
   macro state is primed than when it is not? The standalone L2 re-test of
   C1 (already specified in `c1_l2_test_spec.md`) answers whether the
   compression clock exists at book resolution at all; C8 answers whether
   the two layers MULTIPLY. Both must be tested separately; neither may
   borrow the other's pass.

## 3. The altcoin problem, answered honestly

If the primed market is an altcoin with no full-depth L2 (the Tardis data
covers one instrument), the L2 trigger is UNAVAILABLE for it. The program
then holds the C7 edge alone — daily resolution, no trigger, no timing —
and says so. The alternatives are refused:

- **BTC's book as a proxy for an altcoin's trigger: refused.** The book is
  the asset; cross-asset flow interpretation is exactly the proxy
  substitution this lab forbids.
- **Free top-of-book data as a partial trigger: refused for claims.**
  bookTicker snapshots cannot separate fills from cancels; any altcoin
  trigger built on them is a flagged descriptive aid at best, never a
  tested claim.
- **Panel extension of full-depth L2:** possible later, only after the
  single-instrument L2 test survives, per the one-instrument-first law.

## 4. C8 — the interaction claim (declared, untested, kill lines armed)

- **CLAIM:** microstructure timing features (OFI absorption, Hawkes
  branching, cancellation imbalance) carry MORE out-of-fold timing
  information when the instrument's macro state is C7-primed than when it
  is not — the layers multiply rather than add.
- **MECHANISM:** the primed macro state is a compressed spring; the order
  book is where the release physically occurs. If the trap theory is
  causal, the book should show the loading (absorption) and the release
  (excitation going critical) with sharper hazard signatures inside primed
  states — because there is something loaded to release.
- **TEST:** the L2 hazard model with and without the primed ×
  microstructure interaction term, on gated Tardis data, purged CV on the
  wall-clock label horizon, hour-of-day strata mandatory.
- **KILL LINES (pre-declared):**
  1. the interaction term's HR CI includes 1.0 — the layers only add (or
     do nothing); the multiplication is dead;
  2. the interaction survives only through the frustration-augmented
     variant on unverifiable-volume instruments — dead per C7's own
     precedent;
  3. the 24h-shift book placebo (already pre-declared in the L2 spec)
     reproduces the interaction — pipeline artifact, dead.
- **STATUS:** blocked-on-data (Tardis), untested.
- **WHAT IT CANNOT TELL YOU:** direction, and economics — passing C8
  demonstrates information, not profit; the convexity framework
  (companion document) is the bridge from information to sizing.

## 5. Execution order when the data arrives

1. Verification gate (book reconstruction, snapshots, 100 timestamps) —
   nothing runs before it passes.
2. C1-at-L2 (the compression clock at book resolution) — already
   specified, kill lines armed.
3. C8 (the interaction) — only if C1-at-L2 survives its own kill lines;
   no layer stacking on a dead base.
4. The convexity sizing framework (companion document) — the decision
   context, pre-registered now so that a pass has somewhere to go besides
   celebration.
