# Deep-read note — session 75: "Ascertaining price formation in cryptocurrency markets with Deep Learning" (Fang, Chung, Ventre, Basios, Kanthan, Li, Wu, arXiv:2003.00803v1)

**Deep-read session 75** (null-time session 86, second act, after the edition-7
synthesis pass, log ## 95). Fan Fang, Waichung Chung, Carmine Ventre, Michail
Basios, Leslie Kanthan, Lingbo Li, Fan Wu, "Ascertaining price formation in
cryptocurrency markets with Deep Learning", arXiv:2003.00803v1 [q-fin.GN],
compiled April 6, 2020 (arXiv stamp 9 February 2020). An empirical
deep-learning paper: a two-layer LSTM predicts the direction of the next-tick
mid-price change on live GDAX (Coinbase Pro) level-2 data across
cryptocurrency pairs, with a multi-label variant bounded by the Coinbase
transaction fee, and a "walkthrough" retraining scheme engineered to counter
accuracy decay on live data.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xe0397d_ascertaining_price_formation_in_cryptocurrency_mar.txt,
~22 pp., page-marked). Next UNREAD triage-rank entry (score 24, xe0397d),
second of the score-24 tier, as recomputed by the ## 95 pass against the live
tail.

## The paper in one paragraph

The paper trains a deliberately small network (two LSTM layers, one
fully-connected layer, softmax output, PDF p. 7, Figure 3) on live-captured
GDAX WebSocket data (tickers, level-2 updates, order flow; a single
~30-hour capture, 2018-07-02T17:22:14Z to 2018-07-03T23:32:53Z, 40,951,846
level-2 records across 11 listed products, PDF pp. 5-7, Table 1 p. 7) to
predict binary next-tick mid-price direction, plus a four-class variant whose
"significant change" boundary is set at ±0.2% of price, the Coinbase
transaction fee (Table 2, PDF p. 8). RQ1: pooling all pairs into one
"universal" model beats pair-specific models (avg +3.65% accuracy, +4.25%
after excluding four weak pairs from both sets, PDF p. 13, Table 4) — with
the authors themselves attributing part of the gain to pooled data quantity
(PDF p. 13). RQ2: increasing the input sequence (time steps 1 through 40)
has no significant effect; the OLS slope is ≈ −0.0001 and one time step is
declared best (PDF p. 14, Tables 5-6). RQ3: on live data the universal
model's accuracy decays "to almost random guessing" (PDF pp. 14-15,
Figure 9); the paper responds with an autoencoder denoiser (PDF pp. 15,
18-19), a prediction-bias exhibit showing the model drifting against the
real-time target distribution (PDF p. 16, Figure 12), and "walkthrough
training" — retraining inside the live stream every 196 predictions (stable,
PDF p. 17) or when a modified drawdown of accuracy exceeds 15% (MDD-dynamic,
PDF p. 9) — which lifts accuracy from below 50% through 58% to a stabilized
~76-78% on BTC-USD (PDF p. 17, Figures 13, 11; Table 7, PDF p. 19). RQ4: on
1-minute multi-label live data, the static model decays below 40% (four-class
random = 25%) while stable walkthrough stabilizes around 80% across twenty
repeats (PDF pp. 19-20, Figures 16-17). A decision maker, inventory
management, order placement and costs are all left to future work
(PDF p. 6).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. This is the
direction-prediction paper class read at triage score 24 for a reason: every
mechanism it exhibits is already frozen in the programme's disciplines —
base-rate honesty, statistical baselines, freeze-then-evaluate,
no-re-tune-inside-the-window, benchmark-vs-representation confounds — and
the paper confirms each of them live rather than adding a new rule.

1. [reinforcing, no new item] The headline accuracy is never accompanied
   by its base rate. The "consistent 78%" next-tick binary accuracy
   (PDF pp. 1-2) appears with no up/down class balance for the scoring
   window, no majority-class baseline, and no ROC/false-positive
   accounting anywhere; the only class counts in the paper are Table 7's
   supports (up 5,265, down 4,927, PDF p. 19), i.e., roughly balanced for
   that one BTC-USD window, and the abstract's promised "statistical and
   machine learning techniques" (PDF p. 1) never materialize as a
   statistical baseline in any table. Accuracy without its base rate and
   without a shallow baseline is exactly the exhibit the base-rate and
   two-null admission disciplines already forbid accepting; reinforces,
   no new item.

2. [reinforcing, no new item] The paper's own most honest exhibit is the
   decay: the universal model's accuracy on live data falls "slowly ...
   to almost random guessing" (PDF pp. 14-15, Figure 9), the autoencoder
   only slows the decay and cannot fix a drift in the prediction
   distribution (PDF p. 16, Figure 12), and the static multi-label model
   drops below 40% (PDF p. 19). A fitted state on the limit order book is
   regime-bound; this is a live, page-cited instance of why C1-L2's
   specification is frozen before the data and its features are
   pre-declared, and why anything fitted on a discovery window that does
   not persist cannot be re-armed by post-hoc smoothing; reinforces the
   freeze-then-evaluate spine, no new item.

3. [interpretation caution] The "consistent 78%" is an artifact of
   retraining inside the evaluation window. Walkthrough training retrains
   the model on a buffer built from the live stream every 196 predictions
   (PDF p. 17), and the MDD-dynamic variant retrains "with historical
   data up to the point when the MDD is measured" (PDF p. 9); the
   stabilized 76-78% (Figures 11 and 13; Table 7, PDF p. 19) is achieved
   by a model being updated on the very sequence it is then scored
   against, and the model starts below random guessing before the first
   retrain (PDF p. 17). A programme test that re-tuned inside its own
   evaluation window would pass exactly this check; the reading
   discipline is that no accuracy number from any update-sustained
   segment is evidence of a persistent edge. Reading caution only, no
   queue change.

4. [reinforcing, no new item] The universality claim carries its own
   confound and a survivorship step. The universal model's edge over
   pair-specific models (avg +3.65%, +4.25% selected, Table 4, PDF p. 13)
   is explained in part by the authors themselves as pooled data quantity
   ("10% of joined data is much larger than 10% of one currency pair
   data", PDF p. 13), and the "selected" datasets exclude the four pairs
   that performed poorly (BCH-EUR, BTC-GBP, ETH-EUR, BTC-EUR, PDF p. 13)
   before the universality comparison is re-run on the survivors.
   Benchmark-vs-representation confound plus post-hoc instrument
   selection, both already frozen in the standing confound rules;
   reinforces, no new item.

5. [reinforcing, no new item] One time step suffices (Table 5, PDF p. 14):
   accuracy is flat in the input sequence length (OLS slopes ≈ −0.0001
   to −0.0002, Table 6, PDF p. 14), so the recurrence contributes nothing
   measurable beyond the current tick's feature vector and the "deep"
   label on this architecture is not the source of its accuracy — a
   clean live instance of the representation-confound rule: the model
   family's name is not the mechanism; reinforces, no new item.

6. [cost-survival ammunition] Accuracy is not edge at this horizon: the
   prediction target is the next tick's mid-price direction, the paper
   itself sets the tradability boundary at the ±0.2% Coinbase fee only
   for the multi-label variant (Table 2, PDF p. 8), names execution
   latency as a factor that can make a next-tick prediction obsolete
   (PDF p. 10), and leaves the decision maker, inventory and order
   placement entirely to future work (PDF p. 6); no accuracy figure in
   any table is converted into a round-trip-cost-surviving expectancy.
   Recorded as declared assumptions for any future cost-survival layer;
   never operationalized, nothing armed.

7. [source-quality note] arXiv v1 preprint (q-fin.GN), compiled April 6,
   2020, zero recorded citations in the index, no journal version
   recorded. The extract prints seven authors (PDF p. 1) while the index
   lists four (Fang, Chung, Ventre, Basios — Kanthan, Li, Wu omitted).
   Internal count discrepancy: the abstract says "8 cryptocurrency
   pairs" (PDF p. 1) while Table 1 lists 11 products (PDF p. 7). The
   validity section asserts the data selection "has no bias" and the
   experiments are "not affected by bull or bear market, policy impact
   and other factors" (PDF p. 21) — assertions without exhibits, on one
   ~30-hour July 2018 capture plus scattered August 2018 live BTC-USD
   windows from a single exchange. Check before any formal citation;
   regardless, no empirical claim here can serve as support for any
   programme claim.

## What this paper would have killed if we had done it wrong

This is precisely the paper class that would have armed a dead claim under
a weaker discipline. Sample an accuracy figure from the first hours of live
use and it reads 58% and rising (PDF p. 17); sample it from the
retrained-in-window segment and it reads a "consistent" 76-78% (PDF
pp. 1-2, 17, 19); the paper's own Figure 9 (PDF p. 14) shows the
un-retrained truth — decay to almost random guessing — so any of the
flattering numbers survives only by choosing the segment or by silently
re-tuning inside the evaluation window, which the programme's
freeze-then-evaluate and no-re-tune rules exist to forbid. The
universality path is the second kill avoided: run the comparison before
excluding the four failing pairs and "universal features" is not what the
table shows (PDF p. 13); had a C8-adjacent exhibit cited a pooled universal
model as evidence of instrument-invariant structure, the survivorship step
(PDF p. 13) would have been laundered into a finding. The headline itself
is the third: "78% accuracy" with no base rate, no statistical baseline,
and a next-tick horizon below the ±0.2% fee boundary the paper's own
Table 2 (PDF p. 8) sets — an uncosted direction accuracy that its own
validity section never confronts (PDF p. 21).

## Standing caveat

An engineering report on a live GDAX capture, not an out-of-sample
falsification: one exchange, one ~30-hour collection window (PDF p. 6)
plus a handful of August 2018 live BTC-USD windows, a 2018 crypto regime,
no statistical baseline anywhere despite the abstract's claim (PDF p. 1),
no base rates, no cost or tradability analysis, no error bars on any
accuracy curve, and every stabilized accuracy achieved through retraining
schemes that update the model on the stream being scored (PDF pp. 9, 17).
Count discrepancies against the index (seven printed authors, abstract's
"8 pairs" versus Table 1's 11 products, PDF pp. 1, 7) lower the citation
grade further. A library is ammunition, not evidence; this note cites, it
does not launder. Nothing here validates any programme claim on real data,
and nothing here touches C1-L2's or C8's kill lines.
