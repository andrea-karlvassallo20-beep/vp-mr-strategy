# Deep-read session 56 — Fruth, Schöneborn, Urusov, "Optimal trade execution and price manipulation in order books with time-varying liquidity"

- Authors: Antje Fruth (TU Berlin), Torsten Schöneborn (Deutsche Bank AG, London), Mikhail Urusov (Ulm University)
- Full title: "Optimal trade execution and price manipulation in order books
  with time-varying liquidity"
- Venue: arXiv:1109.2631v1 [q-fin.TR], submitted September 2011 (extract
  title page carries the date line "October 8, 2018" — see the
  source-quality note below)
- What it is: a pure-theory optimal-execution paper on an
  Obizhaeva–Wang-type block-shaped limit order book whose depth and
  resilience are deterministically time-dependent, proving that a model
  with a dynamic, trading-dependent spread is free of both classical and
  transaction-triggered price manipulation while the canonical zero-spread
  variant admits both, with exact characterizations of when.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x95643a_optimal_trade_execution_and_price_manipulation_in_.txt,
~42 pp., page-marked). Next UNREAD triage-rank entry (score 28).

## The paper in one paragraph

The paper extends the Obizhaeva–Wang (2006) block-shaped limit order book
to independently time-dependent depth q_t and resilience ρ_t
(K_t = 1/q_t − γ, deterministic, PDF pp. 3–5), and solves the risk-neutral
cost-minimizing liquidation problem. In the "dynamic spread" model, where
the spread widens with the large trader's own market orders and the two
sides of the book carry separate deviation processes D_t, E_t (PDF p. 5,
eqs. (1)–(2)), only the temporary-impact deviation matters for strategy
choice — the unaffected-price martingale component and the permanent
impact contribute terms invariant across strategies (Proposition 3.3, PDF
pp. 7–8) — and no round trip or intermediate-sale strategy can beat a pure
single-sided program (Proposition 3.4, PDF pp. 8–10). The value function
has a wait-region/buy-region (WR-BR) structure: a time-dependent barrier
c(t) in the ratio of remaining shares to price deviation separates "trade
to the barrier" from "wait for resilience"; this is proved for discrete
time by backward induction with a piecewise-quadratic value function
(Theorem 6.1, PDF pp. 18–19) and for continuous time under continuous K
(Theorem 7.7, PDF pp. 26–27), and the barrier can be infinite — there are
liquidity paths on which the optimum is to not trade at all until the
terminal instant (Propositions 5.8–5.9, PDF pp. 17–18). The sharp result
for model discipline is Section 8: in the zero-spread variant (one price
for buys and sells, symmetric impact, Assumption 8.1, PDF pp. 27–28), a
known nonzero initial deviation admits a profitable round trip by
construction (Remark 8.2, PDF p. 29); if liquidity rises faster than
resilience can restore it (K'_t + 2ρ_t K_t < 0 at a single t), a
pump-and-dump round trip is strictly profitable, the cost infimum is −∞,
and no optimal strategy exists (Proposition 8.3, PDF pp. 29–30); under
the opposite condition, transaction-triggered price manipulation occurs
exactly when f_0 < 0 or f'_t + ρ_t f_t < 0 somewhere (Theorem 8.4 and
Corollary 8.5, PDF pp. 30–31, f in eq. (34)). Closed-form strategies and
barriers follow for constant, exponential and linear K (Examples
9.5–9.7, PDF pp. 37–39), recovering the Obizhaeva–Wang "bathtub"
strategy as the constant-K special case (PDF p. 37).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The zero-spread
   convention mechanically manufactures round-trip profitability. In the
   zero-spread model class that a single-price or mid-only book
   reconstruction implicitly instantiates, Remark 8.2 (PDF p. 29) shows a
   known nonzero deviation direction admits a profitable round trip by
   construction, and Proposition 8.3 (PDF pp. 29–30) shows a single point
   where K' + 2ρK < 0 makes pump-and-dump strictly profitable with the
   cost infimum at −∞ — no self-excitation, no information asymmetry, no
   microstructure signal required: the "anticipatory" structure is a
   property of the convention. Proposed rule (the spread-convention
   declaration rule): any book reconstruction, generative null, or
   flow-measurement input used in a C1-L2/C8-adjacent computation must
   pre-declare its spread convention; a zero-spread / single-price /
   mid-only handling is a distinct configuration counted in the
   multiplicity ledger, and any apparent anticipatory, reversal, or
   round-trip-type structure first observed under it must be shown to
   survive a dynamic (trading-dependent, two-sided) spread handling
   before it may enter any spec as support. It tightens the existing
   reconstruction-admissibility family (the queued volume-conservation
   admissibility rule and event-grain OFI accumulation rule) by adding a
   fourth declaration axis the reconstructions must carry, and it is
   harder to pass: a class of cheap single-price reconstructions becomes
   inadmissible as evidence without an additional robustness arm. PENDING
   OWNER RATIFICATION; nothing armed.
2. [reinforcing, no new item] Deterministic time-variation of liquidity
   alone reshapes optimal schedules and can shut trading off entirely
   without any self-excitation: infinite barriers arise whenever
   illiquidity K falls toward the future faster than resilience restores
   it (Propositions 5.8–5.9, PDF pp. 17–18), and the barrier need not be
   monotone in time (Figure 4, PDF pp. 22–23). Second-market support for
   the already-queued deterministic-clock null arm and the
   release-calendar lead component: calendar-locked liquidity seasonality
   can produce temporal structure that a clock-blind trigger read would
   attribute to endogenous dynamics. No queue change.
3. [interpretation caution] Proposition 3.3 (PDF pp. 7–8): in this model
   class the unaffected-price martingale contribution and the permanent
   impact are strategy-invariant, so all strategy-relevant signal lives
   in the temporary-impact deviation process D and its resilience path.
   Reading discipline for future generative-null validation: agreement
   of prices (or of event counts) between a reconstruction and its null
   does not validate the impact dynamics; the null must match the
   deviation/resilience paths — the same shape as the queued
   dynamics-identification rule's duration-tail requirement. No queue
   change.
4. [cost-survival ammunition] The paper supplies closed-form optimal
   costs and strategies under deterministic time-varying liquidity
   (Theorem 8.4, eq. (37), PDF p. 30; the barrier of Proposition 9.1, PDF
   p. 35; the bathtub recovery of Example 9.5, PDF p. 37), which is
   exactly the machinery a future K7-style cost-survival layer would
   need — declaring the assumptions that layer must carry: block-shaped
   book, exponential resilience, deterministic depth and resilience,
   risk-neutral single large trader, market orders only (PDF pp. 3–7).
   Ammunition only; nothing operationalized, nothing trades live.
5. [source-quality note] Single arXiv v1 preprint; pure theory, zero
   empirical estimation, no data, no code; the submitted v1 (September
   2011) carrying an "October 8, 2018" title-page date line in the
   acquired extract is a version anomaly to be checked before formal
   citation; one author affiliated with Deutsche Bank AG at time of
   writing. Check the published version before formal citation outside
   this note; library invariant applies throughout.

## What this paper would have killed if we had done it wrong

The zero-spread laundering death: reading anticipatory or reversal
structure out of a single-price / mid-only reconstruction of the book and
booking it as a compression-trigger interaction, when this paper proves
that conventions of exactly that shape mechanically admit profitable
round trips whenever the deviation direction is known (Remark 8.2, PDF
p. 29) — a model artifact that prices alone cannot distinguish from an
edge. Pre-empted by the spread-convention declaration rule queued this
session plus the standing reconstruction-admissibility discipline.
Alongside it, the calendar death: attributing deterministic
time-of-day liquidity structure to endogenous self-excitation; pre-empted
by the already-queued deterministic-clock null arm and the primary-metric
pre-commitment. Neither survival implies any claim about C1-L2 or C8;
their kill lines are unchanged.

## Standing caveat

All results live inside a block-shaped order book with exponential
resilience, deterministic (non-stochastic) depth and resilience, one
risk-neutral large trader, market orders only, and the specific
integration conventions of the paper (PDF pp. 3–7); the manipulation
characterizations of Section 8 are statements about the zero-spread model
class, not market observations. This is an arXiv v1 preprint of a 2011
submission; the published version should be checked before any formal
citation outside this note. Nothing here is programme evidence; under the
library invariant it is ammunition, not support.
