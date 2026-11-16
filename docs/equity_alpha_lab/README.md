# equity-alpha-lab (Month 1: research-grade data pipeline)

Point-in-time equity data infrastructure for the six-month equity-alpha
programme. **Descriptive infrastructure only** — no factor, model, or claim
is tested by this package yet. It exists so that every later feature and
target can be traced to information available at decision time, in the
same pre-registration discipline the rest of this repository uses.

## The three design rules

1. **Prices and adjustment factors are stored separately.** Total returns
   are computed, never back-filled into the price column, so any corporate
   action can be re-derived and audited (`returns.total_return_series`).
2. **Every fundamental carries both `period_end` and `announce_date`.**
   Only `announce_date` enters point-in-time logic. Keying on `period_end`
   is the classic lookahead, and the tripwire is built to catch exactly
   that (`pit.assert_no_future_information`).
3. **The security master stores membership intervals, not a current-ticker
   list.** Delisted securities survive; survivorship bias is a number the
   audit reports, not a silent property of the data
   (`universe.survivorship_audit`).

## Modules

| Module | Purpose |
|---|---|
| `schema.py` | Canonical panel schemas + validators (reject announce-before-period-end, bad intervals, duplicates, non-positive prices/factors). |
| `universe.py` | `universe_asof` (half-open membership intervals) and `survivorship_audit`. |
| `pit.py` | `pit_fundamentals` (latest announce_date <= as-of) and the leakage tripwire `assert_no_future_information`. |
| `returns.py` | `total_return_series` (split/dividend-continuous) and `forward_returns` (entry at next open, delisting returns, explicit drops). |
| `quality.py` | `adjustment_continuity_report` (big unadjusted gap with no factor change), `missingness_report`, `check_panel`, `LeakageError`. |

## Declared conventions (frozen before any real data)

- **Decision time:** close of trading date t.
- **Execution:** open of t+1 (`entry_delay=1`; same-close execution is
  rejected by the API).
- **Horizon:** h trading days after entry, on the total-return index.
- **Announcement timing:** a record announced exactly on the as-of date is
  available at that date's close (documented convention).
- **Delisting:** the security master's `delisting_return` is applied at the
  last available trading date. A security with no exit price and no
  delisting return is returned with `dropped=True` and must be counted by
  the caller — never silently filled.

## Schema

See `schema.py` docstrings for the canonical columns. In short:

- `security_master`: sid, ticker, member_start, member_end (NaT = active),
  exchange, delisting_return.
- `prices`: sid, date, open/high/low/close (UNADJUSTED), adj_factor
  (cumulative total-return factor), volume.
- `fundamentals`: sid, field, period_end, announce_date, value.

## Tests

`tests/test_equity_alpha_lab.py` — 15 tests on synthetic panels where the
ground truth is known by construction. The leakage tests deliberately
build cheating snapshots (period-end-keyed fundamentals) and require the
tripwire to fire. Run with `python3 -m pytest tests/test_equity_alpha_lab.py`.

## Data source decision

See `data_source_evaluation.md` — the source must be chosen and its
survivorship characteristics audited BEFORE any factor code is written.

## Limitations

- `forward_returns` is a per-security Python loop; fine for research-scale
  panels, needs vectorization before 10k-name universes.
- No real data is ingested yet; every test is synthetic. The first real
  ingestion must run `check_panel` and publish the findings.
- `adj_factor` is assumed to be a cumulative total-return factor (splits
  AND dividends); the source evaluation must verify this per vendor.
- Trading-calendar handling assumes the panel's own date union as the
  calendar; a proper exchange calendar (holidays) is Month-1 follow-up work.
- US equities only; no point-in-time index membership (e.g. S&P
  constituent history) is wired in yet.
