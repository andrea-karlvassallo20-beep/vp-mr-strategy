# Deep-read session 89 — Arbitrage Analysis in Polymarket NBA Markets (Cheng, Yang and Zou, 2026)

**Library deep-read session 89 (null-time session 99, second of the score-21
tier).** Guang Cheng, Jiaxin Yang and Haoxuan Zou (UCLA), "Arbitrage Analysis
in Polymarket NBA Markets", arXiv:2605.00864v1 [q-fin.TR] (index year 2026;
v1 dated May 5, 2026, submission stamp 22 Apr 2026). One clause on what the
paper is: an empirical limits-to-arbitrage study of a decentralized
prediction-market CLOB quantifying how rare executable single-market
mispricings are and how shallow the extraction ceiling of combinatorial
dislocations is, from 75 million polled top-of-book snapshots across 173
NBA games in one month, with the join of the two asynchronous books carried
by an explicit synchronization-and-imputation pipeline.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x1b6841_arbitrage_analysis_in_polymarket_nba_markets.txt,
~12 pp., page-marked). Next UNREAD triage-rank entry (score 21).

## The paper in one paragraph

Two arbitrage classes are quantified on Polymarket NBA markets (Feb 4 to
Mar 4, 2026; 173 games; 3,042 markets; 75,088,497 limit-order-book
snapshots polled off the CLOB GET /book endpoint at a 3.6 to 5.5 s cycle
per market, Level-1 top-of-book only, deduplicated against the mirrored
order book by cryptographic-hash change detection; PDF pp. 1, 3-4, appendix
A). Single-market arbitrage (Buy path AskA+AskB < 1.00, or mint-and-sell
BidA+BidB > 1.00 on fully collateralized complementary tokens; PDF p. 4)
yields 37 theoretical episodes of which 30 (81.1%) are post-game stale-quote
artifacts where market makers have withdrawn and the median bid-ask spread
has exploded to 7,532.65 bps (PDF pp. 4-5), leaving 7 valid in-game episodes,
median duration 3.6 s, aggregate profit $210.19 capped at a $100-per-episode
one-shot deployment, $4,418.44 uncapped (PDF pp. 4-6). Combinatorial
arbitrage between the Moneyline and Spread of the same game (the spread is
a strict subset of the moneyline, so the pair Ask(ML_A) + Ask(Sp_B) < 1.00
is risk-free with a $2.00 "Middle" jackpot if the final margin falls inside
the gap; PDF pp. 6-7), on 8.59 million unified states joined by a Unified
State Machine with strict forward-fill imputation (appendix B, PDF p. 12),
yields 523 candidates, 233 post-game exclusions, 290 active episodes
concentrated in the final minutes of live play (in-game time-in-arbitrage
0.1762%), median duration 16 s, median yield 101.01 bps, capped profit
$559.59 vs uncapped $2,032.75, with 76.9% of episodes unable to deploy even
$100, averaging 14.79 executable shares; and the Middle jackpot is
realized in zero of the episodes (PDF pp. 7-9). The authors read the whole
pattern as the Shleifer-Vishny limits-to-arbitrage mechanism: risk-free
extraction exists but is structurally confined to retail scale by book
depth (PDF pp. 8-9); the polling cadence makes frequencies lower bounds and
durations upper bounds (PDF pp. 3-4, 9-10); and the mirrored book makes
every crossed signal appear simultaneously Long and Short, so naive summing
doubles apparent profitability until strict deduplication (PDF pp. 3-4),
while staggered 2 to 50 ms serialization of complementary tokens plus
naive state projection registers sub-second phantom arbitrage that only a
500 ms coeval-clustering rule kills (appendix A.2, PDF p. 10).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The cross-stream
   synchronization and single-source-count pre-declaration. The paper
   proves in print that the join of two asynchronously updated streams is a
   free degree of freedom that manufactures phantom structure mechanically,
   and that one shared underlying state can be observed through two views so
   that any crossed signal counts twice: the complementary tokens serialize
   2 to 50 ms apart in the CLOB API, so naively projecting the last-known
   state forward momentarily crosses the new price of one outcome against
   the stale price of its complement, registering sub-second phantom
   arbitrage that the pipeline kills only by a dynamic 500 ms time-based
   clustering rule treating same-batch updates as simultaneous (appendix
   A.2, PDF p. 10); the mirrored book means one shared liquidity pool is
   queried through two reflected order books, so every severe mispricing
   where AskA+AskB < 1.00 automatically manifests as a crossed book where
   BidA+BidB > 1.00, and naively summing the Long and Short signals would
   "falsely double the executable profitability" (PDF pp. 3-4, dedup
   enforced); and the combinatorial leg is evaluated on a Unified State
   Machine merging the two markets' asynchronous update timestamps with
   a strict forward-fill imputation chosen precisely so that only states
   verifiably resting at the evaluation instant are used (appendix B,
   PDF p. 12). Proposal: BEFORE the L0 gate, any C1-L2/C8-adjacent
   computation, comparator, null, baseline or feature that joins two or
   more asynchronously updated data streams (two legs of one book viewed
   separately, two markets, a book feed plus an event or macro timeline,
   the living board plus its klines) must pre-declare, as frozen
   configuration counted in the multiplicity ledger: (i) the merge
   timeline (a declared clock or the union of the streams' update
   timestamps), (ii) the imputation convention (strictly last-known-value
   carried forward, evaluation points using only states verifiably
   resting/available at that instant, never look-ahead), (iii) a
   desync-coeval tolerance with which near-simultaneous staggered updates
   are treated as simultaneous, recorded together with the claimed
   structure's insensitivity to that tolerance (or reported across a
   pre-declared tolerance grid), and (iv) a source-overlap map proving no
   single underlying state is counted through two views (mirrored books,
   complementary tokens, one pool under two labels; double-counting
   inadmissible). Harder-to-pass because a join-established association
   that survives only under its own post-hoc tolerance, imputation or
   dedup rule, or that counts one state twice, now fails at the gate
   instead of surviving as a find. Tightens the same-period-aggregate
   feature availability rule (deep-read 84) by extending the availability
   discipline from aggregate-derived features to any cross-stream imputed
   state at the evaluation instant, and tightens the estimator-
   implementation concordance rule (deep-read 85) by extending the frozen-
   configuration class from one estimator's implementation-vs-definition
   to the join rule of multiple streams; the feature-normalization
   pre-declaration (deep-read 83) binds rolling normalization statistics
   and the estimator-configuration freeze (deep-read 63) binds kernel
   estimator auxiliaries, but none of the queued items binds the sync/
   imputation/tolerance/dedup rule of a stream join, which is exactly the
   degree of freedom the C8 macro-synthesis arms and the base-rate
   confrontation's pre-declared horizon bridge will exercise the moment
   the L2 gate opens. Queued at ## 118; the owner ratifies or kills it.

2. [reinforcing, no new item] Seven episodes in seventy-five million
   snapshots is the burden of proof stated as a base rate: even on a venue
   whose core invariant (complementary prices summing to $1.00 on fully
   collateralized tokens, PDF p. 2) hands every participant a free
   arbitrage detector, 81.1% of raw signals are terminal-state artifacts
   (30 of 37, PDF pp. 4-5) and the residual is 7 episodes, median 3.6 s,
   $210.19 aggregate capped profit in a month across 3,042 markets (PDF
   pp. 4-6). Nothing here moves any C1-L2 kill line (different venue,
   different engine, different grain), and no magnitude may enter the
   record (the laundering rule); what it reinforces is the programme's
   opening axiom that the default is no edge and that any dislocation
   claim must be confronted with exactly this kind of stated base rate
   before it is argued. No queue change.

3. [reinforcing, no new item] The jackpot's realized base rate is zero:
   the combinatorial structure carries a built-in doubling upside (the
   Middle jackpot, $2.00 payout, Table 5, PDF p. 7), and an ex-post
   resolution analysis of all candidate episodes found zero realizations
   in 290, leading the authors to state that algorithmic participants
   "cannot assign meaningful probability weight to this incremental upside
   in rigorous expected-value calculations" (PDF p. 8). This is the
   misses-curriculum discipline applied by the source itself: an
   attractive conditional payoff whose realized frequency over hundreds of
   opportunities is zero is a story, not an expectancy, and the sealed
   prediction ledger and the C1-L2 base-rate confrontation exist to make
   exactly this confrontation mandatory before any upside term is counted
   in the programme. No queue change.

4. [cost-survival ammunition] Executability is the binding constraint, and
   the paper's measurement discipline declares the assumptions a future
   K7-style cost-survival layer must carry: top-of-book only as "the most
   conservative, highly executable measure of available liquidity" with
   the argument that if the top of book fails the threshold deeper levels
   mathematically cannot (PDF pp. 3, 10); a $10 minimum executable size
   at the bottleneck leg to filter dust (PDF pp. 4, 11); a "One-Shot"
   evaluation paradigm because summing consecutive snapshots within an
   episode would assume regenerating liquidity and inflate returns
   (appendix A.5, PDF p. 11); and the finding that 76.9% of combinatorial
   episodes could not absorb a $100 deployment (average 14.79 synthetic
   shares), the capped/uncapped gap $559.59 vs $2,032.75 quantifying the
   divergence between theoretical dislocation and extractable value (PDF
   pp. 8-9). If the L2 phase ever records a dislocation's "value", the
   executable-depth ceiling, not the theoretical size, is the number a
   cost-survival layer prices; the paper supplies the receipt magnitudes
   as ammunition and nothing more. No queue change.

5. [interpretation caution] Every frequency and duration in the paper is
   a sampling artifact of its polling cadence, and the authors say so:
   3.6 to 5.5 s polling means episodes opening and closing inside one gap
   evade detection entirely (frequencies are conservative lower bounds),
   a forward-looking difference credits each detected snapshot with the
   gap to the next (durations are structural upper-bound estimates, not
   exact lifespans), and phase-specific trust ceilings (300 s in-game,
   1800 s pre/post) cap credited durations against outages (PDF pp. 3-4,
   9-10, 11). Any future persistence, duration or episode-count statistic
   on the L2 data must pre-declare its sampling cadence and outage caps
   and must be reported as a bounded measurement with both bias
   directions named, never as an exact rate; the flow-clock scale-
   constant and estimator-freeze families already carry the same
   declaration logic for clocks. No queue change.

6. [interpretation caution] Terminal-state liquidity must be censored by
   pre-declared rule or it manufactures phantom crossings: the post-game
   phase between physical conclusion and oracle resolution sees market
   makers withdraw quotes, the median spread exploding to 7,532.65 bps,
   and stale crossing orders dominate the raw signal set until excluded
   by an explicit phase rule (30 of 37 single-market signals and 233 of
   523 combinatorial candidates are these artifacts; PDF pp. 4-5, 7,
   10-11). The regime-window pre-declaration (deep-read 53) and the macro
   timeline censoring discipline already bind the programme's proximity
   treatment of windows near boundaries; nothing this paper shows
   licenses extending them, but it reinforces why censoring rules are
   frozen before the data and applied by phase, never by post-hoc
   inspection of what the data shows. No queue change.

7. [source-quality note] Preprint arXiv:2605.00864v1, three UCLA authors
   with a named corresponding professor, zero citations recorded at
   cataloguing, no peer-reviewed venue recorded; one month of data on a
   single venue class (Polymarket NBA, a zero-fee venue, PDF p. 10) at
   polled Level-1 snapshots, not full-depth L2, so gross-of-fee
   magnitudes are not transferable to fee-bearing venues and sub-3.6 s
   structure is invisible by construction; the descriptive tables carry
   precise-looking aggregates whose derivations rest on an unspecified
   outlier game (the single-game blowout driving the $210.19 headline
   capped profit, PDF p. 5); and the paper's own limitations section
   declares exactly both bounds honestly (PDF p. 9). An honest
   descriptive microstructure study at preprint grade; read, graded,
   recorded at its grade, consistent with score-21 tier placement.

## What this paper would have killed if we had done it wrong

If the programme had ever joined two asynchronously updated streams
without a pre-declared merge, imputation, tolerance and dedup rule, the
phantom class this paper proves mechanically would have been available for
free: a C8 macro-synthesis arm joining the market series to wall-clock
boundaries around a macro event, a board-plus-klines bridge in the
sealed-ledger machinery, or a cross-leg book computation would each have
carried an undeclared sync tolerance, and a tolerance or imputation rule
selected after seeing the result could have manufactured the first apparent
cross-window co-movement of the programme's record precisely where the
hypothesis most wants to find it. The counterfactual kill is not
hypothetical arithmetic: the paper registers sub-second phantom arbitrage
from a 2 to 50 ms stagger alone until a 500 ms clustering rule is imposed
(appendix A.2, PDF p. 10) and doubles apparent profitability through the
mirrored book until dedup is enforced (PDF pp. 3-4), which are the exact
shapes an undeclared join would produce on the L0-audited data the moment
it arrives. The programme avoided the kill only because its frozen-
configuration families (estimator-config freeze, normalization
pre-declaration, availability rule, concordance rule) already force
declaration of every other preprocessing degree of freedom; this read
adds the one axis none of them covered, the stream join itself, and only
the owner's ratification arms it. Had the session instead read this paper
as market evidence, the kill would have run the other way: a
"venues-are-efficient" or "venues-are-inefficient" prior lifted from
the abstract would have entered the record as ammunition laundering,
exactly what the standing caveat forbids.

## Standing caveat

The venue is not the programme's target market and never can be cited as
one: Polymarket NBA markets are fully collateralized binary token pairs on
one shared mirrored liquidity pool (PDF pp. 2-3), off-chain matched on
Polygon, explicit zero fees during the sample (PDF p. 10), contracts
resolving within hours, with retail-scale flow dominance and structural
isolation between related markets (PDF p. 3). All magnitudes, rates and
durations are venue-, sample- (Feb 4 to Mar 4, 2026) and grain-specific
(3.6 to 5.5 s polled Level-1 only; frequencies lower-bounded, durations
upper-bounded, PDF pp. 3-4, 9-10) and transfer nowhere without
re-derivation; the combinatorial leg exists only because of a subset
structure between moneyline and spread contracts that has no analogue in
a single-asset futures book; the figures are images in the source PDF, so
numeric evidence here is taken from the tables and text only; and the
extract's pagination runs 12 pages with appendices A-B complete. arXiv
v1: the paper may be revised or published; check for a later version
before any formal citation. Nothing in the paper licenses any trading
behaviour, and the zero-fee venue arithmetic in particular is not
operationalizable on any fee-bearing venue the programme will ever touch.
