# L2 Data Acquisition Spec — Layer 0 Unblocking

Purpose: unblock Layer 0 (book reconstruction), the data-quality screen, and the
first L2 test — C1 re-run at L2 resolution (does the compression effect exist
when the state is measured from the book rather than from daily bars?). Not a
model proposal. No panel run. C5/C6 remain blocked until this data passes
verification; no proxies in the meantime.

## Venue and instrument

- **Instrument: BTCUSDT perpetual, USDT-M.** One instrument, not both. BTC has
  the deepest book and the broadest third-party archive coverage; ETH is the
  fallback only if BTC acquisition fails for venue-specific reasons.
- **Venue: Binance USDT-M (primary).** Deepest book of the two candidates and
  the best-documented diff protocol (`@depth@100ms` full-depth incremental
  diffs with sequence numbers `U`/`u`, plus `aggTrade` with aggressor side).
  Bybit USDT-M is the fallback venue; same field requirements, `orderbook.200`
  diff stream equivalent.
- **Acquisition paths, honestly stated:**
  - (a) Self-recording via WebSocket, from now forward. Free, exact fields
    below, but costs calendar time (2–4 weeks wall clock) and must run on a
    host with exchange connectivity — not inside this sandbox.
  - (b) Purchased historical (e.g. Tardis.dev `incremental_book_L2` +
    `aggTrade` for Binance). Immediate, paid, and must still pass the same
    verification — a purchased "clean" feed without raw-diff verification is
    explicitly excluded from trust.
  - The spec below is venue-protocol-specific for Binance; the Bybit fallback
    maps field-for-field.

## Book feed — full-depth incremental L2 diffs, NOT snapshots

Per update, mandatory fields:

| Field | Requirement |
|---|---|
| Price level | absolute price, exchange precision |
| Size | quantity at level (0 = deletion) |
| Side | bid / ask |
| Exchange timestamp | microsecond resolution |
| Local receive timestamp | microsecond, for latency modeling |
| Sequence numbers | Binance: `U` (first update id), `u` (final), `pu` (previous final). NON-OPTIONAL: gaps must be detectable. A diff whose `pu` does not equal the last applied `u` is a gap; the book is invalid from the gap until a fresh snapshot resync. |

- Depth: full book (Binance diff stream is full-depth; if a level-capped feed
  is the only option, cap >= 500 levels per side and flag it).
- No snapshot-only feeds: snapshots cannot distinguish trade-consuming from
  cancelled liquidity. No volume-bucketed data: VPIN needs tick-level signed
  trades.

## Trades feed — signed aggTrades

Per trade, mandatory fields: price, size, aggressor side (`m` flag: buyer is
maker or taker), exchange timestamp (microsecond), trade ID. Trade ID is
non-optional: it enables reconciliation of trades against book updates (a
level decrease at the touch coinciding with a trade of the same size and side
is a fill; without it, fills and cancels are indistinguishable).

## Coverage

- Continuous, 2–4 weeks minimum, no gaps > 1 second during active sessions.
- Ideally spanning a volatility regime change (a平静→high-vol transition), so
  the scale-invariance null can be re-applied to L2 features. If no regime
  change occurs in the window, record that the null's regime coverage is
  limited and state it in any later result.
- Sequence-gap rate must be logged continuously; a session with unresolvable
  gaps is dropped and reported by timestamp, not patched.

## Storage

- Parquet, partitioned by date (one directory per UTC day).
- Raw diffs preserved verbatim in their own dataset — the reconstructed book
  is DERIVED data, rebuildable from diffs + resync snapshots; never overwrite
  raw with derived.
- Schema: `date / ts_exchange_us / ts_local_us / seq_u / seq_pu / side /
  price / size` for diffs; `date / ts_exchange_us / trade_id / side_aggressor /
  price / size` for aggTrades; resync snapshots in a third dataset with their
  own sequence id.

## Verification (mandatory gate before ANY modeling)

1. Reconstruct the book from incremental diffs (resync from snapshot at start
   and after every detected gap).
2. Pull live exchange-rest snapshots (Binance `depth` REST, weight-limited)
   at >= 100 randomly chosen timestamps spanning the full coverage window.
3. Require: mid agreement within one tick, and depth within 10bps of mid in
   aggregate agreement (per-level size match >= 99% of levels within 10bps).
4. If ANY sampled timestamp disagrees by more than one tick: STOP. Report the
   disagreement rate and the offending timestamps verbatim. Do not proceed to
   modeling, do not tune the reconstruction to pass, do not exclude bad
   timestamps silently.
5. Pre-modeling data-quality screen (per the program declaration): fraction of
   book updates that are cancellations vs trades (needs the trade-ID
   reconciliation), depth within 10bps of mid, autocorrelation of OFI. If
   cancellation activity is near zero, absorption states are indistinguishable
   from frozen liquidity and the Hawkes feature is meaningless — report and
   stop before C5.

## Explicitly excluded

- Snapshot-only feeds (cannot distinguish trade from cancel).
- Volume-bucketed or bar-derived "order flow" (VPIN needs tick-level signed
   trades; daily/minute "OFI" measures neither orders nor flow).
- Third-party "clean" or "normalized" feeds that do not expose raw diffs and
   sequence numbers for independent verification — trust is earned by the
   verification gate, not by vendor claims.
- Any proxy substitution for C5/C6 while blocked.

## Carried-forward methodology constraints (binding on the L2 phase)

- Hazard modeling on event clock (state-change rows), not daily or fixed-grid
  rows; the day-spell design does not carry forward.
- Purge/embargo on label horizon; group-aware purging if ever extended.
- Placebo and scale-invariance nulls re-declared for L2 features BEFORE the
  first run, with the same discipline: the first L2 test is C1 at L2
  resolution, and its kill lines must be restated before it runs.
