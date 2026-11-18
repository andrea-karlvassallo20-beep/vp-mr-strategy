# Deep-read session 36 — Filimonov & Sornette, "Apparent criticality and calibration issues in the Hawkes self-excited point process model: application to high-frequency financial data"

**Authors:** Vladimir Filimonov, Didier Sornette (ETH Zürich / Swiss Finance
Institute). **Venue:** arXiv:1308.6756v3 [q-fin.ST], v3 July 2014. One clause:
the origin authors' systematic audit of every way a fitted Hawkes branching
ratio n̂ can drift toward spurious criticality, published as the rebuttal of
Hardiman-Bercot-Bouchaud's continuous-criticality claim.

**Read-line:** Read 2026-11-18, against ONE question: **what here would kill
C1-L2 or C8 faster, or change their kill lines?** Source: legally acquired OA
copy (`docs/library/text/xd18d70_apparent_criticality_and_calibration_issues_in_the.txt`,
~35 pp., page-marked). Named next-read by the standing queue pointer of
sessions 44 and 45 (the origin paper's reckoning); triage score 30. Rank-order
note for the record: three shelf entries score above it unread
(x947263 at 32, xce0ba3 at 31) — the deliberate thematic override is logged
honestly here and the next pointer returns to pure rank order.

## The paper in one paragraph

A synthetic-data audit of Hawkes branching-ratio estimation, motivated by the
contradiction between the authors' own n ≈ 0.7–0.8 readings (origin paper,
session 44) and Hardiman-Bercot-Bouchaud's n ≈ 1 "continuous criticality."
They demonstrate five upward-bias sources: (i) with power-law memory kernels,
tiny outlier fractions drive n̂ to spurious criticality — just 0.17% of
durations inflated 5×, or 1% inflated 2×, push a true n = 0.7 to n̂ ≈ 1, while
the rigid exponential kernel is robust (PDF p. 8); (ii) the regularization
part of the power-law kernel and the shape of the likelihood landscape
(multiple extrema, exhaustive search required) matter materially (pp. 1, 9–13);
(iii) long-memory kernels suffer strong edge effects (p. 1); (iv) exchange
timestamp bundling plus too-fine randomization manufactures spurious
clustering — a pure Poisson (n = 0) calibrates at n̂ ≈ 0.856 when randomized
below the bundling interval (p. 25); and (v) the headline: NON-STATIONARITY.
Concatenating two subcritical segments never yields an intermediate n̂ but one
at least as high as the higher segment — n1 = 0.5 with n2 = 0.2 calibrates at
n̂ = 1 (pp. 30–32); a multi-Poisson series with ONLY day-level intensity
variation (true n = 0) is diagnosed hovering at criticality across 1998–2012,
and residual analysis CANNOT distinguish it from a genuinely critical Hawkes
(pp. 32–33). Their verdict: the continuous-criticality claim "cannot be
supported" (p. 1), their own short-window short-memory results stand, reliable
long-memory estimation from high-frequency data may be impossible, and
single-kernel Hawkes calibration beyond intraday scales is inconsistent with
multifractal market reality (pp. 34–35).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.**

1. `[reinforcing, no new item]` **The critique IS the
   (construction × vintage)-conditional rule.** Sessions 44 and 45 held the
   origin's post-2007 near-critical readings conditional until this paper was
   read; the reckoning resolves the flag exactly as the estimator-mode rule
   demands: a fitted n̂ is a reading of (kernel choice × window × timestamp
   resolution × regime-mixing), never a free-standing endogeneity fact, and
   the paper's own closing metaphor — "calibrating the Hawkes process is akin
   to an excursion within a minefield" (p. 34) — is the negative-knowledge
   content of the whole queue made explicit by the origin authors themselves
   (pp. 1, 34). Nothing in the house arsenal moves.

2. `[interpretation caution]` **A fitted clustering parameter is a clustering
   measure, not a mechanism.** The Poisson-truth-n̂≈1 demonstration (pp.
   32–33) shows day-level non-stationarity alone — no self-excitation at all —
   reproduces the signature readings cited as market facts. Any future
   branching-ratio or clustering-statistic reading attached to the program's
   instruments inherits this caution verbatim: regime-mixing inflation first,
   mechanism second.

3. `[interpretation caution]` **Residual analysis cannot rescue a
   calibration.** Regime-switching Poisson is statistically
   indistinguishable, by the standard residual goodness-of-fit, from a
   critical Hawkes (p. 33); in the measured dossiers' language, a fit that
   passes its own diagnostics can still be the wrong generating model —
   goodness-of-fit is not identification. No dossier statistic is licensed to
   "confirm a mechanism," only to describe a conditional.

4. `[reinforcing, no new item]` **The concatenation result is the
   stability-split session's episode-contamination caution in another
   domain.** Joining segments yields n̂ ≥ the higher segment's truth (pp.
   30–32): episode lumps inflate any clustering statistic computed across
   them — precisely why the session-47 P_move5 cells were flagged and why the
   direction chips, not the arrival cells, are treated as the stable content.

5. `[source-quality note]` **An adversarial defense of the authors' own
   results.** The paper exists to rebut Hardiman-Bercot-Bouchaud and
   concludes their own n ≈ 0.7–0.8 stands (pp. 1, 34) — the same favor is not
   extended to the rival reading, and the "upheld" numbers carry the same
   short-window/exponential-kernel conditionality the origin's own caveats
   (session 44) flagged. Single venue and contract (E-mini S&P 500 / commodity
   futures), TRTH-timestamp dependence, arXiv v3 2014 — check the published
   version before formal citation; zero portability to the program's venue,
   grain, or vintage.

## What this paper would have killed if we had done it wrong

A spec reading any fitted branching ratio (or branching-adjacent clustering
statistic) as a free-standing fact about a venue — "this market IS at
criticality, trade as if" — would have walked the exact minefield the paper
maps: outliers, kernel choice, bundling artifacts, and above all regime-mixing
all push the same direction (up), and the residual diagnostics would have
shown green all the way down (p. 33). And a "regime gauge" built on n̂ without
declaring its regime-mixing content would have measured the calendar of its
own segmentation, not the market. The house arsenal (estimator-mode rule,
never-read-branching-alone, label placebo, calendar discipline) is the
paper's recommendation list restated as rules; this session only confirms
they were already armed.

## Standing caveat

All demonstrations are synthetic; the real-data content is the 1998–2012
activity calibration borrowed for intensities (pp. 31–33). The claim
"long-memory estimation from high-frequency data may be impossible" is itself
a strong claim published on one data stack (TRTH); the multi-scaling/multifractal
extension it points to (Self-Excited Multifractal Process, p. 35) does not yet
exist in calibrated form. Nothing here touches the program's venue, the
dossiers' daily grain, or T1's spell scale; the queue's unread scores above
this entry (x947263 at 32, xce0ba3 at 31) are recorded honestly above and
return as the next pointer.
