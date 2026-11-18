# Library deep-read session 9 — Batra, "Modeling High-Frequency Data
# with Bivariate Hawkes Processes: Power-Law vs. Exponential Kernels"
# (arXiv:2503.14814v1, 2025; Warwick Finance Societies)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x1e82e7_modelling_high_frequency_data_with_bivariate_hawke.txt`,
11 pages, page-marked). Next by triage rank (session 10's pointer).

## The paper in one paragraph

A bivariate Hawkes model of buy and sell arrival streams (exponential
vs power-law kernels) is fitted by L-BFGS-B maximum likelihood to a
TWO-SECOND LOBSTER/Alpha Vantage window of AMD and TSLA (10:23:00 to
10:23:02 on 2025-03-14, "over 200 events", PDF p. 6), the fitted
intensities are compared visually for real vs simulated data, and
the power-law kernel is declared the better fit because the simulated
buy intensity "exhibits fewer peaks" under the exponential kernel
(PDF pp. 7-9). No likelihood values, no parameter tables, no
goodness-of-fit statistics, no out-of-sample test, and no ground
truth are reported anywhere; a "clustering-based liquidity provision"
strategy is sketched (PDF pp. 10-11) with no backtest.

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** This is a
student-society report, not peer-reviewed research, and its evidence
base (one 2-second window, visual comparison) cannot support a spec
amendment in either direction — sharpening on this basis would be
laundering, not method. Two honest recordings:

1. **[triage audit flag, recorded for the owner] The triage scorer
   over-ranked this paper.** It entered the deep-read queue at rank
   5 of 500 (score 41, tied with Bechler-Ludkovski); its content is
   an 11-page term-report with no reported estimates. The scoring
   rubric (title/venue keyword matching, most likely) cannot see
   quality this deep — future triage ranks should be treated as
   candidates, not promises, and the deep-read queue falls back to
   the peer-reviewed entries after this one. Nothing about the
   queue's PRIOR entries changes: sessions 1-8 all read
   peer-reviewed or citable sources.

2. **[reinforcing, no new item] The kernel-choice confound, in a
   weak witness.** Their headline (power-law peaks survive where
   the exponential kernel's rapid decay smooths them out, PDF
   pp. 8-9) is the same mechanism sessions 4/4b already recorded
   against peer-reviewed ground (Hardiman-Bouchaud: branching-ratio
   approximations differ between exponential and nearly-unstable
   power-law regimes; the scale problem). This report adds no
   usable parameter evidence for or against — but it does
   illustrate WHY the trigger layer's kernel form must be
   pre-declared: two kernel families fitted to the SAME two
   seconds of data produce visibly different self-excitation
   pictures, and the paper had no statistic to adjudicate them.
   The already-queued rules (per-branch CIs, boundary-solution
   rule, scale-constant rule) each assume the kernel form is
   fixed BEFORE data; this is the cautionary exhibit for that
   assumption.

## What this paper would have killed if we had done it wrong

Nothing — and that is the honest sentence. Had the trigger layer's
kernel family been chosen by which one "looked better" on a single
window (this paper's method), the choice would have been an
unacknowledged analyst degree of freedom wearing a costume of
fit. The program's own discipline (kernel form declared with the
spec, before data) is what makes this paper's method a
counterexample rather than a template. Grade: **no kill line
changed; no candidate sharpening; one triage-audit flag and one
reinforcing note; the ratification queue stands at ELEVEN
candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence — and this entry is mostly a
label on the shelf saying "ammunition quality: unreliable." The
author is an undergraduate researcher (Warwick Finance Societies,
PDF p. 1); the dataset is a manually-processed CSV of one 2-second
window (PDF p. 6); the claimed strategy (PDF pp. 10-11) has no
backtest, no costs, no capacity statement — and the program never
trades live regardless. arXiv v1 only, not peer-reviewed; do not
cite as evidence for any spec. The peer-reviewed anchors for the
kernel-form question remain Hardiman-Bouchaud (sessions 4/4b) and
the Jaisson-Rosenbaum limit-theorem line cited within them.
