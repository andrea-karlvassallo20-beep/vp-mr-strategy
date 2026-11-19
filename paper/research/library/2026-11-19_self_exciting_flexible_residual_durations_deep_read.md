# Deep-read: Forecasting duration in high-frequency financial data using a self-exciting flexible residual point process (Lee)

Null-time session 66 (log ## 70), deep-read session 55. Kyungsub Lee,
"Forecasting duration in high-frequency financial data using a
self-exciting flexible residual point process," arXiv:2604.00346v2
(v2 dated 18 Aug 2026, per PDF p. 1), Department of Statistics,
Yeungnam University. A single-author statistics paper that formalizes
the author's Lee (2025) "flexible residual" point process — a
self-exciting, exponentially decaying latent intensity driven by
non-exponential i.i.d. residuals through an integrated-intensity
transform — proves its stochastic stability as a positive Harris
recurrent Markov chain, and benchmarks SE/ACD/log-ACD variants with
exponential, Gamma, generalized-Gamma and Burr residuals on one month
of AAPL one-tick mid-price-change durations.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x72c407_forecasting_duration_in_high_frequency_financial_d.txt,
~33 pp., page-marked). Next UNREAD triage-rank entry (score 28).

## The paper in one paragraph

Definition 1 (PDF pp. 3-4) embeds ACD, log-ACD, log-ACI and Hawkes in one
event-time Markov framework: the interarrival time is the inverse
integrated-intensity transform of an i.i.d. residual given the state,
with the state updated by a drift function. Definition 6 (PDF p. 7)
specializes to the self-exciting exponentially decaying flexible
residual process: the latent intensity jumps by alpha at each event and
decays at rate beta between events, with the residual mapped through
the integrated intensity phi; the unit-exponential special case
recovers the exponential Hawkes process exactly (Definition 7, PDF
p. 7). Section 2.3 shows the compensator residual is standard
exponential by the random time change theorem (PDF p. 8), and the
log-likelihood is the standard intensity-based one (PDF p. 9).
Section 3 derives the linear representation (PDF p. 10), motivates the
stability condition alpha < beta*mu-epsilon (Remark 1, PDF p. 7;
necessity argument, PDF p. 10), and proves irreducibility,
aperiodicity and positive Harris recurrence with a Foster-Lyapunov
drift, yielding a unique stationary distribution and the stationary
mean duration in closed form (Theorem 2, PDF p. 11; proofs, PDF
pp. 28-33). The empirics define durations as one-tick mid-price changes
(AAPL, December 2022, 1,023,480 events, mean 0.48s, median 0.13s,
over-dispersion 2.07, kurtosis 61.5, Table 1, PDF p. 12), fit
SE/ACD/log-ACD each with Exp/Gamma/gGamma/Burr residuals (Table 2, PDF
p. 15), forecast 100 events ahead under rolling 5,000-event windows
re-estimated every 100 events (PDF p. 16), and compare by rRMSE,
R-squared, LRMSE, residual KS and Wasserstein (Table 3, PDF p. 17)
with Diebold-Mariano-Harvey tests against SE-Burr under two loss
functions (Table 4, PDF p. 19).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] Residual misspecification soaks into
   absurd parameter magnitudes: the exponential-residual SE (plain
   Hawkes) fit "compensates by inflating the baseline intensity and
   excitation parameters" (PDF pp. 14-15) — mu = 1.4768, alpha = 90.96,
   beta = 285.90 (Table 2, PDF p. 15) against SE-Gamma's
   0.27/0.09/0.11. A future L2/C8 fit whose scale parameters blow up
   is to be read as a residual-distribution red flag first and a
   market fact never; this is the estimator-discipline lesson with a
   magnitude attached. Reinforces the queued estimator-mode candidate
   and the frozen constants discipline; nothing added.

2. [interpretation caution] The same candidate is significantly best
   AND significantly worst depending on the declared loss: SE-Burr
   rejects equal predictability in its favor under squared relative
   error (Panel A, all mean loss differentials negative) and against
   itself under log-ratio squared error (Panel B, all positive), both
   at 1% (Table 4, PDF p. 19; stated with the loss reading, PDF p. 18).
   Any future model-comparison verdict — including a C1-L2 baseline
   comparison — must carry its loss function pre-declared; a ranking
   that flips sign with an undeclared metric choice is manufactured by
   metric selection. Reading discipline only; no queue change.

3. [reinforcing, no new item] Dependence fit does not buy forecast
   gain: the fractionally integrated log-ACD "essentially eliminates
   residual autocorrelation across all lags" (PDF p. 22) yet does not
   improve out-of-sample forecasts (Table 3, PDF p. 17), and even the
   best flexible models fail the residual KS at 1% across every
   specification in Table 3 (PDF p. 17) with P-P misfit acknowledged
   as remaining (PDF pp. 19-20). Reinforces the refusal of
   fit-complacency and the burden-of-proof orientation: no future C8
   diagnostic may read a cleaned ACF as a passed model. Nothing added.

4. [interpretation caution] The stability condition alpha <
   beta*mu-epsilon is residual-distribution-relative: the
   branching-analog ratio and any non-explosion check computed under
   one fitted residual law do not transfer to another. Finding 1's
   re-expression is the demonstration: the same data and dynamics
   produce the same fit at wildly different parameter vectors under
   two residual laws. Any future stability or non-explosion check on a
   fitted Hawkes arm must state which residual distribution the mean
   is taken under, or the check is not a check. No queue change; this
   is a reading discipline on the existing kill-line apparatus.

5. [source-quality note] Single author, arXiv-only (v2 Aug 2026),
   zero citations in our index, the model itself introduced in the
   author's own Lee (2025) (PDF pp. 3, 7), one asset (AAPL), one
   month (December 2022), no code or data statement beyond the LOB
   description, and a near-degenerate Burr identification on the
   self-exciting fits (s1 = 273.95 with SE 0.1444, Table 2, PDF p. 15;
   s1 = 363.29 for logACD-Burr) — shape parameters at an estimated
   magnitude implying a second moment the table does not discuss.
   Solid statistics-paper methodology; evidence scope is one month of
   one equity. Its empirical numbers are ammunition under the library
   invariant, never evidence for any programme claim. Check for a
   published version before any formal citation outside this note.

## What this paper would have killed if we had done it wrong

The parameter-soak death: a future C1-L2 or C8 fit reporting
"ultra-fast decay" or "explosive self-excitation" from inflated
estimates — this paper's own Table 2 (PDF p. 15) shows the same data
and same dynamics producing beta = 285.9 under exponential residuals
and beta = 0.107 under Gamma residuals — read as a market fact by an
analyst who never ran the residual diagnostics. The metric-shopping
death: declaring a benchmark "beaten" off Table 3 alone while Table 4
(PDF p. 19) shows the verdict inverting at 1% significance under the
other loss. Both are pre-empted by the frozen-constants discipline,
the pre-declared metric set in the specs, and the queued
estimator-mode and residual-diagnostic candidates; neither moves any
kill line.

## Standing caveat

arXiv version only (v2, Aug 2026); check the published version before
any formal citation. The Markov-chain theory (PDF pp. 28-33) is
assembled from standard Meyn-Tweedie results. The empirical window is
one asset, one month, equities only: nothing licenses transfer to
tick-scale futures L2 microstructure without re-derivation. The
rolling 5,000-event window and 100-event advance (PDF p. 16) are the
author's stability standards, not published rules; the Burr
shape-parameter identifications near the boundary (Table 2, PDF p. 15)
are unexplored by the author. The paper forecasts durations, not
prices: no predictive claim about returns exists here, so nothing in
it is evidence for or against any programme claim; it informs
estimator discipline only.
