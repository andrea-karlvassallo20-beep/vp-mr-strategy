# Deep-read session 12 — Mercuri, Perchiazzo & Rroji (2022), "A Hawkes model with CARMA(p,q) intensity"

Null-time session 14, parallel slot 19. Authors: Lorenzo Mercuri (Univ. of Milan),
Andrea Perchiazzo (Vrije Universiteit Brussel), Edit Rroji (Univ. of Milano-Bicocca).
arXiv:2208.02659v3 [q-fin.ST], 20 Aug 2022 version, 31 pp. A pure-theory point-process
paper: the Hawkes process generalized so the intensity follows a CARMA(p,q)
(continuous-time ARMA) process, with stationarity/positivity conditions, a closed-form
likelihood, a simulation scheme, closed-form autocorrelations of count increments, and
a strong-mixing/asymptotic-normality result for the empirical ACF.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/x8627c5_a_hawkes_model_with_carma_p_q_intensity.txt, ~31 pp.,
page-marked). Assigned triage-rank entry (score 32, pre-assigned to parallel slot 19 to
avoid duplicate work). Metadata from docs/library/expanded_index.json via the slug.

## The paper in one paragraph

The standard Hawkes process with exponential kernel is Markovian and tractable but its
autocorrelation function for count increments is provably strictly positive and
exponentially decaying in the lag (Prop. 1 / Eq. 9, PDF pp. 5-6, following Da Fonseca &
Zaatour 2014, PDF p. 2), while the authors note empirical ACFs in several applied
literatures reject that monotonicity (PDF p. 2: wind speed in Benth & Rohde 2019,
mortality shocks in Hitaj et al. 2019). Their remedy: drive the intensity as
λt = μ + b⊤Xt where Xt solves dXt = AXt dt + e dNt (Def. 2, Eqs. 17-18, PDF p. 8), i.e.
the excitation kernel becomes the CARMA kernel h(t) = b⊤eᴬt e instead of a single
exponential. They give non-negativity conditions for the kernel (Prop. 2, PDF pp. 8-9),
the stationarity condition −b⊤A⁻¹e < 1 (Prop. 3, PDF pp. 9-10), the infinitesimal
generator and first moments (Props. 4-5, PDF pp. 10-13), the exact likelihood via the
recursive statistic S(k) (Eqs. 46-54, PDF pp. 15-16), closed-form stationary variance and
autocovariance of count increments (Props. 6-7, Eqs. 64-67, PDF pp. 20-21), strong
mixing at exponential rate (Prop. 8, PDF pp. 21-22) and the CLT for the sample ACF
(Prop. 9, PDF pp. 22-23). Section 6 is entirely simulated data: a Hawkes fit and a
CARMA(3,1)-Hawkes fit on simulated series (MLE and an ACF-matching MME), with the
CARMA(3,1) ACF visibly non-monotone (Fig. 3(b), PDF p. 27). No financial data is
touched anywhere in the paper.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. **[candidate sharpening, PENDING OWNER RATIFICATION] — the ACF-shape
   (kernel-validity) gate on the branching-ratio trigger.** The paper's motivating
   result is exactly aimed at C8's trigger machinery: a Hawkes fit with exponential
   kernel implies a count-increment ACF that is strictly positive and strictly
   monotonically decaying in the lag (Eq. 9 and the surrounding discussion, PDF pp.
   5-6; stated as the model's central limitation, PDF p. 2), a testable implication the
   fitted model cannot escape. If the empirical ACF of the event-count increments on a
   fitted day is significantly non-monotone (e.g. a hump: lag-2 autocorrelation
   exceeding the exponential model's own band around its lag-2 fitted decay), the
   exponential-kernel specification is rejected by its own implications on that day,
   and the ML branching ratio ρ(Ĝ) from that fit is a misspecified quantity: the
   closed-form tail of the excitation kernel, what ρ summarizes, is not the object
   being estimated. Proposed pre-declaration text (to be frozen with the rest of C8's
   execution protocol, and to bind any future Hawkes-triggered kill or arm decision):
   NO day's branching-ratio trigger reading is admissible unless the underlying
   exponential-kernel fit passes a pre-registered ACF-shape check (empirical
   increment ACF inside the fitted model's own ACF bands, at a pre-declared lag
   ladder); a day failing the shape check contributes NO trigger firing (neither
   positive nor negative) and the failure rate is reported. This tightens the existing
   ratification-queue item recorded at deep-read session 2 (the estimator-at-scale-W
   rule, library note 2026-11-16_hawkes_branching_deep_read.md): that item froze scale
   and estimator; this adds shape validity of the fitted kernel. It is harder to pass
   because trigger bars that the old protocol would have fired on are now withheld
   when their own fit is shape-rejected, and the pre-declared lag ladder cannot be
   re-picked after seeing the data. It also names the sharper escape route honestly:
   if the BTCUSDT event-count ACFs systematically fail monotonicity, the correct C8
   amendment is a CARMA-type kernel (this paper's own subject), not a threshold move.

2. **[reinforcing, no new item]** Strong mixing at exponential rate for the count
   increments under stationarity (Prop. 8 via Cheysson & Lang 2020, PDF pp. 21-22) plus
   asymptotic joint normality of sample mean, variance, and autocovariances (Prop. 9,
   PDF pp. 22-23, Ibragimov-Linnik theorem 18.5.3, PDF p. 23) supports the existing
   inference discipline: C8's day-block bootstrap and C1-L2's day-blocked folds have a
   mixing-based license even under Hawkes-type clustering, PROVIDED the stationarity
   condition holds on the segment being estimated (Assumption 1, PDF p. 10:
   −b⊤A⁻¹e < 1, generalizing β > α, PDF pp. 4-5). Nothing measured, nothing queued.

3. **[interpretation caution]** The model is about the COUNTING process only: times of
   arrivals, never prices, signs, or book state (Def. 1-2, PDF pp. 6-8). Any future
   CARMA-Hawkes use in the programme would model event timing/clustering per branch,
   not order-flow sign or direction; the paper licenses no directional claim at any
   horizon. The market-microstructure mentions (order-arrival modeling, PDF p. 2,
   citing Bacry et al. 2013, Muni Toke & Yoshida 2017) are motivation by citation, with
   no empirical demonstration in this paper.

4. **[interpretation caution]** The closed-form ACF machinery (Props. 6-7, Eqs. 64-68,
   PDF pp. 20-21) exists only in the stationary regime and only under negative-real-part
   eigenvalue conditions on three matrices (A, Ã, Ãã; Assumption 1 and Props. 6-7,
   PDF pp. 10, 20). A non-stationary or boundary-critical segment (branching ratio
   near 1) violates the license for the ACF-based estimators (the paper's own MME
   restricts θ to the stationary, non-negative-kernel set, PDF p. 24); any pre-registered
   use of these formulas must carry the stationarity screen as a precondition, not a
   diagnostic.

5. **[source-quality note]** arXiv v3, 2020 MSC classes 37A25/47N30/60G55; every
   empirical exercise in Section 6 is on simulated data only (PDF pp. 24-27), so the
   paper provides NO empirical evidence that financial event ACFs are non-monotone
   (that claim rests on its cited applied literatures and on the simulated Fig. 3(b),
   PDF p. 27). Published version to be checked before formal citation. The award
   acknowledgment (JST CREST, PDF p. 28) is a pure funding note, no conflict signal.

## What this paper would have killed if we had done it wrong

If C8's trigger had been treated as "the branching ratio of the market" rather than
"the output of an exponential-kernel estimator at a pre-declared scale," this paper is
the counterexample sitting in wait: the estimator family we froze has a provable
implication (monotone decaying ACF, Eq. 9, PDF p. 6) that real event-count series can
violate, and under that violation the fitted ρ is not a biased-but-honest spectral
radius, it is a summary of the wrong kernel. A C8 result that fired on days whose fits
carried shape-rejected ACFs would have been a kernel-choice artifact with a 0.8
threshold stamped on it. The program's existing discipline (estimator-mode item queued
at deep-read session 2; math verification that caught the β-factor defect before the
threshold froze) is exactly what keeps this from being discovered post-mortem; the
shape gate below is that discipline extended one axis further, from scale to shape.

## Standing caveat

The paper proves properties of its own model; it demonstrates nothing on market data.
Its non-monotone-ACF claim for real data is inherited from citation, not measurement.
The estimation section gives MLE and an ACF moment-matching estimator on simulated
paths only, with no calibration difficulty analysis on irregular real timestamps
(bundling/packet clustering, the trap deep-read session 2 flagged, is not addressed
at all). Strong mixing is inherited from Cheysson & Lang (2020), arXiv preprint at the
time of citation; its proof assumptions (exponentially integrable kernel, Eq. 72,
PDF p. 22) must hold before the inference results are used. As with all
null-time readings: ammunition, not evidence; no empirical claim from this paper
enters the record as support for any program claim.