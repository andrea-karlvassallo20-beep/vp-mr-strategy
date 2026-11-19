# Deep-read session 43 — Filimonov and Sornette, "Apparent criticality and calibration issues in the Hawkes self-excited point process model: application to high-frequency financial data"

Library deep-read session 43 (null-time session 47, log entry
## 51). Vladimir Filimonov (Department of Management, Technology and
Economics, ETH Zurich) and Didier Sornette (ETH Zurich and Swiss Finance
Institute), arXiv:1308.6756v3 [q-fin.ST], stamped 3 Jul 2014 (index year
2013, first posting August 2013); 40 pp. text extract, page-marked,
complete (references PDF pp. 36-40). The third move of the disagreement
the library now holds in both directions: the Filimonov-Sornette reply
to the Hardiman-Bercot-Bouchaud ## 50 read. The paper argues that HBB's
n of roughly 1 is "apparent" criticality produced by five generally
upward estimation biases (outliers, power-law regularization choice,
edge effects, timestamp bundling, non-stationarity and regime shifts)
plus a multi-extrema likelihood surface whose suboptimal minimum sits
in the supercritical regime, and that the Filimonov-Sornette 2012-2013
results (n of 0.7-0.8, read as the landed ## 45) are upheld. Read
2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xd18d70_apparent_criticality_and_calibration_issues_in_the.txt,
40 pp., page-marked). Assigned triage-rank entry (score 30, xd18d70;
consumed as the next unclaimed UNREAD named by the landed ## 50's
closing pointer; no skips this session: the pointer checked out against
the live branch/PR set — zero open pull requests, no note for the slug
on main, no branch claiming it; the read-set was recomputed against all
notes on main by the established extract-path and normalized-title
method and xd18d70 was confirmed the next unclaimed UNREAD, with
x0fd75a the only other score-30 entry not in the read-set). Next
unclaimed UNREAD triage-rank entries: "Sequence Classification of the
Limit Order Book using Recurrent Neural Networks" (score 30, x0fd75a);
behind it "Trade arrival dynamics and quote imbalance in a limit order
book" (score 29, x5f04ef). A successor session must re-read the live
main tail and the branch/PR set first.

## The paper in one paragraph

Section 2 restates the Hawkes model with the three kernel shapes at
issue — exponential (Eq. (5), PDF p. 3), Omori-type power law (Eq. (6)),
the Kagan-Knopoff cutoff power law (Eq. (7)) as used by HBB through the
sum-of-exponentials approximation (Eq. (8), M = 15, m = 5, PDF pp. 3-4) —
the branching-ratio definition and its regime taxonomy (PDF pp. 4-5),
the MLE route with the standing caveat that finite-window calibration
errs DOWNWARD on n (pre-window ancestors are misattributed to mu, and
right-edge daughters are unobserved, PDF pp. 5-6), the residual-analysis
goodness of fit (time change (Eq. (10)), KS and Ljung-Box, PDF pp. 5-6),
and the subordinated (profile) optimization that makes the calibration
tractable (Eqs. (11)-(18), the Lyubushin-Pisarenko relation (17), PDF
pp. 6-7). Section 3 then works four calibration issues on synthetic
data: outliers (a 0.1-0.4 per cent tail of inter-quote durations at or
above twice Q99 in real data, Table 1, PDF p. 9; power-law kernels
"endogenize" them into spurious near-critical n while the exponential
kernel is robust, Fig. 1, PDF pp. 9-10); the regularization choice among
three power-law shapes alone biases n by up to roughly 0.2 and can
manufacture criticality from a true n of roughly 0.8, with AIC selecting
the correct model in the synthetic cases (Fig. 3, PDF pp. 11-13); edge
effects so extreme for small exponents that quasi-stationarity needs
roughly 100 times T0.99 (Table 3: for epsilon = 0.15, T0.99 is 1.3e9
seconds, about 57,778 trading days, PDF pp. 14-15), which makes HBB's
two-month windows formally unable to see the kernel's reach; and a
likelihood surface with multiple extrema on real data, where the global
minimum of a two-month 2001 calibration sits at n = 0.0751 while the
local minimum a wrong start converges to sits at n = 1.1054, with the
HBB published estimates reported as "very close to" the suboptimal one
(Figs. 6-7, PDF pp. 17-19). Section 4 turns to the data: overnight
events are 30-67 per cent of daily mid-price changes in recent years
(Fig. 8, PDF pp. 19-20); FAST/FIX packetization makes the effective
timestamp resolution 300-1700 ms inter-package plus processing overhead
up to 1300 ms before 2009 (Figs. 9-10, PDF pp. 21-24); randomizing
bundled timestamps within intervals smaller than the bundling scale
manufactures clustering, so that pure Poisson data randomized at the
millisecond calibrates to n of roughly 0.856 and near-critically with
enough events per package (Figs. 12-13, PDF pp. 25-26); average-day
U-shape detrending attributes exogenous news spikes (the September 18,
2007 FOMC example) to endogenous self-excitation (Fig. 14, PDF pp.
27-29); and day-level regime shifts alone — independent Poisson days
with real daily intensities concatenated in HBB's two-month windows —
calibrate to n hovering around 1 for the whole 1998-2012 span with
residual analysis unable to reject the null, though the true branching
ratio is zero by construction (Figs. 15-17, PDF pp. 30-33). Section 5
concludes the five upward biases are "largely sufficient to explain the
discrepancy", upholds the authors' previous results, and extends the
warning to all inter-event-time studies and to long-memory estimation
from high-frequency data generally (PDF pp. 34-35).

## Findings, graded (does any kill line move?)

**Grade: NO kill line changed; ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION: the optimizer-path (multi-start) disclosure
rule for the estimator-discipline family.** The paper is otherwise a
dense stack of worked exhibits for registers already standing, in both
directions of the disagreement. Findings, page-cited:

1. **[candidate sharpening, PENDING OWNER RATIFICATION]** The
   multi-extrema exhibit is a mechanism none of the standing
   estimator-discipline components covers. The cost surface of a Hawkes
   calibration has "one pronounced minimum" under correct specification
   (PDF p. 17) — which real data, by the programme's own default
   assumption that the true process is not Hawkes, is not expected to
   satisfy: the authors state that for real data, noise, outliers and
   misspecification make the surface "non-trivial with several local
   minima" so that "local descent methods are not sufficient" (PDF
   p. 17). The concrete exhibit: on the March-April 2001 E-mini
   two-month calibration, the global optimum is mu = 0.3031, n = 0.0751
   (deeply subcritical, cost 2.09e5) while the local optimum found from
   a wrong starting point is mu = 0.0150, n = 1.1054 (supercritical,
   cost 2.85e5), and the authors report the HBB published estimates as
   "very close to" the suboptimal minimum (Fig. 6, PDF pp. 17-18): at
   the published-record level, the critical-versus-subcritical
   disagreement is partly an optimizer-path artifact, with the two
   solutions "in completely different regimes" of the same declared
   model on the same data (PDF p. 18). Deep-read 2's arming conditions
   pre-declare the estimator identity, the window scale and the
   timestamp-bundling two-minimum trap (the C8 arming condition 3), and
   the estimator-at-scale-W item governs scale; none of them govern the
   search itself. Two implementations of the same named estimator with
   the same declared window and the same clock, differing only in
   starting points, return optima on opposite sides of the trigger
   threshold. Pre-declaration text: any pre-registered parametric fit
   must declare, recorded on TRAIN before evaluation data is touched,
   the optimization protocol — algorithm, starting-point scheme
   including the number and placement of multi-starts, convergence
   tolerance and boundary handling — and every reported optimum must
   carry the multi-start evidence that it is the best optimum the
   declared search found; a single-start local optimum is inadmissible
   as a trigger reading; whenever a second optimum lies within a
   pre-declared likelihood-distance band of the reported one, its
   parameter values and the likelihood gap are reported alongside.
   Harder to pass: a fit whose headline parameter sits on one side of
   a decision boundary while a likelier optimum sits on the other is
   inadmissible under the old protocol only if someone happened to
   look; the rule makes looking mandatory and pins the search before
   the data can choose the answer. It tightens only the
   estimator-discipline family (deep-read 2's estimator-identity
   condition and, through it, every pending arm that fits a parametric
   likelihood); no C1-L2 or C8 text moves, no kill line moves, no
   threshold moves, and the component stays dormant if no admissible
   spec functional fits a parametric likelihood at all.

2. **[reinforcing, no new item]** Regime-shift spurious criticality is
   the strongest single worked exhibit yet for the non-stationarity
   half of the estimator-mode register, and a direct design exhibit
   for the queued deterministic-clock null arm: concatenated
   independent Poisson days with intensities taken from the real data
   (true n = 0 by construction) calibrate to n hovering around 1
   across 1998-2012, robust to removing short trading days, and a
   mild-truth variant (exponential Hawkes, true n = 0.3) calibrates
   super-critical with an estimated epsilon of 0.1-0.3, "similar to
   what is reported by [4]" (Fig. 17, PDF pp. 32-33). Mixing two
   stationary Hawkes realizations never yields an intermediate
   estimate: n of the concatenation is always no less than the larger
   component, reaching 1 when the components are n = 0.5 and n = 0.2,
   and a 40 per cent background-activity difference with true n = 0.5
   reads 0.9, a 60 per cent difference reads 1 (Fig. 16, PDF pp.
   30-31). And the residual analysis "cannot reject the null
   hypothesis of Poisson residuals" for the regime-switching
   generation (PDF p. 33): goodness-of-fit cannot certify a model
   class when the null the data imposes is intensity-inhomogeneous —
   the C8 A3 shuffled-arrival placebo and the deterministic-clock null
   arm are the programme's concrete instantiation of exactly this
   lesson, and the exhibits are ammunition for them, never substitutes
   for them. The register and the queued arms stand; nothing is
   added here, and the day-level intensity structure visible in
   Fig. 15 (activity varying by a factor of 2-5 within two-month
   windows, PDF p. 30) is design input the owner may consider when
   the deterministic-clock null's intensity enumeration is ratified;
   nothing is queued for it because what it enumerates belongs to
   that arm's ratification text, not to this note.

3. **[reinforcing, no new item]** Outlier "endogenization" adds the
   missing robustness direction to the kernel-family register: on
   synthetic n = 0.7 with a 1 per cent fraction of durations
   stretched by M = 2, power-law fits read n of roughly 0.98; with
   M = 5, a 0.17 per cent fraction suffices for spurious criticality
   or supercriticality, while the exponential-kernel fit stays within
   one standard deviation of the truth (Fig. 1, PDF pp. 9-10), the real
   tail being 0.1-0.4 per cent of durations at or above twice Q99
   (Table 1, PDF p. 9). Combined with ## 50 the record now holds both
   directions of the kernel-family tradeoff on one shelf: the rigid
   kernel that resists outliers is the kernel that misses true long
   memory; the flexible kernel that reads long memory is the kernel
   that manufactures endogeneity from outliers. No kernel family wins
   both tests on any given dataset; a future fit citing either family
   must disclose its outlier exposure with the same paragraph that
   discloses its window and clock. The register stands, nothing
   added.

4. **[reinforcing, no new item]** The bundling mechanism mechanizes
   deep-read 2's arming condition 3 and gives the L0 timestamp audit
   its causal story: exchange FAST/FIX protocol stamps seconds, the
   provider stamps millisecond arrival times on packages whose
   inter-arrival averaged about 1 second before 2009 with processing
   overhead up to 1.3 seconds, so "it is unacceptable to ignore the
   uncertainty in the timestamps by assuming a millisecond resolution"
   (PDF pp. 21-24). Randomizing bundled events within an interval
   smaller than the true bundling scale manufactures spurious
   clustering whose asymptotic spurious n depends only on the mean
   events per package (Figs. 12-13, PDF pp. 25-26) — which charges
   ## 50's finding 4 with its mechanism: HBB's within-millisecond
   randomisation presumes a bundling scale of at most one millisecond,
   and the paper's own Fig. 10 sample shows the scale in 2002-2008 was
   300-1700 ms. The exchange-clock-and-identical-timestamp-fraction
   disclosure required by deep-read 2, and the L0 100-timestamp
   intake audit, stop precisely this artifact; both stand, and this
   paper may never be cited as precedent for relaxing either.

5. **[interpretation caution]** The signs of the estimation errors do
   not cancel by themselves: the paper's own section 2.3 records the
   finite-window MLE bias as DOWNWARD (pre-window ancestors inflate
   mu, PDF pp. 5-6 — consistent with, and a sibling exhibit to, the
   ## 48 Appendix-B near-critical downward bias), the edge/transient
   effects of section 3.3 are DOWNWARD for small exponents (Fig. 5,
   PDF pp. 15-16), while outliers, regularization mismatch, bundling,
   regime shifts and suboptimal optima are UPWARD (sections 3.1, 3.2,
   4.2, 4.4, PDF pp. 9-13, 25-26, 30-33). A future programme reading
   quoting any single signed bias for this estimator class is
   inadmissible: every disclosed source is signed, the net can land
   on either side of the boundary, and the disclosure list (window
   scale and reach, kernel family and regularization form, outlier
   exposure, bundling scale, regime protocol, optimizer path) is
   mandatory framing for any n estimate the spec tables ever show.
   Model-relative conditions carry; no queue change.

6. **[interpretation caution]** Selection-of-windows is itself a
   reading mode, and the two camps' procedures fail in opposite
   directions on the same instrument: HBB's RTH-only concatenation
   discards 30-67 per cent of daily mid-price changes in recent years
   (Fig. 8, PDF pp. 19-20) and its average-day detrending then
   attributes genuinely exogenous spikes to self-excitation by
   construction — the September 18, 2007 FOMC surprise counted as
   endogenous (Fig. 14, PDF pp. 27-29); the authors' own short-window
   alternative excludes announcement days entirely (PDF p. 30),
   which removes precisely the windows where a null's failure mode
   is loudest. No windowing or day-selection protocol is neutral as
   between the null and the trigger; whichever the C8 family ever
   ratifies must declare its windows, day selection and detrending
   on TRAIN like every other conditioning choice. Interpretation
   discipline only; the no-single-mode register governs; nothing
   queued.

7. **[interpretation caution]** The paper's closing sweep against
   long-memory estimation — "it is very difficult if not impossible
   to estimate reliably long-memory effects using high-frequency
   financial data", and long-memory findings "can result entirely
   from the non-stationarity in the high-frequency financial time
   series" (PDF p. 34) — applies with full force to ## 50's two-regime
   DFA structure: a Hurst exponent of roughly 0.95 above the 1000 s
   scale is exactly what day-to-day intensity drift of the magnitude
   of Fig. 15 (factor 2-5, PDF p. 30) would produce without any slow
   kernel regime at all. Both papers' long-memory and criticality
   numbers are therefore regime-inhomogeneity-confounded at this
   venue and grain: neither the epsilon of roughly 0.15/0.45 split,
   nor the tabled characteristic times of Table 3, nor any "markets
   are critical" reading from either line is citable without a
   stationarity protocol the venue can actually support. No exponent
   enters anything; interpretation discipline only.

8. **[source-quality note]** An adversarial reply by the challenged
   party: the authors are defending their own 2012-2013 numbers, and
   the paper's framing ("our previous results are upheld", abstract,
   PDF p. 1) is a position, not a neutral calibration study; the
   acknowledgements credit Stephen Hardiman and Jean-Philippe
   Bouchaud for "many long and fruitful discussions" and Spencer
   Wheatley for the outlier section (PDF p. 35), so the exchange was
   partly cooperative, and a further HBB response to this reply is
   expected in the literature and is NOT on the shelf (gap declared,
   to be acquired before the disagreement's file is closed). Journal
   record NOT checked at reading — arXiv v3, 3 Jul 2014; index year
   2013; published version to be checked before formal citation.
   Single venue (E-mini S&P 500 futures), single provider database
   (Thomson Reuters Tick History) for the microstructure exhibits,
   simulations elsewhere; the C5 frozen-book blind spot repeats: a
   queue-frozen book generates no mid-price changes, so the frozen-book
   regime is invisible to this event definition by construction (the
   same structural blind spot recorded for ## 45 and ## 50). The
   closing claim that "most if not all studies" of inter-event times
   should be revisited (PDF p. 34) is an argument, not a
   measurement. Grade honestly: an adversarial, technically strong
   reply; interesting precisely because its mechanism exhibits are
   correct regardless of whose side they help.

## What this paper would have killed if we had done it wrong

Had this reply been read as closing the debate — "the rebuttal of the
rebuttal, therefore Filimonov-Sornette wins" — the library would have
converted reply-count into truth and settled the disagreement by
sequence rather than by measurement, in exactly the way the record's
both-directions rule forbids. Had the multi-extrema finding been
confined to the paper's own 4-parameter power-law fit and the
programme's exponential-family MLE silently exempted, the exemption
would have died the first time a real non-Hawkes day handed the
3-parameter surface a second minimum — the paper's own section 4.4
shows the spurious-criticality mechanism is "not unique to the
approximate power law kernel" but holds with exponential kernels
under non-stationarity (PDF p. 33), and its section 3.4 states the
single-minimum property is a correct-specification property (PDF
p. 17) — real data is what the programme assumes it never has. Had
the regime-shift Poisson exhibit been adopted as ammunition against
HBB only, the programme's own pending arms (the deterministic-clock
null, the A3 shuffled-arrival placebo) would have missed that
day-level regime mixing is a symmetric failure mode that its nulls
must enumerate, not just the other camp's. Had the overnight-exclusion
finding been imported as a programme prescription (keep overnight
data), it would have laundered a venue-conditional artifact of
23-hour futures sessions into the crypto L2 stream, which has no
comparable session structure at all. The estimator-mode register,
the both-directions rule, the default assumption of misspecification
and the nulls-not-substitutes discipline prevented all four.

## Standing caveat

Single venue, single instrument for the data exhibits (E-mini S&P 500
futures, 2001-2012 in the calibration exhibits, 1998-2012 in the
synthetic-intensity reconstruction), Thomson Reuters Tick History
timestamps for the microstructure sections, millisecond nominal
resolution with second-scale exchange protocol underneath (PDF pp.
21-24); the RTH/overnight structure, the U-shape, the
announcement-day calendar and the three-times-zone session split are
properties of that venue and none of them transfers to the
programme's 24/7 crypto venue; every synthetic result is conditional
on the simulated kernel family (Eqs. (5)-(8)), the burn-in treatment
and the parameter values chosen to mimic 2001-2012 E-mini; the
authors' own procedure (10-30 minute RTH windows, announcement days
excluded) is a reading mode subject to the same selection caveat its
criticism of HBB establishes; the gap in the shelf — neither the HBB
response to this reply nor the journal versions — must be closed
before the disagreement file is cited as complete. arXiv v3,
published version NOT checked at reading. Laundering directions
named: INTO — nothing; no branching value, no bias sign, no kernel
shape, no bundling scale, no T0.95/T0.99 characteristic time, no
randomization interval, no windowing protocol, no detrending scheme
and no regime-shift exhibit from this paper enters any spec,
default, calibration, tolerance or generative null; the disagreement
stays open in both directions, unsettled by this reply as it was
unsettled by the ## 50 rebuttal; the one thing this paper licenses
into the pending state is the optimizer-path (multi-start)
disclosure rule, queued as PENDING OWNER RATIFICATION and inert
until ratified. OUT — never read backwards as "Filimonov-Sornette
won the debate" (adversarial reply, reply-count is not truth),
"exponential kernels are vindicated" (this paper's own exhibits
3.1, 4.4 show exponential fits failing under outliers and
non-stationarity), or "long memory does not exist in markets" (an
estimation-impossibility argument at this venue and grain, not a
market property).
