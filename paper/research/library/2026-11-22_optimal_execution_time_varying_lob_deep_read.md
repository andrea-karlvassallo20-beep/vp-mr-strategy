# Deep-read session 87 — Optimal execution and price manipulations in time-varying limit order books (Alfonsi & Infante Acevedo, 2012)

**Library deep-read session 87 (null-time session 97, fifth and last of the
score-22 tier).** Aurélien Alfonsi and José Infante Acevedo, "Optimal
execution and price manipulations in time-varying limit order books",
arXiv:1204.2736v1 [q-fin.TR] (Université Paris-Est, CERMICS; header dated
August 14, 2018). One clause on what the paper is: a pure-theory extension of
the Alfonsi-Fruth-Schied general-shape limit-order-book impact model to a
time-varying LOB depth, solving the optimal execution problem in discrete and
continuous time and deriving necessary and sufficient conditions on the
time-varying resilience and depth under which the model admits price
manipulation strategies (PMS) or transaction-triggered price manipulations
(TTPM).

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x750e2f_optimal_execution_and_price_manipulations_in_time_.txt,
~25 pp., page-marked). Next UNREAD triage-rank entry (score 22).

## The paper in one paragraph

The model extends Alfonsi-Fruth-Schied: a martingale unaffected price S0, a
price impact D_t and a volume impact E_t linked through a shape function f
and a time-varying depth λ(t) by E_t = λ(t)F(D_t) (Eqs. 1-5, PDF p. 3), with
the volume impact decaying at a time-varying deterministic resilience ρ_t
(Def. 1.1, PDF p. 3, "model V") or the price impact itself decaying ("model
P", Eq. 7, PDF p. 3). A large trader liquidates a position with market orders
only; the expected cost splits into a martingale term plus a deterministic
function of the trade schedule (Eq. 13, PDF p. 6). For a block-shaped LOB the
cost is a quadratic form (Eqs. 16, 24, PDF pp. 6, 8) and the paper gives
explicit optimal strategies on a time grid (Thms. 2.1-2.2, PDF pp. 7, 9) and
in continuous time (PDF pp. 7-8, 9-10). The viability results are exact:
model V is free of Huberman-Stanzl price manipulation if and only if
2ρ_t + η_t ≥ 0 everywhere (Cor. 2.1, PDF p. 7), model P iff
2ρ_t − η_t ≥ 0 (Cor. 2.3, PDF p. 10), with negative-cost round trips
constructed explicitly whenever the inequality fails (Eqs. 20, PDF p. 7; PDF
pp. 12, 15), and weaker sign-derivative conditions excluding TTPM (Cor. 2.2,
Eq. 22, PDF p. 8; Cor. 2.3, Eq. 30, PDF p. 10; general forms Eqs. 29-30,
PDF p. 10). For general shapes, sufficient (not necessary-and-sufficient)
versions follow from Assumption 2.1/2.2 on f and proofs by Lagrange
multipliers and verification arguments (Thms. 2.3-2.6, PDF pp. 11-14; proofs
PDF pp. 15-24), with the power-law shape f(x) = |x|^γ again giving an exact
iff (Cors. 2.5, 2.7, PDF pp. 12, 15). Two payoffs for market makers
(PDF pp. 7, 10, 19-20): in model V adding limit orders never creates a PMS
while cancelling can, and the optimal strategy under a sinusoidal depth
λ(t) = 4 + cos(2πt) can roughly triple the traded volume (buy 50 by first
buying ~95 and selling ~45, Fig. 1, PDF pp. 8-9). There are no empirics
anywhere in the paper; every figure is a model illustration at chosen
parameters.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [reinforcing, no new item] Every result in the paper is model-relative
   viability theory under deterministic resilience and depth: the unaffected
   price is an exogenous martingale (PDF p. 3), λ, ρ are deterministic C1/C2
   functions (PDF p. 3), there are no data, no costs, no spread, no
   estimation, and the illustrative depth λ(t) = 4 + cos(2πt) is a
   constructed calendar (PDF pp. 8-9). A "no manipulation" theorem here is a
   statement about the internal consistency of an impact model's parameter
   region, not a claim about any market; magnitudes are banned from the
   record under the laundering rule, and the deterministic-calendar shape is
   exactly the artifact family the queued deterministic-calendar null
   (deep-read 73) exists to block on our side. No queue change.

2. [candidate sharpening, PENDING OWNER RATIFICATION] The paper proves, in
   print, that a canonical published impact family is internally
   arbitrageable in computable parameter regions: round trips of negative
   expected cost exist in model V exactly when 2ρ_t + η_t < 0 somewhere
   (Cor. 2.1 with the construction at Eq. 20, PDF p. 7) and in model P
   exactly when 2ρ_t − η_t < 0 (Cor. 2.3, PDF p. 10), and even a PMS-free
   book can admit TTPM whose optimal strategy triples the traded volume
   (Fig. 1, PDF pp. 8-9: buy 50 via buying ~95 and selling ~45), i.e. a
   simulator layer built on this family emits either arbitrage-shaped or
   sign-alternating volume artifacts with no visible marginal signature.
   None of the existing queued rules catches this: the dynamics-identification
   rule for generative nulls (null-time session 58) checks marginal/flow
   statistics, and the queue-jump-diffusion generative-null pre-declaration
   (deep-read 81) pre-declares its flow dynamics but not the viability of any
   transient-impact/reversion layer a null or placebo might carry. Proposed
   amendment, harder-to-pass only, tightening the dynamics-identification
   rule for generative nulls: any generative null, placebo, comparator or
   simulator whose flow dynamics include a transient-impact/reversion
   (resilience) layer must, at pre-declaration and before it may serve as a
   refutation instrument, state the no-PMS/no-TTPM condition of its own
   impact parameterization (from this paper's condition family or its own
   derivation) and record that the armed configuration satisfies it; a null
   whose impact layer can price a negative-cost round trip, or whose optimal
   behaviour embeds TTPM, is inadmissible as a null, because it refutes
   against a benchmark that embeds arbitrage. No kill line touched.

3. [interpretation caution] The market-maker reading (adding limit orders
   never creates a PMS in model V, cancelling can; cancelling among the best
   offers or piling orders at existing prices can in model P; PDF pp. 7, 10,
   19-20) is a qualitative model-world statement about how depth dynamics
   create manipulation-shaped opportunities under a deterministic
   resilience. It must not be cited as support for any read of
   passive-cancel behaviour in the C1-L2 phase's compression/passive-
   withdrawal mechanisms, nor for the manipulation/spoofing fronts: the
   paper's cancels move a deterministic ρ_t or η_t, not a queue, and the
   two-sided two-tick book is collapsed to a one-sided coincidence case
   (Remark 1.2, PDF p. 5). Ammunition at most. No queue change.

4. [interpretation caution] The viability boundary is time-varying and
   regime-bound: every condition is pointwise in t over ρ_t and η_t (Eqs. 19,
   22, 29, 30, PDF pp. 7, 8, 10), so a book whose resilience/depth regime
   crosses 2ρ ± η = 0 flips its internal arbitrageability with the regime.
   Any future viability-style or stability-style feature must therefore
   carry pre-declared regime windows, with no silent regime blending; the
   queued self-excitation regime-window pre-declaration and control-arm
   discipline already forbid the silent version, and this paper shows the
   boundary of the quantity itself moves with the calendar of the depth. No
   queue change.

5. [reinforcing, no new item] The two reversion conventions (volume-impact
   reversion, "model V", versus price-impact reversion, "model P", Def. 1.1,
   PDF p. 3) are different financial stories that coincide mathematically
   when λ is constant (PDF p. 8) and for power-law shapes differ by a
   reparametrization ρ̃_t = ρ_t(1+γ) − η_t (PDF p. 15), yet diverge under
   time-varying depth, with opposite monotonicity assumptions on f between
   the two (Assumptions 2.1 and 2.2, PDF pp. 10, 13). The same book data
   therefore admits two different "what decays" stories whose distinction is
   a convention declaration, not a measurement: the same disambiguation
   family as the level-versus-memory rule (deep-read 59) and the
   spread-convention declaration rule (deep-read 56). Any future
   reversion-decay estimate must declare which object it claims decays.
   No queue change.

6. [source-quality note] arXiv v1, submitted April 2012, header dated August
   14, 2018; no journal counterpart recorded in the index at cataloguing
   (zero citations, topic arxiv-manip); the continuous-time optimality for
   the block case is credited to the contemporaneous Fruth-Schöneborn-Urusov
   working paper (PDF pp. 2, 7-8, 10), so priority overlaps; the model
   assumes an infinite-depth book (Eq. 4, PDF p. 3), market orders only
   (PDF p. 3), and no empirics exist at all. Read, graded, recorded at its
   grade: an ammunition-grade theory paper whose programme value is the
   viability mechanism in finding 2 and the convention disambiguation in
   finding 5.

## What this paper would have killed if we had done it wrong

If the programme ever armed a generative null, placebo or comparator whose
flow dynamics include a transient-impact/reversion layer, and used it as a
refutation instrument without a viability check, this paper is the printed
constructive proof that the null could embed negative-cost round trips
(whenever 2ρ ± η < 0 on any subinterval, Cors. 2.1/2.3, PDF pp. 7, 10) or
TTPM-shaped optimal behaviour (Fig. 1, PDF pp. 8-9) — an internally
arbitrageable benchmark against which any feature's verdict, in either
direction, is a statement about the null's artifact, not about the market.
The dynamics-identification rule already refuses marginal-only nulls, but it
says nothing about the impact layer's internal viability, so the artifact
class would have survived it. The counterfactual kill: an L2 claim
"refuted" by a null that can price a round trip at negative expected cost,
or "confirmed" against one whose optimal behaviour sign-alternates volume by
construction; the proposed pre-declaration in finding 2 exists to make that
null inadmissible before any data is touched.

## Standing caveat

The paper's own applicability boundary: the book has infinite depth on both
sides of an exogenous martingale price (Eq. 4, PDF p. 3); the large trader
uses market orders only and never limits (PDF p. 3); the two-sided model
reduces to the one-sided analysis only when trades do not alternate signs
(Remark 1.2, PDF p. 5); λ, ρ are deterministic and smooth, excluding
endogenous or stochastic liquidity; the general-shape results are sufficient
conditions under opposite monotonicity assumptions on f in the two models
(Assumptions 2.1/2.2, PDF pp. 10, 13), with exact iff statements only for
block and power-law shapes; and there are no empirical results whatsoever.
arXiv-version caution: v1 with an internal header date of August 2018 and
overlapping priority with Fruth-Schöneborn-Urusov [9] — check for a published
counterpart before any formal citation.
