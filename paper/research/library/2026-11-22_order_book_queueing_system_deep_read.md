# Deep-read session 94: Muni Toke, "The order book as a queueing system: average depth and influence of the size of limit orders"

Session: null-time session 104 (log entry ## 125), 2026-11-22.
Authors: Ioane Muni Toke (ERIM, University of New Caledonia; Chair of
Quantitative Finance, Ecole Centrale Paris).
Full title: The order book as a queueing system: average depth and
influence of the size of limit orders.
Venue: arXiv:1311.5661v1 (22 Nov 2013), per docs/library/expanded_index.json
(slug xe1c4ca, topic arxiv-book). One clause: a one-side order book with
Poisson order flows and exponential order lifetimes is analyzed as an
M/M/1+M queueing system, giving a closed-form average book shape (a
conservation-of-flows identity: shape = arrival intensity x cancellation
probability), extended to random limit-order sizes, with the theoretical
prediction that at constant total incoming volume fewer-and-larger limit
orders deepen the near-spread book, tested by a 14-stock Paris panel.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xe1c4ca_the_order_book_as_a_queueing_system_average_depth_.txt,
~26 pp., page-marked). Next UNREAD triage-rank entry (score 20, fourth of
the score-20 tier).

## The paper in one paragraph

The model is a one-side limit order book: ask limit orders arrive at price
i as independent Poisson processes with rates lambda_i, unit market orders
arrive as a Poisson process with rate mu, and every standing limit order
lives an exponential lifetime with parameter theta (PDF pp. 1-4). The
cumulative depth L_1->k is the size of an M/M/1+M queue with arrival rate
lambda_1->k, service rate mu and reneging rate theta, whose stationary
distribution exists for theta > 0 and is written in closed form (eqs. 2-9,
PDF pp. 5-6); a continuous extension replaces the per-price Poisson
processes by a spatial Poisson process with intensity a*h_lambda(p),
giving the average shape b(p) in closed form (Proposition 1, eqs. 10-13,
PDF pp. 7-8). Proposition 2 is a law of conservation of the flows: b(p) =
h(p)C(p) with C(p) the probability that a limit order at price p is
cancelled before execution (eqs. 14-17, PDF pp. 8-9) — the shape of the
book is exactly the fraction of arriving limit orders that will be
cancelled. The shapes reproduce Smith et al. (2003)'s simulated regimes
(Fig. 1, PDF pp. 10-11) and track the only prior analytical formula,
Bouchaud et al. (2002)'s diffusive approximation (eq. 19; comparison
Fig. 2, PDF pp. 11-13). Random (geometric) limit-order sizes turn the
queues into M^X/M/1+M bulk queues with pgf-solved stationarity
(Propositions 3-4, eqs. 20-30, PDF pp. 13-16) whose shapes deepen near
the spread as the average order size grows at constant total volume
(eqs. 29-31, Figures 3-4, PDF pp. 16-19). The empirical section regresses
cumulative depths at 1-10 ticks from the best opposite price on
limit/market order counts and volumes across 14 Paris stocks and 391
thirty-minute intervals (Jan 4 - Feb 22 2010; Table 1, PDF pp. 17-20),
with fixed-effect panel regressions (eq. 32, PDF p. 21) broadly
supporting the size-vs-count result (Table 2, PDF pp. 21-23).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The conservation-of-flows identity
   (Proposition 2, eq. 14, PDF p. 8; eqs. 15-18, PDF pp. 8-9): the
   average shape equals the arrival intensity times the cancellation
   probability — an exact within-model consequence ("the shape of the
   order book is exactly the fraction of arriving limit orders that will
   be cancelled", PDF p. 8), so a book null in this class reproduces
   mean depth BY CONSTRUCTION from its declared flow parameters; a
   shape-agreement audit against such a null certifies arithmetic, not
   mechanism. The stationary depth exists only because theta > 0
   (cancellation is the stabilizer, PDF pp. 5-6): a generative book null
   with no positive cancel rate has no stationary depth at all, and the
   passive-cancel rate is therefore frozen configuration of exactly the
   kind the generative-null pre-declaration family (deep-reads 81/87)
   demands; the zero-intelligence class is also the precise model class
   the passive-withdrawal anatomy must never be laundered from. Licenses
   nothing new: votes for the placebo, generative-null and
   dynamics-identification families. No queue change.

2. [reinforcing, no new item] A sign reversal under covariate-set choice
   is printed in the paper's own results: the market-order volume
   coefficient is significantly POSITIVE without the limit-order
   interaction term (+0.0088, t = 11.1, p < 2.2e-16) and significantly
   NEGATIVE with it (-4.8e-4, t = -5.3, p = 1.4e-7), same data, same
   5,474-point sample (Table 2, top panel, PDF p. 23; specification
   eq. 32, PDF p. 21); the B10 panel repeats it (+0.0097, t = 5.6 →
   -6.2e-4, t = -3.1, PDF p. 23). The covariate set IS configuration: the
   SIGN of a significant coefficient is a function of the
   specification. The paper handles its own reversal honestly (naming
   and resolving the "apparent paradox", PDF pp. 22-23); the printed
   fact is a vote for the estimator-configuration freeze (deep-read 63)
   and the primary-metric pre-commitment (deep-read 55). No queue
   change.

3. [interpretation caution] Distance-indexed depth statistics are
   anchor- and spread-path-conditional: the empirical depths B_i are
   computed at 1-10 ticks from the best opposite price over 30-minute
   intervals, and B_{10+j} "is not exact if the spread reaches a level
   lower or equal to j ticks during interval t" (PDF pp. 20-21), so
   measured depth at tick-distance mixes exact and censored
   observations exactly when the spread tightens toward the ten-limit
   data boundary (PDF pp. 19-20). A future L2 depth feature indexed by
   distance from touch must pre-declare its anchor convention
   (instantaneous vs interval-averaged best price) and its
   truncation-through-spread-tightening composition shift, or it
   silently conditions on the spread path. Feeds the censoring
   discipline and the availability discipline (#45/#48); joins the
   fixed-tick structural-bias caution (deep-read 14). No queue change.

4. [interpretation caution] The model's own simplifications are
   acknowledged empirically false in its class: exponential lifetimes
   where power-law lifetimes are cited, plausibly distance-dependent
   lifetimes, and Poisson flows where complex point processes are known
   to govern order flow (PDF p. 5). The headline fewer-and-larger-orders
   result is therefore a Markovian-family statement, and its empirical
   support is an association at 30-minute grain on a 14-stock panel
   (PDF pp. 19-23): a within-grain association at one grain licenses
   nothing at tick grain, where event-time and volume clocks govern
   (the flow-clock and event-clock families). No queue change.

5. [cost-survival ammunition] All depth/activity magnitudes are
   venue-, sample- and grain-specific and banned from the record under
   the laundering rule: the positive activity-depth relation decays with
   distance from touch (significant at B5 and B10; NOT significant at
   B10-B5, Table 2 lower panel, PDF p. 23); R2 between 0.08 and 0.15
   (PDF p. 23). If a K7-style cost-survival layer ever exists it must
   carry the assumptions this model assumes away: a one-side book with
   an infinite-volume standing bid at zero, unit market orders,
   share-by-share independent cancellations, price-time separable
   intensity (PDF pp. 4-5, 13). A never-operationalized
   execution-strategy application. No queue change.

6. [source-quality note] arXiv v1 (22 Nov 2013); a published version
   exists — check the published version before formal citation. Data:
   14 Paris stocks (13 CAC-40 members plus Ubisoft), Jan 4 - Feb 22
   2010, with 3.5 missing or incomplete trading days acknowledged
   (footnote 2, PDF p. 19); first ten limits only (PDF pp. 19-20); the
   ask/bid side convention for the regression depths is left unstated
   beyond the "first 10 ticks from the best opposite side" definition
   (PDF pp. 20-21) — an unstated convention in exactly the class the
   convention-declaration rule names. No queue change.

## What this paper would have killed if we had done it wrong

Without the estimator-configuration freeze, a future C1-L2 panel
decomposition could have reported whichever covariate-set sign fit the
hypothesis: the paper's own table shows a significant positive and a
significant negative estimate of the SAME coefficient available on the SAME
data (Table 2, PDF p. 23) — the sign is a researcher degree of freedom
invisible to significance stars. Without the censoring discipline, a
distance-from-touch depth statistic would silently shift composition
exactly when the spread tightens toward the data boundary (PDF pp. 20-21)
— the regime where compression claims would live, i.e., precisely the
rows a post-hoc narrative would have preferred to keep uncritically.
Without the generative-null and placebo disciplines, a zero-intelligence
null "reproducing" the average book could have been cited as validation
(PDF p. 8) when the reproduction is the null's own conservation identity:
an arithmetically guaranteed match dressed as a passing test. The
programme's defaults (frozen configuration, primary-metric
pre-commitment, honest censoring, placebo before validation) are what
avoid all three deaths.

## Standing caveat

Everything is for a zero-intelligence Markovian family: independent
Poisson limit flows, unit-size market orders, exponential lifetimes, a
one-side book equivalent to an infinite-volume standing bid at zero,
price/time separability of the limit intensity, geometric order sizes with
share-by-share cancellation. The paper itself flags the exponential
lifetime and Poisson flow assumptions as rough against the empirical
record (PDF p. 5). The empirics cover 14 Paris stocks, 7 weeks of 2010,
the first ten limits, and 30-minute intervals with panel fixed effects;
every magnitude is associative, not causal, and banned from the record.
The queueing results hold for Poisson flows specifically: no excitation
structure (no Hawkes-type self-excitation) exists anywhere in the model
class, so nothing here licenses any claim about intensity feedback — the
C1-L2 family's concerns enter only through what the class's
stationarity does NOT contain. A library is ammunition, not evidence: no
empirical claim from this paper enters the record as support for any
programme claim. arXiv v1: check the published version before formal
citation.
