# Second aggTrades window prepared: 2024-08-01 → 2025-02-28

Infrastructure only. No claims tested; the T1/T2 decision remains the
owner's (memo: paper/research/t1_t2_decision_memo_2026-11-16.md).

## What exists now

- **212 of 212 calendar days** (zero missing dates), BTCUSDT USDS-M
  daily aggTrades from Binance Vision, converted to the programme's
  normalized parquet schema (int64 UTC microseconds, int8
  aggressor_buy) via src/binance_ingest.py — 212/212 conversions, 0
  failures.
- **333,527,416 aggTrades total.**
- Timestamp unit verified at both ends of the window (16-digit =
  microseconds, as required).

## Why this window matters (when the owner decides)

The T3-tested-fail harness and its cached spells live on the
2026-05-15 → 2026-11-14 window. This 2024-08 → 2025-02 window is a
**separate, earlier period**: if the owner decides to run T1, this
window enables the honest question the first window cannot answer
alone — does the compression duration-dependence (or its death)
**reproduce in a different regime**? The scale-invariance null and the
block-temporal placebo are stronger when they are asked on a period
the harness never saw during construction. The harness's
`--claims t1` path with this window as input is ready the moment the
decision lands.

## Standing constraints, unchanged

- aggTrades = taker prints only; no book, no cancellations — the
  passive-withdrawal mechanism observed in the Tesla-day anatomy is
  INVISIBLE here and no taker proxy may be substituted for it (the
  C5/C6 no-proxy-substitution rule).
- Nothing in this unit ran a model, computed a feature, or touched a
  claim.
