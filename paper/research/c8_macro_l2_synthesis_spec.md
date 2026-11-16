# C8 — The Macro-L2 Synthesis: full pre-registration

Status: **DECLARED, UNTESTED, blocked-on-data.** No code run, no data read,
no parameter tuned. This document supersedes and extends §4 of
`c7_l2_integration_spec.md` (which first declared the interaction claim);
that section now points here. Kill lines are armed before the data exists.

The math this claim stands on was verified on 2026-11-16
(`paper/research/phase1_daily/math_verification_2026-11-16.md`): the CKS OFI formula is
byte-exact to the arXiv source (arXiv:1011.6402v3), the Hawkes
log-likelihood is exact against an independent oracle, the branching
ratio is the true spectral radius ρ(G) cross-validated against the `tick`
library, and the estimator defect that overstated n_c by the factor β
was found and fixed BEFORE the 0.8 threshold below was frozen.

## 1. The hypothesis, stated falsifiably

Public math (Hawkes self-excitation, OFI) is run by HFTs at millisecond
horizons, where the macro state is irrelevant; retail looks at daily
candles, where the book is invisible. C8 occupies the unexplored cell:
the PUBLIC microstructure math, on a frontier market's L2 book
(BTCUSDT perp — one-instrument-first law), at MACRO hazard horizons
(4h primary, 24h secondary).

**CLAIM:** a macro C7-style primed state (compression at the bottom of
the range, measured on the daily clock) COMBINED WITH an L2 trigger
(Hawkes branching ratio ρ(Ĝ) > 0.8, or extreme OFI absorption) produces a
breakout hazard that is STRICTLY GREATER than either the macro state
alone or the L2 trigger alone — the layers MULTIPLY, not add.

**FALSIFIABLE CORE (both must hold, or C8 dies):**

- **C8-A (interaction):** the pre-specified primed × trigger interaction
  term in the hazard model has a hazard-ratio 95% CI excluding 1.0.
- **C8-B (joint superiority):** the observed hazard in the combined
  state exceeds max(hazard | primed alone, hazard | trigger alone), with
  the difference's day-block bootstrap 95% CI excluding 0.

A multiplicative interaction without ordinal superiority (K2) is not an
edge; a superior combined hazard that only adds (K1) is not a synthesis.
Both kill.

## 2. Frozen state definitions (no post-hoc tuning)

### 2.1 Macro layer — the primed state

- The C7 registry convention, on the daily clock: compression ≥ 20 days
  (comp_days ≥ 20), quiet (realized-vol percentile ≤ 33rd), low in the
  yearly range (range_pos in the bottom quartile).
- Causality by lag, not convention: the L2 clock consumes
  `primed_lag1` — the flag computed strictly from data ≤ the previous
  UTC close. Same-day C7 state never reaches the L2 clock.
- Continuous components (`comp_days_lag1`, `rvol_pct_lag1`,
  `range_pos_lag1`) enter as covariates: a 60-day coil and a 143-day
  coil are not the same macro state.

### 2.2 L2 triggers (two, pre-registered, multiplicity-taxed)

- **T-H — Hawkes criticality.** Branching ratio ρ(Ĝ) > 0.8, estimated on
  a rolling 4h window of taker events (buy/sell, the verified 2D
  estimator; the 4D version with cancellations only under the C5 gate),
  with per-pair decays and the diurnal baseline (the `fit_hawkes2`
  configuration, whose G = α/β convention is now verified). n_c → 1 is
  the reflexive market: the book going critical.
- **T-O — extreme OFI absorption.** The 4h integrated OFI (CKS exact
  formula, `top_of_book_ofi`) sits in the bottom decile of its trailing
  30-day distribution WHILE |Δmid| over the same window is < 0.5× the
  trailing hourly σ: one-sided flow hitting the book without moving the
  price — loading, not release. Decile and σ-multiplier frozen NOW.

### 2.3 The endpoint — breakout (the WHEN instrument)

- A breakout is |return| ≥ 4× trailing 60-day σ within the horizon,
  measured from the decision row on the 4h clock (primary, H1 = 4h) and
  the 24h clock (secondary, H2 = 24h). Magnitude, not sign: the 0.505
  direction boundary is NOT on trial here.
- Decision rows: one row per hour while the macro state persists, plus
  every trigger onset (rows enter the risk set only where the L2 data
  passes the gate).

## 3. Test design (pre-specified)

- Discrete-time hazard model, hour-of-day strata MANDATORY (the T3
  death: without stratification, quiet sessions carry tighter
  σ-scaled barriers and fake the result).
- Covariates: primed_lag1, trigger (T-H and T-O tested as separate
  trigger families), primed × trigger, σ_H level, comp_days_lag1,
  rvol_pct_lag1, range_pos_lag1.
- The frozen split manifest (`docs/split_manifest.md`) applies: purge at
  the label horizon on every boundary, 24h embargo, thin eras excluded,
  TEST touched once at the end.
- Inference: day-block bootstrap; era-grouped purged CV; the DSR
  multiplicity tax over the trigger family (§4 K5).

## 4. Kill lines (pre-declared, armed — any one fires, C8 dies)

1. **K1 — interaction:** the primed × trigger HR 95% CI includes 1.0.
   The layers only add (or do nothing); the multiplication is dead.
2. **K2 — joint superiority:** h(primed ∧ trigger) −
   max(h(primed alone), h(trigger alone)) has a day-block bootstrap 95%
   CI including 0. Superadditivity on paper is not superiority in
   hazard; dead even if K1 passes.
3. **K3 — book placebo:** the 24h-shift book placebo (pre-declared in
   the L2 spec) reproduces ≥ half the interaction. Pipeline artifact;
   dead.
4. **K4 — era shuffle:** the era-shuffled placebo reproduces the
   interaction at p < 0.01 block-bootstrapped. Climatology wearing an
   interaction costume; dead.
5. **K5 — multiplicity:** two triggers × two horizons = four cells. The
   DSR tax is paid over the family. If exactly one cell survives, the
   claim NARROWS to that cell and is re-registered before any TEST
   touch; zero cells survive → dead; no post-hoc widening ever.
6. **K6 — horizon disagreement:** the 4h and 24h endpoints disagree in
   sign. A macro clock that changes character between adjacent horizons
   is a horizon artifact; dead.
7. **K7 — Hawkes boundary artifact:** if > 50% of T-H trigger windows
   are boundary-constrained (ρ̂(G) ≥ 0.949, the estimator's cap), the
   branching trigger measures the cap, not the market. T-H is dead;
   C8 may survive only on T-O through K5's narrowed re-registration.
8. **K8 — L2 vol-tautology (asked FIRST):** after conditioning on the
   rolling L2 activity factor (trade-count rate, σ_H), the interaction
   retains no out-of-fold information. This is the kill line that
   killed C1, the watchlist, and C7-30m — compression measured from
   OHLCV is volatility wearing a costume. C8's macro layer is exactly
   such a compression state; if the book only respects its quietness,
   the synthesis is quietness in a costume at book resolution; dead.
9. **K9 — regime reproduction:** the interaction must reproduce in
   both validation years. A single-year interaction is noise with a
   story; dead.
10. **K10 — proxy refusal:** no trigger may be substituted with
    bookTicker/aggTrades proxies (passive withdrawal is invisible
    there — the standing constraint). Incremental L2 only; otherwise
    C8 stays blocked rather than tested dishonestly.
11. **K11 — base-layer gate:** C8 runs only after C1-L2 survives its
    own five kill lines. No layer stacking on a dead base
    (`c7_l2_integration_spec.md` §5); if C1-L2 dies, C8 dies with it —
    a synthesis needs something to synthesize.

## 5. What C8 cannot tell you (refused in advance)

- **Direction.** The endpoint is |move|; the 0.505 boundary stands.
- **Economics.** A hazard is information, not profit; the convexity
  sizing framework (companion document) is the bridge from a pass to a
  position, and nothing here sizes anything.
- **Cross-asset generization.** One instrument first. The altcoin
  problem (no full-depth L2 for primed alts) is answered the honest way:
  the macro edge alone, daily resolution, no trigger, no timing — and
  BTC's book is never borrowed as an altcoin's trigger.

## 6. Why this combination, and what kills it interestingly

The mechanism, stated so it can die: the primed macro state is a
compressed spring; the order book is where the release physically
occurs. If the trap theory is causal, the book should show the LOADING
(absorption: flow without price movement) and the release beginning
(criticality: n_c climbing toward 1) with sharper hazard signatures
inside primed states — because there is something loaded to release.
If the layers only add, the macro state is decoration on a
microstructure clock that never needed it, and the compression family
dies its fourth and final death — this time measured in the book
itself, where the executive summary said the coil must live if it
lives anywhere.

## 7. Execution order when the data arrives

1. L0 verification gate (book reconstruction, snapshots) — nothing
   runs before it passes.
2. C1-at-L2 (the compression clock at book resolution) — its kill
   lines decide whether C8's base exists.
3. C8 (this spec) — on gated incremental L2, frozen manifest, kill
   lines 1–11 armed.
4. The convexity sizing framework — the decision context, pre-registered
   so a pass has somewhere to go besides celebration.

## Amendment 1 (2026-11-16, post-declaration): the 0.8 threshold,
source-grounded

Added AFTER the kill lines were frozen; it changes no threshold and
arms no new line — it documents, from the newly acquired source
itself, why the frozen 0.8 is the right calibration.

Source: Filimonov & Sornette, "Quantifying the Reflexivity of
Financial Markets: Towards a Prediction of Flash Crashes"
(downloaded legally; extracted text:
`docs/library/text/xf29859_quantifying_reflexivity_in_financial_markets_towar.txt`).

What the source says, with page cites to the extracted PDF:

- **The modern regime is 0.7-0.8.** On the E-mini S&P 500
  (1998-2010), the branching ratio is "consistently above 0.6 and,
  since 2007, between 0.7 and 0.8 with spikes at 0.9" (PDF p. 13);
  the regime history is itemized on p. 14 (0.3 -> 0.6 in 2000-02,
  0.6 -> 0.7 by 2006, 0.7-0.8 after Q1-2007).
- **The flash-crash signature is a PRECURSORY rise toward
  criticality.** For May 6, 2010: "a precursory early rise of n
  followed by strong increase culminating very close to the
  critical value n = 1" (PDF p. 17); the exogenous April 27, 2010
  crash, in contrast, shows n remaining constant (PDF p. 17) — the
  discriminator between an endogenous and an exogenous event is
  exactly whether n moves BEFORE the price does.
- **The activity contrast:** ~1.5 mid-price changes/second in 2008
  vs. a peak of 194/second at the May 6 flash crash (PDF p. 9).

Reading for C8: 0.8 is the TOP of the source's modern regime
(0.7-0.8), i.e. the frozen threshold selects states that are
unusually endogenous even by post-2007 standards, without waiting
for the near-critical values (n -> 1) that only appear at the
crisis itself. The source's precursory-rise finding is the
mechanistic license for C8's claim structure (the trigger must
LEAD, not accompany): if the BTCUSDT perp book shows n climbing
within primed states before breakout, that is the same signature
the source documented on equities. The threshold stays 0.8; if
the data shows the perp book's regime baseline differs from the
equity regime (e.g. n_c naturally above 0.8 in crypto), that is a
KILL-LINE-7 (boundary-constraint) finding to be reported, not a
threshold to be re-tuned after seeing the answer.
