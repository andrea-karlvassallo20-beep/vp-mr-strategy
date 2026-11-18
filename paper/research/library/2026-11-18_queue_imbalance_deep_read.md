# Deep-read session 11 — Gould & Bonart, "Queue Imbalance as a One-Tick-Ahead Price Predictor in a Limit Order Book"

Null-time session 13 (deep-read 11, offset honored). Martin D. Gould & Julius Bonart,
CFM–Imperial Institute of Quantitative Finance; arXiv:1512.03492v1, 11 Dec 2015. Whether the
normalized best-quote queue imbalance predicts the direction of the next mid-price move, on
LOBSTER Nasdaq 2014 data, against a directional null.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/xdc7998_queue_imbalance_as_a_one_tick_ahead_price_predicto.txt, 30 pp.,
page-marked). NB: a RECOVERY READ, not the queue's next rank — this paper was deep-read in a
parallel workspace whose staged notes were wiped by an environment reset before machine-side
adoption (corrigendum in null-time session 13); the reading is re-earned here from the shelf
with page cites, and nothing from the lost note carries status. Triage trace: this slug scores
15 (rank 47 of 500); the queue's next UNREAD triage pointer is unchanged — "Price-Aware
Automated Market Makers" (score 39).

## The paper in one paragraph

The authors ask whether I(t) := (n_b(b_t,t) − n_a(a_t,t)) / (n_b(b_t,t) + n_a(a_t,t)) (Eq. 7,
PDF p. 7), the normalized difference of best-bid and best-ask queue sizes, predicts the
direction y_i of the next mid-price change: for each of 10 liquid Nasdaq stocks over all 252
trading days of 2014 (10:00–15:30 ET, LOBSTER event data; PDF pp. 8–10), a logistic
regression of y on I is fitted, with I sampled at a uniform random time between consecutive
mid-price changes (Sec. 5.1, PDF pp. 11–12), subsampled to 100 data points per stock-day,
80/20 train/test (Sec. 5.2, PDF p. 12). LR tests reject the no-relationship null for all 10
stocks at the 99% level (Table 3, PDF p. 18). Against the paper's own null — y_hat(I) = 1/2
always, the direction-uncorrelated model (Sec. 5.4, PDF p. 14) — out-of-sample binary
classification (ROC AUC) improves by 50–60% for large-tick stocks and 10–30% for small-tick
(Table 4, PDF p. 20: AUC 0.75–0.81 large-tick, 0.58–0.64 small-tick, null 0.5), and
probabilistic mean-squared-residual improves by 20–30% large-tick and 2–6% small-tick (Table
5, PDF p. 21, null 0.25). Semi-parametric local logistic fits are barely better (Sec. 6.4,
PDF pp. 22–25, Table 6, PDF p. 24). The authors' mechanism for the large/small-tick split
(Sec. 7, PDF pp. 25–26): large-tick books pin the spread at one tick, so the mid can move
only by queue depletion, which I governs directly; small-tick books also move via limit
orders arriving inside the spread, which I cannot see.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The two-null admission rule for the
   C1-L2/C8 benchmark family. The paper's null is deliberately dumb — a constant
   1/2 probability (Eq. 18, PDF p. 14) — and every headline improvement is measured against
   it alone (PDF pp. 3, 21). Meanwhile the paper's own two-line state variable I(t) (Eq. 7,
   PDF p. 7), computed from a single depth snapshot with no event decomposition, no sign
   classification, and no flow estimation, delivers out-of-sample AUC 0.75–0.81 (large-tick)
   and 0.58–0.64 (small-tick) one mid-change ahead (Table 4, PDF p. 20), with in-sample ≈
   out-of-sample throughout (no overfitting; PDF pp. 19–21). Candidate pre-declaration: any
   C1-L2/C8 short-horizon flow feature is admitted only if it adds predictive value beyond
   BOTH (a) the top-of-book OFI benchmark already in the family (CKS kill line 7's
   tautology-controlled comparison) AND (b) a pre-registered queue-imbalance comparator built
   exactly as Eq. 7. A flow feature that does not beat a two-line state variable carries no
   incremental claim. This tightens the existing benchmark family (session 3's CKS
   sharpening): it is harder to pass because the feature must now survive two structurally
   different nulls, and the second is immune to event-flow laundering — the comparator never
   leaves the snapshot. The owner ratifies; nobody else arms anything.

2. [interpretation caution] The venue expectation band travels with the rule. The paper's
   regime mechanism is spread-pinning (PDF pp. 25–26): at s(t) = π the mid moves only by
   queue depletion and I governs the race; at s(t) > π in-spread limit orders move the mid
   outside I's view, and short queues dilute the signal. The C1-L2 venue (Bybit BTCUSDT
   perp) is maximal-small-tick — the honest expectation is the paper's small-tick band (AUC
   0.58–0.64; probabilistic improvement 2–6%, Table 5, PDF p. 21), not the 0.75–0.81
   large-tick ceiling. If the two-null rule is ratified, the queue-imbalance null on this
   venue will be weak, and edging it licenses nothing strong. The large-tick numbers are a
   venue-structure ceiling, not a prior.

3. [interpretation caution] The horizon here is a mid-change-count horizon, not fixed time:
   I is sampled uniformly at random between consecutive mid-price changes (Sec. 5.1, PDF
   pp. 11–12) and predicts the direction of the next change. The authors themselves list
   longer-horizon decay as open (PDF p. 27) and name alternative sampling conventions
   (immediately after the change, immediately before) without testing them (PDF pp. 27–28).
   Any port of I, or of the two-null comparator, to C1-L2's fixed 30m–4h horizons must
   pre-declare its resampling convention: silently switching sampling conventions is an
   analyst degree of freedom, the sibling of the beta bug.

4. [reinforcing, no new item] The percent-improvement framing is a weak-null optical
   multiplier: "considerable improvement" (PDF p. 3) is a percentage of a null with AUC 0.5
   and MSE 0.25; the absolutes are AUC 0.75–0.81 and MSE 0.18–0.20 (Tables 4–5, PDF
   pp. 20–21). This is the LOB-state analogue of the programme's reporting rule that
   benchmark-relative percentages are never reported without their absolutes.

5. [source-quality note] arXiv:1512.03492v1, 11 Dec 2015; Gould & Bonart, CFM–Imperial
   (CFM, a quantitative fund, acknowledged; PDF p. 28). Unpublished on the shelf's
   knowledge — check for a published version before formal citation. One misprint worth
   flagging because it sits in the sign definition: the I > 0 condition is written as
   n_b(b_t,t) > n_a(b_t,t) (PDF p. 8), copying the bid argument into the ask queue where
   Eq. 7 (PDF p. 7) correctly uses n_a(a_t,t); the definition itself is unambiguous and the
   paper's asymmetry results (intercept x_0 significant only for CSCO, ORCL and GOOG; PDF
   p. 18) are unaffected.

## What this paper would have killed if we had done it wrong

If the C1-L2 spec's null family had contained only event-flow benchmarks (the CKS OFI line)
and volume-shaped nulls, a two-line queue-imbalance regression — the cheapest signal any desk
already runs — could have beaten the registered feature after the fact, and the claim would
have died in post-hoc review instead of at a pre-declared gate. And if the headline
"50–60% improvement" (PDF p. 3) had been read as the expected effect size for a crypto perp
venue, kill lines would have been calibrated to a large-tick pinned-spread ceiling that a
maximal-small-tick book structurally cannot reach — a genuine null would then have been
misread as effort failure, the worst kind of false kill. Pre-declaring the second null AND the
small-tick expectation band before the L2 data closes both traps.

## Standing caveat

Ammunition, not evidence: nothing in this note enters any claim as support. The magnitudes are
venue-, era- and design-specific (Nasdaq 2014 equities, one primary-venue exchange per stock
(PDF p. 9), a single year, 10 names, subsample 100/day, 80/20 split per Sec. 5.2, PDF p. 12).
What transfers, cautiously, is the structure: best-quote state imbalance carries out-of-sample
direction information at the shortest horizon, strongly modulated by the spread measured in
ticks. The port to a maximal-small-tick perp venue belongs to C1-L2's own gated spec, not to
this citation. arXiv-version caution applies: check the published version before formal
citation.
