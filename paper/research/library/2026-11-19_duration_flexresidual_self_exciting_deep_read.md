# Deep-read session 55 — Forecasting duration in high-frequency financial data using a self-exciting flexible residual point process

**Authors:** Kyungsub Lee (Department of Statistics, Yeungnam University).
**Full title:** Forecasting duration in high-frequency financial data using a
self-exciting flexible residual point process.
**Venue:** arXiv:2604.00346v2 [q-fin.ST], 18 Aug 2026 stamp, zero citations
recorded in our index. A paper that defines a self-exciting, exponentially
decaying point process with flexible (heavy-tailed) residual innovations,
proves its Markov-chain stability (positive Harris recurrence under
alpha < beta*mu_epsilon), forecasts one-tick mid-price-change durations on
AAPL LOB data, and compares it against ACD/log-ACD/log-ACI/FI-logACD
alternatives.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(`docs/library/text/x72c407_forecasting_duration_in_high_frequency_financial_d.txt`,
~33 pp., page-marked). Next UNREAD triage-rank entry (score 28).

## The paper in one paragraph

The paper builds a point-process family (Definition 1, PDF pp. 3-4) in which
interarrival times are tau_n = Phi^{-1}(eps_n, X_{n-1}) for i.i.d.
innovations eps_n and a latent state updated by tau_n; the self-exciting
exponentially decaying member (Definition 6, PDF p. 7) has latent
intensity Lambda_n = mu + (Lambda_{n-1} - mu + alpha) e^{-beta tau_n}, and
reduces to the exponential Hawkes process when eps is unit exponential
(Definition 7, PDF p. 7). Choosing Gamma, generalized Gamma, or Burr Type
XII residuals (all unit-mean constrained, PDF pp. 13-14) lets the model
carry the heavy-tailed duration distribution the exponential residual
cannot. The Markov chain {Lambda_n} is shown irreducible, aperiodic, a
T-chain, and positive Harris recurrent under the stability condition
alpha < beta*mu_epsilon via a Foster-Lyapunov drift argument (Theorem 2,
PDF p. 11; Propositions 3-6 and Lemmas 8-9, PDF pp. 28-33), with stationary
expected duration E[tau] = (beta*mu_epsilon - alpha)/(beta*mu) (PDF pp.
32-33). Empirically, on one month of AAPL mid-price durations (December
2022; 1,023,480 mid-price-change events, SD/mean over-dispersion 2.0698,
skewness 5.7536, kurtosis 61.4619, Table 1, PDF p. 12), rolling-window
5,000-event estimation shows the flexible-residual self-exciting
specifications beating exponential ones in goodness-of-fit, with SE-Burr
best at rRMSE and log-ACD/FI-logACD best at log-ratio RMSE (Table 3, PDF p.
17); formal Diebold-Mariano (Harvey et al. correction) tests against
SE-Burr reject equal predictability at 1% in BOTH loss directions (Table 4,
PDF pp. 18-19).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The evaluation-metric
   choice alone reverses the forecast verdict at 1% significance: under
   squared-relative-error loss every competitor is significantly worse than
   SE-Burr, and under log-ratio squared-error loss every competitor is
   significantly better (Table 4, PDF pp. 18-19), with both rejections at
   the 1% level. The paper's own summary is explicit that the two metrics
   "capture fundamentally different aspects of predictive performance" (PDF
   p. 18). Proposed amendment (the primary-metric pre-commitment): before
   the L0 gate, any C1-L2/C8-adjacent test spec must pre-declare its single
   primary evaluation metric or loss, named and frozen before the data;
   secondary metrics may be reported but can neither rescue a primary
   failure nor overturn a primary pass. It tightens rule 1 of the
   pre-registration discipline (the spec frozen before the data) by naming
   metric selection as a researcher degree of freedom that this paper shows
   is alone sufficient to flip a conclusion, and it makes future tests
   harder to pass: a skill comparison that fails its primary metric dies
   even if some post-hoc alternative metric flatters it. Killed-if-wrong
   counterfactual: if the rule is wrong, metric pre-commitment costs a
   genuine improvement that only a secondary metric could have surfaced —
   in which case the owner may amend the spec before the data, never after
   it. Full draft context: this note.

2. [reinforcing, no new item] Residual-distribution misspecification is
   absorbed into the dynamics parameters: the exponential-residual
   self-exciting fit compensates the AAPL duration over-dispersion by
   inflating mu, alpha, beta to absurd scales (alpha = 90.96, beta = 285.90
   with tiny standard errors, Table 2, PDF p. 15; the text calls this out
   explicitly, PDF pp. 14-15), while the flexible-residual fits sit at
   alpha, beta ~ 0.1 with stable estimates. A dynamic-parameter estimate is
   not evidence of dynamics until the residual specification is shown to
   fit; this reinforces the frozen-constants discipline and the queued
   estimator-mode candidate. Nothing added.

3. [reinforcing, no new item] The stability boundary is a residual-mean
   boundary: stationarity needs alpha < beta*E[eps] (Remark 1, PDF p. 7;
   Eq. 31 and pp. 32-33), and simulated duration persistence grows as
   alpha/beta approaches unity (PDF pp. 11-12, Fig. 1). Any future near-
   critical / near-unstable Hawkes reading is therefore fragile to the
   innovation-mean assumption itself, doubling the session-63 estimator-
   discipline lesson (the negative-resilience window paper) from the
   residual side. Reinforces the estimator-discipline family; nothing
   added.

4. [interpretation caution] Residual-diagnostic fit is not forecast skill:
   the FI-logACD long-memory model "essentially eliminates residual
   autocorrelation across all lags" (PDF p. 22) yet shows no out-of-sample
   gain (Table 3, PDF p. 17), while the Burr-tailed SE model wins on
   absolute-scale loss retaining residual dependence. Any future C8
   model-comparison argument must rest on the pre-declared primary metric
   (finding 1), never on residual ACF whitening or P-P-plot closeness
   (PDF pp. 19-21) as skill evidence. Reading discipline; no queue change.

5. [reinforcing, no new item] The AAPL mid-price duration distribution is
   violently heavy-tailed at the one-tick event grain (kurtosis 61.46,
   over-dispersion 2.07, PDF p. 12), and the event definition itself (a
   full one-tick mid-price move, i.e. two consecutive same-direction
   half-tick moves, PDF p. 12) materially shapes the target. A generative
   null, placebo, or simulator for L2 order-flow/price-arrival streams must
   reproduce the duration tail as a flow-dynamics statistic, not just event
   counts or static marginals — the queued dynamics-identification rule
   already requires exactly this, and this paper is a second market's
   evidence for why. Nothing added.

6. [source-quality note] Single-author arXiv v2 preprint, zero citations in
   our index, one asset (AAPL), one month (Dec 2022), rolling ~45-minute
   re-estimation windows, no code, no robustness across venues; the base
   model is the author's own Lee (2025), published in Methodology and
   Computing in Applied Probability (PDF p. 25), of which this paper is the
   LOB-forecasting application. Its "strong predictive performance"
   (abstract, PDF p. 1) is practitioner-grade, single-asset evidence and
   enters the record as ammunition under the library invariant, never as
   support for any programme claim. The paper is internally sound and its
   tables are internally consistent; check for a published version before
   formal citation outside the note.

## What this paper would have killed if we had done it wrong

The metric-shopping death: a future C1-L2 skill comparison whose verdict
was read off whichever loss function flattered the programme's prior, when
this paper demonstrates that two standard forecast metrics reject in
opposite directions on the same data at the same 1% level (Table 4, PDF pp.
18-19) — exactly the manufactured-result shape the primary-metric
pre-commitment forecloses. And the residual-laundering death: reading an
inflated alpha/beta from an exponential-residual fit (Table 2, PDF p. 15)
as evidence of genuine self-excitation dynamics in the L2 data, when the
parameters are absorbing a distributional misspecification the flexible
residuals expose. Both are pre-empted by finding 1's queued sharpening, the
frozen-constants discipline, and the already-queued estimator-mode
candidate; no kill line moves.

## Standing caveat

The model is univariate, event-time, exponential-kernel only; calendar-time
seasonality is handled by rolling re-estimation rather than modeled (PDF
pp. 4, 16), which makes the intraday "forecasts" partly a re-estimation
schedule rather than a stationary model claim. The framework is
observation-driven and rules out parameter-driven latent stochasticity by
construction (PDF p. 4). One stock, one month, December 2022 only;
duration-vs-forecast results at this grain say nothing about cross-sectional
signal content, which is the programme's question, not duration point
prediction. KS statistics reject at 1% for every specification including
the paper's own best (Table 3, PDF p. 17) — the authors say so honestly
(PDF pp. 19-20, citing Bauwens et al. 2004); no model here fits its own
data. Execution-strategy and prediction-engineering content, if any, is
engineering and is never operationalized; nothing trades live.
