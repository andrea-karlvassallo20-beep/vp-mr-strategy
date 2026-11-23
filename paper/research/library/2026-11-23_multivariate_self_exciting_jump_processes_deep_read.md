# Deep-read note — library session 100 ("Multivariate self-exciting jump processes with applications to financial data")

- Session: null-time deep-read session 100 (null-time session 110, log ## 132),
  2026-11-23.
- Authors: Heidar Eyjolfsson, Dag Tjøstheim.
- Title: "Multivariate self-exciting jump processes with applications to
  financial data".
- Venue/id: arXiv:2108.10176v1 [math.PR], 23 Aug 2021 (slug x7a86fb, per
  docs/library/expanded_index.json).
- What it is, one clause: a theory-and-fit paper defining a d-dimensional
  self/cross-exciting point process whose SDE-driven intensity jumps by the
  recorded MAGNITUDE of each event (with the mark law allowed to depend on the
  pre-jump intensity level), proving Foster-Lyapunov/Meyn-Tweedie stability
  conditions, and fitting linear and nonlinear bivariate versions to
  threshold-extracted large daily log-return jumps of the S&P 500 and the
  Nikkei 225.

Read 2026-11-23, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x7a86fb_multivariate_self_exciting_jump_processes_with_app.txt,
~22 pp., page-marked). Next UNREAD triage-rank entry (score 20, tenth of the
score-20 tier, per the ## 131 closing pointer).

## The paper in one paragraph

The class: d counting components N_k whose intensity vector solves
dλ(t) = µ(t,λ(t))dt + B dU(t), where U_k(t) sums the non-negative marks Y of
past events and the kth column of B scales how each component's events
excite each intensity (eqs. 1, 3-4 and Definition 1, PDF pp. 3-4); the
distinguishing feature is that events are marked by size, so a large jump
excites the intensity more than a small one, and the jump-size distribution
ν_k(λ,·) may itself depend on the pre-jump intensity value λ(t−), making the
mark law endogenous to the intensity level (PDF p. 4). The extended generator
is computed (eq. 5, Proposition 1, PDF pp. 4-6) and Theorem 1 gives
geometric ergodicity via a Foster-Lyapunov drift condition Af ≤ C0 − C1f on
a norm-like f, through piecewise-deterministic-process theory and Meyn and
Tweedie (PDF pp. 6-7). The linear model µ = A(λ − λ0) is worked in detail:
stability reduces to the symmetric part of M(λ) = A + BJ(λ), where J(λ)
carries the first mark moments, needing all eigenvalues of M+M^T negative
with sup < 0 and bounded first two mark moments (Lemma 1, Lemma 2,
Assumption 2, Propositions 3-4, PDF pp. 8-11); under intensity-free mark
laws, closed forms for first and second moments and the autocovariance
follow (Propositions 5-7, PDF pp. 11-13). The application takes daily
log-returns of the S&P 500 and Nikkei 225 (Yahoo Finance, 2005-2020, PDF
pp. 13-14), defines a jump as |log-return| above a fixed threshold of 0.025,
records jump size as the absolute log-return, and fits eight bivariate
variants by MLE under the imposed stability constraint, split over
all/positive/negative jumps (Table 1, PDF pp. 14-16): the full linear model
II fits best among the six linear forms, and the nonlinear extension — with
mean-reversion speed depending on the intensity norm D exp(−c‖λ‖²), a
built-in regime change, PDF p. 15 — beats it in all three series (models
VII-VIII, LL −1662 vs −1667 for all jumps, Table 1, PDF p. 16),
interpreting: crisis-time clustering of jumps with faster mean reversion at
high intensity, stronger excitation from the S&P into the Nikkei than
vice versa (b21 > b12), strongest for negative jumps, and jump sizes
growing with intensity for the Nikkei but flattening/decreasing at the
highest S&P intensities (Figures 4-5, PDF pp. 18-19).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The paper's own stability theory is a
   printed proof that stability verdicts are moment-bounded outputs: every
   condition of Theorem 1's linear specialization passes through the matrix
   M(λ) = A + BJ(λ) carrying only the first mark moment, plus boundedness
   of the first two mark moments (Lemma 1, Assumption 2, Proposition 3,
   PDF pp. 8-10) — no geometric-ergodicity statement in this family
   constrains the mark law beyond its first two moments. This is the same
   moment-bounded/law-sensitive split the moment-equivalence disclosure
   (#51, deep-read 93) freezes at the gate: a moment-matched generative
   null or comparator in the marked self-exciting family can be certified
   stable and non-explosive while its mark law is arbitrary. The queued
   item already carries the case; nothing added. No queue change.
2. [interpretation caution] The entire point process is manufactured by
   an analyst threshold: a "jump" is defined as a daily log-return whose
   absolute value exceeds a fixed 0.025, the same threshold for both
   series regardless of their differing volatility (PDF p. 14), and every
   excitation, cross-excitation and lead-lag statement downstream is
   conditional on that event definition. The count of events, the fitted
   branching magnitudes and the sign-split asymmetries (b21 > b12, Table 1,
   PDF pp. 16, 18) are all threshold-artifacts in principle: a different
   threshold manufactures a different process. For C1-L2/C8 the analogue
   is any "compression episode", "OFI burst" or "event" whose definition
   embeds a free constant; the estimator-configuration freeze (deep-read
   63) already binds exactly this knob (threshold and event definition as
   frozen configuration), so the reading discipline is recorded as context,
   nothing queued. No queue change.
3. [interpretation caution] Excitation here carries event MAGNITUDE, not
   counts: U_k(t) sums the marks (eq. 3, PDF p. 4), so a model in this
   family is a different process object from a count-only Hawkes on the
   same event set, and the two are not interchangeable (the paper itself
   notes the intensity is a Hawkes process with exponential kernel and
   stochastic jump sizes, PDF p. 8). Within the self-excitation family,
   "does the intensity see counts or marks" is a model-form knob that
   changes what any branching-ratio-shaped estimate in future L2 work
   MEANS, and it interacts with the sign-split fits (all/pos/neg fitted
   separately, Table 1, PDF p. 16), which let sign-conditioned excitation
   structures appear that a pooled fit would not show. Interpretation
   discipline for any future excitation estimate: the mark-feeding
   convention must be part of the frozen estimator identity, which the
   estimator-configuration freeze and the level-versus-memory
   disambiguation (deep-read 59) already cover. No queue change.
4. [reinforcing, no new item] The mark law's endogeneity to intensity —
   ν_k(λ,·) depending on the pre-jump intensity, motivated and fitted
   as jump sizes growing with intensity and more variable at high
   intensity (Definition 1, PDF p. 4; abstract; Figures 4-5,
   PDF pp. 18-19) — is the regime-dependence class the
   self-excitation regime-window pre-declaration (deep-read 53) and the
   moment-equivalence disclosure (#51) already force into the open: a
   moment-matched null reproduces the first two mark moments but has no
   obligation to reproduce the intensity-dependence of the mark law,
   precisely the law-sensitive output class #51 refuses to certify on a
   moment match. Printed reinforcement, no new item. No queue change.
5. [source-quality note] Theory paper with an in-sample fitting
   demonstration, not an empirical study: arXiv v1 preprint (math.PR,
   zero citations recorded in the index), the application is two daily
   index series (S&P 500, Nikkei 225, Yahoo Finance data, PDF pp. 13-14),
   eight nested model forms compared by in-sample log-likelihood with
   gains of a handful of points between the best and second-best (LL −1662
   vs −1667 for all jumps, Table 1, PDF pp. 15-16), no out-of-sample
   validation, no standard errors, no goodness-of-fit or residual
   diagnostics, a single hand-set threshold, and daily-grain data with
   no limit-order-book content anywhere. The headline empirical
   conclusions (nonlinear fit best; S&P 500 leading; crisis clustering
   with stronger mean reversion) are daily-grain, two-market, in-sample
   likelihood comparisons; per the standing caveat they are ammunition,
   never evidence for any programme claim. Check for a published version
   before formal citation (the companion energy-markets paper is in
   Annals of the Institute of Statistical Mathematics, ref. [12],
   PDF p. 21, but this paper shows no journal stamp). No queue change.

## What this paper would have killed if we had done it wrong

Without the estimator-configuration freeze, the 0.025 threshold would be a
tunable "event definition": the same S&P/Nikkei series at threshold 0.02 or
0.03 yields a different point process, different fitted cross-excitation
and possibly a different lead-lag sign, so an excitation claim in future L2
work could be re-threshed into existence and no journal referee would see
it, because the threshold looks like a data-cleaning constant, not a
parameter. Without the moment-equivalence disclosure, a moment-matched
generative null in the marked self-exciting family would be certified
stable by exactly this paper's theory (the proofs use only the first two
mark moments, PDF pp. 9-10) while its intensity-dependent mark law —
the paper's own headline mechanism — silently diverged from the data's, and
the divergence would live precisely in the law-sensitive outputs no moment
audit touches. Without the level-versus-memory disambiguation and the
regime-window pre-declaration, the nonlinear model's built-in regime change
(mean-reversion speed depending on the intensity norm, PDF p. 15, fitted
strongest for negative Nikkei jumps, PDF p. 18) shows how a "crisis
regime" with different dynamics can be a MODEL-FORM property stated by the
analyst inside a self-exciting model, not a measured market state: an L2
spec could find "regimes" that its own kernel-sign convention had assumed.
Without the library-is-ammunition rule, the "S&P 500 leads the Nikkei 225"
contagion direction (b21 > b12, strongest for negative jumps, PDF pp.
17-18) would sit in C8's macro-synthesis as a licensed cross-market
asymmetry, when it is an in-sample likelihood comparison on two daily
index series under one self-selected threshold — exactly the kind of
impressive-empirical-result claim the one question exists to exclude.

## Standing caveat

The stability theory is asymptotic (geometric ergodicity, Foster-Lyapunov)
and gives no finite-sample guidance; all fit results are in-sample
log-likelihoods on one bivariate pair of daily series with no uncertainty
quantification, so the linear-vs-nonlinear and the lead-lag comparisons
are point estimates; the threshold event-definition is arbitrary and
unvaried; the mark data are absolute values of daily log-returns, so
nothing in the paper touches intraday, limit-order-book, or
laboratory-gate regimes; the paper is an arXiv v1 with no recorded
citations in the library index, and the published version should be
checked before any formal citation.
