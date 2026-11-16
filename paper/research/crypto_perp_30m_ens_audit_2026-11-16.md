# Intake audit: crypto_perp_30m_ens.parquet (the owner's 1.27GB upload)

Pulled from the owner's Drive (link-shared, gdown, 1,267,055,191 bytes
verified). Audited memory-bounded (pyarrow row-group streaming - the
file is 1.27GB compressed and must never be loaded whole).

## What it is

- **5,308,089 rows × 43 columns**, 44 row groups.
- **78 crypto perpetual symbols** (ADA, AAVE, AVAX, ARB, APT, ...,
  VIRTUAL), median 65,038 rows per symbol (ADA max 104,431).
- **Era span: 2020-07-04 21:00 → 2026-06-20 10:30 UTC** — six years of
  **30-minute bars** (spacing verified: 1800s; occasional 5400s/14400s
  gaps = market downtime or delisting-era holes, present but rare).
- **Fully dense**: zero nulls across all 43 columns in sampled row
  groups (first, middle, last).
- Timestamps: `era_date` is `timestamp[us]` — microseconds, correct by
  construction.

## Schema families

- **Identifiers/state**: era_date, asset_id, symbol, close, sigma20.
- **Momentum**: f_mom_5/21/63/126/252_21, momentum_30_7, momentum_14_3.
- **Reversal**: f_rev_1/5/21, reversal_1, reversal_7.
- **Volatility**: f_vol_21/63, realized_vol_7/30.
- **Liquidity/microstructure-adjacent (OHLCV-derived)**: f_adv_rank,
  f_amihud, f_dv_chg_21, f_gap_1, f_range_21, rank_adv20_usd.
- **Market structure**: f_beta, market_beta_btc, market_beta_eth.
- **Cross-asset lead-lag**: llgap_btc/eth/sol_3/6, lead_btc/eth/sol_3,
  ll_disp, own_3, own_6.
- **Labels**: `responder` and `y_hold`, both clipped to [−10, +10],
  zero NaNs, 5.31M finite values each - return-like standardized
  targets in the Numerai convention (era + responder + feature
  prefix). The exact label horizon and standardization are NOT
  documented in the file - the owner must supply the label definition
  before any model consumes them (the labeling-specification
  checklist, Library artefact 099).

## Integrity verdict

CLEAN as delivered: dense, well-typed, correctly-unitized, six-year
coverage, era-aligned. One open item: the label definition (what
`responder` and `y_hold` measure, over what horizon, with what
standardization) is undocumented in the file itself.

## Honest placement in the registry (no claims tested)

This panel is the first dataset in the repo that could carry the
**C7 cross-sectional priming question** at sub-daily resolution: 78
perps, 30-minute clock, six years, era-structured for group-aware
purged CV. It is NOT order-book data - every feature is
OHLCV-derived; there is no book, no queue, no cancellations - so the
L0 gate does not apply, and no L2 claim (C5/C6) may draw on it.

What using it honestly would require, in order, ALL pre-registered
before any model runs: (1) the label definition from the owner;
(2) a leakage audit of every feature at the 30m decision moment
(Library artefact 098); (3) the chronological split manifest frozen
before tuning (artefact 100); (4) the C7 kill lines extended to the
30m clock with the multiplicity tax recomputed for 43 features × 78
assets; (5) the vol-tautology check that killed C1 applied to every
"priming-like" feature. Until those exist in writing, this file is
AUDITED and SHELVED - nothing runs.

## What this unit did

Pulled, verified byte count, schema-audited, coverage-audited,
integrity-audited, and shelved with the placement note above. No
features computed, no models fit, no claims touched.
