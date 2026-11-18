# Deep-read session 30 — Abdul Rahman and Upadhye, "Hybrid Vector Auto Regression and Neural Network Model for Order Flow Imbalance Prediction in High-Frequency Trading"

Library deep-read session 30 (null-time session 34, log entry ## 38).
Abdul Rahman and Neelesh Upadhye (Department of Mathematics, Indian
Institute of Technology Madras), arXiv:2411.08382v1 [q-fin.CP],
13 November 2024, 17 pp. text extract, page-marked. Read 2026-11-18,
against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/x98e019_hybrid_vector_auto_regression_and_neural_network_m.txt).
Assigned triage-rank entry (score 32, x98e019). Next UNREAD
triage-rank entry (score 32, xa74970, "Trading in the Sunshine or
in the Shade: Market Impact and Adverse Selection on Hyperliquid").

## The paper in one paragraph

A hybrid forecaster for the same trade-count OFI read through
deep-read session 29: the normalized difference of BUY-classified
and SELL-classified trade counts over a window (eq. (1), PDF
pp. 2-3), explicitly building on Anantha and Jain [13] (PDF p. 3).
A VAR on buy and sell order counts captures linear dependencies, the
residuals are fed to a small feedforward network, and the combined
output forecasts OFI plus a three-way BUY/SELL/HOLD intensity signal
defined by a threshold T close to zero (PDF pp. 3, 5-8). Data:
10,000 seconds of one cryptocurrency's continuous buy and sell order
data on Binance, with three validation datasets of roughly 3,000
points each (BTCUSD, ETCUSDT, synthetic; PDF p. 9); 120 parameter
combinations evaluated manually and via grid search to select lag
order 2, a 32-16-2 network, ReLU, Adam (PDF pp. 9-10). Headline
results: the hybrid beats VAR-only and FNN-only on MSE, MAE, R2 and
intensity accuracy on all three datasets, R2 = 0.997 on BTCUSD,
intensity accuracy 98.18 percent versus 46.61 percent for VAR-only
(Table 4, PDF p. 11), with sample predictions tracking actual OFI to
two or three decimals (Table 5, PDF p. 12). The paper's claim is
that hybrid VAR-FNN modeling is the most effective approach for OFI
prediction in high-frequency trading (PDF p. 1).

## Findings, graded

NO kill line changed. NO new candidate sharpening queued. This is the
default grade: nothing here earns a rule. The read went further: the
results section carries the page-cited signature of target leakage,
recorded here so the paper can never be laundered into the record.

1. **[interpretation caution]** The results are inadmissible as
   evidence. Three page-cited signs, jointly decisive. (a)
   Identity-level predictions: in the sample rows of Table 5, the
   hybrid OFI prediction tracks the actual OFI to within 0.001 to
   0.023 on all six displayed rows (-0.3315 vs -0.3454, -0.9203 vs
   -0.9430, 0.2256 vs 0.2269, -0.1203 vs -0.1221, 0.8431 vs 0.8429,
   -0.5581 vs -0.5616; PDF p. 12): second-scale OFI values
   reconstructed to three decimals are not forecasts, they are the
   label. (b) The linear backbone carries nothing: the appendix VAR
   regression summary shows every lag coefficient statistically
   zero (L1.buy_orders 0.0038, p 0.706; L1.sell_orders 0.0111,
   p 0.268; L2.buy_orders -0.0005, p 0.957; L2.sell_orders 0.0168,
   p 0.095; Appendix A.1, PDF p. 15), and VAR-only validation R2 is
   -0.002 on BTCUSD (Table 4, PDF p. 11) — so the near-perfect
   hybrid metrics cannot come from lag structure that does not
   exist; the network output must overlap the target window. (c) No
   chronological split is ever declared: the paper states training
   and "validation" loss curves as evidence of generalization
   (Appendix A.4, PDF p. 17) without ever saying the validation data
   are later in time than the training data, and the three
   validation datasets are separate slices, not declared holdouts
   (PDF p. 9). Every headline number (R2 0.997, 98.18 percent
   intensity accuracy, Table 4, PDF p. 11) is therefore not cited by
   the record, for any purpose, ever.

2. **[reinforcing, no new item]** Ammunition for the programme's
   leakage-hunting culture. The paper is a worked specimen of
   precisely what the record's discipline exists to catch:
   unlabelled train-test mixing, predictions indistinguishable from
   labels, a missing persistence baseline, 120 hand-evaluated
   parameter combinations with no multiple-testing discussion
   (PDF p. 9), and prose that upgrades "slightly better performance
   metrics" (PDF p. 5) into "significant improvements" (abstract,
   PDF p. 1). Corroborates — by counterexample — why the
   deliberately-flawed examples of the leakage-resistant backtester
   and the K1 costume guard exist. No rule is extended; the
   programme's discipline already covers this failure class.

3. **[reinforcing, no new item]** The OFI name collision repeats and
   closes the count-family bracket opened at deep-read session 29.
   The quantity is again trade-count asymmetry (eq. (1), PDF
   pp. 2-3) with Anantha and Jain [13] as the direct predecessor
   (PDF pp. 3-4), not the Cont-Kukanov-Stoikov depth-change OFI of
   the record's line; nothing in either session transfers onto the
   CKS-family measurements. The one small consistency point for the
   record: a VAR-only R2 of -0.002 on one short crypto sample
   (Table 4, PDF p. 11) squares with session 29's finding that
   nothing strong was demonstrated at this grain, but it rides on
   the same undocumented evaluation and is corroboration of nothing.

4. **[source-quality note]** Two authors, IIT Madras mathematics
   department, no stated practitioner affiliation; arXiv v1 only,
   stamped 13 November 2024, no journal record checked; zero
   indexed citations as of the session date. Internal naming
   inconsistency: the datasets are declared BTCUSD and ETCUSDT
   (PDF p. 9, Table 4, PDF p. 11) but the narrative and figures from
   PDF p. 12 onward call them ETHUSDT, and the limitations section
   repeats the error (PDF p. 13), so it is undetermined which pair
   was actually used; BTCUSD versus BTCUSDT likewise. The appendix
   GitHub repository link is a placeholder, not a link (PDF
   p. 17). The intensity threshold T is never given a value ("close
   to zero", PDF p. 3; Table 1 implies T above 0.059, PDF p. 3), a
   reproduction blocker. The claim that trade classification can be
   "deterministically inferred by tracing the origin of the passive
   order" (PDF p. 2) mirrors the NSE order-number mechanism from
   session 29's paper and does not describe Binance's data model,
   where the taker side is a native flag on the aggTrades stream.
   Extract page-marked and clean; the appendix regression summary
   (PDF p. 15) is the paper's most honest page. Published version to
   be checked before any formal citation; as it stands the paper
   would not survive the programme's haircuts.

## Killed if wrong

Nothing in the record rests on this paper: no rule was added or
amended on its basis. If the leakage reading is wrong and the
authors produce a genuinely chronological holdout under which
R2 = 0.997 survives, the record's obligations would still be
unchanged: any such result would have to be re-measured on the
programme's own tape under the programme's own protocols before
anything could move, and until then this note's inadmissibility
judgment stands. Conversely, if the leakage reading is right and the
paper is later published as-is, it becomes a named specimen of
publishable leakage, reinforcing the record's refusal to accept
headline metrics from any source that does not declare its holdout:
that refusal is already the rule, and this paper is why.

## Standing caveat

10,000 seconds of one cryptocurrency on Binance, roughly 2.8 hours,
single regime; three validation slices of about 3,000 points per
dataset; the data stream (aggTrades, matched trades, or
constructed counts) is never specified; threshold T undeclared; no
costs, no execution, no P&L, no strategy beyond the three-way
signal; no equities, no NSE, no L2 depth of any kind. Laundering
directions named. INTO: no architecture, no hyperparameter, no lag
order, no threshold, no metric, no R2, and no accuracy figure from
this paper enters any spec, default, or calibration, and the hybrid
VAR-FNN construction is not adopted anywhere without its own
pre-registration under the programme's holdout rules. OUT: the R2
values and intensity accuracies are never cited as evidence that
OFI of any definition is predictable at high frequency, never as
evidence that hybrid models beat standalone models, never as
expected BTCUSDT behavior, and never as evidence about any market
the programme measures.
