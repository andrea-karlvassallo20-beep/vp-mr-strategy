# Deep-read session 31 — Barone and Lillo, "Trading in the Sunshine or in the Shade: Market Impact and Adverse Selection on Hyperliquid"

Library deep-read session 31 (null-time session 35, log entry ## 39).
Davide Barone and Fabrizio Lillo (Scuola Normale Superiore, Pisa),
arXiv:2606.15715v1 [q-fin.TR], 14 June 2026, 31 pp. text extract,
page-marked. Read 2026-11-18, against ONE question: what here would
kill C1-L2 or C8 faster, or change their kill lines? Source: legally
acquired OA copy
(docs/library/text/xa74970_trading_in_the_sunshine_or_in_the_shade_market_imp.txt).
Assigned triage-rank entry (score 32, xa74970). Next UNREAD
triage-rank entry (score 31, xce0ba3, "Order Book Queue
Hawkes-Markovian Modeling").

## The paper in one paragraph

Hyperliquid, a fully on-chain central limit order book for
cryptocurrency perpetual futures, offers a protocol-native TWAP
mechanism whose parent-order parameters are publicly visible from
inception, a natural form of sunshine trading. Using address-level
data covering all 201 perpetual markets from 28 July 2025 to
23 March 2026 (more than 641 million fills, about USD 1.93 trillion
notional), the authors reconstruct about 4.3 million hidden
statistical metaorders from same-address same-sign trade sequences
(30-minute inter-arrival splitting rule, at least 10 child orders)
and compare them with about 465,000 visible native TWAPs
(PDF pp. 4-6). Hidden metaorders execute U-shaped, front-loaded
schedules with double-inflection price trajectories and pronounced
post-completion decay, consistent with transient-impact optimal
execution, while TWAPs trade nearly uniformly and track a smooth
concave path (PDF pp. 10-12, Appendix A). Against the Admati and
Pfleiderer (1991) preannouncement predictions: visible TWAPs face
about 9 basis points lower temporary impact than comparable hidden
metaorders on the common support of participation and volume-time
duration (the order-level gap holds at about 8.7 to 8.9 basis
points with market, hour, and day fixed effects, and survives
controlling for the signed pre-start return, PDF pp. 13-16); they
leave about 5 basis points less permanent post-execution
displacement (Table 2, PDF p. 18); hidden metaorders executed in
the direction of already-visible same-side TWAP flow pay higher
permanent costs, about 0.84 to 0.92 basis points per 10 percentage
points of visible same-side dominance, and about 6 basis points
survive controlling for the overlapping flow's own price pressure
(Table 3, PDF pp. 19-20); and during active TWAP windows the
displayed book tilts toward the absorbing side, displayed depth
within five spreads of the mid rises, and fixed-notional sweep
costs fall, while the quoted spread widens, all with no favorable
pre-trend and scaling with announced size (Figure 7, PDF pp. 22-23;
Table 4, PDF pp. 24-25). The comparative static that the announcer
discount should widen with market-wide adverse selection is tested
and honestly reported as a null, reframed as the mechanism being
conditional and event-level rather than market-wide (PDF p. 21).

## Findings, graded

NO kill line changed. ONE new candidate sharpening queued, PENDING
OWNER RATIFICATION.

1. **[candidate sharpening, PENDING OWNER RATIFICATION]** The
   queue-state anticipation disclosure component for the
   queue-state conditioning rule queued through deep-read session 26
   and independently corroborated through deep-read session 27
   (both still PENDING OWNER RATIFICATION),
   covering passive-flow features in the C1-L2 L2 arm. Mechanism,
   page-cited: the displayed book state is not exogenous scaffold,
   it is an elastic response to flow information, including
   anticipated flow. During active visible TWAP programs the
   oriented imbalance within five quoted spreads of the mid jumps
   at the start of the execution window and persists to completion,
   displayed depth rises by about 4,182 USD in the same band, and
   the 10,000 USD sweep cost falls, while the touch widens:
   suppliers rest additional size behind the touch at prices that
   compensate inventory risk rather than quoting more aggressively
   at the best quotes (Figure 7, PDF pp. 22-23; Table 4,
   PDF p. 25). These responses are not pre-trends: the pre-window
   leads for imbalance, depth, and sweep cost are economically
   negligible, and the size interaction shows the imbalance and
   depth responses scale with announced notional (PDF p. 25). The
   same tilt appears gradually around hidden statistical
   metaorders as they become progressively inferable from
   same-address, same-direction trading, rising more persistently
   for longer programs, which the authors read as market makers
   learning a directional program is underway even without
   announcement (PDF pp. 22-23), and they state in the limitations
   that the book response may reflect participants learning from
   repeated address-level trades (PDF p. 26). Consequence for the
   queued rule, harder to pass: a passive-flow feature conditioned
   on queue state is conditioning on a state variable that may
   partially encode anticipated or in-progress flow programs, so
   what is sold as contemporaneous book-state conditioning can
   embed forward-looking flow information, dangerously close to
   conditioning on what the evidence stage is supposed to measure
   rather than scaffold it, the costume failure K1 exists to catch.
   Two pre-declarations. (a) Anticipation-content declaration:
   every queue-state-conditioned passive feature reading in the
   C1-L2 L2 arm must be accompanied, recorded on TRAIN, by a
   declaration of which flow programs the declared state variable
   can respond to on the programme's actual venue and fields
   (visible or protocol-announced flow, and statistically learnable
   from public flow either way), with the declaration made before
   the L2 data arrives. (b) Pre-window lead bound: the conditioning
   state's measured lead against placebo windows must be reported
   with the feature reading on TRAIN, so anticipation-encoding is
   bounded rather than assumed away; a state variable whose lead is
   indistinguishable from placebo carries no anticipation content
   and the disclosure closes, while a state with positive lead must
   be declared as partially anticipatory or replaced. Scope: the
   C1-L2 L2 arm's queue-state-conditioned passive features only,
   as a disclosure requirement on top of the queued conditioning
   rule; C1-L2's spec, its kill lines, and every amendment remain
   untouched; no threshold moves, T-H and T-O untouched; nothing
   is armed.

2. **[reinforcing, no new item]** Pre-trend and placebo discipline
   at the source. The book-response claims are carried by an
   event-time placebo design with event fixed effects, relative-
   minute fixed effects, and a treatment indicator that switches
   on only during the active window (Eq. (10), PDF p. 24), then
   probed with a pre-window lead (Eq. (11)) and a size interaction
   (Eq. (12), PDF p. 24; Table 4, PDF p. 25). The decisive honesty
   move: the relative spread's pre-window lead (+0.21 basis
   points) is of the same order as its active-window coefficient
   (+0.28), and the authors read the lead as selection into
   wider-spread states rather than as a response to TWAP
   visibility, cross-checked against the level behavior of
   statistical metaorders (+0.16 lead, +0.05 start) (PDF p. 25).
   Mechanism-level corroboration of the A3 family's placebo
   discipline already queued through deep-read session 28: without
   the lead test, the spread result would have been misattributed
   to visibility. No parameter transfers.

3. **[reinforcing, no new item]** Metaorder reconstruction with
   declared thresholds and quantified removal. Same-address
   same-sign trade sequences grouped under a 30-minute inter-
   arrival splitting rule, a stricter at-least-10-children
   threshold explicitly chosen to reduce false positives from
   coincidental clustering (native TWAPs at least 5 children,
   because protocol identification is unambiguous), a 24-hour
   completion cap with the removal quantified as immaterial
   (28,904 orders, 0.7 percent by count, 1.5 percent of notional)
   (PDF pp. 5-6). A named sibling of the record's event-grain
   discipline: thresholds declared before results, exclusions
   quantified after. No threshold or rule transfers.

4. **[interpretation caution]** Taker-print reconstruction
   misclassifies aggressive liquidity providers as metaorder
   executioners, and the record's own venue makes this failure
   mode live. In the reconstructed population, 46.2 percent of
   metaorders with at least ten children have at least one
   same-address maker fill during the execution window and 40.3
   percent a same-direction maker fill; the contamination is
   concentrated in the top 40 passive-volume addresses, which
   hold about 68 percent of same-address and 65 percent of
   same-direction passive volume and display both-side maker
   fills consistent with market-making; excluding them drops the
   same-direction maker-fill rate to about 31 percent (PDF p. 26,
   limitation 1). The programme's standing constraint that
   aggTrades is taker prints only means exactly this contamination
   class is unavoidable in any future metaorder-style aggregation
   on the programme's tape: aggressive market makers crossing the
   spread repeatedly in one direction are statistically
   indistinguishable from execution programs using taker data
   alone. Never cited as a solved problem; it is a bound on what
   taker-only aggregation can classify.

5. **[interpretation caution]** The comparison is an observational
   equilibrium comparison between execution regimes, not a
   randomized treatment of visibility, and the authors say so;
   self-selection is carried by trader identity. A taker-identity
   prior predicts the TWAP-versus-statistical choice almost
   perfectly (AUC 0.998, against 0.685 adding pre-start book
   state to a pair-only model at 0.674), the between-taker share
   of the mechanism-choice variation is about 0.93, 86.6 percent
   of orders come from addresses using one mechanism exclusively,
   and sub-account aggregation to master accounts (99.7 percent of
   volume mapped) changes essentially nothing: mechanism
   segregation is a property of entities (PDF pp. 13, 26). So the
   9-basis-point announcer discount is a property of who chooses
   TWAP as much as of visibility itself, and the paper is never
   cited as a causal estimate of the effect of transparency.
   Adjacent honest null worth recording against misreading:
   market state barely predicts native TWAP starts (PR-AUC 0.0053
   against a pair-hour climatology at 0.0033, versus 0.094 to
   0.142 for statistical-metaorder starts), so this paper does
   not show the book forecasting program arrivals (PDF p. 26).

6. **[cost-survival ammunition]** No impact exponent is a stable
   venue constant; execution regime moves both the level and the
   elasticities. Native TWAP temporary impact is a clean power law
   with exponent 0.303, well below the square-root benchmark;
   statistical metaorders are not power-law at all, fitted by a
   saturating arctangent in log-log space with three curve
   crossings between the two regimes (PDF pp. 8-9). The pooled
   impact surface tilts toward volume-time duration (F elasticity
   about 0.31) over participation (eta elasticity about 0.12),
   contrasting with Zarinelli et al.'s both-near-one-half (PDF
   p. 9), and the two regimes' elasticities differ in shape: the
   participation slope is significant for latent metaorders and
   indistinguishable from zero for TWAPs (Table 1, PDF p. 16).
   Any cost model that assumes one universal impact law, or one
   exponent per venue, inherits regime-dependence it cannot see
   from prints alone. No exponent, elasticities, or basis-point
   figure transfers.

7. **[source-quality note]** Two authors, Scuola Normale Superiore
   Pisa, with Fabrizio Lillo a leading market-microstructure
   researcher; arXiv v1 stamped 14 June 2026, roughly four months
   old at reading; no journal record checked; a large and serious
   empirical effort: 641 million fills, USD 1.93 trillion notional,
   201 perpetual markets, about nine months of trades, with
   companion work on Hyperliquid order data cited (Albers,
   Cucuringu, Howison, Shestopaloff) and public data via
   Hydromancer's Reservoir (PDF pp. 4-5, p. 29). The order-book
   analysis rests on a shorter sample, one-minute snapshots, first
   20 levels, 15 December 2025 to 23 March 2026 only (PDF p. 5),
   so the book results cover about three months. The limitations
   section is exemplary: the misclassification diagnostic, the
   randomization caveat, the learnability of hidden programs, and
   the arrival-predictability null are all stated by the authors
   (PDF pp. 26-27). Extract page-marked and clean throughout.
   Published version to be checked before any formal citation.

## Killed if wrong

If the anticipation mechanism is later shown to be
announcement-specific, a Hyperliquid protocol artifact with no
analog where flow is not protocol-visible, the queued anticipation
disclosure component loses its mechanism and should die back to the
conditioning rule as it stands through deep-read sessions 26-27.
The transferable core of the mechanism is the learnable-flow part:
the book state responds to flow programs as they become inferable
from public tape, which is venue-independent. If that part also
fails to appear on the programme's venue and fields, the disclosure
guards a problem that does not exist and should die back.
Conversely, if queue-state-conditioned passive readings are ever
published without the anticipation-content declaration and the
pre-window lead bound, the conditioning state could quietly embed
forward-looking flow information into what is presented as
contemporaneous book-state conditioning, exactly the costume
failure K1 exists to catch, and the queued component is what
forecloses it.

## Standing caveat

One venue, Hyperliquid, a fully on-chain CLOB for perpetual futures
with visible addresses, a protocol-native TWAP, USDC margin, and a
median end-to-end latency of 0.2 seconds, an order of magnitude or
more slower than any centralized exchange (PDF p. 4); trades
28 July 2025 to 23 March 2026, book snapshots only 15 December 2025
onward at one-minute frequency and 20 levels; no Binance, no
BTCUSDT, no spot equities, no traditional market with anonymous
flow. All magnitudes are venue- and period-specific. Laundering
directions named. INTO: no coefficient, elasticity, exponent,
basis-point figure, threshold, dominance share, or normalization
choice (order-anchored 24-hour windows, Parkinson volatility, the
five-spread depth band) from this paper enters any spec, default,
or calibration, and the sunshine-trading framework is not adopted
anywhere without its own pre-registration. OUT: the 9-basis-point
announcer discount, the 5-basis-point permanent gap, the
0.84-0.92-basis-point mirror cost, the book-response magnitudes,
and the impact exponents are never cited as expected behavior of
any market the programme measures, never as expected BTCUSDT book
behavior, never as expected impact on any execution the programme
simulates, and the venue's latency and transparency properties are
never cited as comparable to the programme's venue.
