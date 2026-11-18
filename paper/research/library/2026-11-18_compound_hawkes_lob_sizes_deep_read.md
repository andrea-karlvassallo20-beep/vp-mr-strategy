# Deep-read session 21 — null-time session 24: compound Hawkes
order-book dynamics with calibrated order sizes

Jain, Firoozye, Kochems, Treleaven, "Limit Order Book Dynamics and
Order Size Modelling Using Compound Hawkes Process" (arXiv:2312.08927v5,
first posted 2023, revised 2024-08-14; UCL and J.P. Morgan Chase & Co.).
A 12-dimensional compound Hawkes simulator for the top of a NASDAQ
equity order book, with order sizes sampled from calibrated
distributions and mechanical-spread, time-of-day, and inhibitory
constraints enforced on the intensities.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x798515_limit_order_book_dynamics_and_order_size_modelling.txt,
15 pp., page-marked). Next UNREAD triage-rank entry (score 34).

## The paper in one paragraph

The authors model six queues around the touch (best bid/ask and the
one-tick levels either side) as a 12-dimensional compound Hawkes
process: one dimension each for limit, cancel, and market orders per
queue and side, with each event's size drawn from a fitted
distribution spiked with Dirac masses at round order sizes (PDF pp.
1, 4, 7; round-number spikes also pp. 1-2). Spread positivity is
enforced by scaling in-spread limit-order intensity as (s-1)^beta
with the intensity floored to zero at one tick (PDF pp. 4-5);
time-of-day seasonality enters as a separable 30-minute-bin
multiplier f(Qt) (PDF p. 4); inhibitory cross-excitations are allowed
with total intensity floored at zero (PDF pp. 2, 5). Calibration is
a modified non-parametric least-squares AR method with sign-uniform
kernels and a linearized stationarity constraint, plus a heuristic
that rescales all kernels to cap the norm-matrix eigenvalue at 1 when
the fit violates stationarity (PDF pp. 5-6); power-law kernels beat
exponential ones at 100% AIC selection (PDF p. 7). On Apple 2019
Level 2 data the simulator reproduces signature plots, inter-arrival
shapes, spread distributions, and time-of-day shapes better than a
12D Poisson baseline (PDF pp. 7-9); a constant-order-size variant
overestimates volatility by roughly 100x (PDF pp. 8-9); a
market-impact study replicates concave impact in meta-order size but
exposes a simulator artifact, impact driven by trade COUNT rather
than volume, which the authors attribute to their own
size-independence assumption (PDF p. 10, PDF pp. 9-10).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Default grade; the
mechanisms this paper exhibits are worked examples of two rules
already standing in the ratification queue.

1. [reinforcing, no new item] The d-dimensional worked example of the
   boundary-solution pathology, reinforcing the queued
   boundary-solution rule (deep-read session 5). A standard Hawkes fit
   is stable only if the kernel-norm matrix's maximal eigenvalue is
   below one; the authors state plainly that in practice their
   calibrated kernels "occasionally violate" that constraint, and
   repair the fit by "multiplying all the kernels by a regularizing
   term to cap the eigenvalue at 1" (PDF p. 6) — a silent post-hoc
   rescale that lands the fit exactly ON the constraint boundary.
   The exogenous baseline is likewise repaired post-hoc: the
   non-parametric exogenous estimate is "massively overestimated
   because of the cut-off error and the distributional errors"
   (PDF p. 6), so they rebuild it from the average intensity via
   (I − M)^-1 times Lambda-hat (PDF p. 6, eq. 23). This licenses
   nothing new: under the boundary-solution rule, a branching reading
   pinned to the boundary by a rescale-or-repair pipeline is MISSING,
   not high, not near-critical; under the near-critical
   regime-disclosure rule, only the disclosed estimate chain counts
   as the regime. What it does license: this is no longer a one-paper
   pathology; the optimizer-wall lesson now has a second,
   multidimensional exhibit.

2. [reinforcing, no new item] The exogenous share of fitted
   excitation is an estimator-pipeline PRODUCT, reinforcing the
   near-critical regime-disclosure rule (deep-read session 17). The
   split between exogenous and endogenous intensity in this paper
   depends on a declared cut-off grid, a sign-uniformity constraint,
   a kernel-norm threshold that "zeroes out" small cross-excitations
   (65 of 144 kernels retained at threshold 0.01, PDF p. 7), intensity
   flooring for inhibitory kernels (PDF pp. 2, 5), and the rescaling
   heuristic above. The same fitted history can yield different
   branching readings under different declared pipelines. Disclosure
   of the pipeline, and the regime, before any window narrates a
   branching number: this is exactly what the queued rule already
   demands; the paper adds a named worked example.

3. [reinforcing, no new item] A seasonality-naive null is a broken
   null, reinforcing both the deterministic-clock null arm (deep-read
   session 19) and the hour-of-day stratification rule. The 12D
   Poisson baseline, which carries no U-shape conditioning, produces
   a flat signature plot and misses the inter-arrival and
   price-change-time distributions wholesale (PDF pp. 8-9); the
   Hawkes model reproduces the U-shape only because the f(Qt)
   multiplier is separable and declared (PDF pp. 4, 7, 10). For the
   queued null arms this means: any deterministic-clock null or
   shuffled-arrival placebo must carry the declared deterministic
   seasonality (the same time-of-day multiplier, the same spread
   state dependence), or the two-null comparison fires for the wrong
   reason — seasonality, not memory. Nothing new queued; the null
   arms as drafted already demand the declared-clock form.

4. [reinforcing, no new item] Time-only excitation is formally silent
   about size/marks, reinforcing the size-state persistence
   comparator already in the queue. The paper's own postulate —
   arrival intensities unaffected by past order SIZES — rests on weak
   evidence they concede is weak ("albeit with weak evidence",
   Hoeffding statistic 0.00068, one stock, PDF p. 11, Appendix A) —
   and their own market-impact study then exposes the cost of the
   assumption: simulated impact rises with trade frequency rather
   than volume, "counter-intuitive to the real world phenomenon of
   adverse selection", which they name as "a potential missing piece
   in our simulator" (PDF p. 10); the constant-order-size variant
   overestimates volatility by about two orders of magnitude
   (PDF pp. 8-9). A memory measured on event counts alone may not be
   narrated as a volume-flow or impact fact; that is what the queued
   comparator rule already governs.

5. [interpretation caution] Near-touch flow features must declare
   their spread-state normalization before the first L2 run. In-spread
   limit-order intensity scales empirically as (s-1)^beta with beta
   around 0.75 for the fitted stock (R-squared 0.85, PDF p. 11,
   Appendix B), and the fitted simulator conditions in-spread
   arrivals on the current spread (PDF pp. 4-5). A count of in-spread
   or near-touch arrivals with no spread-state normalization drifts
   with the spread distribution, not with information flow. This is a
   reading discipline for any future reconstruction feature built at
   the touch; no queue item added, no measurement proposed.

6. [source-quality note] UCL/JPMC practitioner preprint, arXiv v5
   (revised 2024-08-14), funded by J.P. Morgan Chase & Co. with a
   dealer disclaimer (PDF pp. 1, 15). The primary calibration,
   NASDAQ 2019 Apple, one medium-tick stock (average spread 1.7
   ticks); the authors themselves report their own model unsuitable
   or misfitted for small-tick and very-small-tick names: Tesla and
   Amazon spreads and volatility severely underestimated, Intel
   left-tail misfit (PDF pp. 10-11, Appendix C). Recommended
   citation: check for a published version before formal use.

## What this paper would have killed if we had done it wrong

Had the programme ever accepted a simulator's fitted kernel matrices,
branching readings, or a homogeneous null as a stand-in for a
registered test, the artifacts this paper itself displays — volatility
overestimated 100x under constant order size (PDF pp. 8-9), a
seasonality-free Poisson null failing wholesale on shape statistics
(PDF pp. 8-9), kernels silently rescaled to the stationarity boundary
(PDF p. 6) — would have manufactured firings or kills on machinery,
not on markets. The library-is-ammunition rule (no empirical claim
from any paper enters the record as support for any programme claim),
the registered-gate requirement, and nothing-measured-during-null-time
are the disciplines that kept this paper's calibrated numbers out of
the trigger bars. The paper earns reinforcement of those disciplines,
nothing else.

## Standing caveat

The model sees only six queues at the top of one side each of the
book; 97.4% single-tick in-spread behaviour is an assumption the
authors measured on their stock but one they state fails for
small-tick names (PDF pp. 3, 10-11). Order-size distributions are
assumed stationary and condition-independent, which the authors flag
as "quite strong" with queue-reactiveness deferred to future work
(PDF p. 4). The market-impact study is simulator output checked
against qualitative empirical shapes, not a measurement of real
impact; its TWAP/child-order machinery is execution-strategy
engineering and is not programme input. All quantitative results are
NASDAQ equities, one exchange, one year; nothing here licenses a
cross-market claim.
