# Library deep-read session 28 — Mercuri, Perchiazzo & Rroji, "A
# Hawkes model with CARMA(p,q) intensity" (arXiv:2208.02659v3, 2022;
# Milan/VUB/Milano-Bicocca; a Hawkes process whose intensity is a
# CARMA(p,q) process, freeing the autocorrelation from monotone
# decay)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x8627c5_a_hawkes_model_with_carma_p_q_intensity.txt`,
~26 pp., page-marked). Next UNREAD triage-rank entry (score 32;
verified unread by the read-slug mapping; part of the shelf's
Hawkes-kernel-geometry cluster the program has been reading since
session 7).

## The paper in one paragraph

The motivation is a kernel-geometry constraint: a Hawkes process
with exponential kernel is Markovian and tractable, but its
autocorrelation function is constrained to be MONOTONE-DECAYING —
while empirical ACFs in several domains (wind speed, mortality
shocks, some insurance-claim series) are non-monotone, and an
exponential ACF "overshoots the empirical one for small lags and
vice versa for large lags" (PDF pp. 1-2). The proposed CARMA(p,q)-
Hawkes process lets the intensity itself follow a CARMA(p,q)
process, so the ACF of counting-increment series can take
non-monotone, oscillating shapes while keeping the self-exciting
Hawkes jump structure (the exponential-kernel Hawkes is the
CAR(1) special case; PDF pp. 3-11). The authors prove stationarity
and positivity conditions, strong mixing of increments (giving the
asymptotic distribution of the empirical ACF), compute the
likelihood, give a simulation method, and develop an estimation
route that matches model ACFs to empirical ACFs by least squares,
with MLE as a cross-check (PDF pp. 12-25). The application section
runs on SIMULATED series only — one standard Hawkes and one
CARMA(3,1)-Hawkes, with parameter recovery studies under MLE and
the ACF-matching estimator; no market data appears anywhere in the
paper (PDF pp. 24-26).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] The kernel choice CONSTRAINS the
   observable dependence shapes — a model's geometry decides what
   its fit can see.** The paper's whole reason for existing is that
   the exponential-kernel Hawkes — the workhorse of the entire
   endogeneity literature the program has been reading (sessions
   7, 9, 12-17, 26) — cannot produce a non-monotone ACF under ANY
   parameter values: fit it to data with oscillating dependence
   and the fit is silently wrong in a known direction (overshoots
   small lags, undershoots large lags; PDF pp. 1-2). This is the
   estimator-mode rule's (session 11) kernel-geometry face, stated
   by construction rather than empirically: any future
   arrival-timing diagnostic that fits an exponential-kernel
   Hawkes has already assumed monotone decay before seeing the
   data. The existing kernel/estimator-mode declarations already
   force the assumption to be stated; nothing new queued.

2. **[reinforcing, no new item] ACF-matching estimation targets a
   grain- and window-dependent object.** The moment-matching
   estimator fits to empirical autocorrelations of counting
   increments over intervals of length tau at lag delta — the
   object being matched depends on tau (PDF pp. 13-25), one more
   instance of the aggregation-endogeneity line (sessions 18/23):
   two ACFs at different increment sizes are different objects,
   and a CARMA(p,q)-Hawkes fitted to one is not a statement about
   the other. Reinforcement only.

3. **[source-quality note] Simulated-only application; the
   motivating data are not market data.** The empirical section is
   parameter-recovery on two simulated paths; the non-monotone ACF
   motivation comes from wind speed (Benth-Rohde), mortality
   (Hitaj et al.), and insurance claims (Swishchuk et al.) — NOT
   from any LOB. The correct citation use is the STRUCTURE (the
   Markov/car relation, the strong-mixing asymptotics, the
   positivity conditions); the paper contains no market fact and
   licenses none. arXiv v3, August 2022; a published version may
   exist (the CARMA-Hawkes line has journal descendants) — check
   before formal citation.

## What this paper would have killed if we had done it wrong

If any future L2 arrival-timing diagnostic (the trigger layer's
peripheral family) had been specified by default with the
exponential-kernel Hawkes, its fitted decay shape would have been
decided by the kernel before the data arrived — an oscillating or
hump-shaped empirical dependence would have been flattened into
the closest monotone the kernel can express, with no diagnostics
flagging it, since the fit "succeeds." The program's
kernel-declaration discipline (estimator-mode rule, session 11)
predates this read; the paper is its kernel-geometry face, stated
in print.

## Standing caveat

No financial data anywhere: the model's suitability for market
arrivals is asserted by lineage (the Hawkes-in-finance literature
it cites), not demonstrated; positivity conditions on the CARMA
parameters are non-trivial and load-bearing (negative intensities
must be excluded by assumption); the ACF-matching estimator's
asymptotics assume strong mixing, which the authors prove for the
model but which is an assumption if the model is wrong; the
simulated recovery studies use known-parameter ground truth no
market ever provides. Nothing here touches the daily-grain
closeness dossier (the parallel measured work of session 34 is at
a grain this paper's machinery does not address). Nothing trades
live.
