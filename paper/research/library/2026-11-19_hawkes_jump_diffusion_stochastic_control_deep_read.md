# Deep-read session 41 — Sakhanda and Ricalde-Guerrero, "Stochastic Optimal Control of Hawkes Jump-Diffusion Systems"

Library deep-read session 41 (null-time session 45, log entry
## 49). Daria Sakhanda and Joshue Heli Ricalde-Guerrero (both
Department of Mathematics, ETH Zurich), arXiv:2608.29473v1
[math.OC], stamped 30 Aug 2026; 30 pp. text extract, page-marked,
complete (references PDF pp. 29-30); companion paper [12]
(arXiv:2511.13568, Nov 2025) is the Poisson anchor. A pure-mathematics
control paper: it augments a growth-environment economy (capital K,
pollution stock P, controlled consumption/abatement) with disasters
driven by a marked subcritical Hawkes process (intensity
lambda_H = mu(P-) + Y-, excitation Y with decay b and mark excitation
a(zeta)), proves well-posedness and nonexplosion of the controlled
jump-diffusion, and proves that under a small-excitation scaling
a_eta = eta*a the Hawkes value function converges to the Poisson
value function with an explicit O(eta) bound. Read 2026-11-19, against
ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/xd02283_stochastic_optimal_control_of_hawkes_jump_diffusio.txt,
30 pp., page-marked). Assigned triage-rank entry (score 30, xd02283;
consumed as the next unclaimed UNREAD named by the landed ## 48's
closing pointer; no skips this session: the pointer checked out against
the live branch/PR set — no note for the slug on main, no open pull
requests, no branch claims the entry). Next unclaimed UNREAD triage-
rank entry: "Critical reflexivity in financial markets: a Hawkes
process analysis" (score 30, xdc14f4). A successor session must
re-read the live main tail and the branch/PR set first.

## The paper in one paragraph

The model extends the authors' Poisson-disaster growth framework [12]
to self-exciting disasters: capital follows a controlled SDE with
multiplicative disaster losses K_t = omega(K-, P-, zeta)*K- (omega in
(0, 1]), pollution follows a controlled diffusion, and the disaster
intensity carries a pollution-dependent baseline mu(P-) plus a Hawkes
excitation component dY_t = -b*Y_t dt + integral a(zeta) N(dt, dzeta)
(Eqs. (2.1)-(2.5), PDF pp. 2-3; Assumptions 4.2, PDF pp. 5-6,
including subcriticality a_bar_1 = integral a(zeta)nu(dzeta) < b,
Eq. (4.7)). Proposition 5.1 establishes global strong well-posedness
and nonexplosion via Poisson embedding (thinning), localization,
uniform moment bounds and the positivity of omega (PDF pp. 8-14).
Theorem 5.3 then shows, under the additional baseline-integrability
hypothesis integral-over-[0,infinity) E[mu(P_t)]dt < infinity (5.34),
that E[Y_t] -> 0 with integral E[Y_t]dt = (y + a_bar*integral
E[mu(P_t)]dt)/(b - a_bar) finite (5.36), i.e. the excess Hawkes
intensity vanishes asymptotically in L1 (Corollaries 5.4-5.5, PDF
pp. 15-17), giving compensator-approximation bounds on finite windows
and the infinite tail (Proposition 5.6, Corollary 5.7, PDF pp. 17-19).
Under the joint scaling a_eta = eta*a with initial excitation
y_eta <= c_y*eta (5.45) and assumed uniform-over-controls discounted
moment bounds (5.47)-(5.48), the weighted excitation functional is
O(eta) uniformly over admissible controls (Proposition 5.8, PDF
pp. 20-23; constant A*). The main theorem (5.10/Theorem 4.3, PDF
pp. 25-29) applies the Poisson verification function — explicit for
the CRRA-type utility, v(k, p) = psi^(-eps)(1-eps)^(-1)k^(1-eps) −
x(1+beta)^(-1)p^(1+beta) (Lemma 5.9, PDF pp. 23-24, jump-increment
growth 5.73-5.74) — to the Hawkes generator, the discrepancy being
exactly the excitation intensity times the Poisson jump increment,
and obtains |V^eta_H(k, p, y_eta) − V_P(k, p)| <=
psi^(-eps)/(1-eps)*A**eta (5.83): the Hawkes control problem
converges to its Poisson counterpart as the self-excitation
magnitude vanishes.

## Findings, graded (does any kill line move?)

NO kill line changed. NO new candidate sharpening. Default grade; the
paper is a purely mathematical worked exhibit for read disciplines
already standing (the regime-disclosure family, the assumption-
honesty discipline, the model-relative register), and the burden of
proof for a sharpening — a specific mechanism making a future test
harder to pass — was not met. Findings, page-cited:

1. **[reinforcing, no new item]** Subcriticality is the load-bearing
   condition everywhere in the paper: Definition 3.1 (branching ratio
   m_h < 1, PDF pp. 5-6), the standing assumption a_bar_1 < b
   (Eq. (4.7), PDF p. 6), and its uniform scaled version
   eta_0*a_bar_1 < b (Eq. (5.46), PDF p. 20) under which the
   positivity kappa = 2b + rho − 2*eta_0*a_bar_1 − 2*delta > 0 that
   drives the O(eta^2) excitation bound is even defined (Eqs.
   (5.56), (5.60)-(5.67), PDF pp. 21-23). Every approximation
   theorem (5.3, 5.8, 5.10) is proven strictly inside the
   subcritical regime, with the scaling keeping the branching ratio
   bounded away from 1; nothing analogous exists near criticality in
   the paper. Eighth worked exhibit for the near-critical
   regime-disclosure family (deep-read 17, boundary rule deep-read 5,
   universality deep-read 38, the ## 46, ## 47 and ## 48 exhibits):
   perturbation results around the Poisson benchmark live only in
   the interior of the stable regime, and any future import of an
   "excitation is a small correction" argument must disclose the
   subcriticality its bound consumes. Nothing added; the rule already
   stands.

2. **[interpretation caution]** The asymptotic Hawkes-to-Poisson
   decay (Theorem 5.3, Corollaries 5.4-5.5, Proposition 5.6,
   Corollary 5.7, PDF pp. 14-19) is conditioned on the baseline-
   integrability hypothesis integral E[mu(P_t)]dt < infinity
   (Eq. (5.34), PDF p. 15): the paper's own decay and the finite
   excitation mass (5.36) hold because the Poisson baseline itself is
   transient. The paper proves nothing about stationary-baseline
   regimes, and the conclusion "the Hawkes self-excitation vanishes
   asymptotically" (PDF pp. 8, 19) is inadmissible when quoted
   without (5.34). Read discipline: this sits beside the ACD
   session's fit-test-conditioned caution (## 48) — a headline
   asymptotic statement whose hypothesis quietly excludes the regime
   a market null would live in. No queue change; the model-relative
   and conditions-carry rules already govern.

3. **[interpretation caution]** The O(eta) value-function convergence
   (Theorem 5.10, PDF pp. 25-29) is a joint parameter-and-initial-
   condition result resting on standing, assumed — not derived —
   uniform-over-controls moment hypotheses: a_eta = eta*a AND
   y_eta <= c_y*eta (Eq. (5.45), PDF p. 20), the discounted baseline
   bound (5.47) and the polynomial-moment bound (5.48), plus the
   admissibility of the Poisson-optimal feedback in the Hawkes
   problem (PDF p. 26) and the integrability/transversality
   conditions (5.80)-(5.82). And the metric is expected discounted
   utility: expectation-level closeness of two control problems
   licenses nothing about the distinguishability of their sample
   paths or finite-window arrival laws. The bound must never be
   imported as "Hawkes = Poisson" in any generative-null or placebo
   argument — if a future arm ever proposed a Poisson null standing
   in for a fitted near-Poisson Hawkes alternative, the citation
   would have to carry the joint scaling, the moment assumptions
   unverified in any application, and the expectation-metric gap, or
   it would weaken the very test it was cited to support.
   Assumption-honesty discipline; nothing moves.

4. **[reinforcing, no new item]** The entire comparison runs through
   an explicitly solved Poisson problem: the verification uses the
   closed form v(k, p) = psi^(-eps)(1-eps)^(-1)k^(1-eps) −
   x(1+beta)^(-1)p^(1+beta) whose jump increment cancels the
   pollution term and satisfies the growth bound of Lemma 5.9 (Eqs.
   (5.73)-(5.76), PDF pp. 23-24), a separable-structure speciality of
   the CRRA-type economy of [12]. No general "Hawkes control =
   Poisson control" theorem exists in the paper, only the
   verification template for one explicitly soluble companion model.
   Seventh worked exhibit for the specification-classification
   family (## 47 sixth): mathematics carried by one model's closed
   form licenses nothing outside it;
   library-is-ammunition prevented any import.

5. **[source-quality note]** math.OC preprint, two mathematicians at
   ETH Zurich; zero finance, zero market, zero data, zero
   calibration, zero empirical content — the applied object is a
   climate-growth economy with pollution-dependent disasters, and
   the programme's objects (venues, order flow, order books) are
   never touched. The finance connection is the word "Hawkes" in the
   title. Extraction clean and complete; references include one raw
   "Google-Books-ID" string (PDF p. 29) and the companion [12]
   arXiv:2511.13568 (PDF p. 30). v1, dated 30 Aug 2026, journal
   record NOT checked at reading, published version to be checked
   before formal citation.

## What this paper would have killed if we had done it wrong

If "the Hawkes value function converges to the Poisson one" had been
imported as a license for a Poisson generative null standing in for a
small-excitation Hawkes alternative in any C1-L2 or C8 arm, an
expectation-level, jointly-scaled, assumption-conditioned
verification result from a growth-economy model would have been
laundered into a distributional-indistinguishability claim the paper
never makes, weakening every placebo that depends on telling the two
apart. If the asymptotic decay theorem had been quoted without its
(5.34) hypothesis, "self-excitation washes out" would have entered
the record as unconditional, in exactly the stationary-baseline
regime a market null would occupy, where the paper says nothing. If
the O(eta) constant had been treated as a result rather than as
conditional on the standing uniform-moment hypotheses (5.47)-(5.48),
assumptions would have silently become theorems. The model-relative
register, the assumption-honesty discipline, the regime-disclosure
rule and nothing-measured prevented all three.

## Standing caveat

No market, no sample, no period, no costs: the paper's mathematics is
applied to a stylized economy with climate disasters, not to any
venue, and no number in it is a measurement of anything. All results
assume the exponential-kernel Markovian Hawkes specification (Y_t of
Eq. (5.43)), marks with finite second moment (a in L2(nu), Eq.
(4.3)), a linear-growth baseline mu(p) <= L_mu(1 + p) (Eq. (4.2)),
strictly positive survival omega in (0, 1] (Eq. (4.6), which is what
preserves capital's positivity at jumps and rules out total
destruction), and boundary non-attainment of the continuous
dynamics (Assumption 4.2(e)); the well-posedness claim is local
square-integrability in time, not global (Remark 5.2, PDF p. 14), and
section 5.2's decay statement is under (5.34). arXiv v1, journal
version unchecked. Laundering directions named. INTO — nothing: no
eta-scaling, no decay theorem, no O(eta) bound, no
generator-comparison template enters any spec, default, calibration,
tolerance or generative null, and the paper's convergence may not
serve as a license for any Poisson-versus-Hawkes substitution in a
C1-L2 or C8 arm without an owner-ratified pre-declared derivation of
its assumptions on the programme's venue and fields. OUT — never read
backwards as "Hawkes = Poisson" (expectation-level, jointly scaled,
assumption-conditioned), "self-excitation washes out asymptotically"
(requires the baseline integrability (5.34); stationary case out of
scope), or "optimal control is robust to excitation" (a
value-function metric is not a pathwise or distributional metric).
