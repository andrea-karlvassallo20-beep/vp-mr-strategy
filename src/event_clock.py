"""Event-clock state-change rows, purged combinatorial CV, embargo.

Infrastructure only. No labels from market data are produced here; the dry
run uses toy labels. The event clock in this dry run is the TRADE clock
(aggTrades only). The quote-clock BBBA generator is implemented for
bookTicker-format frames; Binance publishes no bookTicker archive, so the
quote clock runs on synthetic frames in tests until a real feed exists.
"""

import numpy as np
import pandas as pd


def trade_clock_rows(trades: pd.DataFrame, price_tick: float = 0.1) -> pd.DataFrame:
    """State-change rows on the trade clock: one row per trade that CHANGES
    the state (here: the last-traded price moves by >= 1 tick, or the
    aggressor side flips). Self-thins dead sessions by construction: no
    trades, no rows."""
    req = {"ts_exchange_us", "price", "aggressor_buy"}
    if not req.issubset(trades.columns):
        raise ValueError(f"trades missing columns: {req - set(trades.columns)}")
    t = trades.sort_values("ts_exchange_us", kind="stable").reset_index(drop=True)
    dp = t["price"].diff().fillna(0.0)
    side = t["aggressor_buy"].diff().fillna(1)
    changed = (dp.abs() >= price_tick) | (side != 0)
    rows = t[changed].copy()
    rows["state_change_kind"] = np.where(
        dp[changed] >= price_tick, "price_up",
        np.where(dp[changed] <= -price_tick, "price_down", "side_flip"),
    )
    return rows.reset_index(drop=True)


def bbba_clock_rows(book: pd.DataFrame) -> pd.DataFrame:
    """Quote-clock state-change rows from bookTicker-format frames: one row
    per update that changes mid, spread, or top-of-book sizes."""
    req = {"ts_exchange_us", "bid_price", "bid_qty", "ask_price", "ask_qty"}
    if not req.issubset(book.columns):
        raise ValueError(f"book missing columns: {req - set(book.columns)}")
    b = book.sort_values("ts_exchange_us", kind="stable").reset_index(drop=True)
    changed = (
        b["bid_price"].diff().fillna(0).ne(0)
        | b["ask_price"].diff().fillna(0).ne(0)
        | b["bid_qty"].diff().fillna(0).ne(0)
        | b["ask_qty"].diff().fillna(0).ne(0)
    )
    rows = b[changed].copy()
    rows["mid"] = (rows["bid_price"] + rows["ask_price"]) / 2.0
    rows["spread"] = rows["ask_price"] - rows["bid_price"]
    return rows.reset_index(drop=True)


def purged_cpcv_splits(row_ts: np.ndarray, n_groups: int = 6,
                       label_horizon_us: int = 0, embargo_us: int = 0,
                       n_test_groups: int = 1):
    """Purged combinatorial CV on wall-clock.

    row_ts: decision-row timestamps (microseconds, sorted).
    Groups are contiguous wall-clock blocks. A training row is PURGED if its
    label window [t0, t0 + label_horizon_us] intersects the test window
    extended by the embargo on both sides. Purge is on the LABEL horizon,
    not the feature horizon.

    Yields dicts with test indices and purged train indices. The dry-run
    caller asserts zero overlap between train label windows and the
    (test + embargo) region.
    """
    row_ts = np.asarray(row_ts)
    if len(row_ts) and np.any(np.diff(row_ts) < 0):
        raise ValueError("row_ts must be sorted")
    n = len(row_ts)
    edges = np.linspace(0, n, n_groups + 1).astype(int)
    gids = np.zeros(n, dtype=int)
    for g in range(n_groups):
        gids[edges[g] : edges[g + 1]] = g

    def group_bounds(gs):
        m = np.isin(gids, gs)
        return row_ts[m].min(), row_ts[m].max()

    from itertools import combinations
    for test_groups in combinations(range(n_groups), n_test_groups):
        test_mask = np.isin(gids, test_groups)
        test_idx = np.where(test_mask)[0]
        lo, hi = group_bounds(test_groups)
        win_lo = lo - embargo_us
        win_hi = hi + label_horizon_us + embargo_us
        train_candidate = np.where(~test_mask)[0]
        keep = ~(
            (row_ts[train_candidate] + label_horizon_us >= win_lo)
            & (row_ts[train_candidate] <= win_hi)
        )
        train_idx = train_candidate[keep]
        yield {
            "test_groups": test_groups,
            "test_idx": test_idx,
            "train_idx": train_idx,
            "purged": int(len(train_candidate) - len(train_idx)),
            "test_bounds": (float(lo), float(hi)),
            "purge_window": (float(win_lo), float(win_hi)),
        }


def assert_no_leakage(split: dict, row_ts: np.ndarray, label_horizon_us: int,
                      embargo_us: int) -> int:
    """Kill-line check. A train row is a violation iff its label window
    [s, s+H] intersects [test_lo - embargo, test_hi + H + embargo] — the
    exact complement of the purge condition. Returns violation count
    (0 required); raises with detail otherwise."""
    lo, hi = split["test_bounds"]
    s = row_ts[split["train_idx"]]
    e = s + label_horizon_us
    bad = (e >= lo - embargo_us) & (s <= hi + label_horizon_us + embargo_us)
    n = int(bad.sum())
    if n:
        raise AssertionError(f"{n} train/test label-window overlaps")
    return 0
