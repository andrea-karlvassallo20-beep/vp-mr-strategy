# Deep-read session 37 — Szymanski and Xu, "Mean-Field Limits for Nearly Unstable Hawkes Processes"

Library deep-read session 37 (null-time session 41, log entry
## 45). Grégoire Szymanski (DMATH, Université du Luxembourg) and
Wei Xu (School of Mathematics and Statistics, Beijing Institute of
Technology), arXiv:2501.11648v1 [math.PR], v1 stamped 20 January
2025, 31 pp. text extract, page-marked. Read 2026-11-19, against
ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/x65dac0_mean_field_limits_for_nearly_unstable_hawkes_proce.txt).
Assigned triage-rank entry (score 30, x65dac0; the entry ahead of
it, xf29859, is claimed in flight and is not consumed here). Next
UNREAD triage-rank entry (score 30, x20bdef, "Exact asymptotic
solutions to nonlinear Hawkes processes: a systematic
classification of the steady-state solutions").

## The paper in one paragraph

Pure probability theory, no data. Two linked constructions. First,
scaling limits for a sequence of d-variate Hawkes processes with
general self-exciting kernels whose L1 norms approach one,
extending Jaisson and Rosenbaum's nearly-unstable construction
φn = an·φ to arbitrary kernel shapes, under an L2-bound and vague
convergence condition on the resolvents (Condition 2.1, PDF
pp. 5-7): every limit is a stochastic Volterra equation of affine
type whose kernel is determined by a single Bernstein function
through the exponent Φ(z) = lim βn⁻¹(1 − Lφn(z)) (Eq. (2.4), PDF
p. 7), and the attainable class is universal, every Bernstein
function realizable by some kernel sequence (Lemma 2.4, PDF
pp. 7-8), with the Jaisson-Rosenbaum light-tailed CIR and
heavy-tailed rough limits recovered as the two named special
cases (PDF pp. 8-9). Second, mean-field propagation of chaos for
n exchangeable Hawkes particles sharing one common intensity,
whose aggregate is itself a univariate Hawkes process (Eqs. (3.1)-
(3.3), PDF pp. 10-11); the particle-level limit splits into three
regimes by the joint scaling ζ = n·βn² of particle count against
the squared inverse distance to criticality: complete
synchronization with particles indistinguishable when ζ → 0,
conditional independence as Poisson particles on a common
time-changed clock when ζ is finite, and complete extinction with
all rescaled particles collapsing to zero when ζ → ∞ (Theorems
3.1-3.2, Remarks 3.3-3.4, PDF pp. 11-13). The proofs run through
C-tightness via Kolmogorov-Chentsov, the martingale representation
of the intensity, a coupling removing finitely many particles, and
an exchangeability lemma for empirical measures (PDF pp. 13-25).

## Findings, graded

NO kill line changed. NO new candidate sharpening. Default grade;
the paper is a clean-theory worked exhibit of rules already
standing and the burden of proof for a sharpening was not met.

1. **[reinforcing, no new item]** The limit map is universal and
   non-injective, the fifth worked exhibit for the near-critical
   regime-disclosure rule (deep-read 17, with the boundary-solution
   rule of deep-read 5). In the limit, the kernel survives only
   through the single Bernstein exponent Φ (Eq. (2.4), PDF p. 7),
   and every Bernstein function, hence every affine stochastic-
   Volterra limit in the Abi Jaber-Larsson-Pulido class, is
   attainable by some kernel sequence (Lemma 2.4(2), PDF p. 8).
   Corollary of the paper's own universality: no macroscopic shape,
   rough, CIR-type or otherwise, can identify the microscopic
   kernel that produced it, because the construction can produce
   any of them from near-critical sequences by design (PDF
   pp. 2-4, 7-9). A fitted near-critical reading is a statement
   about the specification, never a discovery about the venue; the
   queued disclosure rule governs, nothing added, no parameter
   transfers.

2. **[reinforcing, no new item]** Deterministic when stable,
   stochastic only near the boundary. Under the stability
   condition the macroscopic limit is the law-of-large-numbers
   deterministic Volterra intensity of Bacry, Delattre, Hoffmann and
   Muzy (PDF p. 2); macroscopic stochasticity enters exactly
   through the asymptotically violated stability condition, and
   the paper says the near-unstable stochastic limit replaces the
   deterministic Volterra intensity of the stable case (Remark 3.4,
   PDF p. 13). Observed stochastic macro structure inside a fitted
   excitation class is therefore a symptom of assumed
   near-criticality, not an independent finding; same governance,
   no transfers.

3. **[interpretation caution]** The mean-field regimes are a
   joint function of particle count and distance to criticality,
   not of either alone: ζ = n·βn² produces synchronization,
   conditional independence or extinction (Theorems 3.1-3.2, PDF
   pp. 11-12; Remark 3.3, PDF pp. 12-13). Two implementations
   with the same fitted kernel but different component counts land
   in different aggregate regimes, so in a multi-component
   excitation system cross-sectional dispersion is a regime
   property, not a free-standing quantity: it collapses under
   synchronization and reappears under conditional independence,
   with nothing in the fitted branching ratio alone deciding which.
   Binds as a reading caution on any hypothetical future
   multi-component (cross-sectional or multi-level) excitation fit
   or any cross-sectional dispersion reading built from coupled
   components. C8's proposed market-book first-PC factor is an
   aggregation of observed features, not a fitted excitation
   system, so nothing in C8 moves and no declaration is queued; the
   near-critical disclosure rule already governs, were such a fit
   ever pre-registered.

4. **[source-quality note]** Pure mathematics (math.PR) with no
   finance section beyond motivation, no data, no calibration, no
   out-of-sample component of any kind; two authors, with
   Szymanski the co-author of the two-square-root-laws market-
   impact paper in the record's cost-survival line (cited here as
   reference [20], Durin, Rosenbaum and Szymanski 2023, PDF
   p. 26) and of the heavy-tailed Hawkes convergence work cited as
   reference [34]; arXiv v1 stamped 20 January 2025, no journal
   record checked at reading; the extract is complete, page-marked
   and ends cleanly at the Appendix B regularity lemmas (PDF
   p. 31), with symbol-level degradation in formula regions only,
   statements anchored to prose. A later version is to be checked
   before any formal citation.

## What this paper would have killed if we had done it wrong

If the universality theorem had been read forward as "any market's
rough or affine macro structure is microstructure-founded by
nearly unstable order flow", a construction result would have been
laundered into a market-truth claim: universality says the limit
class is wide enough to be consistent with anything, which is the
opposite of identification. If the deterministic-when-stable
contrast had been ignored, macro-level stochasticity in a fitted
excitation class would have been booked as an independent
discovery rather than an artifact of the near-critical scaling
assumption. If the three-regime split had been read as a property
of the fitted kernel alone, a cross-sectional dispersion reading
could have been booked stable under one component count and
silently wrong under another. Library-is-ammunition, the
near-critical regime-disclosure rule and nothing-measured
prevented all three.

## Standing caveat

No market, no sample, no period, no costs. The model class is
linear Hawkes with nonnegative kernels whose stability is violated
only asymptotically; the mean-field topology is an all-to-all unit
coupling, a neuroscience-style idealization with no venue analog,
and the extinction regime is an artifact of the rescaling, not a
market process. Laundering directions named. INTO — nothing: no
Bernstein triplet, kernel sequence, regime constant ζ, tightness
argument or regularity exponent enters any spec, default,
calibration, tolerance or generative null, and the model may not
serve as a null or simulator for any C1-L2 or C8 arm without an
owner-ratified pre-declared derivation of its assumptions on the
programme's venue and fields. OUT — the paper is never read
backwards as "markets are nearly unstable" (assumed, not found),
"cross-sectional flow synchronizes" (a regime of an all-to-all toy
model, not a property of any venue), or "macro shape identifies
the kernel" (non-injective by the paper's own Lemma 2.4).
