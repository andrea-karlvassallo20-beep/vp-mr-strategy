# Deep-read session 33 — Kawawa-Beaudan, Sood, Papasotiriou, Borrajo and Veloso, "TradeFM: A Generative Foundation Model for Trade-flow and Market Microstructure"

Library deep-read session 33 (null-time session 37, log entry
## 41). Maxime Kawawa-Beaudan, Srijan Sood, Kassiani Papasotiriou,
Daniel Borrajo and Manuela Veloso (J.P. Morgan AI Research, New
York), arXiv:2602.23784v1 [cs.LG], stamped 27 February 2026, 29 pp.
text extract, page-marked. A 524M-parameter decoder-only Transformer
trained on over 10 billion tokens of raw US-equity trade events
(across more than 9,000 tickers, February 2024 to September 2025),
combined with a deterministic order-book simulator into a closed-loop
generative market model: it generates synthetic order flow and prices,
and is validated by stylized-fact reproduction and distributional
fidelity, not by any predictive or edge claim. Read 2026-11-19,
against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/xe7dc7f_tradefm_a_generative_foundation_model_for_trade_fl.txt).
Assigned triage-rank entry (score 31, xe7dc7f), the standing queue
pointer from null-time session 36.

## The paper in one paragraph

A foundation-model paper, not a microstructure claims paper: raw
trade events (interarrival time, price depth in bps relative to an
estimated mid, log volume, side, add-or-cancel action) are
discretized into a mixed-base composite token (vocabulary 16,384) with
bin edges calibrated on the first 30 days of the training window and
outliers beyond the 1st/99th percentiles assigned to special bins (PDF
pp. 5-7, 20), and a Llama-style decoder with 1,024-token context is
trained on 10.7B tokens to predict the next composite event, with
liquidity-tier, price-level-vs-open and market-vs-participant
indicators as non-predicted conditioning inputs (PDF pp. 6-7, 18). The
unobserved mid-price in this trade-only, partial-observability setting
is replaced by an Exponentially-Weighted VWAP, a ratio of two EMAs
with a time-based halflife, chosen so the normalizing benchmark is
comparable across assets with very different liquidity (PDF pp. 4-5,
15-16). Scale-invariance is the explicit design thesis: relative
(bps) price features, not tick-based depths, give distributional
stationarity across liquidity tiers and across a year of regime change
(Figures 7 and 12, PDF pp. 15, 24-25). Closed-loop with a price-time
priority simulator, generated rollouts reproduce absent return
autocorrelation, volatility clustering and heavy tails (PDF pp. 8-9),
with 2-3x lower K-S distance to real return distributions than a
Compound Hawkes baseline and a calibrated Zero-Intelligence null
(Table 2, PDF p. 9), and lower distributional distances on most
order-flow quantities, with the Hawkes baseline still winning on
bid-ask spreads (Table 3, PDF p. 10). Perplexity degrades only
moderately zero-shot on held-out China and Japan markets with
different auction mechanisms, price limits and spread scales (PDF
pp. 10-11, 24). The stated purposes are synthetic data generation,
counterfactual stress testing and RL agent training (PDF pp. 26, 29);
nothing anywhere in the paper claims directional predictability, an
edge, or information content in any feature, and the validation is
entirely distributional, never conditional-predictive.

## Findings, graded

NO kill line changes. NO new candidate sharpening.

1. **[reinforcing, no new item]** Scale-invariant relative features
   are shown to be the load-bearing design choice, an independent
   corporate-scale corpus for the already-queued scale-constant
   declaration. Distributions of the same feature (price depth,
   price-level-vs-open) constructed in ticks differ wildly across
   liquidity tiers while the bps-relative construction is
   distributionally stationary, across more than 9,000 assets and
   across a full year separating the tokenizer calibration month from
   the comparison month (Figure 7, PDF p. 15; Figure 12, PDF pp.
   24-25; Figure 13 drift check with raw mid-price included as the
   non-stationary control). The paper's own framing is that
   asset-specific calibration is eliminated by constructing
   unit-relative features before any learning happens (PDF p. 5).
   This corroborates the standing discipline that C1-L2 features
   quoted in tick or nominal units import venue-specific price-grid
   structure and must carry a declared scale convention; nothing new
   is queued because that declaration is already standing in the
   ratification queue (scale-constant, among the twenty-six). No bin
   edges, bin counts, halflife, or liquidity-tier boundaries transfer.

2. **[reinforcing, no new item]** The mid-price in a trade-only view
   is an estimator, not an observation, and the estimator's convention
   (two coupled EMAs, a declared time-based halflife) is exactly the
   disclosed-degree-of-freedom the queued estimator-mode component
   guards. The paper is explicit that execution prices are a noisy
   surrogate, that window-based VWAP is not comparable across
   liquidity regimes, and that every price-relative feature in the
   entire model is normalized by this estimated reference (PDF pp.
   4-5, 15-16, Figure 8 p. 17). Second corpus for the premise that a
   feature anchored to an estimated mid inherits the estimator's
   convention and must declare it. The L2 arm of C1-L2 observes the
   book directly, so this reinforces rather than extends: no new
   item.

3. **[interpretation caution]** Stylized-fact reproduction is a weak
   validity bar and must never be read as information content. The
   headline result of the paper is that a purely generative model with
   no directional claim reproduces absent autocorrelation, volatility
   clustering, heavy tails and aggregational Gaussianity (PDF pp.
   8-9); crucially the calibrated Zero-Intelligence null, which
   models nothing, reproduces parts of the applied record and fails
   others (spurious autocorrelation, PDF p. 9), which is the same
   logic as the C8 Hawkes shuffled-arrival placebo: the null-model
   arm exists because matching marginals is not matching mechanism.
   Applied to the programme: any future simulation, bootstrap or
   synthetic-data artifact whose validation is "it reproduces
   stylized facts" has passed only a marginal-distribution test;
   reproduction of absent return autocorrelation is in particular
   compatible with zero predictive information and can never be
   cited as evidence that a C1-L2 or C8 feature carries a
   compression signal.

4. **[interpretation caution]** Perplexity and distributional
   fidelity are not predictive content. The out-of-distribution
   results are perplexity distributions (Figure 5, PDF p. 10) and
   K-S/Wasserstein distances between real and generated marginals
   (Tables 2-3, PDF pp. 9-10); no experiment in the paper conditions
   on the model's output to predict realized returns, and the
   authors themselves flag that the closed-loop evaluation couples
   model quality with simulator fidelity and that full
   disentanglement remains future work (PDF p. 10). Zero-shot
   geographic generalization demonstrates smoothness of the learned
   representation across venues, not transferability of any edge.
   The 2-3x improvement over Compound Hawkes is a generative-fidelity
   ranking; treating it as an information ranking would be a
   laundering move. Neither the numbers nor the ranking ever enter
   any spec.

5. **[cost-survival ammunition]** The paper's D.4-D.6 agenda
   (synthetic-data backtesting, counterfactual stress injection,
   RL-execution training, PDF pp. 26, 29) names, in industry form,
   the failure mode a future cost-survival layer must forbid:
   validating a strategy on generated rollouts substitutes the
   generator's smoothed distribution for the market's tail and
   quietly removes the adversarial part of execution. Should a
   K7-style layer ever exist, any simulator-based cost or impact
   assumption must carry: (a) simulator fidelity is itself validated
   only as fill-volume and lot-count marginals here (correlations
   0.91 and 0.98, PDF p. 24), never in stressed conditions; (b)
   generated spread behavior is the paper's own acknowledged weak
   point, with the Hawkes baseline beating it on spread K-S (Table 3,
   PDF p. 10), so synthetic-rollout cost estimates inherit
   simulator spread artifacts. Declared now as assumptions that layer
   would have to carry; the layer does not exist, so nothing
   operational is touched.

6. **[source-quality note]** An industry research report (J.P.
   Morgan AI Research) posted as arXiv v1 in February 2026, unreviewed
   at reading, zero recorded citations at acquisition; the carry-along
   JPMorgan disclaimer states the document is not research, not
   advice, and not a solicitation (PDF p. 12). The training data is
   proprietary and private (billions of raw US-equity transactions,
   PDF pp. 4, 17-19), so no figure in the paper is reproducible
   end-to-end; the reproducibility guide covers architecture and
   tokenizer pseudocode, not data (PDF pp. 18-23). Triage score 31
   is an access-value rank; the paper was ranked right next to the
   Hawkes-Markovian queue paper read at session 32 and is a
   solid, well-disclosed engineering paper whose content is
   generative fidelity in US equities; it contains no claim-bearing
   material for C1-L2 or C8 and is graded exactly at that level.
   Check for a published or journal version before any formal
   citation. The APAC zero-shot evaluation covers Japan's Itayose
   opening and China's price limits (PDF pp. 10-11), never crypto,
   never BTCUSDT, never anonymous flow.

## What this paper would have killed if we had done it wrong

If the programme had allowed "a large model learned universal market
structure" to serve as support for any claim, the closed-loop numbers
here are precisely the kind of impressive artifact that launders
nothing into something: a 524M-parameter model, a 2-3x fidelity
improvement over a Hawkes baseline, zero-shot transfer across
geographies, and not one sentence anywhere claiming that any feature
predicts anything. The record's rule that the library is ammunition,
not evidence, plus the null-model placebo discipline in C8, is what
keeps fidelity metrics and perplexity gains from being misread as
information content. The second half of the counterfactual: if a
future cost-survival or stress layer had adopted the paper's synthetic
rollout agenda at face value, cost and impact estimates would rest on
a simulator whose spread behavior the paper itself concedes is its
weakest fidelity point, and the resulting net-of-cost numbers would
look conservative while quietly embedding the generator's smoothed
tails. Declaring those assumptions now (finding 5) is the inoculation;
they are declared, not adopted.

## Standing caveat

US equities, proprietary tick data, 368 trading days February 2024 to
September 2025, trade messages only (partial observability by design),
simulated price-time-priority matching in a toy book; the APAC
generalization check is one month (January 2025) of perplexity only.
No crypto, no BTCUSDT, no order-book-native data as input to the
model, no stressed-market validation, and no predictive experiment
anywhere. All bin edges, bin counts (16 per continuous feature),
percentile outlier cuts (1st/99th), tokenizer calibration window (30
days), halflife, liquidity-tier cuts (3) and training hyperparameters
are dataset- and venue-specific choices of the authors. Laundering
directions named. INTO — only the two corroborations above (relative
feature construction, estimated-reference convention) and the two
cautions enter the record as feature-design discipline. OUT — the
fidelity tables, perplexity figures, scaling-law exponents,
geographic-transfer claims, simulator design, and every synthetic
data, RL and stress-testing proposal are never cited as expected
behavior of any market the programme measures, never as expected
BTCUSDT behavior, and never as evidence that any programme feature
carries information.