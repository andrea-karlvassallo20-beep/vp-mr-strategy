# C8 synthesis spec — the combination (Macro Primed x L2 Micro), pre-registered before any model

Status: DRAFT for owner review. Nothing in this document has been
computed on data; no model has been trained; the TEST eras are
untouched. Kill lines below are armed BEFORE any C8 measurement,
following the C7 pre-registration discipline
(`paper/research/phase1_daily/c7_30m_preregistration.md`).

## 0. What C8 is

C8 tests the COMBINATION of two states:

- **Macro state (from C7):** `Primed` = quiet AND range-bottom
  (the C7 control-group design: quiet alone is the Control).
- **Micro state (from the L2 family):** the book is stressed:
  - Hawkes branching ratio $n_c > 0.8$ on the instrument's trade
    arrivals within the 30m bar (Filimonov-Sornette endogeneity,
    `docs/math_cheatsheet.md` Section 2), OR
  - extreme OFI: |integrated OFI| for the bar in the top decile of
    its trailing window (Cont-Kukanov-Stoikov,
    `docs/math_cheatsheet.md` Section 1), OR
  - VPIN in the top decile of its trailing window (Easley-Lopez de
    Prado-O'Hara, `docs/math_cheatsheet.md` Section 5).

Hypothesis (economic, stated before measurement): the known
`y_hold` information in the macro Primed state is amplified when
the L2 book shows endogenous, toxic flow — the micro state is a
signed, asymmetric quantity that the OHLCV compression family
(the C7 vol factor) cannot measure, so the interaction is a
genuine two-family claim, not a rename.

## 1. Data and label

- Panel: the frozen L2-extended panel (C1-L2 pipeline; era
  structure and split manifest as in C7). `y_hold` = 4-hour
  forward return, rank-normalized per era (unchanged).
- Micro features are computed ONLY from gated L2 data
  (`src/gate_tardis_sample.py` pass required) and the trades feed,
  per volume bucket where applicable (Easley et al. volume clock,
  summary 048), aggregated to the 30m bar.
- Macro Primed state: the C7 definition, frozen, with the C7
  control (quiet alone) retained as the honest baseline.

## 2. The estimand

The interaction uplift, measured orthogonally (DML,
`src/dml_orthogonalizer.py`, summary 065):

$$\Delta = E[y \mid \text{Primed}, \text{Micro}] -
E[y \mid \text{Primed}, \neg\text{Micro}]$$

i.e. the effect of the micro state WITHIN the Primed macro state,
with the vol factor and the market-book common factor as
nuisances/confounders ($X$ in the partially linear model). The
comparison that matters is Primed∧Micro vs Primed alone — NOT
Primed∧Micro vs everything, which would smuggle the (dead) C7
priming claim back in.

## 3. Pre-registered kill lines (armed before any measurement)

- **K1 — costume check (the C7 death, extended to L2):** the
  micro state must add information BEYOND the vol factor and the
  market-book factor. Operational form: fit the
  vol+market-factor-only model on TRAIN; the micro-augmented model
  must beat it on VALIDATION by more than its own cross-fold
  variance. If it does not, the "L2 micro state" is the OHLCV vol
  factor wearing a book-derived costume, and C8 is dead.
- **K2 — OOS effect size:** the frozen model's VALIDATION per-era
  mean Spearman of the interaction term with `y_hold` must exceed
  the era-shuffled placebo (labels permuted within era) at
  p < 0.01, block-bootstrapped by day. A CI that includes zero is
  a kill, exactly as in C7-30m (+0.00211 included zero and died).
- **K3 — multiplicity:** the TEST reading is deflated (DSR /
  recentered SPA) over the full search: {3 micro indicators} x
  {2 threshold families: fixed value vs trailing quantile} x
  {threshold grid} x {all composite forms tried on
  TRAIN+VALIDATION}. The count is fixed in this document's
  amendment log before the TEST run.
- **K4 — regime reproduction:** the interaction must appear in
  BOTH the validation year (2024) and the test year (2025-26) with
  the same sign. An interaction that lives in one regime is a
  regime artifact (Engel 1994 precedent, summary 062).
- **K5 — direction humility:** everything is about RANKED
  cross-sectional 4h returns. No directional (time-series UP)
  claim is on trial; the 0.505 boundary is not on trial here.
- **K6 — micro-state validity:** the micro indicators themselves
  must pass their own sanity gates on the gated data: (a) the
  Hawkes fit must converge with $n_c$ in [0, 0.99] on at least
  95% of bars (unconverged bars are missing, not zero); (b) OFI
  and VPIN must be computed from exchange-provided trade side
  where available, with inferred-side features documented
  separately (summary 054). If the micro state cannot be measured
  honestly on the data, C8 is not run at all — an unmeasurable
  hypothesis is not a hypothesis.
- **K7 — cost survival:** any surviving reading is reported both
  raw and net of a round-trip cost assumption (taker fee + half
  spread at the prevailing book). A reading that survives K2 but
  not cost is recorded as "measurable but not harvestable" — a
  fact about the market, not a strategy.

## 4. What is deliberately NOT pre-registered

No model family, no hyperparameters, no exact threshold values
(the trailing-quantile grid is chosen on TRAIN/VALIDATION and the
choice recorded as an amendment). The three micro indicators are
named, but their combination rule is chosen on TRAIN and frozen
before TEST.

## 5. Dependencies (library synthesis feeding C8)

The executable formulas for all three micro indicators are in
`docs/math_cheatsheet.md`; the per-paper context is in
`docs/library/summaries/` (018 OFI, 046-048 VPIN/volume clock,
043/044 WATCH/Wasserstein for the change-detection variant, 049
the Markov-book formalism, 065 DML for the estimand). Paywalled
formulas carry the "Verify against library source before
production" warning; the seven legally downloaded papers
(acquisition log: `docs/library/acquisition_log.json`) are
text-extracted under `docs/library/text/` for page-level
verification.

Nothing in this spec trained a model, computed an OOS reading,
or touched the TEST eras.
