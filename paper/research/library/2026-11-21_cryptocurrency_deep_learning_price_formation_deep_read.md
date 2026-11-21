# Deep-read note — session 75: "Ascertaining price formation in cryptocurrency markets with Deep Learning" (Fang–Chung–Ventre–Basios, arXiv:2003.00803v1)

**Deep-read session 75** (null-time session 86). Fan Fang, Waichung Chung, Carmine
Ventre, Michail Basios (author block completed by Leslie Kanthan, Lingbo Li and
Fan Wu), "Ascertaining price formation in cryptocurrency markets with Deep
Learning" (title printed with no space in "Deep Learning" in the header and the
triage index), arXiv:2003.00803v1 [q-fin.GN], arXiv stamp 9 February 2020,
article-history field "Compiled April 6, 2020". An applied deep-learning paper
predicting the direction of the next-tick mid-price change in cryptocurrency
limit order books, with a walkthrough-retraining scheme designed to fight the
accuracy decay the authors themselves observe on live data.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xe0397d_ascertaining_price_formation_in_cryptocurrency_mar.txt,
22 pp., page-marked), read in full including the references. Second UNREAD
triage-rank entry of the score-24 tier (score 24, xe0397d), after x673148
(read ## 94), under the edition-7 queue recomputation (## 95).

## The paper in one paragraph

The authors record live tick-level data from the GDAX (Coinbase Pro) WebSocket
API — ticker data, level-2 order-book updates (top 50 aggregated depths) and
order flow, for eleven currency pairs, from 2018-07-02T17:22:14Z to
2018-07-03T23:32:53Z, roughly 30 hours, 40.95M level-2 records and 61.9M
order-flow records (PDF pp. 6-7, Table 1 p. 7) — and train a small LSTM (two
LSTM layers, one fully connected layer, softmax) to predict the next-tick
mid-price direction (Fig. 3, PDF p. 7), alongside a four-label variant whose
"sensitive interval" boundaries are set at ±0.2% of the transaction price,
copied from the Coinbase fee schedule (Table 2, PDF pp. 7-8). Their
walkthrough-training idea retrains the model during evaluation, either at a
stable fixed cadence or dynamically whenever a "Modified MDD" computed from
the model's own running accuracy exceeds 15% (PDF pp. 8-9). Findings, by
research question: product-specific LSTMs improve with training-set size at
most splits (Table 3, PDF p. 11); a "universal" model pooled across pairs
beats the mean of product-specific models by 3.65%, or 4.25% after the four
worst pairs are excluded post hoc (Table 4, PDF p. 13); sweeping time steps
1 through 40 yields OLS accuracy slopes of −0.0001/−0.0002, so "one time
step is the best choice" (Tables 5-6, PDF p. 14); on live data the universal
model's accuracy decays to almost random guessing (Fig. 9, PDF pp. 14-15),
an autoencoder denoiser slows the decay (Figs. 11-12, PDF pp. 15-16), and
stable walkthrough retraining (every 196 predictions) lifts live BTC-USD
accuracy from below 50% through 58% to 78%, stabilizing near 76% (Fig. 13,
PDF p. 17), with the reduced architecture reaching the headline 78% average
accuracy (Table 7, PDF pp. 18-19); in the multi-label experiment the static
model falls below 40% against a 25% random floor while walkthrough
retraining stabilizes near 80% (Figs. 16-17, PDF pp. 19-20). The validity
section claims the data selection "has no bias" and covers bull, bear, high-
and low-volume conditions (PDF p. 21).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION (the adaptive-retraining disclosure, below). Nothing measured,
nothing armed, nothing trades live.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   adaptive-retraining disclosure: before the L0 gate, any C1-L2/C8-adjacent
   comparator, null, or baseline that adapts — retrains, re-tunes,
   re-estimates or re-selects — inside its own evaluation window must
   pre-declare the adaptation rule (trigger, data consumed, cadence) in the
   same pre-registration as its frozen configuration, and must report the
   frozen-configuration number side-by-side with the adapted number; a
   number that exists only after its model has consumed the evaluation data
   may not enter any spec as support. The paper proves the mechanism is
   real, on both sides of the comparison: the universal LSTM decays to
   almost random guessing on live data (Fig. 9, PDF pp. 14-15); the headline
   78% live accuracy exists only under walkthrough retraining that consumes
   the live data every 196 predictions — below 50% before the first
   retrain, lifted through 58% to 78%, stabilized near 76% (PDF p. 17;
   Table 7, PDF pp. 18-19); the static multi-label model falls below 40%
   against a 25% random floor (PDF p. 19); and the retrain trigger itself
   is analyst-tuned, not data-driven ("Modified MDD" over 15%, PDF p. 9).
   An adapted-in-window comparator whose apparent competence is
   manufactured by eating the evaluation stream would otherwise pass as an
   honest baseline, and an adapted-in-window null would "track" any regime
   change by construction and could never refute anything. Harder-to-pass
   because an adapted number that beats the data only after consuming it
   now fails at the gate instead of surviving as a baseline. Tightens the
   estimator-configuration freeze by extending the pre-commitment from
   WHICH estimator in WHICH configuration to WHICH adaptation rule — the
   same declaration axis as the dynamics-identification rule for generative
   nulls (a refutation instrument may not silently change during the
   refutation). QUEUED, not armed; the owner's word is the only trigger.

2. [reinforcing, no new item] The 78% headline carries no persistence null
   and no class base rates anywhere in the paper: every reported number
   (Table 3, PDF p. 11; Table 7, PDF pp. 18-19) is a pooled accuracy, the
   "up" support of 5,265 against "down" support of 4,927 in Table 7 is the
   only class-count evidence printed, and no last-sign repeat null is ever
   computed, so an unknown fraction of the headline is mechanical
   sign-persistence before any book state enters. The sign-persistence
   admission null's family, page-cited re-exhibited; no new item.

3. [reinforcing, no new item] The paper's own time-step experiment shows
   the information is in the current tick, not the memory: sweeping time
   steps 1 through 40 (Table 5, PDF p. 14) yields OLS slopes of −0.0001 and
   −0.0002 with intercepts 0.7166/0.7406 (Table 6, PDF p. 14), and the
   paper's own answer is that one time step is the best choice (PDF p. 14)
   — the sequence carries nothing beyond the level. The level-versus-
   memory disambiguation's axis, re-exhibited on the machine-learning side;
   no new item.

4. [interpretation caution] The "universal beats specific" conclusion is
   partly manufactured by exclusion and confounded by size: the four worst
   pairs (BCH-EUR, BTC-GBP, ETH-EUR, BTC-EUR — all at or below roughly
   0.56 accuracy at most splits, Table 3, PDF p. 11) are dropped post hoc
   "for more precise and targeted analysis" (PDF pp. 12-13), and the paper
   itself names the pooled training-set size as part of the explanation
   for the universal model's gain (PDF p. 13), so the universality claim
   conflates a possible real cross-pair effect with an analyst's sample
   selection and a data-size effect that never was decomposed. Any
   C8-adjacent exhibit citing universal-over-specific performance as
   evidence of shared structure would be citing an analyst property;
   reading discipline only, no queue change.

5. [cost-survival ammunition] The multi-label class geometry is the fee
   schedule: the ±0.2% "sensitive interval" boundaries are copied from the
   Coinbase Pro fee table (Table 2, PDF pp. 7-8), so the labels are
   fee-relative by construction, and the decision maker that would turn
   predictions into orders is explicitly "left to future research"
   (PDF p. 6) — no backtest, no PnL, no fees inside the evaluation
   anywhere. A future K7-style cost-survival layer must take its
   pass/fail thresholds from live, per-window fee and rebate schedules
   declared in advance, not from a hand-copied constant; recorded as a
   declaration requirement only, never operationalized, nothing armed.

6. [reinforcing, no new item] Base-rate and validity audit: all live
   evidence comes from one exchange, one summer, effectively one name —
   the recorded corpus is roughly 30 hours of GDAX (2018-07-02 to
   2018-07-03, PDF p. 6), the live experiments use two BTC-USD windows of
   2018-08-01/08-02 and 2018-08-08/08-09 (PDF pp. 15, 17) and one
   randomly-selected one-month 1-minute window (PDF p. 19) — yet the
   validity section claims the selection "has no bias" and that the
   experiments cover bull, bear, high-volume and low-volume conditions
   (PDF p. 21), an overclaim no 30-hour single-venue recording can carry.
   The base-rate audit family; no new item.

7. [source-quality note] arXiv v1 (q-fin.GN), zero recorded citations in
   the index, no journal version recorded, industry co-authors (Turing
   Intelligence Technology), and an internal inconsistency worth a
   check: the article-history field reads "Compiled April 6, 2020" against
   the arXiv stamp of 9 February 2020 (PDF p. 1) — check the publication
   trail before any formal citation; regardless, no claim here can serve
   as support for any programme claim.

## What this paper would have killed if we had done it wrong

Without an adaptive-retraining disclosure, a retrained-in-window deep
comparator is exactly the baseline a hungry C1-L2 spec would grab first:
the paper's own static universal model is near-random on live data
(Fig. 9, PDF pp. 14-15), and the 78% headline exists only because the model
is retrained every 196 predictions on the same live stream it is being
scored against (PDF p. 17; Table 7, PDF pp. 18-19). Had a candidate L2
feature been benchmarked against such a comparator, the feature would look
strong against a moving target whose competence was manufactured inside
the evaluation window, and the sealed-prediction record would have spent
weeks resolving an artifact of the baseline's self-adaptation instead of
any property of the book. The trap arms the null side too: a generative
null or placebo re-fitted mid-evaluation tracks whatever regime arrives by
construction and can never refute the structure it was built to kill. The
disclosure forces both sides to declare their adaptation rule before the
data and to carry the frozen-configuration number beside the adapted one,
so the comparison is between declared objects, not between one frozen
object and one that moved.

## Standing caveat

Single exchange (GDAX/Coinbase Pro), 2018 crypto regime, top-50 aggregated
level-2 depth only; the recorded corpus spans roughly 30 hours (PDF p. 6)
while the live experiments run on August 2018 windows whose relation to the
recorded corpus is not fully specified; the architecture, the optimizer
choice (RMSprop, adopted after observing Adam overfit, PDF p. 5), the retrain
cadence (196 predictions, PDF p. 17) and the 15% Modified-MDD trigger
(PDF p. 9) are analyst choices, never swept or justified beyond eyeball;
no error bars, no statistical tests, no trading simulation and no fees
anywhere in the evaluation; the no-bias / bull-and-bear coverage claimed
in the validity section (PDF p. 21) is not supported by the windows the
paper itself describes. arXiv-version caution: v1, "Compiled April 6, 2020"
against the 9 February 2020 arXiv stamp, unpublished trail — check before
formal citation. Nothing here validates any model beyond one venue and one
era, and the headline number is an adapted-in-window metric by the paper's
own construction.
