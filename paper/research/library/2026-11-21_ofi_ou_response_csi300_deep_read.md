# Deep-read session 68 (null-time session 79, log ## 87) — the Hu–Zhang CSI 300 OFI-response paper read; the correlation-scaled drift construct shown to carry two analyst properties, the pooled forgetting constant shown to contradict the paper's own monthly memory table, and the (window, horizon) cells shown to manufacture factor rankings; nothing sharpened

Chen Hu and Kouxiao Zhang (both Guolian Futures, Shanghai), "Stochastic
Price Dynamics in Response to Order Flow Imbalance: Evidence from CSI 300
Index Futures" (arXiv:2505.17388v1 [q-fin.MF], 23 May 2025). A
modeling-plus-empirics practitioner paper: order flow imbalance is
treated as a step shock whose response is mean-reverting, the shock
process is represented as an Ornstein-Uhlenbeck process driven by a
symmetric Lévy process, the drift of a geometric Brownian motion is
replaced by that process, closed-form mean/variance/quasi-Sharpe
expressions are derived, and one year of CSI 300 index futures tick
data is used to grade OFI against other metrics across (window,
horizon) grids, in combination and by month.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change its kill lines? Source: legally acquired OA copy
(docs/library/text/x8f729f_stochastic_price_dynamics_in_response_to_order_flo.txt,
~37 pp., page-marked, complete, references and appendix included). Next
UNREAD triage-rank entry (score 25, x8f729f), per the recorded ## 86
pointer and re-verified against the file state this session: the
score-sorted triage file recomputed against the 67 notes and the log
tail, with the score-26 tier confirmed fully consumed and the only
earlier apparent gaps (score 29/48/48/42/41 entries) confirmed read via
their note headers. Session-state note, per the goal-autonomy conductor
protocol (edition 5, ## 83): the declared work choice is the standing
deep-read, the protocol's default, which owes no justification; the
synthesis cadence is NOT due — three deep-reads (## 84, ## 85, ## 86)
have landed since the edition-5 reset at ## 83, out of five; no other
front is claimable by a null-time session (the L2 deployment and its
data spend stay owner-side).

## The paper in one paragraph

The Cont-Kukanov-Stoikov order flow imbalance is reproduced verbatim
(OFI as the sum of event contributions e_n, eqs. 1-2, PDF pp. 4-5)
alongside trade imbalance (Lee-Ready, eqs. 3-5, PDF p. 5), Lambda
(price range over trades, eq. 6, PDF p. 6) and AvgEn (the differential
of the cumulative mean of e_n, eq. 7, PDF p. 6), on one year of CSI 300
index futures 500ms-snapshot ticks, about 6 million ticks (PDF pp. 4,
6). Contemporaneous in-window correlation of OFI with mid-price change
runs from 0.20 at 0.5s to 0.54 at 1h, holding ≈0.5 for every window
beyond 5 seconds (Table 2.1, PDF p. 6), while TI is near zero or
negative at short windows and positive only past 2 minutes, and Lambda
negative at 5-30s and positive past 2 minutes (PDF p. 6). The e_n series
shows near-zero skew and kurtosis ≈34 (Table 2.2, PDF p. 9), and its
autocorrelation decays roughly geometrically, which motivates
representing the OFI shock as an Ornstein-Uhlenbeck state with
ρ_k = e^{−θkΔt} (eqs. 8-9, PDF pp. 9-10), a decay the aggregation into
OFI windows inherits (eq. 10, PDF p. 10). The expected cumulative
impact of a shock is the geometric series E[S_n] (eq. 11, PDF p. 11),
scaled into a price-drift level by the observed correlation,
µ_total = OFI·ρ_k·(1−e^{−θt})/(1−e^{−θ}) (eq. 12, PDF p. 11), with the
pooled decay rate θ = 0.5 read off the one-year autocorrelation
(PDF p. 11). The price is then geometric Brownian motion whose drift
µ_t is itself an O-U process driven by a symmetric zero-mean
finite-second-moment Lévy process (system eq. 14, PDF p. 13), tied to
the shock level through µ_0 = OFI_0·ρ_k (PDF p. 13); the text concedes
W_t and L_t "may exhibit correlation" (PDF p. 13). Under those
assumptions the log-return mean is E[R_t] = µ_0(1−e^{−θt})/θ − σ²t/2
(eq. 20, PDF pp. 14-15), the variance follows eq. 22 with the derivation
assuming W⊥L independence (PDF pp. 15, 33), the ratio QS(t) of eq. 24
has an optimal holding time with the mean-return maximum at
t* = −ln(σ²/2µ_0)/θ (eq. 25, PDF p. 18; Appendix A.4, PDF p. 35), and
QS(t) ~ ((µ_0 − σ²/2)/σ)·√t near zero (Appendix A.3, PDF p. 34).
Empirics: LASSO regressions of window-aggregated OFI on forward
mid-price changes over an exhaustive (historical window 1-240 ticks,
forecast horizon 1-3600 ticks, i.e. 0.5s-30m) grid with a 4:1
train/test split and 5-fold CV (PDF p. 20), reported as annual gross
profit aggregates where one index point = CNY 300 (PDF p. 20): profit
rises with horizon from ≈63k points at 0.5s to ≈525k at 30 minutes
(Figs. 3.1-3.4, PDF pp. 21-23; Table B.1, PDF pp. 36-37), regression
coefficients rise from 0.027 to ≈0.067 (Fig. 3.4, PDF p. 23), out-of-
sample tracks in-sample at about the 4:1 ratio (PDF p. 24). Two-factor
LASSO shows TI adding below 1 second and AvgEn dominating beyond 2
minutes (PDF pp. 25-26). Monthly tables show the e_n memory (lag-1
autocorrelation 0.097-0.230 month by month, Table 5.1, PDF p. 27;
cumulative autocorrelation ≈0.5 in strong months against ≈0.2 in weak
ones, PDF p. 27) and the paper closes with a three-part metric-quality
screen: stable contemporaneous correlation across windows, memory with
slowly decaying autocorrelation, and cross-regime stability with
quantitative-only variation and no sign reversal (PDF p. 29).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening — default grade; every
mechanism found is a page-cited instance of a discipline the queue
already carries (the price-process-family invariance rule, the
estimator-configuration freeze, the regime-window pre-declaration, the
dispersion register and the primary-metric pre-commitment), recorded as
reinforcement or caution, not as a new axis.

1. [interpretation caution] The load-bearing level of the whole
   response model is an analyst construct: the initial drift is set to
   µ_0 = OFI_0·ρ_k — the observed imbalance multiplied by its fitted
   contemporaneous correlation with price (PDF pp. 13-14), with the
   correlation quoted as window-stable on exactly the pooled table the
   model needs (Table 2.1, PDF p. 6). The derived objects that matter
   to a trader (the response ratio QS(t), eq. 24, PDF p. 16, its peak
   location t* = −ln(σ²/2µ_0)/θ, eq. 25, PDF p. 18, and the maximum
   mean log-return, Appendix A.4, PDF p. 35) exist under the assumed
   family — GBM price with Lévy-driven O-U drift (eq. 14, PDF p. 13) —
   and under a W⊥L independence (PDF pp. 15, 33) that the text itself
   withdraws one page before imposing it ("may exhibit correlation",
   PDF p. 13). Any C1-L2/C8-adjacent statistic that maps a book-shock
   level to expected drift through a fitted correlation inherits two
   analyst properties at once (the process family and the correlation
   window); both must be pre-declared before such a construct may even
   be interpreted, let alone admitted. Licenses nothing; a reading
   discipline only, the price-process-family invariance rule's exact
   axis. No queue change.

2. [reinforcing, no new item] The paper's calibration contradicts its
   own regime section: θ = 0.5 is frozen from the pooled one-year
   autocorrelation decay ("our observed empirical autocorrelation
   decay rate θ = 0.5", PDF p. 11), while its own monthly table puts
   the lag-1 autocorrelation between 0.097 and 0.230 across months
   (Table 5.1, PDF p. 27), i.e. θ = 1 − ρ_1 sits at 0.77-0.90 month by
   month, never at 0.5, and the memory measure varies more than
   twofold (cumulative autocorrelation ≈0.5 vs ≈0.2, PDF p. 27) with
   the paper's own conclusion that "longer backtesting windows do not
   necessarily enhance model quality" and monthly recomputation is
   required (PDF pp. 28-29). A constant calibrated on pooled data
   while the same data shows the constant is regime-dependent is the
   exact laundering the regime-window pre-declaration and the
   dispersion register exist to kill, demonstrated inside one paper.
   Reinforces both, plus the frozen-constant reporting discipline; no
   new item.

3. [reinforcing, no new item] The (window, horizon) grid manufactures
   the factor ranking: TI adds value below 1-second horizons while
   AvgEn dominates beyond 2 minutes (PDF pp. 25-26), so no metric has
   a horizon-free efficacy; and the paper's own appendix shows that at
   the 30-minute forecast horizon the identical regression's annual
   aggregate halves between historical windows — ≈525.5k points at
   window 1 versus 235.7k (window 30), 226.0k (window 120) and 225.1k
   (window 240), Table B.1, PDF pp. 36-37 — while the paper claims
   window-insensitivity only below the 10-minute horizon
   (PDF pp. 21-22). A conclusion that exists only in the (window,
   horizon) cell it was measured in is what the
   estimator-configuration freeze (#37, the sampling scheme and grid
   axis) and the primary-metric pre-commitment (#35) fail by rule.
   Reinforces both; no new item.

4. [reinforcing, no new item] The paper's proposed metric-quality
   screen (stable contemporaneous correlation across windows, memory
   with slowly decaying autocorrelation, cross-regime quantitative-only
   variation with no sign reversal, PDF p. 29) is a sign-stability
   criterion, and the paper demonstrates it failing on its own
   example: the mid-price-change factor's autocorrelation is negative
   short-term in every month but flips positive in the high-volatility
   month Oct 2024 (PDF p. 28). Pooled sign stability before any level
   claim is the sign-register / sign-kill-line family, with the same
   subsample logic as the sign-persistence admission null (#33):
   stability must be shown where the claim lives, month by month, not
   pooled. Reinforces the family; no new item.

5. [interpretation caution] The model's empirical "validation" is a
   qualitative shape match: annual gross profit aggregates, plotted
   under author-chosen quasi-logarithmic coordinates, are read as
   exhibiting "similar patterns" to the predicted mean-return curve
   (Figs. 3.1-3.2, PDF pp. 21-22) — while the theory curve peaks at t*
   and declines (eq. 25, PDF pp. 18, 35) and the empirical PnL curve
   rises monotonically through the 30-minute horizon with no peak
   (Fig. 3.1, PDF p. 21; Table B.1, PDF pp. 36-37). A shape match of
   unscaled aggregates under chosen coordinates, with the variance side
   explicitly deferred to future work ("variance validation will be
   addressed in subsequent research", PDF p. 19), is not a
   falsification instrument. Any future C1-L2/C8-adjacent model
   validation must pre-declare its test statistic before the data —
   the same clause the dynamics-identification rule for generative
   nulls already carries for refutation instruments, applied here on
   the confirmation side. No queue change.

6. [cost-survival ammunition, relevant only if a future K7-style
   cost-survival layer exists] Every profit table is a cost-free gross
   aggregate over a decision stream re-evaluated at the 500ms snapshot
   rate for a full instrument-year (~6M ticks; PDF pp. 4, 20-25), with
   no fees, no slippage, no queue position, no latency, and resting
   periods excluded from the metric construction (PDF p. 6). The 525k
   index points (×CNY 300) carry zero cost assumptions; the paper may
   never be cited as cost-model support at any layer, and any
   tick-frequency PnL claim from it dies at the first cost ledger. No
   queue change.

7. [source-quality note] arXiv v1 only (23 May 2025), both authors
   industry-affiliated (Guolian Futures, Shanghai), no journal version
   found, zero recorded citations; single instrument (CSI 300 index
   futures) and a single year (months 2312-2411, PDF p. 27), data
   proprietary; finest granularity is the 500ms snapshot, not the
   event, so e_n is computed between snapshots rather than per order
   book event (PDF pp. 4-5); no significance testing or confidence
   intervals on any regression coefficient or profit aggregate
   (Table B.1 reports R², PDF pp. 36-37, with no inference attached);
   train/test is a 4:1 split inside the same year (PDF pp. 20, 24);
   internal sloppiness visible ("U-O process", References "Uhlenback",
   PDF pp. 9, 31). Check for a published version before formal
   citation.

## What this paper would have killed if we had done it wrong

Had a C1-L2/C8-adjacent arm scaled expected impact by a fitted
correlation (µ_0 = OFI·ρ_k, PDF pp. 13-14) and read the response
ratio's peak as a tradable optimal-holding-time find, the derivation's
family dependence — GBM price, Lévy-driven O-U drift, a W⊥L
independence imposed one page after the text conceded the two drivers
"may exhibit correlation" (PDF pp. 13-15, 33) — would have laundered
three modeling choices into a market fact; the price-process-family
invariance rule (#38) exists precisely to fail that construct at the
gate. Had θ = 0.5 been accepted as an instrument invariant because it
was frozen before the regressions ran, the paper's own monthly table
(Table 5.1, PDF p. 27) is the refutation sitting inside the same PDF —
the pooled constant is a regime average masquerading as a parameter,
which is why frozen constants carry stability reporting, never
re-tuning. Had the (window, horizon) grid been searched for the cell
where the factor wins — TI under 1 second, AvgEn past 2 minutes, 525k
versus 226k points at 30 minutes between adjacent window choices
(Table B.1, PDF pp. 25-26, 36-37) — the post-hoc re-configuration mode
the estimator-configuration freeze (#37) fails by rule would have been
run with this paper's blessing. Had the gross tick-frequency PnL been
quoted as an edge, the K7-style cost layer would have annihilated it
unreported: zero cost assumptions anywhere in the paper. And had any
of its empirical figures entered the programme record as evidence for
any claim, the library-is-ammunition rule would have been broken:
this is an industry preprint's internal validation, not evidence.

## Standing caveat

Single instrument (CSI 300 index futures), single year, 500ms
snapshot granularity, no depth anywhere in the model (the paper's own
first limitation, PDF p. 29), variance and quasi-Sharpe layers never
validated empirically (PDF p. 19), the driving Lévy process assumed
symmetric with finite second moments but never identified or fitted,
the metric set is four factors plus lags with no multiplicity
accounting, the correlation that sets the drift level (Table 2.1) is
the same contemporaneous quantity the regressions then lean on at
other windows, and all profit aggregates are gross of costs.
arXiv v1, industry-authored, unpublished: check for a journal version
before any formal citation, and treat every magnitude in the paper as
non-transferable to any C1-L2/C8-adjacent context.
