# Library deep-read session 27 — Nittur Anantha & Jain, "Forecasting
# high frequency order flow imbalance using Hawkes processes"
# (arXiv:2408.03594v1, 2024; SigmaQuant/IISc; Hawkes forecasting of
# the near-term OFI DISTRIBUTION on NSE NIFTY futures, with a
# superior-predictive-ability model comparison)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x78a2e8_forecasting_high_frequency_order_flow_imbalance.txt`,
~21 pp., page-marked). Next UNREAD triage-rank entry (score 32;
verified unread by the read-slug mapping; shelves with the
PIN/VPIN-adjacent OFI line the program carries from the VPIN
toxicity review).

## The paper in one paragraph

The authors model BUY and SELL market-order arrivals (NSE NIFTY
futures, September 19, 2018 — ONE trading day, one contract) as a
bivariate Hawkes process with self- AND cross-excitation, compute
the realized OFI at tick time with DETERMINISTIC trade
classification (NSE trade messages carry the aggressive and passive
order ids, so no Lee-Ready-style inference is needed; PDF pp. 2-6),
and forecast the near-term DISTRIBUTION of OFI by simulating each
fitted model forward (Ogata's thinning / TICK library), scoring the
realized OFI's probability under each forecast distribution, and
ranking seven models under Hansen's test for superior predictive
ability (PDF pp. 4, 12-17). Results: the sum-of-exponentials Hawkes
kernel is the best-performing benchmark (p = 0.743), the
non-parametric conditional-law kernel and even the minute-count VAR
cannot be rejected at the 95 percent level, and the POISSON model
is decisively rejected (p = 0.0) — with the authors explicit that
the sum-of-exponential preference carries a computational
convenience motive and "may exhibit a bias" on full-day data
(PDF pp. 16-17, Table 4). Intraday, the fitted kernel norms show
BUY-BUY and SELL-SELL self-excitation dominating, with transient
episodes of raised BUY-SELL / SELL-BUY cross-excitation (PDF
pp. 17-18, Figure 6).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] Poisson OFI forecasting is
   REJECTED on one day of data — the omissions-manufacture-signals
   family gains an unambiguous head-to-head.** The Poisson model
   was the only competitor rejected outright (p = 0.0) against
   self-and-cross-exciting alternatives (Table 4, PDF p. 16).
   Session 20 recorded that Poisson flow MISPRICES resilience
   robustly (fictitious manipulation profits); this paper adds the
   forecasting face: an omission of self-excitation destroys
   predictive adequacy outright, not marginally. The existing
   flow-model-declaration discipline (session 20) already forces
   the declaration; nothing new queued.

2. **[reinforcing, no new item] Trade classification is a
   construction, and deterministic ids are a venue gift — the
   estimator-mode rule applies to the SIGN of every event.** The
   paper's buy/sell marking is exact because NSE publishes the
   aggressive and passive order ids in the trade message; where
   ids are absent, classification falls back to Lee-Ready/bulk
   algorithms, which "may struggle in highly volatile markets...
   leading to incorrect classification" (PDF pp. 4, 2-3). An OFI
   built on inferred signs is a different estimator from one built
   on venue-assigned signs, and its errors concentrate exactly in
   the high-activity windows any imbalance feature weights most.
   The estimator-mode rule (session 11) already forces the
   declaration; citation recorded as reinforcement for the
   sign-register family (session 10).

3. **[interpretation caution] Cross-excitation between sides is
   regime-episodic, not a constant — kernel-norm time series are
   not transferable as static venue parameters.** The intraday
   analysis shows BUY-SELL / SELL-BUY cross-excitation spiking in
   transient episodes against a dominant self-excitation baseline
   (PDF pp. 17-18): the branching/interaction structure itself is
   time-varying within a single day. Joins the per-branch rule
   (session 9), dispersion register (session 12), and
   kappa-as-state-moment (session 24) in the never-read-alone
   family: a fitted kernel norm is a window mixture, and window-
   mixtures change meaning with regime composition (the
   session-26 RSCHP point, here on real data).

4. **[source-quality note] One day, one instrument, and an
   admitted ranking bias.** All results come from a single trading
  day of a single NIFTY futures contract; the authors themselves
   caveat that the sum-of-exponential preference "may exhibit a
   bias in favor of" the Markovian kernel on full-day data, and
   that CondLaw and VAR cannot be rejected anyway (PDF pp. 16-17).
   Single-day kernel estimation cannot support venue- or
   regime-level claims; the useful content is the METHODOLOGY
   (distributional forecasting + SPA ranking with an explicitly
   named loss) and the Poisson rejection, not the ranking itself.
   arXiv v1, August 2024, no published version located at read
   time — check before formal citation.

## What this paper would have killed if we had done it wrong

If an OFI-family feature had ever been specified with inferred
(Lee-Ready-style) trade signs on a venue where exact signs are
unavailable, its high-activity windows would have carried exactly
the classification noise the authors warn clusters there — a
construction artifact indistinguishable from signal in the windows
that matter. And if any flow-agnostic (Poisson/constant-intensity)
baseline had been pre-registered as a SERVING null, this paper's
result says the null is trivially killable everywhere, arming
nothing and inflating whatever beats it: a null that dies by
omission is a placebo, not a test. The program's sign-declaration
discipline and the existing Poisson-mispricing recording preclude
both; the paper reinforces, changes nothing.

## Standing caveat

One day, one NIFTY (2018) futures contract, large-tick venue with
exchange-provided ids and a co-located custom feed — none of it
transports to small-tick Binance perps; the SPA ranking is
single-day and the authors concede a possible bias toward the
Markovian kernel; the OFI here is a count-based construct at
minute-window granularity in evaluation (different from the CKS
depth-weighted OFI, a construction distinction to respect when
comparing to sessions 3/18/23); no microstructure modeling of the
book itself. arXiv v1, unpublished at read time. Market-making
utility content is the paper's motivation and none of it is
operationalized; the program never trades live.
