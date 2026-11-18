# Library deep-read session 23 — Su, Sun, Li & Yuan, "The Price
# Impact of Generalized Order Flow Imbalance"
# (arXiv:2112.02947v1, 2021; Xi'an Jiaotong University; GOFI/log-GOFI
# generalization of Cont-Kukanov-Stoikov OFI for snapshot data)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xdb066c_the_price_impact_of_generalized_order_flow_imbalan.txt`,
~9 pp., page-marked). Next UNREAD triage-rank entry (score 33;
verified unread by the read-slug mapping, per the skill's selection
protocol; the paper sits in the CKS-OFI family the program has
already read once — the session-3 CKS review and session 18's
Takahashi read both cite Cont-Kukanov-Stoikov (2014)).

## The paper in one paragraph

The authors start from the Cont-Kukanov-Stoikov OFI construction
(mid-price change linear in the net order flow at the best
queues), note that its aggregation assumes the best price moves at
most ONE tick per observation interval, and that this assumption
breaks on China's 3-second snapshot feed, where the best price can
cross several levels inside a single interval (PDF pp. 3-4). Their
Generalized Order Flow Imbalance (GOFI) recomputes the interval's
flow contribution by summing the depth deltas over ALL levels
crossed when the best price jumps, with a level-count determined
by the observed move rather than one tick; the stationarized
variant (log-GOFI) applies the Wang et al. log transform to the
depth terms (PDF pp. 4-5). On ten selected CSI 500 constituent
stocks, linear regressions of mid-price change on each indicator at
30s/1m/5m: classic OFI explains 32.89/38.13/42.57 percent
out-of-sample, log-GOFI 83.57/85.37/86.01 percent — a very large
gap driven by fixing the multi-tick-move misspecification, with
log-GOFI also more stable across scales (PDF pp. 5-6, Tables 1-3).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] A flow-indicator's value is a
   function of the FEED and AGGREGATION, not just the market —
   the estimator-mode line quantified.** The entire gain of GOFI
   over OFI comes from the observation interval's granularity
   versus the feed's discreteness: the SAME market, the SAME
   events, produce materially different OFI series under a 3-
   second snapshot grain than under a one-tick-move assumption,
   and the R^2 gap (43 -> 86 percent at 5 minutes) is entirely an
   aggregation-construction artifact (PDF pp. 3-6). This is a
   direct, quantified reinforcement of the aggregation-endogeneity
   line (session 18's "readings from different grains are
   different objects") and the estimator-mode rule (session 11):
   an OFI-type statistic is never a market property — it is a
   (feed x grain x construction) property, and any future
   trigger-layer feature built from order-flow aggregates declares
   its feed grain and construction in the spec before its value
   is read. Nothing new queued; the existing rules already force
   this.

2. **[interpretation caution] OFI-family R^2 numbers are not
   transportable across venues — especially not to small-tick,
   snapshot-fed crypto.** The 86-percent figure belongs to CSI
   500 stocks: large-tick, price-limit, 3-second-snapshot, order-
   driven with depth concentrated per level — a venue geometry
   where a "multi-tick jump inside one snapshot" is a definable
   event. BTCUSDT is small-tick (continuous distance), feed is
   depth-diff snapshots at sub-second cadence, no price limits
   (PDF pp. 2, 5). The paper's finding licenses NOTHING about
   any Binance window's explainability, and — connecting to
   session 21 — the depth the GOFI construction sums over is
   precisely the depth that carries manipulation-capable
   placement; a GOFI-style feature on gated windows would inherit
   both the aggregation artifact AND the bona fide/manipulation
   mixture.

3. **[source-quality note] Thin provenance: preprint, selected
   sample, extract-damaged text.** arXiv v1 with no visible peer-
   review; ten stocks explicitly chosen "to facilitate the
   presentation" out of the CSI 500 (PDF pp. 1, 5); the extract's
   equation bodies and the Conclusion section are empty or garbled
   in the OA text layer (page 8 is effectively blank), so the
   table statistics carry the read; no significance testing, no
   out-of-sample protocol description beyond the column labels
   "in-sample/out-of-sample". Recorded per the session-9
   triage-audit discipline: the score-33 rank promised CKS-family
   access value, and the paper delivers a real mechanism point,
   but at undergraduate-project bibliography weight — quote it
   only for the aggregation mechanism, never as evidence of any
   market fact.

## What this paper would have killed if we had done it wrong

If the trigger-layer spec had ever cited an OFI-standard R^2 from
a large-tick equity study as if it measured a property of "the
market" rather than of a feed-grain-construction triple, this
paper is the demonstration that the number collapses the moment
the aggregation assumption breaks — the same statistic doubles its
apparent power when the construction is fixed for the feed. And if
the gated BTCUSDT feature layer had copied the CKS one-tick
aggregation verbatim (as many "standard" implementations do), a
sub-second multi-tick move inside a snapshot window would have
been mismeasured by construction — an error invisible in any
backtest because the feature and the label share the same
cheap construction. The program's grain-declaration and
estimator-mode rules predate this read; the paper is their
cleanest quantified illustration the library holds.

## Standing caveat

Chinese large-tick equity venue with 3-second snapshots and price
limits; ten hand-picked stocks from one index; linear mid-price
regressions with no reported standard errors, stationarity
treatment only via logs, and a garbled OA text layer (equations
and conclusion unreadable — the mechanism narrative above is built
from the construction discussion and the tables); no peer-reviewed
version located at read time — check before formal citation. No
execution content beyond citing the optimal-execution literature;
nothing to operationalize; the program never trades live.
