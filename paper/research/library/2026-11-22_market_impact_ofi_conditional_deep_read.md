# Library deep-read session 85 — “Empirical Study of Market Impact Conditional on Order-Flow Imbalance”

Anastasia Bugaenko, “Empirical Study of Market Impact Conditional on
Order-Flow Imbalance”, MSc Quantitative Finance dissertation, Adam Smith
Business School, University of Glasgow, August 2019 (supervisor: Dr Ankush
Agarwal), posted as arXiv:2004.08290v2 [q-fin.CP], 24 Apr 2020. A single-author
master's dissertation measuring the NASDAQ market-order response function
from LOBSTER message/orderbook data, conditioning it on normalized trade
volume and on aggregated order-flow imbalance, and fitting linear and
decision-tree regressors to the aggregate impact.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x1a712b_empirical_study_of_market_impact_conditional_on_or.txt,
~119 numbered body pages plus front matter, 132 PDF pages page-marked, read
in full). Next UNREAD triage-rank entry (score 22), third of the score-22
tier, re-verified note-less against the live library note listing this
session.

## The paper in one paragraph

The dissertation reconstructs market orders from LOBSTER's message and
orderbook files for four NASDAQ stocks — large-tick SIRI and EBAY,
small-tick TSLA and PCLN — over 2 Jan to 30 Jun 2015 (124 trading days,
10:30-15:00 only, event types 4/5 only, first and last hour dropped,
same-timestamp child executions regrouped into parent MOs; PDF
pp. 44-49, 113-116) and estimates the lag-1 response function
R(1) = mean of eps_t times (m_{t+1} − m_t) (Eq. 20, PDF p. 69; Algorithm 1,
PDF p. 71), finding it “strongly positive” for all four stocks and
roughly proportional to the average spread for the small-tick names
(Tables 6-7, PDF pp. 73, 76; benchmarked against Bouchaud et al. 2018,
Table 8, PDF p. 77). Conditioning the response on volume normalized by
the daily mean opposite-side best-quote volume shows an almost flat,
faint relationship (Fig. 5, PDF pp. 81-82), and aggregating signed volume
over T = 5, 10, 20, 50 consecutive MOs (order-flow imbalance, Eq. 21,
PDF p. 83) shows impact linear in small imbalance and concave beyond
(Eq. 22, PDF p. 84; Figs. 6-8, PDF pp. 85-88), attributed to selective
liquidity taking (PDF pp. 82-83, 106-107). On 47,473 TSLA
(imbalance, impact) observations for T = 10 over all of 2015 (outliers
beyond 3 SD removed, then subsampled; PDF p. 87, Table 10, PDF p. 125),
linear regression and decision-tree regression are cross-validated 10
times: the tree wins on average MSE (4.11 vs 4.42 dollar cents) but loses
individual folds (Table 11, PDF p. 126; PDF p. 92), and the slope of the
linear region is read off as Kyle's lambda = 0.011 for TSLA (PDF pp. 92-95).
The abstract's headline: machine learning “predictive accuracy … can
surpass the performance of traditional statistical approaches” (PDF p. 3).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The silent-clip
   estimator bug is banked as the FORTY-SIXTH candidate: the
   estimator-implementation concordance rule (full rule text in the queued
   DECISIONS_PENDING line). Before the L0 gate, every registered
   descriptive statistic, admission null, comparator or refutation
   instrument whose estimator is defined in writing must carry a recorded
   one-time concordance audit before any data is touched: the executable
   implementation is checked against the written definition for silent
   numeric transformations the text does not declare (clips, max/min
   floors, winsorization, sign re-labelling, dropped-observation or
   subsampling rules, same-timestamp aggregation conventions), with the
   audit counted as frozen configuration and every divergence closed by a
   dated amendment before any run; a number produced by an implementation
   that does not match its written definition is inadmissible at the gate,
   however good it looks. Earned by the paper's own printed mechanism:
   Eq. 20 (PDF p. 69) defines R(1) as the signed mean of eps_t times
   (m_{t+1} − m_t), while Algorithm 1 (PDF p. 71, line 10) computes
   R = max(0, (m_{t+1} − m_t)·sign), clipping every negative signed
   response to zero, an undeclared transformation the text never
   mentions; the clipped mean converges to the expected positive part of
   the signed response, not the signed mean, so it is positive for any
   non-degenerate response distribution including a perfectly symmetric
   one, and the paper's own headline “R(1) is strongly positive for all
   stocks” (PDF p. 73) is partially manufactured by the clip (an honest
   signed-mean estimator could still be positive here, but the printed
   statistic cannot establish it). Harder to pass because an estimator
   whose code path embeds an undeclared clip or transformation now fails
   the concordance audit before any data is touched, where today the
   estimator-configuration freeze (deep-read 63) and the
   feature-normalization pre-declaration (deep-read 83) freeze only
   declared configurations and a text-vs-code divergence could survive
   silently into a run. Tightens the estimator-configuration freeze by
   extending the frozen-configuration class from the estimator's declared
   configuration to concordance of its implementation with the written
   definition. Killed-if-wrong counterfactual: if the rule is unnecessary,
   it is because no lawful implementation could diverge from a written
   definition without the divergence being a dated amendment already; this
   paper prints the counterexample in a visible algorithm listing, so the
   rule earns its place.
2. [reinforcing, no new item] The laundering ban binds on the ML
   comparison: the tree-beats-linear claim is a paired-family
   self-comparison on one stock with no market null, no costs and no
   economic baseline (CV MSE 4.11 (SD 1.07) vs 4.42 (SD 0.42) dollar
   cents, Table 11, PDF p. 126), and the paper itself concedes the tree
   “does not always produce more accurate predictions” (PDF p. 92); the
   Kyle-lambda 0.011 read (PDF pp. 92-95) rests on the same
   subsampled-after-outlier-removal construction. Nothing may enter the
   record as support for any programme claim. No queue change.
3. [reinforcing, no new item] Regime non-stationarity of the
   unconditional response: the same estimator over adjacent 2015 halves
   moves materially (TSLA R(1) 2.05 to 2.57 cents, spread 10.82 to 15.05;
   PCLN R(1) 10.09 to 14.35, spread 75.53 to 113.17; Tables 6-7, PDF
   pp. 73, 76), attributed by the paper to the 2015-16 sell-off regime
   (PDF p. 75). Unconditional microstructure level-statistics drift across
   regimes by amounts comparable to their cross-sectional contrasts;
   reinforces the queued self-excitation regime-window pre-declaration
   and the standing horizon discipline. Ammunition, never evidence. No
   queue change.
4. [interpretation caution] Selective liquidity taking is a conditioning
   bias, and the paper says so itself: concavity of impact in the
   imbalance (Figs. 6-7, PDF pp. 85-88) and the flat response-vs-volume
   relation (Fig. 5, PDF pp. 81-82) are attributed to large orders
   arriving only when revealed liquidity is large (PDF pp. 82-83,
   106-107). Any C1-L2/C8 read of a size-conditioned impact shape must
   treat the shape as partly constructed by the arrival/liquidity
   conditioning, not as a causal size law; this joins the
   conditioning-bias reading discipline family (recorded against the
   deep-read 84 liquidity-regime caution). No queue change.
5. [reinforcing, no new item] Tick-regime split: large-tick stocks
   (SIRI, EBAY) pin the spread at one tick, decouple R(1) from the spread
   and make mid-price dynamics queue-shaped, while small-tick TSLA and
   PCLN carry R(1) roughly proportional to spread (PDF pp. 73-74).
   Pooled cross-sectional or cross-asset claims that silently mix tick
   regimes inherit a structural confounder; the cross-market
   replication and control-arm discipline already requires the split. No
   queue change.
6. [interpretation caution] The aggregation clock is event-count, not
   wall-clock: the imbalance and the aggregate response are defined over
   T consecutive market orders (Eqs. 21-22, PDF pp. 83-84) and the
   imbalance amplitude scales with T (PDF pp. 85-86). Any C1-L2/C8
   aggregate-flow feature must declare its clock, which the queued VPIN
   clock pre-commitment amendment (C8 A4) and the flow-clock family
   already own; the drift of the response magnitude with the
   same-timestamp MO-reconstruction convention (PDF pp. 76-77, 116,
   124) is further evidence for the queued spread-convention
   declaration rule. No queue change.
7. [reinforcing, no new item] Hidden-order liquidity dilutes the
   visible-MO impact at the best quote (PDF pp. 45-46, 123): the impact
   of a visible order is partly absorbed by liquidity the message feed
   reveals only at execution. Standing visibility caveat — the same
   family as the aggTrades taker-only constraint — for any future L2
   impact measurement. No queue change.
8. [source-quality note] MSc dissertation (PDF p. 1), not peer-reviewed;
   arXiv v2 (2020) is the terminal public version, no journal counterpart
   to check; zero citations at cataloguing; source code withheld
   (“contact the author”, PDF p. 4); every headline number is anchored
   to Bouchaud et al. (2018) rather than independently replicated, with
   the R(1) under-estimation attributed to the implementation convention
   (PDF pp. 76-77, 124); single-stock ML exercise; MO-only focus under two
   declared simplifying assumptions (MOs never exceed best-quote
   liquidity; LO arrivals and cancellations neglected, PDF p. 67). Read,
   graded plainly as a student dissertation: useful as a mechanism
   exhibit (the print-vs-code clip) and not as an empirical authority.

## What this paper would have killed if we had done it wrong

Without the laundering ban, the abstract's claim that machine-learning
predictive accuracy “can surpass the performance of traditional
statistical approaches” (PDF p. 3) — a one-stock, no-null, no-cost CV
table whose own numbers show the winning model losing folds — would have
entered the record as licence for ML feature-engineering inside the C1-L2
spec. Without the frozen-configuration discipline, the max(0, ·) clip in
Algorithm 1 is exactly the class of silent transformation by which our
own response estimators could drift from their written definitions into
code that manufactures sign. The deep-read did not have to imagine the
failure; the paper printed it.

## Standing caveat

Everything here is 2015, one venue (NASDAQ via LOBSTER), four stocks,
10:30-15:00 windows, 124-248 trading days, mid-price quantities in
dollar cents, market-order-level impact only, meta-orders invisible
(order splitting unobservable in this data class, PDF pp. 70, 107). Treat
the paper as dissertation-grade: cite only for the mechanism exhibits,
never for magnitudes. There is no published version to check beyond the
arXiv v2 posting.
