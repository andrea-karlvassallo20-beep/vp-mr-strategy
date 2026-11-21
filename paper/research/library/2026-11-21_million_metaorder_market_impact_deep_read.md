# Library deep-read session 82 — A Million Metaorder Analysis of Market Impact on the Bitcoin

- **Authors:** Jonathan Donier, Julius Bonart
- **Title:** A million metaorder analysis of market impact on the Bitcoin
- **Venue:** arXiv:1412.4503v3 [q-fin.TR], arXiv stamp 21 Sep 2015 (paper dated
  September 22, 2015)
- **What it is:** a complete-market empirical study of metaorder impact on the
  MtGox Bitcoin/USD exchange in which every trade carries a unique
  (anonymized) trader ID, allowing over one million metaorders to be
  reconstructed and their impact trajectories, speed dependence and
  permanent components measured on a venue with 0.6% fees and essentially no
  arbitrage or market making.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xfcaaa2_a_million_metaorder_analysis_of_market_impact_on_t.txt,
~18 pp., page-marked). Next UNREAD triage-rank entry (score 23).

## The paper in one paragraph

Using all 13M trades on MtGox between August 2011 and November 2013 with
unique trader IDs (PDF p. 4), the authors segment aggressive order flow into
over one million metaorders by inactivity periods (~1 hour) and direction
reversals (PDF pp. 5-7), verify that average execution is linear in time and
that metaorders are not synchronized with the residual flow (Figs. 3-4,
PDF pp. 6-8), and find the square-root impact law I(Q) ≈ ±Y σ (Q/VD)^δ with
δ ≈ 0.5 holds over four decades, trajectory-wise and even at the smallest
scales (Figs. 5-6, PDF pp. 8-10) — on a venue where statistical arbitrage
below the 60 bps fee scale is impossible and no martingale condition or
fair-pricing argument can be invoked (PDF pp. 1-2, 16-17). The Y-ratio
residual after σ_D/√V_D normalization is roughly time-independent, Gaussian
with Y0 = 0.9 and ΣY = 0.35 (Figs. 7-8, PDF pp. 10-11). During a metaorder,
impact is almost perfectly the square root of the TOTAL market imbalance
rather than of the metaorder's own volume (Fig. 11, PDF pp. 13-14), the
permanent impact of ordinary ("informed") metaorders is attributable to
their correlation with the residual order flow, while "isolated"
metaorders — those supplying >75% of net market imbalance over
[t0, t0+10T], ~3% of the sample — show a permanent mechanical impact
consistent with decay to zero (Fig. 12, PDF p. 15) — and measured impact is
at most one to two spreads even for large volumes, so friction costs
dominate impact costs (Fig. 9, PDF p. 12).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [reinforcing, no new item] The canonical square-root impact law — the
   same law the mature-market impact literature reports — holds on a venue
   with 0.6% fees, no statistical arbitrage below the fee scale, no
   high-frequency market making and no well-defined martingale price (PDF
   pp. 1-2, 8, 16-17). Univerality of an impact law across microstructure
   regimes is direct evidence that impact-shaped associations can never, by
   themselves, evidence an anticipation mechanism: the law is a property of
   supply-and-demand absorption, not of information. This reinforces the
   programme's default (no edge) and the laundering ban (library is
   ammunition, not evidence): no empirical magnitude in this paper may
   enter the record as support for any programme claim. No queue change.

2. [interpretation caution] The measured impact of a metaorder INCREASES
   as execution slows (δ′ ≈ 0.4 on µ_V, PDF pp. 13-14) — the opposite of
   intuition — because slower execution gives correlated residual flow time
   to realize alongside; only after conditioning on isolated metaorders
   does impact decrease with slower execution (PDF p. 15). Any future
   C1-L2/C8-adjacent statistic conditioned on duration or participation
   (a compression clock included) must be interpreted through this lens: a
   "slower build-up, larger subsequent move" pattern can be pure
   co-movement correlation with aggregate flow, not a mechanism. No queue
   change.

3. [candidate sharpening, PENDING OWNER RATIFICATION] The residual-flow
   attribution null, queued as the FORTY-THIRD candidate: BEFORE the L0
   gate, any C1-L2/C8-adjacent spec that attributes a price, spread or
   depletion-side association to an identified flow episode (a compression
   cluster, an OFI burst, a metaorder-like run) must pre-declare an
   attribution null in which the aggregate signed order-flow imbalance over
   the same window is conditioned out: the claimed episode-level
   association must be shown to survive in the subsample where the
   residual (episode-minus-aggregate) flow is statistically neutral, per
   this paper's isolated-metaorder construction (the episode accounts for
   more than 75% of net market imbalance over [t0, t0+10T]; the selection
   labels ~3% of metaorders isolated, PDF p. 15), and the conditioning
   window, the neutrality threshold and the imbalance measure must be
   frozen BEFORE the data. Earned by the paper's measured mechanism: during
   a metaorder, impact is almost perfectly the square root of the TOTAL
   market imbalance rather than of the metaorder's own volume (Fig. 11,
   PDF pp. 13-14), the market does not detect individual metaorders and
   "the impacts of different metaorders are in fact dependent and do not
   add up linearly" (PDF p. 16), and the permanent impact of correlated
   "informed" metaorders is fully explained by their correlation with the
   residual order flow while isolated metaorders show a mechanical
   permanent impact consistent with decay to zero (Fig. 12, PDF p. 15) —
   so an episode-attributed "anticipation" association could be pure
   common correlation with aggregate flow and would survive any null that
   does not condition it out. Harder-to-pass because a flow-attribution
   claim that beats only an unconditional or episode-internal null now
   fails by rule instead of surviving as a find; it tightens the
   dynamics-identification rule for generative nulls (null-time session
   58) with the attribution-conditioning null class, and complements the
   queue-jump-diffusion generative null (deep-read session 81) which
   controls the flow dynamics but not the attribution to a specific
   episode.

4. [cost-survival ammunition] Measured impact does not exceed one to two
   spreads even for large metaorders, and fees of the same order as the
   spread mean friction costs dominate impact costs (Fig. 9, PDF p. 12).
   If a future K7-style cost-survival layer exists, it must carry
   fee-and-spread assumptions at least as large as the impact it nets
   out; an edge whose gross size is of impact order can be entirely
   friction. No queue change now; the assumption travels only if that
   layer ever exists.

5. [reinforcing, no new item] Metaorder size, duration and participation
   distributions on this venue are NOT clear power laws (Fig. 3, PDF
   pp. 6-7), yet the square-root law holds regardless — directly
   against the models that require a 3/2 power-law order-size
   distribution to derive it. Reinforces the programme's refusal to
   accept heavy-tail or power-law premises in any spec unless they are
   measured and frozen; assumption-indexed premises can be wrong without
   leaving a mark on the headline law. No queue change.

6. [source-quality note] Single venue (MtGox), single asset, dead
   exchange, crisis-era 2011-2013 Bitcoin microstructure, 0.6% fee
   regime, trader-ID completeness unavailable on any modern venue (PDF
   pp. 3-4); the raw data came from an anonymous source, was
   consistency-checked against public records, and the authors state no
   insurance of accuracy (PDF p. 4n4); metaorder segmentation depends on
   the ~1-hour inactivity classifier (PDF pp. 5-7); all magnitudes
   (δ ≈ 0.5, Y0 = 0.9, ΣY = 0.35, Figs. 5-12) are venue- and era-indexed
   and enter the record as none-of-our-support; the laundering ban binds.
   arXiv v3 — check the published version before any formal citation.

## What this paper would have killed if we had done it wrong

If the C1-L2 spec (or any C8-adjacent conditioning) had attributed an
anticipated-move association to an identified compression episode without
conditioning on the aggregate flow around it, the association the paper
measures between correlated metaorders and their "permanent" impact — which
is entirely co-movement with the residual flow, vanishing for isolated
episodes (Fig. 12, PDF p. 15) — would have been recorded as a mechanism
discovery and then died at the L2 phase, taking the credibility of the
whole compression family with it. Equally, if the programme had cited the
cross-market universality of the square-root law as support for any claim
about the venue it will actually test, it would have laundered a dead
exchange's magnitude — the exact failure class the
library-is-ammunition rule exists to prevent, and the reason the
sharpening above freezes the neutrality construction before the data
instead of choosing it after seeing a result.

## Standing caveat

Everything here is 2011-2013 MtGox: a 0.6%-fee venue with no market making,
no arbitrage below the fee scale, ~0.6% spreads, and an impact regime
measured while the exchange was heading toward collapse. The
trader-ID-complete dataset is the paper's strength and is unavailable on
any venue the programme will test; the informed/uninformed decomposition
is a correlation-based selection (~3% of metaorders), not a label of
information in any economic sense, as the authors themselves note
(PDF pp. 15-16). The square-root law's claim to universality across
venues is a hypothesis this paper strengthens but cannot prove, and the
extract is the arXiv v3 version (21 Sep 2015) — the published version
should be checked before any formal citation. Nothing here licenses a
measurement, an arming or a kill-line move; it licenses one
harder-to-pass admission null, pending the owner's ratification.
