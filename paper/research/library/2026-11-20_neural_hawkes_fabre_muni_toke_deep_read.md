# Deep-read session 63 — Fabre & Muni Toke, "Neural Hawkes: Non-Parametric Estimation in High Dimension and Causality Analysis in Cryptocurrency Markets"

**Authors:** Timothée Fabre (CentraleSupélec / SUN ZU Lab), Ioane Muni Toke
(CentraleSupélec). **Venue/arXiv id:** arXiv:2401.09361v3 [q-fin.TR], 4 Nov 2024
(paper dated November 5, 2024). A methods paper: it solves the Bacry-Muzy
second-order characterization equation for marked multivariate Hawkes kernels
with a physics-informed neural network instead of Wiener-Hopf quadrature
inversion, validates the estimator on six simulated kernel families, and
applies it to one month of Coinbase trades (volume marks on BTC-USD; a
15-pair spillover/causality analysis).

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xc1a00b_neural_hawkes_non_parametric_estimation_in_high_di.txt,
~37 pp., page-marked). Next UNREAD triage-rank entry (score 26).

## The paper in one paragraph

The paper proposes the "moment-based neural Hawkes" estimator: first- and
second-order statistics Λ and G are computed on the event data on a declared
grid (Eq. 8, PDF pp. 4-5; grid rule Eq. 28, PDF pp. 8-9), and the kernel
matrix is recovered by training D separate DGM networks to drive the
characterization-equation residual (Eqs. 19-20, PDF p. 6) to zero, with
causality-respecting temporal loss weights (Eqs. 21-24, PDF pp. 6-7), a
randomized short-time-weighted sampling scheme (S = 0.3, PDF p. 7), a generic
hyperparameter configuration (Table 1, PDF p. 10) and a magnitude-balancing
loss weighting ζ for kernels of different orders (Eqs. 29-30, PDF p. 9). On
simulated data the method recovers exponential, power-law, delayed,
inhibitory, high-dimensional bimodal Gaussian and non-multiplicative kernels
(PDF pp. 10-17) with convergence ∼ N^-0.5 (Figure 8, PDF p. 18) and robustness
to its own hyperparameters (PDF pp. 18-19); against Wiener-Hopf it is far
more stable to statistics-grid choice, while WH oscillations grow worse with
finer grids (Figures 11-14, PDF pp. 19-21). Applications: on Coinbase trades
(Dec 2023, 15 pairs, Table 8, PDF p. 22) the volume mark kernel is concave
non-decreasing with a plateau above ~50,000 USD and volume-dependent latency
peaks (PDF p. 23); the 15-dimensional fit yields branching ratio R = 0.80, a
near-critical t^-1 diagonal power law above 3 ms, an inhibitory valley
between 500 µs and 3 ms (PDF p. 24), and leader/receiver spillover ratios
(Eqs. 50-52, PDF pp. 24-25) in which BTC and ETH lead, XRP both leads and
receives, XRP→XLM causality is strongest, and participation (volume) does not
rank leadership (PDF pp. 25-26); results are robust — by the authors' own
restricted-window and daily-fit checks — to intraday seasonality (PDF p. 26
and Figures 21-24, PDF pp. 33, 36-37).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [reinforcing, no new item] The estimation target sits on a stationarity
   assumption: the characterization theorem and stationarity of Λ both
   ride on R < 1 (Eqs. 4-5, PDF p. 4), and the authors themselves state that
   applying the method "without accounting for this seasonality could ...
   inflate the branching ratios" (PDF p. 26, citing Filimonov-Sornette and
   Wehrli et al.), which is why their own headline fit (R = 0.80, near the
   t^-1 critical diagonal, PDF p. 24) is presented only alongside a
   restricted-stationary-window refit (R = 0.78) and daily medians. Page-
   cited general-form backing for the queued self-excitation regime-window
   pre-declaration and the standing boundary-solution caution; a
   criticality-flavored reading estimated on a non-stationary stretch
   inherits an upward-biased branching ratio before any market structure
   enters. No queue change.

2. [candidate sharpening, PENDING OWNER RATIFICATION — the
   estimator-configuration freeze]. Any C1-L2/C8-adjacent Hawkes (or other)
   kernel estimation must pre-register, before fitting, its FULL estimator
   configuration — the second-order-statistics grid (the h, nlin, nlog or
   equivalent rule), the truncation horizon T, the sampling scheme, any loss
   or magnitude weightings (the ζ of Eqs. 29-30, PDF p. 9; the causality
   weights of Eqs. 21-24, PDF pp. 6-7), quadrature counts, and the training
   configuration — chosen from a declared generic default, with every
   deviation recorded as a dated amendment BEFORE the data is touched; a
   kernel-dependent claim that survives only under a post-hoc re-configuration
   of these auxiliaries may not enter any spec as support. Mechanism, page-
   cited: the same characterization equation on the same statistics yields
   kernel shapes that swing with the auxiliary choices — the paper's own
   benchmark shows WH "can still generate kernels with oscillatory behaviours
   which could lead to false discoveries in practical cases" under a poorly
   chosen grid (PDF p. 21, Figures 13-14), the neural method exists precisely
   because quadrature inversion is unstable there (PDF pp. 2-5, 18-21), the
   ζ weighting exists because raw magnitudes shadow each other and must be
   analyst-rebalanced (PDF p. 9), and the paper's answer is a FROZEN generic
   configuration (Table 1, PDF p. 10; "no fine tuning was made", PDF p. 24).
   This tightens the named-estimator-identity rule by extending the
   pre-commitment from WHICH estimator to WHICH estimator in WHICH exact
   configuration; harder-to-pass because a future kernel-shaped trigger or
   placebo that only passes under retuned bins, grids or weightings now fails
   by rule instead of surviving as a tuning.

3. [interpretation caution] Everything measured sits downstream of declared
   preprocessing conventions: trades sharing a timestamp are aggregated into
   one event (PDF pp. 21-22), microsecond-precision matching-engine
   timestamps of one centralized exchange, a 15-bin logarithmic volume grid
   (Table 9, PDF p. 23), and a 500 µs linear/log statistics grid (PDF p. 23).
   The extracted structure — latency peaks at ~10 µs, 4-5 ms, ~10 ms, extra
   70 µs / 200 µs peaks for large trades, mark-kernel concavity with the
   plateau above ~50,000 USD (PDF p. 23) — is a function of these
   conventions on this venue and month. No shape or magnitude from here may
   enter any spec; any future comparison against the programme's own Tardis
   feed must first reconcile its aggregation and timing conventions before
   differences are read as market facts. No queue change.

4. [interpretation caution] The leader/receiver/spillover results — BTC/ETH
   lead, XRP both leads and receives, XRP→XLM strongest "causality", volume
   does not rank leadership (PDF pp. 24-26) — are summaries of estimated
   kernel magnitudes under one method's weighting choices (finding 2) and
   one month of one venue; the paper itself flags that grid and fit choices
   move smallest branching ratios by "15% to 20%" (PDF p. 26). The library
   is ammunition, not evidence: none of these directional claims may enter
   the cross-market replication front as established structure; recorded as
   a reading discipline only. No queue change.

5. [source-quality note] arXiv-only preprint (v3), q-fin.TR, no published
   version identified in the extract; the index records zero citations; the
   first author is affiliated with the data provider (SUN ZU Lab, PDF p. 1),
   a disclosure, not a flaw, but the empirical results are single-source by
   construction. The numerical validation is real and substantial (six
   simulated kernel families with ground truth, PDF pp. 10-17), the honest
   best access-value read of the score-26 tier so far; cite theorems and
   benchmark claims with the arXiv-version caution and check the published
   version before formal citation.

## What this paper would have killed if we had done it wrong

Had the programme adopted any moment-based kernel estimator (Wiener-Hopf or
this neural successor) for a C8-adjacent trigger or placebo without freezing
its configuration, the exact features the shuffled-arrival placebo would
adjudicate — latency peaks, multimodality, the inhibitory valley, relative
cross-excitation magnitudes — could have been manufactured or erased
post hoc by quadrature counts, grid rules and loss weightings (PDF pp. 18-
21, 9), so the "placebo" would have passed or failed against an estimator
artifact rather than the market: the named estimator-identity discipline
laundered through its auxiliary-configuration gap, which is what the queued
freeze rule closes. Equally, had the paper's causality layer been read as
evidence, a participation-rate (volume) surrogate for leadership and an
XRP→XLM lead-lag "fact" would have entered the cross-market front with zero
of the programme's own measurements behind them — importing someone else's
single-venue December as if it were a finding about markets, the exact
ammo-as-evidence collapse the standing rule forbids.

## Standing caveat

The training is stochastic and the robustness evidence is the authors' own
single-implementation study (PDF pp. 17-19); second-order statistics are an
INPUT, so any clock, aggregation or seasonality error upstream propagates
straight into the kernel (PDF pp. 8-9); the method inherits the Bacry-Muzy
identifiability framework without extending it (baseline vs endogeneity
disentanglement is not addressed here and is known hard); inhibitory parts
are licensed only while P(λ < 0) stays negligible (PDF p. 5) and the
framework assumes positive kernels at setup (PDF p. 4); no finite-sample
constants exist anywhere — all robustness claims are asymptotic or the
authors' own numerics; and the empirical layer is one venue, one month,
fifteen pairs, with branching ratios admitted to be seasonality-sensitive
(PDF p. 26). arXiv-version caution applies throughout.
