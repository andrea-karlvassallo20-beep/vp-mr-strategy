"""Canonical schemas for the point-in-time equity panel.

Design rules (the whole point of Month 1):
1. Unadjusted prices and adjustment factors are stored SEPARATELY. Total
   returns are computed, never back-filled into the price column, so a
   corporate action can always be re-derived and audited.
2. Every fundamental carries BOTH period_end (the fiscal period it
   describes) and announce_date (when it became public). Only announce_date
   enters point-in-time logic; period_end alone is the classic lookahead.
3. The security master carries membership intervals, not a current-ticker
   list, so delisted securities survive and survivorship bias is auditable.
"""

from __future__ import annotations

import pandas as pd

SECURITY_MASTER_COLUMNS = {
    "sid": "object",          # stable security id, survives ticker changes
    "ticker": "object",       # ticker as of membership start (informational)
    "member_start": "datetime64[ns]",  # first date in the universe
    "member_end": "datetime64[ns]",    # delisting/exit date (NaT = still active)
    "exchange": "object",
    "delisting_return": "float64",     # fractional return over the delisting
                                        # event; NaN if none/unknown
}

PRICE_COLUMNS = {
    "sid": "object",
    "date": "datetime64[ns]",          # trading date, already calendar-aligned
    "open": "float64",
    "high": "float64",
    "low": "float64",
    "close": "float64",                # UNADJUSTED close
    "adj_factor": "float64",           # cumulative total-return adjustment,
                                        # grows with each split/dividend
    "volume": "float64",
}

FUNDAMENTALS_COLUMNS = {
    "sid": "object",
    "field": "object",                 # e.g. "earnings", "book_value"
    "period_end": "datetime64[ns]",    # fiscal period end
    "announce_date": "datetime64[ns]", # publication date; the PIT key
    "value": "float64",
}

REQUIRED = {"sid", "date"}


def _check_columns(frame: pd.DataFrame, spec: dict, name: str) -> None:
    missing = set(spec) - set(frame.columns)
    if missing:
        raise ValueError(f"{name} missing columns: {sorted(missing)}")


def validate_security_master(frame: pd.DataFrame) -> pd.DataFrame:
    _check_columns(frame, SECURITY_MASTER_COLUMNS, "security_master")
    sm = frame.copy()
    if sm["member_start"].isna().any():
        raise ValueError("security_master: member_start must not be NaT")
    bad = sm[sm["member_end"].notna() & (sm["member_end"] < sm["member_start"])]
    if len(bad):
        raise ValueError(
            f"security_master: {len(bad)} rows with member_end < member_start"
        )
    if sm.duplicated(subset=["sid", "member_start"]).any():
        raise ValueError("security_master: duplicate (sid, member_start) rows")
    return sm


def validate_prices(frame: pd.DataFrame) -> pd.DataFrame:
    _check_columns(frame, PRICE_COLUMNS, "prices")
    px = frame.copy()
    if px.duplicated(subset=["sid", "date"]).any():
        raise ValueError("prices: duplicate (sid, date) rows")
    if (px["close"] <= 0).any():
        raise ValueError("prices: non-positive close")
    if (px["adj_factor"] <= 0).any():
        raise ValueError("prices: non-positive adjustment factor")
    return px


def validate_fundamentals(frame: pd.DataFrame) -> pd.DataFrame:
    _check_columns(frame, FUNDAMENTALS_COLUMNS, "fundamentals")
    fd = frame.copy()
    if fd["announce_date"].isna().any():
        raise ValueError("fundamentals: announce_date must not be NaT")
    look_ahead = fd[fd["announce_date"] < fd["period_end"]]
    if len(look_ahead):
        raise ValueError(
            f"fundamentals: {len(look_ahead)} rows announced before period end "
            "(impossible: announce_date must be >= period_end)"
        )
    if fd.duplicated(subset=["sid", "field", "period_end"]).any():
        raise ValueError("fundamentals: duplicate (sid, field, period_end) rows")
    return fd
