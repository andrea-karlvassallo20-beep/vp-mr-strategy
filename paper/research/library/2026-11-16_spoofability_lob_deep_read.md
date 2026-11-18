# Library deep-read session 21 — Fabre & Challet, "Learning the
# Spoofability of Limit Order Books With Interpretable Probabilistic
# Neural Networks" (arXiv:2504.15908v1, 2025; CentraleSupélec /
# Paris-Saclay and SUN ZU Lab; Level-3 spoofability measurement on
# Coinbase BTC-USD and ETH-USD)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x2aee07_learning_the_spoofability_of_limit_order_books_wit.txt`,
~20 pp. text + appendix, page-marked). Next UNREAD triage-rank entry
(score 34; flagged in the last two queue pointers as directly aimed
at C5's passive-withdrawal family and C8's spoofing cautions).

## The paper in one paragraph

The authors build multi-scale order-flow features from marked,
Hawkes-inspired kernels applied to Level-3 (market-by-event) data on
Coinbase: limit-order flows weighted by elapsed time, order size,
and POSTING DISTANCE from the best price (exponential kernels with
three time scales beta in {10, 100, 1000}/s and four distance scales
eta in {0.001, 0.1, 1, 10}/bp), plus marketable-order flows; a tiny
feed-forward neural network (one hidden layer, 64 neurons) maps these
31 features to the parameters of the conditional skewed-Gaussian
distribution, over a T = 1 s horizon, of the mid-price move after
each limit-order insertion (PDF pp. 4-7). Counterfactual insertion of
a hypothetical order of size Q at distance delta shows the predicted
risk-adjusted move responds monotonically to size and inversely to
distance: orders of Q >= 50,000 USD placed within several basis
points move the predicted Sharpe of the 1-second move, WITHOUT
touching the best queue — detection models using only top-of-book
imbalance are thereby "not suitable to describe the data" (PDF
pp. 9-10). From the spoofer's viewpoint they write a fully
probabilistic expected-cost function (bona fide order at touch,
non-bona fide order deep, first-passage fill probabilities from the
predicted distribution, Coinbase fees), and flag an order
"suspicious" when inserting it improves the spoofer's expected cost
relative to abstaining (PDF pp. 12-15). Running this on all
88,327,661 orders of 2024-12-04 to 2024-12-07: 31% of large orders
(Q >= 4,500 USD, of which there were 8,601,227) are classified as
spoofable-capable; suspicious orders sit DEEPER (avg. 6.85 bp vs
1.03 bp for normal), are larger (avg. 9,661 vs 2,042 USD), are almost
never at the top of the queue (0% of large suspicious vs 4.20% of
large normal), and are followed by larger, more skewed 1-second
price moves; burst-clusters of suspicious orders often carry
similar ROUND-NUMBER sizes, revealing a single agent; layering is
frequent (PDF pp. 15-19, Table 1).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand. The paper is the
library's most direct hit yet on C5's passive-withdrawal family, and
every finding lands as reinforcement or caution:

1. **[reinforcing, no new item] Round-number size clusters as a
   same-agent fingerprint — the session-17 baseline caution lands
   again, from the manipulator's side.** The authors observe that
   when many orders are flagged suspicious within a very short
   window, they often carry similar ROUND-NUMBER sizes (PDF pp. 15,
   17, Figures 11-13, 15-16), and read this as evidence of a single
   agent. This is the same round-number signature the compound-
   Hawkes simulator read (session 17) flagged for the queued wash
   audit — here it appears as an EMPIRICAL fingerprint of a
   manipulative agent, not a null artifact. The queued wash-audit
   item gains a citation on exactly the mechanism it must control
   for: round-number clustering identifies AGENTS, so a wash-audit
   baseline that ignores it can misattribute coordinated flow to
   coincidental retail. Nothing about the queued item's legal
   content changes; it is not re-armed or re-worded here.

2. **[interpretation caution] The LOB is not all intention — deep,
   non-bona-fide liquidity measurably moves the conditional price
   distribution.** The paper's headline for feature design: passive
   orders placed several basis points from the touch, never at risk
   of likely execution, shift the predicted distribution of the
   next second's mid-price move, and 31% of large orders meet the
   paper's spoofability criterion (PDF pp. 10, 15, Table 1). For the
   L2 feature layer this is a quantified warning that depth- and
   imbalance-based features computed on gated BTCUSDT windows are
   reading a mixture of bona fide intention and manipulation-
   capable placement — a mixture whose proportions are regime- and
   venue-dependent (Coinbase spot, December 2024, small-tick
   asset). The program's existing discipline — depth features are
   descriptions, never independent ground truth for causality
   claims, and every causal language about passive flow goes through
   C5's passive-withdrawal family — covers this; the paper supplies
   the strongest empirical ammunition for that discipline the
   library has yet produced. Top-of-book imbalance signals in
   particular are the WORST-POSITIONED to see the phenomenon (the
   paper's own point against Cartea-style top-of-book frameworks;
   PDF pp. 2-3, 19).

3. **[interpretation caution, extending the estimator-mode line]
   "Spoofability" here is a model-computed counterfactual, not an
   observation of manipulation.** Suspicious = the agent's own
   trained network says her expected cost improves if she inserts
   the order (PDF pp. 14-15). No trader ids, no labels, no
   prosecuted cases; the authors are explicit that without
   anonymized ids detection "with certainty" is impossible and
   their output is a suspicion layer, not a verdict (PDF pp. 14,
   19). The 31% number is therefore DEFINITIONAL — a threshold
   artifact of Q >= 4,500 USD, a q = 100 USD bona fide order at
   touch, and their December week — and would move under any other
   spec. It is quoted nowhere as a base rate of spoofing on any
   venue; it licenses only the mechanism evidence (distance-aware
   flow moves conditional price distributions).

4. **[cost-survival ammunition] The probabilistic expected-cost
   template declares fees, fill probabilities, and liquidation legs
   in one closed expression.** The spoofer cost functions (PDF
   pp. 12-14, eqs. 27-30) integrate taker/maker fees, first-passage
   fill probabilities, and the terminal-liquidation legs of BOTH
   orders; the cross-asset extension is explicit. If a K7-style
   cost-survival layer is ever ratified, any manipulation-adjacent
   cost arithmetic must carry this structure or it will misprice
   the liquidation leg of unfilled passive intent. Declared as
   ammunition only; the program never trades live and nothing here
   is operationalized.

5. **[source-quality note] Two-year train/application gap,
   unremarked.** The model trains on 2022-12-01 to 2022-12-07 and
   is applied 2024-12-04 to 2024-12-07 (PDF pp. 6-7 vs 15); no
   drift discussion separates the regimes. For the program this is
   one more instance of the regressed-process caution: a fitted
   conditional-distribution model applied across a two-year gap
   without a stationarity warrant is an estimator statement about
   the patch it was fitted on, not about the application week — and
   the detection counts inherit that gap silently. arXiv v1
   (April 2025), single week of Level-3 data from a proprietary
   SUN ZU Lab feed; check published version before formal citation.

## What this paper would have killed if we had done it wrong

If the trigger layer had been specified with depth/imbalance
features treated as BONA FIDE liquidity signals — the natural,
pre-registered-looking choice — this paper's mechanism evidence
means those features would be partially reading manipulative
placement on exactly the windows that matter, an entanglement no
label placebo could catch (the labels would be moved by the same
spoofed conditional drift the features read). And if a "manipulation
is rare" prior had been written anywhere into the C8 spec, the 31%
of large orders meeting an unsupervised spoofability criterion on a
major regulated-exchange-adjacent venue in a single December week
would have falsified the prior before it armed. The program's
existing lines — depth describes, C5 owns passive-withdrawal
language, ground truth comes only from the independent
book_snapshot_25 check — are exactly what keep this read inside the
falsification-first discipline.

## Standing caveat

Coinbase SPOT Level-3, BTC-USD/ETH-USD only — not Binance
perpetuals, whose fee/spec geometry (funding, leverage, taker-
dominated flow) differs in exactly the dimensions the cost function
sensitive-weights (PDF pp. 5, 14). Horizon is T = 1 second: the
entire spoofability mechanism lives at a grain the program does
not sample, and NOTHING here licenses any statement about 30m-4h
windows — C8's unexplored cell remains exactly that. The detection
rule assumes the spoofer optimizes against the paper's own model
of impact; sophisticated manipulators adapting to the detector
invalidate the calibration (the arms-race problem the authors
themselves gesture at with "first layer of a large detection
procedure", PDF p. 19). Round-number and layering observations are
from eight illustrative time frames, not from a systematic census.
