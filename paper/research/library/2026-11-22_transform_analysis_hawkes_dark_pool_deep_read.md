# Deep-read session 93: Gao-Zhou-Zhu, "Transform Analysis for Hawkes Processes with Applications in Dark Pool Trading"

Session: null-time session 103 (log entry ## 122), 2026-11-22.
Authors: Xuefeng Gao, Xiang Zhou, Lingjiong Zhu.
Full title: Transform Analysis for Hawkes Processes with Applications in Dark
Pool Trading.
Venue: arXiv:1710.01452v1 (2017), per docs/library/expanded_index.json
(slug x47bbb5, topic arxiv-hawkes). One clause: the paper derives the joint
Laplace transform, moments and distributions of a non-Markovian marked Hawkes
process (general exciting function, time-dependent baseline, i.i.d.
non-negative marks) via the immigration-birth representation, and applies the
formulas to compute fill metrics of a resting midpoint order in a dark pool.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x47bbb5_transform_analysis_for_hawkes_processes_with_appli.txt,
~42 pp., page-marked). Next UNREAD triage-rank entry (score 20).

## The paper in one paragraph

The model is a marked linear Hawkes process with intensity
lambda_t = mu(t) + sum h(t - tau_i) * l_i, mu(t) a general time-dependent
baseline, h a general (non-exponential, only L1-locally-bounded) exciting
function, {l_i} i.i.d. non-negative marks — explicitly non-Markovian
(PDF pp. 1-2). Theorem 1 gives the joint Laplace transform of (N_T, L_T) as
exp(int mu(T-s)(F(s)-1) ds) where F solves a Hammerstein-type Volterra
integral equation, with uniqueness by a Lipschitz/Gronwall argument (PDF
pp. 6-11); Remark 2 recovers the Markovian Errais-Giesecke-Goldberg ODE
system as the exponential special case, and the domain assumptions are
merely Re(theta_1) >= 0, Re(theta_2) >= 0 (PDF pp. 6-7). Corollary 3 and
Proposition 5 give single transforms and the first two moments; N_T-moments
depend on the mark law only through E[l_1], L_T-moments only through
E[l_1], E[l_1^2] (PDF pp. 11-13). Propositions 7-8 give exact mass functions
for N_T and (lattice case) L_T via Faà di Bruno (PDF pp. 13-14, 36-39).
Section 3 models a dark pool's consolidated contra-side arrivals as this
process and computes time-to-first-fill, time-to-complete-fill, expected fill
rate, and fill probabilities/expectations conditioned on a past fill
(PDF pp. 14-29), extended to non-empty pools by treating a time-zero partial
fill as a modified baseline mu + |y|·h(t) (PDF pp. 26-29); numerics are
collocation plus Euler-summation Bromwich Laplace inversion (mesh 150 on
[0,6], ~25 s per solve) and FFT fill curves (PDF pp. 19-25). No estimation on
any data anywhere; every parameter is invented for illustration.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   moment-equivalence disclosure (#51): the paper proves in print that two
   models agreeing in finitely many mark-moments can disagree arbitrarily in
   law-sensitive outputs. Proposition 5 with Remark 6 shows E[N_T] and E[L_T]
   depend on the mark law ONLY through E[l_1] (and E[L_T^2] only through the
   first two moments, PDF pp. 12-13), while the same-mean mark laws
   (constant, exponential, hyper-exponential) are then shown to produce
   systematically different fill-rate and conditional-fill outputs
   (Figures 2-4, PDF pp. 20-23), with a proved ordering
   E[sigma^(3)_x] > E[sigma^(2)_x] = x+1 > E[sigma^(1)_x] = ceil(x) in the
   compound-Poisson case and the explicit statement that the Hawkes
   time-to-complete-fill "depends on the distribution of l_i, not just its
   coefficient of variation" (PDF pp. 20-21, 41-42). Proposed amendment:
   BEFORE the L0 gate, any model-based comparator, null, or statistic built
   from a marked point-process or marked-intensity construction must
   pre-declare, as part of its frozen configuration, which of its outputs
   are moment-bounded (provably functions of finitely many moments of the
   mark/size law, hence inheritable from a moment-matched calibration) and
   which are law-sensitive (functions of the full mark law); a
   concordance or validation audit that matches only finitely many moments
   may certify the moment-bounded outputs and may NOT certify the
   law-sensitive ones. Harder-to-pass because today a moment-matched
   implementation can pass the estimator-implementation concordance
   audit (deep-read 85) while its law-sensitive outputs — the exact class
   the paper shows to differ across same-mean laws — were never checked
   against the declared law; under the rule such an audit fails at the
   gate. Tightens the estimator-implementation concordance rule (deep-read
   85, which checks code against a written definition but never asks
   which outputs of that definition survive moment-matching) and joins the
   estimator-configuration freeze (deep-read 63) and the transform-domain
   admissibility pre-declaration (#50) in extending frozen configuration
   to the analytic sensitivity class of the estimator's outputs. The
   paper is silent on estimation, so nothing here launders; the mechanism
   is the proved moment-dependence hierarchy, not its numerics.

2. [reinforcing, no new item] The instability lever is again the
   self-excitation magnitude: the numerics fix the branching structure at
   ||h||_L1 = 0.9 (C = 0.9 power-law kernels, PDF p. 23) and the fill
   metrics drift materially with the kernel tail exponent gamma
   (Figures 5-7, PDF pp. 24-26) — the same near-critical configuration
   whose frozen distance from criticality the self-excitation
   regime-window pre-declaration (deep-read 53) already demands, here
   instantiated wholesale in invented parameters. All numeric magnitudes
   from this paper are banned from the record under the laundering rule
   (invented parameters, no data). No queue change.

3. [interpretation caution] The first-event statistic is baseline-only:
   time-to-first-fill has distribution 1 - exp(-int mu) with the
   self-excitation component absent entirely (PDF p. 16), so a first-
   arrival statistic carries zero information about the excitation
   structure; excitation becomes measurable only conditional on a realized
   event, and even then the conditional formulas require treating the
   conditioned fill as a random time-dependent baseline (eqs. 3.6-3.9,
   eq. D.1, PDF pp. 17-18, 26-28, 39-40). This is a clean instantiation
   for the C1-L2 family of the level-versus-memory disambiguation
   (deep-read 59) and a sibling of the model-inversion identifiability
   pre-declaration (#49): an excitation parameter inferred from
   first-event behavior is unidentified by construction, and any future
   admission statistic whose power rests on first-move priming must say
   so against its own baseline decomposition. No queue change.

4. [cost-survival ammunition] The dark-pool fill-rate arithmetic
   (time-to-complete-fill, expected fill rate, cross-pool routing context,
   PDF pp. 15-29) is execution-strategy engineering and is NOT
   operationalized, per the standing rule. Recorded only as assumptions a
   future K7-style cost-survival layer would have to carry if one ever
   exists: the numerical-tolerance conventions are themselves
   configuration — piecewise-linear collocation on 150 subintervals,
   Euler-summation Bromwich inversion, FFT across order sizes (PDF
   pp. 17, 19) — and any transform-computed number inherits them. No
   queue change.

5. [source-quality note] arXiv v1 preprint; the published version exists
   (the authors are established; the arXiv id is the only venue on the
   shelf record) — check the published version before formal citation.
   Internal defects that do not touch the results: repeated "¿From" LaTeX
   typesetting artifacts (PDF pp. 17, 22, 37, 40), a dense but correct
   Faà di Bruno apparatus (PDF pp. 36-39), and the non-empty-pool
   section leaving the conditional Y > 0 branch informal (PDF
   pp. 26-28). Zero empirical content: no dataset, no calibration, all
   parameters invented for illustration. No queue change.

## What this paper would have killed if we had done it wrong

If a future L2 comparator had been built as a marked Hawkes intensity and
validated by matching its predicted count and volume moments to cached
data, this paper is the printed proof that the validation would have been
vacuous for exactly the outputs it mattered for: two mark laws with the
same mean produce the same E[N_T] and E[L_T] to the exact decimal
(Proposition 5, PDF pp. 12-13) while their fill/conditional outputs
provably separate (eq. 3.10 and Figures 2-4, PDF pp. 20-23). Without the
concordance discipline (deep-read 85) the moment-matched implementation
would look faithful; without the moment-equivalence disclosure the
law-sensitive tail of its output family — the part C1-L2 would actually
test — would ride on an uninstantiated distributional assumption chosen
by the implementer after the fact. And if a "priming implies imminent
events" narrative had been fed by first-arrival rates, the baseline-only
theorem (PDF p. 16) shows the first event would have carried no
self-excitation signal at all: the claim would have been laundering the
baseline, not testing the mechanism. The program's defaults (no empirical
input from papers, frozen configuration, concordance against written
definitions) are what avoided both.

## Standing caveat

Everything is for a self-exciting linear marked Hawkes family with
non-negative marks and additive intensity feedback; the dark-pool mapping
assumes midpoint pegging, time-priority matching, an empty (or
independently distributed initial-liquidity) pool, and contra-side
arrivals exogenous to the resting order — no adverse selection, no
information asymmetry, no re-routing response to the resting order itself
beyond the excitation term. The stability of every formula rests on
||h||_L1 < infinity with the branching interpretation ||h||_L1
(unmarked case) at 0.9 in the numerics; nothing here licenses use at or
near criticality. The conditional-fill formulas are specific to the
single-past-fill conditioning event. arXiv v1: check published version
before formal citation. A library is ammunition, not evidence: no
empirical claim from this paper enters the record as support for any
programme claim.
