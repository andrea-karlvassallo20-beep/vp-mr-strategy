# The null-time programme — what gets done while the L2 environment is being built

Written 2026-11-16, after the math layer verification (math_verification_2026-11-16.md),
the C8 macro-synthesis draft, and the library expansion to 110 OA papers. The owner is
procuring Tardis full-depth L2 data and studying medicine; this document is the standing
answer to "what do we do with the time in between." It is a queue, not a wish list: every
item names what it feeds, whether it is blocked on L2, and how it would be judged.

## 1. The endpoint, restated

The programme's endpoint has not moved: **C1-L2** — does Layer-2 microstructure carry a
compression signal that daily bars could not see — tested behind the L0 gate, kill lines
armed, nothing re-tuned after the fact. Everything in null time either (a) makes the
C1-L2 test sharper when the data arrives, (b) accumulates evidence that does not need
L2 (the sealed-prediction record), or (c) keeps the public instrument honest. Nothing in
null time may touch the sealed C7 panel, fit anything to discovery data, or quietly
expand scope into new claims without pre-declared kill lines.

## 2. What the surprise ledger now does every night (done tonight)

The heat map's time half is now wired into the nightly `board_refresh.py` cycle
(`surprise_ledger.py` runs after the board rebuild). Every night the top-k primed
candidates per class on the LIVING board (mega_dormancy_table) are sealed — hash-chained,
append-only, feature vector frozen, no outcome fields — and every past-horizon entry is
resolved against the same cached klines. This is the cheapest evidence in the whole
programme: it costs nothing, needs no L2, and by the time the L2 environment is ready
there will be weeks of sealed-prediction-vs-reality pairs. The study (Spearman rho
between sealed score and realized 10-bar jump, per class) is descriptive, but it is the
only running falsification of the priming score's RANKING that exists. If after ~100
resolutions the rho is indistinguishable from zero, the priming score's ranking carries
no cross-sectional information at daily grain — that would be a named, dated death,
recorded in the ledger, and it would sharpen C1-L2's motivation (the signal, if any,
lives where daily scores cannot see it).

Honesty note sealed into the adapter: mega-board fields absent from the ledger schema
(evr_m, vol_ratio) are sealed as null, never invented; a primed candidate whose klines
cannot be found is not sealed at all — a score that cannot be resolved against data is
not a prediction.

## 3. The queue (prioritized, each item tagged)

### [null-time, ready now] T1: compression duration-dependence on the second aggTrades window
The owner's memo says run; the second window (2024-08-01 to 2025-02-28, 333,527,416
BTCUSDT aggTrades, 212/212 days, zero missing) was prepared precisely so T1 runs on a
regime the harness never saw during construction. The standing constraint is recorded:
aggTrades is taker prints only — the passive-withdrawal mechanism from the Tesla-day
anatomy is invisible, and no taker proxy may be substituted. T1's question
(duration-dependence of the compression clock) is taker-visible. This is the single
highest-value unblocked item; it needs only the owner's word, which the memo already
leaned toward.

### [null-time, ready now] The misses curriculum, quantified
The Tesla day proved a move can arrive unprimed. That is one anecdote; null time can make
it a base rate. On the cached full-universe klines: enumerate every ≥4-sigma day on the
board, look up the priming state the night before each, and build the honest 2x2 —
primed-vs-unprimed against moved-vs-silent. This measures the priming score's coverage
miss rate (moves that arrive without priming) and its false-alarm rate (priming that
resolves into nothing), descriptively, at daily grain. It feeds directly into what C1-L2
must beat: if daily-grain priming has near-zero coverage, the L2 phase is not refining a
working signal, it is looking for one that daily data provably cannot rank. Pre-declare
the descriptive protocol first; no directional claim, no kill line needed because
nothing is claimed — but the table itself becomes the reference the C1-L2 spec must
confront.

### [null-time, ready now] Library deep-read programme
110 legal-OA papers are downloaded and text-extracted. The null-time ritual: one paper
per session, read against ONE question — "what here would kill C1-L2 faster, or change
its kill lines?" — and the answer written into a dated note (paper/research/library/).
Priority order: (1) CKS 2014 and the deep-OFI line (the math layer was just verified
against them; the verification found a β-factor bug once — re-read for its siblings),
(2) Hawkes branching and excitation stability (the same β lesson), (3) VPIN and
order-flow toxicity (C5's neighborhood), (4) anything on passive-cancel/frozen-book
regimes (the 91.6-96.8% passive-cancel fraction on the replay days makes this the most
live mechanism the L2 data will see). A library is ammunition, not evidence — the
standing caveat binds; the read notes cite, they never launder.

### [null-time, ready now] Website honesty pass
The site is now 12 pages plus the heat map. The standing risk is drift: pages written at
different dates quietly disagree. A null-time pass: read every page against the claims
ledger and fix any sentence that states a claim whose status has moved (C7-30m's death
should be stated as a death everywhere it is mentioned; the compression family now has
three independent kills). The claims ledger is updated with every PR by rule — the prose
pages have no such rule, so they rot. This pass is the rot-remover.

### [needs L2, blocked] Everything behind the gate
C1-L2 itself, C5 (passive cancellation), C6, the macro-synthesis (C8 draft). The block is
solely Tardis full-depth data passing the L0 gate's 100-timestamp audit on every day.
Null time can do exactly one thing for these: keep the verification kit ready so the
data is audited the day it arrives (src/intake_audit.py asserts timestamp units on
arrival; src/verify_l2_gate.py is the gate). Nothing else should be pre-built — the
programme's discipline is that the test specification is frozen before the data, and it
already is.

### [owner-curated, standing] The macro timeline
data/macro_timeline.csv is curated by the owner; it is the regime context for every
censoring decision. Null time can extend it backward (the farther back the event
history, the more censoring windows later hazard work can use) — but every row is
hand-checked or it is worthless. Boring, valuable, endless.

## 4. Methodology review — what I would change about SMH itself, and what I would not

Would not change: falsification-first, kill lines before tests, dead mechanisms named,
the sealed panel, the refusal of WHICH WAY at daily grain. This spine is the asset; the
last month of the record (three independent deaths of the compression family, honestly
recorded) is what makes the programme credible rather than merely active.

Would change, in null time, without touching any claim:

1. **Sealed predictions over retrospective scans.** The clue scans rank; only the
   ledger's sealed-then-resolved record can say whether a ranking ever carried
   information. The nightly seal turns the whole descriptive program from a collection
   of candidate lists into a slow, accumulating measurement. Every future scan should
   ask: does this produce something sealable? If not, it is a tour, not an instrument.

2. **The base-rate discipline.** The programme is very good at finding candidates and
   very good at killing claims; it has been weak on stating base rates — of ~1,300
   series, how many are primed tonight (113), how many move, how many moves arrive
   unprimed. The misses curriculum (above) fixes this. A score without its base rate
   is a story; with it, it is a measurement.

3. **Prose rot as a named enemy.** The heat map once vanished from the site nav because
   nav rewrites used stale lists; prose pages state claim statuses that have since died.
   The fix is mechanical: any page that states a claim must cite the claims ledger, and
   the null-time pass re-verifies them. (The heat map/refresh wiring fixed in PR #126 is
   the same lesson: instruments that are not in the nightly cycle rot silently.)

4. **Reading with a question, not for coverage.** 110 papers is ammunition; the
   programme's edge has never been reading volume, it is reading adversarially — every
   paper interrogated for what would kill the next test faster. The read notes should
   be graded by whether they changed a kill line.

## 5. What was done in this session (so the queue starts from truth)

- `surprise_ledger.py`: `seal_from_mega()` — the living board is sealed into the
  hash-chained ledger (mega schema mapped honestly; absent fields sealed null;
  unresolvable candidates excluded). First mega-board snapshot sealed tonight:
  11 candidates.
- `board_refresh.py`: surprise_ledger.py added to the nightly cycle — seal, resolve,
  study, every night, from now on.
- Tests: 2 new (mega-schema mapping + resolution on mega-sealed entries;
  unresolvable-candidate exclusion), 11 green in the suite.
- This document.

The queue's order is the recommendation: T1 first (it is armed and the data is paid
for), the misses curriculum second (it is the base-rate spine), the library third (it
sharpens kill lines), the website pass fourth (it prevents rot). The owner decides; the
memo rule stands.


Landing structure note, added 2026-11-24 at the ## 141 landing with the owner's word, after the one-file transport wall: the log is split for transport, byte-preserved. The former single-file log held 997,904 characters (fnv-1a 3713757117 over UTF-16 code units, tail ## 141). Its verbatim slice [9509, 262004), entries ## 6 through ## 49, now lives at paper/research/nt_archive/nt_archive_006_049.md; its verbatim slice [262004, 515493), entries ## 50 through ## 84, at paper/research/nt_archive/nt_archive_050_084.md; its verbatim slice [515493, 769316), entries ## 85 through ## 116, at paper/research/nt_archive/nt_archive_085_116.md. This file keeps the byte range [0, 9509) verbatim above this note, the standing preamble ## 1 through ## 5, and the byte range [769316, 997904) verbatim below it, the live tail ## 117 through ## 141. New entries append to this file; the numbering continues unchanged; no other content in the record changed. Nothing measured, no kill line moved, nothing armed, nothing trades live.

## 117. Null-time session 99 (2026-11-22), first act: the eighth synthesis pass — the cadence recomputed from the edition-9 reset at ## 111 (deep-reads 84-88 landed at ## 112 through ## 116, the window CLOSED at five of five per the ## 116 closing pointer, which directed the pass run first), goal state rewritten as EDITION 10, the G2 brief-debt recomputed against the grown queue (briefs cover forty of forty-seven at pass time; items 41-47 owed); NO sharpening queued by the pass

Session-state note, per the goal-autonomy conductor protocol (edition 9,
## 111, ACTIVE at session start): the live main tail (through ## 116) and
docs/DECISIONS_PENDING.md were read first; the open-PR set was read (empty,
no race); the cadence check was recomputed from first principles against
the edition-9 reset at ## 111 — deep-read 84 landed ## 112, 85 landed
## 113, 86 landed ## 114, 87 landed ## 115, 88 landed ## 116: five of five,
the window CLOSED, and the ## 116 closing pointer records explicitly that
the next deep-read session MUST open with the eighth synthesis pass before
its read — so per the conductor protocol section 3 point 2, the ## 116
pointer's own instruction, and the ritual's director step, the pass runs
FIRST and this session's deep-read follows as ## 118. The declared work
choice is therefore the pass first, then the standing deep-read, matching
the recorded instruction.

Facts recomputed from the live record (main tail through ## 116 at pass
time):

- Phase 1 (Daily/AVFI): CLOSED and ARCHIVED by the Board's dated word
  2026-11-19; archived is NOT falsified; every kill line stays frozen;
  unchanged. Phase 2 (Crypto L2): ACTIVE, the Board's only active
  research front (C1-L2 → C8 → Convexity Sizing), blocked on the
  owner's data acquisition; the L0 dry run is unblocked. Unchanged.
- Library: eighty-eight deep-read notes on main's tip through deep-read
  session 88 (the 89th lands as this session's second act and counts);
  the ratification queue holds FORTY-SEVEN candidate sharpenings plus
  probe E1 at pass time (this session's second act may queue the next;
  see ## 118), zero armed; T1 armed awaiting the owner's word in its
  booked state (sign inverted); T2 tested-fail; the blocked list stays
  blocked.
- Deep-read queue pointer: the score-22 tier is CLOSED (## 110-## 115:
  x0fc07a ## 110, x0acf9d ## 112, x1a712b ## 113, x85b5e3 ## 114,
  x750e2f ## 115); the score-21 tier is OPEN (x532697, "Conservation
  Laws in a Limit Order Book", read ## 116); next UNREAD "Arbitrage
  Analysis in Polymarket NBA Markets" (Cheng-Yang-Zou, score 21,
  x1b6841), then "Collective synchronization and high frequency
  systemic instabilities in financial markets" (Calcagnile-Bormetti-
  Treccani-Marmi, score 21, x9921ac), last of the tier — recomputed by
  title-matching the score-sorted triage file against the live log tail
  and the library note listing this pass; x1b6841 is consumed as this
  session's second act (## 118) and #89 counts toward the edition-10
  cadence.
- Cadence: the edition-9 window is CLOSED at five of five; the cadence
  is RESET by this edition (next due at five or more deep-reads since
  edition 10; #89 lands as this session's second act immediately after
  this pass and counts, so the counter stands at ONE of five).

What the window since edition 9 (log entries ## 112 through ## 116)
taught this pass, stated as ranking evidence, nothing laundered: the five
landed deep-reads of the window (sessions 84-88) moved ZERO kill lines and
queued exactly THREE sharpenings (#45, the same-period-aggregate feature
availability rule, ## 112; #46, the estimator-implementation concordance
rule, ## 113; #47, the impact-viability pre-declaration for generative
nulls, ## 115) — all three frozen-configuration/pre-declaration
extensions of already-queued families, so the declining-yield expectation
named at editions 3-9 holds: the queue keeps being fed from the same
declare-before-the-data vein, not from any new mechanism class. The
window was clean of race collisions (the last logged concurrent-instance
events remain ## 98, ## 105 and ## 109), so the byte-gate discipline held
through five same-day landings; the truncation-and-collision
infrastructure gap nevertheless stays live on the strength of those three
logged events plus the write-side truncation class (## 75, ## 78, ## 94,
## 98). The window's honest scoring: five reads landing the same day
against a head now descending through score-21 territory is exactly the
declining-yield regime the editions have been recording; the queue's
growth (three, all same-family) is not evidence of rising discovery, and
no empirical claim from any paper in the window entered the record as
support for any programme claim.

Named gaps restated (this pass's product, zero status): the append-only
log's write-side ~64K truncation class (## 75, ## 78, ## 94, ## 98) still
has NO standing CI check enforcing byte-size monotonicity of the large
tracked files, and no session-side read-back verification helper for
large reads AND writes through the tooling path — the rising collision
history makes this the ranked infrastructure item; the weekly directorate
has still not sat — FORTY-SEVEN candidates plus probe E1 pending at pass
time (forty-eight after this session's second act, see ## 118), zero
armed, the G2 briefs cover the first forty queued items (through item
40), so briefs for items 41-47 (the noise-model pre-declaration ## 100;
the queue-jump-diffusion generative-null pre-declaration ## 107; the
residual-flow attribution null ## 108; the feature-normalization
pre-declaration ## 110; the same-period-aggregate feature availability
rule ## 112; the estimator-implementation concordance rule ## 113; the
impact-viability pre-declaration ## 115) plus any successor are owed
before the next sitting, and the G2 item-41 brief remains the
highest-leverage lawful non-deep-read work item; front 3 stays blocked on
codespace/data presence. GOALS.md status lines refreshed as operative
bookkeeping (the front 2 pointer and tier history, the front 4 cadence
note, the G2 count reconciliation to the post-session queue of
forty-eight); rankings and gates live in the protocol, never there.

NO sharpening queued by this act (the pass names gaps, it does not
amend); DECISIONS_PENDING.md is NOT touched BY THE PASS (this session's
second act queues the forty-eighth candidate and updates that file under
its own rule, see ## 118); the protocol file itself changes by this act
only as the edition rule allows (section 2 rewritten whole as EDITION 10
with this entry as the change record, an edition-10 note appended;
nothing else in the protocol moves); T1 stays armed awaiting the owner's
word; the queue FORTY-SEVEN plus probe E1 at pass time, zero armed.
Nothing measured, no kill line moved, nothing armed, nothing trades
live.

## 118. Null-time session 99 (2026-11-22), second act: library deep-read session 89 — the Cheng-Yang-Zou Polymarket NBA arbitrage read, second of the score-21 tier; the paper graded an honest limits-to-arbitrage empiricism whose magnitudes are all banned from the record under the laundering rule (venue-, sample- and polling-grain-specific, zero-fee venue), whose desync phantom-arbitrage and mirrored-book double-counting mechanics are banked as the evidence for ONE candidate sharpening (the cross-stream synchronization and single-source-count pre-declaration, #48), whose executable-depth bottleneck is recorded as cost-survival ammunition, and whose polling-bound frequencies and terminal-state censoring reinforce the standing base-rate and censoring disciplines; NO kill line moved; the ratification queue moves to forty-eight candidate sharpenings plus probe E1

Session-state note first (goal-autonomy protocol, ACTIVE; goal state edition
10, ## 117, installed as this session's first act): the live main tail (read
through ## 116 before the session's edits; the pass lands as this session's
first act ## 117 in the same push) and docs/DECISIONS_PENDING.md were read
(ratification line: forty-seven candidates plus probe E1 at session start,
zero armed); the cadence check was recomputed from first principles — the
edition-9 counter stood at FIVE of five after deep-read 88 (## 116), so per
the ## 116 closing pointer, the conductor protocol section 3 point 2 and the
ritual's director step the eighth synthesis pass ran FIRST (logged as
## 117, goal state rewritten as EDITION 10, queue recomputed at the pass),
and the deep-read follows as this session's second act. Verified against
live state before reading: the triage file score-sorted and recomputed
against the live library note listing (the score-22 tier CLOSED ## 110-##
115; the score-21 tier OPEN with x532697 read ## 116; the head x1b6841
verified note-less, extract present and page-marked; then x9921ac verified
note-less with extract present; the open-PR set read at session start:
empty, no race; the protocol file read whole and internally consistent).
This is deep-read 89, the FIRST read counted against the edition-10
cadence (counter ONE of five; the window is OPEN from this landing). No
inaccessible or blocked status this session; the extract was present,
page-marked, complete and read in full (12 PDF pages, abstract, body,
references and appendices A-B complete; the figures themselves are images
in the source PDF, their captions and the tables' values present in the
extract).

- **Library deep-read session 89** (front 2, second of the score-21 tier;
  note:
  paper/research/library/2026-11-22_polymarket_nba_arbitrage_deep_read.md):
  Guang Cheng, Jiaxin Yang and Haoxuan Zou (UCLA), "Arbitrage Analysis in
  Polymarket NBA Markets" (arXiv:2605.00864v1 [q-fin.TR], index year 2026,
  v1 dated May 5, 2026), score 21, index entry x1b6841. The paper: an
  empirical limits-to-arbitrage study of Polymarket's NBA markets from
  75,088,497 polled top-of-book snapshots across 173 games, Feb 4 to
  Mar 4 2026, 3,042 markets, Level 1 only, deduplicated against the
  mirrored order book (PDF pp. 1, 3-4, appendix A); single-market
  arbitrage (AskA+AskB < 1.00 or BidA+BidB > 1.00 on fully collateralized
  complementary tokens, PDF p. 4) yielding 37 theoretical episodes of
  which 30 (81.1%) are post-game stale-quote artifacts with the median
  spread exploded to 7,532.65 bps, leaving 7 valid in-game episodes,
  median duration 3.6 s, capped profit $210.19 at $100 per episode,
  $4,418.44 uncapped (PDF pp. 4-6); combinatorial arbitrage on
  moneyline-spread subset pairs (Ask(ML_A) + Ask(Sp_B) < 1.00 with the
  "Middle" $2.00 jackpot, PDF pp. 6-7), evaluated on 8.59 million states
  unified by a state machine with strict forward-fill imputation
  (appendix B, PDF p. 12), yielding 523 candidates, 233 post-game
  exclusions and 290 active episodes concentrated in the final minutes
  of live play (in-game time-in-arb 0.1762%, PDF p. 7), median duration
  16 s, median yield 101.01 bps, capped $559.59 vs uncapped $2,032.75,
  76.9% of episodes unable to deploy $100 (average 14.79 shares), the
  jackpot realized zero times (PDF pp. 7-9); the desync phantom class:
  staggered 2 to 50 ms serialization of complementary tokens plus naive
  forward projection momentarily crosses the new price against the stale
  complement, registering sub-second phantom arbitrage, killed inside the
  pipeline only by a dynamic 500 ms coeval-clustering rule (appendix A.2,
  PDF p. 10); the mirrored book makes every crossed signal appear
  simultaneously Long and Short, so naive summing would falsely double
  executable profitability until strict dedup (PDF pp. 3-4); the polling
  cadence makes all frequencies conservative lower bounds and all
  durations upper bounds (PDF pp. 3-4, 9-10). Findings, graded:
  1. [candidate sharpening, PENDING OWNER RATIFICATION] The cross-stream
     synchronization and single-source-count pre-declaration: BEFORE the
     L0 gate, any C1-L2/C8-adjacent computation, comparator, null,
     baseline or feature joining two or more asynchronously updated
     data streams (two legs of one book viewed separately, two markets,
     a book feed plus an event or macro timeline, the living board plus
     its klines) must pre-declare as frozen configuration (i) the merge
     timeline (a declared clock or the union of update timestamps),
     (ii) the imputation convention (strictly last-known-value carried
     forward, evaluation points using only states verifiably resting at
     that instant, never look-ahead), (iii) a desync-coeval tolerance
     with which staggered near-simultaneous updates are treated as
     simultaneous, recorded with the claimed structure's insensitivity
     to that tolerance (or across a pre-declared tolerance grid), and
     (iv) a source-overlap map proving no single underlying state is
     counted through two views (mirrored books, complementary tokens,
     one pool under two labels; double-counting inadmissible) — the
     paper proves the failure class in print on all four axes (the
     2-50 ms desync crossing, appendix A.2, PDF p. 10; the mirrored
     Long/Short double-count, PDF pp. 3-4; the forward-fill join of two
     asynchronous books, appendix B, PDF p. 12), and none of the queued
     items binds the stream-join rule itself (the same-period-aggregate
     availability rule binds aggregate-derived features, the concordance
     rule binds text-vs-code in a single estimator, the normalization
     pre-declaration binds rolling statistics, the estimator-configuration
     freeze binds kernel auxiliaries); harder-to-pass because a
     join-established association that survives only under its own
     post-hoc tolerance, imputation or dedup rule, or that counts one
     state twice, now fails at the gate instead of surviving as a find;
     tightens deep-read 84's availability rule and deep-read 85's
     concordance rule by extending frozen configuration to the join of
     streams; queued at #48, PENDING OWNER RATIFICATION; full draft
     with the killed-if-wrong counterfactual in the session note.
  2. [reinforcing, no new item] Seven single-market episodes in
     seventy-five million snapshots is the no-edge default stated as a
     base rate: on a venue whose core invariant hands every participant
     a free arbitrage detector, 81.1% of raw signals are terminal-state
     artifacts and the residual is 7 episodes, median 3.6 s, $210.19
     capped profit in a month across 3,042 markets (PDF pp. 4-6);
     different venue, engine and grain, so no kill line moves and no
     magnitude may enter the record (the laundering rule); recorded as
     reinforcement of the burden of proof only. No queue change.
  3. [reinforcing, no new item] The jackpot's realized base rate is
     zero: the combinatorial structure's doubling upside materialized
     in zero of 290 episodes, the authors concluding participants
     cannot assign meaningful probability weight to the incremental
     upside (PDF p. 8) — the misses-curriculum discipline applied by
     the source itself; an attractive conditional payoff whose realized
     frequency is zero over hundreds of opportunities is a story, not
     an expectancy. No queue change.
  4. [cost-survival ammunition] Executability is the binding
     constraint: top-of-book-only as the most conservative executable
     measure (PDF pp. 3, 10), a $10 minimum bottleneck-leg size (PDF
     pp. 4, 11), a One-Shot paradigm crediting one execution per
     episode because consecutive snapshots would assume regenerating
     liquidity (appendix A.5, PDF p. 11), and 76.9% of combinatorial
     episodes unable to absorb $100 (average 14.79 shares) with the
     capped/uncapped gap $559.59 vs $2,032.75 quantifying
     theoretical-dislocation-versus-extractable-value (PDF pp. 8-9);
     a future K7-style cost-survival layer must carry these
     assumptions: the executable-depth ceiling, not the theoretical
     size, is what prices value. No queue change.
  5. [interpretation caution] Every frequency and duration is a
     sampling artifact of the 3.6 to 5.5 s polling cadence: episodes
     inside one gap evade detection (frequencies are lower bounds),
     forward-difference durations are structural upper-bound estimates,
     and phase trust ceilings (300 s in-game, 1800 s pre/post) cap
     credited durations against outages (PDF pp. 3-4, 9-11); any
     future persistence, duration or episode-count statistic on the
     L2 data must pre-declare its cadence and outage caps and be
     reported as a bounded measurement with both bias directions
     named. No queue change.
  6. [interpretation caution] Terminal-state liquidity must be censored
     by pre-declared rule: the post-game window between physical
     conclusion and oracle resolution sees makers withdraw, the median
     spread explode to 7,532.65 bps, and stale crossings dominate the
     raw signal set (30 of 37 and 233 of 523) until excluded by
     explicit phase rule (PDF pp. 4-5, 7, 10-11) — reinforcing the
     regime-window pre-declaration (deep-read 53) and the macro
     censoring discipline: censoring rules are frozen before the data
     and applied by phase, never by post-hoc inspection. No queue
     change.
  7. [source-quality note] Preprint v1 (three UCLA authors, zero
     citations at cataloguing, no peer-reviewed venue), one month of
     data on a single venue class, explicitly zero fees (PDF p. 10),
     polled Level-1 snapshots rather than full-depth L2, precise-looking
     aggregates resting on an unspecified outlier game (PDF p. 5), with
     both bounds stated honestly in the paper's own limitations
     (PDF p. 9); read, graded, recorded at its grade, consistent with
     score-21 tier placement.
- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (12 PDF pages, abstract, body, references
  and appendices A-B complete).
- Ratification queue after this session: FORTY-EIGHT candidate sharpenings
  plus probe E1, zero armed (ONE queued this session: #48, the cross-stream
  synchronization and single-source-count pre-declaration, joining the
  frozen-configuration and availability families of deep-reads 84 and 85;
  T1 remains armed awaiting the owner's word in its booked state (survived
  all five kill lines with sign inverted); T2 tested-fail); the blocked
  list stays blocked. Deep-read queue pointer: next UNREAD "Collective
  synchronization and high frequency systemic instabilities in financial
  markets" (score 21, x9921ac), last of the score-21 tier (verified
  note-less this session, extract present) — re-read the live tail and
  recompute the tier against the notes before consuming; after it the
  score-20 tier opens at its score-sorted head ("Multivariate Hawkes-based
  Models in LOB: European, Spread and Basket Option Pricing", score 20,
  xaace1f). The edition-10 cadence counter stands at ONE of five by this
  landing (#89, the first counted from the edition-10 reset at ## 117).
- docs/DECISIONS_PENDING.md IS touched by this session (rule: one
  candidate sharpening queued; the ratification line moves to forty-eight
  candidates plus probe E1, zero armed, most recently joined the
  cross-stream synchronization and single-source-count pre-declaration,
  deep-read 89).

Nothing measured, no kill line moved, nothing armed, nothing trades live.
Guard clean before commit: the session assembled the full tracked tree of
main's tip locally (the public main archive, text files restored whole,
including the data CSV trees in the marker sweep's scope) and ran
src/integrity_guard.py over it — marker sweep, library-provenance audit
and encoding sanity all exiting zero on the assembled tree, and exiting
zero again on the same tree plus this session's changed files before
commit; the CI jobs run over the pushed tree and must be verified green
on both jobs before merge.

## 119. Null-time session 100 (2026-11-22): library deep-read session 90 — the Calcagnile-Bormetti-Treccani-Marmi-Lillo collective-synchronization cojump read, last of the score-21 tier; the paper graded an honest endogeneity-of-synchronization empiricism (total one-minute extreme moves decreasing secularly while high-multiplicity cojumps grow up to tenfold, a power-law multiplicity tail truncated at the finite universe, and under 40% of the largest synchronized moves attributable to scheduled macro news, with news-triggered systemic moves completing within ~5 minutes), whose magnitudes are all banned from the record under the laundering rule, whose news-minority fraction reinforces the C8 shuffled-arrival placebo and deterministic-calendar families, whose ~5-minute propagation window reinforces the newly queued cross-stream desync-tolerance disclosure (#48), and whose identity-dropping multiplicity-vector Hawkes is banked as an interpretation caution on aggregate attribution; NO kill line moved; NO sharpening queued; the ratification queue stands at forty-eight candidate sharpenings plus probe E1

Session-state note first (goal-autonomy protocol, ACTIVE; goal state edition
10, ## 117): the live main tail (through ## 118) and docs/DECISIONS_PENDING.md
were read (ratification line: forty-eight candidates plus probe E1 at session
start, zero armed); the cadence check was recomputed from first principles —
the edition-10 counter stood at ONE of five after deep-read 89 (## 118), so no
synthesis pass is due and the default work choice for this session is the
standing deep-read ritual itself, which needs no justification under the
protocol; the cadence counter moves to TWO of five by this landing (#90).
Verified against live state before reading: the triage file score-sorted and
recomputed against the live library note listing (the score-22 tier and
above CLOSED through ## 118; the score-21 tier exhausted by this read —
x532697 landed ## 116, x1b6841 landed ## 118; the head x9921ac verified
note-less with its extract present and page-marked; after it the score-20
tier opens at its score-sorted head xaace1f, verified note-less this session
with extract present; the open-PR set read at session start: empty, no
race). This is deep-read 90, the SECOND read counted against the edition-10
cadence. No inaccessible or blocked status this session; the extract was
present, page-marked, complete and read in full (28 PDF pages, abstract,
body, references, support-information appendices A-C and Table 1 complete).

The paper: "Collective synchronization and high frequency systemic
instabilities in financial markets" (Lucio Maria Calcagnile, Giacomo
Bormetti, Michele Treccani, Stefano Marmi, Fabrizio Lillo; arXiv:1505.
00704v1, May 5, 2015). One-minute extreme returns (bipower-EMA volatility
threshold θ = 4, sensitivity 6, 8, 10; PDF p. 5) in 140 liquid Russell 3000
stocks per year, 2001-2013, after dividing out the mean intraday pattern
(PDF pp. 15-16); cojumps of multiplicity M synchronized across assets; a
three-parameter multivariate Hawkes model of the multiplicity vector
(η = 0.15, β = 0.6 — memory ≈ 1.67 minutes — γ = 2.65; PDF pp. 10-12, 19,
21-22).

Findings, graded (all page-cited in the session note
paper/research/library/2026-11-22_collective_synchronization_cojumps_deep_read.md):

  1. [reinforcing, no new item] Under 40% of high-multiplicity cojumps are
     preceded by a scheduled macro announcement, consistently across all
     years and even at the largest M (PDF pp. 2-3, 9-10, 14): the systemic
     structure is majority-endogenous, so no C1-L2/C8 systemic association
     conditioned on a news/event timeline may interpret its conditioning as
     causal without a null against endogenous clustering — reinforces the
     C8 shuffled-arrival placebo (A3, PROPOSED, owner-gated) and the
     deterministic-calendar null (deep-read 73) by the same mechanism the
     paper measures in print. No queue change.
  2. [reinforcing, no new item] News-triggered systemic cojumps complete
     within ~5 minutes; the attribution fraction is nearly identical across
     τ = 1 to 15 minute lookback windows (PDF pp. 9-10): the tolerance-grid
     insensitivity pattern is exactly what the cross-stream synchronization
     and single-source-count pre-declaration (#48, queued deep-read 89)
     demands a book-plus-macro-timeline join demonstrate, and a join whose
     macro alignment survives only under a silently chosen window is a
     tuning artifact. No queue change.
  3. [reinforcing, no new item] The headline claim survives its own
     pre-emptive grid checks — thresholds θ ∈ {4, 6, 8, 10}, one-to-five
     minute detection windows, 140- vs 700-asset universes (PDF pp. 5,
     7-8, 16-17): windows, thresholds and universe sizes are declared
     configuration, reinforcing the regime-window pre-declaration
     (deep-read 53), the primary-metric pre-commitment (deep-read 55) and
     the estimator-configuration freeze (deep-read 63). No queue change.
  4. [interpretation caution] The multiplicity-vector Hawkes drops the
     identity of the cojumping stocks (PDF p. 11); the 85%-endogenous
     share and the multiplicity-graded excitation (PDF pp. 12-13) license
     nothing at the episode level — an aggregate burst or synchronization
     statistic is equally consistent with common correlation, book-size
     scaling and the level-versus-memory confound, and must pass the
     level-versus-memory disambiguation (deep-read 59, queued) and the
     residual-flow attribution null (deep-read 82, queued) before any
     episode-level reading. No queue change.
  5. [interpretation caution] The multiplicity power-law tail (≈ M^-1.5)
     is explicitly truncated at the finite support M ≤ N and extends when
     N = 700 (PDF pp. 7-8): cross-sectional count statistics inherit a
     universe-size censor, so the universe definition is frozen
     configuration under the standing censoring discipline, and a tail
     statement without it is ambiguous. No queue change.
  6. [reinforcing, no new item] Extremity is defined only after removing
     the mean intraday pattern (PDF pp. 15-16): a future intraday
     extremity or compression-clock feature thresholding raw magnitudes
     would re-import the time-of-day geometry the deterministic-calendar
     null (deep-read 73) exists to kill, and the normalization itself is
     feature-normalization pre-declaration territory (deep-read 83,
     queued). No queue change.
  7. [source-quality note] arXiv v1 preprint, Kibot one-minute bars, one
     venue class, 2001-2013; heuristic weighted-moment calibration with an
     analyst-chosen 0.5 loss weighting (PDF pp. 20-21); the 85%-endogenous
     figure is partly imposed by the parametrization (µ = ηE[λt], spectral
     radius 1 - η by construction, empirical frequencies substituted for
     expected intensities: PDF pp. 11, 19, 21-22), the stationary
     multiplicity distribution matched by construction (PDF p. 19), with
     the honest calibration-on-J=10 versus test-on-J=30/60 split as the
     genre's redeeming feature (PDF pp. 12, 20-21); all magnitudes banned
     from the record as support under the laundering rule; check the
     published version before formal citation.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (28 PDF pages, abstract, body, references,
  support-information appendices and Table 1 complete).
- Ratification queue after this session: UNCHANGED — FORTY-EIGHT candidate
  sharpenings plus probe E1, zero armed (nothing queued this session;
  T1 remains armed awaiting the owner's word in its booked state
  (survived all five kill lines with sign inverted); T2 tested-fail); the
  blocked list stays blocked. Deep-read queue pointer: next UNREAD
  "Multivariate Hawkes-based Models in LOB: European, Spread and Basket
  Option Pricing" (score 20, xaace1f), the score-20 tier's score-sorted
  head (verified note-less this session, extract present) — re-read the
  live tail and recompute the tier against the notes before consuming.
  The edition-10 cadence counter stands at TWO of five by this landing
  (#90).
- docs/DECISIONS_PENDING.md is NOT touched by this session (rule: no
  candidate sharpening queued).

Nothing measured, no kill line moved, nothing armed, nothing trades live.
Guard clean before commit: the session assembled the full tracked tree of
main's tip locally (the public main archive, restored whole) and ran
src/integrity_guard.py over it — marker sweep, library-provenance audit
and encoding sanity all exiting zero on the assembled tree, and exiting
zero again on the same tree plus this session's changed files before
commit; the CI jobs run over the pushed tree and must be verified green
on both jobs before merge.

## 120. Null-time session 101 (2026-11-22): library deep-read session 91 — the Guo-Swishchuk-Rémillard multivariate Hawkes LOB option-pricing read, first of the score-20 tier; the paper graded pure theory assembly with invented parameters and zero empirical calibration, whose α/β near-criticality price explosion reinforces the estimator-configuration freeze and regime-window families and whose count-conditioned-limit unpredictability statement reinforces the availability discipline (deep-read 84, #48), and which earned ONE candidate sharpening: the model-inversion identifiability pre-declaration (#49) — its headline "implied order flow" product proves in print that a parametric model can be inverted onto a scalar observed quantity through analyst-supplied unidentified parameters, with a self-fed circular simulation (PDF pp. 14-15); NO kill line moved; the ratification queue moves to forty-nine candidate sharpenings plus probe E1

Session-state note first (goal-autonomy protocol, ACTIVE; goal state edition
10, ## 117): the live main tail (through ## 119) and docs/DECISIONS_PENDING.md
were read (ratification line: forty-eight candidates plus probe E1 at session
start, zero armed); the cadence check was recomputed from first principles —
the edition-10 counter stood at TWO of five after deep-read 90 (## 119), so no
synthesis pass is due and the default work choice for this session is the
standing deep-read ritual itself, which needs no justification under the
protocol; the cadence counter moves to THREE of five by this landing (#91).
Verified against live state before reading: the triage file score-sorted and
recomputed against the live library note listing (the score-21 tier CLOSED
through ## 116-## 119; the score-20 tier opens at its score-sorted head
xaace1f, verified note-less this session with its extract present and
page-marked; after it the score-20 tier continues at x2b0051 "Pricing VIX
options under the Heston-Hawkes stochastic volatility model", verified
note-less this session with extract present — NOT the already-read Micro
structural Foundation for the Rough Hawkes-Heston paper (deep-read,
2026-11-19), a different paper; the open-PR set read at session start:
empty, no race). This is deep-read 91, the THIRD read counted against the
edition-10 cadence. No inaccessible or blocked status this session; the
extract was present, page-marked, complete and read in full (28 PDF pages,
abstract, body, all sections 1-10, references complete).

The paper: "Multivariate Hawkes-based Models in LOB: European, Spread and
Basket Option Pricing" (Qi Guo, Anatoliy Swishchuk, Bruno Rémillard; 2022,
arXiv:2209.07621v1). Mid-price as multivariate general compound Hawkes
process (Hawkes counts times Markov-chain jump sizes, eqs. 1-3, PDF pp.
2-3), exponentiated into the EMGCHP to keep prices positive (Definition 3.1,
PDF p. 3), LLN/FCLT diffusion limits into geometric Brownian motion (Theorems
3.2-3.7, PDF pp. 4-8), then Black-Scholes European pricing with the Hawkes
composite volatility (eqs. 29-33, PDF pp. 8-10), greeks including the flow
sensitivities (eqs. 34-39, PDF pp. 12-13), Margrabe spread options on two
Hawkes assets and one 2D EMGCHP with model-endogenous correlation (Sections
5-6, PDF pp. 15-21), three-stock basket options via Gentle's approximation
(Section 7, PDF pp. 21-24), minimal hedge (Section 8, PDF pp. 24-26), and
the closing "implied order flow" inversion σ̂²implied = σ*²E(N_t) +
a*²Var(N_t) through analyst-supplied α/β (eqs. 44-47, PDF pp. 14-15).

Findings, graded (all page-cited in the session note
paper/research/library/2026-11-22_multivariate_hawkes_lob_option_pricing_deep_read.md):

  1. [reinforcing, no new item] The option price is nearly flat in α/β at
     small values and explodes as α/β → 1 (Figure 2, PDF pp. 10-11): any
     Hawkes-adjacent statistic is acutely sensitive to the memory ratio near
     criticality, so the branching/memory configuration and the distance
     from spectral radius 1 are research degrees of freedom that could
     manufacture a "regime" or "stress" result by post-hoc re-tuning —
     reinforces the estimator-configuration freeze (deep-read 63) and the
     self-excitation regime-window pre-declaration (deep-read 53); distance
     from criticality is frozen configuration, not a free dial. No queue
     change.
  2. [reinforcing, no new item] The paper states in print that the
     count-conditioned limit "cannot provide us a model for prediction
     tasks since we cannot observe the order flow N_t in advance" (PDF p. 6)
     and prices only under deterministic centralization: a flow-conditioned
     theoretical quantity must condition only on flow verifiably observable
     at the evaluation instant — the same availability discipline demanded
     by the same-period-aggregate feature availability rule (deep-read 84)
     and #48 (deep-read 89), now stated by a Hawkes pricing paper against
     its own theorem. No queue change.
  3. [candidate sharpening, PENDING OWNER RATIFICATION] The implied
     order-flow construction is an under-identified, circular inversion
     (eqs. 44-47, PDF pp. 14-15): one observed scalar (option-implied
     volatility) is split between two unknowns E(N_t) and Var(N_t) through
     an analyst-supplied α/β from unspecified "historical estimation" (PDF
     p. 14) — the same σ̂²implied maps to a continuum of (E, Var) pairs as
     α/β varies, so the "forecast information" is created by the split, not
     measured — and the numerical demonstration is explicitly circular,
     feeding the model's own computed option values back as the observed
     input (PDF p. 14, Figures 4-5, PDF p. 15). Queued proposed sharpening
     #49, the model-inversion identifiability pre-declaration: BEFORE the
     L0 gate, any C1-L2/C8-adjacent computation, comparator, null or
     feature that inverts a parametric model onto an observed quantity —
     implied volatility onto order-flow moments, a measured compression
     score onto a latent priming intensity, an observed spread onto a
     book-state parameter — must pre-declare, as frozen configuration
     counted in the multiplicity ledger: (i) which model parameters are
     FROZEN and from where (dated estimation source or declared generic
     default), every deviation a dated amendment before the data is
     touched; (ii) an identifiability statement proving the observed
     quantity admits a unique parameter split over the unknowns given the
     frozen set, or the inversion declared under-identified with its null
     surfaces reported across a pre-declared frozen-set grid; and (iii) an
     input-provenance trace proving the "observed" input is not itself
     generated by the model family being inverted — self-fed inversions
     are inadmissible at the gate; harder-to-pass because a recovered
     latent quantity that can be re-split arbitrarily after seeing the
     data, or whose input is circularly model-generated, now fails by rule
     instead of surviving as an inverse-problem find; tightens the
     estimator-configuration freeze (deep-read 63) by extending
     pre-commitment from WHICH estimator in WHICH configuration to the
     identifiability of the inversion's parameter split, and the
     dynamics-identification rule for generative nulls (null-time session
     58) on the input-provenance axis, joining the noise-model
     pre-declaration (deep-read 76) in extending frozen configuration into
     the model-input chain; full draft with the killed-if-wrong
     counterfactual in the session note.
  4. [interpretation caution] The EMGCHP-to-GBM chain is a large-n
     trading-frequency asymptotic (PDF pp. 8-9) resting on a mid-price
     model the authors themselves had to exponentiate to avoid non-positive
     prices (Definition 3.1, PDF p. 3): any future L2-derived
     diffusion-limit input to a null or comparator is an asymptotic
     approximation, not book law, and its magnitudes are banned from the
     record as support under the laundering rule. No queue change.
  5. [source-quality note] arXiv v1 preprint, companion to a PhD thesis
     (Guo 2022, PDF pp. 2, 28); no empirical calibration anywhere — every
     parameter invented (PDF pp. 10, 18, 21, 23); internal defects: the
     text labels the diffusion approximation (eq. 20) as the "solution of
     equation (30)" (eq. 31, PDF p. 9), and claims "Since Φ and φ are
     always non-negative, delta and theta are always positive" (PDF p. 12),
     contradicting its own negative-signed theta formula and classical
     theory; check the published version before formal citation. No queue
     change.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (28 PDF pages, abstract, body, references
  complete).
- Ratification queue after this session: FORTY-NINE candidate sharpenings
  plus probe E1, zero armed (ONE queued this session, the model-inversion
  identifiability pre-declaration, #49; T1 remains armed awaiting the
  owner's word in its booked state (survived all five kill lines with sign
  inverted); T2 tested-fail); the blocked list stays blocked. Deep-read
  queue pointer: next UNREAD "Pricing VIX options under the Heston-Hawkes
  stochastic volatility model" (score 20, x2b0051), next in the score-20
  tier (verified note-less this session, extract present) — re-read the
  live tail and recompute the tier against the notes before consuming.
  The edition-10 cadence counter stands at THREE of five by this landing
  (#91).
- docs/DECISIONS_PENDING.md is updated by this session (rule: one candidate
  sharpening queued; queue line moves to forty-nine candidates plus probe
  E1, zero armed).

Nothing measured, no kill line moved, nothing armed, nothing trades live.
Guard clean before commit: the session assembled the full tracked tree of
main's tip locally (the public main archive, restored whole) and ran
src/integrity_guard.py over it — marker sweep, library-provenance audit
and encoding sanity all exiting zero on the assembled tree, and exiting
zero again on the same tree plus this session's changed files before
commit; the CI jobs run over the pushed tree and must be verified green
on both jobs before merge.

## 121. Null-time session 102 (2026-11-22): library deep-read session 92 — the Zamora
Font VIX-options Heston-Hawkes read, second of the score-20 tier; the paper graded
pure existence-theory pricing (a semi-analytical VIX call formula under Heston
variance plus an independent compound Hawkes jump component, with a continuum of
equivalent martingale measures Q(a), generalized Riccati ODEs, and VIX² proved to
be a positive linear combination of the variance and the Hawkes intensity), zero
empirical content, whose measure-continuum pricing reinforces the
estimator-configuration freeze and whose intensity-plus-variance scalar cleanly
instantiates the under-identified split already covered by the model-inversion
identifiability pre-declaration (#49, deep-read 91), and which earned ONE candidate
sharpening: the transform-domain admissibility pre-declaration (#50) — the paper
proves its formula's transform exists only on an explicit contour whose boundary is
a function of the frozen α/β memory ratio and the jump-moment mgf (L_J := (1/η)
M_J^{-1}((β/α)exp(α/β − 1)), Re(ψ) < (β−α)/(αβ), Lemma 5.3 and eq. 7.2, PDF pp. 7-8,
14-15, 18-20), and faults its closest prior model in print for publishing the same
formal transform with no domain study at all (Remark 3.1 on the SVCIJ-H of
Ye-Wu-Chen, PDF p. 5); NO kill line moved; the ratification queue moves to fifty
candidate sharpenings plus probe E1

Session conduct before the reading (the state re-read, not remembered): the
live main tail (through ## 120) and docs/DECISIONS_PENDING.md were read
(ratification line: forty-nine candidates plus probe E1 at session start,
zero armed); the goal-autonomy protocol's cadence was recomputed from first
principles — the edition-10 counter stood at THREE of five after deep-read 91
(## 120), so no synthesis pass is due, the work choice is the standing
deep-read default, and this read moves the counter to FOUR of five; verified
against live state: entry x2b0051 score-sorted next-UNREAD, note-less against
the live library listing (NOT the already-read Rough Hawkes-Heston
microfoundation paper or the already-read Heston-queue-Hawkes option-pricing
paper, both different works), extract present, page-marked (28 PDF pages,
abstract through references complete, read in full); the open-PR set read
at session start: empty, no race. No inaccessible or blocked status this
session.

The paper, one paragraph: dv_t = −κ(v_t − v̄)dt + σ√v_t dW_t + η dL_t with L an
independent compound Hawkes process, general positive jump law (Assumption 1,
mgf maximal domain, PDF p. 3); arbitrage-freeness taken seriously instead of
assumed — Theorem 4.3 gives a continuum of equivalent (local) martingale
measures Q(a), |a| < √(2c_l), c_l explicit in (κ, σ, η, T, jump mgf, α/β)
(Proposition 4.2, PDF pp. 5-6), restricted to a true-martingale subset
E_m(Q_1, 2+ε_1) under Assumption 2's parameter restrictions carrying the
needed inverse-moment and martingale integrability (PDF pp. 6-7); the joint
conditional characteristic function of (v_T, λ_T) is exponential-affine
e^{F+Gv_t+Hλ_t} with (F, G, H) solving generalized Riccati ODEs that are
PROVED to have solutions on [0,T] only inside the explicit complex domain
0 < Re(φ) < min{2κ(a)/σ²(2e^{κ(a)T}−1), L_J}, Re(ψ) < (β−α)/(αβ), the
non-explosion resting on sup_t E[e^{η Re(G)J_1}] < (β/α)exp(α/β−1) (Lemma 5.3,
Proposition 5.4 and the appendix comparison argument, PDF pp. 7-11, 15-20);
VIX²_t then proved a positive linear combination A(a)v_t + B(a)λ_t + C(a)
by the Markov property of the exponential Hawkes and a forward-variance /
variance-swap computation (Propositions 6.2-6.9, Appendix A.2, PDF pp. 11-13,
20-26); the call price assembled by the Lewis/erfc identity on a contour
restricted by eq. (7.2), 0 < φ_R < min{2κ(a)/(σ²A(a))(2e^{κ(a)T}−1),
L_J/A(a), (β−α)/(B(a)αβ)} (Theorem 7.1, PDF pp. 14-15). No numerics, no
calibration, no data anywhere.

Findings, graded (all page-cited in the session note
paper/research/library/2026-11-22_vix_options_heston_hawkes_deep_read.md):

  1. [candidate sharpening, PENDING OWNER RATIFICATION] The transform-domain
     admissibility pre-declaration (#50): BEFORE the L0 gate, any
     C1-L2/C8-adjacent computation, comparator, null or feature whose value
     is computed through a transform of the data or of a fitted model — a
     characteristic-function / Fourier-inversion estimator, an
     affine-transform price or intensity formula, a spectral or
     Laplace/Fourier representation, a moment-generating-function identity —
     must pre-declare, as frozen configuration counted in the multiplicity
     ledger: (i) the domain of existence of the transform as an explicit
     function of the frozen parameters (the region where the defining
     expectation or integral is finite and the associated ODE/integral
     solutions exist), or a dated derivation of that domain; (ii) a recorded
     check, before any data is touched, that every evaluation point lies
     inside the pre-declared domain for ALL frozen configurations it may
     take (boundary-approach behavior declared beside the value); and (iii)
     the numerical-tolerance convention for transform truncation/contour
     choice, frozen — an evaluation outside the proven domain makes the
     statistic UNDEFINED by rule, and an implementation that silently
     returns a finite number (by truncation, damping or contour shift the
     text never authorized) fails the concordance audit; harder-to-pass
     because a transform-based number computed where the underlying
     transform provably does not exist — today survivable as a silent
     numerical artifact of a Fourier or spectral routine — now fails at the
     gate, and a claimed structure resting on such a number is dead by
     rule; tightens the estimator-implementation concordance rule
     (deep-read 85), which checks code against a written definition but
     never requires the definition's own existence domain proven or the
     evaluation point checked against it, and joins the
     estimator-configuration freeze (deep-read 63) and the price-process-
     family invariance rule (deep-read 66) in extending frozen
     configuration to the existence conditions of the analytic object
     itself; the paper proves the failure class is real twice over: its own
     formula exists only on the contour (7.2) whose boundary L_J depends on
     the α/β memory ratio and the jump mgf (PDF pp. 7-8, 14-15, 18-20), and
     its Remark 3.1 states the closest published predecessor (the SVCIJ-H of
     Ye-Wu-Chen [36]) propagated the same formal transform with NO domain
     study ("we miss this study in [36, Proposition 2]", PDF p. 5) — so the
     unchecked-domain failure is not hypothetical, it is the published
     baseline of exactly the family a future L2 comparator would borrow
     from; full draft with the killed-if-wrong counterfactual in the
     session note.
  2. [reinforcing, no new item] The equivalent-martingale-measure family is
     a continuum indexed by a free parameter a (Theorem 4.3: κ(a) = κ + aσ,
     v̄(a), prices all Q(a)-dependent, PDF pp. 5-6), and the paper itself
     cites [33, 34] that "exposures computed under the risk neutral measure
     are essentially arbitrary" (PDF p. 2): every model-implied theoretical
     quantity is a function of an analyst-chosen measure within a family —
     reinforces the estimator-configuration freeze (deep-read 63: the
     measure-indexing parameter is exactly a frozen configuration, never
     re-picked after the result) and the model-inversion identifiability
     pre-declaration (#49: recovering a latent quantity from an observed
     price under an un-fixed member of a continuum is under-identified by
     construction). No queue change.
  3. [reinforcing, no new item] VIX²_t is proved to be A(a)v_t + B(a)λ_t +
     C(a) with B(a) > 0 (Proposition 6.9, PDF p. 13): the model's headline
     observable-equivalent is a one-scalar sum of an observable variance and
     an unobservable self-excitation state — precisely the split that #49
     declares under-identified when performed post hoc; the paper itself
     never inverts (it prices forward from a known state), so the caution
     lands on any future use of a Hawkes-implied intensity against a
     compressed-book observable, which travels the already-queued rule. No
     queue change.
  4. [interpretation caution] The α/β near-criticality sensitivity recurs on
     the existence side: the admissible Re(ψ) bound (β−α)/(αβ) and L_J both
     tighten toward zero as α/β → 1, the same self-exciting configuration
     that inflates magnitudes (deep-read 91, ## 120) also shrinking the
     region where any transform of the process exists at all — where a
     future L2-derived Hawkes-adjacent statistic is computed near its own
     spectral boundary, both its magnitude interpretation AND its
     well-definedness require the frozen distance from criticality of the
     self-excitation regime-window pre-declaration (deep-read 53), one
     mechanism viewed from magnitude and from existence; all magnitudes
     from this paper are banned from the record under the laundering rule
     (there is no empirical content to launder). No queue change.
  5. [source-quality note] arXiv v1 preprint, companion to the
     change-of-measure paper [7] (to appear in Adv. Appl. Probab.) and [6];
     no empirical calibration anywhere, parameters symbolic; internal
     defects that do not touch the domain argument: the Lewis/erfc identity
     stated in two disagreeing forms between (1.1) and (3.2) (PDF pp. 2, 4),
     a garbled comparison line in the Lemma A.6 proof as printed (PDF
     p. 26, the claim itself true), a "Hakwes" typo (PDF p. 3); check the
     published version before formal citation. No queue change.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (28 PDF pages, abstract, body, references
  complete).
- Ratification queue after this session: FIFTY candidate sharpenings plus
  probe E1, zero armed (ONE queued this session, the transform-domain
  admissibility pre-declaration, #50; T1 remains armed awaiting the owner's
  word in its booked state (survived all five kill lines with sign
  inverted); T2 tested-fail); the blocked list stays blocked. Deep-read
  queue pointer: next UNREAD "Transform Analysis for Hawkes Processes with
  Applications in Dark Pool Trading" (score 20, x47bbb5), next in the
  score-20 tier — re-read the live tail and recompute the tier against the
  notes before consuming. The edition-10 cadence counter stands at FOUR of
  five by this landing (#92).
- docs/DECISIONS_PENDING.md is updated by this session (rule: one candidate
  sharpening queued; queue line moves to fifty candidates plus probe E1,
  zero armed).

Nothing measured, no kill line moved, nothing armed, nothing trades live.
Guard clean before commit: the session assembled the full tracked tree of
main's tip locally (the public main archive, restored whole) and ran
src/integrity_guard.py over it — marker sweep, library-provenance audit
and encoding sanity all exiting zero on the assembled tree, and exiting
zero again on the same tree plus this session's changed files before
commit; the CI jobs run over the pushed tree and must be verified green
on both jobs before merge.

## 122. Null-time session 103 (2026-11-22): library deep-read session 93 — the Gao-Zhou-Zhu transform-analysis dark-pool read, third of the score-20 tier; the paper graded pure transform-theory for a marked linear Hawkes process with a general (non-Markovian) exciting function and time-dependent baseline (joint Laplace transform via the immigration-birth representation and a Hammerstein-Volterra integral equation, moments, Faà di Bruno mass functions, synthetic dark-pool fill metrics), zero empirical content; NO kill line changed; ONE candidate sharpening queued, the moment-equivalence disclosure (#51), PENDING OWNER RATIFICATION; the ratification queue moves to fifty-one candidates plus probe E1

Provenance note (added by the ## 123 restoration): the landed session-103
instance's own ## 122 append never survived its landing push — the log repair
recorded at ## 123 found the live file truncated with no session-103 entry
in it — so this entry is RECONSTRUCTED 2026-11-22 by null-time session 104
from the landed instance's own surviving products only (the session note on
main, paper/research/library/2026-11-22_transform_analysis_hawkes_dark_
pool_deep_read.md; PR #294's body; the squash-commit message d2a0d182),
following the ## 74 reconstruction precedent. Every verdict, finding and
queue number below is the landed record exactly; nothing new is authored.

Session-state note (director step, per docs/goal_autonomy_protocol.md,
edition 10): the edition-10 cadence counter stood at FOUR of five after
deep-read 92, so no synthesis pass was due at session start; this read
(#93) moves the counter to FIVE of five, closing the edition-10 window —
the NEXT session opens with the synthesis pass (edition 11, its own log
entry) before its read. The entry x47bbb5 was verified note-less against
the live library listing (the two score-20 entries ranked above it,
xaace1f and x2b0051, both carry notes dated 2026-11-22 on main's tip);
its extract was present and page-marked (42 PDF pages); read in full.

Verdict: NO kill line changed; ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION — the moment-equivalence disclosure (#51): the
paper proves in print that E[N_T] and E[L_T] depend on the mark law ONLY
through E[l_1] (and E[L_T^2] only through the first two moments,
Proposition 5 with Remark 6, PDF pp. 12-13) while the same-mean mark laws
(constant, exponential, hyper-exponential) are shown to produce
systematically different fill-rate and conditional-fill outputs
(Figures 2-4, eq. 3.10, PDF pp. 20-23, 41-42). Proposed amendment: BEFORE
the L0 gate, any model-based comparator, null, or statistic built from a
marked point-process or marked-intensity construction must pre-declare,
as part of its frozen configuration, which of its outputs are
moment-bounded (provably functions of finitely many moments of the
mark/size law, hence inheritable from a moment-matched calibration) and
which are law-sensitive (functions of the full mark law); a concordance
or validation audit that matches only finitely many moments may certify
the moment-bounded outputs and may NOT certify the law-sensitive ones.
Harder-to-pass: a moment-matched implementation that today passes the
estimator-implementation concordance audit (deep-read 85) while its
law-sensitive outputs ride on an unverified distributional assumption
chosen after the fact now fails at the gate. Tightens the
estimator-implementation concordance rule (deep-read 85) and joins the
estimator-configuration freeze (deep-read 63) and the transform-domain
admissibility pre-declaration (#50).

Reinforcing (no new item): the numerics fix the branching structure at
0.9 (C = 0.9 power-law kernels, PDF p. 23) with fill metrics drifting
materially by kernel tail exponent (Figures 5-7, PDF pp. 24-26) — the
same near-critical configuration whose frozen distance from criticality
the self-excitation regime-window pre-declaration (deep-read 53) already
demands; all numeric magnitudes banned from the record under the
laundering rule (invented parameters, no data). Interpretation caution:
time-to-first-fill is baseline-only (its distribution 1 - exp(-integral
of mu) with the self-excitation component absent entirely, PDF p. 16),
so an excitation parameter inferred from first-arrival behavior is
unidentified by construction (the level-versus-memory disambiguation,
deep-read 59; the model-inversion identifiability pre-declaration,
#49). The dark-pool fill-rate arithmetic is execution-strategy
engineering, recorded as cost-survival ammunition only and never
operationalized. Source-quality note: arXiv v1 preprint (4 Oct 2017); a
published version exists — check it before formal citation; all numerics
synthetic; internal defects not touching the transform argument
(repeated "¿From" typesetting artifacts, PDF pp. 17, 22, 37, 40; the
non-empty-pool section leaving the conditional Y > 0 branch informal,
PDF pp. 26-28).

- Inaccessible/blocked status: none this session (the extract was
  present, page-marked and read in full, 42 PDF pages, abstract, body,
  references, appendices A-E complete).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed; T1 remains armed awaiting the owner's word
  in its booked state (survived all five kill lines with sign inverted);
  T2 tested-fail; the blocked list stays blocked. docs/DECISIONS_PENDING.md
  updated by this session: the queue line moves from fifty to fifty-one,
  the thirty-ninth dashboard. Deep-read queue pointer: next UNREAD "The
  order book as a queueing system: average depth and influence of the
  size of limit orders" (the score-20 entry xe1c4ca, verified note-less,
  next in the score-20 tier) — re-read the live tail and recompute the
  tier against the notes before consuming. The edition-10 cadence
  counter closes at FIVE of five by this landing (#93): the NEXT session
  opens with the ninth synthesis pass (edition 11, its own log entry)
  before its read.

Nothing measured, no kill line moved, nothing armed, nothing trades live.
Guard clean before commit per the landed record; the CI jobs run over the
pushed tree and must be verified green on both jobs before merge.

## 123. Null-time session 104 (2026-11-22), first act: the session-103 race-and-truncation corrigendum — the programme log restored byte-verified from the intact git-history core (entries through ## 121 restored to the landed ## 121 content, ## 122 reconstructed from the landed session-103 products per the ## 74 precedent), the write-side truncation class taking its fifth logged instance with the live log itself as the casualty, and the parallel-instance collision recorded under the main-wins protocol; NO kill line moved

Session-state note, per the goal-autonomy conductor protocol (edition 10,
## 117, ACTIVE): this entry records a landing-path repair, not new
research. The standing directive scheduled the next null-time deep-read
session; at session start the live main tail and docs/DECISIONS_PENDING.md
were read as mandated, and the log file's own state forced this first
act: the live main tree (tip d2a0d182, the PR #294 squash of session 103)
carried paper/research/null_time_programme.md as a 63,998-byte file ending
mid-sentence inside entry ## 20 — the whole of the remainder of ## 20's
text, entries ## 21 through ## 121, and any session-103 entry were absent
from the live file. docs/DECISIONS_PENDING.md on main was intact and
consistent with a landed session 103 (fifty-one candidates plus probe
E1, the moment-equivalence disclosure queued), and the session-103 note
on main was intact — the corrupted artifact was the log alone.

Byte-level verification (everything in this paragraph is cmp-verified
observable repo state): the damaged blob is byte-identical to the first
63,998 bytes of the intact core as it landed at b4a7d002 (PR #293's
squash of session 92, 822,696 bytes through ## 121, carrying the ## 121
separator formatting fix); that core is byte-identical on the session-92
branch deep-read/session-92-x2b0051 (tip 2efebe6c); and the write-side
~64K truncation class named at editions 8 through 10 (## 75, ## 78,
## 94, ## 98) has its FIFTH logged instance, this time consuming the
live log itself. This session's own read of the log through the same
~64K content channel reproduced the truncation exactly before any
repair was attempted, confirming the class as a tooling-channel
failure mode, not a session-specific error; and the integrity guard
passed the corrupted tree because it sweeps conflict markers, library
provenance and encoding, not byte-size monotonicity of the log — so CI
stayed green through the corruption. The discipline of byte-verifying
large pushes against the assembled local copy after pushing (the PR
#289 convention) is restated; the standing CI gap (a byte-monotonicity
check on the log file) remains the ranked infrastructure item,
candidate-improvement status only, NOT implemented by this act.

Landing-path reconstruction (observable branch/PR state): two
session-103 instances ran the same x47bbb5 read in parallel against the
same ## 121 pointer, both branches still standing on the remote. Branch
null-session-103-deep-read-93 (tip f83d9175) opened PR #294, which
merged as d2a0d182: its library note and its DECISIONS_PENDING update
are the LANDED, OPERATIVE record (both verified byte-identical between
branch and main), while its log file was the truncated assembly.
Branch deep-read-93-transform-analysis-hawkes-dark-pool (tip 66b477c7)
never landed: it carries the full intact core plus its own complete
## 122 entry, which grades the same read NO-sharpening (queue fifty,
DECISIONS_PENDING untouched) and a note differing in authorship from
the landed one. Under the main-wins race protocol (## 105, ## 109) its
product is superseded and discarded off-record; its ## 122 entry is
NOT restored. Consistency check between the two independent reads of
the same paper (the ## 109 precedent): both graded NO kill line moved;
both recorded the paper as zero-empirical-content pure transform
theory; both banked the branching-0.9 invented numerics under the
laundering ban; both flagged the baseline-only first-fill identification
caution; both cited the arXiv v1 caution. They differ on one point: the
landed instance queued the moment-equivalence disclosure as #51, the
superseded instance treated the same mechanism as already covered by
#46/#49/#50 and queued nothing. The landed record stands; the
superseded instance's strengthening of the same discipline family is
recorded here as corroboration from an independent read, nothing more.

The repair (this act): the live log is restored to the intact core
verbatim (byte-verified against all surviving copies: the b4a7d002
parent blob, the session-92 branch tip, and the truncation-point match
of the damaged file) plus the RECONSTRUCTED ## 122 entry (the entry
immediately above), built only from the landed instance's own surviving
products, per the ## 74 reconstruction precedent, and labeled as a
reconstruction inside the entry itself. Nothing else on main was
damaged: the session-103 note and DECISIONS_PENDING on main are
byte-identical to what PR #294's head pushed; the corrupted artifact is
the log alone, and the log alone is restored.

Landing-path-integrity items registered under the gap family named at
editions 8-10 and the session-90 corrigendum precedent (## 105, ## 109):
branches null-session-103-deep-read-93 (the landed race branch; its
product lives on main; the branch is owner-deletable) and
deep-read-93-transform-analysis-hawkes-dark-pool (the superseded
duplicate; owner-deletable) are both named in the record; no session
tool deletes remote branches. Root cause recorded plainly: the landing
instance assembled its log push from a content channel that delivered
only the first ~64K bytes of the 822,696-byte file, and its push
enshrined the truncated read as the file's whole content — the same
class the record has logged four times before (## 75, ## 78, ## 94,
## 98) — with the guard's byte-monotonicity gap letting CI pass it.

docs/DECISIONS_PENDING.md is NOT touched by this corrigendum (rule: no
candidate sharpening queued; the ratification file stands as landed —
fifty-one candidate sharpenings plus probe E1, zero armed).

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py --sweep, --library
and --encoding exit zero on the assembled tree (main's tracked tree
restored whole plus this session's changed files) before commit; the
full-tree checks run in CI over the pushed tree and must be verified
green on both jobs before merge.

## 124. Null-time session 104 (2026-11-22), second act: the ninth synthesis pass — the cadence recomputed from the edition-10 reset at ## 117 (deep-reads 89-93 landed at ## 118 through ## 122, the window CLOSED at five of five per the ## 122 closing pointer, which directed the pass run before the read, and run against the restored record after the session's first-act repair), goal state rewritten as EDITION 11, the G2 brief-debt recomputed against the grown queue (briefs cover forty of fifty-one; items 41-51 owed), the truncation-and-collision history absorbed into the named-gap block; NO sharpening queued by the pass

The pass re-read the live record through the restored tail (## 1 through
## 122) and recomputes the edition-10 window: deep-reads 89-93 landed at
## 118, ## 119, ## 120, ## 121 and ## 122; ZERO kill lines moved in the
window; FOUR sharpenings queued in it, all four frozen-configuration or
pre-declaration extensions of already-queued families (#48, the
cross-stream synchronization and single-source-count pre-declaration,
## 118; #49, the model-inversion identifiability pre-declaration,
## 120; #50, the transform-domain admissibility pre-declaration, ## 121;
#51, the moment-equivalence disclosure, ## 122) — the declining-yield
expectation named at editions 3-10 holds: the queue keeps being fed from
the same declare-before-the-data vein, not from any new mechanism class.
The window was NOT infrastructure-clean: the session-103 double-instance
collision and the write-side truncation of the programme log itself
(repaired byte-verified by the session's first act, ## 123) give the
collision history its fourth logged event (## 98, ## 105, ## 109, ## 123)
and the write-side ~64K truncation class its fifth instance (## 75, ## 78,
## 94, ## 98, ## 123) — this time the casualty was the live log on main,
and the integrity guard's byte-monotonicity gap let CI pass it; the gap
stays the ranked infrastructure item, candidate-improvement status only.

Products of this pass, traveling only through the sanctioned channels:
(1) goal state rewritten whole as EDITION 11 (protocol section 2,
edition rule; the section 16 note records the change) — facts block
recomputed from the live record at ## 122 (queue fifty-one plus probe
E1 at pass time, zero armed; ninety-five library note files through
deep-read 93, the 96th landing as this session's third act and counting),
ranked fronts unchanged in order with statuses recomputed, the
deep-read pointer recomputed by title-matching the score-sorted triage
file against the restored tail and the library listing (the score-21
tier CLOSED at ## 116, ## 118 and ## 119; the score-20 tier OPEN with
three of its fifteen entries consumed at ## 120 through ## 122; next
UNREAD xe1c4ca, "The order book as a queueing system: average depth and
influence of the size of limit orders" — consumed as this session's
third act), cadence: RESET by this edition, the counter
standing at ONE of five with #94 landing as this session's third act and
counting; (2) docs/GOALS.md status board refreshed to edition 11
(operative bookkeeping only; the protocol's section 2 stays the ranking
authority). The pass measures nothing, arms nothing, launders nothing
INTO any spec, and queues NO sharpening; the G2 brief debt is named not
paid (briefs owed for items 41-51 before the next directorate sitting:
#41 the noise-model pre-declaration, ## 100; #42 the queue-jump-diffusion
generative null, ## 107; #43 the residual-flow attribution null, ## 108;
#44 the feature-normalization pre-declaration, ## 110; #45 the
same-period-aggregate feature availability rule, ## 112; #46 the
estimator-implementation concordance rule, ## 113; #47 the
impact-viability pre-declaration for generative nulls, ## 115; #48 the
cross-stream synchronization and single-source-count pre-declaration,
## 118; #49 the model-inversion identifiability pre-declaration, ## 120;
#50 the transform-domain admissibility pre-declaration, ## 121; #51 the
moment-equivalence disclosure, ## 122).

docs/DECISIONS_PENDING.md is untouched BY THE PASS (this session's third
act grades the next read; the file moves only if a sharpening is
queued). Nothing measured, no kill line moved, nothing armed, nothing
trades live. Guard clean on the assembled tree plus this session's
changed files before commit; the CI jobs run over the pushed tree and
must be verified green on both jobs before merge.

## 125. Null-time session 104 (2026-11-22), third act: library deep-read session 94 — the Muni Toke order-book-as-a-queueing-system read, fourth of the score-20 tier; the paper graded a zero-intelligence Markovian queueing construction of book depth whose conservation-of-flows identity, printed sign-reversal under covariate-set choice, and spread-path-conditional distance-indexed depth statistics reinforce already-queued families and move NOTHING; NO kill line moved; NO new candidate sharpening

The paper: Ioane Muni Toke, "The order book as a queueing system: average
depth and influence of the size of limit orders" (arXiv:1311.5661v1,
22 Nov 2013; slug xe1c4ca, per docs/library/expanded_index.json). A
one-side order book with per-price Poisson limit-order arrivals, unit
Poisson market orders (rate mu) and exponential order lifetimes
(rate theta), treated as an M/M/1+M queueing system: stationary
distribution of the cumulative depth, a continuous spatial-Poisson
extension giving the closed-form average shape b(p) (Proposition 1,
eq. 12, PDF p. 8), a law of conservation of the flows stating the
average shape equals the arrival intensity times the cancellation
probability (Proposition 2, eqs. 14-17, PDF pp. 8-9), a geometric-size
extension via M^X/M/1+M bulk queues (Propositions 3-4, eqs. 27-30,
PDF pp. 14-16), the theoretical result that at constant total incoming
volume fewer-and-larger limit orders deepen the near-spread book
(eqs. 29-31, Figures 3-4, PDF pp. 16-19), and a 14-stock, 391-interval,
7-week Paris panel (Jan 4 - Feb 22 2010) with fixed-effects regressions
broadly consistent with it (Table 2, PDF pp. 19-23). Read in full
(26 page-marked PDF pages) against the one question. Note landed at
paper/research/library/2026-11-22_order_book_queueing_system_deep_read.md.

Verdict: NO kill line changes. NO new candidate sharpening. Findings
(all graded against the restored record and the queue as it stands at
fifty-one candidates plus probe E1):

1. [reinforcing, no new item] The conservation-of-flows identity:
   the average book shape is the arrival intensity times the
   cancellation probability (Proposition 2, eq. 14, PDF p. 8; eqs.
   15-18, PDF pp. 8-9), an exact within-model consequence — a book
   null in this class reproduces mean depth BY CONSTRUCTION from its
   declared flow parameters, so a shape-agreement audit against such a
   null certifies arithmetic, not mechanism; and the stationary depth
   exists only because theta > 0 (cancellation is the stabilizer, PDF
   pp. 5-6): a generative book null with no positive cancel rate has no
   stationary depth at all. Votes for the generative-null pre-declaration
   and placebo families (deep-reads 81/87) and for specifying the
   passive-cancel rate as frozen configuration; the paper's printed
   model is exactly the zero-intelligence class the passive-withdrawal
   anatomy must not be laundered from. No queue change.
2. [reinforcing, no new item] A sign reversal under covariate-set
   choice is printed in the paper's own results: the market-order
   volume coefficient is significantly POSITIVE without the limit-order
   interaction term (+0.0088, t = 11.1, p < 2.2e-16) and significantly
   NEGATIVE with it (-4.8e-4, t = -5.3, p = 1.4e-7) on the same data and
   sample (Table 2, top panel, PDF p. 23; specification eq. 32,
   PDF p. 21; the B10 panel repeats the pattern, +0.0097, t = 5.6 →
   -6.2e-4, t = -3.1, PDF p. 23). The covariate set IS configuration:
   the SIGN of a significant coefficient is a function of the
   specification. The paper handles its own reversal honestly (naming
   the apparent paradox and resolving it, PDF pp. 22-23); the fact is a
   vote for the estimator-configuration freeze (deep-read 63) and the
   primary-metric pre-commitment (deep-read 55), not a new item. No
   queue change.
3. [interpretation caution] Distance-indexed depth statistics are
   anchor- and spread-path-conditional: the empirical depths B_i are
   computed at 1-10 ticks from the best opposite price over 30-minute
   intervals, and the paper states B_{10+j} "is not exact if the spread
   reaches a level lower or equal to j ticks during interval t"
   (PDF pp. 20-21), so measured depth at tick-distance mixes exact and
   censored observations exactly when the spread tightens toward the
   ten-limit data boundary (PDF pp. 19-20). A future L2 depth feature
   indexed by distance from touch must pre-declare its anchor
   convention (instantaneous vs interval-averaged best price) and its
   truncation-through-spread-tightening composition shift, or it
   silently conditions on the spread path. Feeds the censoring
   discipline and the availability discipline (#45/#48); joins the
   fixed-tick structural-bias caution (deep-read 14). No queue change.
4. [interpretation caution] The model's own simplifications are
   acknowledged empirically false in its class (exponential lifetimes
   vs the power-law lifetimes cited, lifetimes plausibly
   distance-dependent; Poisson flows vs the complex point processes
   known to govern order flows; PDF p. 5), so the headline
   fewer-and-larger-orders result is a Markovian-family statement;
   its empirical support is an association at 30-minute grain on a
   14-stock panel (PDF pp. 19-23), which licenses nothing at tick grain
   where event-time and volume clocks govern (a within-grain
   association at one grain is not evidence at another). No queue
   change.
5. [cost-survival ammunition] All depth/activity magnitudes (the
   positive activity-depth relation decaying with distance —
   significant at B5 and B10, not significant at B10-B5, Table 2 lower
   panel, PDF p. 23; R2 0.08-0.15, PDF p. 23) are venue-, sample- and
   grain-specific and banned from the record under the laundering rule;
   a future K7-style cost-survival layer would have to carry the
   assumptions the model assumes away (a one-side book with an
   infinite-volume standing bid at zero, unit market orders,
   share-by-share independent cancellations, price-time separable
   intensity, PDF pp. 4-5, 13). A never-operationalized
   execution-strategy application. No queue change.
6. [source-quality note] arXiv v1 (22 Nov 2013); a published version
   exists — check it before formal citation. Data: 14 Paris stocks
   (13 CAC-40 members plus Ubisoft), Jan 4 - Feb 22 2010, with 3.5
   missing or incomplete trading days acknowledged (footnote 2,
   PDF p. 19); first ten limits only (PDF pp. 19-20); the ask/bid
   side convention for the regression depths is left unstated beyond
   the "first 10 ticks from the best opposite side" definition
   (PDF pp. 20-21) — an unstated convention in exactly the class the
   convention-declaration rule names. No queue change.

Counterfactual (what this paper would have killed if we had done it
wrong): without the estimator-configuration freeze, a future C1-L2
panel decomposition could report whichever covariate-set sign fits the
narrative — the paper's own table shows a significant positive and a
significant negative estimate of the same coefficient available on the
same data (Table 2, PDF p. 23). Without the censoring discipline, a
distance-from-touch depth statistic would silently shift composition
exactly when the spread tightens (PDF pp. 20-21) — the regime where
compression claims would live. Without the generative-null and placebo
disciplines, a zero-intelligence null "reproducing" the average book
could be cited as validation (PDF p. 8) when the reproduction is the
null's own conservation identity — an arithmetically guaranteed match
dressed as a test.

- Inaccessible/blocked status: none this session. The extract was
  present, page-marked and read in full (26 PDF pages, abstract, body,
  references complete).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read, NONE queued by
  this session's first or second act; docs/DECISIONS_PENDING.md is NOT
  touched by this session; T1 remains armed awaiting the owner's word in
  its booked state (survived all five kill lines with sign inverted);
  T2 tested-fail); the blocked list stays blocked. Deep-read queue
  pointer: next UNREAD "Hawkes Processes" (xf8b5bc, score 20, verified
  note-less this session against the live listing), next in the
  score-20 tier — re-read the live tail and recompute the tier against
  the notes before consuming. The edition-11 cadence counter stands at
  ONE of five by this landing (#94), counted from the edition-11 reset
  at ## 124.
- Byte-landed log note (session-specific): this session pushed the
  restored and appended log through the tooling path and byte-verified
  the pushed branch copy against the assembled local copy (md5 match)
  before opening the PR, per the PR #289 convention and the ## 123
  root-cause record.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit; the CI jobs run
over the pushed tree and must be verified green on both jobs before
merge.

## 126. Null-time session 105 (2026-11-22): library deep-read session 95 — the Laub-Taimre-Pollett "Hawkes Processes" survey read, fifth of the score-20 tier; the 2015 pedagogical survey graded zero-empirical-content codification whose branching-ratio arithmetic (n = ∫µ = α/β, stationarity strict, explosion at n ≥ 1, endogeneity read as probability n), printed Lorenzen timestamp-randomisation critique, exponential-kernel recursion bargain, MLE failure-mode catalogue, and residual (random time change) test loop all reinforce already-queued families and move NOTHING; NO kill line moved; NO new candidate sharpening

The paper: Patrick J. Laub, Thomas Taimre, Philip K. Pollett, "Hawkes
Processes" (arXiv:1507.02822v1 [math.PR], last edited 13 July 2015; slug
xf8b5bc, per docs/library/expanded_index.json). A survey of the linear
Hawkes process: counting/point processes, conditional intensity and
compensator (PDF pp. 2-4); the linear definition with exponential and
power-law kernels (PDF pp. 5-6); the immigration-birth branching
representation, branching ratio n = ∫µ = α/β, asymptotic normality under
0 < n < 1, a.s. explosion for n ≥ 1, and a uniformly random arrival
endogenous with probability exactly n (PDF pp. 6-8); the exponential-kernel
covariance density and shifted-scaled-Cauchy power spectral density for
α < β (Theorem 2, PDF pp. 9-11, Appendix A pp. 26-27); nonlinear and
mutually-exciting generalisations (PDF pp. 11-12); the financial section —
the Aït-Sahalia-Cacho-Diaz-Laeven Hawkes diffusion (5m + 3m² parameters,
fitted only for pairs, no AIC/BIC comparisons, the von Neumann elephant
verdict, PDF pp. 12-13) and the Filimonov-Sornette mid-price-change
stylisation with the Lorenzen critique of Unif(0,1) timestamp jitter
(second-resolution data, impossible simultaneity, smoothing that fit
better than millisecond truth, biased α and β, PDF p. 13); MLE with the
O(k) recursive log-likelihood (Markov joint (N, λ*), PDF pp. 15-17),
small-sample bias, local optima, kernel sensitivity, the GMM
alternative's "rather arbitrary" smoothing (PDF p. 17), and the printed
minefield quote (PDF pp. 14-15); goodness of fit via the random time
change theorem to a unit-rate Poisson process, tested as iid Exp(1)
interarrivals (PDF pp. 18-20); three exact simulation algorithms
(PDF pp. 20-24). Read in full (28 page-marked PDF pages) against the one
question. Note landed at
paper/research/library/2026-11-22_hawkes_processes_survey_deep_read.md.

Verdict: NO kill line changes. NO new candidate sharpening. Findings
(all graded against the restored record and the queue as it stands at
fifty-one candidates plus probe E1):

1. [reinforcing, no new item] Branching-ratio arithmetic in definition
   form: n = α/β for the exponential kernel, stationarity strict
   (0 < n < 1), explosion a.s. for n ≥ 1, endogeneity of a uniform
   random arrival with probability exactly n (PDF pp. 7-8). An
   estimated n is an endogeneity fraction ONLY inside a stationary fit;
   an n crossing 1 is the model's own stationary moment ceasing to
   exist, not a regime discovery to report. Votes for the existing
   branching-ratio / self-excitation stability family. No queue change.
2. [reinforcing, no new item] The Lorenzen critique printed in the
   survey's own section: second-resolution timestamps with simultaneous
   arrivals jittered by Unif(0,1) fractions, smoothing that fit the
   model better than true millisecond data, biased α and β (PDF p. 13).
   A textbook instance of the already-queued timestamp/convention
   discipline and estimator-configuration freeze (deep-read 63); nothing
   here tightens either. No queue change.
3. [interpretation caution] The Markov/recursion bargain: the O(k)
   recursive likelihood and cheap derivatives exist because the
   exponential kernel makes (N, λ*) Markov (PDF pp. 16-17); any other
   kernel family forfeits the recursion (PDF pp. 21-22). A future
   Hawkes arm faces a declared configuration trade — kernel family,
   optimiser, and effective-configuration statement move together. Feeds
   the estimator-mode freeze already queued. No queue change.
4. [interpretation caution] MLE's printed failure modes: significant
   small-sample bias, many local optima, high sensitivity to excitation
   function (PDF p. 17); GMM moments smoothed by a "rather arbitrary"
   user-selected procedure (PDF p. 17); the minefield quote
   (PDF pp. 14-15). Substantively covered by the estimator-mode register
   and noise-model pre-declaration already queued: optimiser, kernel
   family, and smoothing must be pre-declared because each choice moves
   (α, β, n). No queue change.
5. [reinforcing, no new item] The residual loop is the compensator-null
   discipline in closed form: transform arrivals by the FITTED
   compensator and demand a unit-rate Poisson process (Theorems 4-5,
   PDF p. 18; eq. 18, p. 16), tested as iid Exp(1) interarrivals
   (QQ/KS/AD/Lewis/Brownian tests, PDF pp. 18-20). A future placebo or
   generative-null arm earns nothing from "looks clustered"; the pass
   condition is available and explored-data-free. No queue change.
6. [cost-survival ammunition] Overfitting arithmetic any K7-style
   cost-survival layer must quote before adopting a Hawkes contagion
   component: 5m + 3m² parameters (plus 3m for stochastic volatility),
   fitted only for market pairs even after simplifications, no AIC/BIC
   comparisons against the nested Merton model; a
   never-operationalised execution-strategy application (PDF pp. 12-13).
   No queue change.
7. [source-quality note] arXiv v1 pedagogical survey, zero empirical
   content (every figure simulated; the estimation section bypasses
   real-data challenges by declared choice, PDF pp. 14-15); value here
   is codification of exact formulas, not new results; minor
   typographical slips ("natually", "moest") confirm early-draft status;
   check for a journal version before formal citation (PDF p. 1).
   No queue change.

Counterfactual (what this paper would have killed if we had done it
wrong): without the timestamp discipline, a future L2 event arm could
have inherited the Filimonov-Sornette path wholesale — second-resolution
data, jittered simultaneity, and a branching-ratio "trend" that is
partly the smoothing artifact the survey prints (PDF p. 13). Without the
stationarity condition, an estimated n crossing 1 could have been read
as an exciting regime discovery rather than the detonation of the
model's own moment conditions (PDF pp. 7-8). Without the residual
discipline, a placebo arm could declare success because simulated
output "looks" clustered, when the compensator-transform test is
decisive either way (PDF p. 18). Without the cost-survival ceiling, a
5m + 3m²-parameter Hawkes diffusion with no AIC/BIC comparisons could
have been adopted as a market model before the L2 data had even passed
the L0 gate (PDF pp. 12-13).

- Inaccessible/blocked status: none this session. The extract was
  present, page-marked and read in full (28 PDF pages, abstract, body,
  appendices and references complete).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read;
  docs/DECISIONS_PENDING.md is NOT touched by this session; T1 remains
  armed awaiting the owner's word in its booked state; T2 tested-fail);
  the blocked list stays blocked. Deep-read queue pointer: next UNREAD
  "Theory of earthquakes interevent times applied to financial markets"
  (x97b372, score 20, sixth of the score-20 tier, verified note-less this
  session against the live listing) — re-read the live tail and recompute
  the tier against the notes before consuming. The edition-11 cadence
  counter stands at TWO of five by this landing (#95), counted from the
  edition-11 reset at ## 124.
- Byte-landed log note (session-specific): this session assembled the
  log locally from the live main copy plus this entry and will
  byte-verify the pushed branch copy against the assembled local copy
  (md5 match) before opening the PR, per the PR #289 convention and the
  ## 123 root-cause record. The write path this session is the
  connector push (branch off live main head, full-file contents
  byte-checked), used because the local execution environment exposes
  no git CLI or credentials this cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit; the CI jobs run
over the pushed tree and must be verified green on both jobs before
merge.

## 127. Null-time session 106 (2026-11-22): library deep-read session 96 — the Jagielski-Kutner-Sornette earthquake-interevent-times read, sixth of the score-20 tier; the 2016 research letter graded a pooled-parameter Hawkes interevent-PDF transplant from seismology to daily loss exceedances whose boundary-pinned branching ratio (n = 1.00 exactly at every mean interevent time ≥ 5 days, the bound "imposed to ensure stationarity"), definitional rate-identity violation repaired by a post-hoc three-parameter scaling law, and cross-sectionally averaged per-asset calibrations reinforce already-queued families and move NOTHING; NO kill line moved; NO new candidate sharpening

The paper: Maciej Jagielski, Ryszard Kutner, Didier Sornette, "Theory of
earthquakes interevent times applied to financial markets" (arXiv:1610.08921v2
[q-fin.ST], 28 Oct 2016, submitted to Physica A; slug x97b372, per
docs/library/expanded_index.json). Daily loss exceedances (thresholds set to
hit mean interevent times of 2, 5, 10, 30, 70 days) across 15 records — four
US equities, five indices, two crudes, five FX pairs (PDF p. 4) — are fitted
with the Saichev-Sornette closed-form interevent-time PDF of a self-excited
Hawkes process with an Omori-Utsu power-law kernel Φ(t) = θ t0^θ/(t0+t)^{1+θ}
(PDF pp. 2-4, eqs. 1-6), parameters calibrated per asset by maximum likelihood
and then averaged across the 15 assets (PDF pp. 4-5), the branching ratio
saturating at its imposed stationarity upper bound n = 1.00 for every ⟨τ⟩ ≥ 5
days (Table 1, PDF p. 4), the average rate λ violating its definitional
identity λ = 1/⟨τ⟩ and repaired by the post-hoc scaling law λ(⟨τ⟩) =
0.17 + 0.90 exp(−⟨τ⟩/10) which "imitates a spurious power law" in range (eq. 7,
Fig. 2, PDF pp. 5-6), and a closing concession that the mono-fractal Hawkes
family under-describes multifractal volatility clustering, so even the
markets-are-critical reading "may be an artefact of its mono-fractal nature"
(PDF p. 6). Read in full (9 page-marked PDF pages, references through [55])
against the one question. Note landed at
paper/research/library/2026-11-22_earthquake_interevent_times_hawkes_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail; the session's work choice is the DEFAULT deep-read (next
UNREAD triage entry, re-ranked against the notes: the score-20 tier holds
fourteen entries, five consumed by ## 120-## 122 and ## 125-## 126, x97b372
next, no note on main per the live listing), so no justification is owed.
Synthesis cadence NOT due: this landing is the THIRD of five deep-reads since
the edition-11 reset at ## 124 (after #94 at ## 125 and #95 at ## 126).

Verdict: NO kill line changes. NO new candidate sharpening. Findings
(all graded against the restored record and the queue as it stands at
fifty-one candidates plus probe E1):

1. [reinforcing, no new item] Boundary-pinned branching ratio: Table 1's
   n = 0.78 at ⟨τ⟩ = 2 days and exactly n = 1.00 at every larger mean
   interevent time, with the bound explicitly "imposed to ensure
   stationarity" (PDF p. 4), is the branching-ratio stationarity discipline
   (n = ∫µ, strict 0 < n < 1, explosion a.s. for n ≥ 1; the survey read, log
   ## 126, finding 1) printed as a live borderline case: the unconstrained
   likelihood wanted the non-stationary side, and the paper's own hedge
   (citing the Hardiman-Bercot-Bouchaud vs Filimonov-Sornette controversy,
   PDF p. 4) concedes the point. A pinned-at-bound fit reads as "at the edge
   of the existence domain", never as a critical-regime discovery. No queue
   change.
2. [interpretation caution] The rate-identity violation and its post-hoc
   repair: λ ≠ 1/⟨τ⟩ as the Hawkes construction requires, repaired by a
   three-parameter functional form selected after the failure was seen (eq. 7,
   PDF pp. 5-6). A future exceedance-family or interevent-family statistic
   must pre-declare its threshold grid and treat rate-vs-mean identities as
   diagnostics, not fit targets — both already carried by the
   estimator-configuration freeze (deep-read 63) as frozen configuration. The
   paper's honest headline is that the mono-fractal Hawkes family
   under-describes the clustering it is fitted to: a good interevent-PDF fit
   certifies nothing about the mechanism (PDF pp. 5-6). No queue change.
3. [interpretation caution] Pooled-parameter averaging across 15 assets
   after per-asset MLE (PDF pp. 4-5), with no printed fit statistic anywhere,
   turns a cross-sectional configuration choice into a "universality" curve:
   the Table 1 error-bar range (PDF p. 4) is parameter dispersion, not
   goodness of fit. Feeds the estimator-mode freeze and the pooled-vs-
   conditional reading discipline (the Cox-ratio read's pooled-accuracy
   lesson, log ## 70). No queue change.
4. [interpretation caution] Daily-grain, closing-price, loss-exceedance-only
   events (PDF p. 4): nothing here bears L2 information, and the paper's
   universality claims may never enter the record as support for any program
   claim — the library-is-ammunition caveat binds; the daily grain is already
   bracketed by the queued C1-L2 base-rate confrontation. No queue change.
5. [source-quality note] arXiv v2, 9 pages, research-letter grade: visual
   double-log fit judgement, no model comparison against the Denys et al.
   superstatistics baseline beyond curves, and a universality conclusion
   resting on finding 3's pooled averages. Check the published Physica A
   version before formal citation. No queue change.

Counterfactual (what this paper would have killed if we had done it wrong):
without the stationarity discipline, Table 1's n = 1.00 would have been read
as printed market criticality — a substantive regime discovery laundering a
parameter pinned to an imposed stationarity bound, when the honest statement
is that the stationary model is at the edge of its existence domain and the
unconstrained fit would cross it (PDF pp. 3-4). Without the frozen-
configuration discipline, eq. 7 is exactly the forbidden move: a
re-functionalization chosen after the definitional identity failed on the
data, presented as a novel characterization (PDF pp. 5-6). Without the
library-is-ammunition caveat, the "universal scaling law of interevent
times" headline would have entered as evidence that long-memory
self-excitation is a market property, when the paper's own print is a
phenomenological curve match with no fit statistic and a stated
mono-fractality failure (PDF pp. 5-6).

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (9 PDF pages, abstract, body, figures and
  references complete).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read;
  docs/DECISIONS_PENDING.md is NOT touched by this session; T1 remains
  armed awaiting the owner's word in its booked state; T2 tested-fail); the
  blocked list stays blocked. Deep-read queue pointer: next UNREAD
  "Asymmetric excitation of left- and right-tail extreme events probed using
  a Hawkes model: application to financial returns" (x55e853, score 20,
  seventh of the score-20 tier,
  verified note-less this session against the live listing) — re-read the
  live tail and recompute the tier against the notes before consuming. The
  edition-11 cadence counter stands at THREE of five by this landing (#96),
  counted from the edition-11 reset at ## 124.
- Byte-landed log note (session-specific): this session assembled the
  log locally from the live main copy plus this entry and will
  byte-verify the pushed branch copy against the assembled local copy
  (md5 match) before opening the PR, per the PR #289 convention and the
  ## 123 root-cause record. The write path this session is the
  connector push (branch off live main head, full-file contents
  byte-checked), used because the local execution environment exposes
  no git CLI or credentials this cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit; the CI jobs run
over the pushed tree and must be verified green on both jobs before
merge.

## 128. Null-time session 107 (2026-11-22): library deep-read session 97 — the Tomlinson-Greenwood-Mucha-Kruczyński two-tailed POT Hawkes asymmetry read, seventh of the score-20 tier; the 2021 S&P 500 daily-returns model family finding extreme losses exciting about twice as many daughters as gains (γ↔←/γ↔→ = 2.2 ± 0.5) with loss-excitation decaying about five times faster (β←/β→ = 4.6 ± 1.2), a fitted type-conditional reproduction above unity (γ↔← = 1.2) held subcritical only by the spectral-radius check (ρ ≈ 0.82-0.87, arithmetic on the printed tables, no data touched), the authors' own residual evidence that branching elements fitted across regime onsets are inflated upper bounds, and a GARCH-residual sensitivity appendix flagging exactly the frozen-configuration freedoms — all reinforcing; NO kill line moved; NO new candidate sharpening

The paper: Matthew F. Tomlinson, David Greenwood, Marcin Mucha-Kruczyński,
"Asymmetric excitation of left- and right-tail extreme events probed using a
Hawkes model: application to financial returns" (arXiv:2011.12291v2
[q-fin.ST], 10 Aug 2021, referee-acknowledged, formatted for Physical Review
E; slug x55e853, per docs/library/expanded_index.json). A two-tailed
peaks-over-threshold marked Hawkes family — bivariate coupled, bivariate
decoupled, asymmetric common-intensity, and symmetric common-intensity forms
(PDF pp. 2-4, eqs. 1-13) — is fitted by maximum likelihood (L-BFGS-B, MCMC-
verified per Appendix B, PDF pp. 13-14) to exceedances of fixed 2.5%/97.5%
training quantiles of S&P 500 daily log-returns (1959-10-02 to 2020-11-20,
training to 2008-09-01; PDF pp. 4-5) and compared by AIC, BIC, likelihood
ratio and Ogata residual analysis (PDF pp. 5-9, Tables III-V). The
common-intensity form with asymmetric tails wins both training and forecast,
the two tails share one arrival intensity (PDF pp. 6-7), the headline
asymmetries are γ↔←/γ↔→ = 2.2 ± 0.5 and β←/β→ = 4.6 ± 1.2 (PDF p. 7), read
as negativity bias (PDF p. 10), and Appendix A shows the γ-asymmetry is
reproducible by GJR-GARCH leverage alone while the β-asymmetry is not
(PDF pp. 10-13, Tables VI-VIII), with POT Hawkes on GARCH residuals
"highly sensitive" to the volatility-model assumptions (PDF pp. 11-12). Read
in full (15 page-marked PDF pages, appendices and references complete)
against the one question. Note landed at
paper/research/library/2026-11-22_asymmetric_tail_excitation_hawkes_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail (edition 11); the session's work choice is the DEFAULT deep-read
(next UNREAD triage entry, re-ranked against the notes: the score-20 tier
holds fifteen entries, six consumed — xaace1f at ## 120, x2b0051 at
## 121, x47bbb5 at ## 122, xe1c4ca at ## 125, xf8b5bc at ## 126 and
x97b372 at ## 127 — so this read takes x55e853 seventh, no note on main
per the live listing), so no justification is owed. Synthesis cadence
NOT due: this landing is the FOURTH of five deep-reads since the
edition-11 reset at ## 124 (#94 at ## 125, #95 at ## 126, #96 at
## 127, #97 here).

Verdict: NO kill line changes. NO new candidate sharpening. Findings
(all graded against the restored record and the queue as it stands at
fifty-one candidates plus probe E1):

1. [reinforcing, no new item] Multitype branching-ratio discipline, printed
   as a live case: subcriticality is correctly stated as ρ(Γ) < 1 (PDF p. 3),
   but the fitted tables give a type-conditional reproduction ABOVE unity —
   γ↔← = 1.2 ± 0.1 under θci (Table II, PDF p. 6), equivalently the θbi
   left-mother column sum 0.58 + 0.60 = 1.18 (Table I, PDF p. 6) — with the
   cascade still finite only because the balanced type mix holds the total
   reproduction at (1.2 + 0.54)/2 ≈ 0.87 and the θbi spectral radius at
   ≈ 0.82 (arithmetic on the printed table values this session performed
   descriptively; no data touched, nothing measured). A future multitype
   self-excitation score checks spectral radius on the fitted matrix and
   never reads a per-type reproduction above one as regime criticality —
   the discipline standing from the survey read (log ## 126, finding 1)
   and the earthquake-interevent read (log ## 127, finding 1), now in its
   multitype form. No queue change.
2. [interpretation caution] The paper's own residual evidence that
   endogeneity estimates across regime onsets are inflated upper bounds:
   localized lag-1 ACF peaks at the tail ends of the 1973-4, 1987 and
   GFC clusters print systemic over-forecasting, and the authors' stated
   cause is un-modelled non-constant exogenous intensity forcing all
   excess intensity into self-excitation — "self-excitement may more so
   be the mechanism by which the excited state persists" (PDF pp. 9-10).
   Feeds the endo-exo / apparent-criticality reading discipline and the
   estimator-mode freeze; the instigation-versus-persistence split is
   unresolved by the paper's own fit. No queue change.
3. [interpretation caution] Configuration freedom does measurable work in
   the headline: constant quantile thresholds produce a 168:124 left/right
   forecast split under distribution drift (PDF p. 8), while the
   GARCH-residual alternative is "highly sensitive" to the volatility-model
   assumptions and produces decay constants of order 10³ days the authors
   themselves call "not naturally described by a Hawkes-type self-exciting
   process" (PDF pp. 10-12, footnote 2, PDF p. 12). The threshold-grid
   pre-declaration and grain-attribution requirements are already frozen
   as configuration (deep-read 63; reaffirmed deep-read 96, log ## 127
   finding 2). No queue change.
4. [interpretation caution] Daily closing-price, single-index grain; no L2
   information; the negativity-bias reading is the authors' speculation,
   not a measured causal claim (PDF p. 10); the model's own left-tail
   residual excesses fail the KS test in the GFC and Covid clusters
   (Fig. 5, PDF p. 9) — printed failure exactly where the macro synthesis
   would depend on it. The daily grain is already bracketed by the queued
   C1-L2 base-rate confrontation; the empirical asymmetry claims are
   standing context only, never support for any program claim — the
   library-is-ammunition caveat binds. No queue change.
5. [source-quality note] arXiv v2, 15 pages, Physical-Review-E-formatted
   with anonymous-referee acknowledgment (PDF p. 10) — the published version
   should be checked before formal citation; the extract garbles the
   Table I/II γ and β submatrix subscripts (cross-read against eqs. 3-11
   and the ratio statements on PDF p. 7) and the KS p-values of Figs. 1, 5
   and 9; one author has an industry affiliation (CheckRisk LLP, PDF p. 1);
   single asset, no cross-market replication. No queue change.

Counterfactual (what this paper would have killed if we had done it wrong):
without the spectral-radius discipline, γ↔← = 1.2 would have been read as
printed loss-driven supercriticality — a type-conditional reproduction
count laundered into a regime discovery, when the stationary process survives
only via the sub-unity right-tail mix (ρ ≈ 0.82-0.87). Without the endo-exo
reading discipline, the over-forecasting ACF peaks the authors honestly print
(PDF pp. 9-10) would have been tuned away as model refinement instead of
standing as evidence that branching elements are inflated where exogenous
intensity is un-modelled. Without the frozen-configuration discipline, the
constant-versus-normalized threshold choice — which flips the asymmetry
story's composition between the raw fit and every GARCH-residual fit (PDF
pp. 8, 12, Tables VII-VIII) — is exactly the researcher degree of freedom
the estimator-configuration freeze removes. Without the
library-is-ammunition caveat, "negativity bias in markets" would have entered
the record as an established market property on the strength of a
within-family fit whose left tail fails its own residual test in the two
crisis regimes that matter most.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (15 PDF pages, abstract, body, both
  appendices, figures and references complete; the extraction's table-
  subscript garbles are recorded in finding 5 and every number used was
  cross-checked against the equations and the paper's own ratio
  statements on PDF p. 7).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read;
  docs/DECISIONS_PENDING.md is NOT touched by this session; T1 remains
  armed awaiting the owner's word in its booked state; T2 tested-fail); the
  blocked list stays blocked. Deep-read queue pointer: next UNREAD
  "Analysis of Contagion in China's Stock Market: A Hawkes Process
  Perspective" (x999a87, score 20, eighth of the score-20 tier, verified
  note-less this session against the live listing) — re-read the live tail
  and recompute the tier against the notes before consuming. The
  edition-11 cadence counter stands at FOUR of five by this landing (#97),
  counted from the edition-11 reset at ## 124; the synthesis pass is due
  at the next session after the fifth deep-read lands.
- Byte-landed log note (session-specific): this session assembled the
  log locally from the live main copy plus this entry and will
  byte-verify the pushed branch copy against the assembled local copy
  (md5 match) before opening the PR, per the PR #289 convention and the
  ## 123 root-cause record. The write path this session is the
  connector push (branch off live main head, full-file contents
  byte-checked), used because the local execution environment exposes
  no git CLI or credentials this cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit; the CI jobs run
over the pushed tree and must be verified green on both jobs before
merge.

## 129. Null-time session 108 (2026-11-22): library deep-read session 98 — the Yang "Analysis of Contagion in China's Stock Market" read, eighth of the score-20 tier; the 2023/2025 single-author thesis-graded multivariate Hawkes study of Chinese index and sector daily extremes, whose unchecked above-unity self-excitation diagonals, never-evaluated spectral-radius condition, six-deep configuration-freedom stack (percentile thresholds, grid-searched ω, 150-day windows, representative-period selection, inhibitory link, MC-noisy SGD compensator), visually-only goodness-of-fit, drifting baseline intensities, and "spatiotemporal" title over a non-spatial multivariate type-indexed fit reinforce already-queued families and move NOTHING; NO kill line moved; NO new candidate sharpening

The paper: Junwei Yang, "Analysis of Contagion in China's Stock Market: A
Hawkes Process Perspective" (arXiv:2512.08000v1 [q-fin.ST], title page dated
"This version: May 18, 2023", arXiv stamp 8 Dec 2025; slug x999a87, per
docs/library/expanded_index.json). Experiment 1 turns daily returns of the
Shanghai Composite, Shenzhen Component and ChiNext indices (Feb 2013 - Mar
2023, n = 2,452 each) into two event types at the 10th/90th SSE-history
percentiles and fits bivariate exponential-kernel Hawkes by MLE (tick), decay
grid-searched to ω = 0.1, reading the up-weighted impact-matrix rows as trend
continuation and oversold rebound (PDF pp. 13-16, Tables 1-2). Experiment 2
slices three CSI sector indices into fifteen 150-day windows, builds six
event types, and fits a six-dimensional inhibitory nonlinear Hawkes
(unconstrained µ, α under g(x) = max(x, 0.01), eq. 13, PDF p. 18) by
Monte-Carlo-integrated stochastic-gradient backprop (Mei-Eisner, Algorithm 1,
PDF pp. 11-12), comparing an active period 3 and a dormant period 5 and
reading the block contrast as trend continuation versus sector rotation
(PDF pp. 16-19, Tables 3-4). Appendices derive the likelihood and run the
random-time-change residual check visually only (PDF pp. 24-27), against a
homogeneous-Poisson baseline whose moment estimates drift (λ̂train =
[0.100, 0.101] versus λ̂test = [0.067, 0.082], called "a scheme change in
market structure", PDF p. 25). Read in full (27 page-marked PDF pages,
appendices and references complete) against the one question. Note landed
at paper/research/library/2026-11-22_china_contagion_hawkes_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail (edition 11); the session's work choice is the DEFAULT
deep-read (next UNREAD triage entry, re-ranked against the notes: the
score-20 tier holds fourteen entries per the live edge_triage_scores.json
recounted this session (the ## 128 entry printed "fifteen"; the live file
holds fourteen), seven consumed — xaace1f at ## 120, x2b0051 at ## 121,
x47bbb5 at ## 122, xe1c4ca at ## 125, xf8b5bc at ## 126, x97b372 at ##
127 and x55e853 at ## 128 — so this read takes x999a87 eighth, no note on
main per the live listing), so no justification is owed. Synthesis cadence
NOW DUE AT THE NEXT SESSION: this landing is the FIFTH of five deep-reads
since the edition-11 reset at ## 124 (#94 at ## 125, #95 at ## 126, #96 at
## 127, #97 at ## 128, #98 here); the next session must open with the
edition-12 synthesis pass per the protocol's section 4 before any further
deep-read.

Verdict: NO kill line changes. NO new candidate sharpening. Findings (all
graded against the queue as it stands at fifty-one candidates plus probe
E1):

1. [reinforcing, no new item] Spectral-radius discipline, printed as a live
   omission case: the paper states ρ(A) < 1 only in theory (PDF p. 9) and
   never evaluates it on any fitted matrix. Arithmetic on the printed
   Experiment-1 impact matrices (descriptive only, no data touched): ρ ≈
   0.654 for SSE (A = [[0.382, 0.387], [0.218, 0.343]], PDF p. 14, eq. 12),
   ρ ≈ 0.562 for Shenzhen with one small negative eigenvalue (det < 0;
   Table 2, PDF p. 16) and ρ ≈ 0.560 for ChiNext — all subcritical, so
   nothing near-critical is laundered; the omission is the reinforcement.
   No queue change.
2. [reinforcing, no new item] Experiment 2 prints per-type self-excitation
   diagonals above unity in the active period (1.161, 1.143, 1.313, 0.671,
   0.831, 1.092, Table 4a, PDF p. 19) with no full-matrix stationarity
   check and no branching read; Gershgorin arithmetic on the printed table
   (row 0: centre 0.696, radius 1.451, discs reaching ≈ 2.15; row 3 centre
   1.228) leaves ρ unverifiable from the print while the paper reads the
   diagonals straight as trend continuation (PDF pp. 18-19) — exactly the
   apparent-criticality case the queued branching-matrix pre-declaration
   family (## 118 lineage; reaffirmed ## 126-## 128, findings 1) exists to
   prevent. No queue change.
3. [interpretation caution] The configuration-freedom stack runs six deep
   before any claim: percentile thresholds indexed to the SSE history
   (PDF p. 14), one grid-searched ω = 0.1 shared across types (PDF
   pp. 14-16), fifteen equal 150-day windows with representative periods
   chosen by narrative (PDF pp. 17-18), the unconstrained inhibitory form
   under g(x) = max(x, 0.01) (eq. 13, PDF p. 18), and the MC-integrated
   SGD gradient whose compensator term is a sampled average, not an exact
   integral (Algorithm 1, PDF pp. 11-12). The MC noise in the compensator
   is a freedom the certified estimator modes do not carry; under the
   estimator-configuration and estimator-mode freezes it is standing
   context only. No queue change.
4. [interpretation caution] The paper's own baseline shows non-constant
   background intensity across the sample (λ̂test strictly below λ̂train,
   read by the authors as a market-structure scheme change, PDF p. 25), and
   every goodness-of-fit exhibit is visual Q-Q/scatter with no printed test
   statistic anywhere (PDF pp. 25-27, Figs. 5-7). The endo-exo reading
   discipline (un-modelled exogenous forcing inflates self-excitation;
   log ## 128 finding 2) and the printed-statistic-or-it-did-not-happen
   convention both apply unchanged. No queue change.
5. [source-quality note] Student-thesis grade relative to its score-20
   rank, read per the session-9 triage-audit rule rather than silently
   skipped: single author acknowledging a dissertation committee and
   supervisor (PDF p. 1); title page dated May 18, 2023 against an arXiv
   2512.08000v1 stamp of 8 Dec 2025 (PDF p. 1); the abstract promises
   "spatiotemporal Hawkes processes" (PDF p. 1) while the paper fits
   ordinary multivariate type-indexed Hawkes processes with no spatial
   structure at all; a 36-plus-2-parameter six-type model fitted per
   150-trading-day window (PDF pp. 17-19); daily grain only, three Chinese
   indices and three Chinese sector indices, no L2 content, no published
   version to check. No queue change.

Counterfactual (what this paper would have killed if we had done it wrong):
without the load-bearing spectral-radius discipline, the above-unity
diagonals of Table 4a would print as measured trend persistence — a per-type
reproduction count laundered into a market property, on 150-day windows with
no stationarity check at all. Without the estimator-configuration freeze,
this paper is the compounding case: thresholds, grid-searched decay, window
segmentation, representative-period selection, link-function, and MC-noisy
SGD compensator — six researcher degrees of freedom stacked on 150
observations per fit; the "sector rotation confirmed" headline (PDF pp.
18-19) is what six knobs produce, and the pre-declaration exists so the
programme can never occupy that position. Without the
library-is-ammunition caveat, the oversold-rebound and
chasing-gains-cutting-losses readings (PDF pp. 14-15) would have entered
the C8 macro-synthesis as established Chinese-market properties on the
strength of a within-family student-thesis fit with no printed residual
statistic.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (27 PDF pages, abstract, body, both
  appendices, figures and references complete; the one earlier mis-guess of
  the extract filename was corrected against the live listing and nothing
  was skipped).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read;
  docs/DECISIONS_PENDING.md is NOT touched by this session; T1 remains
  armed awaiting the owner's word in its booked state; T2 tested-fail); the
  blocked list stays blocked. Deep-read queue pointer: next UNREAD
  "A market impact game under transient price impact" (xc495e3, score 20,
  ninth of the score-20 tier, verified note-less this session against the
  live listing) — re-read the live tail and recompute the tier against the
  notes before consuming. The edition-11 cadence counter now stands at
  FIVE of five by this landing (#98), counted from the edition-11 reset at
  ## 124; the edition-12 synthesis pass is DUE and must open the next
  session before any further deep-read, per the protocol's section 4.
- Byte-landed log note (session-specific): this session assembled the
  log locally from the live main copy plus this entry and will
  byte-verify the pushed branch copy against the assembled local copy
  (md5 match) before opening the PR, per the PR #289 convention and the
  ## 123 root-cause record. The write path this session is the
  connector push (branch off live main head, full-file contents
  byte-checked), used because the local execution environment exposes
  no git CLI or credentials this cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit; the CI jobs run
over the pushed tree and must be verified green on both jobs before
merge.
## 130. Null-time session 109 (2026-11-23), first act: the tenth synthesis pass — the cadence recomputed from the edition-11 reset at ## 124 (deep-reads 94-98 landed at ## 125 through ## 129, the window CLOSED at five of five per the ## 129 closing pointer, which directed the pass run before the read, against the clean tail), goal state rewritten as EDITION 12, the G2 brief-debt recomputed against the standing queue (briefs cover forty of fifty-one; items 41-51 owed), the FIRST zero-yield window recorded (zero kill-line moves, zero sharpenings in the window); NO sharpening queued by the pass

The pass re-read the live record through the clean tail (## 1 through
## 129) and recomputes the edition-11 window: deep-reads 94-98 landed at
## 125, ## 126, ## 127, ## 128 and ## 129; ZERO kill lines moved in the
window; ZERO sharpenings queued in it — the first fully zero-yield window
since the pass sequence began at edition 3, confirming the
declining-yield expectation named at editions 3-11 at its floor: the
score-20 tier is returning reinforcing reads and interpretation cautions
only, and the queue's declare-before-the-data vein is fully extended
pending owner ratification, not a source of new mechanism classes. The
window WAS infrastructure-clean: no new truncation, corruption or
collision instance anywhere in ## 125 through ## 129; the write-side
~64K truncation class (five instances: ## 75, ## 78, ## 94, ## 98,
## 123) and the collision history (four events: ## 98, ## 105, ## 109,
## 123) stand unchanged; the byte-monotonicity/verification infrastructure
gap stays the ranked infrastructure item, candidate-improvement status
only.

Products of this pass, traveling only through the sanctioned channels:
(1) goal state rewritten whole as EDITION 12 (protocol section 2,
edition rule; the section 17 note records the change) — facts block
recomputed from the live record at ## 129 (queue fifty-one plus probe
E1 at pass time, zero armed; one hundred library note files through
deep-read 98, the 101st landing as this session's second act and
counting), ranked fronts unchanged in order with statuses recomputed, the
deep-read pointer recomputed by title-matching the score-sorted triage
file against the live tail and the library listing (the score-21
tier CLOSED at ## 116, ## 118 and ## 119; the score-20 tier OPEN with
EIGHT of its FOURTEEN entries consumed at ## 120 through ## 122 and
## 125 through ## 129; next UNREAD xc495e3, "A market impact game
under transient price impact" — consumed as this session's second
act), cadence: RESET by this edition, the counter
standing at ONE of five with #99 landing as this session's second act and
counting; (2) docs/GOALS.md status board refreshed to edition 12
(operative bookkeeping only; the protocol's section 2 stays the ranking
authority). The pass measures nothing, arms nothing, launders nothing
INTO any spec, and queues NO sharpening; the G2 brief debt is named not
paid (briefs owed for items 41-51 before the next directorate sitting:
#41 the noise-model pre-declaration, ## 100; #42 the queue-jump-diffusion
generative null, ## 107; #43 the residual-flow attribution null, ## 108;
#44 the feature-normalization pre-declaration, ## 110; #45 the
same-period-aggregate feature availability rule, ## 112; #46 the
estimator-implementation concordance rule, ## 113; #47 the
impact-viability pre-declaration for generative nulls, ## 115; #48 the
cross-stream synchronization and single-source-count pre-declaration,
## 118; #49 the model-inversion identifiability pre-declaration, ## 120;
#50 the transform-domain admissibility pre-declaration, ## 121; #51 the
moment-equivalence disclosure, ## 122).

docs/DECISIONS_PENDING.md is untouched BY THE PASS (this session's second
act grades the next read; the file moves only if a sharpening is
queued). Nothing measured, no kill line moved, nothing armed, nothing
trades live. Guard clean on the assembled tree plus this session's
changed files before commit; the CI jobs run over the pushed tree and
must be verified green on both jobs before merge.

## 131. Null-time session 109 (2026-11-23), second act: library deep-read session 99 — the Schied-Zhang market-impact-game read, ninth of the score-20 tier; the 2013/2017 two-agent Nash-equilibrium theory of the hot-potato game under transient (propagator) impact, whose endogenous-volume-without-information mechanism, game-form-dependent sign-structure inversion (single-agent buy-only vs two-agent oscillating on the same convex kernel), grain-inverting cost-frequency behavior with odd/even-N grid-parity artifacts, and zero-spread/quadratic-slippage/coin-toss-latency assumptions reinforce already-queued families and move NOTHING; NO kill line moved; NO new candidate sharpening

The paper: Alexander Schied and Tao Zhang, "A market impact game under
transient price impact" (arXiv:1305.4013v7 [q-fin.TR], stamp 8 May
2017; slug xc495e3, per docs/library/expanded_index.json). Two competing
agents liquidate inventories in a propagator impact model: martingale
unaffected price (PDF p. 3), discrete grid, strictly positive-definite
decay kernel G (eqs. 1-2, PDF pp. 3-4), average-price execution with symmetric
latency by coin toss and quadratic transaction costs (Definitions
2.1-2.2, eq. 3, PDF pp. 3-4). Theorem 2.5 proves existence and uniqueness
of the Nash equilibrium in adapted strategies with an explicit
deterministic formula: strategies spanned by two kernel-only vectors v
and w (eqs. 7-8, PDF pp. 5-6). For vanishing transaction costs and fine
grids the equilibria oscillate — the "hot-potato game" — read as
protection against predatory trading (Remark 2.10, PDF p. 8). Theorem
2.7, the main result, identifies the critical threshold theta* = G(0)/4
above which all oscillations disappear (equilibria become buy-only or
sell-only), proven for log-convex kernels and equidistant grids through
triangular-Toeplitz inversion, the Kaluza sign criterion and M-matrix
theory (PDF pp. 7-8, 19-24); below theta*, Proposition 2.8 proves the
last three trades of w alternate signs (PDF p. 8) and Proposition 2.9
proves full-vector sign alternation for exponential kernels (PDF
pp. 18-19). Numerical simulations on invented parameters (Figures 1-6,
PDF pp. 9-13) show expected costs increasing in trading frequency for
small theta but decreasing at theta*, an odd/even-N grid-parity sawtooth
at theta = 0 that disappears already at theta = 0.01 (Figure 4, PDF
pp. 10-11), and expected costs lower WITH transaction costs than
without, minimum near theta of 0.06 (Figure 5, PDF pp. 11-12),
interpreted through the asymmetry that predatory strategies are round
trips penalized more than one-directional liquidations (PDF p. 11); a
price-of-anarchy comparison against unaware single-trader strategies is
defined (PDF pp. 11-13). Zero empirical content anywhere; the
Flash-Crash hot-potato vignette from the CFTC-SEC report (27,000
contracts, 49 percent of volume, roughly 200 net, in 14 seconds, PDF
pp. 1-2) is motivating narrative only. Read in full (26 page-marked
PDF pages, abstract, body, both proof sections, all six figures and
references complete) against the one question. Note landed at
paper/research/library/2026-11-23_market_impact_game_transient_price_impact_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail (edition 12, written this session's first act, ## 130);
the session's work choice is the DEFAULT deep-read (next UNREAD triage
entry, re-ranked against the notes: the score-20 tier holds fourteen
entries per the live edge_triage_scores.json, eight consumed — xaace1f
at ## 120, x2b0051 at ## 121, x47bbb5 at ## 122, xe1c4ca at ## 125,
xf8b5bc at ## 126, x97b372 at ## 127, x55e853 at ## 128 and x999a87
at ## 129 — so this read takes xc495e3 ninth, no note on main per the
live listing), run after the edition-12 synthesis pass discharged first
per the ## 129 closing pointer's instruction.

Verdict: NO kill line changes. NO new candidate sharpening. Findings (all
graded against the queue as it stands at fifty-one candidates plus probe
E1):

1. [reinforcing, no new item] Endogenous volume without information,
   proven in print: the two-agent Nash equilibrium on a propagator impact
   model generates strong two-sided recirculation (single components of
   the equilibrium vectors exceeding 60 percent of the initial position,
   Figure 1, PDF p. 9) with near-zero net liquidation, purely from
   strategic interaction — protecting against predatory trading
   (Theorem 2.5 and Remark 2.10, PDF pp. 5-8). High L2 activity, volume
   and turnover is not per se evidence of information-bearing flow: the
   C8 shuffled-arrival placebo and the generative-null pre-declaration
   families (## 118 lineage; #42, #47) already carry the case, and this
   read changes nothing. No queue change.
2. [interpretation caution] The sign structure of simulated endogenous
   flow is decided by the strategic-structure assumption, not by the
   kernel: for the same convex nonincreasing decay kernel, the
   single-agent optimum is buy-only or sell-only (Alfonsi-Fruth-Schied
   Theorem 1, quoted as Remark 2.11, PDF p. 10) while the two-agent
   equilibrium on the identical kernel oscillates (Theorem 2.7,
   Propositions 2.8-2.9, PDF pp. 7-8, 17-18). No data can identify game
   form within the propagator family, and it flips the predicted sign
   structure; under the estimator-configuration freeze and the
   dynamics-identification and generative-null pre-declarations the
   game form of any future generative null is one more knob frozen
   before the data. Recorded as standing context. No queue change.
3. [interpretation caution] Grain conclusions invert with a cost
   constant: expected costs increase in trading frequency for small
   theta, decrease at theta = theta* = G(0)/4, and exhibit a pure
   odd/even-N grid-parity sawtooth at theta = 0, gone already at
   theta = 0.01 (Figure 4 and discussion, PDF pp. 10-11).
   Grid parity and the direction of grain-dependence are simulation
   artifacts conditional on an unmeasured cost parameter in this model
   family; never market structure. Reinforces the grain-association
   caution and the flow-clock scale-constant frozenness. No queue
   change.
4. [cost-survival ammunition] The "transaction costs can reduce
   everyone's expected costs" result (minimum near theta of 0.06,
   Figure 5, PDF pp. 11-12; the calming-effect discussion, PDF p. 24)
   matters only if a future K7-style cost-survival layer exists; that
   layer must carry the declared assumptions: zero bid-ask spread
   averaged over order types with rebates and dark pools argued away
   (Remark 2.3, PDF p. 5), quadratic temporary impact as slippage
   (eq. 3, PDF p. 4), symmetric latency by coin toss (Definition 2.2,
   PDF p. 4), martingale unaffected price (PDF p. 3). A "taxes calm
   fire sales" reading is model-internal on invented parameters;
   banned from the record as support for any programme claim. No queue
   change.
5. [source-quality note] Established-authors theory preprint: arXiv v7
   stamped 8 May 2017 on a 2013 id; the v-vector oscillation assertions
   are simulation-only (PDF p. 8); oscillation and no-oscillation
   proofs limited to log-convex kernels and equidistant grids, the
   general equivalence conjectured and the authors stating their
   proofs "cannot be extended beyond our stated conditions" (Remark
   2.12, PDF p. 10); several numerical observations proven only in
   the companion follow-up paper (ref. [23], PDF pp. 11, 26); zero
   empirical content, no L2 data anywhere; check for a published
   version before formal citation. No queue change.

Counterfactual (what this paper would have killed if we had done it
wrong): without the library-is-ammunition caveat, the "transaction costs
can calm fire sales and reduce everyone's costs" result (PDF pp. 10-12,
24) would have entered the C8 macro-synthesis as a licensed market
property — a policy-flavored structural claim from a two-agent
model-internal statement on an idealized block book with declared zero
spread and invented parameters. Without the estimator-configuration
freeze, the game-form knob would launder sign structure post hoc: the
same convex kernel predicts buy-only behaviour for one agent (Remark
2.11) and oscillating hot-potato behaviour for two (Theorem 2.7), so any
observed L2 oscillation could be "explained" by assuming two agents and
any absence by assuming one, the assumption chosen after the fact — the
pre-declaration discipline exists so the programme can never occupy that
position. Without the grain-association caution, the odd/even-N
sawtooth of Figure 4 would be reproducible "alternating structure" at
fine sampling, a pure simulation artifact elevated to a market property.
Without the laundering discipline, the CFTC-SEC hot-potato magnitudes
(49 percent of volume on roughly 200 net contracts in 14 seconds, PDF
pp. 1-2) would sit in a claim as programme evidence, when they are a
single-day, single-venue regulatory quote usable only as motivation,
never as support.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (26 PDF pages, abstract, body, both proof
  sections, all six figures, references complete; nothing skipped).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read;
  docs/DECISIONS_PENDING.md is NOT touched by this session; T1 remains
  armed awaiting the owner's word in its booked state; T2 tested-fail); the
  blocked list stays blocked. Deep-read queue pointer: next UNREAD
  "Multivariate self-exciting jump processes with applications to
  financial data" (x7a86fb, score 20, tenth of the score-20 tier,
  verified note-less this session against the live listing) — re-read the
  live tail and recompute the tier against the notes before consuming.
  The edition-12 cadence counter stands at ONE of five by this landing
  (#99), counted from the edition-12 reset at ## 130 (the next synthesis
  pass due at five or more deep-reads since edition 12).
- Byte-landed log note (session-specific): this session assembled the
  log locally from the live main copy plus these two entries and will
  byte-verify the pushed branch copy against the assembled local copy
  (md5 match) before opening the PR, per the PR #289 convention and the
  ## 123 root-cause record. The write path this session is the
  connector push (branch off live main head, full-file contents
  byte-checked), used because the local execution environment exposes
  no git CLI or credentials this cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit; the CI jobs run
over the pushed tree and must be verified green on both jobs before
merge.

## 132. Null-time session 110 (2026-11-23): library deep-read session 100 — the Eyjolfsson-Tjøstheim multivariate self-exciting jump-process read, tenth of the score-20 tier; the 2021 SDE-intensity self/cross-excitation class whose marks (not just counts) drive the intensity and whose mark law may depend on the pre-jump intensity level, whose moment-only stability conditions, analyst-threshold event definition, magnitude-fed excitation model form, in-sample daily-index fit and S&P-leads-Nikkei likelihood comparison reinforce already-queued families and move NOTHING; NO kill line moved; NO new candidate sharpening

The paper defines a d-dimensional self/cross-exciting point process whose
intensity vector solves dλ(t) = µ(t,λ(t))dt + BdU(t), with U_k(t) summing
the non-negative marks of past events so a large jump excites more than a
small one, and the jump-size law ν_k(λ,·) allowed to depend on the
pre-jump intensity value λ(t−) (eqs. 1, 3-4, Definition 1, PDF pp. 3-4);
geometric ergodicity is proved via the extended generator and a
Foster-Lyapunov drift through piecewise-deterministic-process theory and
Meyn-Tweedie (Theorem 1, PDF pp. 4-7), the linear model's stability
reducing to the symmetric part of M(λ) = A + BJ(λ) with J carrying only
the first mark moment plus boundedness of the first two mark moments
(Assumption 2, Propositions 3-4, PDF pp. 8-11) and closed moment and
autocovariance forms under intensity-free mark laws (Propositions 5-7,
PDF pp. 11-13). The application extracts jumps as daily S&P 500 and
Nikkei 225 log-returns above a fixed 0.025 threshold (PDF p. 14), fits
eight bivariate variants by MLE split over all/positive/negative jumps
(Table 1, PDF pp. 14-16), and finds the nonlinear extension — with
mean-reversion speed depending on the intensity norm, a built-in regime
change (PDF p. 15) — best by a handful of in-sample log-likelihood points
(LL −1662 vs −1667 all jumps, PDF p. 16), with stronger cross-excitation
from the S&P into the Nikkei than vice versa (b21 > b12), strongest for
negative jumps, and jump sizes growing with intensity but flattening at
the highest S&P intensities (Figures 4-5, PDF pp. 18-19). Read in full
(22 page-marked PDF pages, abstract, body, all seven propositions, both
lemmas, both theorems, all five figures, Table 1 and the references
complete) against the one question. Note landed at
paper/research/library/2026-11-23_multivariate_self_exciting_jump_processes_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail (edition 12, written at ## 130); the session's work
choice is the DEFAULT deep-read (next UNREAD triage entry, re-ranked
against the notes: the score-20 tier holds fourteen entries per the live
edge_triage_scores.json, nine consumed — through xc495e3 at ## 131 — so
this read takes x7a86fb tenth, verified note-less against the live
listing). Synthesis cadence: ONE of five already counted by #99 at
## 131; this landing makes TWO of five, so no synthesis pass is due.

Verdict: NO kill line changes. NO new candidate sharpening. Findings (all
graded against the queue as it stands at fifty-one candidates plus probe
E1):

1. [reinforcing, no new item] Stability verdicts in the marked
   self-exciting family are provably moment-bounded outputs: every linear
   stability condition passes through M(λ) = A + BJ(λ) carrying only the
   first mark moment, plus bounded first-two-moment regularity (Lemma 1,
   Assumption 2, Propositions 3-4, PDF pp. 8-10) — the same
   moment-bounded/law-sensitive split the queued moment-equivalence
   disclosure (#51, deep-read 93) freezes at the gate; a moment-matched
   null in this family certifies as stable while its mark law is
   arbitrary. The queued item already carries the case. No queue change.
2. [interpretation caution] The point process is manufactured by an
   analyst threshold: a jump is |daily log-return| above a fixed 0.025,
   unvaried across two series with different volatility (PDF p. 14), and
   every excitation, cross-excitation and lead-lag statement downstream
   is conditional on that event definition; the analogue in C1-L2/C8 work
   is any episode definition embedding a free constant, which the
   estimator-configuration freeze (deep-read 63) already binds as frozen
   configuration. Recorded as context. No queue change.
3. [interpretation caution] Excitation here carries event MAGNITUDE, not
   counts (U_k(t) sums the marks, eq. 3, PDF p. 4), so a marked model is
   a different process object from a count-only Hawkes on the same
   event set, and the mark-feeding convention plus the sign-splitting of
   the fits (all/pos/neg separately, Table 1, PDF p. 16) are model-form
   knobs that change what any future branching-ratio-shaped estimate
   means; covered by the frozen estimator identity of the
   estimator-configuration freeze and the level-versus-memory
   disambiguation (deep-read 59). No queue change.
4. [reinforcing, no new item] The mark law's dependence on the pre-jump
   intensity (Definition 1, PDF p. 4; fitted growth of jump sizes and
   variability with intensity, Figures 4-5, PDF pp. 18-19) is the
   regime-dependence class the self-excitation regime-window
   pre-declaration (deep-read 53) and the moment-equivalence disclosure
   (#51) already force into the open; printed reinforcement of the
   law-sensitive output class. No queue change.
5. [source-quality note] arXiv v1 theory preprint (math.PR, zero
   citations recorded in the index) with an in-sample fitting
   demonstration, not an empirical study: two daily index series, eight
   nested forms compared by in-sample log-likelihood (gains of a handful
   of points, Table 1, PDF pp. 15-16), no out-of-sample validation, no
   standard errors, no residual diagnostics, one hand-set threshold, no
   limit-order-book content; the headline conclusions (nonlinear best,
   S&P leading, crisis clustering with faster mean reversion) are
   daily-grain in-sample likelihood comparisons and enter the record only
   as ammunition; check for a published version before formal citation
   (the companion energy paper ref. [12] is journal-published, PDF p. 21;
   this paper shows no journal stamp). No queue change.

Counterfactual (what this paper would have killed if we had done it
wrong): without the estimator-configuration freeze, the 0.025 threshold
would be a tunable event definition — the same series re-threshed yields
a different point process and possibly a different cross-excitation sign,
unseen because the threshold looks like a data-cleaning constant.
Without the moment-equivalence disclosure, a moment-matched generative
null in this family would be certified stable by exactly this paper's
moment-only theory while its intensity-dependent mark law silently
diverged in precisely the law-sensitive outputs no moment audit touches.
Without the regime-window pre-declaration and level-versus-memory
disambiguation, the nonlinear model's built-in regime change
(mean-reversion speed depending on the intensity norm, PDF p. 15, fitted
strongest for negative Nikkei jumps, PDF p. 18) shows a "crisis regime"
can be a model-form property assumed by the analyst inside a
self-exciting model, not a measured market state — an L2 spec could
"find" regimes its own kernel convention had put there. Without the
laundering discipline, the S&P-leads-Nikkei contagion direction (b21 >
b12, PDF pp. 17-18) would enter C8's macro-synthesis as a licensed
cross-market asymmetry, when it is an in-sample likelihood comparison on
two daily index series under one self-selected threshold.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (22 PDF pages, abstract, body, both
  theorems, both lemmas, all seven propositions, all five figures, Table
  1, references complete; nothing skipped).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read;
  docs/DECISIONS_PENDING.md is NOT touched by this session; T1 remains
  armed awaiting the owner's word in its booked state; T2 tested-fail); the
  blocked list stays blocked. Deep-read queue pointer: next UNREAD
  "Risk-Sensitive Compact Decision Trees for Autonomous Execution in
  Presence of Simulated Market Response" (x7e576d, score 20, eleventh of
  the score-20 tier, verified note-less this session against the live
  listing) — re-read the live tail and recompute the tier against the
  notes before consuming. The edition-12 cadence counter stands at TWO of
  five by this landing (#100), counted from the edition-12 reset at ## 130
  (the next synthesis pass due at five or more deep-reads since
  edition 12).
- Byte-landed log note (session-specific): this session assembled the log
  locally from the live main copy (fetched over the connector, md5-matched
  against the restored main tarball copy byte-for-byte before appending)
  and will byte-verify the pushed branch copy against the assembled local
  copy (md5 match) before opening the PR, per the PR #289 convention and
  the ## 123 root-cause record. The write path this session is the
  connector push (branch off live main head, full-file contents
  byte-checked), used because the local execution environment exposes
  no git CLI or credentials this cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit; the CI jobs run over the pushed tree and
must be verified green on both jobs before merge.

## 133. Null-time session 111 (2026-11-23): library deep-read session 101 — the Vyetrenko-Xu risk-sensitive compact decision tree read, eleventh of the score-20 tier; the 2019 ICML execution-agent paper whose market response to the agent's own aggressive orders is synthesized inside a historical-replay LOB simulator by an analyst impact rule (a single threshold CMI plus a KL-tuned parameter set), whose risk parameter sweeps the learned policy from all-passive to all-aggressive, and whose headline 32%-cost-saving figure is graded by the same simulator its benchmark was tuned in — execution-strategy engineering that reinforces existing freezes and moves NOTHING; NO kill line moved; NO new candidate sharpening

The paper sets order execution over a parent order as an infinite-horizon MDP
(remaining position plus discretized LOB state variables as states, a binary
passive-limit versus aggressive-market child placement as action, execution
yield against the parent-arrival mid as reward, Section 3.1, PDF pp. 4-5,
eq. 4), trains it inside a LOB replay simulator where queue position and
cancellations are unobserved and must be assumed (a pre-set cancellation
convention, a historical latency profile, always-filled aggressive orders,
zero impact for passive joins, Section 2.1, PDF pp. 3-4), synthesizes the
market response to the agent's own aggressive orders with a single-threshold
impact rule (below CMI the simulated book diverges from history until the
next historical aggressive trade in the agent's direction or next adverse
move, eqs. 2-3, PDF p. 4), tunes simulator parameters by minimizing a KL
divergence between historical and simulated benchmark cost distributions
(eq. 1, PDF p. 4), learns with tabular risk-sensitive Q-learning in the
Mihatsch-Neuneier transform framework (U_beta on the TD error, eqs. 11-14,
PDF p. 6) plus eligibility traces, uses Dantzig-regularized LSPI only for
feature selection (Section 3.3, PDF pp. 6-7), and renders the tabular policy
as a decision tree by Hunt's algorithm (Section 4.2, PDF p. 7). Results on
one liquid futures contract: sweeping beta from 0 to 1 moves the learned
policy monotonically from all-passive (highest yield, highest variance) to
all-aggressive (lowest expectation, lowest variance), Figure 3, PDF p. 7;
the chosen decision-tree policy reports 32% execution-cost savings at a 27%
increase in cost standard deviation, computed entirely in-simulator against
a simulator-tuned benchmark, Figure 6, PDF pp. 7-8. Read in full (10
page-marked PDF pages, header and disclaimer block, body, all six figures,
references complete) against the one question. Note landed at
paper/research/library/2026-11-23_risk_sensitive_compact_decision_trees_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail (edition 12, written at ## 130); the session's work choice
is the DEFAULT deep-read following the pointer set at ## 132: the score-20
tier holds fourteen entries per the live edge_triage_scores.json, ten
consumed through x7a86fb at ## 132, so this read takes x7e576d eleventh,
verified note-less against the live tree. Synthesis cadence: this landing
makes THREE of five counted from the edition-12 reset at ## 130 (## 131, ##
132, this session); no synthesis pass is due.

Verdict: NO kill line changes. NO new candidate sharpening. Findings (all
graded against the queue as it stands at fifty-one candidates plus probe
E1):

1. [reinforcing, no new item] The paper's own stated hazard — training on
   historical replay without agent-market interaction is unrealistic
   (Section 1.3, PDF p. 3) — is the reflexivity-of-evaluation class the
   library-is-ammunition rule already carries: an evaluation inside an
   environment whose response law was fit to the same data is an
   in-environment statement, not a market statement; the entire results
   section (Figure 6, PDF pp. 7-8) is ammunition, never evidence. The
   existing rule carries the case. No queue change.
2. [interpretation caution] The impact law is analyst-manufactured with a
   free threshold and assumed conventions: response eqs. 2-3 carry the
   single parameter CMI, and the simulator parameter set psi (queue
   cancellation convention, latency profile, fill assumptions) is KL-tuned
   against benchmark cost distributions (Section 2, PDF pp. 3-4); every
   policy learned there is conditional on (CMI, psi), the simulator
   analogue of the frozen estimator-configuration freeze (deep-read 63).
   Recorded as context. No queue change.
3. [interpretation caution] The risk parameter beta is a preference
   constant chosen by trader's risk appetite (Section 4.1, PDF p. 7) and
   silently selects the qualitative policy shape (all-passive at beta=0 to
   all-aggressive at beta=1, Figure 3, PDF p. 7); the frozen-constants rule
   is the existing guard should any future design ever carry such a knob.
   No queue change.
4. [cost-survival ammunition] The simulator assumptions are a checklist a
   future K7-style cost-survival or execution-feasibility layer must carry
   explicitly (unobserved queue position and cancellation convention,
   latency by time of day, immediate top-level fills, zero passive-join
   impact, the divergence splice of eq. 3, Section 2.1, PDF pp. 3-4); a
   cost estimate produced under any of these silently asserts them.
   Relevance only if such a layer exists. No queue change.
5. [source-quality note] arXiv v2 q-fin.TR (revised 2021-01-06), ICML 2019
   PMLR header, zero citations in the index, ten pages, one instrument, the
   headline 32% saving an in-simulator comparison against a simulator-tuned
   benchmark, no out-of-sample or live confirmation, LSPI convergence
   flagged unguaranteed by the authors themselves (Section 3.3, PDF pp.
   6-7), and the J.P. Morgan disclaimer stating the paper is not its
   research (PDF p. 1). Ammunition only; check the published PMLR version
   before formal citation. No queue change.

Counterfactual (what this paper would have killed if we had done it wrong):
without the library-is-ammunition rule, the 32% figure (Figure 6, PDF p. 8)
would enter the record as empirical support for execution-adjacent claims,
when the policy was graded by the same simulator whose impact law and
benchmark were tuned to the same history — a closed loop that cannot fail
visibly from inside. Without the estimator-configuration freeze, CMI and the
psi conventions would look like data-cleaning constants while they are the
model's degrees of freedom: re-set the cancellation convention or latency
profile and a different tree descends from the same history, indistinguishable
by any external test. Without the frozen-constants rule, a beta-shaped risk
parameter would select the policy's qualitative character before any market
evidence arrived, leaving no visible fingerprint. And for C8: the paper
manufactures multi-agent "other participants" entirely from a single-agent
history plus an assumed response law, which is why any macro-synthesis input
phrased as "markets respond as if..." must be traced to a measured response
or marked as an assumed law, or the synthesis inherits simulator assumptions
dressed as market facts.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (10 PDF pages, header and disclaimer, body,
  all six figures, references complete; nothing skipped).
- Ratification queue after this session: FIFTY-ONE candidate sharpenings
  plus probe E1, zero armed (NONE queued by this read;
  docs/DECISIONS_PENDING.md is NOT touched by this session; T1 remains
  armed awaiting the owner's word in its booked state; T2 tested-fail); the
  blocked list stays blocked. Deep-read queue pointer: next UNREAD "Càdlàg
  semimartingale strategies for optimal trade execution in stochastic
  order book models" (x150a2c, score 20, twelfth of the score-20 tier,
  verified note-less this session against the live listing) — re-read the
  live tail and recompute the tier against the notes before consuming. The
  edition-12 cadence counter stands at THREE of five by this landing
  (#101), counted from the edition-12 reset at ## 130 (the next synthesis
  pass due at five or more deep-reads since edition 12).
- Byte-landed log note (session-specific): this session assembled the log
  locally from the public main archive (fetched as the repository tarball,
  restored whole) and will byte-verify the pushed branch copy against the
  assembled local copy (md5 match) before opening the PR, per the PR #289
  convention and the ## 123 root-cause record. The write path this session
  is the connector push (branch off live main head, full-file contents
  byte-checked), used because the upgraded local execution environment
  exposes no git CLI or GitHub credentials this cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit; the CI jobs run over the pushed tree and
must be verified green on both jobs before merge.

## 134. Null-time session 112 (2026-11-23): library deep-read session 102 — the Ackermann-Kruse-Urusov càdlàg-semimartingale execution read, twelfth of the score-20 tier; the 2020/2021 pure-theory paper that extends the block-LOB execution family to stochastic depth and stochastic resilience, characterizes minimal costs through a quadratic BSDE over càdlàg semimartingale strategies, and proves twice in print that the conventional finite-variation bookkeeping conventions become catastrophically ill-posed (unbounded negative costs, constant positive parameters) the moment the admissible strategy class widens — ONE new candidate sharpening queued (the strategy-class/convention well-posedness pre-declaration), PENDING OWNER RATIFICATION; NO kill line moved

The paper sets optimal execution over a stochastic block order book:
price impact gamma > 0 follows d(gamma) = gamma(mu d[M] + sigma dM) (eq. 1,
PDF p. 2), resilience rho is progressively measurable, an execution
strategy is ANY cadlag semimartingale with X_{t-} = x and X_T = 0 (both
directions, infinite variation, jumps = block trades), the price deviation
solves dD = -rho D d[M] + gamma dX + d[gamma,X] (eq. 2 — the covariation
term is the paper's own adjustment, PDF p. 2), and expected costs are
J = E[int D- dX + int (gamma/2) d[X]] (eq. 3, PDF p. 3 — the quadratic-
variation term is the second adjustment; both derived as discrete-time
limits, Appendix A, PDF pp. 42-44, with the discrete recursion motivating
the BSDE, Appendix B, PDF pp. 44-47). Under 2rho + mu - sigma^2 > 0 and a
[0,1/2]-valued BSDE solution, the value function is
V_t(x,d) = (Y_t/gamma_t)(d - gamma_t x)^2 - d^2/(2 gamma_t)
(Theorem 3.4(i), PDF p. 10), an optimal strategy exists IFF the process
beta-tilde from (14) admits a cadlag semimartingale version
(Theorem 3.4(ii)-(iii), PDF pp. 10-11), and it is then explicit (eq. 18).
The two counterexamples carry the bite: with CONSTANT positive gamma and
rho in (0, 1/T) — parameters that pass every pointwise sign condition in
the impact-viability family — the conventional cost functional ~J (6)/(20)
has ess inf = -inf over semimartingale strategies (scaled Brownian
strategies nu*W with nu -> inf, Section 4.1, PDF pp. 13-14), and even with
the right J the conventional dynamics (24) without d[gamma,X] again give
J -> -inf once gamma is itself stochastic (scaled-GBM strategies,
Section 5.1, PDF pp. 15-17); with both corrections the problems are
well-posed and the optima explicit (Sections 4.2, 5.2, PDF pp. 14-15,
18-19). Section 6: optimal strategies can have infinite variation even
when ALL exogenous processes are smooth (Example 6.1, PDF pp. 20-21); a
jump only in the drift mu of gamma forces a block trade inside (0,T)
(Example 6.2, PDF pp. 21-22, Figure 2, PDF p. 23); NEGATIVE resilience —
the paper's own reading: self-exciting behaviour where the large
investor's trading stimulates other market participants to trade the
same direction (PDF p. 22) — makes oversell-then-flip-to-buying optimal
by design (Example 6.3, PDF pp. 23-24, Figure 3, PDF p. 24); and an
optimum can fail to exist while the value function stays finite
(Example 6.4, PDF p. 25, infinite-variation mu). Section 7, Section 8
and Appendix C prove BSDE existence and the comparison 0 <= Y <= 1/2
(Propositions 7.1, 7.3, C.1, PDF pp. 26-29, 49-50). Read in full (53
page-marked PDF pages, abstract, body, counterexamples, examples, proofs,
both appendices, references complete; nothing skipped) against the one
question. Note landed at
paper/research/library/2026-11-23_cadlag_semimartingale_optimal_execution_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail (edition 12, written at ## 130); the session's work
choice is the DEFAULT deep-read following the pointer set at ## 133: the
score-20 tier holds fourteen entries per the live edge_triage_scores.json,
eleven consumed through x7e576d at ## 133, so this read takes x150a2c
twelfth, verified note-less against the live tree. Synthesis cadence: this
landing makes FOUR of five counted from the edition-12 reset at ## 130
(## 131, ## 132, ## 133, this session); no synthesis pass is due.

Verdict: NO kill line changed; ONE new candidate sharpening queued, PENDING
OWNER RATIFICATION. Findings (all graded against the queue as it stands at
fifty-one candidates plus probe E1 at session start):

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   strategy-class/convention well-posedness pre-declaration: BEFORE the L0
   gate, any C1-L2/C8-adjacent comparator, null, cost model, simulator or
   refutation instrument that defines a cost, objective or "optimality"
   statement must pre-declare, as frozen configuration counted in the
   multiplicity ledger, (i) the admissible process/strategy class over
   which the written definition is posed, and (ii) a recorded
   well-posedness statement for the pairing of that class with the chosen
   bookkeeping convention (boundedness-below over the declared class, or
   the dated limiting derivation that produced the convention), with every
   deviation a dated amendment before the data is touched; an objective
   computed under a convention whose well-posedness over the declared
   class was never established fails at the gate, and any comparison
   resting on it is dead by rule. The paper proves the failure class is
   real twice with no empirical content: constant positive (gamma, rho)
   passing every pointwise sign condition still give ess inf ~J = -inf
   over semimartingale strategies (Section 4.1, PDF pp. 13-14), and the
   corrected J with the conventional dynamics again diverges once gamma
   is stochastic (Section 5.1, PDF pp. 15-17) — while the corrected
   pairings ((3) with (2)) are well-posed, each correction forced by the
   discrete-time limit (Appendix A, PDF pp. 42-44). Harder-to-pass because
   a comparator whose cost bookkeeping is inherited from a narrower class
   than the one it simulates or optimizes over — today survivable as a
   silent convention producing finite numbers while its own objective's
   infimum diverges — now fails at the gate BEFORE any data is touched,
   where no queued rule asks the question: the estimator-implementation
   concordance rule (deep-read 85) audits code against the written
   definition and passes a wrong-pairing definition; the impact-viability
   pre-declaration (deep-read 87) checks pointwise sign conditions and
   passes both counterexamples; the transform-domain rule (#50) covers
   transform existence domains, not bookkeeping conventions. Tightens the
   concordance rule (deep-read 85) by extending the audit from
   implementation-vs-definition to definition-vs-admissible-class, and
   joins the impact-viability pre-declaration (deep-read 87) and the
   dynamics-identification rule (null-time session 58) in the
   generative-null pre-declaration family. Killed-if-wrong counterfactual
   in the session note.
2. [reinforcing, no new item] The paper's corrections are forced, not
   chosen: both adjustment terms ((gamma/2)d[X] and d[gamma,X]) are
   derived as discrete-time limits (Appendix A, PDF pp. 42-44), the paper
   states in print that the conventional forms "can result in an
   ill-posed optimization problem" (PDF p. 4), and the conventional forms
   recover exactly in the finite-variation special case (PDF p. 4). The
   estimator-implementation concordance rule (deep-read 85) already
   carries the implementation-vs-definition half; finding 1 extends it to
   the class pairing. No further queue change.
3. [interpretation caution] Existence is not implied by finiteness: a
   finite value function can coexist with NO optimal strategy (Example
   6.4, PDF p. 25), with existence routed through the
   semimartingale-version property of beta-tilde (Theorem 3.4(ii), PDF
   pp. 10-11); any future comparator or baseline referencing "optimal"
   model behavior must carry an existence statement or it references a
   vacuous object. Recorded as context. No queue change.
4. [interpretation caution] Negative resilience self-excitation
   re-encodes sign-alternation as optimal design: the paper's explicit
   reading of rho < 0 is self-exciting behaviour where the large investor
   stimulates same-direction trading (PDF p. 22), inside which
   oversell-then-buy-back is optimal with beta > 1 forcing 1-beta negative
   (Example 6.3, PDF pp. 23-24) — a measured sign-alternating flow pattern
   is not itself diagnostic of any mechanism when the assumed
   impact/resilience law can make it optimal, the same
   conditional-on-the-law shape as the price-process-family invariance
   rule (deep-read 66). No queue change.
5. [source-quality note] arXiv v2 [math.PR] revised 2021-07-26, 53 PDF
   pages, zero citations in the index, pure theory with no data (Figures
   1-3 are simulations of the paper's own theorems, PDF pp. 19, 23, 24),
   referee acknowledgement (PDF p. 50), companion discrete-time study
   self-cited as arXiv:2006.05843 (PDF p. 50); a refereed published
   version likely exists, check it before formal citation. No queue
   change.

Counterfactual (what this paper would have killed if we had done it
wrong): without finding 1's pre-declaration, a future C8 comparator or
generative null borrowing a cost convention from the finite-variation
execution literature — the family the queue already cites for the
impact-viability conditions — and then simulating or optimizing over a
wider process class would produce finite single numbers while its own
objective's infimum is -inf over exactly that class, with constant
positive parameters that pass every pointwise condition, the divergence
living only in the infimum so no computed value shows it; a claimed
refutation or cost comparison resting on such a number would be
manufactured by the convention with no visible fingerprint. And without
the queued disambiguation family, a sign-alternating optimal-looking
flow pattern in a model with a negative-resilience component would read
as detected manipulation-type behaviour when Example 6.3 proves it is
simply optimal inside the assumed law.

- Inaccessible/blocked status: none this session. The extract was present,
  page-marked and read in full (53 PDF pages, header, body, both
  counterexamples, all examples, proofs, both appendices, the comparison
  appendix and references complete; nothing skipped).
- Ratification queue after this session: FIFTY-TWO candidate sharpenings
  plus probe E1, zero armed (ONE queued by this read — the
  strategy-class/convention well-posedness pre-declaration;
  docs/DECISIONS_PENDING.md IS updated by this session accordingly; T1
  remains armed awaiting the owner's word in its booked state; T2
  tested-fail); the blocked list stays blocked. Deep-read queue pointer:
  next UNREAD "Measuring tail risk at high-frequency: an L1-regularized
  extreme value regression approach with unit-root predictors"
  (xf959b8, score 20, thirteenth of the score-20
  tier, verified note-less this session against the live listing) —
  re-read the live tail and recompute the tier against the notes before
  consuming. The edition-12 cadence counter stands at FOUR of five by
  this landing (#102), counted from the edition-12 reset at ## 130 (the
  next synthesis pass due at five or more deep-reads since edition 12).
- Byte-landed log note (session-specific): this session assembled the log
  locally from the public main archive (fetched as the repository tarball,
  restored whole; the local copy byte-verified against the fetched
  branch copy by md5 before appending) and will byte-verify the pushed
  branch copy against the assembled local copy (md5 match) before opening
  the PR, per the PR #289 convention and the ## 123 root-cause record.
  The write path this session is the connector push (branch off live main
  head, full-file contents byte-checked), used because the upgraded local
  execution environment exposes no git CLI or GitHub credentials this
  cycle.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit; the CI jobs run over the pushed tree and
must be verified green on both jobs before merge.

## 135. Null-time session 113 (2026-11-23): GOALS.md G2 executed — the queue fully briefed: the G2 item-41 brief extended in the same product to items 41 through 52, the count reconciliation extended to fifty-two, all FIFTY-TWO queued sharpenings plus probe E1 now carry sitting-ready briefs

Session-state note (director step, per docs/goal_autonomy_protocol.md,
edition 12, ACTIVE, consistent with the live tail at ## 134): the
declared work choice is the edition-12 guidance's ranked non-deep-read
item — "the G2 brief for item 41 remains the ranked choice" — chosen
over the lawful deep-read floor for rotation freshness (the last four
landed sessions, ## 131 through ## 134, were all deep-reads; rotation
rule point 3 discourages another consecutive read when a ranked
alternative stands). The same G2 product lawfully extends through the
last unbriefed item: briefs summarize already-recorded proposals with
their sources, and items 42-52 are as recorded as item 41; writing the
item-41 brief alone would leave the doc internally inconsistent (a
sitting could not batch-ratify families holding unbriefed members).
The synthesis cadence is NOT due: the edition-12 counter stands at
FOUR of five (deep-reads 99-102 landed ## 131-## 134); no pass runs
this session, and the next work-selecting session that lands a fifth
deep-read opens with the pass before its read. Race checks at the
choice: live main fetched and verified (log 929,723 chars, tail
"## 134", zero "## 135" on main), zero open PRs at the check.

Work, all inside the standing order's carve-outs (notes and
bookkeeping; nothing armed, nothing measured, nothing trades live):

- docs/DIRECTORATE_BRIEFS.md (G2 refresh, the queue's batch-ratify
  reading material): items 41-52 briefed, each with its join order,
  its queuing log entry, the library note holding the full draft, the
  one-paragraph mechanism, and the sitting's accept/reject question —
  B10 the noise-model pre-declaration for de-noised inputs (41st,
  ## 100, Clinet–Potiron parametric-noise plug-in read: the de-noising
  functional form moves the residual-noise share from ~0% to 20-30% of
  variance with nothing changed but the form); B11 the
  feature-normalization pre-declaration (44th, ## 110, the
  Zheng–He–Yang cross-exchange read: rolling normalizations whose
  windows are never stated, unauditable from the text); B12 the
  estimator-implementation concordance rule (46th, ## 113, the
  Bugaenko read: Eq. 20 defines a signed mean while Algorithm 1 clips
  every negative response to zero); B13 the model-inversion
  identifiability pre-declaration (49th, ## 120, the Guo–Swishchuk–
  Rémillard read: one observed scalar split between two unknowns
  through an analyst-supplied constant — information created by the
  split); B14 the transform-domain admissibility pre-declaration
  (50th, ## 121, the Zamora Font VIX-options read: evaluations outside
  the transform's proven domain are undefined by rule, silent finite
  numbers fail the concordance audit); B15 the moment-equivalence
  disclosure (51st, ## 122, the Gao–Zhou–Zhu dark-pool read: mean fill
  outputs are moment-bounded while same-mean mark laws produce
  systematically different fill-rate outputs — a moment-matched audit
  certifies only the moment-bounded half); B16 the
  strategy-class/convention well-posedness pre-declaration (52nd,
  ## 134, the Ackermann–Kruse–Urusov read: conventional bookkeeping
  goes ill-posed (infimum −∞) the moment the declared strategy class
  widens, the divergence living only in the infimum so no computed
  value shows it); D5 the queue-jump-diffusion generative-null
  pre-declaration (42nd, ## 107, the Cont–de Larrard read: liquid-book
  queues are fluctuation-dominated, a depletion-side drift could be
  pure diffusion); F8 the same-period-aggregate feature availability
  rule (45th, ## 112, the Deng–Zhou read: a feature built from
  period aggregates is available only at the period's close); F9 the
  cross-stream synchronization and single-source-count pre-declaration
  (48th, ## 118, the Cheng–Yang–Zou Polymarket read: merge timeline,
  imputation, desync tolerance and a source-overlap map against the
  mirrored Long/Short double-count, proven in print on all four axes);
  H2 the residual-flow attribution null (43rd, ## 108, the
  Donier–Bonart million-metaorder read: impact is the square root of
  the TOTAL market imbalance, the market does not detect individual
  metaorders — episode attribution must survive the
  aggregate-conditioned subsample); H3 the impact-viability
  pre-declaration for generative nulls (47th, ## 115, the
  Alfonsi–Infante Acevedo read: a canonical published impact family
  is internally arbitrageable in computable parameter regions, and no
  other queued rule catches the impact layer). Family placements
  follow each item's own recorded "tightens" pointer: B10-B16 join the
  estimator-discipline family (its intro and sitting question updated
  from nine to sixteen members); D5 joins the admission-null family
  (its sitting question updated); F8-F9 join the
  measurement/manipulation family (its sitting question updated);
  H2-H3 join the dynamics-identification family (its question updated
  to the three-part binding ask). The count reconciliation is extended
  and closes exactly at fifty-two (the 41-52 join list: ## 100, ##
  107, ## 108, ## 110, ## 112, ## 113, ## 115, ## 118, ## 120, ##
  121, ## 122, ## 134), with the protocol-vs-tail supersession note
  extended (the edition-12 facts block said FIFTY-ONE at ## 129; the
  tail and DECISIONS_PENDING say FIFTY-TWO). Probe E1 re-checked,
  unchanged, standing separately. NOTHING invented, NOTHING queued,
  NOTHING armed; every brief cites its log entry and note.
- docs/GOALS.md surgical edits, two, status bookkeeping with zero
  ranking action: (1) the front-2 NOTE refreshed — the edition-12
  counter stated at ONE of five by the ## 130 refresh was stale
  against the ## 131-## 134 landings and now reads FOUR of five (the
  next read landing makes FIVE and the successor session opens with
  the pass), and the "briefs owed from item 41" sentence is discharged
  (all fifty-two briefed, item 52 as B16, next refresh owed from item
  53, none queued yet); (2) the G2 STATUS refresh note appended with
  the twelve item-to-family placements, and the FEEDS line's queue
  count corrected from FIFTY-ONE to FIFTY-TWO. Nothing gated was
  touched; the protocol's section 2 remains the ranking authority.

Ratification queue after this session: FIFTY-TWO candidate sharpenings
plus probe E1, zero armed — UNCHANGED from the ## 134 landing; briefs
queue nothing. docs/DECISIONS_PENDING.md is NOT touched this session.
T1 remains armed awaiting the owner's word in its booked state
(survived all five kill lines with sign inverted; T2 tested-fail); the
blocked list stays blocked. Deep-read queue pointer: unchanged — next
UNREAD "Measuring tail risk at high-frequency: an L1-regularized
extreme value regression approach with unit-root predictors" (xf959b8,
score 20, thirteenth of the score-20 tier, verified note-less by the
## 134 session), then the last of the score-20 tier; re-read the live
tail before consuming. NOTE for the successor: this landing keeps the
edition-12 counter at FOUR of five; if the successor runs a deep-read,
that landing makes FIVE and the NEXT session after it opens with the
synthesis pass (edition 13) before its read.

Byte-landed log note (session-specific): this session assembled the log
locally from the public main archive (fetched as the repository tarball,
restored whole; the local copy byte-verified against the fetched
branch copy by md5 before appending) and will byte-verify the pushed
branch copy against the assembled local copy (md5 match) before
opening the PR, per the PR #289 convention and the ## 123 root-cause
record.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit; the CI jobs run over the pushed tree and
must be verified green on both jobs before merge.

## 136. Null-time session 114 (2026-11-23): library deep-read session 103 — the Hambuckers-Sun-Trapin L1-regularized extreme-value regression read, thirteenth of the score-20 tier; the 2023 dynamic-GPD conditional-tail paper whose shape and scale ride lagged liquidity/volatility covariates, whose unregularized MLE provably cannot control t-test size under local unit-root predictors (printed false-positive selection near 1.0 for inactive unit-root covariates, standard errors non-computable on its own nine-stock data) and whose out-of-sample K-S test rejects its own model on three of nine mega-liquid stocks — ONE new candidate sharpening queued (the conditional-tail covariate-integration pre-declaration), PENDING OWNER RATIFICATION; NO kill line moved

The paper sets dynamic peaks-over-threshold at the 5-minute grid: negative
returns against a rolling 90%-quantile threshold u_t over twelve window
lengths from one week to twelve weeks (PDF p. 13), exceedances fitted to a
GPD with time-varying shape k_t bounded 0 < k_t < 0.5 by logit link "to
ensure a finite conditional variance" (eq. 3, PDF p. 3) and log scale with
an autoregressive term plus lagged covariates (eq. 4, PDF pp. 3-4). The
mechanism core: with local unit-root predictors the MLE remains consistent
but its limit is NON-NORMAL (Theorem 2, PDF p. 6), and three printed
reasons make t-test covariate selection inadmissible (uncontrollable
type-I, severe size distortion selecting unit-root predictors, low power
for shape coefficients, PDF pp. 6-7); the remedy is a two-step adaptive
L1-regularized MLE with the oracle property for both stationary and local
unit-root predictors (Theorem 4, PDF p. 9), tuned by AIC/HQ/BIC (PDF p. 7).
Simulations: t-tests select truly INACTIVE unit-root covariates at rates
"much higher than α = 0.05 ... regardless of the DGP" (PDF p. 11), printed
at essentially 1.0 in Table 2's false-positive columns while ALMLE+BIC
achieves near-perfect correct selection (Table 2, PDF p. 14). Empirics:
nine liquid US stocks, all transactions January 2006 to December 2014, 42
liquidity/volatility predictors; headline: tail SEVERITY strongly
associated with LOW price impact in periods of high volatility of
liquidity and volatility of volatility (conclusion verbatim, PDF p. 21),
Amihud-type impact coefficients −0.91 to −1.79 on most of the nine stocks
(Table 5, PDF p. 17), sign-stable for the shape equation. The MLE
comparison: 39-42 of 42 shape predictors and 43 of 43 scale predictors
"selected", Fisher information not positive definite so standard errors
not computable, "variable interpretation very difficult if not
impossible" (Tables 7-8, PDF pp. 19-20; PDF p. 16). Out-of-sample VaR:
coverage near nominal by construction (threshold is the rolling 90%
quantile) while the K-S test rejects the regression model on three of nine
stocks at 1% (GE 2.68e-12, XOM 6.32e-8, HD 0.0023, BA 0.0431 at the 5%
edge; Table 9, PDF p. 21). Read in full (~24 page-marked PDF pages,
header, body, theory, simulations, all printed tables, appendix tables,
references complete; nothing skipped) against the one question. Note
landed at
paper/research/library/2026-11-23_l1_regularizer_extreme_value_regression_deep_read.md.

Director step (goal-autonomy protocol, ACTIVE): protocol read, consistent
with the live tail (edition 12, written at ## 130); the session's work
choice is the DEFAULT deep-read following the pointer set at ## 135 (the
## 135 session ran the G2 briefs refresh, a non-deep-read, so the counter
carried forward): the score-20 tier holds fourteen entries per the live
edge_triage_scores.json, twelve consumed through x150a2c at ## 134, so
this read takes xf959b8 thirteenth, verified note-less against the live
tree. Synthesis cadence: this landing makes FIVE of five counted from the
edition-12 reset at ## 130 (## 131, ## 132, ## 133, ## 134, this
session); the NEXT work-selecting session opens with the synthesis pass
(edition 13) BEFORE its read. Race checks at the choice: live main
fetched and verified (the ## 135 tail confirmed as the live tail, zero
"## 136" on main before this append).

Verdict: NO kill line changed; ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION. Findings (graded against the queue as it
stood at fifty-two candidates plus probe E1 at session start):

1. [candidate sharpening, PENDING OWNER RATIFICATION] The conditional-tail
   covariate-integration pre-declaration: BEFORE the L0 gate, any
   C1-L2/C8-adjacent conditional extreme-value model (GPD/POT tail
   regression, time-varying tail-shape or tail-scale spec, any
   covariate-conditioned exceedance or severity model) must pre-declare,
   as frozen configuration counted in the multiplicity ledger: (i) the
   integration order of every candidate covariate (I(0), I(1),
   local-to-unit-root), declared before estimation, with local unit-root
   covariates flagged and their coefficients read under the local √T
   standardization (PDF pp. 4-5) rather than as ordinary fixed-parameter
   estimates; (ii) the covariate-selection procedure as frozen
   configuration, with t-test selection from an unregularized
   conditional-tail likelihood INADMISSIBLE by rule; and (iii) any
   regularized selection's tuning criterion (AIC/HQ/BIC/other) frozen
   with the penalty set, never silently re-tuned per instrument.
   Harder-to-pass because a conditional-tail covariate claim riding on
   unregularized t-statistics — today survivable as an ordinary
   regression finding — now fails at the gate BEFORE any data is touched,
   and the paper proves the failure class real three times over: the
   non-normal MLE limit under local unit-root predictors so t-statistics
   have no controlled meaning (Theorem 2, PDF p. 6; three inadmissibility
   reasons, PDF pp. 6-7), false-positive selection of truly inactive
   unit-root covariates at rates up to essentially 1.0 rather than the
   nominal 0.05 (PDF p. 11; Table 2, PDF p. 14), and on the paper's own
   data the unregularized MLE selecting 39-43 of 43 predictors with a
   Fisher information matrix not positive definite, standard errors not
   computable, interpretation "very difficult if not impossible" (Tables
   7-8, PDF pp. 19-20; PDF p. 16). No queued rule asks the question:
   the estimator-implementation concordance rule (deep-read 85) audits
   implementation against definition, not the selection procedure's size;
   the estimator-configuration freeze (deep-read 63) freezes the
   estimator's configuration, not selection-method admissibility; the
   pre-registration family (primary-metric pre-commitment, deep-read 55;
   base-rate confrontation; regime-window pre-declaration) freezes
   metrics and windows, not covariate order classes. Tightens the
   concordance rule (deep-read 85) and joins the estimator-configuration
   freeze (deep-read 63) and primary-metric pre-commitment (deep-read 55)
   in closing a researcher degree of freedom that alone can manufacture
   a finding. Killed-if-wrong counterfactual in the session note.
2. [interpretation caution] The shape bound 0 < k_t < 0.5 is imposed
   a priori "to ensure a finite conditional variance" (PDF p. 3): the
   family cannot express heavier-than-finite-variance tails, and any
   conditional-tail estimate through it is conditional on that support
   bound; coefficients on local unit-root predictors are local-to-zero
   order (PDF pp. 4-5), a categorically different object from stationary
   significance. Context only. No queue change.
3. [interpretation caution, cost-survival ammunition] Even with oracle
   selection, 42 covariates and nine mega-liquid stocks, the
   out-of-sample K-S rejects the conditional GPD on three of nine at 1%
   (GE 2.68e-12, XOM 6.32e-8, HD 0.0023, BA 0.0431 at the 5% edge; Table
   9, PDF p. 21) while coverage sits near nominal by construction
   (rolling 90% quantile threshold, PDF p. 13): the printed honest
   ceiling of the conditional-tail genre at exactly the grain C8 would
   work; no "passes everywhere" expectation may be assumed into any
   future C8 kill line. The severity-vs-low-impact headline (Table 5,
   PDF p. 17; conclusion, PDF p. 21) is descriptive ammunition for the
   C8 covariate shortlist (impact, vol-of-liquidity, vol-of-vol) and
   NEVER program evidence: conditional association, one asset class,
   in-sample, bounded shape, rejected on a third of its own universe.
   No queue change.
4. [reinforcing, no new item] The MLE comparison carries the
   estimation-discipline case whole (39-43 of 43 "selected", signs
   flipping stock to stock, standard errors non-computable, Tables 7-8,
   PDF pp. 19-20; PDF p. 16), and the all-positive autoregressive
   log-scale term (Table 8, PDF p. 20) is the level-persistence habit
   the level-versus-memory disambiguation rule (deep-read 59) already
   guards. No queue change.
5. [source-quality note] arXiv v1 [econ.EM], 3 Jan 2023, zero citations
   in the index; Table 2 (PDF p. 14) reports DGP 5/DGP 6 rows while the
   simulation section defines exactly four DGPs ("four data generating
   processes", PDF p. 9; DGP 1-4, PDF p. 10) with no DGP 5/6 definition
   anywhere in the text — an internal inconsistency; check the published
   version before formal citation. No queue change.

Counterfactual (what this paper would have killed if we had done it
wrong): without finding 1, a future C8 covariate screen is exactly the
paper's MLE comparison — 42 candidate covariates, nearly all
"selected", signs unstable instrument to instrument, no computable
standard errors, and a printed false-positive rate for persistent
covariates at essentially 1.0 — a liquidity-covariate "discovery"
manufactured by the selection procedure with no visible fingerprint in
the outputs; the matched-control and estimator-discipline design avoids
precisely this. Without the library-is-ammunition rule, the nine-stock
severity headline would enter the programme record as a market fact
about low impact and unstable liquidity fattening tails, when it is a
conditional association through a bounded-shape model that its own
out-of-sample test rejects on three of its own nine instruments.

- Inaccessible/blocked status: none this session. The extract was
  present, page-marked and read in full (~24 PDF pages, header, body,
  theory, simulations, all printed tables, appendix tables, references
  complete; nothing skipped).
- Ratification queue after this session: FIFTY-THREE candidate
  sharpenings plus probe E1, zero armed (ONE queued by this read — the
  conditional-tail covariate-integration pre-declaration;
  docs/DECISIONS_PENDING.md IS updated by this session accordingly; T1
  remains armed awaiting the owner's word in its booked state; T2
  tested-fail); the blocked list stays blocked. Deep-read queue
  pointer: next UNREAD "The adaptive nature of liquidity taking in
  limit order books" (x1e5f02, Taranto-Bormetti-Lillo 2014,
  arXiv:1403.0842v2, score 20, FOURTEENTH AND LAST of the score-20
  tier, verified note-less this session against the live listing) —
  once it lands the tier is consumed and the pointer recomputes against
  the full score-sorted file; re-read the live tail and recompute the
  tier against the notes before consuming. The edition-12 cadence
  counter stands at FIVE of five by this landing (#103), counted from
  the edition-12 reset at ## 130: the NEXT session opens with the
  synthesis pass (edition 13) BEFORE its read.
- Byte-landed log note (session-specific): this session assembled the
  log locally from the public main archive (fetched as the repository
  tarball, restored whole) and appends this entry to that
  byte-verified copy, pushing the four changed files (note, log,
  GOALS.md, DECISIONS_PENDING.md) in ONE commit to main via the
  connector push, per the ## 123 root-cause record. No git or gh CLI
  exists in this environment, so the CI green-check cannot be verified
  from this channel; the landing commit must be confirmed on GitHub.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit.

## 137. Null-time session 115 (2026-11-23), first act: the eleventh synthesis pass — the cadence recomputed from the edition-12 reset at ## 130 (deep-reads 99-103 landed at ## 131 through ## 136, ## 135 the G2 briefs refresh interleaved and non-counting, the window CLOSED at five of five per the ## 136 closing pointer, which directed the pass run before the read, against the clean tail), goal state rewritten as EDITION 13, the G2 brief-debt recomputed against the standing queue (briefs cover fifty-two of fifty-three; the item-53 brief executed as this session's second act, ## 138), the edition-12 zero-floor expectation corrected by the record (TWO sharpenings in the window: #52 at ## 134, #53 at ## 136; declining-yield holds ABOVE floor, not at it); NO sharpening queued by the pass

Session-state note (director step, per docs/goal_autonomy_protocol.md,
edition 13, ACTIVE, written by this pass and consistent with the live
tail at ## 136): the declared work choice is the CADENCE RULE's own
instruction — the ## 136 closing pointer directed the next session to
open with the synthesis pass before its read, and the counter stood at
FIVE of five, so the pass runs FIRST as this session's first act. The
pass's work-selection guidance (edition 13, section 2) then ranks the
session's second act: the G2 item-53 brief over the lawful deep-read
floor, for rotation freshness (the ## 136 landing was a deep-read;
rotation rule point 3 discourages consecutive reads when a ranked
alternative stands — the same reasoning session 113 recorded at
## 135), and because a directorate sitting cannot batch-ratify
families holding unbriefed members (item 53 is unbriefed at pass time).
Race checks at the choice: live main fetched and verified (head at this
session's start = the ## 136 landing commit 55531e3, tail "## 136",
zero "## 137" on main).

The pass re-read the live record through the clean tail (## 1 through
## 136) and recomputes the edition-12 window: deep-reads 99-103 landed
at ## 131, ## 132, ## 133, ## 134 and ## 136 (## 135 the G2 briefs
refresh, bookkeeping, non-counting); ZERO kill lines moved in the
window; TWO sharpenings queued in it — #52 the strategy-class/convention
well-posedness pre-declaration (deep-read 102, ## 134) and #53 the
conditional-tail covariate-integration pre-declaration (deep-read 103,
## 136) — correcting the edition-12 floor reading in its strict form:
the score-20 tier did NOT return reinforcing reads only, and the
queue's declare-before-the-data vein was NOT fully extended; both new
items extend that same vein, but each names a mechanism class no queued
rule asked (an objective convention whose infimum diverges over the
wider admissible strategy class; covariate integration orders whose
local unit-root asymptotics make t-test selection structurally
inadmissible). The declining-yield expectation named at editions 3-12
holds in yield but NOT at a zero floor; the tier's one remaining entry
(x1e5f02) is the standing read. The window WAS infrastructure-clean:
no new truncation, corruption or collision instance anywhere in
## 131 through ## 136, all landings byte-verified against their
assembled local copies per the PR #289 convention; the write-side
~64K truncation class (five instances: ## 75, ## 78, ## 94, ## 98,
## 123) and the collision history (four events: ## 98, ## 105, ## 109,
## 123) stand unchanged; the byte-monotonicity/verification
infrastructure gap stays the ranked infrastructure item,
candidate-improvement status only, now extended with one recorded
channel limitation: the verification loop's CI step (gh run list) is
unexecutable from the current session channel (no gh CLI; the landing
lands through the connector push and the commit check is owner-side
work, recorded at ## 136).

Products of this pass, traveling only through the sanctioned channels:
(1) goal state rewritten whole as EDITION 13 (protocol section 2,
edition rule; the section 18 note records the change) — facts block
recomputed from the live record at ## 136 (queue FIFTY-THREE plus
probe E1 at pass time, zero armed, unchanged by the pass; one hundred
and five library note files through deep-read 103), ranked fronts
unchanged in order with statuses recomputed, the deep-read pointer
recomputed by title-matching the score-sorted triage file against the
live tail and the library listing (the score-21 tier CLOSED at ## 116,
## 118 and ## 119; the score-20 tier OPEN with THIRTEEN of its
FOURTEEN entries consumed — xaace1f ## 120, x2b0051 ## 121, x47bbb5
## 122, xe1c4ca ## 125, xf8b5bc ## 126, x97b372 ## 127, x55e853
## 128, x999a87 ## 129, xc495e3 ## 131, x7a86fb ## 132, x7e576d
## 133, x150a2c ## 134, xf959b8 ## 136; next UNREAD x1e5f02, "The
adaptive nature of liquidity taking in limit order books,"
Taranto-Bormetti-Lillo 2014, the tier's LAST entry — once it lands the
tier is CLOSED and the pointer recomputes to the score-19 tier, five
entries, head x03aa07 "How does latent liquidity get revealed in the
limit order book?"), cadence: RESET by this edition, the counter
standing at ZERO of five, the successor session's read #104 counting
as the window's first; (2) docs/GOALS.md status board refreshed to
edition 13 (operative bookkeeping only; the protocol's section 2 stays
the ranking authority); (3) work-selection guidance for the second act
(the G2 item-53 brief, executed as ## 138) and for the successor (the
read-back verification helper remains the ranked non-deep-read choice
after the briefs close to fifty-three; the deep-read remains the
floor). The pass measures nothing, arms nothing, launders nothing
INTO any spec, and queues NO sharpening; the G2 item-53 brief debt is
named and paid by the second act (## 138) under this edition's
guidance.

- Inaccessible/blocked status: none this act (the live protocol, log,
  GOALS.md, DECISIONS_PENDING.md and the triage file all read clean and
  whole; the briefs doc read clean).
- Ratification queue after this act: FIFTY-THREE candidate sharpenings
  plus probe E1, zero armed — UNCHANGED by the pass (the pass queues
  nothing; docs/DECISIONS_PENDING.md is untouched by this session
  entirely, the second act being a G2 brief which grades nothing);
  T1 remains armed awaiting the owner's word in its booked state; T2
  tested-fail; the blocked list stays blocked. Deep-read queue
  pointer: unchanged — next UNREAD "The adaptive nature of liquidity
  taking in limit order books" (x1e5f02, Taranto-Bormetti-Lillo 2014,
  score 20, FOURTEENTH AND LAST of the score-20 tier, verified
  note-less at ## 136), then the score-19 tier recomputes (five
  entries, head x03aa07) — re-read the live tail before consuming.
  The edition-13 cadence counter stands at ZERO of five (next pass due
  when five or more deep-reads have landed since edition 13).
- Byte-landed log note (session-specific): this session continues the
  ## 136 local-assembly convention (log assembled locally from the
  public main archive, restored whole; the landing is one connector
  push per act, files byte-verified against the assembled local copies
  before pushing), per the ## 123 root-cause record. No git or gh CLI
  exists in this environment: the CI green-check stays unverifiable
  from this channel and is recorded as owner-side work; the landing
  commits must be confirmed on GitHub.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit.

## 138. Null-time session 115 (2026-11-23), second act: GOALS.md G2 executed under the edition-13 guidance — the item-53 brief landed: the conditional-tail covariate-integration pre-declaration briefed as B17 (53rd, queued ## 136 by null-time session 114's deep-read 103), the count reconciliation extended to fifty-three, all FIFTY-THREE queued sharpenings plus probe E1 now carry sitting-ready briefs

Session-state note (director step, per docs/goal_autonomy_protocol.md,
edition 13, ACTIVE, written by this session's first act): the declared
work choice is the edition-13 pass's OWN ranked guidance for the
second act — the G2 item-53 brief — chosen over the lawful deep-read
floor for rotation freshness (the ## 136 landing was a deep-read;
rotation rule point 3 discourages another consecutive read when a
ranked alternative stands — the same reasoning session 113 recorded
at ## 135), and for sitting-readiness (a directorate sitting cannot
batch-ratify families holding unbriefed members; item 53 stood
unbriefed). The work is pure bookkeeping inside the standing order's
carve-outs: the brief summarizes an already-recorded proposal with
its sources; it invents nothing, queues nothing, and arms nothing.

Work:

- docs/DIRECTORATE_BRIEFS.md (G2 refresh, the queue's batch-ratify
  reading material): item 53 briefed as B17 — the conditional-tail
  covariate-integration pre-declaration (53rd in join order, queued
  ## 136 via deep-read 103 / null-time session 114; full draft in log
  ## 136 and the library note
  paper/research/library/2026-11-23_l1_regularizer_extreme_value_regression_deep_read.md;
  one-paragraph mechanism: any conditional extreme-value model must
  pre-declare every candidate covariate's integration order and use
  a frozen covariate-selection procedure in which t-test selection
  from an unregularized conditional-tail likelihood is inadmissible,
  because the Hambuckers-Sun-Trapin paper prints the unregularized
  MLE's non-normal limit under local unit-root predictors, selection
  of truly inactive unit-root covariates at rates of essentially 1.0,
  and its own MLE selecting 39-43 of 43 covariates with standard
  errors non-computable; the sitting's accept/reject question: is B17
  accepted into the estimator-discipline B-family as the standing
  covariate-side discipline for any future conditional tail model, or
  does it duplicate an existing member) — placed in the B-family
  (estimator discipline), extending it to seventeen items, the family
  intro and sitting question updated; the count reconciliation
  extended to fifty-three (one join at log entry ## 136, closing
  exactly); the header refresh paragraph and the tail refresh
  paragraph record this session; the "How to read" queue count updated
  to fifty-three; the probe-E1 section head updated to "not counted in
  the fifty-three", probe E1 re-checked, unchanged, standing
  separately.
- docs/GOALS.md surgical edits, two, status bookkeeping with zero
  ranking action: (1) the front-2 NOTE refreshed at the pass (## 137)
  already states the item-53-brief-as-second-act choice; (2) the G2
  STATUS refresh note appended with the B17 placement, the
  fifty-three count reconciliation, and the next refresh owed from
  item 54 (none queued yet).

Ratification queue after this act: FIFTY-THREE candidate sharpenings
plus probe E1, zero armed — UNCHANGED by this session (the pass queues
nothing; the brief queues nothing). docs/DECISIONS_PENDING.md is NOT
touched this session. T1 remains armed awaiting the owner's word in
its booked state (survived all five kill lines with sign inverted; T2
tested-fail); the blocked list stays blocked. Deep-read queue
pointer: unchanged — next UNREAD "The adaptive nature of liquidity
taking in limit order books" (x1e5f02, Taranto-Bormetti-Lillo 2014,
arXiv:1403.0842v2, score 20, FOURTEENTH AND LAST of the score-20 tier,
verified note-less at ## 136), then the score-19 tier recomputes
(five entries, head x03aa07 "How does latent liquidity get revealed in
the limit order book?") — re-read the live tail before consuming. The
edition-13 cadence counter stands at ZERO of five: the successor
session's read #104, whenever it lands, counts as the window's first.
With the briefs closed to all fifty-three, the edition-13 guidance's
next ranked non-deep-read choice for a preferring session is the
read-back verification helper; the deep-read remains the floor.

Byte-landed log note (session-specific): this session continues the
## 136 local-assembly convention (log assembled locally from the
public main archive, restored whole; the landing is a single
connector push covering both acts, files byte-verified against the
assembled local copies before pushing), per the ## 123 root-cause
record. No git or gh CLI exists in this environment: the CI
green-check stays unverifiable from this channel and is recorded as
owner-side work; the landing commit must be confirmed on GitHub.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit.

## 139. Null-time session 116 (2026-11-24): library deep-read session 104 — the Taranto-Bormetti-Lillo adaptive liquidity-taking read, fourteenth AND LAST of the score-20 tier, which the landing CLOSES; the 2014 asymmetric-liquidity dissection whose mechanical-impact decomposition (penetration probability times half-gap, validated) pins efficiency restoration on taker volume adaptation with quote revision REINFORCING the move, whose trade-time-vs-physical-time inversion separates the 2004-LSE and 2009-NASDAQ efficiency-recovery scales, and whose model proves the diffusivity of simulated prices to be a function of the agents' predictor — public DAR(p) bounds it to lags below the predictor window, private metaorder-aware gives it at all scales — ONE new candidate sharpening queued (the generative-null agent information-set pre-declaration), PENDING OWNER RATIFICATION; NO kill line moved

Session-state note (director step, per docs/goal_autonomy_protocol.md,
edition 13, ACTIVE, consistent with the live tail at ## 138): the
declared work choice is the DEFAULT deep-read following the pointer set
at ## 137 — the edition-13 counter stands at ZERO of five, this read is
#104 and counts as the window's first, and rotation is fresh (## 137 and
## 138 were the synthesis pass and the G2 item-53 brief, both
non-reads); no ranked non-deep-read alternative stands ahead of it
(the edition-13 guidance ranks the read-back verification helper for a
non-deep-read-preferring session only after the briefs closed at
## 138, and the deep-read remains the floor). Race checks at the
choice: live main fetched and verified (head ca44a55, tail "## 138",
zero "## 139" on main). Channel note: the verification loop's CI step,
recorded as owner-side work at ## 136 through ## 138, is now PARTIALLY
executable from this channel via the unauthenticated GitHub API — the
CI run at the ## 138 landing commit reads "completed, success" (both
jobs; the deploy workflow failed at the deploy step, the same
transient class that failed twice before and self-recovered on
subsequent runs; the next docs-triggered deploy, including this
session's, is the recovery channel) — recorded here as the CI
verification of the ## 136 and ## 137-138 landings finally in hand.

The paper sets asymmetric liquidity, after Lillo-Farmer, as the
reconciliation of persistent order flow with efficient prices, and
dissects it on four mega-liquid stocks (AZN, VOD full LOB LSE 2004;
AAPL, MSFT NASDAQ Jul-Aug 2009; small- and large-tick pairs, Table 1,
PDF p. 7): a DAR(500) sign predictor (Table 2 and Appendix A, PDF
pp. 8, 37-39), returns split into mechanical and quote-revision
components (PDF p. 13), the mechanical impact approximated as
penetration probability times half the opposite gap (eq. 3, validated
against all four stocks, PDF pp. 14, 17-18, Figure 8). Printed
mechanism: rising correctness of the sign prediction drops the
penetration probability — takers adapt market order volume to the
outstanding opposite liquidity — with best-side volumes eroding then
refilling near the predictor extremes (Figures 4, 6, 7; PDF pp. 10-17),
and the quote revision acting in the SAME direction as the mechanical
impact at moderate correctness, vanishing at extreme correctness (PDF
pp. 17-19): providers reinforce rather than restore efficiency, and the
paper's own reading assigns the restoration to the taker. Transaction-
level inefficiency regions print for the NASDAQ stocks (eq. 4; MSFT
"clearly inconsistent with market efficiency", PDF p. 19), recovering
after s trades: AAPL 5 lags / 5.5 s, MSFT 11 / 18.7 s, AZN 1 / 23.1 s,
VOD 5 / 114.5 s — the 2009 NASDAQ market needs more trade lags but less
physical time than 2004 LSE, "high frequency trading decreases the
physical time needed to restore efficiency in the market, but it might
increase the trade time" (PDF p. 22). The modeling half: the Toth et
al. (2011) construction recovers diffusivity only below the
limit-order lifetime and under unrealistically low cancellation rates,
where its conditional volume profile takes the wrong sign versus data
(PDF pp. 23-26, Figure 11); the adaptive fix makes the beta exponent of
the volume fraction f a function of correctness, penetration
probability α(1−ε·ε̂), and the reduced return model r = A(ε−ε̂)+η exactly
efficient and diffusive at all lags (eqs. 5-6, PDF pp. 26-29),
equivalent to the propagator model under the AR predictor (PDF
pp. 28-29). The load-bearing print: under the PUBLIC DAR(p) predictor
diffusivity holds only for lags below p (shown at p = 500 and p =
10000, Figure 13, PDF p. 34); under the PRIVATE metaorder-aware
predictor (the LMF continuation probability, eq. 9, PDF pp. 30-33)
diffusivity holds at all scales, by construction, insensitive to
parameters (Figure 12, PDF p. 33). Read in full (40 page-marked PDF
pages, header, body, all fourteen figures, the DAR(p) appendix,
references complete; nothing skipped; Figure 3's raw axis text
partially garbled in the extract, its content stated in the
accompanying text, PDF pp. 8-9) against the one question. Note landed
at
paper/research/library/2026-11-24_adaptive_liquidity_taking_deep_read.md.

Verdict: NO kill line changed; ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION. Findings (graded against the queue as it
stood at fifty-three candidates plus probe E1 at session start):

1. [candidate sharpening, PENDING OWNER RATIFICATION] The generative-
   null agent information-set pre-declaration: BEFORE the L0 gate,
   any C1-L2/C8-adjacent generative null, placebo, comparator or
   simulator whose simulated participants act on a decision rule fed
   by any input must pre-declare, as frozen configuration counted in
   the multiplicity ledger, for each simulated agent class: (i) the
   information set its rule consumes, every input marked PUBLIC
   (derivable from the public observables the null simulates) or
   PRIVATE (not so derivable: agent-internal state, metaorder
   continuation knowledge, the knowing-taker assumption), and (ii)
   which macro-level outputs of the simulation are claimed invariant
   to that marking and which are information-set-dependent, with every
   deviation a dated amendment before any data is touched. Harder-to-
   pass because a null whose agents silently consume private
   information today passes as an ordinary null while its produced
   macro properties are artifacts of the choice: the paper proves the
   failure class on its own model with nothing changed but the takers'
   predictor — public DAR(p) bounds simulated diffusivity to lags
   below the predictor window (Figure 13, PDF p. 34), private
   metaorder-aware restores it at all scales "by construction"
   (Figure 12 with text, PDF p. 33), the authors themselves marking the
   private predictor as "not typically of public domain" (PDF p. 32).
   No queued rule asks the question: the impact-viability
   pre-declaration (deep-read 87) audits impact-parameterization sign
   conditions, not agent knowledge; the dynamics-identification rule
   (null-time session 58) demands dynamics identified, not inputs
   declared; the queue-jump-diffusion pre-declaration (## 107)
   freezes null parameters, not agent inputs. Tightens the
   impact-viability pre-declaration (deep-read 87) and joins the B17
   conditional-tail item (deep-read 103) in closing a researcher
   degree of freedom that alone can manufacture a macro-level
   conclusion. Killed-if-wrong counterfactual in the session note.
2. [reinforcing, no new item] The impact decomposition — mechanical
   impact as penetration probability times half-gap (eq. 3, validated)
   with the quote-revision channel measured separately — is ammunition
   for the C8 mechanism shortlist, never program evidence, and the
   trade-time-vs-physical-time inversion of efficiency recovery
   (PDF p. 22) reinforces the queued flow-clock scale-constant
   discipline: cross-era comparisons must state their clock. No queue
   change.
3. [interpretation caution] The measurements assign efficiency
   restoration to the taker adaptation, with quote revision
   REINFORCING the price move at moderate correctness (PDF pp. 17-19);
   any C1-L2/C8 narrative assigning the restoration role to market
   makers must trace to a measured component, not an assumed law. No
   queue change.
4. [interpretation caution] The model's private predictor lets the
   simulated taker consume structurally defined non-public knowledge
   (her continuation law, PDF pp. 30-33): read jointly with finding 1 —
   private information in a simulator is not illegitimate, it is a
   load-bearing configuration that cannot be silent. No queue change.
5. [source-quality note] arXiv v2 [q-fin.ST] 11 Apr 2014, "Submitted
   to: JSTAT", 40 pages, zero citations in the index, four
   mega-liquid stocks across two venues and eras, the NASDAQ
   inefficiency regions self-flagged as regime-dependent and partly
   scarcely populated (PDF p. 15), and a DAR(p) estimation that
   smooths negative fitted coefficients with a ten-point moving average
   before zeroing them (Appendix A, PDF p. 39) — any reuse must carry
   that preprocessing; check the published JSTAT version before formal
   citation. No queue change.

Counterfactual (what this paper would have killed if we had done it
wrong): without finding 1, a future C8 generative null could claim "no
null reproduces the measured compression signal" while its simulated
takers silently ran on a private-information rule, or claim "a null
reproduces everything" while its agents ran on a truncated public
predictor — either conclusion manufactured by an undeclared agent
information set, the refutation carrying the artifact with no visible
fingerprint in the outputs. Without the mechanism-channel caution, the
paper's taker-side efficiency narrative would enter the record as a
market fact about who restores efficiency, when it is a four-stock
conditional association whose provider-side extension the authors
themselves leave as future work (PDF p. 37).

- Inaccessible/blocked status: none this session. The extract was
  present, page-marked and read in full (40 PDF pages, header, body,
  all fourteen figures, the DAR(p) appendix, references complete;
  nothing skipped).
- Ratification queue after this session: FIFTY-FOUR candidate
  sharpenings plus probe E1, zero armed (ONE queued by this read — the
  generative-null agent information-set pre-declaration;
  docs/DECISIONS_PENDING.md IS updated by this session accordingly; T1
  remains armed awaiting the owner's word in its booked state; T2
  tested-fail); the blocked list stays blocked. Deep-read queue
  pointer: the score-20 tier is now CLOSED (all fourteen entries
  consumed, the last being this read); the pointer recomputes against
  the full score-sorted file to the score-19 tier (five entries), next
  UNREAD "How does latent liquidity get revealed in the limit order
  book?" (x03aa07, score 19, first of the score-19 tier, verified
  note-less this session against the live listing; distinct from the
  session-3 Hiremath latent-regimes note) — re-read the live tail and
  recompute the tier against the notes before consuming. The
  edition-13 cadence counter stands at ONE of five by this landing
  (#104), counted from the edition-13 reset at ## 137. Directorate
  briefs: cover all items through 53 (## 138); the item-54 brief is
  owed before the next sitting, and is the ranked non-deep-read choice
  for a preferring session together with the read-back verification
  helper.
- Byte-landed log note (session-specific): this session continues the
  ## 136 local-assembly convention (log assembled locally from the
  public main archive, restored whole; the landing is one connector
  push, files byte-verified against the assembled local copies before
  pushing), per the ## 123 root-cause record. CI verification now
  partially executable from this channel via the unauthenticated
  GitHub API (recorded above); the deploy workflow's deploy-pages step
  is the remaining owner-side item. The landing commit must be
  confirmed on GitHub.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the assembled
full tree (main's tracked tree restored whole plus this session's changed
files) with marker sweep, library-provenance audit and encoding sanity
all exiting zero before commit.
## 140. Null-time session 117 (2026-11-24): library deep-read session 105 — the Kato optimal-execution-with-market-impact read, FIRST of the score-19 tier, consuming the TRUE tier head and correcting the ## 139 closing pointer's two errors (the tier was claimed to hold five entries with head x03aa07; the triage file holds SEVENTEEN entries at score 19 and the head is xc35349, both verified against the note register this session); the stochastic-control dissection proving the value function's behaviour at the time origin to be a function of the impact function's growth class alone — at-most-linear impact admits instantaneous block liquidation at strictly positive finite cost, superlinear impact forbids it — ONE new candidate sharpening queued (the impact growth-class pre-declaration), PENDING OWNER RATIFICATION; NO kill line moved

Session-state note (director step, per docs/goal_autonomy_protocol.md,
edition 13, ACTIVE, consistent with the live tail at ## 139): the
declared work choice is the DEFAULT deep-read — the edition-13 counter
stands at ONE of five (## 139, deep-read #104), this read is #105 and
counts as the second, and no ranked non-deep-read alternative stands
ahead of it (the item-54 directorate brief is owed before the NEXT
sitting, not this one; the sitting is owed its brief, the session is
owed its read). CORRIGENDUM, worked as this session's first act per the
honest-error protocol (## 139's text above stays unedited): the ##
139 closing pointer named "How does latent liquidity get revealed in
the limit order book?" (x03aa07) as first of a claimed FIVE-entry
score-19 tier. Recomputed live against the triage file and the note
register: the score-19 tier holds SEVENTEEN entries (xc35349, x88c3e6,
x3ba398, x70d4f8, x03aa07, xa911d0, x021d63, xf1e828, x201cd0,
x06003f, x62c427, x776d3c, x5eed77, x2e38f9, x4207fb, xf8425e,
x374d57), NONE with a deep-read note (all seventeen unread), and the
ritual's selection order — score descending, triage-file order
breaking ties, the same order the score-20 tier was consumed in —
makes xc35349 the true head. x03aa07 remains unread, fifth in the
tier order; the GOALS.md front-2 NOTE, a living refreshed block, is
corrected by this session's refresh. Race checks at the choice: live
main fetched and verified byte-true against the local tree (head
98f8de27, the ## 139 landing; tail "## 139"; zero "## 140" on main).
Channel note: CI on the ## 139 landing (98f8de27) verified "completed,
success" and the Deploy Salient site workflow "completed, success" on
the same head — both verified from the live API at the last session's
close; the unauthenticated GitHub API hit its 60-request rate limit at
this session's start, so this session's race checks and landing
verification run through the authenticated github_app channel, and
the post-push CI check is recorded honestly as partially executed if
the limit does not reset in time.

The paper: Kato, "An Optimal Execution Problem with Market Impact"
(arXiv:0907.3282v8, 36 pp., page-marked, read in full including both
examples, the sell-off section, the discrete-derivation appendix and
all of appendix B's proofs), the preprint of the Finance and
Stochastics publication (DOI 10.1007/s00780-014-0232-0, stated on the
extract, PDF p. 34). A single trader liquidates Phi shares under a
convex PERMANENT impact g(zeta) on a generic diffusion log-price, the
model derived as the discrete-to-continuous limit under condition [A]
(the per-step impact g_n C¹-matched to h(n·psi), Sec. 7, PDF pp.
14-16); the value function is continuous in every argument except the
time origin, where right-continuity is DECIDED BY THE GROWTH CLASS OF
g: h(infinity) = infinity (superlinear) makes no-trading optimal in
infinitesimal time and bounds liquidation proceeds in a vanishing
window to zero (Theorem 1(i), PDF p. 6; Lemma 9's explicit phi(r) -> 0,
PDF pp. 20-22), while h(infinity) < infinity (at-most-linear) makes the
value JUMP at t = 0 to J_u, the utility of selling any amount
instantly at the strictly positive discounted price e^{-h(infinity)
psi} (Theorem 1(ii) with the zeta^delta strategies (3.1), PDF p. 6);
uniqueness of the viscosity solution binds exactly in the
quadratic-or-faster class, lim inf h(zeta)/zeta > 0 (Theorems 2-4, PDF
pp. 6-8). The sell-off condition changes nothing in continuous time
(PDF p. 9). Examples: linear impact gives the exact block-sale value
w + (1-e^{-alpha·phi})/alpha · s attained arbitrarily fast, timing
flipping wholly with the drift sign (Sec. 5.1 with Remark 5, PDF
p. 11); quadratic impact makes the optimal schedule's FORM depend on
holdings against two thresholds — small holders finish, large holders
cannot finish at all within the horizon, the middle regime solved
only numerically (Theorem 2 of Sec. 5.2, Figures 1-4, PDF
pp. 11-13) — and the author's own conclusion concedes the model's
scope: real traders liquidate gradually despite concave empirical
impact, the missing piece being risk aversion or the transient
component, "we surmise another reason: the existence of a temporary
(or transient) impact" (Remark 2, PDF p. 5; Sec. 6, PDF p. 14).

Findings, graded (all page-cited in the session note,
paper/research/library/2026-11-24_kato_optimal_execution_market_impact_deep_read.md):

- ONE new candidate sharpening queued as the fifty-fifth, PENDING
  OWNER RATIFICATION: the impact growth-class pre-declaration —
  BEFORE the L0 gate, any C1-L2/C8-adjacent impact function (a
  generative null's, placebo's, comparator's, cost model's or
  simulator's, permanent or transient) must pre-declare as frozen
  configuration counted in the multiplicity ledger (i) its large-size
  growth class (at-most-linear / strictly superlinear /
  quadratic-or-faster) and (ii) for discrete-grain constructions, the
  rescaling defining its continuous-time limit (the condition-[A]
  class), with any instantaneous/block-liquidation-feasibility or
  vanishing-window-cost conclusion licensed only under the declared
  class. Mechanism: Kato proves the macro admissibility flip on one
  and the same admissible strategy class with nothing changed but the
  impact function's tail — the same auditor's test the ## 139 agent
  information-set item ran on the predictors, now run on the impact
  functional; the symbol statements binding which solution claims are
  well-posed (Theorem 4's quadratic class, PDF p. 8) also live on the
  undeclared datum. No queued rule asks it (impact-viability audits
  sign conditions, strategy-class well-posedness declares the process
  class but the flip is not a strategy-class effect, queue-jump
  freezes parameters, agent information-set marks inputs); tightens
  the impact-viability pre-declaration and joins the generative-null
  pre-declaration family.
- [reinforcing, no new item] Permanent-only impact is a declared
  exclusion with a printed converse: the author himself concedes the
  permanent-only model cannot reproduce observed gradual liquidation
  and surmises transient impact (PDF pp. 5, 14) — reinforces the
  transient-layer family's premise that the impact decomposition is
  a declared datum, not a default.
- [interpretation caution] Linear permanent impact carries no
  scheduling signal for a risk-neutral trader — the whole value is
  attained by instantaneous liquidation, timing flips wholly with
  the drift sign, mu-tilde = 0 makes every schedule identical
  (PDF p. 11): an impact-timing covariate grounded in a linear
  permanent spec is a drift reading in disguise.
- [cost-survival ammunition] The holdings-dependent regime structure
  (small holders finish, large holders cannot; thresholds Phi-hat 1,
  Phi-hat 2; middle regime numeric only, PDF pp. 11-13) blocks any
  "one cost curve" shortcut in a future K7-style cost layer.
- [source-quality note] The preprint states its own published version
  (Finance and Stochastics, DOI 10.1007/s00780-014-0232-0, PDF
  p. 34): the standing arXiv caution upgrades to "published version
  identified; cite it". Pure theory, no data, all examples
  Black-Scholes drift with risk-neutral utility.

Ratification queue after this session: FIFTY-FIVE candidate
sharpenings (fifty-four through ## 139 plus the impact growth-class
pre-declaration queued this session), plus probe E1, zero armed. T1
remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue: the score-19 tier holds seventeen entries,
one consumed (xc35349, this session); next UNREAD: "LOB-Impact
Benchmark: Emergent Market Impact in Generative Limit Order Books"
(x88c3e6, score 19, second of the tier, verified note-less this
session), then x3ba398 "The microstructural foundations of leverage
effect and rough volatility", then x70d4f8 "Price impact without
order book: A study of the OTC credit index market", then x03aa07
"How does latent liquidity get revealed in the limit order book?" —
re-read the live tail before consuming; the ritual's slug-keyed
unread rule applies, and the pointer-computation error that produced
the ## 139 five-entry claim is the recorded reason this entry states
the whole remaining tier order explicitly.

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit.
## 141. Null-time session 118 (2026-11-24): library deep-read session 106 — the Nigmatulin et al. LOB-Impact Benchmark read (x88c3e6), SECOND of the score-19 tier per ## 140's explicit tier order; a generative-LOB evaluation benchmark that injects execution-style metaorders into neural message models and grades the emergent impact through a fixed claim ladder with paired blind controls and physics-known kernel baselines — the neural panel's one repeated signature: an impact law always exists, is always the model's own (visible at least 3x the blind floor in all 25 model-stock cells), is never the square-root law (binned exponents 0.63-1.21, all 25 day-clustered intervals excluding 0.5; amplitudes Y = 2-50 against the empirical ~0.5) and never credibly relaxes (end-over-peak mostly above 1, the price still moving in the metaorder's direction after execution stops) — ONE new candidate sharpening queued (the intervention-attribution blind-arm pre-declaration), PENDING OWNER RATIFICATION; NO kill line moved

Session-state note (director step, per docs/goal_autonomy_protocol.md,
edition 13, ACTIVE, consistent with the live tail at ## 140): the
declared work choice is the DEFAULT deep-read — the edition-13 counter
stands at TWO of five before this read, no synthesis pass is due, and
no ranked non-deep-read alternative displaces the read (the item-54 and
item-55 directorate briefs are owed before the NEXT sitting, not this
session; the ## 140 precedent governs: the sitting is owed its brief,
the session is owed its read); this read is #106 and counts as the
third, and the read-back verification helper stays the ranked
non-deep-read choice for a preferring session. Race checks at the
choice: live main fetched and verified (head 7d74be68, the ## 140
landing; zero "## 141" on main; the local tree byte-true against
main's blobs, all four ## 140 files hash-matched at the last landing's
verification). Channel note: no gh CLI in the session channel again
this session; the landing verification and the CI check run through
the unauthenticated GitHub API (rate limit permitting), recorded
honestly as partially executed if the limit does not reset in time.

The paper: Nigmatulin, Mohl, Frey, Li, Marti-Shahandeh, Cucuringu,
Calinescu, Foerster and Zohren, "LOB-Impact Benchmark: Emergent Market
Impact in Generative Limit Order Book Models" (arXiv:2610.27100v1,
9 pp., page-marked, read in full including Table 3's all-five-stock
panel, the claim-ladder figure and the reference list; published
version identified on the extract: ICAIF '26 proceedings, ACM, DOI
10.1145/3858063.3858909, CC-BY 4.0, PDF p. 1). The benchmark takes any
message-level generator plus a per-stock LOBSTER calibration
(evaluation month January 2026 held out of training) and runs three
phases with two paired controls: free generation reading the flow
balance (the trade-sign memory gamma_flow against the mid-price Hurst
exponent H, persistent flow uncompensated by transient impact being "a
free lunch built into its own market", PDF p. 2); a 100-child build-up
metaorder injection (median-size aggressive children, participation
eta = 10% per the identity Delta_N = 9 phi, child count fixed a priori
at the empirical metaorder length, PDF p. 4) fitted as I = a*q^delta
with existence decided before magnitude — an identifiability test
validated by planted laws (downward bias at most 0.11, printed
exponents conservative) and 500 null trials with zero false laws (PDF
pp. 3-4); and a relaxation window in which injection stops and the
post-execution impact is read against the real market's one-half-to-
two-thirds decay and against kernel baselines whose physics is written
in (Propagator, Obizhaeva-Wang, closed-form end-over-peak 0.94 and
0.87, PDF p. 8). The blind control pairs every visible build-up: same
windows and seeds, the injected orders fill in the simulator's
plumbing while neither model input carries them, so the
visible-over-blind ratio attributes the response to the model itself
(C3's at-least-3x criterion, PDF p. 4; measured v/b 5.0-38, PDF
pp. 7-8). Panel: 13 models on 5 NASDAQ stocks, one per order-to-trade
cohort (4 replay baselines including the no-model kernels, 4
parametric generators, 5 neural SSM generators of 55M-120M parameters
sharing one eight-name corpus that contains four of the five
evaluation stocks, EA the flagged exception; Tables 1-2, PDF
pp. 4-5). Results: C2 and C3 pass in all 25 neural cells, C1, C4 and
C5 fail — the neural generators drift freely (-3 to -879 ticks),
their exponents sit above the square-root reference in every cell,
their amplitudes run four to a hundred times the empirical cost, and
the price keeps moving after execution stops, with the three lowest
end-over-peak descents riding the heaviest-drift rows ("the descent
is drift, not resilience", PDF p. 8). Two load-bearing prints for the
record: distributional scores do not rank response fidelity — the
rank correlation between LOB-Bench KS and |delta - 0.5| is unstable in
sign (+0.54 GOOG against -0.71 MSFT) and mostly negative within the
neural family, "the better mimic can sit farther from the impact law"
(PDF p. 8) — and book mechanics alone identify at delta = 0.73-0.81,
inside the learned range, "so the exponent cannot attribute the
response, and a large amplitude could be purely mechanical impact"
(PDF p. 2). The authors attribute the joint shape/relaxation failure
to insufficient replenishment under limited long-horizon memory,
"tentatively" (PDF pp. 1, 8), warn that such simulators "can reward
schedules that a real book would punish" (PDF p. 8), and fix the
repair direction: "learn replenishment rather than unlearn
persistence; killing flow memory would restore the balance vacuously"
(PDF p. 8). Everything at one operating point of one month of one
exchange; "a month atypical by about one within-month standard
deviation would already move the exponent past its half-width cap"
(PDF p. 9). Benchmark released open source (PDF p. 9).

Findings, graded (all page-cited in the session note,
paper/research/library/2026-11-24_lob_impact_benchmark_deep_read.md):

- ONE new candidate sharpening queued as the fifty-sixth, PENDING
  OWNER RATIFICATION: the intervention-attribution blind-arm
  pre-declaration — BEFORE the L0 gate, any C1-L2/C8-adjacent
  generative-null, placebo, comparator or simulator experiment whose
  readout includes the system's own response to an injected or
  experiment-side intervention must pre-declare, as frozen
  configuration counted in the multiplicity ledger, a blind
  attribution arm: runs identical to the visible runs in conditioning
  windows and seeds, in which the intervention executes in the
  simulator's plumbing (book reconstruction, matching, level
  consumption) but does not enter the model's inputs, with the
  response attributed through the visible-over-blind ratio under a
  margin fixed before the data — and every response conclusion
  (shape, magnitude, relaxation, reproduction or refutation of any
  mechanism claim) licensed only from runs that clear the declared
  blind floor; response conclusions from visible-only runs are
  unlicensed at the gate. Mechanism: the benchmark prints that book
  mechanics ALONE identify an impact law inside the learned range
  (replay kernels, no model inside, delta = 0.73-0.81 on AMD against
  the neural 0.66-0.93, PDF pp. 2, 7-8), so neither existence nor
  exponent nor amplitude separates plumbing from model, and only the
  paired blind arm does (C3, PDF p. 4). No queued rule asks the
  question (dynamics-identification demands flow-dynamics statistics,
  not intervention-response attribution; the residual-flow
  attribution null conditions aggregate flow out of real-data
  episodes, not plumbing out of simulator experiments; the agent
  information-set pre-declaration marks the agents' declared inputs,
  not the model's view of the experimenter's own injection;
  queue-jump freezes null parameters; impact growth-class declares
  the impact functional's tail); tightens the dynamics-identification
  rule for generative nulls on the intervention-response axis and
  joins the residual-flow attribution null in extending the
  attribution family from observational episode attribution to
  experimental response attribution, complementing the agent
  information-set pre-declaration whose declaration the blind arm
  operationalises from the experimenter's side.
- [reinforcing, no new item] Distributional realism licenses nothing
  about response and does not even rank it (the KS-vs-impact-error
  rank correlation unstable in sign across stocks, mostly negative
  within the neural family, "the better mimic can sit farther from
  the impact law", PDF p. 8) — reinforces the dynamics-identification
  rule's static-match-alone inadmissibility with a printed panel-wide
  mechanism.
- [reinforcing, no new item] The relaxation failure prints the
  transient-layer premise as a generator failure: persistent flow plus
  insufficient replenishment produces steep, non-relaxing,
  quasi-permanent emergent impact (no neural cell passes C5 anywhere;
  the C1 balance the benchmark enforces is the free-lunch check,
  PDF p. 2) — reinforces the impact-viability/transient-layer
  pre-declaration family (deep-read 87): a null missing the
  transient/replenishment component misprices every counterfactual
  response it is asked.
- [interpretation caution] Free drift is a first-class measurement
  confounder in generative nulls: every neural generator drifts
  freely (up to -879 ticks per rollout, PDF p. 7), the benchmark
  carries a three-part drift discipline (antisymmetrisation Eq. 2, a
  separate no-injection arm, an explicit C5 drift criterion, PDF
  pp. 2, 4), and the panel's three lowest descents ride the
  heaviest-drift rows, "the descent is drift, not resilience" (PDF
  p. 8) — any future symmetry- or response-based reading on a
  generative null must carry its drift arm.
- [interpretation caution] Exponent-type estimates are
  operating-point- and sample-fragile and only quotable behind an
  identification gate: one participation, one child size, one shape,
  one month of one exchange, "a month atypical by about one
  within-month standard deviation would already move the exponent past
  its half-width cap" (PDF p. 9); existence-before-magnitude validated
  by planted-law recovery and 500 zero-false-law null trials (PDF
  pp. 3-4) reinforces the frozen-configuration identifiability axis,
  and the operating-point fragility is the standing reading
  discipline for any exponent- or shape-like quantity the L2 phase
  may estimate from a single window.
- [cost-survival ammunition] Calibration survives in corpus and dies
  out of corpus (Y = 2-19 in-corpus against 12-50 on the
  out-of-corpus EA, "the OOD result does not destroy the law; it
  destroys its calibration", PDF p. 8), and such a simulator "can
  reward schedules that a real book would punish" (PDF p. 8) — a
  future cost layer or null comparator run cross-instrument must
  declare its calibration corpus against the evaluation universe.
- [source-quality note] arXiv v1, published version identified on the
  extract (ICAIF '26 proceedings, ACM, DOI 10.1145/3858063.3858909,
  CC-BY 4.0, PDF p. 1): the standing arXiv caution upgrades to
  "published version identified; cite it". Zero citations; the
  benchmark's authors largely overlap the evaluated generator
  family's authors (honest self-evaluation, criteria fixed in
  advance); pure methodology, the empirical anchors are literature
  citations, the measurements are of models, not markets.

Ratification queue after this session: FIFTY-SIX candidate
sharpenings (fifty-five through ## 140 plus the intervention-
attribution blind-arm pre-declaration queued this session), plus
probe E1, zero armed. T1 remains armed awaiting the owner's word; the
blocked list stays blocked. Deep-read queue: the score-19 tier holds
seventeen entries, two consumed (xc35349, ## 140; x88c3e6, this
session); next UNREAD: "The microstructural foundations of leverage
effect and rough volatility" (x3ba398, score 19, third of the tier,
verified note-less this session), then x70d4f8 "Price impact without
order book: A study of the OTC credit index market", then x03aa07
"How does latent liquidity get revealed in the limit order book?" —
re-read the live tail before consuming; the ritual's slug-keyed
unread rule applies, and ## 140's explicit remaining-tier order
remains the reference (unchanged by this session's consumption, the
stated order after x88c3e6 begins at x3ba398).

Nothing measured, no kill line moved, nothing armed, nothing trades
live. Guard clean: python3 src/integrity_guard.py run over the
assembled full tree (main's tracked tree restored whole plus this
session's changed files) with marker sweep, library-provenance audit
and encoding sanity all exiting zero before commit.
