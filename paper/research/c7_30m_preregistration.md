# C7 pre-registration at the 30-minute clock — the track, before any model

## 0. Label definition (empirically recovered, pending owner confirmation)

- `y_hold` = **4-hour forward return, rank-normalized cross-sectionally
  per era** — verified: per-era Spearman vs the 4h forward return
  computed from the panel's own closes: 0.87, 0.71, 0.79, 0.85, 0.74
  across five well-separated eras (46–67 symbols each).
- `responder` = next-30m-bar return (Spearman 0.93; scale ~201x) — NOT
  the C7 target; it is the short-horizon label and stays out of the
  priming question.

## 1. Leakage audit (Task 1) — result: NO LEAKS, documented drops

Per-era cross-sectional Spearman of every feature vs `y_hold`, 60
full eras spread across the whole file (full table:
`leakage_audit_c7_30m.csv`):

- **No feature exceeds the 0.80 leak line.** The strongest is
  `f_beta` at mean |rho| = 0.196. The panel is clean of direct future
  leaks.
- **Documented drops and exclusions:**
  - `lead_btc_3`, `lead_eth_3`, `lead_sol_3`, `ll_disp` are CONSTANT
    within every era (market-level aggregates) — they carry ZERO
    cross-sectional information and are excluded from the
    cross-sectional model (they are not leaks; they are degenerate
    for this question).
  - Exact duplicates (one of each pair retained):
    `f_adv_rank` == `rank_adv20_usd` (rho = 1.00).
  - Exact mirror pairs (documented, both retained as one signed
    feature each — no information doubled): `f_mom_21` == −`f_rev_21`,
    `f_mom_5` == −`f_rev_5`, `f_rev_1` == `reversal_1` == −`own_6`.

## 2. Vol-tautology check (Task 2) — the C7 kill lines at 30m

**The measurement that motivates the kill line:** the six
"priming-like" volatility features are ONE FACTOR wearing six names —
mean per-era cross-sectional Spearman: sigma20~f_vol_21 = 0.99,
sigma20~realized_vol_30 = 0.94, sigma20~f_range_21 = 0.92,
f_vol_21~realized_vol_30 = 0.95, f_vol_63~f_range_21 = 0.91,
realized_vol_30~f_range_21 = 0.93, sigma20~realized_vol_7 = 0.82.
Likewise `f_amihud` == −`f_adv_rank` (−0.93). "Low volatility" at this
resolution is a single axis, not six independent clues.

**The extended C7 kill lines (pre-declared, armed before any
model):**

- **K1 — vol-tautology (the C1 death, extended):** after
  conditioning on the single vol factor (the first principal
  component of the six vol features, or any one of them), NO
  "priming" composite may retain out-of-sample information about
  `y_hold` at 4h. Operational form: fit the vol-factor-only model on
  TRAIN; the priming-augmented model must beat it on VALIDATION by
  more than its own cross-fold variance. If it does not, "priming" is
  quietness wearing a costume, and C7-30m is dead.
- **K2 — OOS effect size:** the frozen model's VALIDATION per-era
  mean Spearman with `y_hold` must exceed the era-shuffled placebo
  (labels permuted across symbols within each era) at p < 0.01,
  block-bootstrapped by day.
- **K3 — multiplicity:** the TEST reading is deflated (DSR) over all
  configurations tried on TRAIN+VALIDATION, 43 features x 78 assets
  x every composite — the everything-search tax.
- **K4 — regime reproduction:** the effect must appear in BOTH the
  2024 validation year and the 2025–26 test year; an effect that
  lives only in one regime is a regime artifact, not priming.
- **K5 — direction humility:** everything above is about RANKED
  cross-sectional 4h returns. Nothing here may be read as a
  directional (time-series UP) claim; the 0.505 boundary is not on
  trial in this document.

## 3. What is deliberately NOT pre-registered

No model family, no hyperparameters, no feature composite — those
are chosen on TRAIN/VALIDATION after this document is merged, and the
choice is recorded as an amendment, not silently.

Nothing in this unit trained a model, computed an OOS reading, or
touched the TEST eras.
