# Deep-read session 33 — TradeFM: A Generative Foundation Model for Trade-flow and Market Microstructure

- **Authors:** Maxime Kawawa-Beaudan, Srijan Sood, Kassiani Papasotiriou, Daniel Borrajo, Manuela Veloso (J.P. Morgan AI Research)
- **Full title:** TradeFM: A Generative Foundation Model for Trade-flow and Market Microstructure
- **Venue:** arXiv:2602.23784v1 [cs.LG], 27 Feb 2026
- **What it is:** a 524M-parameter decoder-only Transformer pre-trained on
  >10B tokens of raw US-equity trade events (>9K names, Feb 2024–Sep 2025),
  with scale-invariant features and a custom tokenizer, rolled out through a
  deterministic price-time-priority simulator and graded on stylized-fact
  reproduction and distributional fidelity against Zero-Intelligence and
  Compound Hawkes baselines, plus zero-shot APAC transfer.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xe7dc7f_tradefm_a_generative_foundation_model_for_trade_fl.txt,
~29 pp., page-marked). Next UNREAD triage-rank entry (score 31).

## The paper in one paragraph

TradeFM treats the raw trade event stream (interarrival time, normalized
price depth, log volume, action, side) as a "language": each feature is
binned (quantile bins for price features, log-width bins for volume and
time), the bins are composed into a single 16,384-word composite trade
token, and the model — conditioned on liquidity tier, a market-vs-participant
indicator, and the intraday price level relative to the open — is trained
next-token on a proprietary tick dataset, with tokenizer bin edges calibrated
on the first 30 days only (Feb 2024) and a temporal hold-out from Jan 2025
onward (PDF pp. 4, 6-7, 18). All price normalization routes through a
proposed EW-VWAP mid-price estimate — a ratio of two exponential moving
averages whose halflife is described as "time-based" but never numerically
disclosed (PDF pp. 4-5, 15-16). Evaluation is closed-loop: generated events
are executed by a deterministic matching simulator, and the emergent returns
are graded on absence of autocorrelation, volatility clustering, heavy tails
and aggregational Gaussianity (PDF pp. 8-9, 21-22); distributional fidelity
K-S/Wasserstein beats a calibrated Zero-Intelligence agent and a Compound
Hawkes baseline on most order-flow quantities, with Compound Hawkes winning
bid-ask spreads (Table 3, PDF p. 10), plus zero-shot China/Japan perplexity
with "moderate degradation" (PDF pp. 10-11). No return-forecasting test
appears anywhere in the paper: the headline results are distributional
similarity metrics, not out-of-sample predictive performance.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] the
   reference-estimator declaration component: wherever any programme
   feature, conditioning state, or admissibility gate is computed
   relative to an *estimated* reference price (mid-price estimate,
   VWAP/EW-VWAP family, EMA-smoothed price) rather than to a feed-native
   observable or the event's own touch, the pre-registration must declare,
   recorded on TRAIN before L2 data arrives, the estimator functional
   (the exact EMA/recurrence form) and every smoothing constant (halflife
   or window), plus the estimator's initialization/warm-up handling;
   reference-normalized readings computed under an undeclared estimator
   or undeclared smoothing constants are inadmissible. Mechanism,
   page-cited: TradeFM's entire price-feature space — depth dt and
   intraday level Δpt — is a deterministic function of the EW-VWAP
   estimate ˆp = Nt/Dt defined by the pair of EMA recursions
   Nt = α·(p·vt) + (1−α)·Nt−1, Dt = α·vt + (1−α)·Dt−1 (PDF pp. 4-5,
   16), and the halflife that sets α is never stated (PDF pp. 5, 16);
   the same raw trade therefore maps to different normalized features
   — one bin index up or down — under different halflife choices, and
   the tokenizer bin edges are calibrated on those halflife-dependent
   normalized values (PDF pp. 4, 6). This is a single, silent,
   analyst-tunable knob upstream of every price-relative feature,
   exactly the undisclosed-degree-of-freedom family the programme has
   been closing one component at a time (session 3's normalized-units
   pre-declaration for extreme-OFI thresholds; session 36's queue-label
   convention covering *reference construction* for queue-state
   conditioning labels). This component extends that disclosure duty
   from labeling conventions and threshold units to the *estimator
   constants themselves*, across every reference-normalized feature in
   the C1-L2 L2 arm and any future C8 arm. Harder to pass: a
   reference-normalized feature can no longer satisfy an otherwise
   complete pre-registration while its halflife remains a free parameter
   selectable post hoc against TEST; the disclosure costs nothing when
   the constant was already frozen, and it makes every future
   reference-relative reading testable for implementation identity.
   Scope: a disclosure requirement on pre-registration declaration
   blocks only; the C1-L2 and C8 spec texts, every kill line, T-H and
   T-O remain untouched; no threshold moves; nothing is armed. If every
   admissible programme feature is computed against feed-native
   observables (best bid/ask, the event's own touch), the component
   guards nothing on that route and stays dormant.
   Killed-if-wrong: if reference-relative readings on the programme's
   venue and fields are later shown to be invariant to the estimation
   halflife over its plausible range, the declaration guards nothing
   and should die back to the standing declaration rules as they are.

2. [reinforcing, no new item] — generative fidelity is not prediction,
   and the paper's own headline metric reproduces the null: the primary
   stylized fact "reproduced" in Experiment 1 is the *absence* of return
   autocorrelation (PDF pp. 2, 8-9), i.e. the model's success criterion
   is similarity to the efficient-market null, and every quantitative
   claim is a K-S/Wasserstein distance between distributions (Tables 2-3,
   PDF pp. 9-10) with no out-of-sample return-forecasting test anywhere.
   This corroborates the house rule that a library is ammunition, not
   evidence: no fidelity figure from a generative microstructure model is
   ever citable as evidence that any programme feature carries
   information, and "the model reproduces heavy tails and volatility
   clustering" is a realism claim about marginals, not an edge.

3. [reinforcing, no new item] — the partial-observability result cuts
   toward the programme's endpoint, not away from it: TradeFM learns
   from trade events without the book (PDF pp. 1-3), and its weakest
   fidelities are precisely the book-state quantities — bid-ask spreads,
   where Compound Hawkes wins the K-S statistic (0.218 vs 0.238,
   Table 3, PDF p. 10), and order-book imbalance, where its margin over
   Hawkes is thin (0.142 vs 0.155) while the simulator's spread emerges
   indirectly from deterministic matching rather than from the model
   (PDF p. 10). Trade prints underspecify book state; this is the
   session-1 caveat (OFI is cancel-blind) and the T1 standing
   constraint (passive withdrawal is invisible in aggTrades) appearing
   in a third corpus. Nothing here licenses relaxing the Tardis L2
   requirement or substituting a taker proxy on any C1-L2 arm.

4. [interpretation caution] — scale-invariance is a modeling
   convenience demonstrated on one venue and one year: relative
   (bps/ration) features are shown more stationary across assets and
   months than tick-based features (Fig 7, PDF pp. 5, 15; Figs 12-13,
   PDF pp. 24-25), but the stationarity is measured on US equities
   Feb 2024–Sep 2025 under the one undisclosed EW-VWAP halflife, and
   the zero-shot China/Japan "moderate perplexity degradation"
   (Fig 5, PDF p. 11) is perplexity on the paper's own tokenization,
   not demonstrated feature equivalence across venues. No bin edge,
   halflife, liquidity-tier definition, or universality claim transfers
   to BTCUSDT or to any market the programme measures; a future
   cross-market reading of programme features may invoke
   scale-invariant *design discipline*, never the paper's fitted
   evidence of transfer.

5. [source-quality note] — arXiv v1 (27 Feb 2026), J.P. Morgan AI
   Research, with the bank's informational-only disclaimer (PDF
   pp. 1, 12); the dataset is proprietary and undisclosed (beyond "raw,
   tick-level US equities transactions," 368 trading days, PDF p. 4),
   no code or data is released, so nothing quantitative is checkable;
   the comparison baselines are the paper's own choice (ZI and Compound
   Hawkes; LOB-Bench neural baselines excluded on input-grounds, PDF
   p. 8), and the closed-loop evaluation partially entangles model and
   simulator fidelity — the authors state full disentanglement remains
   future work (PDF p. 10). Graded as an industrial research
   demonstration, strong on scale and engineering, unverified and
   unverifiable on evidence; published version to be checked before
   formal citation.

## What this paper would have killed if we had done it wrong

The synthetic-data siren. Had the programme accepted generative realism
as validation, a future cost-survival or robustness layer could have been
"tested" against TradeFM-style synthetic order flow — path-plausible,
stylized-fact-conformant, and generated through a deterministic
toy-matching simulator whose spread is an artifact of the matching logic
(PDF pp. 8, 21-22) — and a strategy surviving there would have been
recorded as surviving realistic conditions, when it had merely survived a
smooth surrogate of the single historical path. The guard against it was
already standing: default assumption no edge, library is ammunition not
evidence, nothing operationalized from a paper, and every cost-survival
claim must carry its assumptions rather than borrow a simulator's
plausibility. The second near-miss is subtler: had session 36's
convention-queue stopped at labeling conventions, the EW-VWAP halflife
would have remained exactly the kind of silent upstream knob — present in
a leading industrial model without even a stated value (PDF pp. 5, 16) —
that survives every admissibility gate and is tunable after the data
arrives; the queued declaration component closes that door before any L2
feature is ever computed.

## Standing caveat

TradeFM is a US-equities, trades-only, one-venue, one-year industrial
model on proprietary data: no book input (deliberately), no crypto, no
BTCUSDT, no futures, no survivorship or delisting discussion, no
transaction costs or market impact in evaluation, and a deterministic
simulator validated only on fill-volume and lot-count CDF correlations
(0.91 and 0.98, PDF p. 24). All bin edges are calibrated on Feb 2024
only (PDF p. 4) and frozen thereafter, an engineering choice whose
robustness is argued, not proven. Perplexity, K-S and Wasserstein figures
are incomparable across tokenizations and never comparable to the
programme's statistics. Nothing in this paper bears on any kill line, and
its empirical claims enter the record only as the standing caveats above.
Laundering directions named: INTO — the reference-estimator declaration
mechanism, the partial-observability corroboration, and the
fidelity-is-not-prediction caution enter only as feature-design and
interpretation discipline. OUT — no perplexity value, bin edge,
halflife, liquidity-tier definition, stylized-fact figure, "2–3×"
fidelity claim, zero-shot transfer claim, or APAC degradation figure is
ever cited as expected behavior of any market the programme measures, or
as evidence that any programme feature carries information, and no
synthetic-data route replaces any sealed, forward, or holdout window.
