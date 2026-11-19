# Deep-read session 47 — Xu, Gould, and Howison, "Multi-Level Order-Flow Imbalance in a Limit Order Book"

Library deep-read note, null-time ritual. Deep-read session 47, logged
under its null-time session number in `paper/research/null_time_programme.md`.
Authors: Ke Xu, Martin D. Gould, and Sam D. Howison, Mathematical
Institute, University of Oxford. Published record: arXiv:1907.06230v2
[q-fin.TR], 26 October 2019 (v1 July 2019); a direct empirical extension
of the Cont-Kukanov-Stoikov (2014) order-flow imbalance line: the scalar
OFI becomes a vector MLOFI of net order flow at the first M populated
price levels, fitted contemporaneously against the mid-price change on
LOBSTER data for 6 Nasdaq stocks across all of 2016, with a worked
estimator comparison (multivariate OLS versus Ridge) and metric
comparison (adjusted R2 versus out-of-sample RMSE) as its central
result.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x09d0b5_multi_level_order_flow_imbalance_in_a_limit_order_.txt,
32 pp., page-marked, read in full). Next UNREAD triage-rank entry
(score 29, file-order next after the variance-Hawkes paper consumed
through deep-read 46), re-verified unread against all 47 library notes
on main.

## The paper in one paragraph

The authors define the mth MLOFI component as the Cont-style net order
flow e_m = deltaW_m - deltaV_m summed over 10-second windows at the mth
populated price level on each side (Eqs. 9-12, PDF pp. 7-9), level-1
MLOFI being exactly OFI, and fit dP = alpha + sum_m beta_m MLOFI_m on
LOBSTER data for AMZN, TSLA, NFLX, ORCL, CSCO, and MU, all order flow
from 4 January to 30 December 2016, 10:00-15:30 on each day, hidden
liquidity excluded, 252 days x 11 half-hour windows = 2772 regressions
per stock with mean coefficients reported (PDF pp. 10-13): univariate
OFI is strongly significant (beta significant in 100 per cent of
samples; Tables 3-4, PDF pp. 13-14), but the joint OLS fit on M = 10
levels is unstable, because the MLOFI components are strongly
multicollinear (sample correlations above 0.5 for small-tick stocks and
above 0.7 for the rest, eigenvalue ratios essentially zero; Figs. 1-2,
PDF pp. 17-18), the same beta_1 collapses to weak significance in the
joint OLS fit (Tables 5-6, PDF pp. 15-16), and OLS overfits —
out-of-sample RMSE rises for M beyond about 5 on AMZN and TSLA while
in-sample RMSE keeps falling, "a classic hallmark of overfitting"
(Fig. 5, PDF pp. 23-24); switching to Ridge regression (lambda chosen
per 30-minute window by 5-fold cross-validation over 50 log-spaced
candidates; Table 7, PDF p. 19) stabilises the beta_m, makes almost all
of them significant (Tables 8-9, PDF pp. 20-21), makes out-of-sample
RMSE fall monotonically in M for every stock, and improves on OFI alone
by about 17/15/31/68/74/64 per cent for AMZN/TSLA/NFLX/ORCL/CSCO/MU
(Table 10, PDF p. 26) — 15-30 per cent for small-tick and 65-75 per cent
for large-tick stocks; the authors attribute the Cont et al. (2014)
contrary conclusion to OLS instability plus an in-sample-only adjusted
R2 metric (Section 6.1, PDF pp. 25-26), explain the large-tick/small-tick
split by spread geometry (Section 6.4, PDF pp. 27-28), and argue the
improvements are economically meaningful for high-frequency prediction
algorithms, un-costed (PDF p. 28).

## Findings, graded (does any kill line move?)

Verdict: NO kill line changes. NO new candidate sharpening. Default
grade. The paper is a worked exhibit for rules the programme already
enforces (estimator-mode pre-declaration, goodness-of-fit-metric
pre-declaration, holdout/leakage discipline, library-is-ammunition).
Nothing here would kill C1-L2 or C8 faster; nothing licenses a spec
change.

1. [reinforcing, no new item] — the estimator and the metric ARE the
   verdict: on identical features, data, and target, multivariate OLS
   with adjusted R2 supports "deep levels do not matter" (the Cont et
   al. Appendix B3 reading, re-confirmed here) while Ridge with
   out-of-sample RMSE supports "deep levels strongly matter" (Section
   6.1, PDF pp. 25-26; Tables 9-10, PDF pp. 21, 26). Any programme
   claim that turns on a multivariate feature set must pre-declare both
   the estimator and the GoF metric, which the standing rules already
   require; no rule moves.

2. [reinforcing, no new item] — the overfitting exhibit is textbook:
   in-sample RMSE decreases in M while out-of-sample RMSE increases
   past M about 5 for AMZN and TSLA (Fig. 5, PDF pp. 23-24), and the
   authors themselves state that adjusted R2 underestimates
   out-of-sample variance under multicollinearity (PDF p. 23). This is
   exactly the behaviour the leakage screens and pre-declared holdouts
   exist to catch; they need no amendment. The multicollinearity
   measurement itself (correlations 0.5-0.7+ across book levels,
   eigenvalue ratios near zero, PDF pp. 17-18) corroborates the
   standing requirement to screen collinear book features before any
   joint interpretation.

3. [interpretation caution] — contemporaneous is not predictive: every
   regression explains the mid-price change in the SAME 10-second
   window as the flow (Eqs. 7, 16, PDF pp. 7, 14); there is no forecast,
   no execution model, no cost, anywhere in the paper, and the
   "economically meaningful" claim is an un-costed high-frequency
   precision argument (PDF p. 28). An out-of-sample RMSE improvement in
   contemporaneous explanation licenses nothing about any
   horizon-explicit compression-clock claim, and the marginal
   magnitudes (fractions of a tick, against spread-crossing costs on a
   venue whose spread is one tick for the largest improvements) would
   not survive the economic gate as stated.

4. [interpretation caution] — the large-tick/small-tick split is venue
   structure, not a universal: the 65-75 per cent improvements
   concentrate in stocks whose spread is pinned at one tick (ORCL,
   CSCO, MU; Table 1, PDF p. 11; Section 6.4, PDF pp. 27-28), where
   in-spread arrivals are impossible and deep cancellations enable
   multi-tick moves; and the authors themselves exhibit the small-tick
   degeneracies (the same MLOFI vector mapping to different mid-price
   outcomes, PDF pp. 27-28), which is precisely why MLOFI is a coarser
   statistic than book state. Nothing transfers to any venue the
   programme measures without its own venue-explicit, horizon-explicit
   test; no figure in this paper is a venue constant.

5. [source-quality note] — arXiv v2, anonymous reviewer thanked,
   published version not checked at reading (uncertain, flagged for
   verification); 6 stocks, one year, one venue, hidden orders excluded,
   off-venue flow unobserved (PDF pp. 10-11); 2772 fits per stock with
   mean parameters and mean standard errors reported; Ridge standard
   errors via van Wieringen's formula (PDF p. 20). Extract caution:
   Table 6 (PDF p. 15) is captioned as the OLS significance tests but
   its first column header reads "Ridge" — a copyediting slip (the
   values match the OLS fits of Table 5), flagged so no later citation
   borrows the wrong label. Graded per the session-9 triage-audit rule:
   read it, grade it plainly, do not promote it.

## What this paper would have killed if we had done it wrong

Had the 65-75 per cent out-of-sample RMSE improvements been read as
"deep-book flow carries an edge", a costless contemporaneous
mid-price-explanation regression on tick-constrained Nasdaq equities
would have been laundered into a predictive claim the paper never makes.
Had the beta_1 collapse in the joint OLS fit been read as "deep levels
do not matter" (the Cont et al. reading) or the Ridge significances as
"every level matters causally", the estimator would have decided the
science twice, and the paper's own Section 6.1 exhibits both errors on
the same data. Had adjusted R2 been imported as a GoF metric for any
multivariate book feature, the paper's own Figure 5 (out-of-sample RMSE
rising while adjusted R2 and in-sample RMSE improve) is the
counterexample already on file. Multicollinearity screening,
estimator-mode pre-declaration, GoF pre-declaration, holdout discipline,
and nothing-measured prevented all of it.

## Standing caveat

All quantitative content is 6 liquid Nasdaq stocks, one calendar year
(2016), one venue, 10-second windows, contemporaneous explanation of
mid-price changes, no costs, no execution, hidden liquidity excluded,
lambda selected per window by cross-validation on the same windows.
Nothing transfers to any venue the programme measures; nothing enters
any spec, default, kill line, threshold, or generative null. Laundering
directions named: INTO — the Ridge-versus-OLS estimator lesson, the
overfitting exhibit, and the metric-dependence of the CKS contradiction
enter as read discipline reinforcing standing rules; OUT — no beta_m,
no lambda, no RMSE figure, no 65-75 per cent range, no MLOFI definition
change, and no "deep levels matter" sentence is ever cited as expected
behavior of any market the programme measures, or as evidence that any
programme feature carries information. Nothing measured, no kill line
moved, nothing armed, nothing trades live.
