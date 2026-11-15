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

## Schema: `paper/research/clue_scan/board_table.csv` (the heat-map board)

Purpose: the unified EVERYTHING board - crypto top-500, commodities,
indexes, large-cap equities and the full S&P 500 scan tables merged into
one ranked table by `src/board_heatmap.py`. Descriptive only; the input
to the heat-map page and the surprise ledger.

| Column | Type | Rule |
|---|---|---|
| `series` | string | scan series name (perp symbol, or lowercase yahoo name) |
| `class` | string | `commodity`, `index`, `equity`, `sp500`, `crypto` |
| `venue` | string | `binance` or `yahoo` |
| `last_date` | string | `YYYY-MM-DD` of the last bar the score was computed on |
| `primed_score` | float | descriptive priming score from `clue_scan.primed_score`; 0-1 |
| `artifact_flag` | bool | move-already-happened: abs 30d return > 20% |
| `genesis_flag` | bool | too new: <90d listing history (crypto) or short-history sp500 addition |
| `eligible` | bool | candidate only if NOT artifact and NOT genesis (and not a stablecoin) |
| `data_file` | string | cached klines CSV the surprise ledger must resolve against |
| `board_rank` | int | 1 = highest primed_score on the whole board |

## Ledger: `logs/board_surprise_ledger.jsonl` (hash-chained, append-only)

Purpose: the time half of the heat map - sealed priming scores vs
realized jumps. Two record types on one SHA-256 chain (same discipline
as `logs/forward_calibration.jsonl`): `snapshot` (top-k eligible
candidates per class sealed at t0 with their full feature vector, no
outcome fields allowed) and `resolution` (max abs close move over the
10-bar horizon, read from the same cached klines, appended only once
the horizon has strictly passed). Monotonic timestamps, verify-before-
write, tamper refuses all writes. Study output:
`paper/research/clue_scan/surprise_study.md` - Spearman rho between
sealed score and realized jump, per class; descriptive only.
