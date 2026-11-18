# Library deep-read session 25 — Barzykin, Boyce, Neuman & Tuschmann,
# "Optimal Execution with Passive Market Impact"
# (arXiv:2607.28323v1, 2026; HSBC and Imperial College London; a
# mesoscopic model of passive impact with explicit optimal quotes)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x28ad86_optimal_execution_with_passive_market_impact.txt`,
~31 pp., page-marked). Next UNREAD triage-rank entry (score 33;
verified unread by the read-slug mapping; the sibling of session
24's Ouazzani Chahdi et al. framework — its authors are explicit
that [34] is "the closest theoretical antecedent," PDF p. 2). Note:
first author is the same Barzykin whose HSBC industry read closed
session 15 — the industry's-exogenous-absorption-warning line
continues.

## The paper in one paragraph

The authors build a MESOSCOPIC optimal-execution model — meso-
scopic because it deliberately does not model individual child
orders, cancellations, or venue mechanics: a passive fill "is
typically achieved through a chain of quote submissions,
cancellations, repos, venue choices, and quote-distance
adjustments," and the economically relevant impact is the impact
of that tactical chain, not of an isolated resting order (PDF
pp. 2-3). Two empirical observables are combined: the
Avellaneda-Stoikov exponential fill intensity lambda*e^{-k*delta}
in the distance delta from the midprice, and the
Cont-Kukanov-Stoikov linear short-horizon response of price
changes to order flow imbalance (via per-level MLOFI coefficients
whose impact beta(delta) decays at rate l in delta), yielding a
reduced-form permanent passive impact rate eta*e^{-m*delta} with
m = k + l (PDF pp. 4-5, eqs. 2.6-2.8). For the equal-decay case
m = k the optimal liquidation quote is EXPLICIT (Theorem 3.1, a
bidiagonal-matrix system); NASDAQ estimates give l << k so
m ~ k for equities, while LSEG FX (conflated 5 ms snapshots,
synthetic eligibility-proxied fills, 10-second buckets) shows a
visible gap, m != k, motivating a Lambert-W semi-explicit solution
for distinct decay rates (Theorem 6.1, PDF pp. 7, 16-18, Tables
4-5). Simulation: stronger passive impact eta makes the optimal
quote DEEPER — the trader trades fill probability for impact
control, liquidating less, slower, but without worse implementation
shortfall (PDF pp. 9-11, Figure 2, Table 3).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[interpretation caution] A passive fill in recorded data is
   the ENDPOINT of an unseen tactical chain, not an order that
   "rested and got hit."** Remark 2.1 makes the point
   constructively: maintaining a quote at distance delta means
   repeated cancel-and-repost attempts, geometrically many more
   submissions the deeper the quote, whose continuous limit IS the
   exponential fill intensity (PDF p. 5, eq. 2.9). For the L2
   feature layer: a passive fill event observed in the gated
   BTCUSDT data underdetermines the strategy that produced it —
   re-post frequency, distance adjustments, and cancellation
   behavior are all upstream of the visible fill, and any
   feature treating fills as samples from a single resting
   order's lifetime mismeasures its own input. This is a new
   instance (the tactical-chain face) of the depth-measurement
   cautions already carried in C5's family language; the
   existing discipline covers it, and the C8/L2 specs already
   require construction declarations, so nothing is queued.

2. **[reinforcing, no new item] Distance is an informative proxy
   only in the right tick geometry — the estimator-mode rule gets
   its own back-from-the-paper example.** The authors find the
   MLOFI impact decay estimates for LARGE-tick stocks "should be
   interpreted with particular caution": impact may depend on the
   VOLUME QUEUED AHEAD rather than distance, and the coarse price
   grid prevents distance from substituting for queue volume (PDF
   p. 15). This is the mirror image of session 21 (where distance
   was essential because spoofers exploit small-tick continuity)
   and session 23 (where the construction triple decided the
   statistic): the same covariate changes information content
   with the venue's tick geometry. Continue: any distance-based
   reading on the program's small-tick venue declares its tick
   geometry; nothing new queued — the estimator-mode rule (session
   11) already forces the declaration.

3. **[reinforcing, no new item] The m ~ k coincidence is an
   empirical, asset-class-, and construction-specific finding —
   not a law.** The equities near-equality of impact decay and
   fill-intensity decay justifies the closed-form case, but FX
   breaks it visibly, and the authors themselves flag their FX
   estimates as "a public-data, venue-level result" from conflated
   snapshots with SYNTHESTIC passive fills proxied by next-bucket
   aggressor trades — public venue data "captures only part of
   the total FX liquidity and information set" (PDF pp. 16-17).
   Two reinforcements: (a) the construction triple again — the
   fitted number is a function of conflated-cadence, bucket-size,
   and proxy-fill choices, quantified across five currency pairs
   (Table 5); (b) the venue-freeze warrant (session 14): a fitted
   coincidence on one venue family licenses nothing on another;
   the paper's own response (a distinct-decay extension with
   Lambert-W) is the epistemically correct one.

4. **[cost-survival ammunition] Impact feeds back into the
   agent's own quoting — static cost schedules misprice tactical
   execution.** The central execution-theoretic result: under
   stronger passive impact, the optimal policy quotes DEEPER,
   accepting fewer and slower fills to control accumulated impact,
   with implementation shortfall roughly unchanged (PDF pp. 9-11,
   Figure 2, Table 3). If a K7-style cost-survival layer is ever
   ratified, its execution-cost arithmetic must model the
   feedback of impact onto one's own subsequent quoting (the
   session-24 no-relaxation schedule plus this paper's tactical
   response), or it will price a strategy the optimal policy
   would not trade. Declared as ammunition only; the program never
   trades live; the explicit-solution machinery is not
   operationalized.

5. **[source-quality note] The simulation parameters are
   illustrative, and the FX proxy-fill estimator is a construction
   to cite, not import.** The Monte Carlo runs use a single
   hand-set parameter table (Table 1), and the FX fill estimates
   are exposure-style SYNTHETIC fills from public quote and trade
   data rather than bank-level execution records (PDF pp. 8-9,
   15-16). arXiv v1 (July 2026), no published version located at
   read time — check before formal citation. Nothing here
   weakens the paper; the estimates are recorded as
   construction-specific demonstrations of the method, not as
   market facts about any venue the program touches.

## What this paper would have killed if we had done it wrong

If the L2 feature layer had ever treated passive fills as samples
from a single order's resting lifetime, the underlying
cancel-and-repost chains would have made the fill statistics of
different distance cohorts incomparable without any visible
distortion — the tactical-chain structure lives upstream of every
observable the features see. And if any future cost or viability
arithmetic had assumed static execution schedules under passive
impact, the optimal-quoting result says the schedules themselves
move in response to the impact — an internal feedback a static
schedule cannot see, mispricing its own policy. The program's
construction-declaration discipline and the never-trade-live rule
predate this read; the paper reinforces both without changing
either.

## Standing caveat

Mesoscopic by construction: no order-book state, no queue
priority, no adverse-selection microstructure (absorbed into
noise) — the model's own scope choice, and the reason it travels
between equities and FX at all; permanent-only impact in the core
model (a transient extension exists in Section 6); NASDAQ
estimates from a mixture of small- and large-tick stocks with the
large-tick decay estimates flagged by the authors; FX estimates
from conflated public snapshots with synthetic fills — a method
demonstration, not venue facts. arXiv v1, unpublished at read
time. Execution content is the paper's subject and none of it is
operationalized here; nothing trades live.
