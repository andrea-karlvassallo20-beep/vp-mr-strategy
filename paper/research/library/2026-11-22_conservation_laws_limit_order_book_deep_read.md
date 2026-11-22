# Deep-read session 88 — Conservation Laws in a Limit Order Book (Rosenzweig, 2019)

**Library deep-read session 88 (null-time session 98, head of the score-21
tier).** Jan Rosenzweig (Pine Tree Funds; visiting senior research fellow,
King's College London), "Conservation Laws in a Limit Order Book",
arXiv:1910.09202v2 [q-fin.TR] (index year 2019; v2 stamp 8 Dec 2020). One
clause on what the paper is: a deterministic fluid-dynamics-style continuum
model of limit-order-book quantity, in which book formation and recovery
after aggressive liquidity taking are governed by a nonlinear transport
equation whose self-similar solutions yield a t^{1/3} recovery scaling and a
square-root steady-state profile, with no data anywhere.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x532697_conservation_laws_in_a_limit_order_book.txt,
~11 pp., page-marked). Next UNREAD triage-rank entry (score 21).

## The paper in one paragraph

The book's quantity h(S,t) at level S obeys a conservation law with a
source/sink split, h_t(S,t) - Q_S(S,t) = P(S,t), where Q is the inter-level
quantity flux and P collects order creation/cancellation away from the touch,
while aggressive liquidity taking enters only as a boundary condition, not
as a source term (Eqs. 1-4, PDF pp. 1-2). A fluid-dynamics apparatus is then
bolted on: a velocity u(S,q,t) of volume at level S and queue place q
(Eq. 5, PDF p. 2), a constitutive pressure proportional to level occupancy,
p = theta*h(S,t), read as market makers preferring empty levels to full ones
(Eq. 6, PDF p. 2), and an algebraic velocity profile proportional to the
pressure gradient in which queue-front orders move only at a slip rate u0
and queue-rear orders are most mobile (Eq. 7, PDF p. 3). These assemble into
a second-order nonlinear isotropic transport equation, h_t = (h^2)_{SS} +
(u0*h)_S + P, in a rescaled time t -> t/(theta*(beta+1)), identical to the
gravity-driven thin-film equation of an inviscid fluid (Eqs. 8-9, PDF p. 3),
with anisotropy admitted to be handled only through boundary conditions
(PDF p. 3). Steady states are square-root profiles, pressure maximal at the
touch and book quantity vanishing after finitely many levels (Eq. 11, PDF
pp. 3-4). The main result: book recovery from aggressive taking is
self-similar with H(t) ~ t^(-1/3), L(t) ~ t^(1/3), S0(t) ~ t^(1/3) (Eq. 13,
PDF p. 4), the similarity function satisfying 3(v^2)'' + v's - gamma*v' + v =
0 with dimensionless touch speed gamma (Eqs. 14-16, PDF p. 4); the deep book
decays like 1/s, formally implying infinite book volume cut off in real life
only by quantity discreteness (Eq. 18, PDF p. 4), and there is no positive
similarity solution for a retreating touch, gamma < 0 (PDF p. 4). Touch and
far-field asymptotics are worked out (Eqs. 17-20, PDF pp. 4-5), and the
similarity profile is noted to resemble the Gatheral and Bouchaud et al
order-density shapes, which the author attributes to the boundary conditions
rather than to any mechanism (PDF p. 5). Simulations of a post-execution ask
book show the self-similar pressure wave advancing per t^(1/3) until the
touch hits a firm stop simulating the bid book, after which pressure builds
at the constrained touch and the book converges very slowly to the steady
square-root profile on time scales the author declares of no practical
importance (PDF pp. 5-6; Figs. 5-6, PDF pp. 10-11). No data, no stochastic
term, no estimation, no costs appear anywhere; all six figures are model
illustrations; the author closes by stating the model holds only "in a
statistical ensemble sense" and that it would be foolish to feed it a real
book snapshot and expect a realistic prediction (PDF p. 6).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The headline t^{1/3} recovery law is printed
   from pure determinism: a nonlinear transport equation with zero noise,
   zero self-excitation and zero information flow produces a power-law
   book-recovery shape as a closed-form structural consequence (Eqs. 9, 13,
   PDF pp. 3-4; conclusions, PDF p. 6; Figs. 5-6, PDF pp. 10-11), and the
   steady square-root profile is likewise a boundary-condition artifact of
   the same equation (Eq. 11, PDF pp. 3-4). A power-law recovery exponent is
   therefore not evidence of a stochastic mechanism, let alone of an
   anticipatory one: this is exactly the artifact class the queued
   deterministic-calendar null (deep-read 73) exists to block, and the
   laundering rule bans every magnitude and exponent in this paper from the
   record. What the paper licenses is ammunition only: a transport-family
   simulator with analytically known self-similar attractors is a cheap
   deterministic comparator for future generative-null work. No queue
   change.

2. [reinforcing, no new item] The time-scale collapse is printed in the
   derivation: the constitutive constants theta, rho and beta are grouped
   into a single clock rescaling, t -> t/(theta*(beta+1)), before any
   solution is computed (Eq. 9, PDF p. 3), and the author states the
   transport equation's form is independent of the algebraic velocity
   profile, which only sets the relaxation time scale (PDF p. 6). Any fit of
   this family to data therefore carries a fully free clock constant and no
   mechanism-identification content: precisely what the queued flow-clock
   scale-constant item, the estimator-configuration freeze (deep-read 63)
   and the primary-metric pre-commitment (deep-read 55) already bind, and
   why a post-hoc "t^{1/3} confirmed" fit would be unfalsifiable by
   construction. No queue change.

3. [interpretation caution] The model's micro-assumptions are conventions,
   not measurements: pressure uniform within a level and proportional to
   occupancy (Eq. 6, PDF p. 2), queue-front immobility and queue-rear
   mobility (Eq. 7, PDF p. 3). The same observable book admits many such
   micro-stories, so the convention-declaration discipline applies to any
   future pressure, urgency or queue-mobility feature: the unobservable
   being operationalized must be declared, per the level-versus-memory
   disambiguation (deep-read 59) and the spread-convention declaration rule
   (deep-read 56). Additionally, the framework solves only the advancing
   touch (no positive similarity solution for gamma < 0, PDF p. 4) and
   handles anisotropy only through boundary conditions, which the author
   concedes is "sometimes considered to be a problem" (PDF p. 3): nothing
   here may be cited for touch-retreat, withdrawal or compression-front
   anatomy in the L2 phase. No queue change.

4. [interpretation caution] The similarity far field decays like 1/s,
   formally implying infinite book volume, cut off only by real-life
   quantity discreteness (Eq. 18, PDF p. 4): a generative null or comparator
   built on this family carries a free volume-support truncation that
   materially changes deep-book marginals, and neither that truncation nor
   the 1/s tail is decided by anything observable. The queue-jump-diffusion
   generative-null pre-declaration (deep-read 81) and the impact-viability
   pre-declaration (deep-read 87) already require generative nulls to
   pre-declare their own parameterization before serving as refutation
   instruments; a transport-family null's support truncation belongs to that
   same declaration duty and needs no new rule. No queue change.

5. [reinforcing, no new item] The author's own applicability boundary is the
   honest one the programme demands of its own constructions: the model is
   "not intended to simulate a real world order book with all its
   complexities", is valid only "in a statistical ensemble sense" for the
   collective behaviour of market makers, and "it would be foolish to take a
   snapshot of any real world order book, feed it to our model as the
   initial condition, and expect a realistic prediction of the shape of the
   order book in the future" (PDF p. 6). The paper thus arrives
   pre-disclaimed against exactly the laundering move the programme's
   library rules forbid; its self-declared status is ammunition, and it is
   recorded as such. No queue change.

6. [source-quality note] Single practitioner author (fund manager at Pine
   Tree Funds, visiting senior research fellow at King's College London, PDF
   p. 1), arXiv v2 stamped 8 Dec 2020 over a 2019 v1, zero citations recorded
   at cataloguing, no peer-reviewed venue recorded, no empirics anywhere,
   and the text carries multiple uncorrected typographic slips ("cocnept",
   PDF p. 2; "assosi-acated", PDF p. 5; "releave" and "soluction", PDF p. 6)
   indicating light editing. Consistent with its score-21 tier placement as
   an ammunition-grade analytical toy from the practitioner literature. Read,
   graded, recorded at its grade.

## What this paper would have killed if we had done it wrong

If the programme had read this paper as market evidence, the kill would have
run through book-recovery features: a future C8 or C1-L2 resiliency-style
statistic measuring depth recovery after aggressive volume would have been
pre-armed with a "recovery follows t^{1/3}" prior lifted from the abstract,
and an estimator handed that prior would find the exponent, because the
family's clock constant absorbs all the freedom the data could offer (t ->
t/(theta*(beta+1)), Eq. 9, PDF p. 3) and the exponent itself is emitted by
determinism with no information content (finding 1). The Bechler-Ludkovski
resiliency read (deep-read 78, log ## 102) already recorded the measured
version of this trap, recovery shapes being clock artifacts; this paper
records the constructive version, a closed-form deterministic generator of
power-law recovery. The programme avoided the kill because the
deterministic-calendar null (deep-read 73) refuses deterministic generators
as refutation instruments without declaration, the primary-metric
pre-commitment (deep-read 55) forbids choosing the exponent test after
seeing the prior, and the laundering rule bans the exponent's entry into
the record in the first place. Had any of those three been missing, this
paper is a printed example of how a model constant becomes a market "law".

## Standing caveat

The model's applicability boundary, stated by the author himself: ensemble
sense only, never a snapshot-level predictor (PDF p. 6); continuum
approximation with fractional quantities unphysical and invoked only to cut
off the divergent far field (PDF p. 4); isotropy handled only in boundary
conditions and admitted as questionable (PDF p. 3); the retreating-touch
case unsolved (no positive similarity solution for gamma < 0, PDF p. 4);
infinite formal book volume in the similarity far field (Eq. 18, PDF p. 4);
convergence to the steady profile on time scales exceeding any practical
ones (PDF pp. 5-6); simulations initialised from the author's own
constructed profiles, not data (PDF pp. 5-6); and no stochastic term, no
costs and no venue anywhere. arXiv-version caution: v2 of 8 Dec 2020 with
no recorded journal counterpart — check for a published version before any
formal citation.
