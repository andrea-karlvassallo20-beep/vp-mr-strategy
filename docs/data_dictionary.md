# Data Dictionary — Free Binance Public Archives (Prep Sprint)

Scope: the free `data.binance.vision` archives for BTCUSDT — **aggTrades** and
**bookTicker** — plus the curated macro timeline. This is PREP data only. The
Tardis full-depth incremental L2 remains the Layer 0 requirement per
`paper/research/l2_data_acquisition_spec.md`; nothing in this document replaces
it.

## Honest capability statement (read before using any of this)

| Feed | What it is | What it CAN measure | What it CANNOT measure |
|---|---|---|---|
| aggTrades | Signed trades (aggressor side) | Trade sign, trade intensity, aggressor imbalance, VPIN on trade-count buckets, Hawkes trade-to-trade excitation | Anything about resting liquidity |
| bookTicker | Best bid/ask + sizes, every update | Spread, top-of-book imbalance (microstructure proxy), quote-update intensity | Depth beyond the touch; cancellations vs trades (a bid size decrease is either); book reconstruction. It is a snapshot stream, NOT incremental L2 — the acquisition spec explicitly excludes snapshot-only feeds from Layer 0 |
| macro_timeline | Curated event calendar | Regime context, event windows for censoring/stratification | Nothing market-internal |

Consequence, pre-declared: claims C5 (absorption asymmetry) and C6 (depth OFI)
remain **blocked on the Tardis data** even when these free feeds are ingested.
The free data can support trade-flow analyses only, and any result derived
from it will be labeled free-data / partial-book, never presented as a test
of a book-based claim.

## Timestamp rule (strict, non-negotiable)

- All timestamps are **UTC, epoch microseconds, int64**, column
  `ts_exchange_us`.
- Source archives are milliseconds; conversion is `ms * 1000`, exact, no
  float intermediates, no NaN. A row that fails timestamp coercion raises
  and kills the file — bad rows are never dropped silently.
- Rows must be non-decreasing in `ts_exchange_us`; out-of-order rows are
  sorted (stable) and the violation is reported, never ignored.
- No local timestamps in the free data (Binance archives are exchange time
  only). Local receive-time latency modeling requires the self-recorded or
  Tardis feed and is out of scope here.

## Binary flag rule (strict)

- Trade direction is stored as `aggressor_buy` **int8**: `1` = aggressor
  buys, `0` = aggressor sells.
- Source field `is_buyer_maker`: `true` means the buyer was the maker, so
  the AGGRESSOR sold -> `aggressor_buy = 0`; `false` -> `aggressor_buy = 1`.
- Accepted literals: `true/false`, `t/f`, `1/0` (case-insensitive). Anything
  else raises and kills the file. No third state exists; no NaNs permitted.

## Schema: aggTrades (normalized)

Loader: `src/binance_ingest.py::load_agg_trades`
Output: `data/processed/aggtrades/<source-stem>.parquet`

| Column | Type | Rule |
|---|---|---|
| `ts_exchange_us` | int64 | UTC µs, from `transact_time` (ms) |
| `trade_id` | int64 | `agg_trade_id` |
| `price` | float64 | > 0, else file rejected |
| `size` | float64 | >= 0, else rejected |
| `aggressor_buy` | int8 | 1/0 per the binary flag rule |

Source columns (Binance vision CSV): `agg_trade_id, price, quantity,
first_trade_id, last_trade_id, transact_time, is_buyer_maker`. Headerless
legacy files are supported (fixed column order assumed).

## Schema: bookTicker (normalized)

Loader: `src/binance_ingest.py::load_book_ticker`
Output: `data/processed/bookticker/<source-stem>.parquet`

| Column | Type | Rule |
|---|---|---|
| `ts_exchange_us` | int64 | UTC µs, from `event_time` (futures) else `transaction_time` (spot) |
| `update_id` | int64 | sequence id of the best-bid/ask update |
| `bid_price` | float64 | > 0 |
| `bid_qty` | float64 | >= 0 |
| `ask_price` | float64 | > 0 |
| `ask_qty` | float64 | >= 0 |

Integrity invariants enforced at load: `bid_price <= ask_price` (a crossed
row rejects the file), all prices > 0, all qty >= 0, timestamps
non-decreasing.

## Ingestion

```
python3 src/binance_ingest.py aggtrades  --src data/raw/aggTrades   --out data/processed/aggtrades
python3 src/binance_ingest.py bookticker --src data/raw/bookTicker  --out data/processed/bookticker
```

- Accepts `.csv` and `.zip` (one csv per zip), daily or monthly archives.
- One parquet per source file; raw archives are never modified.
- Raw and processed data are git-ignored (see `.gitignore`); only code,
  schemas, and the curated macro timeline are versioned.

## Schema: `data/macro_timeline.csv` (curated by Andrea)

Purpose: known scheduled macro/crypto events, used for regime context,
event-window stratification, and censoring decisions in later hazard work.
Populated by hand; validated by a loader (to be added with the first use).

| Column | Type | Rule |
|---|---|---|
| `event_id` | string | unique, stable; `YYYYMMDD-HHMM-<slug>` |
| `event_date_utc` | string | `YYYY-MM-DD` (UTC) |
| `event_time_utc` | string | `HH:MM` 24h UTC; `00:00` if intraday time unknown (all-day flag) |
| `all_day` | int8 | 1 if the event has no single decision moment (e.g. a weekend summit) |
| `event_type` | string | controlled vocabulary: `FOMC`, `CPI`, `NFP`, `PCE`, `GDP`, `ECB`, `BOE`, `CRYPTO_REGULATORY`, `EXCHANGE_EVENT`, `HALVING`, `ETF_FLOW_REPORT`, `OTHER` |
| `asset_scope` | string | `ALL`, `BTC`, `ETH`, `CRYPTO`, `EQUITIES`, ... |
| `expected_resolution_utc` | string | `YYYY-MM-DD HH:MM` when the outcome becomes public; empty if unknown |
| `surprise_note` | string | free text, filled AFTER the event only; never used as a feature (it is look-ahead by construction) |
| `source` | string | citation or URL |
| `confidence` | string | `confirmed` / `expected` / `rumored` |

Rules: one row per event; times in UTC only; `surprise_note` is annotation,
never a model input; unknown values are empty strings, never `NULL`/`NaN`
placeholders invented by tooling.
