# Drive upload intake audit — 2026-11-16

The owner's Drive "Data" folder (upload in progress at audit time) shows
two Binance Vision aggTrades archives. Both were pulled from the public
source (data.binance.vision) and are byte-identical to the Drive files
(sizes 9,357,158 and 6,893,634 bytes match exactly). The ~1GB parquet
has not appeared in the folder yet; monitoring continues.

## File 1: BTCUSDT-aggTrades-2025-01-01.zip (USDS-M, 9.4 MB)
- 726,611 aggTrades, full-day span 00:00:00.051 → 23:59:59.458 UTC
- 7 columns WITH a header row: agg_trade_id, price, quantity,
  first_trade_id, last_trade_id, transact_time, is_buyer_maker
- Timestamps MILLISECONDS (13-digit) — the ingest normalizer scales to µs
- Price range 92,796.5 – 95,161.2
- Integrity: 0 nulls, 0 duplicate agg_trade_ids, monotonic ids
- Verdict: CLEAN. Same schema as the programme's existing aggTrades
  pipeline (src/binance_ingest.py) — ingests directly.

## File 2: BTCUSD_PERP-aggTrades-2021-02-08.zip (COIN-margined, 6.9 MB)
- 508,984 aggTrades, full-day span 00:00:00.682 → 23:59:59.768 UTC
- 7 columns WITHOUT a header row (data starts at line 1) — a schema
  difference from the 2025-era USDS-M file; the ingest must not assume
  a header for coin-margined/2021-era archives
- Timestamps MILLISECONDS
- Price range 38,062 – 47,000 — this is 2021-02-08, the day of the
  Tesla $1.5bn BTC purchase announcement: an intraday +23% event day
- Integrity: 0 nulls, 0 duplicate ids
- Verdict: CLEAN, and a NEW INSTRUMENT CLASS for the programme — the
  first COIN-margined (dapi) file in the repo. Descriptive note only:
  a significant-event day is a candidate case study for the move
  census's event anatomy, but no claim is tested on one day.

## Standing rule observed
Neither file is order-book data (aggTrades = taker prints), so the L0
gate does not apply. Both ingest through the existing aggTrades path.
No features, no models, no claims run on this data in this unit.
