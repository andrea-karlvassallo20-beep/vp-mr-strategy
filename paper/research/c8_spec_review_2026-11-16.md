# Independent review of the C8 pre-registration — before it is armed

Reviewer's role: second pair of eyes on a colleague's spec, per the
programme's own discipline (kill lines before measurement; reviews
before arming). The C8 spec (`docs/c8_synthesis_spec.md`) is strong —
seven kill lines, the costume check extended to L2, the "unmeasurable
hypothesis is not a hypothesis" gate, cost survival with the honest
"measurable but not harvestable" category. The findings below are
offered as REQUIRED amendments, not criticism for its own sake.

## Verdict: DO NOT ARM until amendments A1-A5 are recorded.

## A1 (blocking) — the spec's economic premise was falsified while it
was being written

The spec's hypothesis: "the known `y_hold` information in the macro
Primed state is amplified when..." — but C7-30m tested-fail
established that the macro Primed state carries NO information beyond
quietness (Primed − Quiet-Not-Primed = +0.00211, CI includes zero,
16,402 eras). There is no "known information" to amplify. The spec was
drafted in parallel with the C7 verdict and inherits a dead premise.

**Amendment required:** restate the hypothesis as a PURE INTERACTION —
interactions can exist without main effects (a 2x2 cell logic) — and
correct the language. The honest form: "the micro state's effect on
4h rank returns may DIFFER between Primed and quiet-not-Primed assets;
if it does not differ, C8 is dead." This is a weaker, testable claim.

## A2 (blocking) — the 2x2 is incomplete; the estimand is not an
interaction as written

The spec's Δ = E[y|Primed,Micro] − E[y|Primed,¬Micro] is a
WITHIN-Primed contrast, not an interaction. Without the control arm —
E[y|¬Primed,Micro] − E[y|¬Primed,¬Micro] — "interaction" is not
identified: a positive within-Primed contrast could simply be "micro
state predicts returns everywhere," which is a C5/C6 claim wearing
C8's name, and would smuggle the (dead) Primed main effect back in as
the conditioning.

**Amendment required:** the estimand becomes the
difference-of-differences: ΔΔ = Δ(Primed) − Δ(quiet-control), DML-
orthogonalized with the vol factor and market factor as nuisances.
The Micro-within-Control arm is mandatory, not optional.

## A3 (blocking) — the Hawkes n_c threshold needs its own placebo

Branching-ratio estimation on ~30 minutes of arrivals is noisy, and
n_c is notoriously biased upward under discretization. K6's
convergence gate is good but insufficient: a threshold of n_c > 0.8 is
meaningless if the estimator returns >0.8 on noise.

**Amendment required:** pre-declare the estimator exactly (exponential
kernel, Ozaki-recursion MLE per the cheatsheet, µs timestamps) AND a
shuffled-arrival placebo: fit the same estimator to time-shuffled
arrivals per bar; the placebo n_c distribution must be recorded and the
production threshold must exceed the placebo's 95th percentile.
Without this, K1's costume check can pass on estimator bias alone.

## A4 (required) — VPIN's clock must be fixed before the run

The spec says VPIN is computed "per volume bucket where applicable,
aggregated to the 30m bar" — two clocks, ambiguous. VPIN was designed
for volume buckets; computing it on fixed 30m bars changes its
distribution and its decile thresholds. The two-clock ambiguity is
exactly the trap T3 died on.

**Amendment required:** pre-declare ONE clock for VPIN (the original
volume-bucket construction, buckets then attributed to bars by bucket
start time), and record the alternative as a counted configuration in
K3's multiplicity ledger — not as a silent choice.

## A5 (required) — the "market-book common factor" is undefined

K1 conditions on "the vol factor and the market-book factor" — the
vol factor is defined (the six-feature family, one factor); the
market-book factor is not. An undefined nuisance is an unbounded
analyst degree of freedom.

**Amendment required:** define it before the run — e.g., the first
principal component of the cross-sectional micro indicators within
each era — and freeze it in the amendment log.

## What the review endorses without reservation

- The estimand's discipline (DML, orthogonalization, purged folds)
- K2's placebo at p < 0.01, block-bootstrapped
- K3's pre-counted multiplicity ledger
- K4's regime reproduction requirement
- K5's direction humility (0.505 not on trial)
- K6's "an unmeasurable hypothesis is not a hypothesis"
- K7's cost survival and the "measurable but not harvestable" category
- Nothing trained, nothing measured, TEST untouched — confirmed by
  this review's own reading of the spec and the repo state

## Reviewer's one-sentence summary

C8 is the right next claim — the first two-family test, and the
Tesla-day anatomy is its motivating observation — but as written it
条件s on a state this programme just buried; restate it as a pure
difference-of-differences interaction, arm the Hawkes placebo, fix
VPIN's clock, define the market factor, and then it is ready.
