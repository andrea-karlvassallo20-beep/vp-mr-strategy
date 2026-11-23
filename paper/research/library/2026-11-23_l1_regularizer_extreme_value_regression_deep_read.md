# Deep-read session 103 — Hambuckers, Sun & Trapin (2023), "Measuring tail risk at high-frequency: an L1-regularized extreme value regression approach with unit-root predictors"

Authors: Julien Hambuckers, Li Sun, Luca Trapin. Venue: arXiv:2301.01362v1
[econ.EM], 3 Jan 2023. One clause on what it is: a conditional extreme-value
econometrics paper — a dynamic GPD tail regression estimated at the 5-minute
grid, its shape and scale driven by lagged liquidity and volatility
covariates, with covariate selection by adaptive L1-regularized MLE, proved
oracle-consistent under both stationary and local unit-root predictors, then
applied to nine liquid US stocks.

Read 2026-11-23, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xf959b8_measuring_tail_risk_at_high_frequency_an_l_1_regul.txt,
~24 pp., page-marked). Next UNREAD triage-rank entry (score 20, thirteenth of
the score-20 tier).

## The paper in one paragraph

The model is dynamic peaks-over-threshold: negative 5-minute returns are
compared to a threshold u_t defined as the 90%-quantile of losses over a
moving window h, with twelve window lengths from one week to twelve weeks
(PDF p. 13), and exceedances are fitted to a GPD whose time-varying shape
k_t is bounded 0 < k_t < 0.5 by a logit link "to ensure a finite conditional
variance" (eq. 3, PDF p. 3) and whose log scale carries an autoregressive
term plus a linear predictor of lagged covariates (eq. 4, PDF pp. 3-4).
The methodological core: with local unit-root predictors the MLE stays
consistent but its limit is NON-NORMAL (Theorem 2, PDF p. 6), and the paper
prints three reasons t-test covariate selection is inadmissible in exactly
this setting — type-I error cannot be controlled, size distortion selecting
unit-root predictors is severe, and power for shape coefficients is low
(PDF pp. 6-7) — then proposes a two-step adaptive L1-regularized MLE
(ALMLE) with the oracle property for both stationary and local unit-root
predictors (Theorem 4, PDF p. 9), tuned by AIC/HQ/BIC over a lambda grid
(PDF p. 7). Simulations over the DGPs show t-tests selecting truly
INACTIVE unit-root covariates at rates "much higher than α = 0.05 ...
regardless of the DGP" (PDF p. 11), printed at essentially 1.0 in the
Table 2 false-positive columns while ALMLE with BIC achieves near-perfect
correct selection (Table 2, PDF p. 14). Empirics: nine liquid US stocks
(AXP, BA, GE, HD, IBM, JNJ, JPM, KO, XOM), all transactions 2006-2014,
42 liquidity and volatility predictors. The headline: tail SEVERITY (k) is
"strongly associated to low price impact in periods of high volatility of
liquidity and volatility of volatility" (conclusion, PDF p. 21) — the
Amihud-type impact measures carry negative coefficients −0.91 to −1.79 on
most of the nine stocks (Tables 5-6, PDF pp. 17-18), i.e. LOW impact
predicts a FATTER tail, and the sign pattern is stable for the shape
equation. The contrast that carries the lesson: the same data under plain
MLE selects 39-42 of 42 predictors in the shape equation and 43 of 43 in
the scale equation, all coefficients nonzero, while "we cannot compute the
corresponding standard errors because the obtained Fisher information
matrix of the MLE is not positive definite. This makes variable
interpretation very difficult if not impossible" (Tables 7-8, PDF
pp. 19-20; PDF p. 16). Out of sample, one-step VaR forecasts at levels
0.90-0.9999 track nominal coverage closely everywhere (by construction:
the threshold is the rolling 90% quantile), and the K-S test of the
fitted GPD rejects the regression model on THREE of nine stocks at the 1%
level (GE p = 2.68e-12, XOM p = 6.32e-8, HD p = 0.0023, with BA at the 5%
edge p = 0.0431; Table 9, PDF p. 21).

## Findings, graded (does any kill line move?)

NO kill line changes. ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The conditional-tail
   covariate-integration pre-declaration: BEFORE the L0 gate, any
   C1-L2/C8-adjacent conditional extreme-value model — a GPD/POT tail
   regression, a time-varying tail-shape or tail-scale spec, any
   covariate-conditioned exceedance or severity model — must pre-declare,
   as frozen configuration counted in the multiplicity ledger, (i) the
   integration order of every candidate covariate (I(0), I(1),
   local-to-unit-root), declared and recorded BEFORE estimation, with
   local unit-root covariates flagged and their coefficients read under
   the local (√T-standardization, PDF pp. 4-5) limit rather than as
   ordinary fixed-parameter estimates; (ii) the covariate-selection
   procedure as frozen configuration, with t-test selection from an
   unregularized conditional-tail likelihood INADMISSIBLE by rule; and
   (iii) for any regularized selection actually used, the tuning criterion
   (AIC/HQ/BIC/other) frozen with the penalty set, never silently
   re-tuned per instrument. The paper proves the failure class is real
   in print, three times over: the unregularized MLE's limit is
   non-normal under local unit-root predictors so t-statistics have no
   controlled meaning (Theorem 2, PDF p. 6, with the three printed
   inadmissibility reasons, PDF pp. 6-7); the simulations show t-tests
   selecting truly inactive unit-root covariates at rates up to
   essentially 1.0 rather than the nominal 0.05 (PDF p. 11; Table 2,
   PDF p. 14); and on the paper's own nine-stock data the unregularized
   MLE selects nearly everything while its Fisher information matrix is
   not positive definite, so standard errors are not computable at all
   (Tables 7-8, PDF pp. 19-20; PDF p. 16). Harder-to-pass because a
   future C8 conditional-tail covariate claim riding on unregularized
   t-statistics — today survivable as an ordinary regression finding
   indistinguishable from a real one — now fails at the gate BEFORE any
   data is touched, where no queued rule asks the question: the
   estimator-implementation concordance rule (deep-read 85) audits
   implementation against the written definition and says nothing about
   the selection procedure's own size behavior; the
   estimator-configuration freeze (deep-read 63) freezes the estimator's
   configuration but not the admissibility of selection methods; the
   pre-registration family (primary-metric pre-commitment, deep-read 55;
   base-rate confrontation; regime-window pre-declaration) freezes
   metrics and windows, not covariate order classes. Tightens the
   concordance rule (deep-read 85) by extending the audit from
   implementation-vs-definition to selection-procedure-vs-its-own-size
   under the declared covariate classes, and joins the
   estimator-configuration freeze (deep-read 63) and the
   primary-metric pre-commitment (deep-read 55) in closing a researcher
   degree of freedom that alone can manufacture a finding.
2. [interpretation caution] The shape bound is a prior, not a result:
   k_t is imposed into (0, 0.5) "to ensure a finite conditional variance"
   (PDF p. 3), so this entire model family cannot express
   heavier-than-finite-variance tails, and any conditional-tail estimate
   it produces is conditional on that support bound. Compounding it,
   coefficients on local unit-root predictors are local-to-zero order
   under the √T standardization (PDF pp. 4-5): a printed "significance"
   for a persistent covariate means something categorically different
   from the stationary case. Recorded as context; no queue change.
3. [interpretation caution, cost-survival ammunition] Even with oracle
   selection, 42 covariates, and nine mega-liquid stocks, the
   out-of-sample K-S test rejects the conditional GPD on three of nine
   instruments at 1% (GE 2.68e-12, XOM 6.32e-8, HD 0.0023, BA 0.0431 at
   the 5% edge; Table 9, PDF p. 21), while empirical coverage sits near
   nominal everywhere because the threshold is a rolling 90% quantile by
   construction (PDF p. 13): calibration-by-construction with fit
   rejection on a third of its own universe is the honest printed
   ceiling of the conditional-tail genre at exactly the grain C8 would
   work — a "passes everywhere" expectation for any future C8
   conditional-tail layer is not printed anywhere here and must not be
   assumed into a kill line. The empirical headline — severity linked
   to LOW price impact under high vol-of-liquidity and vol-of-vol
   (Table 5, PDF p. 17; conclusion verbatim, PDF p. 21) — is descriptive
   ammunition for C8's covariate shortlist (impact, vol-of-liquidity,
   vol-of-vol) and NEVER program evidence: conditional association, one
   asset class, in-sample, bounded shape, rejected out-of-sample on
   three of its own nine instruments.
4. [reinforcing, no new item] The MLE comparison is the
   estimation-discipline family's whole case in one table set: 39-42 of
   42 shape predictors and 43 of 43 scale predictors "selected",
   coefficient signs flipping stock to stock, standard errors
   non-computable, interpretation "very difficult if not impossible"
   (Tables 7-8, PDF pp. 19-20; PDF p. 16). The autoregressive log-scale
   term is positive on all nine stocks (Table 8, PDF p. 20), the same
   level-persistence habit the queue's level-versus-memory
   disambiguation rule (deep-read 59) already guards. No queue change.
5. [source-quality note] arXiv v1 [econ.EM], 3 Jan 2023, zero citations
   in the index. Internal inconsistency: appendix Table 2 (PDF p. 14)
   reports DGP 5 and DGP 6 rows, but the simulation section defines
   exactly four DGPs ("four data generating processes", PDF p. 9; DGP
   1-4, PDF p. 10) and no DGP 5/6 definition appears anywhere in the
   text — resolve against a published version before formal citation.
   No queue change.

## What this paper would have killed if we had done it wrong

Without finding 1's pre-declaration, a future C8 covariate screen would walk
exactly into the paper's MLE comparison: 42 candidate covariates, nearly
all "selected", signs unstable instrument to instrument, no computable
standard errors, and a printed false-positive rate for persistent
covariates at essentially 1.0 — a liquidity-covariate "discovery"
manufactured by the selection procedure with no visible fingerprint in
the outputs. The matched-control and estimator-discipline design avoids
precisely this. And without the library-is-ammunition rule, the nine-stock
severity headline would enter the programme record as evidence that low
impact plus unstable liquidity fattens tails, when it is a conditional
association through a bounded-shape model that its own out-of-sample test
rejects on a third of its universe — ammunition for the covariate
shortlist, not a fact about markets.

## Standing caveat

Everything above is the arXiv v1 text (~24 page-marked PDF pages: header,
body, theory, simulations, all printed tables, appendix tables,
references complete; nothing skipped). The three theorems are the durable
content; the empirics are one asset class, in-sample, shape bounded a
priori, out-of-sample fit rejected on three of nine instruments. The DGP
5/6 definitional gap is unresolved in this version. Nothing here licenses
any C8 tail claim, any covariate claim, or any market fact; check the
published version before formal citation.

Nothing measured during this session. No kill line moved. Nothing armed.
Nothing trades live.
