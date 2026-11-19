# Deep-read session 46 — McGillivray and Swishchuk, "Variance-Hawkes Process and its Application to Energy Markets"

Library deep-read session 46 (null-time session 50, log entry ## 54).
Joshua McGillivray and Anatoliy Swishchuk (University of Calgary,
NSERC-supported, PDF p. 16), arXiv:2410.08420v1 [q-fin.MF], 10 Oct 2024:
a modelling paper that defines the variance-Hawkes process B(Nt), a
standard Brownian motion with a (discontinuous, pure-jump) Hawkes
subordinator, hand-fits it to 2018 and 2019 front-month WTI crude oil
and NYMEX natural gas futures log returns, derives its generator and
an Ito formula, conjectures its distribution, and gives closed forms
for second and cross moments of the Hawkes process and its intensity
under an exponential kernel.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x618573_variance_hawkes_process_and_its_application_to_ene.txt,
24 pp., page-marked, read in full). Next UNREAD triage-rank entry
(score 29), selected per the session-49 pointer and re-verified unread
against all library notes on main at session start; no shelf gap, no
inaccessibility.

## The paper in one paragraph

The authors subordinate a standard Brownian motion by a simple
exponential-kernel Hawkes process, Vt = B(Nt), arguing that price moves
with trade arrivals, so a discontinuous counting subordinator is a more
faithful "business time" than the continuous subordinators (gamma,
inverse Gaussian) usual in the time-change literature (PDF pp. 5-7). A
simple clustered-Gaussian model a + sigma-hat * B(Nt) is "fit" to the
log returns of one year each of 2018/2019 natural gas and crude oil
front-month futures by hand, "using trial and error" with parameters
v0 ≈ 400, v ≈ 400, β = 800, α = 700 (so branching ratio α/β = 0.875) and
an arbitrary coefficient b = 1/e, with distributional overlap judged
visually (PDF pp. 7-9, Figs. 2-5). Supporting motivation: per-minute
2024 trade-volume quantiles of WTI and Henry Hub futures do not follow
exponential quantiles and volume clusters by time of day, "not ...
expected under a Poisson model" (PDF pp. 10-11, Figs. 6-9). The paper
then derives the generator of (lambda_t, Nt, B(Nt)) termwise from the
Cui-Hawkes-Yi moment recurrences (PDF pp. 12-14; closed moment forms in
Appendix B, PDF p. 24), proves the Ito identity dB^2(Nt) =
2B(Nt)dB(Nt) + dNt and checks it against Euler-Maruyama simulation with
errors mostly within ±20% plus discretization spikes (PDF pp. 14-15,
Figs. 15-17), and closes with Conjecture 1, that B(Nt)/d ~ sqrt(Nt)
N(0,1), supported only by Monte Carlo distribution matching (PDF pp.
15, 19-20, Fig. 14).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] — Another high branching ratio appears
   as a matter of course: the hand-picked fits carry α/β = 700/800 =
   0.875 on daily energy futures (PDF pp. 8-9, Figs. 2-5), adding an
   energy-markets, daily-grain instance to the running exhibit
   (deep-reads 20 and 21's FX RFQs 0.86-0.90; 0.92 synthetic) that
   near-critical fitted branching is commonplace and
   specification-sensitive. Supports the near-critical
   regime-disclosure rule's disclosed-regime requirement; no rule
   moves, and this paper's 0.875, being hand-chosen, may not be read as
   a measured market quantity at all.

2. [reinforcing, no new item] — The calibration is explicitly
   non-statistical: "we chose to fit these datasets by hand using trial
   and error" because "a calibration method has not yet been vetted"
   (PDF p. 7), the coefficient b is fixed at 1/e for convenience (PDF
   p. 8), and the fits are described as "not as precise as they could
   be had they have been chosen mathematically" (PDF p. 8). A worked
   exhibit for the estimator-discipline family (estimator-identity
   pre-declaration, and the optimizer-path multi-start disclosure
   component queued through deep-read 43): hand-tuned distributional
   overlap can never support a calibration claim; under the queued
   declarations such a fit is dead on arrival, which is why no new
   arm is needed.

3. [reinforcing, no new item] — The subordination argument is the
   programme's own flow-clock position stated independently: prices
   progress in trade-arrival time, and continuous subordinators are
   approximations of a discontinuous arrival-count process (PDF pp.
   5-6); the exponential kernel is the only Hawkes kernel admitting a
   Levy-process reading (PDF p. 7, after Bacry et al. 2015). Supports
   the flow-clock scale-constant rule (one declared clock for all
   rates) and the ACF-shape kernel-validity gate's pre-registration
   requirement (the kernel family is structural, not a free knob).

4. [interpretation caution] — Conjecture 1, that the subordinated
   process is conditionally Gaussian, B(Nt)/d ~ sqrt(Nt)N(0,1), is
   unproven and evidenced only by Monte Carlo distribution matching
   across 2^14 simulations (PDF pp. 15, 19-20, Fig. 14). If any future
   generative null or simulation layer ever uses subordinated-normal
   forms, the arrival-time conditional normality it assumes must be
   tested on programme data, not imported from this conjecture; a
   conjecture in the library charges a caution, never a null.

5. [interpretation caution] — The empirical clustering exhibits are
   coarse-grain and off-venue: per-minute trade-volume quantiles and
   intraday volume profiles of 2024 WTI and Henry Hub futures (PDF
   pp. 10-11, Figs. 6-9), plus daily closes sourced from Marketwatch
   (PDF p. 17). They justify the authors' modelling choice on their
   market only; they are not evidence that BTCUSDT arrivals cluster,
   and the paper's own chain (order-arrival clustering claimed, trade
   volume measured) is loose. Reinforces the ammunition-not-evidence
   boundary; no queue change.

6. [source-quality note] — arXiv v1, no peer-reviewed venue verified at
   reading (uncertain, flagged); NSERC-funded university preprint with
   the authors' own "future work" including calibration, the
   distributional proof, and risk-neutral valuation (PDF p. 16),
   i.e. the calibration and distribution theory the programme would
   care about are declared open by the authors themselves; four
   one-year daily datasets with no goodness-of-fit statistics, no
   likelihood, no stability check (though the exponential kernel with
   α/β = 0.875 is stationary), and front-month futures series with
   unaddressed roll effects. Check the published version before formal
   citation.

Laundering directions named: INTO — nothing from this paper may enter
any spec, calibration table, null model, or trigger bar: the 0.875
branching is a hand-picked parameter, the fits are visual overlays, and
Conjecture 1 is unproven; OUT — the paper's smallness may not be read
backwards as "subordination framing is worthless": its subordination
argument independently supports the flow-clock position, and its honest
lack of a vetted calibration is exactly the discipline the
estimator-discipline family already demands of the programme.

## What this paper would have killed if we had done it wrong

Had the α/β = 0.875 "fits" been read as measured near-criticality,
distributional overlap produced by trial-and-error parameter choice
would have been laundered into a criticality claim about a market the
programme does not trade — the exact failure the near-critical
regime-disclosure and estimator-discipline rules block. Had Conjecture
1's Monte Carlo agreement been accepted as proof, a future generative
null could have embedded an unproven conditional-Gaussian identity
(perpetuating the square-root-of-time-in-event-time tradition without
tests, precisely how specification assumptions smuggle into
generative-null layers). Had the per-minute energy-volume quantile
exhibits been cited for BTCUSDT, an off-venue, coarse-grain exhibit
would have charged a crypto claim.

## Standing caveat

arXiv v1, no peer-reviewed venue verified (uncertain, flagged); hand
calibration only; daily Marketwatch closes on front-month futures
(roll effects unaddressed); energy futures only, never crypto; the
distributional claim is conjectural; moments are exponential-kernel
specific; the Ito-formula check is Euler-Maruyama with visible
discretization error spikes. The library is ammunition, not evidence:
nothing in this paper enters any spec, default, kill line, threshold,
or generative null; it charges warnings only.
