# Deep-read session 29 — Nittur Anantha and Jain, "Forecasting high frequency order flow imbalance using Hawkes processes"

Library deep-read session 29 (null-time session 33, log entry ## 37).
Aditya Nittur Anantha (SigmaQuant Technologies Pvt. Ltd., Indian
Institute of Science) and Shashi Jain (Indian Institute of Science),
arXiv:2408.03594v1 [q-fin.TR], 7 August 2024, 21 pp. text extract,
page-marked. Read 2026-11-18, against ONE question: what here would
kill C1-L2 or C8 faster, or change their kill lines? Source: legally
acquired OA copy
(docs/library/text/x78a2e8_forecasting_high_frequency_order_flow_imbalance.txt).
Assigned triage-rank entry (score 32, x78a2e8). Next UNREAD
triage-rank entry (score 32, x98e019, "Hybrid Vector Auto Regression
and Neural Network Model for Order Flow Imbalance").

## The paper in one paragraph

A trade-count order flow imbalance is defined as the normalized
difference of SELL-classified and BUY-classified trade counts over a
window (eq. (3), PDF p. 5), with the aggressor side determined
deterministically from the two exchange order numbers carried on each
NSE trade message, no Lee-Ready or bulk classification inference
involved (PDF p. 5). The paper fits bivariate self- and
cross-exciting Hawkes processes to one day of NIFTY futures trade
arrival times (19 September 2018, current-month contract, 375
one-minute windows; PDF pp. 5-7), forecasts the next minute's OFI
distribution by simulating each fitted intensity (Ogata's thinning,
500 simulations per window; PDF pp. 10, 12-13, 15-16), scores each
model's empirical forecast distribution by the probability it assigns
the realized OFI, and compares negative log-likelihood losses across
all models with White's reality check and Hansen's test for superior
predictive ability (PDF pp. 7-8, 11, 16). Competing kernels are
exponential, sum-of-exponentials, power-law (parametric),
conditional-law and EM (non-parametric), plus a VAR on minute counts
and a Poisson benchmark (PDF pp. 13, 16): sum-of-exponentials
(p 0.743) and conditional-law (p 0.257) are the only non-rejected
benchmarks, with VAR at 0.101 also not rejected at 95 percent
(Table 4, PDF p. 16), and the sum-of-exponentials is favored on
computational cost alone (PDF pp. 16-17). Appendix tests show the
minute-level realized OFI stationary (ADF) and strongly non-normal
(Kolmogorov-Smirnov, Shapiro-Wilk, Anderson-Darling; PDF p. 20),
and the fitted sum-of-exponentials interactions show BUY-BUY and
SELL-SELL self-excitation dominating the day with intermittent
cross-excitation episodes (PDF p. 18).

## Findings, graded

NO kill line changed. NO new candidate sharpening queued. This is the
default grade: nothing here earns a rule.

1. **[interpretation caution]** The OFI name collision. This paper's
   OFI is the normalized trade-count asymmetry (delta-N of classified
   trades, eq. (3), PDF p. 5), not the Cont-Kukanov-Stoikov
   depth-change OFI of the record's line: the paper cites CKS 2014
   (PDF p. 3) for the price-impact relationship of a related but
   distinct quantity, and its own OFI counts trades, not book-depth
   changes (PDF pp. 3, 5). Any cross-reading of this paper's results
   onto the record's CKS-family OFI (multi-level OFI, the event-grain
   accumulation rule queued through deep-read session 25) conflates
   two different measurements that share only the acronym. The
   immediate next entry in the queue (x98e019) sits in the same
   count-family, so the distinction stays live over the coming
   sessions.

2. **[reinforcing, no new item]** Aggressor side must come
   exchange-native, never inferred. The paper's classification is
   deterministic because NSE trade ticks carry both order numbers,
   and the paper's stated reason for avoiding Lee-Ready and bulk
   classification is precisely that inference-based rules misclassify
   in volatile, fast-moving markets (PDF p. 4). Corroborates the
   standing "aggTrades is taker prints only, no taker proxy"
   constraint at the mechanism level: the programme's taker flag is
   exchange-native on its venue, and this paper independently
   documents why tick-rule inference is a degraded substitute. The
   NSE order-ID mechanism itself is a venue property and transfers
   nowhere.

3. **[reinforcing, no new item]** Aggregation discards event
   clustering, but this paper does not prove the recovery. The
   motivation is on the record's side: aggregating buy orders into
   windows "can miss out on the clustering of order arrivals"
   (PDF p. 3). Yet the paper's own SPA table cannot reject the VAR on
   minute counts at 95 percent (VAR p 0.101, Table 4, PDF p. 16), the
   authors concede that the conditional-law and VAR models cannot be
   rejected with 95 percent confidence (PDF p. 17), and they flag a
   possible same-day bias favoring the sum-of-exponentials choice
   (PDF p. 17). So the event-grain OFI accumulation rule queued
   through deep-read session 25 gains no corroboration here, and the
   record says so honestly rather than laundering a thin result into
   support.

4. **[interpretation caution]** The headline is a benchmark-selection
   exercise, not a forecasting edge. The deliverable is a
   simulation-based method for producing near-term OFI distributions
   (Algorithm 5.3, PDF pp. 15-16) and a loss-construction framework
   that lets White's reality check and Hansen's SPA compare many
   models at once (PDF pp. 7-8, 11). There is no price prediction,
   no P&L, no costs, no strategy: the stated use cases are
   post-facto adverse-selection estimation for market makers and
   surveillance for regulators (PDF p. 3). The SPA numbers are
   benchmark-rejection p-values over 315 one-minute loss
   observations, one instrument, one session, and are never
   out-of-sample beyond that day. Non-rejection of a benchmark is
   weak evidence; the normality rejections (PDF p. 20) say the OFI
   distribution is asymmetric and heavy-tailed, which is the honest
   reading of why distributional rather than point forecasts are
   used (PDF p. 4).

5. **[source-quality note]** Two authors, one at a quant technology
   firm (SigmaQuant) with an academic affiliation (Indian Institute
   of Science), one academic; arXiv v1 only, stamped 7 August 2024,
   no journal record checked; zero indexed citations as of the
   session date; single-market (NSE India), single-instrument,
   single-session dataset (PDF p. 5); the power-law kernel is fitted
   by an ad-hoc stochastic gradient descent on the likelihood with
   no convergence guarantees stated (Algorithm 5.1, PDF pp. 11-12);
   extract page-marked and clean throughout, tables legible, figures
   unrecoverable in the extract but non-load-bearing. Published
   version to be checked before any formal citation.

## Killed if wrong

Nothing in the record rests on this paper: no rule was added or
amended on its basis, so if the SPA ranking is later shown to be an
artifact of the single-day sample, the probability-of-realized-OFI
loss construction, or the same-day bias the authors themselves flag
(PDF p. 17), nothing dies and nothing needs repair. Conversely, if
the record ever cited this paper as confident evidence that
event-time OFI forecasting beats calendar-time count aggregation,
that would be a laundering of a non-rejected null: the honest
citation is that VAR (p 0.101) could not be rejected at 95 percent
on this paper's own test (Table 4, PDF p. 16), and any such citation
should die in review.

## Standing caveat

One trading session (19 September 2018), one instrument (NIFTY
futures expiring 27 September 2018), NSE India tick data, 375
one-minute windows, 315 loss observations; deterministic aggressor
classification via NSE order numbers, a venue property other markets
do not share; realized minute OFI stationary and strongly non-normal
(PDF p. 20); no costs, no P&L, no execution, regulatory and
risk-management framing only; no crypto, no BTCUSDT. Laundering
directions named. INTO: no kernel form, no sum-of-exponentials or
power-law parameterization, no window or simulation parameter
(1-hour fit, 1-minute forecast, 500 simulations), no loss
construction, and no p-value from this paper enters any spec,
default, or calibration, and the Hawkes-forecasting construction is
not adopted anywhere without its own pre-registration. OUT: the
sum-of-exponentials headline and the SPA p-values are never cited as
evidence that event-time modeling beats calendar aggregation beyond
this paper's own single-day NSE sample, never as expected behavior
of the programme's CKS-family OFI quantities, never as expected
BTCUSDT behavior, and never as evidence about any market the
programme measures.
