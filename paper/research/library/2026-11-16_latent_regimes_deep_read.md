# Library deep-read, session 3: Hiremath & Hiremath, "Aliens on Earth: Early Detection of Latent Microstructure Regimes in Limit Order Books" (arXiv:2604.20949, Apr 2026)

Read against ONE question: **what here kills C1-L2 (or C8) faster, or
changes a kill line?** Source: the extracted text
(`docs/library/text/xd60110_early_detection_of_latent_microstructure_regimes_i.txt`);
page markers cited inline.

## What the paper establishes

- The structural-flaw thesis (p. 3): the standard early-warning toolkit -
  order flow imbalance, spread widening, volatility spikes - is REACTIVE
  BY CONSTRUCTION: each observable is defined by the stress regime it is
  meant to predict, so a detector built on them fires at tau >= sigma
  with zero or negative lead time. "Not a tuning failure... the logical
  outcome of measuring observables that are defined by the regime you
  are trying to predict."
- A three-regime causal DGP: stable -> latent build-up -> stress, where
  build-up produces persistent but weak drift in LOB features (gradual
  depth erosion, mild spread widening, slightly elevated imbalance)
  BEFORE stress materializes (pp. 6-7). Identifiable up to label
  permutation (Theorem 1) via the monotone temporal drift.
- Two guarantees: positive expected lead time iff the drift-to-noise
  ratio eta > sqrt(2 log(1/delta) / T1) (Proposition 1, p. 9), and a
  closed-form lower bound on P(detection before onset) as a function of
  eta, build-up duration T1 and false-alarm delta (Proposition 2).
- Simulation: mean lead +18.6 +/- 3.2 steps, precision 1.00, coverage
  0.54 - and the conditional breakdown: the 46% MISSED detections
  concentrate in short-build-up, high-noise cells, exactly as the bound
  predicts (p. 2-3).
- Real data: one week of Binance BTC/USDT top-20 depth at 1 Hz, 5
  labelled stress events (spread > 3x rolling 10-min median sustained
  30 s): lead +38 +/- 21 s, precision 1.00, coverage 0.80; depth erosion
  and HMM entropy account for >99% of first triggers; baselines
  (imbalance, volatility, CUSUM, BOCPD, HMM thresholds) show NEGATIVE
  lead times (pp. 2, 26-30). Their honesty: "order-of-magnitude
  indicators and proof-of-concept", n_sigma = 5.
- Two protocol details worth stealing: causal z-scoring (rolling 30-min
  past-only) and intraday seasonality removal - "without it, the depth
  erosion channel produces false triggers at predictable times
  unrelated to latent instability" (p. 28); rolling HMM fit on the
  trailing 24 h only, never the test period (p. 29).

## Findings, graded by whether they change a kill line

**Changed no kill line.** All five C1-L2 lines and C8's eleven stand.
Five sharpenings:

1. **The paper IS the C1-L2 hypothesis, stated as theory** (reading, not
   a change): compression at the L2 clock is the "latent build-up"
   regime - persistent weak drift (depth erosion) below detection
   thresholds, preceding stress. Their Proposition 1 gives the condition
   under which ANY detector can have positive lead time: drift-to-noise
   over build-up duration. This is the theory citation for why C1-L2's
   question is well-posed at all - and for why its answer may honestly
   be "below SNR" rather than "absent".

2. **The missed-detection structure is a reading aid for kill line 1**
   (pre-declared as descriptive, NOT a new test): their 46% misses
   concentrate in short-build-up/high-noise cells. If C1-L2's OOF
   concordance lands near the 0.52 kill, the honest autopsy should
   report the concordance BY compression-duration stratum (descriptive
   conditional breakdown, exactly their Section 6 style) before naming
   the dead mechanism - "the mechanism is not there" and "the mechanism
   is below the SNR bound for short build-ups" are different funerals.
   No new kill line; a pre-named diagnostic for the post-mortem.

3. **OFI is reactive by construction - a narrative constraint on C8**
   (reinforces, does not change): if OFI/imbalance are consequences of
   stress, not precursors, then C8's "extreme OFI absorption" trigger
   must never be narrated as anticipating the move; it is a
   contemporaneous state that the macro-Primed state conditions. C8's
   24h-shift book placebo already guards the timing claim; this is the
   citation that says the burden is real. The paper's own winning
   channels were depth erosion and HMM entropy - the depth family, which
   is exactly C6's neighborhood and a candidate micro-state if C8 ever
   needs a replacement trigger (pre-registered, never substituted
   mid-flight).

4. **The hour-of-day control has an empirical citation now**: their
   seasonality removal is "essential" because depth false-triggers at
   predictable hours - the same reason C1-L2's kill line 4 and the
   harness's mandatory hour-of-day stratification exist. Reinforces;
   no change.

5. **Small-sample honesty is precedented**: 5 events reported with CI
   and a "preliminary, order-of-magnitude" label - the same discipline
   as our dry-run reporting. A citation for the culture, not the code.

## Honest caveats about the paper itself

Simulated DGP is Gaussian and their own assumptions (sparsity,
weak correlation for MAX aggregation) are acknowledged as possibly
unreal in real LOBs; the real-data week is one symbol, 5 events, and
their stress label (spread-only) explicitly misses stealth depth
collapse - the mirror image of our trade-touch labels missing quote
flickers. Both proxy biases are now recorded in one place.

## Grade

Session grade: **no kill line changed; one pre-named post-mortem
diagnostic (concordance by compression-duration stratum, descriptive
only), one narrative constraint pinned with a citation (OFI is
contemporaneous, never anticipatory), one theory citation for the
well-posedness of C1-L2 (drift-to-noise over build-up duration), one
reinforcing citation for the hour-of-day control.**
