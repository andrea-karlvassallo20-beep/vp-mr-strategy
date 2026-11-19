# Deep-read: Hawkes processes for credit indices time series analysis (Bahamou, Doumergue, Donnat)

Null-time session 64 (log ## 68), deep-read session 54. Achraf Bahamou,
Maud Doumergue, Philippe Donnat, "Hawkes processes for credit indices
time series analysis: How random are trades arrival times?", arXiv:1902.03714v1
(11 Feb 2019), authors at Hellebore Capital Ltd, London. A practitioner
methods paper: a two-stage maximum-likelihood fitting algorithm (2SHLO)
for multivariate exponential-kernel Hawkes processes, validated on
simulated data and applied to publicly reported trades on three European
credit indices (ITXEB Main, ITXEX Crossover, ITXES Senior Financial,
5-year maturities), quantifying self-excitation, volume-bin influences,
and cross-index influence at "mid-frequency" (minute-scale) trade
arrivals.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xdb216a_hawkes_processes_for_credit_indices_time_series_an.txt,
~19 pp., page-marked). Next UNREAD triage-rank entry (score 28).

## The paper in one paragraph

The paper proposes 2SHLO (Two Stage Hawkes Likelihood Optimization):
since the negative log-likelihood of a multivariate exponential Hawkes
process is CONVEX in (baseline mu, adjacency alpha) once the decays beta
are fixed, but non-convex in beta overall (PDF pp. 6-7, eqs. (5)-(7)),
they profile out (mu, alpha) by accelerated/projected gradient or
Newton descent at each beta, and run Nelder-Mead only over the
lower-dimensional beta surface (Algorithm 1, PDF p. 7; Algorithms 3-4,
PDF pp. 16-17). They validate on simulated 2D Hawkes data (parameters
recovered asymptotically, Fig. 3, PDF pp. 8-9), and apply to 2017
reported trades with the intensity forced to zero in overnight gaps
(the Bowsher spillover variant was tried first and the spillover
parameter estimated to null, PDF pp. 8-9; appendix PDF pp. 13-17),
finding stable out-of-sample fits on Jan-Jul 2018 (Fig. 4, PDF pp. 9-10),
branching ratios around 0.6 per index univariately (Table 2, PDF p. 9),
large trades purely self-exciting and triggering small trades in the
volume-bin fit (PDF p. 10, Fig. 5), and cross-index adjacency with ITXES
the least influenced, all fitted baselines RISING in the multivariate
model relative to the univariate one because including other series
removes Poissonian mass from the baseline (PDF p. 11, Fig. 6).
Goodness of fit is assessed by the compensator time-change residual
Poisson QQ test (PDF pp. 7-8; Figs. 8-9, PDF pp. 18-19).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The decay parameters beta sit on a flat,
   valley-ridden non-convex surface (Fig. 7, PDF p. 17), and every fast
   fitting approach that avoids that surface does so by FIXING the
   decays a priori, which the authors themselves flag as a
   model-mismatch risk (PDF p. 6). This is the estimator-discipline
   lesson with a second face: decay handling is a researcher degree of
   freedom in BOTH directions — free
   (multi-mode, init-dependent) or fixed (mismatch). It reinforces the
   already-queued estimator-mode candidate sharpening and the frozen
   constants discipline; nothing new is earned here, no queue change.

2. [interpretation caution] The estimated baseline mu is
   MODEL-RELATIVE, not intrinsic: the authors observe all three index
   baselines INCREASE when the univariate fit is replaced by a
   multivariate one, "explained by the fact that we decreased the
   'Poissonian' behaviour of the arrival times by including more
   information about the influence of other indices" (PDF p. 11).
   The same event stream therefore yields different self-excitation
   shares depending on how many coordinates were fitted. Any future
   L2/C8 self-excitation or "endogeneity" reading must declare the
   model's dimensionality and channel set BEFORE comparing branching
   ratios across fits, or the comparison is manufactured by model
   choice. No rule change proposed; this is a reading discipline.

3. [reinforcing, no new item] The out-of-sample compensator
   time-change QQ validation (fit on 2017, tested on 2018, PDF pp. 8-10,
   Figs. 4, 8-9) and the honest gap treatment (null overnight intensity
   adopted only after a spillover model estimated its spillover to
   null, PDF pp. 8-9) reinforce the seeded out-of-sample discipline and
   the declared-gap discipline already encoded in the L0 amendment and
   kill lines. Nothing added.

4. [cost-survival ammunition] The volume-bin finding (large trades
   purely self-exciting, small trades driven by large ones, PDF p. 10)
   declares an assumption any future K7-style cost layer must carry:
   self-excitation is not homogeneous across trade-size bins, so a
   cost-survival model that extrapolates a single market-wide branching
   ratio to execution fragments of different sizes would misprice
   survival. Relevance only if that layer exists.

5. [source-quality note] A fund-authored practitioner paper: zero
   citations in our index, arXiv-only (v1), data "provided by
   otcstreaming.com, and available on demand" (PDF p. 1) — not
   reproducible from the paper alone — three indices, one year train,
   half-year test, and copyediting-grade errors ("Ogota" for Ogata at
   PDF p. 2, "fastly" at PDF p. 11). The triage score 28 ranked access
   value; the paper graded as solid practitioner-grade methodology but
   evidence-light: its empirical numbers (branching ratios 0.57-0.62,
   PDF pp. 9-10) are ammunition under the library invariant, never
   evidence for any programme claim. Check for a published version
   before any formal citation outside this note.

## What this paper would have killed if we had done it wrong

The dimension-comparison death: a future C1-L2 or C8 report comparing
self-excitation strength (branching ratio, endogeneity share) between a
univariate feature fit and a multivariate one, or between two fits with
differently handled decays, would read the model-choice artifact
(Finding 2's baseline shift; Finding 1's decay surface) as a market
fact — "reflexivity rose/dropped" manufactured entirely by which
coordinates and kernel handling the analyst chose. The second death is
the decay-mismatch death: fixing betas a priori for speed (the standard
practice the paper catalogues, PDF p. 6) and treating the resulting
smooth convex fit as truth. Both are pre-empted by the frozen-constants
discipline, the queued estimator-mode sharpening, and the
burden-of-proof orientation; neither moves any kill line.

## Standing caveat

The paper's scope is minute-scale "mid-frequency" credit-index reported
trades, three indices, sparse data (7k-22k trades per index-year,
Table 1, PDF p. 2); nothing licenses transfer to tick-scale L2 futures
microstructure without re-derivation. The fit's global-minimum claim
(eq. (7), PDF p. 7) is heuristic at the beta level (Nelder-Mead over a
non-convex profile surface, Fig. 7, PDF p. 17) — mode sensitivity is
unquantified. The volume-bin count (3 bins per index, PDF p. 10) and
the data's availability-on-demand basis limit replication. arXiv v1
only; check the published version before formal citation.
