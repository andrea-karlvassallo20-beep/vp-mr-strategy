## 41. Null-time session 37 (2026-11-19): deep-read session 33 — the TradeFM generative foundation model paper read; the reference-estimator declaration queued for the normalization-disclosure family

Deep-read session 33 of null-time session 37
(paper/research/library/2026-11-19_tradefm_generative_foundation_model_deep_read.md):
Kawawa-Beaudan, Sood, Papasotiriou, Borrajo, Veloso (J.P. Morgan AI
Research), "TradeFM: A Generative Foundation Model for Trade-flow and
Market Microstructure" (arXiv:2602.23784v1, 27 Feb 2026) — a 524M
decoder-only Transformer trained on >10B tokens of proprietary US-equity
trade events with scale-invariant features and a composite-token
tokenizer, rolled out closed-loop through a deterministic price-time
simulator and graded on stylized facts and distributional fidelity
against Zero-Intelligence and Compound Hawkes baselines, plus zero-shot
APAC perplexity transfer. Read against the ONE question.

**Grade: NO kill line changed. ONE new candidate sharpening queued,
PENDING OWNER RATIFICATION:** the reference-estimator declaration
component for the normalization-disclosure family (deep-read session
33). Mechanism, page-cited: every price-relative feature in TradeFM
is a deterministic function of the EW-VWAP mid-price estimate — the
ratio of two EMA recursions whose halflife is described only as
"time-based" and never numerically disclosed (PDF pp. 4-5, 16) — and
the same raw trade maps to different normalized features and bin
indices under different halflife choices, with the tokenizer bin
edges calibrated downstream of that undisclosed constant (PDF pp. 4,
6): a single silent analyst-tunable knob sitting upstream of every
reference-relative reading. One pre-declaration, harder to pass:
wherever any programme feature, conditioning state, or admissibility
gate is computed relative to an estimated reference price
(mid-price estimate, VWAP/EW-VWAP family, EMA-smoothed price) rather
than to a feed-native observable or the event's own touch, the
pre-registration must declare, recorded on TRAIN before L2 data
arrives, the estimator functional and every smoothing constant
(halflife or window) plus initialization/warm-up handling;
reference-normalized readings under an undeclared estimator or
undeclared smoothing constants are inadmissible. This extends
session 3's normalized-units pre-declaration and session 36's
queue-label reference-construction duty from labeling conventions
and threshold units to the estimator constants themselves, and
forecloses post-hoc halflife selection against TEST. Scope:
pre-registration declaration blocks only; the C1-L2 and C8 spec
texts, every kill line, T-H and T-O remain untouched; no threshold
moves; nothing is armed. Killed-if-wrong: if reference-relative
readings on the programme's venue and fields are later shown
invariant to the estimation halflife over its plausible range, the
component guards nothing and should die back to the standing
declaration rules as they are.

Findings, page-cited: reinforcing, no new item — generative fidelity
is not prediction, and the paper's own primary reproduction target is
the efficient-market null itself (absence of return autocorrelation,
PDF pp. 2, 8-9) with every quantitative claim a distributional K-S
or Wasserstein distance (Tables 2-3, PDF pp. 9-10) and no
out-of-sample return-forecasting test anywhere: no fidelity figure
from any generative microstructure model is ever citable as evidence
that any programme feature carries information. Reinforcing, no new
item — from trade events alone TradeFM's weakest fidelities are
exactly the book-state quantities: Compound Hawkes wins the
bid-ask-spread K-S statistic (0.218 vs 0.238) and the
order-book-imbalance margin is thin (0.142 vs 0.155), the spread
emerging from the simulator's deterministic matching rather than
the model (Table 3, PDF p. 10): trade prints underspecify book
state, the session-1 cancel-blindness caveat and the T1
passive-invisibility constraint in a third corpus; nothing licenses
any taker proxy or relaxes the Tardis L2 requirement.
Interpretation caution — scale-invariance is a modeling convenience
demonstrated on one US venue and one year under the one undisclosed
halflife (Figs 5, 7, 12-13; PDF pp. 5, 11, 15, 24-25); no bin edge,
halflife, liquidity-tier definition, or universality claim transfers
to BTCUSDT or any market the programme measures, and the APAC result
is perplexity on the paper's own tokenization, not demonstrated
cross-venue feature equivalence. Source-quality note — arXiv v1,
industrial research disclosure (JPM informational-only disclaimer, PDF
pp. 1, 12), proprietary undisclosed dataset, no code or data released,
baselines chosen by the authors (LOB-Bench neural baselines excluded
on input grounds, PDF p. 8), and the closed-loop evaluation partially
entangles model and simulator fidelity by the authors' own admission
(PDF p. 10): graded as an engineering demonstration, unverifiable on
evidence; published version to be checked before formal citation.
Killed-if-wrong for the queued item stated above. Standing caveat:
US equities, trades-only, one venue, one year, proprietary data; no
crypto, no BTCUSDT, no futures, no costs, no impact, no delisting
discussion; simulator validated only on fill CDFs (0.91/0.98
correlations, PDF p. 24); all figures incomparable to programme
statistics. Laundering directions named: INTO — the
reference-estimator declaration mechanism, the
partial-observability corroboration, and the
fidelity-is-not-prediction caution enter only as feature-design and
interpretation discipline; OUT — no perplexity, bin edge, halflife,
liquidity tier, stylized-fact figure, "2-3x" fidelity claim, or
zero-shot transfer claim is ever cited as expected behavior of any
market the programme measures or as evidence that any programme
feature carries information, and no synthetic-data route replaces
any sealed, forward, or holdout window.

Ratification queue after this session: TWENTY-SEVEN candidate
sharpenings (the twenty-six standing plus the reference-estimator
declaration component for reference-normalized features joined here
through deep-read session 33), zero armed. T1 remains armed awaiting
the owner's word; the blocked list stays blocked. Deep-read queue
pointer: the next UNREAD triage entry is "Diffusive limit of
Hawkes-driven order book dynamics" (score 31, x5db64b). Nothing
measured, no kill line moved, nothing armed, nothing trades live.
