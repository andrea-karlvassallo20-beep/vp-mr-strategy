# Null-time synthesis for owner review — the negative-knowledge map
# (the convergent findings of library deep-read sessions 1-24)

Written 2026-11-18, at the owner's request, as a SYNTHESIS NOTE: this
document rearranges what the deep-read notes already record; it makes
NO new claim, moves NO kill line, queues NO new candidate sharpening,
and measures nothing. Every finding below cites the deep-read note
(and through it, the source's PDF pages) where it was first recorded.
If anything here reads as an edge claim, it is a drafting error — the
library is ammunition, not evidence, and the program never trades
live. The owner's word governs everything: T1 is armed awaiting it,
the fourteen queued candidates await it, and this map exists to make
the owner's review of all three FASTER, not to replace it.

## Why this map exists

Twenty-four deep-read sessions against ONE question — *what here
would kill C1-L2 or C8 faster, or change their kill lines?* — have
produced zero new kill lines and fourteen queued sharpenings, but
they have also produced a noticeable CONVERGENCE: the papers keep
finding the same four failure modes by different routes. A successor
(or the owner) should not have to re-read 24 notes to see the shape.
The map is organized as: (1) the four convergent families, each with
its citations and its current queue/record status; (2) what each
family licenses and forbids for any future feature spec; (3) the open
territory the library has NOT mapped. Status language is the house
language: [rule armed], [queued, PENDING OWNER RATIFICATION],
[interpretation caution, recorded], [warrant, recorded].

## Family A — no free-standing readings

**Statement.** No fitted microstructure quantity is a property of
"the market." Every one is a property of a construction triple:
(feed x grain x construction), further entangled with regime. A
statistic read outside its declared construction is not merely
imprecise — it can invert.

**Convergent citations (first-recorded note; PDF cites within).**
- Branching ratio never read alone: per-branch rule [queued, PENDING
  OWNER RATIFICATION] — session 9 (Lee & Seo); joined by the
  exogenous-absorption caution — session 17 (12D compound Hawkes
  simulator), and THEORY-side by the MIHM identity (branching =
  transient-impact fraction in a martingale price) — session 20
  (Alfonsi & Blanc).
- Dispersion register [queued, PENDING OWNER RATIFICATION] —
  session 12 (Horst & Xu).
- Flow-clock scale-constant rule [queued, PENDING OWNER
  RATIFICATION] — session 8 (Bechler-Ludkovski dynamic OFI).
- Estimator-mode rule [queued, PENDING OWNER RATIFICATION] —
  session 11 (Bergault et al. price-aware AMMs).
- A fitted kappa (price resistance) is a book-state moment, moves
  with volatility [interpretation caution, recorded] — session 24
  (Ouazzani Chahdi et al.).
- Quantified demonstration that the SAME market yields materially
  different OFI series under one changed aggregation assumption
  (classic OFI out-of-sample 33-43 percent vs generalized
  construction 84-86 percent on CSI 500) — session 23 (Su et al.);
  aggregation endogeneity grain-dependent — session 18 (Takahashi
  SVAR-ITH); grain-specific moments — session 22 (Petukhina et al.).
- The delivery pipeline lives in the timestamps [interpretation
  caution, recorded]: arrival-timing structure at fine grains is a
  SUM of market and transport structure — session 19 (Maciejewski
  CME measurement).

**What Family A licenses for a future feature spec:** a statement of
feed, grain, construction, clock, and estimator mode in the spec
BEFORE any value is read; multiple readings of the same object where
branching/elasticity-type quantities appear; a transport-control
(book_snapshot_25 ground-truth) wherever arrival timing is
tail-relevant.
**What it forbids:** cross-grain or cross-venue comparison of a
statistic; citing a paper's fitted number as a property of the
program's venue, feed, or vintage; any "universal" reading.

## Family B — the book is not all intention

**Statement.** Passive depth carries manipulation-capable content
and moves the conditional price process itself. Depth is
causal-language territory, never a neutral regressor, never "just
liquidity."

**Convergent citations.**
- Depth-describes-never-ground-truths discipline, and C5's
  passive-withdrawal family as the ONLY legal route for causal
  language about passive flow [rule armed, in house rules]:
  reinforced quantitatively by session 21 (Fabre & Challet
  spoofability: deep, never-at-the-touch orders shift the predicted
  1-second mid-price distribution; 31 percent of large orders meet
  their spoofability criterion on one Coinbase week; top-of-book
  imbalance the worst-positioned to see it) and theoretically by
  session 24 (passive impact monotone, ~sqrt(participation), NO
  relaxation — passive placement moves the conditional price
  process in equilibrium).
- Round-number size clusters as a same-agent fingerprint
  [reinforcing, recorded for the queued wash-audit] — session 17
  (compound Hawkes simulator, null side) and session 21 (manipulator
  side).
- Cost-survival ammunition: manipulation-adjacent cost arithmetic
  must carry probabilistic fill/fee/liquidation-leg structure —
  session 21 (expected-cost template); flow-model declaration per
  the Poisson-mispricing rule — session 20.

**What Family B licenses:** treating depth features as descriptions
with entangled content, with the Layer 0 ground-truth check as the
separator; C5 routing for every causal sentence about passive flow.
**What it forbids:** pre-registering depth/imbalance as BONA FIDE
liquidity signals; top-of-book-imbalance logic imported as a
manipulation screen; any wash-audit or spoof-audit baseline that
ignores same-agent fingerprints.

## Family C — omissions manufacture signals

**Statement.** A wrong flow/price model does not merely fail — it
actively forges structure: Poisson flow admits parameter-free
(fictional) manipulation profits (session 20); a constant-information-
content propagator assigns passive flow the WRONG SIGN (session 24,
the sign-register rule [queued, PENDING OWNER RATIFICATION] via
session 10, Sadoghi-Vecer); pipeline queueing launders into
"clustering" (19); calendar composition folds into "drift"
  (22, second seasonality citation for the queued drift item, after
  15/Barzykin).

**What Family C licenses:** every modeled layer declares its flow
model and sign register in the spec; drift statistics declare
calendar composition before being reported.
**What it forbids:** silent Poisson/constant-kappa-style assumptions
in any cost or impact arithmetic; sign registers inherited from an
aggressive-order construction; one-number drift reports.

## Family D — regime is a variable, including who trades

**Statement.** Agent composition, calibration quality, and market
structure drift across vintages and venues; effects at one grain
license nothing at another horizon.

**Citations.** Composition drift [interpretation caution, recorded] —
session 22 (PoH: 2018 human-shaped activity is vintage/venue-local);
venue-freeze warrant — session 14 (sparse LOB: queue machinery is
book-shape-specific); macro censor quantified — session 18;
regressed-process caution (two-year train/application gaps) —
session 21; CKS horizon-gap (1-second OFI licenses nothing about
30m-4h) — session 3 and session 18; C8's unexplored cell remains
exactly that.

**What Family D licenses:** citing vintage and venue before every
market-structure narrative; grain declarations per Family A.
**What it forbids:** porting fitted structure across time, venue, or
horizon; reading a 1-second (or 5-minute, or 3-second-snapshot)
result toward the program's 30m-4h horizon.

## What this map does NOT cover (open territory)

- No paper in the library licenses ANY statement about the funded-
  cost/funding-rate channel of perpetual futures specifically —
  the queue-shape and impact literatures are spot/equity-shaped.
- Spoofing-at-scale on Binance perps in the program's own vintage:
  session 21 measured Coinbase SPOT in 2024; the proportions on the
  program's venue and windows are UNKNOWN and stay that way until
  the owner authorizes measurement.
- The fourteen queued sharpenings remain exactly as queued — this
  map summarizes them, ratifies nothing, and adds no fifteenth.
- Agent-level structure (ids, single-trader dynamics) is absent from
  every read: the program's data has no ids, and every paper that
  needed them said so.

## Bottom line for the owner

The convergence is negative knowledge: a citation-backed map of the
standard ways an edge-shaped artifact forges itself out of an
unexamined construction (feed, grain, sign register, calendar,
pipeline, agent mixture). If T1 — armed, awaiting your word —
survives contact with this map, it survives because its spec already
declares its construction against every family above. If any future
feature spec cannot answer Families A-D in one paragraph each, the
library says kill it in writing, in advance, before it is ever
measured. Nothing in this map is evidence of anything; nothing here
trades live.
