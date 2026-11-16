# Library deep-read, session 2: Hardiman & Bouchaud (2014), "Branching ratio approximation for the self-exciting Hawkes process"

Read against ONE question: **what here kills C1-L2 (or C8) faster, or
changes a kill line?** Source: the extracted text
(`docs/library/text/x36082b_branching_ratio_approximation_for_the_self_excitin.txt`,
arXiv:1403.5227v3); page markers cited inline.

## What the paper establishes

- The branching ratio n = integral of the Hawkes kernel maps to a
  branching-process interpretation: the fraction of events that are
  endogenous "daughters" of prior events (p. 1). n >= 1 is
  non-stationary; n -> 1 is "critical".
- MLE branching-ratio estimation (n-hat = alpha-hat/beta-hat for the
  exponential kernel) has named pitfalls (p. 2): the estimate is heavily
  kernel-choice dependent, and on imperfect event data the
  log-likelihood surface can have TWO minima - the global one driven by
  spurious sub-millisecond clustering from exchange timestamp BUNDLING,
  the local one fitting the true lower-frequency dynamics.
- Their model-independent estimator needs only the mean and variance of
  the event count in a window W: n-tilde = 1 - sqrt(mu_W / sigma2_W)
  (Eq. 7, p. 3). Poisson statistics (variance = mean) gives n = 0.
- Bias direction: sigma2_W/W under-estimates the autocovariance
  integral for finite W, so Eq. 7 GENERALLY UNDER-ESTIMATES n, becoming
  exact only as W -> infinity (p. 3).
- Window choice is a real trade-off (p. 3-4): W must be much larger
  than the correlation timescale (they use W = 20 x beta^-1) but small
  enough that the sample has enough windows to estimate the variance;
  too-large W has too few observations.
- The scale-sensitivity result (p. 2): with FIXED W, the branching-ratio
  estimate of S&P futures mid-price changes drifts upward over years as
  market latency falls; scaling W down over time (halving every ~18
  months) recovers a CONSTANT estimate near criticality (n ~ 1). A
  fixed-window n is therefore confounded with the market's own speed.

## Findings, graded by whether they change a kill line

**Changed no kill line.** C8's eleven lines (including the Hawkes
boundary-constraint majority and the shuffled-arrival placebo) stand.
Four sharpenings for the C8 amendment, to be ratified by the owner
before arming:

1. **The two estimators have OPPOSITE biases, so the estimator itself
   must be pre-declared.** Our MLE path on 30-minute windows was found
   biased UPWARD (C8 review A3 - hence the placebo); Hardiman-Bouchaud's
   mean-variance estimator is biased DOWNWARD on finite windows. An
   analyst who silently switched estimators could move n_c across the
   0.8 threshold in either direction without touching any parameter.
   Proposal for the amendment: name the estimator (MLE, exponential
   kernel, Ozaki recursion as verified in the cheatsheet), name W, and
   record the mean-variance value as a mandatory cross-check reported
   alongside, with the placebo above whichever is used.

2. **The timestamp-bundling trap is a live hazard in OUR data.** The
   paper's two-minimum pathology comes from events bundled into the
   same millisecond by the exchange feed. Tardis CSVs carry BOTH
   exchange and local timestamps; the C8 event stream must pre-declare
   the clock (exchange timestamp, the event clock audit already prefers
   it) and add a bundling check: the fraction of identical-timestamp
   events in the trigger window is reported, and the placebo is run
   with intra-timestamp jitter preserved. This is the sibling of the
   beta bug: an estimator-level artifact that no parameter choice can
   fix downstream.

3. **W must be pre-declared relative to the kernel timescale, not the
   convenience of the window.** Their guidance W >> beta^-1 (they use
   20x) with enough windows for the variance. For a 30-minute trigger
   window this means beta^-1 must be estimated on calibration data
   BEFORE the threshold is armed, and W fixed thereafter - otherwise W
   is a free knob that tunes n_c.

4. **The drift artifact guards the regime-reproduction kill line.**
   The paper shows fixed-W n drifts as market latency changes. Binance
   fee-tier changes, engine upgrades, and venue outages are latency
   events; a C8 "era shuffle" that fails while the raw n_c series shows
   a drift would be read exactly through this lens: is the reflexivity
   real, or did the clock speed change? The regime-reproduction line
   already exists; this note is the citation that sharpens its reading.

5. **Criticality is the honest prior.** If crypto trade arrivals are
   near-critical with long memory (as equities appear to be), then n_c
   > 0.8 may be the NORM rather than the exceptional state, and the
   threshold's discriminating power is what the placebo must establish
   - reinforcing that the 0.8 line is unarmed until the placebo's 95th
   percentile is known.

## Grade

Session grade: **no kill line changed; three pre-declarations
required before arming C8 (estimator identity + W fixed to the
estimated kernel timescale + the clock/bundling check), one cross-check
mandated (mean-variance n reported beside MLE n), one reinforcing
citation (fixed-window drift -> regime-reproduction reading).** This
note and session 1 (CKS OFI) together give the C8 amendment its
estimator-hygiene section.
