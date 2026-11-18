# Library deep-read session 12 — Horst & Xu, "Functional Limit Theorems
# for Hawkes Processes" (arXiv:2401.11495v3, 2024; Humboldt/BIT; pure
# probability theory, FLLNs/FCLTs for subcritical and critical Hawkes)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x47738d_functional_limit_theorems_for_hawkes_processes.txt`,
~60 pp., page-marked). The next UNREAD triage-rank entry (score 38),
after the pointer correction recorded in the programme log: triage
ranks 1 (MMHP, Fabre & Muni Toke) and 2 (Explainable Patterns in
Crypto Microstructure) were already deep-read as sessions 3 and 4.

## The paper in one paragraph

The authors prove that the long-run behavior of a Hawkes process is
fully determined by TWO quantities: the average number of child
events m = ||phi||_L1 (the branching ratio) and the dispersion of
child events Psi_1(t) = integral of s*phi(s) ds, with sigma :=
Psi_1(infinity) (PDF pp. 1, 9-10). For SUBCRITICAL processes
(m < 1), classical FLLNs and FCLTs hold and the increments are
ALWAYS asymptotically independent — "long-range dependencies can
never be observed in the subcritical case," no matter how
heavy-tailed the kernel (Theorems 2.8-2.9, PDF pp. 11-13). For
CRITICAL processes (m = 1), the behavior BIFURCATES on sigma:
weakly critical processes (sigma < infinity) are NOT asymptotically
stationary — no classical FLLN/FCLT — the rescaled intensity converges
to a CIR process WITHOUT mean reversion that grows to infinity
a.s., and arrival increments have correlations decaying at rate
C/T, i.e., long-range dependence (PDF pp. 4-5, 10-11); strongly
critical processes (sigma = infinity, regularly varying integrated
tail) DO satisfy FLLNs/FCLTs but their limits are Gaussian processes
with long-range dependence (PDF pp. 5-6). Convergence rates are
given via Wasserstein bounds, fully determined by the decay of the
time-scaled integrated resolvent (PDF pp. 5).

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. One candidate sharpening is queued, two reinforcing notes
recorded:

1. **[candidate sharpening, PENDING OWNER RATIFICATION] The
   dispersion register.** The paper's central theorem is that the
   same branching ratio m has DIFFERENT asymptotics depending on
   the child-event dispersion sigma (finite: non-stationary,
   CIR-without-mean-reversion; divergent: stationary-flavored but
   long-range-dependent), and Bacry et al.'s moment condition is
   not sharp (PDF pp. 3-4, Theorem 2.9). Pre-declaration text for
   the trigger layer: every branching-ratio reading near unity
   carries, BESIDE its bootstrap CI, its child-event dispersion
   statistic Psi_1-hat (estimated, with its own CI, and labeled
   finite-vs-divergent under the declared kernel family) — because
   m-hat near 1 is an UNIDENTIFIED object without it: two windows
   with the same m-hat can live in different limit regimes. This is
   the rigorous form of session 4/4b's scale problem and completes
   the per-branch rule structurally: per-branch (session 9) fixes
   WHICH excitation, the dispersion register fixes WHICH kernel
   regime, the CI and boundary-solution rules fix WHICH estimate.
   Harder to pass is the only legal direction, and this one adds a
   required statistic where none existed.

2. **[reinforcing, no new item] Long-range dependence is itself a
   criticality fingerprint.** Subcritical processes never display
   it (Theorem 2.8-2.9); critical ones cannot avoid it (rate C/T
   correlations, PDF p. 5). Corollary for the interpretation
   table: on a gated window, arrival-count subsamples showing
   slowly-decaying cross-correlation are EVIDENCE toward the
   critical regime — an independent, non-parametric cross-check on
   the branching reading that requires no kernel fit at all. It
   goes in the interpretation table, not a kill line: descriptive
   ammunition the trigger's readings can be audited against.

3. **[reinforcing, no new item] The stationary-initialization
   assumption fails at criticality.** Weakly critical processes are
   NOT asymptotically stationary (PDF p. 4) — which is precisely
   the initialization Lee & Seo's tick-Hawkes estimator (and every
   filter-evolution estimator mode) leans on (session 9's intensity
   stationarity condition, eq. 8 there). Session 13's estimator-
   mode rule gains its limit-theoretic citation: the
   filter-evolution-from-declared-init mode is well-posed on
   subcritical windows and UNSTABLE on critical ones, so the
   declared estimator mode and the branching regime must be read
   together — the estimator is not regime-free.

## What this paper would have killed if we had done it wrong

If the trigger layer had fired on "branching CI excludes 1" alone
(taken as a portable, kernel-free reading), this paper is the
counterexample library: m-hat = 0.98 with a light-tailed kernel and
m-hat = 0.98 with a heavy-tailed kernel are different objects with
different limits, different stationarity, and different dependence
— and any downstream test that assumed one regime (stationary
filtering, independence across blocks, a single mean) would have
been silently mis-specified on the other. The dispersion register
in item 1 moves the regime question to the required-statistic
layer, where it is binding. Grade: **no kill line changed; one
candidate sharpening queued (the dispersion register), zero
armed** — the owner's word remains the only trigger.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The paper is pure theory — no finance, no calibration,
no venue; its transfer to the program is structural, not empirical:
the dispersion statistic Psi_1 must itself be ESTIMATED on a finite
window, and its own estimate inherits every finite-sample caution
the branching CI carries (the same boundary-solution pathology can
live in the tail fit — cite the register's CI, never its label).
The nearly-unstable sequences of Jaisson-Rosenbaum (cited within,
and the anchor of sessions 4/4b) are a DIFFERENT limit object than
the fixed-critical limits here — the paper itself stresses the
difference (PDF p. 4) — so the queued rules must not mix the two
regimes when citing. arXiv v3 (math.PR, Dec 2024); check for a
journal version before formal citation.
