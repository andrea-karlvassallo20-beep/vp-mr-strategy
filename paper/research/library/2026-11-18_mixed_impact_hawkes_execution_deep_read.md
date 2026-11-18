# Deep-read session 24: Alfonsi and Blanc, "Dynamic optimal execution in a mixed-market-impact Hawkes price model"

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/x7c5b08_dynamic_optimal_execution_in_a_mixed_market_impact.txt,
~27 pp., page-marked). Next UNREAD triage-rank entry (score 34, x7c5b08).

## The paper in one paragraph

A theory paper (Alfonsi and Blanc, arXiv:1404.0648v2, CERMICS ENPC): the
Obizhaeva-Wang execution model (block limit order book, linear mixed
impact - a proportion nu permanent, 1-nu transient with exponential
resilience speed rho - plus quadratic execution costs) is generalized so
that the other traders' signed market-order volume follows a bivariate
marked Hawkes process with exponential kernel beta, self-excitation
iota_s and cross-excitation iota_c (PDF pp. 3, 7). The optimal execution
strategy is solved in closed form as the Obizhaeva-Wang schedule plus a
trend term and a dynamic term that reacts jump-for-jump to other traders'
orders, the reaction flipping from opposite-direction under resilience
dominance to same-direction under self-excitation dominance (PDF
pp. 9-11). No Price Manipulation Strategy exists if and only if the
price is a martingale with the strategic trader absent (Theorem 2.1,
PDF p. 5); within the model this holds exactly when beta equals rho,
alpha equals (1-nu)rho on the support, and the book starts in the
associated steady state (Proposition 5.1, PDF p. 13) - the
self-excitation of the flow exactly compensating the resilience of the
market makers, an echo of the propagator balance of Bouchaud et al.
Under purely Poisson (exogenous) order flow, profitable round-trip
manipulations are robust and implementable without knowing any model
parameter (Proposition 5.2, PDF pp. 15-16). No data is fitted anywhere;
the authors flag every idealization against the empirical literature and
leave estimation to future work (PDF pp. 2, 7, 9, 14).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Default grade. The
paper is a closed-form execution theory under idealized impact; against
the ONE question it supplies worked exhibits for standing rules and one
class of reading discipline, nothing that tightens a future test.

1. [reinforcing, no new item] The model's no-arbitrage equilibrium pins
   the flow's endogeneity ratio to the price model's transient-impact
   share: with no cross-excitation, the Hawkes norm iota_s/beta must
   equal 1-nu, and cross-excitation must stay small (the stationarity
   condition becomes 2*iota_c < nu*rho, PDF p. 14). The lesson for the
   record: an "endogeneity" or branching reading is not a free-standing
   market quantity - inside one coherent model class its equilibrium
   value is a function of the impact decomposition you assumed, and
   there is no universal near-critical level implied by stability or by
   efficiency. This is a worked exhibit for the estimator-mode register
   and the uncertainty-band-not-point-estimate rule already standing in
   the queue from the Hardiman-Bouchaud reads: a fitted branching value
   acquires meaning only relative to a declared model, kernel family,
   and impact decomposition. It licenses nothing new.

2. [reinforcing, no new item] Stability and the absence of free profits
   are the same conditions in this model class: no PMS if and only if
   the price is a martingale when the strategic trader is absent
   (Theorem 2.1, PDF p. 5), and no weak PMS (no profitable instant
   reaction to others' orders) if and only if the same parameter
   identities hold (Proposition 5.1 and Corollary 5.1, PDF pp. 13-15).
   The authors themselves call the exact calibration of such parameters
   "miraculous" and give three reasons fitted parameters should not be
   expected to satisfy them, including that fitting a PMS-free market
   has no guarantee of yielding a PMS-free model (PDF p. 14). Two
   disciplines are reinforced: knife-edge equilibria are model objects,
   never market facts, and any future statement that a measured
   configuration is "stable" or "manipulable" is model-coupled and
   carries the model's falsified idealizations with it - the
   mechanism-level-transfer-only rule.

3. [reinforcing, no new item] A deliberately misspecified flow does not
   produce neutral behaviour but structure: with purely Poisson
   arrivals, the round trip that trades a fixed opposite fraction of
   every incoming order is profitable on average for any fraction
   below one, without knowing the impact parameters, the resilience, or
   the intensities (Proposition 5.2, PDF pp. 15-16). Read as a worked
   exhibit for the null discipline the queue already carries: what a
   null arm returns depends on what the null destroys, so the null must
   be honest about the components it carries - the same class of lesson
   as the U-shape seasonality exhibit from the compound-Hawkes read and
   the publisher-clock exhibit from the CME feed read. It is a
   model-internal identity, not a market claim, and it licenses nothing
   new; the deterministic-clock null arm's enumeration is untouched.

4. [cost-survival ammunition] If a K7-style cost-survival or
   execution-assumption layer is ever built, this paper declares the
   assumptions it must not inherit: block book, linear impact,
   exponential transient decay, and exponential Hawkes kernels are each
   flagged by the authors themselves as contrary to empirical facts
   (PDF pp. 2, 7, 9), and the closed-form strategy is qualitative only
   in their own reading. The layer, if it ever exists, must declare its
   impact functional form and decay family explicitly and carry the
   falsification record of the linear-exponential pair. Nothing in this
   paper is operationalized now; the execution content is recorded as
   engineering context, never as programme input, and nothing trades
   live.

5. [source-quality note] Two authors, CERMICS (ENPC-INRIA), with funding
   from the Fondation Natixis and the Chaire Risques Financiers; the
   shelf extract is arXiv v2 stamped June 2015 while the title page
   carries a later date line (October 2018), indicating a post-stamp
   author revision; the index records zero citations despite the 2014
   vintage; no published version is on the shelf. Check the published
   version before any formal citation. The paper confronts no market
   data: the estimation is "left for future research" by the authors'
   own statement (PDF p. 7), and the strategic trader's own orders are
   assumed not to excite the flow of others, an approximation justified
   by the splitting-dominance argument citing Toth et al. (PDF p. 8) but
   never tested here.

## What this paper would have killed if we had done it wrong

If the programme had treated the MIHM equilibrium identities (beta equals
rho, alpha equals (1-nu)rho) as a market law - measuring the Hawkes
decay and the price decay and declaring the market in or out of
equilibrium, or reading any measured branching value as "the" endogenous
share because one model class pins it to the transient impact share - it
would have laundered a knife-edge identity of an idealized model into a
claim about the BTCUSDT tape. Every load-bearing assumption in the chain
is flagged by the paper's own authors: linear impact, exponential
resilience, block book, exponential kernel, no excitation from the
strategic trader, and zero data confrontation. The standing discipline
blocked each route in advance: the library is ammunition, not
evidence; nothing from the shelf enters a spec without its own
pre-registration; branching readings carry the estimator-mode register;
and knife-edge equilibria recorded as model objects never leave the note.

## Standing caveat

The paper is single-asset, closed-form theory with no calibration, no
data, and idealizations its own authors list against the empirical
literature; the cross-excitation/splitting idealization would matter
most directly to the programme (whose compression question concerns how
participants' reactions to flow build over hours). Any transfer to C8 or
C1-L2 contexts is mechanism-level only and may carry no parameter value,
equilibrium identity, or strategy formula. arXiv v2 with an internally
later revision date: check the published version before formal
citation. Laundering directions: INTO - no MIHM condition, cost
parameter, or strategy formula enters any spec, default, calibration,
or cost assumption, and the equilibrium identities may not become
programme hypotheses without a fresh pre-registration through the
owner; OUT - no reading that a measured branching value should sit near
any particular level because this model's equilibrium pins it, no
"stable versus manipulable" transfer to any real tape, and no
operationalization of the reaction strategies under any circumstances.
