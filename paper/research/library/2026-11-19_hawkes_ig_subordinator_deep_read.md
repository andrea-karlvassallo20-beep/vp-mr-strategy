# A Hawkes microfoundation for multitype inverse-Gaussian subordinators — deep-read note

Paper: Yingli Wang (Fudan), Wei Xu (Beijing Institute of Technology), and
Lingjiong Zhu (Florida State), "A Hawkes Microfoundation for Multitype
Inverse Gaussian Subordinators" (arXiv:2610.10525v1 [math.PR], 7 Oct
2026). Triage: score 29, slug xf77014_a_hawkes_microfoundation_for_
multitype_inverse_gau (edge_triage_scores.json), the NEXT unclaimed
UNREAD entry in triage order: the top UNREAD per the ## 59/## 60 tail
pointers, "From Glosten-Milgrom to the whole limit order book"
(x0d8b2a, score 29), is claimed by a live branch (PR #231, drafted as
deep-read 50 / log ## 61), so per the ## 48 racing-slot division this
session consumes the entry behind it. Extract: 35 pp., page-marked,
complete, references included (docs/library/text/xf77014_a_hawkes_
microfoundation_for_multitype_inverse_gau.txt).

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xf77014_a_hawkes_microfoundation_for_multitype_
inverse_gau.txt, ~35 pp., page-marked). Next UNREAD triage-rank entry
(score 29), consumed after the live-claim check above; re-verified
unread against all 49 library notes on main plus the Glosten-Milgrom
claim on PR #231; no other open PR or branch claims the slug.

Operational disclosure: no functional git/gh CLI existed in this
session's execution environment; the repo was read and written through
the authenticated GitHub API only. No main tarball could be assembled,
so the integrity guard could not be run over the full tree locally; the
guard's exact marker-sweep logic was run over this session's changed
files (clean, zero offenders), the library-provenance audit is untouched
by this session (no docs/library/summaries/ file changed), and the
branch CI runs the real guard over the full tree — check-run output
recorded in the log entry. The push was verified by read-back of the
landed blob, per the ## 60 read-side-truncation lesson.

## The paper in one paragraph

The authors prove that a nearly critical multivariate linear Hawkes
system — kernel-mass matrix A_T with spectral radius below one,
normalized defect B_T = (I − A_T)r_T converging to a nonsingular
M-matrix B, baseline balanced so T·r_T·µ_T → η — has its rescaled event
counts and integrated intensities converge jointly, in the product
M1-topology, to a pure-jump Lévy subordinator they call the multitype
inverse-Gaussian subordinator, whose Laplace exponent is fixed by the
coupled quadratic system B^T z + z∘²/2 = u (assumptions (8) and
Theorem 2.2, PDF pp. 6-7; Lemmas 4.1-4.3, PDF pp. 23-25). The mechanism
is a cluster argument: finite-variance near-critical immigration-
branching produces rare families of order r_T^-2 events with depth
order r_T^-1; the balance keeps a non-degenerate population of them;
and finite-mean reproduction delays collapse each family's internal
calendar time into a single macroscopic jump exactly when
T·r_T → ∞ (Lemma 5.1, an iff, PDF p. 27). Diagonal B gives independent
classical IG clocks (PDF p. 7); the square-root specialization reproduces
the Abi Jaber-Attal-Rosenbaum hyper-rough-boundary IG law (PDF pp. 8-9);
subordinating an independent Brownian motion gives a symmetric NIG
process (Corollary 2.7, PDF p. 9). Sections 3 and 6 weaken the
high-intensity assumption of Xu's multivariate scaling theory to an
accumulated-activity condition, upgrade convergence to product M1 for
monotone paths (Theorems 3.2, 3.7; PDF pp. 12, 19), and extend the
scalar limit to finite-variance age-dependent branching, where the
offspring variance σ² rescales the dispersion but leaves the mean
activity rate fixed (Proposition 6.2, PDF pp. 30-32). There is no
empirical work: no data, no estimation, no venue, anywhere.

## Findings, graded (does any kill line move?)

Verdict: NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] — the phase-diagram lesson: the
   branching-ratio exponent alone does not determine the macroscopic
   path type. The paper places the programme's whole near-critical
   reading list in one diagram: with r_T ≍ T^-β, every β ∈ (0,1) is the
   IG calendar-collapse region; the boundary T·r_T → λ recovers the
   persistent-family CIR regime of Jaisson-Rosenbaum; heavy-tailed
   reproduction delays instead retain memory and give rough/Volterra
   limits because family depth survives the observation scale (PDF
   pp. 3-4). What is decided is NOT a_T → 1 but the conjunction of
   criticality speed, immigration balance, and the kernel's temporal
   tail. This reinforces the existing estimator-discipline and
   near-criticality register cautions in the pending state (the
   apparent-criticality family among them) exactly as they stand: a
   fitted branching ratio near one licenses no macro-regime claim
   without kernel-tail diagnostics, and this paper is the cleanest
   statement of WHY. Nothing new is queued; the existing rules cover it.

2. [interpretation caution] — calendar collapse is an
   observation-grain statement, and jump timing at a fixed grain is a
   clock artifact, not a market property. The collapse Lemma 5.1 is an
   iff under the immigration balance (PDF p. 27): families' internal
   timing disappears below the observation scale precisely when
   T·r_T → ∞, and the topology must be M1 because J1 cannot merge a
   staircase of microscopic jumps (each normalized jump r_T² → 0,
   counts simple) into one macroscopic jump (PDF pp. 4, 8, 25). Reading
   discipline for C1-L2: a cascade resolved event-by-event at fine
   grain is the SAME object that appears as an instantaneous activity
   jump at coarse grain; in the M1 limit the compensator and the count
   coincide, so coarse-grain intensity is blind to the intra-avalanche
   structure the paper proves exists. Any future compression-signal
   reading at L2 grain must therefore treat "jump moments" as
   grain-relative descriptions, and any coarse-grain fit cannot
   distinguish a genuine Poisson-type jump from a collapsed cascade
   under J1-style diagnostics. No queue change; a reading mode.

3. [interpretation caution] — a triangular-array theorem is not a
   finite-sample market fact, and the NIG corollary is a clock law,
   never a returns model. Every constant in the limit lives on the
   array index T (assumptions (8), PDF p. 6): the balance
   T·r_T·µ_T → η is a normalization theorems are BUILT on, not a
   condition any finite market satisfies or fails. The paper contains
   zero empirical content. The authors themselves fence the financial
   reading: a process-level return model subordinating Brownian motion
   by this clock "would additionally need signs, imbalance, leverage,
   and a rule for composition at clock jumps" (PDF p. 33). Never read
   backwards as "returns are NIG," "near-critical flow makes macro
   volatility jump-like," or "market time is IG." No queue change.

4. [reinforcing, no new item] — the x^-3/2 Lévy singularity is a
   mechanism output, not a criticality certificate. The limiting
   Lévy density's x^-3/2 near-zero behavior comes from the
   critical-branching Borel family-size asymptotic with exponential
   tempering from the r_T^-2 cutoff (PDF pp. 28, 27), and the
   infinite-activity, finite-variation limit follows (PDF p. 28).
   Proposition 6.2 shows the offspring variance σ² rescales the jump
   dispersion and tail scale while leaving the mean activity rate
   ϑ fixed (PDF pp. 30-32). This reinforces the existing
   apparent-criticality caution in the pending state: heavy
   cascade-size tails at finite sample are what ANY finite-variance
   near-critical branching produces, so observing them licenses no
   claim that the underlying market is at criticality. Nothing new
   added.

5. [source-quality note] — arXiv:2610.10525v1, pure math.PR, 7 Oct
   2026: a proof paper with no data, no estimation, and no market; the
   financial interpretation is one closing paragraph (PDF p. 33) and
   the finance in it is inherited from citations, not measured. The
   square-root specialization matches the Abi Jaber-Attal-Rosenbaum
   hyper-rough boundary law (PDF pp. 3, 8-9): two independent routes to
   the same law is mathematical consistency between theorems, not
   corroboration by markets. v1 preprint; published version and any
   referee-driven changes NOT checked at reading, uncertain until
   verified.

## What this paper would have killed if we had done it wrong

Had the IG-clock law been laundered INTO the record as "market time is
inverse-Gaussian at near-criticality," an asymptotic theorem about a
triangular array the market never is would have become a calibration
assumption for C1-L2's compression clock, and every later
miss would have been blamed on the data instead of the imported
fiction. Had the calendar-collapse iff been read backwards — "jump
timing is real because the theorem says families become jumps" — the
grain-relativity the paper actually proves would have been inverted
into a market property, arming a kill line against the wrong target.
Had the M1-versus-J1 statement been ignored inside a generative-null
or placebo design, a null whose staircases merge only in M1 would have
been certified in J1 (or vice versa), a refutation instrument failing
at exactly the statistics it exists to test — the same instrument-
class defect the ## 57 dynamics-identification rule was queued
against. Had the NIG corollary been exported as a returns model, the
authors' own fence (signs, imbalance, leverage, composition at jumps,
PDF p. 33) would have been laundered away and a clock theorem would
have become return-predictive support for nothing. Had the x^-3/2
singularity been quoted as evidence that markets sit at criticality,
the paper's own mechanism — any finite-variance near-critical
branching produces exactly this tail (PDF pp. 28, 32) — would have
testified against the citation. Library-is-ammunition, the INTO/OUT
laundering rules, and the placebo-precedent family prevented all
five.

Laundering directions named: INTO — nothing; no exponent parameter
(η, ϑ, γ, B, σ²), no x^-3/2 density, no IG/NIG marginal law, no
collapse condition, no topology convention, and no first-passage
representation from this paper enters any spec, default,
calibration, tolerance, clock choice, or generative null. OUT —
never read backwards as "returns are NIG" (clock law, composition
rules absent, PDF p. 33), "near-critical flow implies jump-like
macro clocks in finite data" (triangular-array limit, PDF p. 6),
"branching ratio near one identifies the regime" (phase diagram,
PDF pp. 3-4), "critical families are macroscopic" (a single
unconditioned family vanishes: P(r_T²S_T > ε) ≤ r_T/ε → 0, PDF p. 28),
or "heavy cascade tails certify criticality" (mechanism output,
PDF pp. 28, 32).

## Standing caveat

A pure-probability preprint: every claim is a theorem under
assumptions (8) — subcriticality each T, M-matrix defect limit,
immigration balance, uniformly bounded first delay moment — with no
empirical validation, no venue, no sample, and prices nowhere in the
model; the multitype dependence is cross-EXCITATION structure
inherited by the limit, a statement about family compositions, not
about assets. The genuinely coupled (non-diagonal) result rests on
this paper's own cluster identification and M-matrix uniqueness,
beyond the diagonal-atom scope of the prior scaling theory it
extends (Remarks 3.10-3.11, PDF pp. 21-22). arXiv:2610.10525v1,
indexed 2026; published version and any journal-revision differences
NOT checked at reading, uncertain until verified.
