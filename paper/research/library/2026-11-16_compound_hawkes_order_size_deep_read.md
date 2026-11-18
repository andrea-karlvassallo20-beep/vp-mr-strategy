# Library deep-read session 17 — Jain, Firoozye, Kochems & Treleaven,
# "Limit Order Book Dynamics and Order Size Modelling Using Compound
# Hawkes Process" (arXiv:2312.08927v5, 2023-24; UCL & JPMorgan; 12D
# compound Hawkes LOB simulator, NASDAQ Level-2 data)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x798515_limit_order_book_dynamics_and_order_size_modelling.txt`,
14 pp., page-marked). Next UNREAD triage-rank entry (score 34; the
sibling of session 16's paper).

## The paper in one paragraph

A 12-dimensional compound Hawkes simulator for the top of the limit
order book: six queues per side ({ask+1, ask0, ask-1, bid+1, bid0,
bid-1}) with spread-preserving state transitions, event intensities
conditioned on time-of-day (a U-shape multiplier), inhibitory
cross-excitation kernels allowed with intensities floored at zero,
order sizes sampled i.i.d. from round-number-spiked distributions
calibrated by maximum likelihood, and non-parametric kernel
estimation (a linear-log spaced grid per Bacry et al.) with parametric
power-law/exponential fits chosen by AIC (PDF pp. 1-7). Empirics:
twelve months of NASDAQ Level-2 for AAPL (average spread 1.7 ticks —
a medium-tick stock), plus large/small/very-small-tick appendices;
validation on simulated data shows ~6% average kernel-norm estimation
error; the simulator reproduces signature plots, long absolute-return
autocorrelations, spread and return distributions, and a concave
market-impact function (PDF pp. 6-8).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand. Four reinforcing
notes recorded, one of which carries a caution for the QUEUED
wash-trading audit:

1. **[reinforcing, no new item] Inhibitory cross-excitation kernels
   are fitted, not hypothetical.** Their norm matrix contains
   genuinely NEGATIVE entries — events that suppress other event
   types (in-spread limit orders and opposing-side top cancels
   inhibit each other), with total intensity floored at zero
   (PDF pp. 1-2, 7). This is the cross-branch sign territory of
   the queued sign-register rule and the per-branch rule, now on a
   year of measured NASDAQ data: the excitation structure of a real
   book is NOT component-wise non-negative, the classical stability
   bound (max eigenvalue of the norm matrix < 1) is being applied to
   a matrix that violates the textbook sign assumptions, and the
   authors themselves flag occasional violations handled by a
   heuristic rescaling. Interpretation language for the trigger
   layer: a fitted branching/norm matrix on the gated BTCUSDT
   windows should be READ with its signs, and any stability bound
   applied to it must state which sign regime it assumes — the
   per-branch and sign-register rules already require the signs;
   this is the venue demonstration that the signs are present in
   quantity.

2. **[reinforcing, extends a queued audit's toolkit] The
   round-number caution for the wash-trading statistics.** Their
   stylized facts: over 40% of market orders and 60% of limit
   orders come at size 100; outright cancels are 99.3% of all
   cancels (PDF p. 1). Ordinary, non-manipulated flow is ALREADY
   massively round-number-clustered. The queued wash-trading
   audit (sessions 5-6) uses round-size clustering and
   unrounded-fraction statistics as wash signatures against
   Aloosh-Li's ground truth — that ground truth compares wash to
   non-wash traders, so the DISCRIMINATING object is the deviation
   from the ordinary-flow round-number profile, not the presence of
   round-number spikes. Recorded as an explicit caution so the
   audit, when it runs on gated windows, is calibrated against the
   window's OWN ordinary-flow baseline rather than an implicit
   smooth-size ideal that no book satisfies.

3. **[reinforcing, no new item] Power-law kernels selected 100% of
   the time (AIC) over exponential**, on twelve months of data, with
   kernel shapes stable across days (PDF pp. 6-7). Independent
   venue support for the kernel-caution recorded at session 9 and
   the dispersion register's motivation: exponential kernels
   smooth genuine long-memory, and kernel form is a first-class
   specification choice, not a convenience.

4. **[reinforcing, no new item] The exogenous-intensity cut-off
   bias, handled explicitly.** Non-parametric estimation with a
   finite cut-off "massively overestimates" the exogenous base
   intensity; the authors back it out from the average event
   intensity via (I - Ĝ) Λ̂ instead (PDF p. 6, citing
   Kirchner-Bercher). This is the estimator-hygiene face of the
   drift-reporting item: the base rate's estimate depends on the
   cut-off, and an uncorrected cut-off inflates the very mu the
   drift-reporting rule tracks. One more reason the state of the
   baseline rate is reported beside any branching reading.

## What this paper would have killed if we had done it wrong

If the wash-trading audit had run its round-number statistic
against a smooth-size ideal — the naive reading of "round-number
clustering indicates manipulation" — then EVERY ordinary book
would have flagged (60% of limit orders at size 100 is normal
behavior, not wash). The audit's discriminating power lives in the
deviation from the ordinary round-number profile, and item 2
records that before any window is gated. Similarly, had a stability
bound been quoted for a signed norm matrix without stating its sign
regime, the bound would have beendecorative rather than a
constraint. Grade: **no kill line changed; no candidate sharpening;
four reinforcing notes (one extending the queued wash audit's
toolkit with its baseline caution); the ratification queue stands
at FOURTEEN candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The simulator is engineering, not evidence: kernels are
zeroed at a 0.01 norm threshold for parsimony, stability-violating
fits are capped by a heuristic rescaling, order sizes are i.i.d.
marks (the authors note "lack of support" for size-dependent
intensities on THEIR data — a venue-specific finding, not a
license), and the venue is US equities Level-2, one tick regime
family. The AIC kernel selection is in-sample, not out-of-sample.
arXiv v5 (Aug 2024); check for a published version before formal
citation.
