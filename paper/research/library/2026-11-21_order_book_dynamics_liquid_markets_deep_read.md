# Deep-read session 81 — Order book dynamics in liquid markets: limit theorems and diffusion approximations

**Deep-read session 81** (null-time session 92; third read of the
score-23 tier). Rama Cont, Adrien de Larrard (Columbia University /
CNRS-Université Pierre et Marie Curie), "Order book dynamics in liquid
markets: limit theorems and diffusion approximations" (arXiv:1202.6412v1
[q-fin.TR], stamp 28 Feb 2012, 40 pp. in the extract). A limit-theorem
paper: the limit order book reduced to a piecewise-constant process on
(bid price, ask price, bid queue, ask queue) whose dynamics are driven by
the net order flow, and a functional central limit theorem (the heavy
traffic / diffusion limit) showing that, when order arrivals are
frequent and the order flow satisfies finite-second-moment and mixing
conditions, the rescaled queue process converges to an explicit
Markovian jump-diffusion in the positive orthant, from which the
price-change duration law and the next-tick probability follow in
closed form.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x6c29fa_order_book_dynamics_in_liquid_markets_limit_theore.txt,
~40 pp., page-marked). Next UNREAD triage-rank entry (score 23).

## The paper in one paragraph

The book is reduced to (sb, sa, qb, qa): bid/ask prices (multiples of
the tick) and the outstanding queue sizes at the best bid and ask
(PDF pp. 6-7), justified by the observation that most order flow and
most price impact concentrate at the best levels. When either queue is
depleted, the price moves by one tick and both queues are re-initialized
to new values drawn from sequences (Rk) after increases and (~Rk) after
decreases, which may be IID, pegged-order-dependent via
q_(τn) = g(q_(τn−), εn), or otherwise state-dependent (Def 1 and
Examples 1-2, PDF pp. 8-11); the model therefore needs the assumption,
empirically defended for 2008 US liquid equities, that the bid-ask
spread is one tick more than 98% of the time and that any wider spread
closes within milliseconds (Table 3, Fig 4, PDF pp. 7-8). Under
stationarity of the inter-event durations to rate λ, and a uniformly
mixing order-size array with vanishing first moment scaled to √n and
finite long-run variance (Assumptions 1-2, PDF pp. 19-20) — itself
defended against one day of Citigroup/GE/GM data: Pareto order-size
tails with index > 2 (Table 4, PDF p. 14), zero linear autocorrelation
of sizes and durations with dependence that lives in squared sizes and
inverse durations (Figs 6-9, PDF pp. 15-16) — the rescaled queue process
converges (Theorem 2, PDF p. 21) to a jump-diffusion: planar Brownian
motion with drift (λaVa, λbVb) and a covariance matrix built from the
order-size second moments and the cross-correlation ρ (eqs 13-14,
PDF p. 21), re-initialized at each boundary hit from declared
distributions F, ~F; the approximation is practical at a γ1 ~ 10-100 s
grain because the effective drift-to-fluctuation ratio is small (Figs
11-13, PDF pp. 17-20; Table 5 at 30 s: |μ| an order of magnitude below σ
for all three stocks, PDF p. 24). The price process then converges
(Proposition 1, PDF pp. 26-27) to the difference of the boundary
occupation times of the limiting queue process, and the paper derives a
closed-form conditional duration law whose tail index π/2α depends on ρ
(Proposition 2, PDF pp. 27-28) plus the Dirichlet solution and closed
forms for the probability that the next tick is up, pup(x, y), which in
balanced flow is a function of the queue-size ratio and ρ alone (Theorem
3 and eqs 33-34, PDF pp. 29-30). If order sizes lose their second
moment, the limit is a Lévy-driven, not diffusion-driven, regulated
process (Remark 1, PDF p. 23). All empirical anchors are three US
equities on one day (June 26, 2008).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [reinforcing, no new item] The reduced form is legally usable only
   under a spread-convention declaration. The entire one-dimensional
   price ladder with (qb, qa) state EXISTS only because the paper
   assumes the spread is one tick >98% of the time and re-closes in
   milliseconds (Table 3, Fig 4, PDF pp. 7-8) — a property of 2008 US
   liquid equities, not a property of BTCUSDT perp books, where
   multi-tick spreads persist long enough to be measured states rather
   than instantaneous transitions. An L2 reconstruction that borrows
   the (s, qb, qa) reduction without declaring its spread handling is
   exactly the defect the queued spread-convention declaration rule
   (deep-read session 56, null-time session 67) exists to catch: the
   zero-spread/single-price handling is a distinct configuration counted
   in the multiplicity ledger. No queue change; the queued rule carries
   the load, this paper supplies its mechanism.
2. [interpretation caution] In this model class market orders and
   cancellations are mathematically IDENTICAL: both enter the queue
   dynamics only through the same signed size V (PDF p. 7), and every
   downstream closed form (duration law, pup) is blind to which one
   depleted the queue. No C1-L2/C8-adjacent statistic built from
   best-queue net flow may attribute a depletion event to a
   cancellation-specific or taker-specific mechanism on this evidence;
   the passive-cancellation mechanism (the blocked C5 front) is
   structurally invisible at this grain, which reinforces why C5 sits
   behind L0 full-depth snapshots and not behind net-flow arithmetic.
   Reading discipline only; no queue change.
3. [source-quality note] The closed forms are regime- and venue-indexed:
   balanced flow (Va = Vb = 0) for the cleanest stated laws, ρ ≈ −0.7
   quoted "in practice" for finite duration moments (PDF p. 28), a
   three-stock one-day sample (Citi/GE/GM, June 26, 2008, a crisis-era
   tape) for every empirical magnitude, and the paper's own caveat that
   heavy-tailed order flows exit the diffusion regime entirely
   (Remark 1, PDF p. 23) and that heavy-traffic limits can fail to
   exist (PDF p. 5). Nothing in Props 2-3 or Tables 3-5 may enter the
   programme record as support for any claim (laundering ban); read,
   graded, recorded; no promotion.
4. [candidate sharpening, PENDING OWNER RATIFICATION] The
   queue-jump-diffusion generative-null pre-declaration. BEFORE the L0
   gate, any C1-L2/C8-adjacent spec that claims an anticipatory,
   depletion-side or queue-evacuation structure must pre-declare, as
   one of its admission nulls, a moment-matched queue-jump-diffusion
   null: the synthetic generator Theorem 2 + Definition 1 license —
   planar Brownian increments with drift (λaVa, λbVb), covariance built
   from the pre-declared flow moments and cross-correlation ρ (eqs
   13-14, 17-18, PDF pp. 21, 23), re-initialized at each boundary hit
   from the declared post-move depth distribution F (PDF pp. 9-11) —
   with ALL null parameters (arrival rates, first and second moments of
   order sizes, ρ, F, and the moment-existence check Assumption 2
   requires, since the diffusion limit fails without finite second
   moments, PDF pp. 19-20, 23) frozen BEFORE the data, and the claimed
   structure shown to survive that null in the subsample where its
   information lives. The paper earns the requirement with a specific
   measured mechanism: in a liquid book the queue is
   FLUCTUATION-DOMINATED at intraday scales — the drift-to-fluctuation
   ratio √n·V̄/sd is small across Dow-Jones names (Fig 11, PDF p. 18),
   batch-size variance scales linearly as Assumption 2 demands (Fig 13,
   PDF p. 20), and at a 30 s grain the mean net queue change is roughly
   an order of magnitude smaller than its standard deviation (Table 5,
   PDF p. 24) — so an apparent depletion-side "anticipation" drift could
   be produced by pure diffusion fluctuations with zero information,
   and would survive any null whose fluctuation scale is weaker than
   the measured regime. Harder-to-pass because a queue-mechanic claim
   that beats only a static-marginal or weaker-variance null now fails
   by rule instead of surviving as a find; tightens the two-null
   admission family (log ## 17), joining the Gould-Bonart Eq.-7
   comparator, the tautology-controlled OFI benchmark, the
   sign-persistence admission null and the deterministic-calendar null
   with the null class specific to the queue mechanic, and tightens the
   dynamics-identification rule for generative nulls (null-time session
   58) by naming a flow-dynamics null whose parameters carry that
   rule's freeze discipline. This note is the full draft; the
   killed-if-wrong counterfactual: had the deterministic-calendar null
   (queue #40) or any two-null admission case closed without this null
   in the set, a fluctuation artifact of exactly the regime this paper
   measures could pass an admission gate it should fail.
5. [reinforcing, no new item] The claim that finer time-scale structure
   "averages out to a diffusion" at 10-100 s horizons (PDF pp. 17-19)
   is generated inside the paper's own assumption set and sample; it is
   ammunition, not evidence: it motivates C1-L2's premise (if daily
   grain cannot see it, the L2 tape is where compression structure
   would live) but supports nothing. It also shifts with the venue: a
   crypto perp tape with heavier order-size tails exits the diffusion
   regime (Remark 1, PDF p. 23), which is why the sharpening above
   freezes the moment-existence check as part of the null
   configuration. Nothing measured, nothing armed.

## What this paper would have killed if we had done it wrong

If the programme had imported eq (33)/(34) (pup) or the Proposition 2
duration law as the expected-behavior model inside a C1-L2 spec —
calibrating a depletion-timing or imbalance feature against a β/ρ
formula — the feature would silently inherit the one-tick
instantaneous-spread-closure assumption, the market-order/cancellation
identity and the balanced-flow conditions of a one-day 2008 US-equities
tape (PDF pp. 7-9, 19, 28-30): a BTCUSDT perp L2 "confirmation" would
be manufactured by construction inside the wrong model class, exactly
the laundering pattern the library ban exists to kill. And without the
fluctuation-dominance evidence now on record (Figs 11-13, Table 5), the
programme could have drafted an admission gate with a null whose
variance scale is weaker than the measured regime, and a
diffusion-fluctuation artifact would have walked through it as an
anticipatory find. The one-question rule plus the standing
two-null discipline kept both failure paths closed; the sharpening adds
the specific null class this paper proves is the default regime of a
liquid book.

## Standing caveat

arXiv v1, 28 Feb 2012 (revised from earlier drafts); the published
version (Cont & de Larrard, SIAM Journal on Financial Mathematics,
2013) supersedes it and must be checked before any formal citation.
Data: Citigroup, General Electric and General Motors, June 26, 2008
only, US equities, a crisis-period tape; no crypto, no perpetual
futures, no venues with persistent multi-tick spreads; the millisecond
spread-closure and one-tick-spread observations are venue- and
period-specific; the diffusion regime is empirical and fails for
heavy-tailed order flows (Remark 1, PDF p. 23) and heavy-traffic limits
may fail to exist (Dai-Nguyen, cited PDF p. 5). Regardless, no claim in
this paper can serve as support for any programme claim.
