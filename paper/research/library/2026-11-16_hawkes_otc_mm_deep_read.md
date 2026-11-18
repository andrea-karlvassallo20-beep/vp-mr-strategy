# Library deep-read session 15 — Barzykin, "Hawkes-Driven OTC Market
# Making: Volterra–Riccati Approximation" (arXiv:2608.02002v2, 2026;
# HSBC; Hawkes-driven OTC RFQ market making, spot-FX data)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xa868e3_hawkes_driven_otc_market_making_volterra_riccati_a.txt`,
~25 pp., page-marked). Next UNREAD triage-rank entry (score 37).

## The paper in one paragraph

An OTC request-for-quote market-making control problem where RFQ
arrivals follow a general-kernel Hawkes process and fills are
controlled thinnings of the exogenous request flow (the dealer's
quote changes the probability of winning a request but never
creates it, PDF pp. 6-7). Empirical motivation: three years of
spot-FX RFQs (EURUSD/GBPUSD/USDJPY, > 5*10^5 qualified events per
pair) fitted in seasonality-adjusted ACTIVITY TIME with a
three-exponential kernel (half-lives 1/10/60 minutes), yielding
branching ratios of 0.86-0.90 — with the author's own insistence
that these are PREDICTIVE memory objects, not causal cascades
(PDF pp. 3-5). Because general kernels make the control problem
path-dependent (exponential lifts are high-dimensional; power-law
kernels are infinite-dimensional), a three-level Volterra-Riccati
approximation is built around the conditional forecast curve of
future RFQ intensity: certainty-equivalent mean, covariance
correction, and a state-feedback rule that re-prices each quote
under the post-request forecast — where observing a request is
itself information, valued separately from winning it (PDF
pp. 8-12). Validation against an exact lifted-HJB exponential
benchmark shows the state-feedback policy tracking the optimum
in directional regimes while a memory-free Poisson policy suffers
substantial regret (PDF pp. 12-13).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand. This read's value
is two strong practitioner citations reinforcing the queue's
existing branching machinery, plus one execution-layer gift:

1. **[reinforcing, strengthens queued candidates] The
   EXOGENOUS-ABSORPTION warning, from inside the industry.** The
   author states it as a FIRST-CLASS modeling caveat: "We do not
   attach a structural contagion interpretation to the Hawkes
   branching representation. Correlated RFQs may be reactions to
   a common unobserved cause — public market activity,
   volatility, a client execution programme or another latent
   liquidity factor — rather than consequences of earlier RFQs.
   If such exogenous variation is omitted from the baseline
   intensity, a fitted Hawkes model may absorb part of it into the
   excitation kernel and thereby produce a large branching ratio"
   (PDF p. 2), restated beside the estimates: the branching ratio
   "should not be interpreted as direct evidence that one
   client's RFQ causes another client's RFQ" (PDF p. 4). This is
   exactly the false-critical concern behind the queued per-branch
   rule (session 9), the boundary-solution rule (session 7), and
   the drift-reporting item (sessions 4/4b) — now stated
   independently by an industry author on his own fitted
   branching ratios of 0.86-0.90. No new rule needed; the queued
   rules gain their practitioner anchor.

2. **[reinforcing, extends a queued candidate] The seasonality/
   activity-time caution for fitted kernels.** The kernel is
   fitted only after a deterministic time change that removes the
   intraday seasonality profile (PDF pp. 3-4): fitting in
   calendar time "would confound deterministic seasonality with
   residual serial dependence," and "all rates entering a
   control problem must be expressed in the same clock" (PDF
   p. 4). This EXTENDS the queued drift-reporting item (sessions
   4/4b) from stochastic mu-drift to DETERMINISTIC intraday
   seasonality: a branching or flow-state reading computed on a
   window that has not declared its seasonality treatment is
   conflating the diurnal profile with endogeneity. Recorded as
   an extension of the existing candidate, not a new entry — the
   drift-reporting item now explicitly covers both the stochastic
   and the seasonal component of the baseline rate's time
   variation. It also independently supports session 13's
   estimator-mode rule and session 16's clock statement (A4's
   volume clock is one more clock that must not be mixed
   mid-analysis).

3. **[cost-survival ammunition, not a strategy] The information
   value of observing a request, priced separately from winning
   it, and the observation update as a first-class state input**
   (PDF pp. 11-12). The program never trades live; this is the
   K7-style citation for how a WHEN/execution instrument's cost
   layer should treat information events and the post-event
   forecast update — IF the owner ever ratifies cost modeling.
   Nothing armed.

## What this paper would have killed if we had done it wrong

If the trigger layer had read ITS OWN fitted branching ratio as
evidence of endogenous cascading — the natural reading of 0.86-0.90
on major-pair RFQ flow — this paper is the counterexample written
by the practitioner who fitted those very numbers: the mass can be
exogenous variation wearing the kernel as a costume. The queued
rules (per-branch CIs, dispersion register, boundary-solution,
drift/seasonality reporting) each remove one costume in advance.
Grade: **no kill line changed; no candidate sharpening; two
reinforcing citations (the industry's own exogenous-absorption
warning; the seasonality/clock caution extending the drift item)
and one cost-survival note; the ratification queue stands at
FOURTEEN candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The fitted branching ratios are from filtered, size-
bucketed, seasonality-adjusted RFQ activity time on a private HSBC
dataset — magnitudes never transfer, and the author himself bars
the causal reading; the Volterra-Riccati hierarchy is validated
only in the exponential benchmark (its long-memory application is
illustrative); the RFQ two-way side is a latent mark, not an
observation (PDF p. 5) — a further warning against treating
side-signed flow readings as directly observed. arXiv v2
(q-fin.RM, Aug 2026); single-author industry preprint — check
for any peer-reviewed version before formal citation.
