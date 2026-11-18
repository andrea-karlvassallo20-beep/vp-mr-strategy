# Functional Limit Theorems for Hawkes Processes — deep-read note

Paper: Ulrich Horst & Wei Xu, "Functional Limit Theorems for Hawkes Processes"
(arXiv:2401.11495v3 [math.PR], v3 stamp 29 Dec 2024, dated 31 Dec 2024).
Triage: score 38, slug x47738d_functional_limit_theorems_for_hawkes_processes
(edge_triage_scores.json). Extract: 61 pages, page-marked, complete.

Read line: Null-time session 19 (deep-read 17). Sections 1-2 (intro, literature,
main results; PDF pp. 1-21) read in full detail; proofs Sections 3-6
(PDF pp. 21-61) skimmed as proof machinery — the paper is theory-only, no
empirical content exists anywhere in it. Read against the ONE question: what
here would kill C1-L2 or C8 faster, or change their kill lines?

## What the paper proves

- The long-run behavior of a Hawkes process is fully determined by the average
  offspring m = ||phi||_L1 AND the dispersion of child events, sigma = Psi_1(inf)
  = integral s phi(s) ds (Abstract, PDF p. 1).
- Subcritical (m < 1): FLLN/FCLT hold, precise form depends on dispersion.
  The classical Bacry et al. FCLT holds iff Psi_1(t)/sqrt(t) -> 0, and their
  condition is NOT sharp: Theorem 2.9 gives FCLTs under weaker moment-type
  conditions with nonstandard fractional Gaussian limits in between
  (Theorem 2.9, PDF pp. 12-13). Subcritical increments are ALWAYS
  asymptotically independent — long-range dependence is impossible in the
  subcritical regime regardless of the kernel tail (Theorem 2.8 commentary,
  PDF p. 12).
- Weakly critical (m = 1, sigma < infinity): functional central limit theorems
  DO NOT hold. The rescaled intensity converges to a CIR process WITHOUT mean
  reversion and the rescaled process to an integrated CIR (Theorem 2.10,
  PDF p. 14; stated Abstract PDF p. 1, discussion PDF pp. 4-5). This is the
  Jaisson-Rosenbaum near-unstable light-tailed regime (contrast stated
  PDF pp. 2, 4). Increment correlations decay like C/T (PDF p. 5).
  Every exponential kernel (and every exponential mixture) has finite sigma,
  so exponential-family criticality is ALWAYS weak criticality.
- Strongly critical (m = 1, sigma = infinity, tail regularly varying):
  FLLN/FCLT DO hold, but the limits are LRD Gaussian processes
  (Theorems 2.14/2.16, PDF pp. 15-16; Remark 2.15, PDF p. 16; Remark 2.17 on
  the highly nonstandard scaling constant, PDF p. 17). This regime requires
  heavy-tailed kernels (Sec. 1.2.4, PDF p. 5) — outside the declared
  exponential family.
- Rate of convergence: Theorem 2.12 bounds the Wasserstein distance between
  the rescaled process and its limit by a function of ||IR(n) - IR*||
  (PDF p. 15); for an exponential kernel IR(n) = R = R* exactly, i.e. the
  rate constant is zero — the best case (Example 2.1, PDF p. 15).

## Grade

NO kill line changed. ONE candidate sharpening queued, PENDING OWNER
RATIFICATION: the near-critical regime-disclosure rule — a branching-ratio
trigger bar fired from n-hat inside its pre-declared near-critical band must
disclose the limit regime of the declared fitted kernel class: exponential
family => sigma always finite => weakly critical => mean-reverting-CIR
asymptotics WITHOUT FLLN/FCLT (Theorem 2.10, PDF p. 14), NOT the
strongly-critical long-memory Gaussian regime, which requires heavy-tailed
kernels the declared family structurally cannot reach (Sec. 1.2.4, PDF p. 5;
Theorems 2.14/2.16, PDF pp. 15-16). Reading language importing
criticality-with-long-memory from outside the declared kernel family is
inadmissible; failure to disclose the regime makes the bar inadmissible.
Harder to pass: the near-critical band gains a mandatory stated-regime
clause the old protocol did not have. Distinct from and tighter than the
queued ACF-shape gate (kernel-shape validity at all n), the
boundary-solution rule (optimizer artifacts at the wall), and the
estimator-at-scale-W item (window discipline).

## Reinforcing evidence, no new items

- Theorem 2.9's sharpness boundary keeps the declared exponential family in
  the classical FCLT regime (Psi_1(t)/sqrt(t) -> 0 trivially), and Example
  2.1's zero rate constant is the formal counterpart: day-block inference
  on exponential fits stands on the paper's own ground. Any widening of the
  kernel family must re-run the regime check before trigger readings carry
  asymptotic language.
- Subcritical increments are always asymptotically independent (Theorem 2.8
  commentary, PDF p. 12): long-memory talk attached to any subcritical-fit
  bar is a category error.

## Laundering directions (both named)

1. INTO the programme: importing the strongly-critical LRD Gaussian limit as
   the "critical market" story smuggles in heavy-tailed-kernel theory the
   declared exponential family cannot reach; the paper's own regime map is
   the barrier.
2. OUT of the programme: reading "no FCLT at weak criticality" as "the
   trigger cannot work near n = 1" applies a long-run asymptotic statement
   about the PROCESS to the finite-window ESTIMATOR distribution the trigger
   actually reads. The two are not the same object; the trigger's admissibility
   conditions are the queued estimator rules, not this theorem.

## Source quality

arXiv v3, math.PR, theory-only, no data anywhere; DFG CRC/TRR 388 Project B02
funding acknowledged (PDF p. 1). Two typos noted: "Strongly critical Hakes
processes" (Sec. 1.2.4 heading, PDF p. 5) and "bee seen" (PDF p. 13).
Published version to be checked before formal citation.

Nothing measured, no kill line moved, nothing armed, nothing trades live.
