# Deep-read session 61 (null-time session 72, log ## 79) — non-parametric neural marked-Hawkes kernels; the estimator family shown to pre-decide the excitation sign; zero sharpenings queued

Sobin Joseph and Shashi Jain (Department of Management Studies, Indian
Institute of Science, Bangalore), "Non-Parametric Estimation of
Multi-dimensional Marked Hawkes Processes" (arXiv:2402.04740v1
[stat.ML], 7 Feb 2024; "Preprint. Under review", PDF p. 1). Shallow
neural-network estimators of marked Hawkes kernels ϕ(t, m) as a joint
function of time and marks — SNH with marks (excitatory-only) and
NNNH with marks (inhibition allowed through a ReLU-clipped intensity)
— trained by MLE with an analytically integrated intensity, validated
visually on synthetic data and applied to a 30-minute Binance
BTC-USD/ETH-USD market-order window with trade volume as the mark.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x973a89_non_parametric_estimation_of_multi_dimensional_mar.txt,
24 pp., page-marked). Next UNREAD triage-rank entry (score 26).

## The paper in one paragraph

The paper extends the authors' Shallow Neural Hawkes (SNH) and Neural
Network for Non-Linear Hawkes (NNNH) estimators to marks: the kernel
ϕdj(t, m) is approximated by a two-layer feed-forward network (P
neurons, Eq. 10) whose SNH variant wraps the output in an exponential —
strictly positive, so strictly excitatory (Eq. 11, PDF pp. 8-9) — while
the NNNH variant leaves the kernel signed and clips the resulting
intensity at zero with an outer max (Eqs. 12-13, PDF pp. 9, 23-24). The
ground-intensity log-likelihood (Eq. 7, PDF p. 6) separates from the
mark-density term (Eq. 8), which is fitted by a Gaussian mixture under an
explicit i.i.d. and cross-dimension-independence assumption on marks
(PDF p. 10); the compensator is computed analytically by ordering the
ReLU zero-crossings (Appendix A, PDF pp. 22-24). Synthetic validation is
visual (kernel error plots and QQ plots, one-dimensional coupled-kernel,
decoupled non-linear, and 2-dimensional cases, PDF pp. 13-16); the real
application is 30 minutes of Binance BTC-USD and ETH-USD market orders
(16 July 2022, 02:00-02:30 UTC; 30,388 orders after collapsing
multi-counterparty fills into single orders, Table 1, PDF p. 17), where the
estimated kernels are read as volume-dependent self- and
cross-excitation of buy/sell arrivals (PDF pp. 17-18).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. The default grade is
earned: the paper's empirical base is a single 30-minute spot window
with visual-only validation (PDF pp. 13-18), it reports no branching
ratio, no dispersion statistic and no criticality reading (so it cannot
inform the C8 trigger threshold in either direction), and every
discipline-relevant mechanism it touches is already held by standing or
queued rules. The findings below therefore interpret, they do not queue.

1. [interpretation caution] The estimator family pre-decides the
   excitation SIGN: the SNH-with-marks kernel is exp(...) > 0 by
   construction (Eq. 11, PDF pp. 8-9) — it cannot express a damping or
   inhibiting kernel at all; the NNNH variant restores sign freedom but
   clips the intensity at zero through the outer ReLU (Eq. 12, PDF p. 9).
   Their own crypto reading shows the mark-gradient sign is
   heterogeneous across branches — buy-BTC self-excitation DECREASES
   with volume while sell-BTC stays flat and both ETH branches increase
   (PDF pp. 17-18) — so an excitatory-only or pooled estimation
   launders precisely the damping branches that the sign-register rule
   (deep-read session 10, log ## 16) and the per-branch rule (deep-read
   session 7) require to be reported two-sided with CI. This extends
   those standing rules' interpretation to mark-dependence signs; no
   queue change.
2. [reinforcing, no new item] The event-unit is a pre-processing
   decision with kernel consequences: a market order filled by multiple
   counterparties is collapsed into ONE event with summed volumes before
   estimation (PDF p. 17) — the opposite convention to the raw
   taker-print stream the programme's gated data uses; and their marks
   are coin-denominated, so mark scales across dimensions are
   incommensurable (ETH total volume ~10x BTC on fewer ETH events,
   Table 1, PDF p. 17). Reinforces the queued clock and event-grain
   pre-declarations and the unit-declaration sharpening: the kernel is
   a functional of the chosen event unit, and C1-L2's declared
   taker-print convention now has its page-cited counterexample.
3. [reinforcing, no new item] Non-parametric does not mean
   assumption-free: P = 64 hidden neurons, per-layer learning rates,
   initialization ranges and a 10-iteration validation-stop are all
   analyst degrees of freedom (PDF pp. 12-13), and the headline
   cross-excitation conclusion ("ETH trades influence BTC, not the
   other way around", PDF pp. 17-18) rests on kernels estimated under
   these unregistered knobs — same-day-class evidence for why the
   trigger layer pre-declares kernel family and estimator identity with
   the spec (deep-read session 2) instead of trusting a flexible
   learner's output shape.
4. [interpretation caution] Nothing here carries criticality or a
   branching-ratio reading, and the evaluation carries no numeric error
   table anywhere (kernel error plots and QQ plots only, PDF
   pp. 13-16, Figs. 3-10): no magnitude from this paper may be quoted
   in any spec, and its framework cannot support or oppose the 0.8
   trigger in either direction; the paper is relevant to the programme
   only as an estimator-family caution.
5. [source-quality note] arXiv v1, "Preprint. Under review" (PDF p. 1),
   authors citing their own prior work (SNH 2022, NNNH 2023) as the
   foundation; synthetic validation visual-only; empirical content is
   one 30-minute spot window on one venue, four "dimensions" (buy/sell
   × BTC/ETH); marks assumed i.i.d. within dimension with buy/sell
   independence explicitly assumed (PDF p. 10); mark selection in real
   applications admitted unresolved by the authors themselves (PDF
   p. 20); code repository linked (PDF p. 10); check the published
   version before any formal citation.

## What this paper would have killed if we had done it wrong

If the programme had ever adopted a "non-parametric" flexible marked
Hawkes estimator as the trigger layer because it looks assumption-free,
this paper is the worked counterexample of what that choice silently
decides: the SNH branch cannot output a negative kernel at all (the
output layer is an exponential, Eq. 11, PDF pp. 8-9), so an inhibitory
regime (the Poisson-cluster damping world of deep-read session 10, or
the negative-resilience mechanism of deep-read 53) measured through it
would have been forced into a positive, cascade-shaped reading; and the
NNNH branch's outer zero-clip (Eq. 12, PDF p. 9) writes clipping into
the compensator itself — the exact "floored at zero" move the
sign-register rule forbids, here implemented as architecture. The
pre-declared kernel family, the named estimator identity, the
two-sided sign register and the boundary-solution rule (deep-read
session 5) are jointly what keep an artifact like this from being
read as reflexivity.

## Standing caveat

A 2024 preprint under review; single-venue spot data, 30 minutes,
visual-only validation; the GMM mark density assumes i.i.d. marks within
dimension and independence across buy/sell dimensions (PDF p. 10), which
the microstructure the programme already holds (buy/sell volume
coupling) contradicts as an approximation; marks are coin units —
denomination- and venue-specific, so no magnitude transfers; the
event-collapse preprocessing (PDF p. 17) means their event stream is
not the raw taker-print stream. Applicability boundary: an estimator of
this family, if ever ported to a gated perp window, would need its
event-unit convention declared with the clock, its hyperparameters
registered with the spec, and its output read through the per-branch
sign discipline. The library is ammunition, not evidence.
