# TradeFM: A Generative Foundation Model for Trade-flow and Market Microstructure — deep-read

Library deep-read session 33 (null-time session 37). Maxime Kawawa-Beaudan, Srijan
Sood, Kassiani Papasotiriou, Daniel Borrajo, Manuela Veloso (J.P. Morgan AI
Research, New York), "TradeFM: A Generative Foundation Model for Trade-flow and
Market Microstructure" (arXiv:2602.23784v1, 27 February 2026): a 524M-parameter
decoder-only Transformer trained on billions of US-equity trade events that
generates synthetic order flow evaluated against stylized facts in a
closed-loop deterministic market simulator.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xe7dc7f_tradefm_a_generative_foundation_model_for_trade_fl.txt,
~29 pp., page-marked). Next UNREAD triage-rank entry (score 31).

## The paper in one paragraph

TradeFM is a generative foundation model for market microstructure: a
Llama-style decoder-only Transformer, 524M parameters, trained from scratch on
10.7B trade-event tokens from >9K US equities over 368 trading days, February
2024 through September 2025, with a January-2025-onward temporal hold-out and an
APAC geographic hold-out (China, Japan) (PDF pp. 1, 4). Each trade event is
reduced to scale-invariant features — interarrival time, log-transformed
volume, price depth relative to an Exponentially-Weighted VWAP estimate of the
unobserved mid-price, and price level relative to the day's open — so that a
single model spans assets of vastly different price, liquidity and activity
profiles without per-asset calibration (PDF pp. 4-6). The features are
discretized into bins calibrated on the first 30 days of data only
(February 2024) and composed into a single mixed-radix trade token of
vocabulary 16,384 (PDF pp. 5-6, 20). Generated events are executed in a
deterministic price-time-priority simulator, closing the loop between model
predictions and market state (PDF pp. 7-8). The model is judged not by
perplexity but by stylized-fact reproduction (no return autocorrelation,
volatility clustering, heavy tails, aggregational Gaussianity; PDF pp. 8-9)
and distributional fidelity of order flow against Zero-Intelligence and
Compound Hawkes baselines (PDF pp. 9-10), with claimed 2-3x lower
distributional error than the Hawkes baseline and moderate zero-shot APAC
perplexity degradation (PDF pp. 1, 10-11, 24). The entire result set is
conditional on a proprietary J.P. Morgan tick dataset; no code, data, or
independent replication accompanies the paper (PDF pp. 1, 4, 12-13).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. Tokenizer and bin edges calibrated once, on the first 30 days of the
   training window, then frozen for the whole evaluation horizon, with drift
   between the calibration month and nine held-out months reported openly
   (PDF pp. 4-6, 20, 24-27; Figure 13). [reinforcing, no new item]: this
   corroborates the programme's own pre-fixed-conditioning discipline — every
   bin edge, estimator constant, and windowing choice in a C1-L2-style run
   must be frozen before the first test event and never re-fit inside the
   window. The paper is an industry demonstration that frozen calibration is
   workable at scale; it is not evidence in this programme's record and
   licenses nothing measurable here.

2. Every price feature is normalized against the EW-VWAP estimator — a
   volume-weighted, halflife-smoothed execution-price estimate introduced
   precisely because the true mid-price is unobserved in the partial-trade
   data, and argued by the authors to outperform rolling VWAP and plain EMA
   (PDF pp. 4-5, 15-17). [reinforcing, no new item]: this corroborates the
   already-queued estimator-mode register candidate — the choice of reference
   or estimator mode (rolling window, halflife, volume weighting) is an
   undisclosed degree of freedom that materially moves normalized features,
   and TradeFM is a worked example that a corporate lab's headline
   results are themselves conditional on that choice. Nothing new is
   queued; the existing queued item is unchanged.

3. The closed-loop evaluation admits its own entanglement: the bid-ask
   spread distribution is reproduced worse than by the Compound Hawkes
   baseline because the spread "emerges indirectly from the simulator's
   deterministic order matching logic", and the authors state that "full
   disentanglement [of model quality from simulator fidelity] remains future
   work" (PDF p. 10). [interpretation caution]: any future programme
   diagnostic in which book- or spread-like quantities emerge from simulated
   matching logic rather than from measured data must be read as
   partially an artifact of the simulator's rules, not of the underlying
   signal. For C1-L2 specifically: nothing in this paper tests the
   incrementality of Layer-2 book information over trade-flow information;
   a generative trade-event model reproducing stylized facts through a
   simulator says nothing about whether the real L2 book carries compression
   structure that daily bars cannot see, and must not be cited either way.

4. Scale-invariance is engineered, not discovered: relative (bps) price
   features, log volume, log interarrival time, and a three-bin ADV
   liquidity conditioning token are constructed specifically to enforce
   cross-asset homogeneity (PDF pp. 5-6, 16). [reinforcing, no new item]:
   consistent with the programme's own normalization rules; the paper's
   zero-shot APAC transfer (PDF pp. 10-11, 24) is a corporate empirical
   claim, is ammunition at most, and never enters the record as support for
   any programme claim.

5. The empirical headline numbers (2-3x distributional-error reduction,
  0.91/0.98 simulator-fill correlations, stylized-fact reproduction) rest on
   proprietary data, a proprietary model, and an in-house evaluation
   pipeline, with a JP Morgan disclaimer explicitly denying investment-research
   status (PDF pp. 1, 9-10, 12, 24). [source-quality note]: an industry
   research paper, arXiv v1, no peer-review or journal record checked at
   reading, no code or data release; graded exactly as a source of method
   discipline and caution, not as evidence, and to be re-checked against a
   published version before any formal citation.

## What this paper would have killed if we had done it wrong

Had the one-question discipline been absent, this is the paper most likely to
have quietly demotivated C1-L2 itself: "a 524M-parameter model learns
microstructure from trade flow alone, so what would the L2 book add?" Read
wrong, its stylized-fact reproduction could have been used to argue that
trade-event information suffices, licensing a de facto relaxation of C1-L2's
claim (the compression signal, if any, lives where trade-flow models already
see) — precisely the kind of scope-rot that pre-registered kill lines exist
to prevent. A second, subtler trap: the paper's own admission that spread
fidelity is an artifact of the simulator's matching logic shows how easily
simulator-conditioned "stylized facts" launder into evidence about markets.
The programme's rule that nothing here is evidence, only ammunition, and that
no empirical claim from any paper enters the record, blocks both. A third
trap is normalization envy: adopting EW-VWAP-style estimators or the paper's
bin edges because they worked in a US-equity corporate setting would be an
imported, undeclared degree of freedom — exactly what the estimator-mode and
pre-fixed-conditioning rules exist to force into the open before any window
is touched.

## Standing caveat

All quantitative claims are conditional on a proprietary J.P. Morgan tick
dataset (Feb 2024 through Sep 2025, US equities plus one APAC month), an
in-house model and simulator, and no released code, data, or seeds; results
are not independently verifiable as published. arXiv v1 dated 27 February
2026; no journal or peer-review record checked at reading — check the
published version before formal citation. Scope boundaries: US equities with
a coarse three-bin liquidity conditioning; APAC "generalization" measured only
as perplexity overlap, not distributional fidelity; spreads and book
quantities emerge from the simulator's deterministic matching rules rather
than from measured book dynamics, and model-versus-simulator disentanglement
is explicitly future work by the authors' own admission (PDF p. 10). Laundering
directions named: INTO — only the frozen-calibration discipline, the
estimator-mode disclosure lesson, and the simulator-artifact caution enter as
reading and design discipline. OUT — the 2-3x error figures, the APAC
transfer claim, the stylized-fact reproduction, the EW-VWAP superiority
claim, the tokenization scheme and bin counts are never cited as expected
behavior of any market the programme measures, never as expected BTCUSDT
book behavior, and never as evidence that any programme feature carries
information.
