# Deep-read note — library session 97 ("Asymmetric excitation of left- and right-tail extreme events probed using a Hawkes model: application to financial returns")

- Session: null-time deep-read session 97 (null-time session 107, log ## 128),
  2026-11-22.
- Authors: Matthew F. Tomlinson, David Greenwood, Marcin Mucha-Kruczyński.
- Title: "Asymmetric excitation of left- and right-tail extreme events probed
  using a Hawkes model: application to financial returns".
- Venue/id: arXiv:2011.12291v2 [q-fin.ST], 10 Aug 2021 (dated 12th August 2021
  on the title page; slug x55e853, per docs/library/expanded_index.json).
- What it is, one clause: a two-tailed peaks-over-threshold (2T-POT) marked
  Hawkes study estimating asymmetric self- and cross-excitation between extreme
  daily gains and losses of the S&P 500 index, finding extreme losses excite
  about twice as strongly as gains while their excitation decays about five
  times faster.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x55e853_asymmetric_excitation_of_left_and_right_tail_extre.txt,
~15 pp., page-marked). Next UNREAD triage-rank entry (score 20, seventh of
the score-20 tier, verified note-less this session against the live listing).

## The paper in one paragraph

The paper defines exceedances of fixed thresholds — the 2.5% and 97.5%
training-period sample quantiles, u← = −0.01840 and u→ = +0.01872 — of S&P 500
daily log-returns (1959-10-02 to 2020-11-20, Yahoo Finance; training to
2008-09-01, forecast after; PDF pp. 4-5) as left- and right-tail events of
Hawkes-type point processes, with exponentially decaying kernels, a quantile
impact function κ on the excess magnitudes, and conditionally scaled GPD
excesses σ⇌(t) = ς⇌ + η⇌[λ⇌(t) − µ⇌] (PDF pp. 2-3, eqs. 5-10), subcriticality
stated as spectral radius ρ(Γ) < 1 of the branching matrix (PDF p. 3). Four
nested forms are compared by log-likelihood, AIC/BIC, likelihood-ratio tests
and Ogata residual analysis (PDF pp. 5-9, Tables III-V): a decoupled bivariate
model worst, a symmetric common-intensity model next, and the two asymmetric
2T-POT models best, with the common-intensity form θci preferred in training
and the bivariate in forecast but statistically indistinguishable (Table IV,
PDF pp. 6-7), the authors inferring that both tails share one conditional
arrival intensity (PDF p. 6). The headline asymmetries: γ↔←/γ↔→ = 2.2 ± 0.5 —
an extreme loss triggers about twice as many daughter events (of either tail)
as an extreme gain — while β←/β→ = 4.6 ± 1.2, so loss-excitation decays about
five times faster, read as negativity bias (abstract; PDF p. 7; PDF p. 10).
Appendix A fits the same machinery to GARCH-normalized residuals: even with
the GJR leverage effect the iid-residual null is rejected (Fig. 9, PDF
pp. 11-12), the leverage effect can reproduce the γ asymmetry but not the β
asymmetry across all four GARCH variants (Tables VII-VIII, PDF pp. 12-13).
Appendix B verifies L-BFGS-B estimates against PyMC3 MCMC posteriors
(PDF pp. 13-14). References through [52] (PDF pp. 14-15).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The paper prints a live multitype case of the
   branching-ratio stationarity discipline, and its fitted tables reward the
   discipline's check rather than its headline. The subcriticality condition
   is correctly stated as spectral radius ρ(Γ) < 1, not as a per-type
   reproduction count (PDF p. 3). Yet the fitted tables imply that an extreme
   loss is a mother whose expected daughters number γ↔← = 1.2 ± 0.1 under
   θci (Table II, PDF p. 6), equivalently 0.58 + 0.60 = 1.18 summed across
   the bivariate Γ's left-mother column (Table I, PDF p. 6) — above unity —
   while the process is stationary only because the balanced type mix keeps
   the total reproduction at (1.2 + 0.54)/2 ≈ 0.87 (and the θbi spectral
   radius at ≈ 0.82, arithmetic on the printed table values, no data touched).
   A future multitype self-excitation score must check spectral radius on the
   fitted matrix, never read a type-conditional reproduction above one as
   regime criticality. This is exactly the branching-ratio / n = ∫µ discipline
   (deep-read 95's survey note; log ## 126, ## 127 findings 1), now with a
   printed multitype instance where the honest headline survives only because
   the check is the spectral one. No queue change.
2. [interpretation caution] The residual diagnosis the paper itself prints:
   lag-1 autocorrelation peaks localized to the tail ends of the 1973-4,
   Black Monday and 2007-9 clusters mean systemic over-forecasting late in
   high-activity regimes, and the authors' stated cause is that neglected
   non-constant exogenous intensity forces all excess intensity into
   endogenous self-excitation, inflating the branching elements — "rather
   than being the mechanism by which the system reaches the excited state,
   self-excitement may more so be the mechanism by which the excited state
   persists" (PDF pp. 9, Fig. 7 on PDF p. 10). Printed support for the
   endo-exo / apparent-criticality reading discipline already standing (the
   apparent-criticality read lineage; the estimator-mode freeze): any future
   endogeneity estimate fitted across regime onsets is an upper bound until
   exogenous intensity is modelled, and the instigation/persistence split is a
   reading the paper itself concedes it cannot resolve with its fit. No queue
   change.
3. [interpretation caution] Threshold and normalization configuration does
   measurable work in the headline, all of it pre-declarable and none of it
   new. Constant quantile thresholds on raw returns with no volatility
   normalization guarantee a balanced 50/50 left/right training split but
   produce a 168:124 left/right forecast split under a drifting return
   distribution, which the paper flags and defers (PDF p. 8). Appendix A
   shows the alternative is worse: POT Hawkes on GARCH-normalized residuals
   is "highly sensitive" to the volatility-model assumptions, and with the
   leverage term the fitted decay constant β→^-1 is of order 10³ trading
   days, "the model is reflecting a long timescale variation that is not
   naturally described by a Hawkes-type self-exciting process" (PDF pp. 10-12,
   footnote 2 on PDF p. 12). Both branches — constant thresholds on raw data
   and model-normalized residuals — carry a declared configuration choice
   that changes the fitted asymmetries; the threshold-grid pre-declaration and
   the grain-attribution diagnostics for this are already frozen in the
   estimator-configuration freeze (deep-read 63; reaffirmed as a
   rate-identity diagnostic at deep-read 96, log ## 127 finding 2). No queue
   change.
4. [interpretation caution] Nothing here bears L2 information, and the
   negativity-bias asymmetry claim cannot license anything programme-side.
   Daily closing-price index returns, one market, quantile thresholds and a
   1959-2008 training window with a forecast window dominated by GFC and
   Covid (PDF pp. 4-5, 8-9); the "twice as many daughters" headline is indexed
   to that configuration, and the paper's own left-tail residual excess
   magnitudes fail the KS test against the model, attributed to
   underestimation of λ← at cluster onsets in GFC and Covid (Fig. 5, PDF
   p. 9) — a printed failure of the model at exactly the moments the macro
   synthesis would care about. The daily grain is already bracketed by the
   queued C1-L2 base-rate confrontation; the empirical asymmetry claims are
   recorded as standing context only, never as support for any program claim —
   the library-is-ammunition caveat binds. No queue change.
5. [source-quality note] arXiv v2, 15 pages, referee-acknowledged and
   formatted for Physical Review E ("we thank the anonymous referees", PDF
   p. 10); the extraction garbles several table subscripts (the γ and β
   submatrices of Tables I-II required cross-reading against eqs. 3-11 and
   the paper's own ratio statements on PDF p. 7), the KS p-values of Figs. 1,
   5 and 9 are typographically mangled in the extract, and one author is
   affiliated with CheckRisk LLP (industry, PDF p. 1). Single asset, single
   index, no out-of-market replication; check the published version before
   formal citation. No queue change.

## What this paper would have killed if we had done it wrong

Without the spectral-radius discipline, a future multitype self-excitation arm
would have read γ↔← = 1.2 as printed evidence that loss-driven excitation is
supercritical, laundering a type-conditional reproduction count into a regime
discovery, when the process is stationary only because right-tail events
reproduce below unity and the spectral check — the one the paper itself
declares as the correct one (PDF p. 3) — puts the cascade at ≈ 0.82-0.87.
Without the endo-exo reading discipline, the localized lag-1 ACF peaks the
authors honestly print as over-forecasting (PDF pp. 9-10) would have been
tuned away as model refinement instead of standing as the paper's own
evidence that branching elements fitted across regime onsets are inflated
upper bounds. Without the frozen-configuration discipline, the
constant-versus-normalized threshold choice — which visibly flips the
headline asymmetry's composition between the raw-return fit and every
GARCH-residual fit (PDF pp. 8, 12, Tables VII-VIII) — is exactly the
researcher degree of freedom the estimator-configuration freeze exists to
remove: the same asymmetry story can be manufactured or dissolved by the
residualization choice. And without the library-is-ammunition caveat, the
"negativity bias in markets" interpretation would have entered the record as
an established market property, when what is printed is a good
within-Hawkes-family, single-index fit whose left tail fails its own residual
test in the two crisis regimes the macro synthesis would most need it for.

## Standing caveat

Everything is daily-grain, single-index, closing-price data; nothing transfers
to intraday or book-level claims without independent measurement, and both
the model family and its comparisons are within-family: the symmetric and
decoupled forms are nested constraints of the same 2T-POT machinery, so the
AIC/BIC/LRT hierarchy certifies only that asymmetric common-intensity Hawkes
beats simpler Hawkes, not that Hawkes is the data-generating process (PDF
pp. 5-7). The γ-asymmetry is reproducible by GJR-GARCH leverage alone, so
only the β-asymmetry is novel to the model family (PDF pp. 7, 12-13), and
the interpretation of that β-asymmetry as psychology (negativity bias) is
the authors' speculation, not a measured causal claim (PDF p. 10). Residual
concerns the authors print and leave open: discretization error at small
∆τ (PDF pp. 7-8), the un-modelled long-term distribution drift behind the
168:124 forecast split (PDF p. 8), and the left-tail residual-excess KS
failure in the crisis clusters (PDF p. 9). arXiv v2; the extraction's
table-subscript garbles mean every number used here was cross-checked
against eqs. 3-11 and the ratio statements on PDF p. 7; check the published
version before formal citation.
