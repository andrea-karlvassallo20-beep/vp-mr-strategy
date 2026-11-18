# Library deep-read session 30 — Barone & Lillo, "Trading in the
# Sunshine or in the Shade: Market Impact and Adverse Selection on
# Hyperliquid" (arXiv:2606.15715v1, 2026; Scuola Normale Superiore,
# Pisa; sunshine trading measured on a fully on-chain perp CLOB)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xa74970_trading_in_the_sunshine_or_in_the_shade_market_imp.txt`,
~31 pp., page-marked). Next UNREAD triage-rank entry (score 32;
verified unread by the read-slug mapping; NOTE: the shelf slug ends
"_market_imp" — the session-36 log pointer truncated it). Venue
proximity flag: this is the FIRST paper in the entire deep-read
queue with the program's own geometry — crypto PERPETUAL futures on
a central limit order book, USDC-margined, oracle-indexed, hourly
funding — not spot equity, not FX.

## The paper in one paragraph

Hyperliquid's protocol-native TWAP orders are visible from
inception and stay visible while active — a natural sunshine-trading
laboratory. Across all 201 Hyperliquid perpetual markets
(2025-07-28 to 2026-03-23; >641 million fills; public on-chain,
address-level data), the authors compare 465,000 visible native
TWAPs against 4.3 MILLION statistical (hidden) metaorders
reconstructed by same-address same-sign aggregation under a
standard splitting hypothesis (PDF pp. 3-4). Hidden metaorders show
front-loaded U-shaped schedules and double-inflection impact
trajectories with pronounced peaks and post-trade decay — optimal
strategic execution under transient impact — while visible TWAPs
trade nearly uniformly and trace the smooth concave square-root
path (PDF p. 3). Testing Admati-Pfleiderer's preannouncement
predictions: visible TWAPs cost ~9 bps LESS in temporary impact
than comparable hidden metaorders; leave ~5 bps less permanent
displacement; hidden metaorders executed ALONGSIDE already-visible
same-direction TWAP flow suffer ~0.8-0.9 bps more permanent
displacement per 10-point increase in visible-flow dominance (the
adverse-selection cost shifts to NON-announcers); and while a TWAP
is active, DISPLAYED DEPTH RISES and the book TILTS toward the
absorbing side, scaling with announced size, not explained by
pre-trends (PDF pp. 3-4).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] Displayed depth is CONDITIONAL on
   the visible-flow regime — the book "responds," it does not just
   "exist."** The fourth finding is the sleeper hit: the measured
   displayed-depth response (rises, tilts toward the absorbing
   side, scales with announced size) means depth features computed
   on any window read a book whose shape partially REFLECTS the
   prevailing visible flow. For the L2 feature layer this is the
   equilibrium-side mirror of session 21 (depth carries
   manipulation-capable content) and session 24 (passive placement
   moves the price process): here depth carries ABSORPTION-GAME
   content. The existing depth-describes-never-ground-truths
   discipline and the Layer 0 ground-truth check already cover the
   entanglement; nothing queued, no wording changed.

2. **[reinforcing, no new item] "Hidden metaorders" are a
   CONSTRUCTION, and the headline gaps partly inherit it.** The
   4.3M hidden metaorders are statistical reconstructions under a
   splitting hypothesis (aggregation threshold, same-address
   same-sign), while the 465k TWAPs are protocol-native and exactly
   observed — the ~9 bps and ~5 bps announcer advantages are
   measured against a comparison class whose members are
   themselves estimates (PDF pp. 3-4). This is the estimator-mode
   family's reconstruction face: a metaorder count is a
   (splitting rule x address rule) artifact. The paper is careful
   with conditioning; the citation discipline here is to quote the
   mechanism (visibility changes costs), never the separators as
   venue constants.

3. **[interpretation caution] Venue observability is
   load-bearing and NON-PORTABLE — the perp-venue caution,
   quantified.** Hyperliquid's data has ADDRESS-LEVEL identity and
   protocol-native order visibility — capabilities the program's
   Binance data does NOT have (session 21's no-ids caveat) — and
   0.2 s median end-to-end consensus latency (PDF p. 4). The
   sunshine mechanisms (cost shifting to non-announcers, depth
   elicitation) are consequences of THIS venue's observability
   geometry; magnitudes are venue-specific and the
   venue-freeze warrant (session 14) applies with extra force now
   that the library finally contains a perp-venue study: quote
   mechanisms with vintage and venue, port nothing numerically.

4. **[reinforcing, no new item] The two program grains stay
   separate: this paper's fine-grain flow/cost findings license
   nothing at the daily grain, and vice versa.** The closeness
   dossier (measured session 34) found daily volume ratios carry
   nothing; this paper finds the visible-flow regime measurably
   moves fine-grain costs and depth. Both are true: visibility
   lives at the flow grain, closeness lives at the daily
   prestate grain. No porting in either direction — the
   grain-specific-objects rule (sessions 18/22/23) already forces
   the separation, and the cost-survival ammunition file gains the
   fine-grain visibility template (any K7 layer must declare the
   venue's visibility/latency geometry).

## What this paper would have killed if we had done it wrong

If the L2 feature layer had ever treated displayed depth as a
static factual snapshot of liquidity (the natural reading), the
depth elicitation finding is the demonstration that depth
PARTIALLY REFLECTS the visible-flow regime — features computed on
it are functions of the absorption game, and their apparent
predictive content could be visibility-regime content, an
entanglement no label placebo would catch because the labels ride
the same regime. And if any cross-venue statement had been built
from the 9 bps separator without declaring the reconstruction
behind the comparison class, it would have imported a splitting-
hypothesis artifact as a venue fact. The program's depth-disciplne,
construction declarations, and venue-freeze warrant predate this
read; all three are reinforced, none changed.

## Standing caveat

One venue, eight months (July 2025-March 2026 — a specific
crypto-vintage), 201 perp markets ranging from majors to thin
tokens; statistical metaorder reconstruction rests on a splitting
hypothesis with no ground truth; the sunshine-vs-hidden comparison
is not randomized — traders who CHOOSE the visible TWAP may
differ in informativeness from those who don't, and the authors
condition on observables but selection remains; block-level
latency (0.2 s median) is a different execution physics from
centralized matching engines (session 19's pipeline caution cuts
the other way here too). arXiv v1, June 2026, no published version
located at read time — check before formal citation. Execution and
sunshine-strategy content is the paper's subject; none of it is
operationalized; the program never trades live.
