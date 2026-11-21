# Deep-read session 72 (null-time session 83, log ## 92) — the Guo–Remillard–Swishchuk multivariate general compound point process paper read; the "as good as Hawkes" claim shown to be a variance-scaling fit on a single 2012 trading day with every limit-theorem premise assumed rather than tested, the parameter n shown to conflate the state count with the asymptotic scaling variable, and the "mid-price prediction" shown to be a rolling re-estimation of a diffusion coefficient with a 15.46% test error and no directional content; nothing sharpened

Qi Guo, Bruno Remillard, Anatoliy Swishchuk, "Multivariate
General Compound Point Processes in Limit Order Books"
(arXiv:2008.00124v1 [q-fin.MF], 4 August 2020; 16 pp.). A
stochastic-modelling paper: the LOB mid-price is written as a
d-dimensional compound point process S_t whose state jumps are
ergodic Markov-chain values X_{i,k} driven by a general multivariate
point process N_t (assumptions 2.0.1-2.0.2, PDF pp. 4-5), and the
paper proves a LLN (Thm 3.1), an FCLT I with random centralization
(Thm 3.2, PDF pp. 6-8) and an FCLT II with deterministically
centralized order flow (Thm 4.1, PDF pp. 11-12), yielding the
working approximation S_{nt} ~ sigma* Lambda^{1/2} W(t) sqrt(n) +
a* N_{nt} (Remark 3.3, eq. 26) and its forecast-relevant variant
S_{nt} ~ sqrt(n) sigma* Lambda^{1/2} W_1 + sqrt(n) a* Sigma^{1/2}
W_2 + a* n t lambda-bar (eq. 34). Numerics: LOBSTER level-1 data
for MSFT/INTC/AAPL/AMZN/GOOG on one day, 21 June 2012 (PDF pp. 6-8);
two-state (up/down tick) Markov chains for INTC/MSFT, 2-state vs
7-state for AAPL/GOOG/AMZN (PDF pp. 9-11), comparisons against the
multivariate general compound Hawkes process on standard deviations
across window sizes 0.1-12 seconds and 10 seconds-20 minutes (Figs.
1-5, Tables 4-7), plus a 5-fold rolling cross-validation of the
diffusion coefficient on the last 50 minutes of each name (PDF p.
14, Table 8).

Read 2026-11-21, against ONE question: what here would kill C1-L2
or C8 faster, or change their kill lines? Source: the library's
page-marked text extract
(docs/library/text/xd0900e_multivariate_general_compound_point_processes_in_l.txt,
16 pp., read in full). Next UNREAD triage-rank entry (score 25,
xd0900e), per the recorded ## 91 pointer and re-verified against the
live main file state this session: the score-25 tier read status on
main is x074d5c (read, ## 85), x8f729f (read, ## 87), x6b73c4 (read,
## 88), x475f30 (read, ## 90), x6aed5b (read, ## 91), then xd0900e —
the pointer is correct, the extract exists, is page-marked, and was
read in full.

## One-paragraph summary

The paper generalizes the compound Hawkes mid-price model by
replacing the Hawkes intensity with an arbitrary multivariate point
process assumed only to satisfy a LLN and an FCLT (PDF pp. 2-5),
proves the resulting two diffusion limits (PDF pp. 6-8, 11-12), and
fits them by matching theoretical to empirical standard deviations of
mid-price increments across window sizes for five names on one 2012
LOBSTER day, reporting coefficient percentage errors under 5-7% for
INTC/MSFT/AAPL/GOOG and 22-28% for AMZN (Tables 5-7), near-parity of
cost with the Hawkes version (Table 4: MSE differences of order
10^-8 against standard deviations of order 10^-2/10^-3), and a
rolling 5-fold cross-validated test error of 15.46% overall against
a 7.92% in-sample error (Table 8), which the authors advertise as
"good prediction in the LOB" (PDF p. 14). Every empirical claim
rests on a single trading day in five large-cap names, on analyst
choices of window grid, state count (2 or 7, with the 4-7 range
imported from a different paper on different data, PDF pp. 9-10),
and on premises 2.0.1-2.0.2 that are assumed for the unspecified
point process and never checked against the data used.

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The entire limit structure is
   conditional on assumptions 2.0.1-2.0.2 — a LLN and an FCLT for
   the underlying multivariate point process (PDF pp. 4-5) — and the
   paper is explicit that "the MGCPP is... a generalization for all
   multivariate compound models whose point processes N_t satisfy
   the assumptions 2.0.1 and 2.0.2" (Remark 3.6, PDF p. 11). Nothing
   in the paper identifies the point process or verifies those
   premises on the data; subcriticality/stationarity content is
   inherited by assumption, not tested. This is the already-queued
   price-process-family and estimator-identity family with another
   concrete instance: a diffusion coefficient fitted to a theorem
   whose premises were assumed is a fit to the assumption, and a
   C1-L2 or C8 statistic built that way would pass its kill lines
   for construction reasons. No queue change.

2. [interpretation caution] The headline "MGCPP is as good as
   MGCHP" is a variance-scaling parity, not a validation: the
   comparison is standard deviations of the two FCLT sides across
   window sizes (eq. 25, PDF p. 8), MSEs of order 10^-8 against
   standard deviations of order 10^-2 to 10^-3 (Table 4), and
   least-squares sqrt-time coefficient errors of 3.4-4.7% for
   INTC/MSFT (Table 5). No direction accuracy, no levels, no order
   of the price path, only the second moment's scaling with clock
   time. Reading discipline for any future C8 macro-synthesis
   exhibit: a model matching diffusion scaling is not evidence it
   anticipates anything. No queue change.

3. [interpretation caution] The forecast claim is weak by the
   paper's own numbers: the rolling 5-fold cross-validation targets
   the same diffusion coefficient, not the mid-price path, and
   yields a 15.46% overall test error, nearly double the 7.92%
   fit error (Table 8, PDF p. 14), with per-fold errors as high as
   42.15% (AMZN fold 5). The authors' conclusion that this "is
   still a good prediction in the LOB" (PDF p. 14) is a variance
   re-estimation being marketed as forecast. FCLT II itself is
   motivated by the admission that the FCLT I approximation
   "cannot help us with the forecasting task directly because we
   couldn't have the order flow N_{nt} in advance" (PDF p. 11) —
   the paper's own statement that the setup carries no anticipation
   content usable ahead of the flow. No queue change.

4. [interpretation caution] The asymptotic variable n is
   over-loaded: the limit theorems are stated as n -> infinity for
   Markov chains "with n states {1,...,n}" (Thm 3.2, PDF pp. 6-7;
   Thm 4.1, PDF p. 11), and the same n scales the time horizon in
   the approximations (eqs. 25-26, 34-35), while the numerical work
   fixes n at either 2 or 7 states and interprets accuracy as a
   function of that analyst choice, with the "best number of states
   is 4 to 7" range imported from a companion Hawkes paper on
   other data (PDF pp. 9-10) and AMZN failing under 10% error at
   every state count (28.29% at 7 states, Table 6). A scaling limit
   whose premise is large n, evaluated at n = 2 or 7 on a single
   day, has unexamined finite-n bias built into every fitted
   coefficient. This is the window/level-declaration family and
   the estimator-identity family again; no new item.

5. [reinforcing, no new item] Single-day, single-venue, five
   large-cap NASDAQ names, 21 June 2012, LOBSTER level-1 (PDF pp.
   6-8): regime breadth is nil, the day is a decade and a half
   stale, and no cross-market or cross-period replication exists
   in the paper. Any programme use of these numbers as base rates,
   diffusion scales or cross-asset correlation structure (Lambda,
   Sigma) would be importing one day's geometry as if it were a
   property of markets. Reinforces the base-rate audit family; no
   queue change.

6. [source-quality note] arXiv v1, theorem-plus-numerics draft, no
   recorded citations in the acquisition index, no published version
   found for this exact title; the companion MGCHP result appears
   in Wilmott magazine 2020 (ref. [14]) — check both before any
   formal citation. The numerics carry no evidential weight in this
   programme regardless (the library is ammunition, not evidence);
   the generalizable content is the failure-mode map: assumed limit
   premises, asymptotic conflations, variance-fit marketed as
   forecast.

7. [cost-survival ammunition] The multivariate dependence entering
   only through Lambda and Sigma in the diffusion limit (Thm 3.2,
   PDF pp. 6-8) means cross-name contamination is confined to two
   matrices whose estimators inherit every fault above; any future
   K7-style cost-survival or cross-asset layer would have to carry
   its own day-breadth and premise-verification assumptions;
   recorded as an assumption class only, nothing operationalized,
   nothing armed.

## What this paper would have killed if we had done it wrong

If the programme had no estimator-identity discipline, this is the
shape of paper that launders a fitted second moment into a
predictive model: "good prediction in the LOB" would have entered
the record as evidence of anticipation, when the tested quantity
is a diffusion coefficient whose 15.46% out-of-sample error is
against itself, on one day, under premises assumed rather than
checked, at an asymptotic n the empirical work contradicts. A C8
macro-synthesis exhibit built on similar ingredients — untested
process assumptions, analyst-set state counts, variance scaling read
as forecast — would pass every kill line for construction reasons
and fail them nowhere. The estimator-identity family, the
price-process-family invariance rule (#38) and the base-rate audit
family are the existing immune response; this paper is a further
confirmed case of the disease they fence off, not new medicine.

## Standing caveat

Everything empirical here is one trading day (21 June 2012), five
large-cap NASDAQ names, LOBSTER level-1, with 2- or 7-state Markov
chains chosen by reference to a different paper, window grids chosen
by the authors, and the assumed-not-proven 2.0.1-2.0.2 premises
carrying the whole limit structure. The math (LLN, FCLT I/II under
stated conditions) is standard and may be cited for the conditional
statements only. Nothing in this paper is admissible as support for
any programme claim, predictive or otherwise; it is usable only as
a map of failure modes (assumed limit premises, asymptotic-variable
conflation, variance-fit sold as forecast, single-day parameter
estimates) that C1-L2 and C8 pre-declarations must continue to
fence off.
