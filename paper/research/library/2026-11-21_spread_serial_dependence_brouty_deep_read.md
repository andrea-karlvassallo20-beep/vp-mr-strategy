# Deep-read session 69 (null-time session 80, log ## 88) — the Brouty–Garcin–Roccaro spread-estimation-under-serial-dependence paper read; the price-process family shown to manufacture or erase the measured spread at the estimator's own bias, the estimator-and-scales choice shown to decide the answer on identical data, and the bootstrap relevance test shown to reject the true value inside its own confidence interval; nothing sharpened

Xavier Brouty, Matthieu Garcin, Hugo Roccaro (ESILV, Léonard de Vinci,
Paris), "Estimation of bid-ask spreads in the presence of serial
dependence" (arXiv:2407.17401v3 [q-fin.ST], 2024; extract title page
dated 6 January 2025; zero recorded citations, no published version
found). A microstructure-noise estimation paper: the observed log-price
p_t = m_t ± S/2 (eqs. 1-2, PDF pp. 3-4) hides a latent effective spread
S, and the paper builds variance-of-increments estimators for S² at two
time scales (L, L′) under four dependence models — the baseline
independent-increments case (eq. 6, Thm 1, PDF pp. 5-6), fractional
Brownian-motion price with Hurst H ≠ 1/2 (eq. 8, PDF p. 8; forced H =
1/2 shown to bias both the two-scale and Roll estimators, bias equal to
4σ²τ^{2H}(1 − 2^{2H−1}) for (L, L′) = (1, 2), the same bias as Roll's,
PDF pp. 8-9; plug-in Ĥ at eq. 10, CLT valid only for H ≤ 3/4, Thm 2,
PDF p. 10), autocorrelated trade signs via binarized OU signs (eqs.
12-17, PDF pp. 12-14; bias of the standard estimator −S²(2ρ − ρ²) ≤ 0,
same for Roll, PDF pp. 12-13), and a four-parameter combined model
fitted by numerical least squares (PDF p. 15) — graded against the
benchmarks Roll, Corwin–Schultz, Abdi–Ranaldo and Ardia–Guidotti–
Kroencke (AGK1/AGK2) in 10,000-day simulations of one-minute closes
(PDF pp. 16-21) and on CAC 40 one-minute data, 19 September 2022 to 31
March 2023, with "truth" the daily average of five-minute-sampled
spreads (PDF pp. 22-23).

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change its kill lines? Source: legally acquired OA copy
(docs/library/text/x6b73c4_estimation_of_bid_ask_spreads_in_the_presence_of_s.txt,
~40 pp., page-marked, complete, references and appendices included).
Next UNREAD triage-rank entry (score 25, x6b73c4), per the recorded ## 87
pointer and re-verified against the live file state this session: the
score-25 tier order in docs/library/edge_triage_scores.json is x074d5c
(read, ## 85), x8f729f (read, ## 87), then x6b73c4 — the pointer is
correct. Read-status recomputation note for the record: the three
score-25 slugs this session's preparation could not initially
reconcile (x217e71 "Optimal execution with deterministically time
varying liquidity: well posedness and price manipulation", x475f30
"High-Resilience Limits of Block-Shaped Order Books", x6aed5b
"Detecting Financial Market Manipulation with Statistical Physics
Tools") were re-checked against the full note set and the full log on
the live tree: all three follow x6b73c4 in triage file order (x475f30
and x6aed5b immediately after, x217e71 later in the tier), no note
cites their slugs or titles, and no log entry reports reading them —
they are UNREAD and undisputed, the earlier session's pointer skipped
nothing, and the apparent discrepancy dissolves. Session-state note,
per the goal-autonomy conductor protocol (edition 5, ## 83): the
declared work choice is the standing deep-read, the protocol's default,
which owes no justification; the synthesis cadence is NOT due — four
deep-reads (## 84, ## 85, ## 86, ## 87) have landed since the
edition-5 reset at ## 83, out of five, and this session's read makes
the cadence due (five of five) at the NEXT null-time session, which
must open with the synthesis pass; no other front is claimable by a
null-time session (the L2 deployment and its data spend stay
owner-side).

## The paper in one paragraph

The paper's program is to estimate the latent squared spread S² from
close prices alone by comparing the variance of L-scale and L′-scale
price increments, V(Lτ) = Lτσ² + S²/2 in the baseline model (PDF pp.
5-6), and to repair the estimator when its independence assumptions
fail: under fBm price dynamics V(Lτ) = (Lτ)^{2H}σ² + S²/2 (eq. 8, PDF
p. 8) so forcing H = 1/2 manufactures or erases spread mass at
magnitude 4σ²τ^{2H}(1 − 2^{2H−1}) for the (1, 2)-scale pair, and Roll's
estimator carries exactly the same bias, equal to −4 times the
covariance of successive increments (PDF pp. 8-9); under autocorrelated
trade signs the bias is −S²(2ρ − ρ²) ≤ 0, again identical for Roll (PDF
pp. 12-13). The proposed repairs (Ŝ²2, plug-in H, eq. 10, PDF pp.
10-11; Ŝ²3, plug-in ρ, eqs. 15-17, PDF pp. 13-14; Ŝ²4, the combined
4-parameter numerical fit, PDF p. 15) are then graded in simulation
against Roll, Corwin–Schultz, Abdi–Ranaldo and AGK1/AGK2 with a
bootstrap relevance test that asks whether the true spread lies in the
estimator's own confidence interval: in the BASELINE model, the
no-dependence case they were built for, CS and AGK2 are rejected
(Tables 1-2, PDF pp. 17-18 — small variance plus significant bias
means the true value sits outside a narrow CI); at H = 0.3 only Ŝ2,1,
Ŝ4,1 and AGK1 survive (PDF p. 18); in the autocorrelated-signs model
only Ŝ2,1, Ŝ3,1 and Ŝ4,1 survive (Table 4, PDF p. 19); and under
infrequent trading the high-low-based estimators (CS, AR) degrade while
the close-price-based ones (Roll, Ŝ1,1) stay robust down to π_liq =
0.1 (Fig. 5, PDF pp. 21-22). On CAC 40 one-minute data against
five-minute-sampled spread averages (PDF pp. 22-23), the plain
uncorrected Ŝ1,1 is best on average (MAPE 6.06%, followed by Ŝ2,1 and
Roll tied at 7.01%; Ŝ3,1 at 14.88%, CS worst at 20.21%, Table 5, PDF
p. 22), and by market-cap rank Ŝ2,1/Ŝ3,1 do relatively better on small
caps (Table 6, PDF p. 23), leaving the authors' own conclusion that
"deciding to use Ŝ2,1 or Ŝ3,1 is a difficult task without a deeper
preliminary empirical study of the dataset" (PDF p. 22).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening — default grade; every
mechanism found is a page-cited instance of a discipline the queue
already carries (the price-process-family invariance rule #38, the
estimator-configuration freeze #37, the dispersion register, the
primary-metric pre-commitment, the spread-convention declaration),
recorded as reinforcement or caution, not as a new axis.

1. [reinforcing, no new item] The price-process family alone
   manufactures or erases the spread statistic: the same close-price
   series carries V(Lτ) = (Lτ)^{2H}σ² + S²/2 under fBm rather than
   Lτσ² + S²/2 under diffusive prices (eq. 8, PDF p. 8), so an
   estimator scale-pair frozen at H = 1/2 eats spread mass of order
   4σ²τ^{2H}(1 − 2^{2H−1}), and Roll's estimator — the field's default
   — carries exactly the same bias, shown by the authors to equal −4
   times the covariance of successive increments (PDF pp. 8-9); even
   the CLT invoked for the corrected estimator is only valid for
   H ≤ 3/4 (Thm 2, PDF p. 10, asymptotics at PDF pp. 36-37). This is
   the price-process-family invariance rule (#38, queued at ## 85 in
   the Langnau–Punche read) demonstrated one level deeper: there the
   smile structure of a book statistic changed with the assumed
   family; here the headline LEVEL of the spread itself moves with
   the assumed H, with the estimator holder none the wiser because
   the bias is silent in the point estimate. Any C1-L2/C8-adjacent
   statistic computed from price increments (variance-scaled
   impact, microstructure noise floors) inherits this axis
   entirely. Licenses nothing; reinforces #38. No queue change.

2. [reinforcing, no new item] The estimator-and-scales identity
   decides the answer on identical data: benchmarks built for the
   baseline model (CS, AGK2) are rejected by the paper's own
   relevance test in the baseline model itself (Tables 1-2, PDF
   pp. 17-18); the survivors set changes entirely with the
   dependence mode (H = 0.3: Ŝ2,1, Ŝ4,1, AGK1; autocorrelated signs:
   Ŝ2,1, Ŝ3,1, Ŝ4,1, PDF pp. 18-19); the empirical ranking on CAC 40
   puts the UNCORRECTED estimator first (MAPE 6.06% vs 7.01% for the
   corrected Ŝ2,1, Table 5, PDF p. 22), and by market cap the ranking
   inverts toward small caps (Table 6, PDF p. 23), with the authors'
   own summary that choosing between Ŝ2,1 and Ŝ3,1 alone requires "a
   deeper preliminary empirical study of the dataset" (PDF p. 22).
   WHICH estimator, WHICH scales (L, L′), WHICH input set
   (close-based vs high-low, with the high-low family degrading
   under infrequent trading, Fig. 5, PDF pp. 21-22) — each is a
   researcher degree of freedom that flips the conclusion, which is
   the named-estimator identity and estimator-configuration freeze
   (#37) stated as a demonstration rather than a rule. Reinforces
   #37 and the primary-metric pre-commitment; no new item.

3. [reinforcing, no new item] The bootstrap relevance test is a
   dispersion-register exhibit in the wild: the paper's own Tables
   1-4 (PDF pp. 17-19) show estimators whose confidence intervals
   are narrow enough and biased enough that the TRUE value is
   rejected by the estimator's own CI — statistical significance
   coexisting with full miscalibration (CS: bias −3.2×10−4 with
   standard deviation 6.0×10−5, rejected at p ≈ 1.1×10−7, PDF
   p. 18). Confidence intervals on a dispersion-degenerate estimator
   are not evidence that the estimate is right; they are sometimes
   the sharpest available proof that it is wrong. Reinforces the
   dispersion register and the estimator-discipline family (the
   estimator must report its own bias regime, not only its
   variance); no new item.

4. [interpretation caution] The measured "spread" is a
   convention-of-instrument object, not one quantity: the paper's
   several estimators target the same latent S yet return rankings
   that depend on input granularity (close-price estimators robust,
   high-low estimators degraded, under infrequent trading, PDF
   pp. 21-22) and on the estimation scales; the "truth" used on real
   data is itself a proxy (the daily average of five-minute-sampled
   spreads, PDF pp. 22-23), so the empirical MAPE table grades
   estimators against an estimator-mode artifact of the sampling
   convention. Any C1-L2/C8 figure quoted as "the spread" or "the
   cost per trade" without naming its estimator, scales and sampling
   convention is not yet a defined quantity; the spread-convention
   declaration discipline (quote the instrument with the number)
   governs before any such figure may be interpreted. A reading
   discipline only; licenses nothing.

5. [source-quality note] arXiv v3, citation-free at acquisition (zero
   recorded citations, no published version found), author team
   overlapping the Garcin/ESILV fractal-markets program that
   produced earlier shelf entries; the simulation and empirical
   sections are self-contained internal validation, single market
   (CAC 40), a single 6.5-month window, against a proxy truth; the
   page-marked extract mangles some displayed mathematics
   typography (integral kernels, variance terms), so claims were
   checked against equation context rather than glyph-exact
   reading. Check for a published version before formal citation.

## What this paper would have killed if we had done it wrong

Had any C1-L2/C8-adjacent spread, cost or noise-floor figure been
estimated from price increments with the process family assumed
diffusive (H = 1/2) and frozen — the field default this paper shows
carries a bias identical in form to Roll's — the number would be a
family artifact moving as 4σ²τ^{2H}(1 − 2^{2H−1}) with the true H
(PDF pp. 8-9), and the price-process-family invariance rule (#38)
exists precisely to fail that figure at the gate: family declared
first, bias regime reported with the number. Had the estimator and its
scale pair (L, L′) been chosen after inspecting which one produced the
wanted ranking — the paper's own tables flip the ranking with the
estimator, the market-cap segment and the dependence mode (PDF
pp. 18-19, 22-23) — the estimator-configuration freeze (#37) and the
primary-metric pre-commitment would have been run with this paper's
blessing. Had a confidence interval been read as calibration, Tables
1-4 are the refutation sitting inside the same PDF: the estimator most
significantly wrong about the true value is the one with the narrowest
variance (PDF p. 18), which is what the dispersion register is for.
Had the paper's MAPE table been allowed into the record as evidence
that any estimator is "best", the library-is-ammunition rule would have
been broken twice: it is internal validation, and its truth column is
itself a sampling-convention proxy. And had the quoted spread figure
entered a cost-survival layer without the estimator identity, scales
and sampling convention named, the K7-style layer would have received
an undefined quantity and laundered it as cost. Nothing here was
measured, and nothing here licenses any arming.

## Standing caveat

Single market (CAC 40), single window of six and a half months, truth
proxy built from five-minute-sampled spreads rather than the true
latent spread, simulation base rates set by the authors' own model
choices (minute closes, fixed S and σ grids), the corrected estimators
require estimating H or ρ plug-ins whose own estimation error is only
partially propagated (dS2 with Ĥ is asymptotically unbiased only, PDF
p. 11), the four-parameter combined estimator is a numerical least
squares fit with no convergence diagnostics reported, no transaction
costs anywhere in the empirical section, and the relevance test's
bootstrap parameters sit in the appendix rather than the main text.
arXiv v3, unpublished, zero citations: check for a journal version
before any formal citation, and treat every magnitude as
non-transferable to any C1-L2/C8-adjacent context.
