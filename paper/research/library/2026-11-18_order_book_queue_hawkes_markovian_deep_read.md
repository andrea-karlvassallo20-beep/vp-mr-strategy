# Deep-read session 32 — Protter, Wu and Yang, "Order Book Queue Hawkes-Markovian Modeling"

Library deep-read session 32 (null-time session 36, log entry
## 40). Philip Protter (Department of Statistics, Columbia
University), Qianfan Wu (Kelley School of Business, Indiana
University Bloomington) and Shihao Yang (H. Milton Stewart School
of Industrial and Systems Engineering, Georgia Institute of
Technology), arXiv:2107.09629v3 [q-fin.TR], v3 stamped 5 January
2022, 71 pp. text extract, page-marked. Read 2026-11-18, against
ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/xce0ba3_order_book_queue_hawkes_markovian_modeling.txt).
Assigned triage-rank entry (score 31, xce0ba3). Next UNREAD
triage-rank entry (score 31, xe7dc7f, "TradeFM: A Generative
Foundation Model for Trade-flow and Market Microstructure").

## The paper in one paragraph

A level-K (K = 3, 24 event types) limit-order-book event taxonomy
in the Queue-Reactive lineage: trades, insertions and
cancellations at each of K queues per side, plus six
reference-price-change events grouped by cause (trade, full
cancellation, spread-crossing insertion) and direction (PDF
pp. 7-10). The event process is a multivariate Hawkes whose
baseline intensities are made Markovian: the baseline is a step
function of the current liquidity state (queue size at the
associated level, or the bid-ask spread for the two
spread-crossing event types, in ten buckets) plus a 126-category
intraday time factor, finer at the open and close (PDF
pp. 10-13). Estimation is Kirchner's non-parametric binned
autoregression, extended from constant to varying baseline, with
bin-size 0.25 seconds, support 20 seconds, LASSO applied to the
excitement-function coefficients only, and AIC model selection
across seven nested specifications (PDF pp. 13-22). On 20 trading
days of LOBSTER-reconstructed NASDAQ ITCH data for Apple, January
2019 (PDF pp. 22-23), the paper reports: most estimated
excitement functions decay exponentially with trailing zeros,
but non-exponential shapes appear for higher-level trade events
that arrive in wide-spread states (PDF pp. 25-27); the
first-level insertion and cancellation kernels are similar in
shape, a similarity that fades at levels 2-3, read as participants
sequencing insertions and deletions at the touch, which is less
risky than acting at deeper levels (PDF pp. 25-26, 44-45);
arrival intensity increases with the liquidity state for
first-level trades, cancellations and insertions but decreases
for level-2 and level-3 insertions, read as incremental
queue-fill risk deterring deeper passive posts (PDF pp. 27-28);
and a U-shaped intraday intensity with a sharp elevation 15:55 to
16:00, read as algorithmic execution and exchange end-of-day
policies (PDF pp. 28-29). Qualitative conclusions survive
ignoring order sizes, dropping LASSO and doubling the bin size
(PDF pp. 30, 48-69), and in-sample AIC ranks the Hawkes part
above the state parts, with every part adding on top of the rest
on all 20 days for the liquidity-state and time-factor additions
(Table 1, PDF pp. 31-32).

## Findings, graded

NO kill line changed. ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION.

1. **[candidate sharpening, PENDING OWNER RATIFICATION]** The
   queue-label convention declaration component for the
   queue-state conditioning rule queued through deep-read session
   26, corroborated session 27, and already extended by the
   anticipation disclosure component joined at deep-read session
   31 (all still PENDING OWNER RATIFICATION), covering
   passive-flow features in the C1-L2 L2 arm. Mechanism,
   page-cited: the entire event taxonomy and every liquidity
   state in this model are defined relative to a reference price
   that must lie strictly between best bid and best ask, and all
   queue indices are counts of ticks from that reference (PDF
   pp. 5-7, 12-13). The convention is not innocuous: when the
   spread is an even number of ticks the midpoint lands exactly
   on a valid price position, so the reference must be displaced
   by plus or minus half a tick, resolved toward whichever side is
   closer to the previous reference value (Supplementary A, PDF
   pp. 38-39). The displaced convention silently reassigns which
   price level counts as the first ask, the first bid, and every
   deeper-level label, so two implementations of the same
   declared conditioning functional can read different conditioning
   states from the same book, and the divergence concentrates in
   the wide-spread states where conditioning carries its
   information: the fitted state effects differentiate there
   (PDF pp. 27-28) and the non-exponential kernel shapes
   concentrate there (PDF pp. 26-27). On the programme's own venue and fields the
   ambiguity is routine, not exotic: with BTCUSDT tick sizes and a
   five-to-six-figure price, any even-tick spread puts the quoted
   mid on the valid price grid, so the tie-break fires whenever a
   queue-state functional anchors to the mid or a reference
   rather than to the event's own touch. Consequence for the
   queued rule, harder to pass: a queue-state-conditioned passive
   feature can satisfy the conditioning declaration (it declared
   "the pre-event volume at the touched level, or the declared
   alternative") while its conditioning state still depends on
   an undeclared labeling convention, an undisclosed degree of
   freedom that survives every admissibility gate and invites
   post-hoc selection among equally "declared" implementations.
   One pre-declaration. Queue-label convention declaration:
   whenever a queue-state conditioning functional is defined
   relative to a reference price or mid rather than to the event's
   own touch, the pre-registration must declare, recorded on TRAIN
   before L2 data arrives, the reference construction and the
   even-grid tie-break rule (previous-reference anchoring or the
   declared alternative), the level-indexing origin, and the
   touched-level identification rule; readings with undeclared
   conventions are inadmissible. Functionals anchored entirely to
   the event's own touch on a feed-native price field satisfy the
   declaration trivially, and if it later holds that every
   admissible functional on the programme's venue and fields is
   event-touch-anchored, the component guards nothing on that
   route and stays dormant there. Scope: the pending
   queue-state conditioning rule's declaration block only, as a
   disclosure requirement; the C1-L2 spec, its kill lines, T-H
   and T-O, and every amendment remain untouched; no threshold
   moves; nothing is armed.

2. **[reinforcing, no new item]** Queue-state conditioning is not
   redundant with flow excitation, and the state effects are
   event-type-specific. The liquidity state and time factor add
   explanatory power on top of the Hawkes part on all 20 days
   (Model 6 minus Model 4, median per-sample AIC difference
   -0.23, 20 of 20 days, Table 1, PDF pp. 31-32), and the fitted
   state effects run in opposite directions by event type:
   arrival intensity rises with the current queue size for
   first-level trades, cancellations and insertions but falls for
   second- and third-level insertions (PDF pp. 27-28, Figures 8,
   S3-S4). A second corpus-level corroboration of the queued
   queue-state conditioning rule's premise, that state-blind
   passive aggregates are inadmissible: state matters, and the
   direction depends on which queue the event acts on, so the
   conditioning functional must be declared rather than
   defaulted. No parameter transfers.

3. **[reinforcing, no new item]** The accumulation dichotomy is a
   named sibling of the event-grain OFI accumulation rule (deep-read
   session 25). Regular (non-reference-price-changing) events are
   additive, so order sizes are summed into the binned counts,
   while the six reference-price-changing events are treated as
   pure points because they shift the queue distribution and
   cannot be decomposed into same-event smaller sizes (PDF p. 16).
   The sensitivity disclosure matches what the event-grain
   discipline demands: accumulation choices declared before
   results, the alternative convention (order size ignored, all orders of
   size 1) run after, the difference disclosed in level and
   smoothness, and the qualitative conclusions shown to survive
   (PDF pp. 48-49, 55; Table S1, PDF p. 69). No threshold
   transfers.

4. **[interpretation caution]** Exponential-kernel assumptions are
   visibly wrong for a class of events, so kernel form is a
   declared convention, never a discovered truth. Most estimated
   excitement functions decay exponentially with trailing zeros,
   agreeing with the exponential-kernel literature, but
   non-exponential shapes recur for higher-level trade events
   (second and third best price, arriving when the spread is
   large), with the authors stating it may be problematic to
   adopt the exponential shape assumption for stimulating
   functions across all events (PDF pp. 26-27, Figures 6-7;
   Figure S2, PDF p. 46). Any excitation-decay or Hawkes-family
   reading in a C1-L2 or C8 arm carries its kernel-form
   declaration as an assumption, and the paper's fitted shapes
   are never cited as the expected shape on any market the
   programme measures.

5. **[interpretation caution]** Every "explanatory power" claim in
   the paper is in-sample AIC comparison on one stock in one
   month, and the paper never claims more. The decisive AIC
   differences are minuscule per-sample numbers (median -0.58 for
   Hawkes over the state parts, -0.23 and -0.08 for the additions
   of the state parts and LASSO on top, Table 1, PDF p. 32); no
   out-of-sample, forecasting, or goodness-of-fit beyond AIC
   appears anywhere; stationarity and ergodicity are explicitly
   left to future research (PDF p. 34). Applied to the record: a
   fitted AIC improvement is bookkeeping, not an edge, and the
   paper is never citable as evidence that any programme feature
   carries information. The AIC bookkeeping itself counts only
   effective parameters and drops empty buckets from the degrees
   of freedom (PDF pp. 21-22), a discipline worth naming as a
   sibling for any future model-selection bookkeeping, not an
   import.

6. **[reinforcing, no new item]** Intraday time clustering
   corroborates the C1-L2 spec's hour-of-day strata. Arrival
   intensities elevate in the first and last 30 minutes, with a
   sharp increase 15:55 to 16:00 attributed by the authors to
   algorithmic execution rules and exchange end-of-day policies
   (PDF pp. 11-12, 28-29, Figure 9). The spec's declared
   hour-of-day stratification already carries time clustering as
   a confounder to condition on; this is a second corpus for
   keeping it. The paper's bucketing choices (126 categories)
   never transfer.

7. **[source-quality note]** Three authors, with Philip Protter a
   leading stochastic-process authority (Columbia Statistics), and
   the modelling squarely in the Queue-Reactive lineage of Huang,
   Lehalle and Rosenbaum and Morariu-Patrichi and Pakkanen,
   already deep-read at session 28 (the record's sibling note on
   state-dependent Hawkes LOB modelling); arXiv v3 stamped January
   2022, about four years old at reading; no journal record
   checked at reading. The scope is deliberately modest and
   honestly disclosed: one stock (Apple), one month (January
   2019), 20 trading days, LOBSTER-reconstructed NASDAQ ITCH
   data, level-3 book, regular hours only, bin-size 0.25
   seconds, support 20 seconds, LASSO parameter 0.0005 (PDF
   pp. 22-23, 30, 33-34), with stationarity deferred and no
   out-of-sample claim made. Published version to be checked
   before any formal citation. Triage score 31 is an access-value
   rank, not a promise; the paper is a solid, narrow,
   descriptive modelling paper and is graded exactly at that
   level.

## What this paper would have killed if we had done it wrong

If the programme had adopted a Hawkes-excitation feature on
queue-state-conditioned book data without this paper's taxonomy
lesson, it could have silently built a conditioning state whose
queue labels are convention-dependent: the same declared
functional, "the pre-event volume at the touched level or the
declared alternative", reads different states from the same book
whenever the mid sits on the valid price grid, and the divergence
concentrates in wide-spread states, exactly where the state
effects differentiate and where non-exponential excitation
lives. The error is invisible to every within-measurement check:
conservation identities pass, the conditioning declaration reads
as satisfied, and the sign guard sees a well-formed feature. It is
foreclosed only by declaring the labeling convention before the
data arrives, which is what the queued component requires. The
existing discipline that already caught the adjacent halves of
this failure mode: the event-grain rule for accumulation choices,
the anticipation disclosure for forward-looking content, and
this component for labeling conventions.

## Standing caveat

One stock, one month, one venue (NASDAQ through LOBSTER ITCH
reconstruction), level-3 book, regular hours, penny-tick US
equities microstructure with a five-figure nominal price and
dollar-denominated queues; no crypto, no BTCUSDT, no futures, no
anonymous flow. All fitted shapes, liquidity-bucket boundaries
(ten categories at 100-share intervals), time categories (126),
bin size, support length and LASSO parameter are dataset- and
venue-specific, and every explanatory-power claim is an in-sample
per-sample AIC difference. Laundering directions named. INTO —
the queue-label convention mechanism, the event-type-specific
state-direction contrast, the accumulation dichotomy and the
time-clustering corroboration enter only as feature-design
discipline (the sharpening and cautions above); no kernel shape,
bucket boundary, bin size, support length, regularization
parameter, intensity level, AIC figure or end-of-day spike
enters any spec, default or calibration. OUT — the fitted kernel
shapes, the liquidity-state curves, the time-factor profile and
the AIC rankings are never cited as expected behavior of any
market the programme measures, never as expected BTCUSDT book
behavior, and never as evidence that any programme feature
carries information.
