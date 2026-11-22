# Deep-read note — library session 98 ("Analysis of Contagion in China's Stock Market: A Hawkes Process Perspective")

- Session: null-time deep-read session 98 (null-time session 108, log ## 129),
  2026-11-22.
- Authors: Junwei Yang.
- Title: "Analysis of Contagion in China's Stock Market: A Hawkes Process
  Perspective".
- Venue/id: arXiv:2512.08000v1 [q-fin.ST] (title page dated "This version: May
  18, 2023"; arXiv stamp 8 Dec 2025; slug x999a87, per
  docs/library/expanded_index.json).
- What it is, one clause: a single-author graduate-thesis-style study fitting
  self-exciting and inhibitory multivariate Hawkes processes to daily
  extreme-return events of Chinese market and sector indices to read trend
  continuation and sector rotation as contagion.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x999a87_analysis_of_contagion_in_china_s_stock_market_a_ha.txt,
~27 pp., page-marked). Next UNREAD triage-rank entry (score 20).

## The paper in one paragraph

Two experiments. Experiment 1 (PDF pp. 12-16) turns daily returns of the
Shanghai Composite, Shenzhen Component and ChiNext indices (Feb 2013 - Mar
2023, n = 2,452 each) into two event types (sharp rise / sharp decline at the
10th and 90th percentiles of the SSE return history) and fits bivariate
exponential-kernel Hawkes models by MLE (Python tick), with the decay rate
grid-searched to ω = 0.1, printing impact matrices whose up-event row has the
largest entries, read as trend continuation and "oversold rebound" (PDF
pp. 14-15, Table 2). Experiment 2 (PDF pp. 16-19) slices three CSI sector
indices (Consumer, Healthcare, Finance & Real Estate, 2013-2023) into fifteen
150-day windows, builds six event types (up/down per sector), and fits a
six-dimensional nonlinear Hawkes with unconstrained µ and α via a
Monte-Carlo-integrated stochastic-gradient backprop estimator (Mei-Eisner)
under a link g(x) = max(x, 0.01) (eq. 13, PDF p. 18, Algorithm 1, PDF p. 12),
comparing an active period 3 (2014-12 to 2015-08) and a dormant period 5
(2016-03 to 2016-11) and reading the diagonal-versus-off-diagonal block
contrast as trend continuation in active markets and sector rotation in
dormant ones (PDF pp. 18-19, Table 4). Appendices derive the likelihood
(PDF pp. 23-24) and run the random-time-change residual check visually
(Q-Q plots, no printed test statistic; PDF pp. 24-27), against a homogeneous
Poisson baseline whose moment estimates drift from λ̂train = [0.100, 0.101]
to λ̂test = [0.067, 0.082], called "a scheme change in market structure"
(PDF p. 25).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The paper states the spectral-radius
   stationarity condition only in theory (ρ(A) < 1, PDF p. 9) and never
   evaluates it on any fitted matrix. Arithmetic on the printed Experiment-1
   impact matrices (descriptive only, no data touched, log ## 128 finding-1
   precedent) gives ρ ≈ 0.654 for SSE
   (A = [[0.382, 0.387], [0.218, 0.343]], PDF p. 14), ρ ≈ 0.562 for Shenzhen
   (with one small negative eigenvalue, det < 0, from cross-excitation
   exceeding within-type persistence, Table 2, PDF p. 16) and ρ ≈ 0.560 for
   ChiNext — all subcritical, so no printed near-criticality is laundered
   here; the omission itself is the reinforcement: spectral-radius checking
   on the fitted matrix stays load-bearing in any future multitype
   self-excitation score. No queue change.
2. [reinforcing, no new item] Experiment 2 prints per-type self-excitation
   diagonal entries above unity in the active period (1.161, 1.143, 1.313,
   0.671, 0.831, 1.092, Table 4a, PDF p. 19) with no full-matrix stationarity
   check and no branching-ratio read; Gershgorin arithmetic on the printed
   Table 4a rows (row 0: centre 0.696, radius 1.451, discs reaching ≈ 2.15;
   row 3 centre 1.228) leaves the spectral radius unverifiable from the
   print, and the paper reads the >1 diagonals straight as "trend
   continuation" (PDF pp. 18-19). This is exactly the case the
   apparent-criticality / branching-matrix pre-declaration family already
   queued (## 118 lineage; reinforced at ## 126 finding 1, ## 127 finding 1,
   ## 128 finding 1) exists to prevent. No queue change.
3. [interpretation caution] The configuration freedom stack compounds six
   deep before any claim: percentile event thresholds indexed to the SSE
   history (PDF p. 14), a single grid-searched ω = 0.1 shared across types
   (PDF pp. 14-16), fifteen equal 150-day windows with "representative"
   periods selected by narrative (PDF pp. 17-18), an unconstrained-µ, α
   inhibitory form under a link g(x) = max(x, 0.01) (eq. 13, PDF p. 18), and
   a Monte-Carlo-integrated SGD-gradient estimator whose compensator term is
   a sampled average, not an exact integral (Algorithm 1, PDF pp. 11-12). The
   MC noise in the compensator is a sixth freedom the certified estimator
   modes do not carry; under the estimator-configuration freeze this is
   standing context, never an operational option. No queue change.
4. [interpretation caution] The paper's own baseline shows the background
   intensity is not constant across the sample (λ̂test strictly below
   λ̂train, read by the authors as a market-structure scheme change, PDF
   p. 25), and all goodness-of-fit evidence is visual Q-Q/scatter in the
   appendix with no printed test statistic anywhere (PDF pp. 25-27, Figs.
   5-7). The non-constant-intensity reading discipline (un-modelled exogenous
   forcing inflates self-excitation estimates; log ## 128 finding 2) and the
   printed-statistic-or-it-did-not-happen convention both apply unchanged. No
   queue change.
5. [source-quality note] Single-author graduate-thesis write-up (acknowledges
   a dissertation committee and supervisor, PDF p. 1); version mismatch
   (title page "This version: May 18, 2023" on an arXiv v1 stamped 8 Dec 2025,
   PDF p. 1); the abstract and introduction promise "spatiotemporal Hawkes
   processes" (PDF p. 1) while the paper fits ordinary multivariate
   (type-indexed) Hawkes processes with no spatial structure at all; a
   six-type model (36 influence parameters plus µ and ω) fitted per
   150-trading-day window (PDF pp. 17-19); daily grain only, three Chinese
   indices and three Chinese sector indices, no L2 content, no published
   version to check. Grade plainly: student-thesis tier relative to its
   score-20 rank, per the session-9 triage-audit rule. No queue change.

## What this paper would have killed if we had done it wrong

Without the spectral-radius discipline already load-bearing in the record,
the >1 self-excitation diagonals of Table 4a would print as measured trend
persistence — a per-type reproduction count laundered into a market-property
claim, the exact "trend continuation" narrative the paper draws from 150-day
windows with no stationarity check at all. Without the
estimator-configuration freeze, this paper is the compounding case: event
thresholds, a grid-searched decay rate, window segmentation,
representative-period selection, an inhibitory link function, and an
MC-noisy SGD compensator — six researcher degrees of freedom stacked before
the headline, on a sample of 150 trading days per fit; whatever "sector
rotation" pattern survives that stack is uninterpretable, and the
configuration pre-declaration exists so the programme can never be in this
position. Without the library-is-ammunition caveat, the "oversold rebound"
and "chasing gains and cutting losses" readings (PDF pp. 14-15) would have
entered the C8 macro-synthesis as established Chinese-market properties on
the strength of a within-family fit from a student thesis with no printed
residual statistic.

## Standing caveat

Everything is daily-grain, index-level, China-only, 2013-2023; nothing
transfers to intraday or book-level claims without independent measurement.
All fitted comparisons are within-family — the only baseline is a homogeneous
Poisson moment fit (PDF pp. 25-26), so nothing certifies Hawkes against any
non-Hawkes alternative, and goodness-of-fit is entirely visual. Per-window
fitting with windowed narrative comparison cannot separate regime change
from estimation noise at 150 observations per fit. arXiv-only with a
2023-title-page/2025-stamp version mismatch; not published as far as the
record shows; check any published version before formal citation.
