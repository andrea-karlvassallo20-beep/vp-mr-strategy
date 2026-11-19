# Deep-read session 33 — Kawawa-Beaudan, Sood, Papasotiriou, Borrajo and Veloso, "TradeFM: A Generative Foundation Model for Trade-flow and Market Microstructure"

Library deep-read session 33 (null-time session 37, log entry
## 41). Maxime Kawawa-Beaudan, Srijan Sood, Kassiani
Papasotiriou, Daniel Borrajo and Manuela Veloso, J.P. Morgan AI
Research, New York, arXiv:2602.23784v1 [cs.LG], 27 February 2026,
29 pp. text extract, page-marked. Read 2026-11-19, against
ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/xe7dc7f_tradefm_a_generative_foundation_model_for_trade_fl.txt).
Next UNREAD triage-rank entry (score 31, xe7dc7f), after the
Order Book Queue Hawkes-Markovian paper of deep-read session 32.

## The paper in one paragraph

A 524M-parameter decoder-only transformer (Llama-family backbone,
GQA, RoPE, 1,024-token context) trained from scratch on over 19
billion composite tokens from more than 9K US equities across 368
trading days, February 2024 to September 2025, with January 2025
onward held out for test (PDF pp. 1, 3-4, 18). Trade events
(interarrival time, price depth in bps, log volume, action, side)
are normalized into scale-invariant features relative to an
Exponentially-Weighted VWAP mid-price estimate, then discretized
into a mixed-base composite token of vocabulary 16,384, with
liquidity-tier, market-versus-participant and price-level-change
context tokens (PDF pp. 4-7, 16-17). The model's rollouts are fed
through a deterministic price-time-priority order-book simulator
in a closed loop (PDF pp. 7-8, 21-22), and evaluation is entirely
distributional: reproduction of stylized facts (near-zero return
autocorrelation, volatility clustering, heavy tails, aggregational
Gaussianity, PDF pp. 8-9); K-S and Wasserstein distances on return
and order-flow distributions against a calibrated Zero-Intelligence
agent and a Compound Hawkes baseline, with TradeFM at 2-3x lower
K-S distance on returns but the Hawkes baseline better on spreads
(PDF pp. 9-10, Tables 2-3); zero-shot geographic generalization to
China and Japan shown only as overlaid perplexity distributions
(PDF pp. 10-11, 24); and controllability of conditioning tokens
shown as volume and interarrival dispersions moving in the expected
direction with the liquidity and market-versus-participant tokens
(PDF pp. 10-11, 29). No return-prediction, forecasting-accuracy or
economic-value claim is made anywhere; the closing pitch is synthetic
data, stress testing and agent training (PDF p. 11, pp. 26-29).

## Findings, graded

NO kill line changed. ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION.

1. **[candidate sharpening, PENDING OWNER RATIFICATION]** The
   normalization-reference filter-disclosure component, a sibling
   of the queue-label convention declaration component queued
   through deep-read session 32 (both still PENDING OWNER
   RATIFICATION), covering reference-normalized features in the
   C1-L2 L2 arm and any future reference used by a conditioning or
   feature functional. Mechanism, page-cited: every price-related
   feature in this pipeline (price depth, price level versus
   open) is normalized by a filtered reference price, the
   EW-VWAP of execution prices, defined as the ratio of two EMAs
   of volume-weighted price and volume (PDF pp. 4-5), with the
   recency-volume weighting governed by a smoothing factor alpha
   "determined by a time-based halflife" (PDF pp. 5, 15-16) whose
   value is never stated anywhere in the paper; the estimator is
   advertised as more stable and responsive than VWAP or EMA at
   unstated time scales (PDF p. 17, Figure 8), and the tokenized
   depth bin of every event depends on it (PDF pp. 16-18, A.4).
   The halflife is therefore an undisclosed degree of freedom
   upstream of every normalized feature: two implementations of
   the same declared feature with different halflives read
   different depths, different bins, and different conditioning
   states from the same tape, and the divergence concentrates in
   exactly the thin-liquidity stretches where few prints inform
   the estimate and where any microstructure signal is most
   likely to live. The paper itself demonstrates the stakes of
   reference choice by devoting Appendix A.3 to arguing that the
   reference construction is not innocuous across liquidity
   regimes (PDF pp. 15-16). Consequence for the queued family,
   harder to pass: a feature can satisfy a reference-construction
   declaration (it declared "the EW-VWAP of prints" or "an EMA of
   mids") while still hiding a free smoothing clock that
   survives every admissibility gate and invites post-hoc
   selection among equally "declared" implementations. One
   pre-declaration. Normalization-reference filter disclosure:
   whenever an admissible feature or conditioning state
   normalizes prices through a filtered reference (EWMA, EW-VWAP,
   or the declared family), the pre-registration must declare,
   recorded on TRAIN before L2 data arrives, the filter family
   and its smoothing parameter (halflife or decay constant); no
   post-hoc halflife selection, and normalized readings with
   undeclared smoothing parameters are inadmissible. Features
   anchored entirely to unfiltered feed-native prices satisfy
   the declaration trivially, and if every admissible feature on
   the programme's venue and fields is price-raw, the component
   guards nothing on that route and stays dormant there. Scope:
   the pending declaration family only, a disclosure
   requirement; the C1-L2 spec, its kill lines, T-H and T-O,
   and every amendment remain untouched; no threshold moves;
   nothing is armed.

2. **[reinforcing, no new item]** Scale-invariant relative
   features over tick-denominated ones. The paper's Figure 7
   argument is that tick-based depths fragment into
   liquidity-specific distributions while relative (bps)
   depths homogenize (PDF pp. 5, 15), and its drift appendix
   shows the relative features holding their distributions
   from the calibration month to a year later while raw
   mid-price drifts (PDF pp. 24-26, Figures 12-13). This is a
   second corpus-level corroboration of the flow-clock
   scale-constant and normalization-declaration family
   already standing in the ratification queue: any
   tick-denominated feature on the programme's venue is a
   liquidity-regime proxy by accident and must carry its
   normalization as a declared convention. No parameter
   transfers; the paper's specific bin choices (16 bins,
   quantile versus log-width) never enter the record.

3. **[interpretation caution]** Distributional realism is not
   predictive content, and the paper never claims it is. Every
   quantitative headline (2-3x lower K-S than Compound Hawkes,
   Table 2, PDF p. 9; superior fidelity on most order-flow
   quantities, Table 3, PDF p. 10) is a distance between
   marginal distributions of generated versus real data, with no
   forecasting test, no information coefficient, no economic
   value anywhere; the authors even set next-token perplexity
   aside in favor of stylized facts because of non-stationarity
   (PDF p. 8). Applied to the record: a generative model's
   realism metrics can be cumulative-edit-distance bookkeeping
   of the highest quality and still license nothing about
   whether any programme feature carries information. TradeFM
   is never citable as evidence for any programme claim, and
   its reported numbers are not transferable to any kill line.

4. **[interpretation caution]** The closed-loop results are
   simulator-entangled, and the authors say so plainly. The ZI
   control through the identical simulator fails the stylized
   facts while TradeFM passes them, and Table 3 evaluates order
   flow before simulator interaction, but the authors state that
   full disentanglement of model quality from simulator fidelity
   remains future work (PDF p. 10); the simulator itself is
   validated only as fill-volume and lot-count CDFs against
   replayed real orders, correlations 0.91 and 0.98 (PDF p. 24).
   Any future programme use of a learned simulator (there is
   none planned) inherits this confound, and any synthetic-data
   appendix to a future test must carry its simulator-fidelity
   provenance as a declared assumption.

5. **[reinforcing, no new item]** Aggregate-versus-participant
   flow differ in dispersion by construction, and the model
   reproduces this only because it is told which context it is
   in via the IMP token (PDF pp. 6, 10-11, Figure 6). This
   corroborates the standing discipline that market-level
   aggregates and participant-level sequences are different
   objects requiring declared context: a feature computed on
   aggregated flow must declare its aggregation level on TRAIN,
   the same spirit as the pending conditioning declarations. No
   new item; the paper's conditioned dispersions never transfer.

6. **[cost-survival ammunition]** Recorded only for a future
   K7-style cost-survival layer, none of which exists: the
   paper's stress-test and RL-execution sections (10x injected
   order flow moving mid-price plausibly, PDF pp. 26, 29; RL
   fine-tuning against the closed loop, PDF p. 29) are
   execution-strategy engineering. By the ritual's own rule
   they enter as standing context never operationalized: nothing
   trades live, no execution logic is adopted, and the observed
   mid-price response to injected flow in a toy simulator with
   no queue-depth state (PDF pp. 21-22) is not a venue-calibrated
   impact model under any future cost assumption.

7. **[source-quality note]** Corporate research (J.P. Morgan AI
   Research) on entirely proprietary tick data that no outside
   reader can access; arXiv v1 stamped 27 February 2026, under
   three months old at reading; no journal record or peer review
   at reading; the headline generalization result (zero-shot
   APAC) is presented as overlaid perplexity histograms with no
   numeric summary (PDF pp. 10-11); the spread-fidelity loss to
   the Hawkes baseline is honestly disclosed (PDF p. 10). A
   credible, briskly written engineering report whose empirical
   claims are unverifiable from outside the institution; graded
   exactly at that level, and the published version must be
   checked before any formal citation. Triage score 31 is an
   access-value rank, not a promise.

## What this paper would have killed if we had done it wrong

If the programme had treated a filtered reference price as a
neutral plumbing choice, it could have built a family of
"declared" depth-normalized features whose mutual disagreement is
dominated by an unstated halflife, then selected among them
post hoc on the L2 window, exactly the undisclosed-degree-of-freedom
failure the queue-label convention component forecloses for level
indexing. The failure would be invisible to every
within-measurement check: conservation identities pass, the
reference construction reads as declared, and the sign guard sees
well-formed features; two honest implementations would report two
different results from the same tape and the louder one would win.
The second trap this paper pins: on reading "foundation model
reproduces stylized facts with 2-3x lower distributional error,"
a programme without the library-is-ammunition-not-evidence rule
could import a generative-realism number as if it were a
prediction-of-returns number. The record avoided both by
discipline already standing: pre-declaration of construction
conventions before the data arrives, and the laundering caveat
that no empirical claim from any paper ever enters the record as
support for a programme claim.

## Standing caveat

US equities trade-print data from a single institutional
propagation feed, February 2024 to September 2025, plus one month
of China and Japan prints for the OOD check; no crypto, no
BTCUSDT, no futures, no anonymous flow; the partial-observation
setting means book state is never observed, only estimated through
EW-VWAP; every fidelity number is entangled with one proprietary,
deterministic simulator whose own book carries no queue-depth
heterogeneity at price levels beyond best bid and ask in its
fill logic. All bin counts, outlier percentiles, halflife
conventions (undisclosed), liquidity-tier boundaries and context
choices are pipeline-specific. Laundering directions named.
INTO — the normalization-reference filter-disclosure mechanism
and the scale-invariant-over-tick-denominated corroboration enter
only as feature-design discipline; the declared-versus-default
conditioning distinction enters only as a disclosure requirement.
OUT — every K-S and Wasserstein figure, perplexities, scaling-law
exponents, the stylized-fact plots, tokenization constants and
any implication that a generative model's realism licenses a
predictive claim are never cited as expected behavior of any
market the programme measures, never as expected BTCUSDT
behavior, and never as evidence that any programme feature
carries information. Synthetic-data generation, stress testing
and RL training are standing context only.
