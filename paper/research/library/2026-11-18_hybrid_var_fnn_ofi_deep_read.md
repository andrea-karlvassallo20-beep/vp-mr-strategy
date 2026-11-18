# Library deep-read session 29 — Rahman & Upadhye, "Hybrid Vector
# Auto Regression and Neural Network Model for Order Flow Imbalance
# Prediction in High-Frequency Trading" (arXiv:2411.08382v1, 2024;
# IIT Madras; VAR for the linear part, FNN on the residuals, on
# 2.8 hours of Binance order data)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x98e019_hybrid_vector_auto_regression_and_neural_network_m.txt`,
~12 pp., page-marked). Next UNREAD triage-rank entry (score 32;
verified unread by the read-slug mapping; cites session 27's
Anantha-Jain paper as alternative approach [13], so the chain
continues).

## The paper in one paragraph

The authors forecast OFI with a hybrid: a VAR captures linear
dependence in (buy, sell) order series, and the VAR residuals are
fed to a small feedforward network (32-16, ReLU, Adam) that models
non-linear patterns; a two-neuron output predicts buy and sell
sides separately, with OFI computed from both, plus a "trading
intensity" side-classification (PDF pp. 1-9). Data: 10,000 seconds
(~2.8 hours) of one cryptocurrency's continuous buy/sell order data
from Binance, with three validation sets of ~3,000 points each
(BTCUSD, ETCUSDT, synthetic); 120 hyperparameter configurations
were evaluated (grid search and Latin Hypercube; PDF pp. 9-10).
Results: the hybrid beats FNN-only and VAR-only on MSE/MAE and R^2
everywhere — most strikingly VAR-only predicts trading-intensity
side at 46.61 percent (BTCUSD) and 50.37 percent (synthetic) — coin
flip — while FNN-only and hybrid reach 95-99 percent, and the
hybrid's R^2 is 0.983-0.999 across all three validation sets
(PDF pp. 10-11, Table 4).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[interpretation caution] Near-perfect next-step OFI "prediction"
   at the second grain is persistence wearing a costume — a
   fine-grain label-window artifact, not information.** The paper
   does not state the exact step-ahead convention, but R^2 = 0.997
   on one-step OFI and 98 percent side-accuracy at second
   granularity is the signature of a highly persistent series
   effectively predicting itself (order flow at second grain is
   strongly autocorrelated; the FNN's input windows and label
   windows share the same drift), while VAR-only at the SAME data
   reads coin flip (46-51 percent) — the 50-point gap between two
   model classes on identical data is a statement about the
   EVALUATION, not the market. For the program this is the
   sharpest specimen yet of why one-step-ahead flow accuracy at
   fine grains licenses NOTHING at 30m-4h horizons: the program's
   label-placebo discipline (null-vs-null) exists to catch exactly
   this class of score. Nothing queued; the discipline already
   covers it, and the closeness-dossier grain (measured session
   34) is a different object entirely.

2. **[reinforcing, no new item] 120 configurations across 3,000-
   point validation sets is selection on noise, quantified.** The
   "best" configuration (lag 2, 32-16-2, ReLU, Adam) was chosen
   from 120 tried on ~3,000 points per set (PDF pp. 9-10); the
   reported winners therefore carry a maximum-of-120 selection
   bias the paper does not discuss. This is the estimator-mode
   family's selection face, the same structure session 27's
   authors at least ADMITTED (their SPA bias caveat): the honest
   comparison protocol the program requires (pre-registered
   models, no post-hoc configuration search on the evaluation
   data) is exactly what this paper lacks.

3. **[reinforcing, no new item] No price, no cost, no edge claim
   anywhere — flow accuracy is treated as an end in itself.** The
   paper predicts OFI and side-intensity; it never asks whether
   the predictions anticipate price, survive costs, or time
   anything. Read against the program's ONE question, the honest
   transcription is: improved predictability of a self-predictive
   object was demonstrated; no kill line for C1-L2 or C8 is even
   addressable. This is the "impressive empirical results" contour
   the house rules route to standing caveats, and it confirms
   rather than challenges the program's refusal to treat fine-
   grain flow accuracy as evidence.

4. **[source-quality note] Thin provenance throughout.** 2.8
   hours of ONE unnamed cryptocurrency as the training set; two
   ~3,000-point validation slices; a synthetic set the hybrid
   scores at 0.999 (the highest number in the paper belongs to
   data the authors generated themselves); "BTCUSD" and "BTCUSDT"
   naming inconsistency across tables; no published version
   located (arXiv v1, November 2024). Citation use: as a specimen
   of the fine-grain persistence artifact and of configuration-
   selection-on-noise — never as an OFI market fact.

## What this paper would have killed if we had done it wrong

If the trigger layer had ever been scored on one-step-ahead flow
accuracy at second grain — the natural "did the features work"
metric — this paper is the existence proof that such a scoreboard
can read 95-99 percent while containing zero timing information at
the horizons C1-L2 and C8 live on: the VAR/FNN gap shows the
metric rewards persistence-modeling, not anticipation. And if any
spec had selected its configuration by grid search on evaluation
windows, the winner would carry the same max-of-120 bias. The
program's label-placebo requirements and pre-registered-model
comparison protocol preclude both failures; the paper is their
cautionary illustration in print.

## Standing caveat

A short applied preprint with unusually small data (10,000 seconds
of training data; 3,000-point validation sets), an unresolved
step-ahead/label-window convention, no statistical significance
testing, no price or economic evaluation, and hyperparameter
search performed on the evaluation sets themselves. Nothing here
survives contact with the program's grain (30m-4h) or venue rules;
nothing is operationalized; nothing trades live.
