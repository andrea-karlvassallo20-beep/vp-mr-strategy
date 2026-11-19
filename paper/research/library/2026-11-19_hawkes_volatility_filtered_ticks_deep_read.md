# Deep-read: Hawkes volatility on filtered tick structures (Lee 2022/2024)

Null-time session 62 (log ## 66), deep-read session 52. Kyungsub Lee, "Application
of Hawkes volatility in the observation of filtered high-frequency price
process in tick structures," arXiv:2207.05939v2 (2022 submission, v2 dated
21 Sep 2024, per PDF p. 1). A single-author statistics paper deriving
closed-form variance (volatility) formulas for unmarked and marked bivariate
Hawkes price-move models and applying them to 0.1-second-filtered NBBO mid-price
tick data for US equities and E-mini S&P 500 futures.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xb710f4_application_of_hawkes_volatility_in_the_observatio.txt,
~37 pp., page-marked). Next UNREAD triage-rank entry (score 28).

## The paper in one paragraph

The paper models up (N1) and down (N2) tick-level mid-price moves as mutually
exciting bivariate Hawkes processes with exponential kernels and a common
decay per leg (Assumption 1, PDF pp. 4-5), derives the moment machinery
(a Sylvester equation for the second intensity moments, an affine-in-t
approximation for the intensity-count cross moments, Theorem 5, PDF pp. 6-8),
then extends to a marked model whose marks are integer tick jump sizes with a
LINEAR impact function on jumps beyond one tick (Assumption 2, PDF pp. 8-10),
handling possible mark-intensity dependence semi-parametrically through
covariance-adjusted conditional expectations (Definition 2, PDF p. 11). The
variance formulas (Theorem 13, Corollaries 14-15, PDF pp. 14-15) turn
parameter estimates into price-change variance over an interval. Empirics:
raw tick data does not fit a single-kernel exponential Hawkes well, so the
mid-price is filtered at a 0.1-second observation grid before estimation (PDF
pp. 4, 16-17, Figure 1); a 10,000-path simulation with power-law true kernels
shows the exponential marked Hawkes volatility computed on filtered data is
nearly unbiased (sample std 167.35 vs Hawkes mean 166.53, PDF p. 17,
Figure 2). Daily Hawkes volatility tracks 5-minute realized volatility and
absolute daily changes closely (2016-2019 NVDA et al., PDF pp. 18-21,
Figures 8-10); exceedance counts sit on the normal curve (PDF p. 20).
Intraday estimation on 30-minute rolling windows gives real-time volatility
(PDF pp. 22-23, Figures 11-13), whose weight in a linear blend with GARCH
grows monotonically through the day until it dominates roughly 30 minutes
after the open (AAPL, PDF pp. 24-25, Figure 14). Pre-market E-mini futures
Hawkes volatility linearly explains post-open stock volatility (adjusted
R-squared 0.52 for the best windows, beating two-scale realized variance at
0.27, PDF pp. 25-27) and improves stock volatility forecasts at every
pre-market interval (RMSRE, PDF pp. 27-28, Figure 16).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The paper's core preprocessing fact is that the
   aggregation grid is load-bearing: raw tick data records dozens of events
   per second (AMZN, 20 June 2018: up to 60 per second) and does not fit a
   single-kernel exponential Hawkes; the chosen fix is a 0.1-second filter
   "validated through numerous empirical studies" with "no clear standard"
   for the interval, picked because it makes estimates stable (PDF pp. 4,
   16-17). This is the aggregation researcher-degree-of-freedom demonstrated
   on live data: the model fits or fails depending on a hand-chosen grid. It
   licenses nothing new because C1-L2 already closes this channel before the
   data: labels on wall-clock economic barriers with a TRADE-through touch
   rule, covariates refreshed on the event clock, frozen barrier widths with
   a noise floor (c1_l2_test_spec.md sections 1-2). The clocks are frozen;
   there is no post-hoc grid to tune. Reinforcement of the existing
   discipline, not a tightening of it.

2. [interpretation caution] The unrestricted semi-parametric marked variance
   (Definition 2 + Theorem 13) can produce NEGATIVE variance estimates when
   the covariance-adjusted mark expectations are computed from sample means;
   the paper's own remedy is to prefer the restricted linear-in-t version
   (Corollary 14, PDF p. 14). Same estimator-discipline family as the queued
   estimator-mode sharpening: any future marked-Hawkes variance machinery in
   C8's neighborhood must pre-declare the restricted estimator and declare a
   negative-variance output a named abort signal, not a license to switch
   estimators after seeing results. Reading rule only; queues nothing.

3. [reinforcing, no new item] At daily grain the fine-grain instrument and
   the coarse benchmark agree: daily Hawkes volatility, 5-minute realized
   volatility, and absolute daily changes show the same dynamics and are
   treated as interchangeable summaries of the same quantity (PDF pp. 19-21,
   Figures 8-10). This is a direct instance of the premise the queued
   thirty-first sharpening (the C1-L2 base-rate confrontation, ## 65) forces
   into the spec: measurements taken at fine grain do not add information
   once they are summarized at daily grain. The L2 positive must therefore
   be pre-declared as incremental at finer-than-daily timing or book
   resolution, exactly as the queued confrontation paragraph demands.
   Reinforcement of an item already pending owner ratification; nothing new
   queued.

4. [interpretation caution] The headline intraday claim ("increasing
   predictive power of intraday Hawkes volatility over time") is a
   likelihood-re-optimized-per-T blend with no multiplicity control across
   T, and the futures-stock result (pre-market E-mini Hawkes volatility
   explaining post-open AAPL volatility, adjusted R-squared 0.52, against a
   same-day realized target) is one name, one year (2019), no costs, no
   overlap control (PDF pp. 24-28). R-squared is not edge and not a C8
   input; the SHAPE (early-session fine-grain information carrying what the
   previous day's daily summary cannot) is the C1-L2/C8 motivation itself,
   and it stays ammunition, not evidence. The Q-Q residual diagnostics
   reject unit-exponential residuals on some days and are dismissed without
   test or mechanism ("we believe this does not significantly affect the
   estimation of volatility," PDF pp. 19-20), a named example of
   fit-complacency to be refused anywhere a future estimator's residuals
   fail their distribution.

## What this paper would have killed if we had done it wrong

If the clocks were not frozen, this paper is the demonstration of the death:
a compression "signal" discovered at one aggregation grid and absent at
another, with the grid chosen after seeing the data because it made
estimates stable. The spec's pre-declared barrier/event clocks remove the
choice. If the base-rate confrontation had not been queued, finding 3 would
have been discoverable only AFTER the L2 phase, as a post-hoc excuse on a
dead or laundered result; queued now, it is a kill line the positive must
survive before any data arrives. If an unrestricted marked-Hawkes variance
ever enters a C8 pre-registration without the abort rule, finding 2 is the
post-null re-tuning channel the gates forbid: negative variance, switch
estimator, iterate to significance.

## Standing caveat

arXiv version only (v2 of a 2022 submission, revised Sep 2024); check the
published version before any formal citation. Zero recorded citations in our
index; single author. The empirical sections are graphical and descriptive:
no formal inference backs the monotone-likelihood, blend-weight, or
cross-market R-squared claims; the 0.1-second filter is the author's
stability standard, not a published rule; the futures-stock study is
AAPL-only (one year, no cost layer); residual misfit days are acknowledged
and waved off without test (PDF pp. 19-20). Nothing here is program evidence
for any claim; it informs reading discipline and estimator caution only.
