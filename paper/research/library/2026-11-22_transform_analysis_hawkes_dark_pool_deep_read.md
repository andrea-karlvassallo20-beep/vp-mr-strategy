# Deep-read 93 — Gao, Zhou, Zhu, "Transform Analysis for Hawkes Processes with
# Applications in Dark Pool Trading"

Deep-read session 93 (null-time session 103). Authors: Xuefeng Gao, Xiang Zhou
(Department of Systems Engineering and Engineering Management, The Chinese
University of Hong Kong), Lingjiong Zhu (Department of Mathematics, Florida
State University), 2017, arXiv:1710.01452v1 — a pure-theory derivation of the
joint Laplace transform, moments and distributions of a marked linear Hawkes
process with a general (non-exponential, non-Markovian) exciting function and
a time-dependent baseline intensity, via the immigration-birth representation,
applied to synthetic dark-pool fill metrics.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8 faster,
or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x47bbb5_transform_analysis_for_hawkes_processes_with_appli.txt,
~42 pp., page-marked). Next UNREAD triage-rank entry (score 20, third of the
score-20 tier, after the Guo-Swishchuk-Rémillard multivariate Hawkes LOB option
read of deep-read 91 / ## 120 and the Zamora Font VIX-options Heston-Hawkes
read of deep-read 92 / ## 121).

Session-state note (director step, per docs/goal_autonomy_protocol.md): the
live main tail (through ## 121) and docs/DECISIONS_PENDING.md were read at
session start (ratification line: fifty candidates plus probe E1, zero armed);
the open-PR set was read (empty, no race); the cadence check was recomputed
from first principles — the edition-10 counter stood at FOUR of five after
deep-read 92 (## 121), so no synthesis pass is due yet and the default work
choice for this session is the standing deep-read ritual itself, which needs
no justification under the protocol; this read (#93) moves the counter to
FIVE of five, so the NEXT session must open with the synthesis pass (edition
11) before or instead of its read. Verified against live state before
reading: the triage file score-sorted, the entry x47bbb5 confirmed as the
next UNREAD by title-matching the score-20 tier against the live library note
listing (the two entries ranked above it, xaace1f and x2b0051, both carry
notes dated 2026-11-22 on main's tip; x47bbb5 itself is note-less), and its
extract present and page-marked (87,613 bytes, 42 PDF pages, abstract through
Appendix E complete). This is deep-read 93, the FIFTH read counted against
the edition-10 cadence.

## The paper in one paragraph

The paper studies a marked linear Hawkes process N with cumulative mark
process L, intensity λt = μ(t) + ∫ h(t−s) dLs where the baseline μ(·) is a
general non-negative function of time, h is a general locally bounded exciting
function with ‖h‖L1 < ∞, and the i.i.d. non-negative jump sizes 𝓁n enter the
intensity multiplicatively (PDF pp. 1-2, eq. 1.1) — non-Markovian for general
h. Theorem 1 gives the joint Laplace transform E[e^{−θ1NT−θ2LT}] =
exp(∫₀ᵀ μ(T−s)(F(s)−1) ds) for R(θ1), R(θ2) ≥ 0, where F is the |F| ≤ 1
unique solution of a Hammerstein-type Volterra integral equation (2.2),
proved by the Hawkes-Oakes immigration-birth (Galton-Watson cluster)
representation with uniqueness by a Gronwall argument carrying constant
3‖h‖L∞E[𝓁1] (PDF pp. 6-11); the exponential-kernel case recovers the
Errais-Giesecke-Goldberg affine point-process transforms exactly (Remark 2,
PDF pp. 6-8). Proposition 5 derives first and second moments through renewal
functions ψ1, ψ2, ψ3 (PDF pp. 12-13), Propositions 7-8 the probability mass
functions of NT and of LT (lattice mark case) by Faà di Bruno expansion
(PDF pp. 13-14, appendices A-C, PDF pp. 34-39). The application half models
the executions of a resting midpoint-peg dark order as (N, L) and computes
time-to-first-fill (determined by μ alone, P(τ(1) ≤ t) = 1 − e^{−∫₀ᵗ μ}, PDF
p. 16), time-to-complete-fill and expected fill rate by numerically inverting
the Lt transform (EULER after Abate-Whitt, collocation for the Volterra
equation on a 150-subinterval mesh, FFT via Carr-Madan, PDF pp. 16-23),
conditional fill probabilities and conditional expected fill size given a
past fill (PDF pp. 17-18, appendix D, PDF pp. 39-40), and the non-empty-pool
extension where a zero-time partial fill turns the baseline into the
time-varying μ(t) = μ + |y|h(t) (PDF pp. 26-28), with heavy-tailed initial
liquidity (mass at zero, two-sided Weibull) after the empirical dark-pool
stylized fact of Ganchev et al. (PDF pp. 29-30). All numerics are synthetic
MATLAB experiments; no data, no calibration, anywhere.

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] Theorem 1 is precisely the positive example the
   freshly queued transform-domain admissibility pre-declaration (#50,
   deep-read 92) demands: the existence statement is stated WITH its domain —
   R(θ1) ≥ 0, R(θ2) ≥ 0, h locally bounded, ‖h‖L1 < ∞ (PDF pp. 2, 6) — and
   the |F(t)| ≤ 1 bound is what keeps the defining expectation finite all the
   way to the boundary R(θ) = 0 where the Laplace transform doubles as a
   characteristic function; the uniqueness proof is quantitative (Gronwall
   with constant 3‖h‖L∞[0,T]E[𝓁1], PDF pp. 10-11), so the domain is an
   explicit function of the frozen configuration (E[𝓁1], ‖h‖∞) exactly in the
   shape clause (i) of the pre-declaration. Nothing here extends the rule:
   the paper conforms to it, which is evidence the rule describes real
   practice, not a hypothetical discipline. No queue change.

2. [reinforcing, no new item] Every statistic in the paper is CONSTRUCTED, not
   closed: F (hence the transform, moments and every dark-pool metric) is the
   numerical collocation solution of the Volterra equation on a chosen mesh —
   150 subintervals, ~25 s per solve, runtime reported per configuration
   (Table 1, PDF pp. 19-20) — and the distribution of LT is then a numerical
   Bromwich inversion (EULER) of that numerical solution (PDF pp. 19-23);
   a discretization choice sits between the written definition and every
   reported number, exactly the frozen-configuration class the
   estimator-implementation concordance rule (#46, deep-read 85) and clause
   (iii) of #50 (frozen numerical-tolerance/truncation convention) already
   make mandatory. Supports both queued rules; licenses nothing new. No
   queue change.

3. [interpretation caution] Remark 6 and Proposition 5: the first moments of
   NT and LT depend on the mark law ONLY through E[𝓁1] (E[LT] = E[𝓁1]·E[NT]),
   and the second moment of LT only through the first two mark moments (PDF
   pp. 12-13); likewise the conditional at-least-one-fill probability (3.6)
   is independent of the mark distribution entirely, and the exactly-one-fill
   probability (3.7) depends on it only through its Laplace transform (PDF
   pp. 17-18). Reading discipline for any future C8-adjacent Hawkes-moment
   feature: low-order moments and many conditional functionals are BLIND to
   the mark mechanism, so a moment-based feature may never be interpreted as
   evidence about trade-size dynamics beyond the mean, and two different mark
   mechanisms (constant vs exponential vs hyper-exponential sizes, the
   paper's own Figure 3 experiment, PDF pp. 20-22) are observationally
   equivalent at the moment level while differing in the tails. Feeds the
   model-inversion identifiability pre-declaration family (#49, deep-read
   91) as reading discipline only. No queue change.

4. [interpretation caution] The baseline-intensity experiment (Figure 8, PDF
   pp. 25-27): the expected fill rate under a piecewise-constant baseline is
   NOT reducible to the baseline level path — a pool with the LOW baseline
   level first can out-fill the constant-1 pool on the later interval because
   the intensity carries the entire event history across the regime change;
   any future feature built on a Hawkes intensity across an intraday
   regime boundary inherits this path-dependence, so "same parameters,
   different history" is not a covariate, it is a different law — an
   interpretation caution for cross-window comparisons in any C8 arm that
   pools regimes with a common frozen configuration. No queue change.

5. [cost-survival ammunition] The entire application half (PDF pp. 14-30) is
   execution-strategy engineering for a venue class (midpoint-peg dark-pool
   resting orders under first-come-first-served matching) outside the
   C1-L2/C8 scope: time-to-first-fill, time-to-complete-fill, fill rates,
   conditional fill probabilities are liquidity-seeking/routing quantities
   and are recorded here only as standing context; the "liquidity begets
   liquidity" clustering motivation (PDF p. 3) is industry folklore cited
   from practitioner papers (Buti et al., Markov-Ingargiola, Mittal-Taur),
   never evidence for any programme claim; if a future K7-style
   cost-survival layer ever exists, its assumptions must carry what this
   model assumes away: no adverse selection against the pegged midpoint,
   no information leakage from fills, initially empty (or Weibull-Y)
   pools, and matching-rule invariance across venues. No queue change.

6. [source-quality note] arXiv v1 preprint (4 Oct 2017); the paper appeared
   later in peer-reviewed form — cite only the published version after
   verification, per standing convention. No empirical content anywhere:
   all numerics are synthetic MATLAB experiments with invented parameters
   (μ = 1, ‖h‖ = 0.9, unit-mean marks, PDF pp. 19-30). Internal defects
   that do not touch the transform argument: a "¿From" typesetting artifact
   (PDF pp. 17, 40), variable-of-integration slips inside Proposition
   5(iii)-(iv) as printed (ψ2/ψ3 definition lines carry both s- and
   t-arguments in one integral; the claim and proof are unaffected, PDF
   pp. 12-13). Check the published version before formal citation. No queue
   change.

## What this paper would have killed if we had done it wrong

Counterfactual for the already-queued #46 and #50. Had the programme not
already frozen the numerical convention, this paper exhibits a third silent
failure mode beyond the two the VIX-options read named (evaluation outside
the existence domain; concordance of code with a written definition): a
statistic whose value exists ONLY as a numerical Volterra solve returns a
finite number for EVERY mesh — collocation does not error on
under-resolution, it just converges slowly — so two implementations of the
same written definition at different meshes produce different numbers, both
"correct against the text," and a post-hoc mesh re-choice after seeing
results would be a researcher degree of freedom invisible both to the
concordance audit (both meshes faithfully implement the definition) and to
the configuration freeze (both meshes are legal declarations) — a future
L2 comparator built on a transform of a fitted Hawkes family would have
carried this freedom silently into a kill-line verdict. And had the
moment-blindness of finding 3 gone unrecorded, a moment-based Hawkes feature
could have "survived" its gates while being narrated as evidence about a
mark-size mechanism (fat-tailed vs constant trade sizes) the moment provably
cannot see — laundering mechanism attribution without laundering a single
empirical number. Under the existing rules both failures are dead on
arrival: the convention is frozen before the data, and the identification
claim is bounded by what the functional can identify.

## Standing caveat

Purely theoretical, single-variate LINEAR marked Hawkes: no multivariate
cross-excitation (so nothing here speaks to C8's cross-stream arms), no
nonlinearity, no nearly-unstable regime (the branching structure is
subcritical by ‖h‖L1 < ∞ throughout), and the mark enters only as 𝓁·h — a
multiplicative restriction, not a general marked Hawkes. All numerics are
synthetic (MATLAB on a desktop, invented parameters); nothing in this paper
is evidence about crypto L2 microstructure, and the standing caveat binds
absolutely — no magnitudes, no stylized facts, nothing measured here may
enter any spec as support. The dark-pool model assumes first-come-first-served
matching (pro-rata pools named and set aside, PDF p. 4), midpoint pegging
with no limit-price or minimum-execution-size attributes (PDF p. 4), and
its clustering motivation rests on practitioner folklore, not measurement.
arXiv v1 (1710.01452v1, 4 Oct 2017); a peer-reviewed version exists — verify
against it before any formal citation.

Nothing measured, no kill line moved, nothing armed, nothing trades live.
