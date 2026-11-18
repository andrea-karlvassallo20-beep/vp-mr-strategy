# Deep-read 19 — Bergault & Cognéville, "Simulating and analyzing a sparse order book: an application to intraday electricity markets"

Library deep-read session 19 (null-time session 22, log entry ## 26).
Philippe Bergault (Université Paris Dauphine-PSL) and Enzo Cognéville (EDF
R&D & FiME), arXiv:2410.06839v1 [q-fin.TR], 9 Oct 2024: a simulator for
SPARSE limit order books, marked inhomogeneous Poisson event streams on a
moving K-limit window, calibrated on EPEX Spot German/French intraday
electricity.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x3ff3a4_simulating_and_analyzing_a_sparse_order_book_an_ap.txt,
22 pp., page-marked). Next UNREAD triage-rank entry (score 37); also the
corrected burst slot 04 assignment (corrigendum ## 24b names this slug as
slot 04's paper, so this read consumes that slot consistently).

## The paper in one paragraph

The authors model the K = 5 best limits per side with marked point processes
whose intensities are DETERMINISTIC functions of calendar time (and, for
market orders, of the spread): lambda_M(t,S) = lamM_bar * exp(-kM*(T-t)) *
exp(-bM*S), lam_L(t) = lamL_bar * exp(-kL*(T-t)), lam_C(t) =
lamC_bar * exp(-kC*(T-t)) (PDF pp. 15-16), with NO self-excitation anywhere
in the model. Marks come from parametric densities: market-order size
bounded by the visible opposite volume (one market order cannot consume the
K first limits, PDF pp. 6-7), exponential distance-to-opposite-best for new
limits with a time-varying parameter, discrete volume distributions
(PDF pp. 15-16). One order per price level is assumed, justified for sparse
books where stacking behind an occupied price is pointless (PDF p. 9).
When a limit leaves the K-window, a synthetic K-th limit is drawn as a
boundary condition (PDF pp. 9-10). Calibrated by least squares to EPEX 2021
hour products, the simulator reproduces the empirical intensity ramp toward
maturity (the Samuelson effect, documented there for ALL interactions, not
only price changes, PDF p. 4 Fig. 2), the level-by-level spread
distributions (first three limits within ~15% of historical means, PDF
pp. 18-19), and the realized-volatility signature plots (PDF pp. 19-20).
The authors print their model's main failure plainly: the simulated
distributions are too localized, the no-excitation construction lacks
extreme events, and Hawkes self-excitation is their suggested fix (PDF
p. 19).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] **The
   deterministic-clock null arm for the branching-ratio trigger.** The
   paper's books display strong event clustering with ZERO excitation: all
   clustering comes from deterministic calendar-time intensities (PDF p. 4
   Fig. 2, PDF pp. 15-16), and those clock-driven books still match the
   empirical spread distributions (PDF pp. 18-19) while provably missing
   the tails (PDF p. 19). Mechanism for C8: a window whose clustering fires
   the trigger may be firing on the calendar clock (session opens and
   closes, hour-of-day ramps), and the standing gates do not separate the
   two: the shuffled-arrival placebo destroys clock and excitation
   together, the ACF-shape gate is consistent with an inhomogeneous Poisson
   (disjoint-interval counts stay independent, so the ACF stays flat or
   decaying), and a mean-variance-style branching estimate is inflated by
   cross-window clock variance alone (Var(Lambda) > 0 raises n-hat above
   its true value of zero). Pre-declaration text: no branching-ratio
   trigger reading is admissible unless the apparent branching exceeds an
   inhomogeneous Poisson null whose deterministic intensity carries the
   same calendar-clock profile (hour-of-day, session segments), profile
   fitted on calibration windows DISJOINT from evaluation; the
   clock-explained fraction is reported, and clock-explained windows
   contribute no firing (neither positive nor negative). Harder to pass: a
   bar that survives the bootstrap-band, kernel-family, ACF-shape, and
   wash-audit gates can still die here. Tightens only the branching-ratio
   trigger family; generalizes the recorded hour-of-day stratification
   caution (deep-read 3: "seasonality removal is essential") from an
   estimation-window caution into an explicit null arm. No C1-L2 text
   moves.

2. [reinforcing, no new item] The boundary content is declared, not
   silent: beyond-K depth is SYNTHESIZED from parametric draws, harmless
   only around the inner limits and only for K large enough (PDF
   pp. 9-10). Independent support for the E1 volume-conservation
   declared-boundary-term discipline and the queued distance-grid
   sign-invariance rule: depth beyond the registered window must never be
   implicitly borrowed into a feature. Nothing added.

3. [interpretation caution] The model has no partial cancellations: a
   partial cancel is approximated as a full cancellation followed by a
   smaller insertion at the same limit (PDF p. 9). For depth persistence
   features (the queued size-state persistence comparator's territory): a
   volume reduction at an occupied level is NOT a level disappearance;
   conflating the two changes the state machine the feature assumes.
   Event-type mapping comes from the registered typology, never from this
   parsimony choice.

4. [reinforcing, no new item] Model-check honesty: validation by
   realized-volatility signature plots, whose value depends on the
   sampling step until it stabilizes (PDF pp. 19-20), and the printed
   failure of the simulator (underdispersed outputs, PDF p. 19). Supports
   the pre-registered sampling-scale discipline and the negative-result
   culture; no queue change.

5. [source-quality note] arXiv v1 only [q-fin.TR], 9 Oct 2024; no
   published version found this session; one author is EDF R&D staff (the
   venue's own market, declared honestly); empirical scope is EPEX
   electricity only, hour products, 2021, symmetric bid/ask parameters by
   calibration choice (PDF p. 15); fitting is least squares on functional
   forms the data "suggest" (PDF pp. 15-16), not likelihood. Check for a
   published version before formal citation; cite structure, never
   magnitudes, never parameters from this market.

## What this paper would have killed if we had done it wrong

Two deaths invited themselves. First, reading "Poisson reproduces the
spread distributions" as license to build C8's null family flat and
clock-free: the trigger would then fire on every predictable session ramp,
a false-positive machine the paper itself disarms by disclosing the same
construction lacks the tails. Second, citing the authors' "Hawkes would fix
the extremes" sentence as evidence that our market IS self-exciting: a
discussion-section proposal in an electricity paper promoted to support
for C8's mechanism. The library-is-ammunition rule bars both; this paper
earns exactly one null-arm pre-declaration and nothing else.

## Standing caveat

The book modeled here is sparse by construction and by market: gaps of
many ticks between limits, one order per price, no partial cancels, no
stacked depth, no excitation; where one side empties there is no mid-price
at all (PDF p. 3). None of its parameters, functional forms, or fitted
values transfers to a dense contemporary L2 tape, and the paper does not
claim otherwise. The transferable content is one structural fact:
deterministic calendar-clock intensity generates first-order event
clustering without excitation, and excitation's signature is dispersion
and tails, not means.
