# Chronological Split Manifest — C7 at the 30-minute clock (FROZEN)

**Frozen before any model is trained or tuned.** Library artefact 100.
Any change to this manifest after training begins is a protocol
violation and must be recorded as such.

Dataset: `crypto_perp_30m_ens.parquet` (5,308,089 rows, 78 perps,
2020-07-04 21:00 → 2026-06-20 10:30 UTC, 30-minute bars).
Target: `y_hold` = 4-hour forward return, rank-normalized
cross-sectionally per era (empirically recovered and verified: per-era
Spearman vs the 4h forward return 0.71–0.87 across five separated
eras; pending the owner's one-word confirmation of the recovered
definition).

## The splits (era_date, UTC)

| split | eras from | eras through | share | role |
|---|---|---|---|---|
| TRAIN | 2020-07-04 21:00 | 2023-12-31 23:30 | ~57% | fitting, including all cross-fitting |
| VALIDATION | 2024-02-01 00:00 | 2025-06-30 23:30 | ~22% | model selection ONLY |
| TEST | 2025-08-01 00:00 | 2026-06-20 10:30 | ~14% | touched ONCE, at the end, by the final frozen model |

## Purge and embargo (the leakage fence)

- **Label horizon H = 4 hours = 8 bars.** Any row whose label window
  crosses a split boundary is PURGED from both sides.
- **Embargo = 48 bars (24 hours)** after each split's last training
  era: no train-era label window may overlap validation feature
  windows, and no validation window may overlap test. This is why the
  boundaries above leave month-long gaps (all of January 2024 and
  July 2025) — those eras belong to NOBODY.
- Crypto regimes shift massively; the embargo is deliberately
  conservative (24h ≫ 4h label horizon) because volatility clustering
  spans the boundary even when labels do not.

## Rules of engagement

1. Eras with fewer than 40 symbols in the cross-section are excluded
   from evaluation (thin-era noise).
2. Feature set: the 43 columns minus the documented drops and the
   era-constant columns (see the leakage audit) — the exact frozen
   list is `paper/research/leakage_audit_c7_30m.csv`.
3. The multiplicity tax (DSR / effective trials) is computed over
   every model/feature configuration tried on TRAIN+VALIDATION, and
   the TEST reading is deflated by it.
4. The vol-tautology kill line (below) runs BEFORE any priming claim
   is interpreted.
