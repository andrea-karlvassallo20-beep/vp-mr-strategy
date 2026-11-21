# Deep-read note — session 74: "A new self-exciting jump-diffusion process for option pricing" (Souto Arias–Cirillo–Oosterlee, arXiv:2205.13321v2)

**Deep-read session 74** (null-time session 85). Luis A. Souto Arias, Pasquale
Cirillo, Cornelis W. Oosterlee, "A new self-exciting jump-diffusion process
for option pricing", arXiv:2205.13321v2 [q-fin.PR], 2022, v2 stamped
10-13 February 2023. A pricing-methodology paper: it introduces the
Heston-Queue-Hawkes (HQH) asset model — Heston diffusion plus the
Queue-Hawkes (Q-Hawkes) jump process, whose "ephemeral" memory deletes the
effect of each self-exciting jump at once at a stochastic expiration time
rather than continuously — and exploits its closed-form characteristic
function to price European and Bermudan options with a Fourier-cosine
(COS) method extended to discrete distributions.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x673148_a_new_self_exciting_jump_diffusion_process_for_opt.txt,
~23 pp., page-marked). Next UNREAD triage-rank entry (score 24, x673148),
first of the score-24 tier.

## The paper in one paragraph

The paper defines a Heston jump-diffusion in which the jump counting
process has stochastic intensity with two variants: the Q-Hawkes intensity
dλt = α(dNt − dNQ_t), where a second counting process NQ_t erases a unit of
self-excitation per jump (Eqs. 1-3, 8-9, PDF pp. 2-4), and the classical
exponential-kernel Hawkes intensity (Eq. 4, PDF pp. 3, 8-9). The HQH
model's asset-level characteristic function decomposes into the Heston
factor and a compensated jump factor in closed form (Prop. 4, Eq. 17,
PDF pp. 6-7); the HH alternative needs a numerically solved ODE system
(Prop. 7, PDF pp. 9-10). The Q-Hawkes intensity has a closed-form PMF via
a negative-binomial convolution (Prop. 3, PDF pp. 5-6), and partial
integrals of the characteristic function are worked out in full
(Prop. 5, Appendix A, PDF pp. 7-8, 22-23). On the numerical side the
authors extend the COS method to discrete distributions (the DCOS method,
Def. 1 and Eq. 40-48, PDF pp. 10-11, with an exact aliasing error formula
showing DCOS always overestimates the PMF, Eq. 48, PDF p. 11), reduce the
Bermudan COS recursion from three dimensions to one for HQH using the
analytical marginals (Prop. 8 and Eqs. 60-65, PDF pp. 12-14), and run
parametric pricing experiments under two scenarios (Table 1, PDF p. 15):
HQH prices are 12.36x faster than HH (Table 2, PDF p. 16), HH always
yields higher implied volatilities than HQH (PDF pp. 16-17), the smile
differences between the two self-exciting models are driven mainly by the
mean jump size μY rather than the clustering rate α (PDF p. 15), and the
model differences grow with the degree of self-excitation α/β and the
initial state of excitation αQ0/λ0 (PDF pp. 18-19). No data is fit
anywhere; all experiments are parametric exercises.

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Nothing in this paper
changes an admission rule, a null family, or a window discipline; it is a
Fourier pricing paper whose market content is entirely risk-neutral model
geometry, read here for identification discipline only.

1. [reinforcing, no new item] First-moment equivalence of the two
   memory mechanisms: the paper states that Q-Hawkes and Hawkes have the
   same expectations, both in intensity and in counting processes, and
   differ only in moments of order k ≥ 2 (PDF p. 5, cf. E[Mt] Eq. 68,
   PDF p. 19, identical for both models). Any estimator calibrated only on
   first moments (mean intensity, mean count) is therefore unidentified
   between a continuous-decay memory and an all-at-once stochastic
   erasure memory — the fitted "degree of self-excitation" would carry
   the memory-mechanism assumption, not the data, exactly the family
   dependence already frozen by the price-process-family invariance rule
   (log ## 85) and the level-versus-memory disambiguation. Reinforces
   that family; no new item.

2. [reinforcing, no new item] Smile flexibility is parameter geometry,
   not information: the self-exciting models produce a wider range of
   volatility smiles than Bates (PDF p. 16), but the paper's own
   sensitivity study attributes the HQH-versus-HH gap mainly to the mean
   jump size μY, with the clustering rate α second (PDF p. 15), and the
   two models converge to Bates at both α → 0 and β → ∞ (PDF p. 18).
   The flexibility claim quantifies how much of an implied-volatility
   surface a two-parameter excitation block can absorb without any
   predictive content — reinforcing the standing caution that model-fit
   flexibility is never evidence of structure; no new item.

3. [interpretation caution] Risk-neutral pricing absorbs self-excitation
   into a compensated drift: the asset SDE carries the compensation term
   −μ̄Y λt− dt so the discounted price is a martingale under Q (Eq. 1,
   PDF p. 2), and every implied-volatility difference the paper exhibits
   is a difference in assumed pricing measure, not a measured property of
   any market (PDF pp. 15-17). Any C8-adjacent exhibit citing option
   prices or implied volatilities generated under a self-exciting model
   as support for anticipatory or predictive structure would be
   laundering pricing-measure geometry into a forecast claim; reading
   discipline only, no queue change.

4. [reinforcing, no new item] Nothing is validated on data, and the paper
   says so only implicitly: all experiments are parametric exercises on
   the model's own simulation (Table 1, PDF p. 15; the deeper
   experiments "not shown here" live in a GitHub repo, PDF p. 18), with
   no fit to any market series, no calibration procedure, and no
   out-of-sample anything. This cannot serve as support for any
   programme claim, empirical or otherwise — the default ammunition-not-
   evidence rule; no new item.

5. [cost-survival ammunition] If a future K7-style cost-survival layer
   ever prices or hedges under a self-exciting jump model, this paper
   declares the numerical-implementation assumptions that layer must
   carry before any cost number is trusted: the DCOS aliasing error is
   one-sided (the PMF is always overestimated, Eq. 48, PDF p. 11), so
   option-value approximations inherit a sign-consistent bias; the HH
   route needs 2 × Nx × Nλ × NH² ODE solves per recursion step
   (Remark, PDF p. 15), a computational-fragility surface the HQH route
   avoids only by assuming the Q-Hawkes memory; and the moments of the
   log-asset price "may become infinite depending on the parameter set"
   via the Heston component (footnote 2, PDF p. 2). Recorded only as
   declared assumptions; never operationalized, nothing armed.

6. [source-quality note] arXiv v2 preprint (q-fin.PR), zero recorded
   citations in the index, no journal version recorded; the index year
   (2022) is v1's year while the extract carries the v2 stamp of
   February 2023 — check the published version before any formal
   citation; regardless, a pure-methodology preprint with no empirical
   content can never serve as support for any programme claim.

## What this paper would have killed if we had done it wrong

Without the price-process-family invariance rule, this paper is exactly
the kind that launders a mechanism choice into a finding: two memory
mechanisms — continuous exponential decay and stochastic all-at-once
erasure — agree on every first moment (PDF p. 5) and differ only in
higher-order moments, so a C1-L2 intensity estimator calibrated on
first-moment statistics would have returned a confident "self-excitation
parameter" whose value is a function of the untested memory-family
assumption. Had a spec entered the record on the strength of such a fit,
the falsification record would have been spent arbitrating a kernel-shape
choice disguised as a measurement, and worse, the same artefact family
would resurface at the ODE boundary: the paper's own HH implementation
needs 2 × Nx × Nλ × NH² numerical ODE solves per step (PDF p. 15), so a
fragility in the numerics would masquerade as a regime change in the
excitation. The implied-volatility counterfactual is the third kill
avoided: the self-exciting models produce wider smiles than Bates
(PDF p. 16), and a naive reading would file that as "the market prices
contagion", when the paper shows the width is mostly μY geometry
(PDF p. 15) inside a martingale construction (Eq. 1, PDF p. 2).

## Standing caveat

A pricing-methodology paper with no empirical anchor: no data is fit, no
calibration is performed, all numerics are parametric exercises in the
model's own simulation under two hand-picked scenarios (Table 1,
PDF p. 15); the jump and diffusion components are assumed independent
(PDF p. 2), the log-asset moments can be infinite for some parameter sets
(footnote 2, PDF p. 2), the Q-Hawkes joint characteristic function is
one-dimensional only — cross-excitation, marks and general expiration
mechanisms are named future work (PDF p. 20) — and the Bermudan recursion
truncates the activation-number sum by quadrature without a stated
truncation-error bound (Eqs. 64-65, PDF pp. 14-15). arXiv-version
caution: v2 stamped 13 February 2023, index year 2022, zero recorded
citations — check the published version before formal citation. Nothing
here validates any model on real data, and the paper claims no
predictive content anywhere.
