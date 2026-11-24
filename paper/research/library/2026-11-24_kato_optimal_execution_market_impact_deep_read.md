# Deep-read session 105 — Kato (2014), "An Optimal Execution Problem with Market Impact"

Authors: Takashi Kato. Venue: arXiv:0907.3282v8 [q-fin.TR], 13 Dec 2014;
preprint of the article published in Finance and Stochastics, DOI
10.1007/s00780-014-0232-0 (PDF p. 34). One clause on what it is: a
stochastic-control theory paper that solves a continuous-time optimal
liquidation problem under a convex permanent market-impact function,
proving that the value function's behaviour at the time origin, the
semi-group property, and the viscosity-solution characterisation of the
HJB all hinge on the growth class of the impact function at large
execution speed.

Read 2026-11-24, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xc35349_an_optimal_execution_problem_with_market_impact.txt,
~36 pp., page-marked). Next UNREAD triage-rank entry (score 19, FIRST of
the score-19 tier; the tier holds SEVENTEEN entries — this session
consumes the true tier head, correcting the ## 139 closing pointer,
which named x03aa07 as head of a claimed five-entry tier; both claims
were wrong, verified against the triage file and the note register this
session).

## The paper in one paragraph

A single trader liquidates a holding of Phi shares of one risky asset
over a horizon, execution speed zeta_r chosen progressively with no
short sales, the unaffected log-price following a generic bounded-
coefficient diffusion and the sale subtracting a permanent impact
g(zeta_r)dr per unit time, g convex, non-decreasing, C¹, with h = g'
its marginal impact (Sec. 2, PDF pp. 3-5; the model is derived as the
limit of discrete-time models under the C¹-matching condition [A],
g_n's derivative matching h(nψ) per step, Sec. 7, PDF pp. 14-16).
The main theorem proves the value function is continuous in every
argument EXCEPT the time origin, where right-continuity is decided by
h(infinity): if h(infinity) = infinity (superlinear impact) no-trading
is optimal in infinitesimal time and liquidation proceeds in a
vanishing window are bounded to zero (Lemma 9's explicit bound
phi(r) -> 0, PDF pp. 20-22); if h(infinity) < infinity (at-most-linear
impact) the value function jumps at t = 0 to J_u, the utility of
selling any amount psi INSTANTLY at the strictly positive discounted
price e^{-h(infinity)·psi} (Theorem 1, PDF p. 6, realised by the
zeta^delta strategies (3.1)). The Bellman principle holds via Nisio's
method (Theorem 2, PDF p. 6; proof pp. 19-20), the HJB characterisation
requires the technical condition (3.4) verified through [C1]-[C2]
(Theorem 3 with Proposition 1, PDF pp. 7-8, proof pp. 24-26), and
UNIQUENESS of the viscosity solution binds exactly in the
quadratic-or-faster class, lim inf h(zeta)/zeta > 0 (Theorem 4,
PDF p. 8). The sell-off condition (must liquidate everything) changes
nothing in continuous time (Theorem 1 of Sec. 4, PDF p. 9). The
examples: under log-linear impact g(zeta) = alpha·zeta the
risk-neutral value is exactly w + (1-e^{-alpha·phi})/alpha · s,
attained by liquidating the whole holding arbitrarily fast (Theorem 1
of Sec. 5.1, PDF p. 11), the timing flipping wholly with the drift
sign (Remark 5: mu-tilde > 0 immediately, < 0 at the terminal time,
= 0 all schedules identical, PDF p. 11); under log-quadratic impact
g(zeta) = alpha·zeta² the optimal schedule's FORM depends on holdings
phi against two thresholds (Theorem 2 of Sec. 5.2, PDF pp. 11-12):
small holders finish via constant-velocity sell-off by time
phi·sqrt(alpha/mu-tilde), large holders cannot finish at all within
the horizon (the arctanh schedule, "the trader cannot finish the
selling", PDF p. 12), the middle region solved only numerically at
n = 500 (Figures 1-4, PDF p. 13). The author's own conclusion: convex
impact induces gradual liquidation, linear impact does not, and since
empirical impact is often concave, the observed gradual liquidation
of real traders must come from risk aversion or — "we surmise" —
transient impact, which this paper excludes "due to technical reasons"
(Remark 2, PDF p. 5; Sec. 6, PDF p. 14).

## Findings, graded (does any kill line move?)

NO kill line changed. ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The impact
   growth-class pre-declaration: BEFORE the L0 gate, any C1-L2/C8-
   adjacent impact function — a generative null's, placebo's,
   comparator's, cost model's or simulator's impact parameterization,
   permanent or transient — must pre-declare, as frozen configuration
   counted in the multiplicity ledger: (i) the impact function's
   large-size growth class (at-most-linear, h(infinity) < infinity;
   strictly superlinear, h(infinity) = infinity; quadratic-or-faster,
   lim inf h(zeta)/zeta > 0), and (ii) for any discrete-grain
   construction, the rescaling that defines its continuous-time limit
   (the condition-[A] class: the per-step impact g_n C¹-matched to its
   own h at the grain, Sec. 7 and eq. (7.5), PDF pp. 15-16) — with any
   conclusion that depends on instantaneous/block-liquidation
   feasibility or on vanishing-window cost bounds licensed only under
   the declared class. Harder to pass because the choice is load-
   bearing and today silent: Kato proves in print, on one and the same
   admissible strategy class, that two impact functions identical in
   every parameter but the growth class disagree on whether the price
   can be pushed through an instantaneous block sale at strictly
   positive finite cost — at-most-linear admits it (the value jump
   J_u selling psi shares instantly at e^{-h(infinity)·psi}, Theorem
   1(ii), PDF p. 6), superlinear forbids it (Lemma 9's proceeds bound
   phi(r) -> 0 in vanishing time, PDF pp. 20-22) — so a
   "crash-speed", "liquidation-feasibility" or "vanishing-time cost"
   conclusion from an impact-bearing null is today a function of an
   undeclared researcher degree of freedom, with no visible
   fingerprint in the outputs; and the characterisation/uniqueness
   theorems themselves bind only in the quadratic-or-faster class
   (Theorem 4, PDF p. 8), so even which solution statements are
   well-posed depends on the class. No queued rule asks the question:
   the impact-viability pre-declaration (deep-read 87) audits the
   pointwise no-PMS/no-TTPM sign conditions of the transient layer,
   not the large-size growth class; the strategy-class/convention
   well-posedness pre-declaration (deep-read 102) declares the
   admissible process class, but the flip proven here is NOT a
   strategy-class effect — it holds over the same unbounded class
   A-tilde (PDF pp. 11-12); the queue-jump-diffusion generative-null
   pre-declaration (queued ## 107) freezes null parameters, not
   functional form; the generative-null agent information-set
   pre-declaration (queued ## 139) marks agent inputs, not the impact
   functional's tail. Tightens the impact-viability pre-declaration
   (deep-read 87) by extending the generative-null pre-declaration
   family from sign-condition viability to the impact function's
   growth class, and joins the strategy-class well-posedness
   pre-declaration (deep-read 102) in forcing the mathematical
   objects a cost or optimality statement is posed over to be
   declared before the statement may license anything.
2. [reinforcing, no new item] Permanent-only impact is a declared
   exclusion, not a neutral default: the paper's own machinery cannot
   treat transient impact without losing the Bellman-principle proof
   (Remark 2's honest statement that the temporary-impact value
   function exists but its properties cannot be studied "due to
   technical reasons", PDF p. 5), and the author's conclusion concedes
   the model's limit outright: real traders liquidate gradually
   despite concave empirical impact, and the reconciliation must come
   from risk aversion or the transient component, "we surmise another
   reason: the existence of a temporary (or transient) impact"
   (PDF p. 14). Reinforces the transient-layer pre-declaration family
   (impact-viability, deep-read 87, whose premise is that any
   impact/reversion layer must be declared before a null may refute)
   with the printed converse: a permanent-only specification silently
   excludes the component the author himself identifies as necessary
   to reproduce observed schedule behaviour. No queue change.
3. [interpretation caution] Linear permanent impact carries no
   scheduling signal for a risk-neutral trader: with g(zeta) =
   alpha·zeta the value is exactly w + (1-e^{-alpha·phi})/alpha · s,
   attained by liquidating the whole holding arbitrarily fast
   (Theorem 1, Sec. 5.1, PDF p. 11), timing flipping wholly with the
   drift sign (mu-tilde > 0 immediately, < 0 at the terminal time, = 0
   every schedule identical in profit, Remark 5, PDF p. 11). Any
   future impact-timing covariate or "execution pressure" reading
   grounded in a linear permanent-impact specification is a drift
   reading in disguise: under linearity the schedule information lives
   in drift and risk aversion, not impact. No queue change.
4. [cost-survival ammunition] The interactive-regime structure any
   K7-style cost layer must carry: under quadratic impact the optimal
   schedule's form depends on holdings phi against two thresholds
   (Phi-hat 1, Phi-hat 2, eqs. (5.3), PDF p. 12) — small holders finish
   via constant-velocity sell-off by time phi·sqrt(alpha/mu-tilde),
   large holders cannot finish at all within the horizon (PDF p. 12),
   the middle regime solved only numerically (PDF p. 13) — so a
   single optimal-schedule or cost-bound template does not transfer
   across inventory states; blocks the "one cost curve" shortcut if a
   cost layer is ever ratified. Relevant only under a future
   K7-style cost-survival layer. No queue change.
5. [source-quality note] arXiv v8 [q-fin.TR] 13 Dec 2014, 36 pages: the
   preprint of the peer-reviewed published version, stated on the
   extract itself — "published in Finance and Stochastics, DOI:
   10.1007/s00780-014-0232-0" (PDF p. 34) — so the standing arXiv
   caution upgrades to "published version identified; cite it". Pure
   theory: no data anywhere, all examples Black-Scholes drift with
   risk-neutral utility (the control collapses to a deterministic
   problem, Proposition 2, PDF p. 10); the viscosity characterisation
   needs condition (3.4) verified via [C1]-[C2] (PDF pp. 7-8). No
   queue change.

## What this paper would have killed if we had done it wrong

Without finding 1's pre-declaration, a future L2-phase impact
comparator or generative null could produce or refute a
"fast-crash"/"instantaneous liquidation" conclusion while its impact
function's undeclared growth class silently chose the answer: the
value function's discontinuity at the time origin would be read as a
market property when Theorem 1 proves it is a function-class property
(Theorem 1(i)-(ii), PDF p. 6); and a discrete-grain simulator refined
across grains without declaring the condition-[A] rescaling would
present changing outputs as a robustness sweep when Section 7 proves
the continuous-time model itself changes with the undeclared
rescaling (Theorem 1 of Sec. 7, PDF pp. 15-16). The
frozen-configuration/multiplicity-ledger discipline, extended by this
item to the impact function's tail, closes the laundering channel
before any L0 gate run. Without finding 2's converse, a permanent-only
execution model would enter the record as the neutral default for
schedule questions when its own author concedes it cannot reproduce
the observed behaviour (PDF p. 14).

## Standing caveat

Everything above is the arXiv v8 text (36 page-marked PDF pages: header,
body, both examples, sell-off section, the discrete-derivation appendix
A with both convergence propositions, all of appendix B's proofs,
references complete; nothing skipped). Scope: one risky asset, permanent
impact only, no short sales, strategy class bounded execution speed
with the terminal-unbounded extension proven value-neutral (PDF
pp. 11-12), T = 1, risk-neutral utilities for every worked example. The
author's own honesty: permanent-plus-concave impact does not predict
the gradual liquidation real traders practise (PDF p. 14). Nothing here
licenses any C1-L2 or C8 claim: the paper is ammunition for impact-
functional discipline and cost-layer structure, not evidence. The
published version is Finance and Stochastics (DOI 10.1007/s00780-014-
0232-0, PDF p. 34); cite it for any formal citation.

Nothing measured during this session. No kill line moved. Nothing armed.
Nothing trades live.
