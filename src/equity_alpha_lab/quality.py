"""Data-quality checks and the leakage error type.

adjustment_continuity_report: a split or dividend must show up as a jump in
adj_factor with NO jump in the unadjusted close beyond the action, and the
total-return series must be continuous across the action. Large single-day
unadjusted gaps WITHOUT an adj_factor change are the classic sign of a bad
corporate-actions table.

missingness_report: per-sid counts of missing trading dates relative to the
panel's own calendar (the union of dates the exchange was open, proxied by
the dates any security traded).

check_panel: one-call audit that runs the schema validators plus the
continuity check and returns a dict of findings. It raises on schema
violations and RETURNS (not raises on) continuity findings, because a
continuity finding is a research decision, not a crash.
"""

from __future__ import annotations

import pandas as pd

from .schema import (
    validate_security_master,
    validate_prices,
    validate_fundamentals,
)


class LeakageError(Exception):
    """Raised when a value can only be explained by future information."""


def adjustment_continuity_report(
    prices: pd.DataFrame,
    max_unexplained_daily_ret: float = 0.20,
) -> pd.DataFrame:
    """Flag large unadjusted close moves with no adj_factor change.

    A row is flagged when |close-to-close return| exceeds
    max_unexplained_daily_ret AND the adj_factor did not change that day.
    Genuine corporate actions change the factor; genuine crashes are rare
    and belong in a manual review list, not in the silently-accepted pile.
    """
    px = validate_prices(prices).sort_values(["sid", "date"])
    ret = px.groupby("sid")["close"].pct_change()
    fac_change = px.groupby("sid")["adj_factor"].diff()
    flagged = px[
        ret.abs().gt(max_unexplained_daily_ret)
        & (fac_change.fillna(0).abs() < 1e-12)
    ].copy()
    flagged["close_ret"] = ret[flagged.index]
    return flagged[
        ["sid", "date", "close", "close_ret", "adj_factor"]
    ].reset_index(drop=True)


def missingness_report(prices: pd.DataFrame) -> pd.DataFrame:
    """Per-sid count of panel dates with no price row."""
    px = validate_prices(prices)
    calendar = pd.DatetimeIndex(sorted(px["date"].unique()))
    rows = []
    for sid, grp in px.groupby("sid"):
        have = pd.DatetimeIndex(grp["date"].unique())
        missing = calendar.difference(have)
        rows.append(
            {
                "sid": sid,
                "panel_dates": len(calendar),
                "observed": len(have),
                "missing": len(missing),
                "first_date": have.min(),
                "last_date": have.max(),
            }
        )
    return pd.DataFrame(rows)


def check_panel(
    security_master: pd.DataFrame,
    prices: pd.DataFrame,
    fundamentals: pd.DataFrame | None = None,
    max_unexplained_daily_ret: float = 0.20,
) -> dict:
    """Full audit. Raises on schema violations; returns findings otherwise."""
    sm = validate_security_master(security_master)
    px = validate_prices(prices)
    fd = validate_fundamentals(fundamentals) if fundamentals is not None else None

    flagged = adjustment_continuity_report(px, max_unexplained_daily_ret)
    missing = missingness_report(px)

    sids_px = set(px["sid"].unique())
    sids_sm = set(sm["sid"].unique())
    findings = {
        "n_securities": len(sids_px),
        "n_security_master": len(sids_sm),
        "prices_without_master": sorted(sids_px - sids_sm),
        "master_without_prices": sorted(sids_sm - sids_px),
        "n_flagged_continuity": len(flagged),
        "continuity_flags": flagged,
        "missingness": missing,
        "n_missing_rows": int(missing["missing"].sum()),
    }
    if fd is not None:
        sids_fd = set(fd["sid"].unique())
        findings["fundamentals_without_prices"] = sorted(sids_fd - sids_px)
        findings["n_fundamental_fields"] = fd["field"].nunique()
    return findings
