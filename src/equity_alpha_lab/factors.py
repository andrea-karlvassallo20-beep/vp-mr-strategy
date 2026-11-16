"""Price-based cross-sectional factors (Month 2: the factor zoo, price wing).

DESCRIPTIVE ONLY. Nothing here tests a claim. Each function consumes the
validated prices panel and returns a LONG frame (sid, date, value) where the
value at date t uses ONLY information available at the close of t — the
same decision-time convention the pipeline froze in Month 1.

All factors are computed on the total-return series (split/dividend-safe)
except the liquidity factors, which need dollar volume and therefore use
unadjusted close x volume (a trading-cost proxy, correctly unadjusted).

Fundamental factors (value, quality) are deliberately absent: they stay
blocked until a point-in-time fundamentals source passes the
data_source_evaluation gate. Adding them before that gate would be the
exact sin the gate exists to prevent.
"""

from __future__ import annotations

import pandas as pd

from .returns import total_return_series
from .schema import validate_prices


def _long_frame(values: pd.Series, name: str) -> pd.DataFrame:
    out = values.rename(name).reset_index()
    out.columns = ["sid", "date", "value"]
    out["factor"] = name
    return out[["sid", "date", "factor", "value"]]


def momentum(prices: pd.DataFrame, window: int = 252, skip: int = 21) -> pd.DataFrame:
    """Medium-term momentum: total return from t-window to t-skip.

    The 21-day skip is the standard crash-avoidance lag (a stock that
    crashed in the last month is not a momentum winner). Returns the raw
    return, NOT z-scored: cross-sectional standardization happens at
    evaluation time, once, under a declared convention.
    """
    tr = total_return_series(prices)
    lagged = tr.groupby(level="sid").shift(skip)
    base = tr.groupby(level="sid").shift(window)
    mom = (lagged / base - 1.0).dropna()
    return _long_frame(mom, "momentum")


def reversal(prices: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Short-term reversal: NEGATIVE of the past `window`-day total return."""
    tr = total_return_series(prices)
    base = tr.groupby(level="sid").shift(window)
    rev = -(tr / base - 1.0)
    return _long_frame(rev.dropna(), "reversal")


def volatility(prices: pd.DataFrame, window: int = 63) -> pd.DataFrame:
    """Trailing realized volatility of daily total returns (unannualized)."""
    tr = total_return_series(prices)
    ret = tr.groupby(level="sid").pct_change()
    vol = ret.groupby(level="sid").rolling(window).std().reset_index(level=0, drop=True)
    return _long_frame(vol.dropna(), "volatility")


def range_position(prices: pd.DataFrame, window: int = 252) -> pd.DataFrame:
    """Position of the total-return index in its trailing range, 0..1."""
    tr = total_return_series(prices)
    roll_min = tr.groupby(level="sid").rolling(window).min().reset_index(level=0, drop=True)
    roll_max = tr.groupby(level="sid").rolling(window).max().reset_index(level=0, drop=True)
    pos = (tr - roll_min) / (roll_max - roll_min)
    return _long_frame(pos.dropna(), "range_position")


def amihud_illiquidity(prices: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Amihud: mean of |daily total return| / dollar volume over `window`.

    Units are per-dollar; the cross-sectional rank is what matters. Uses
    unadjusted close x volume (dollar volume actually traded).
    """
    px = validate_prices(prices).sort_values(["sid", "date"])
    tr = total_return_series(px)
    ret = tr.groupby(level="sid").pct_change()
    dollar_vol = px["close"] * px["volume"]
    dollar_vol.index = tr.index
    illiq = (ret.abs() / dollar_vol).groupby(level="sid").rolling(window).mean().reset_index(level=0, drop=True)
    return _long_frame(illiq.dropna(), "amihud")


def dollar_volume(prices: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Trailing mean dollar volume (liquidity/size proxy; log not applied)."""
    px = validate_prices(prices).sort_values(["sid", "date"])
    dv = (px["close"] * px["volume"])
    dv.index = pd.MultiIndex.from_frame(px[["sid", "date"]])
    roll = dv.groupby(level="sid").rolling(window).mean().reset_index(level=0, drop=True)
    return _long_frame(roll.dropna(), "dollar_volume")


PRICE_FACTORS = {
    "momentum": momentum,
    "reversal": reversal,
    "volatility": volatility,
    "range_position": range_position,
    "amihud": amihud_illiquidity,
    "dollar_volume": dollar_volume,
}


def compute_all(prices: pd.DataFrame) -> pd.DataFrame:
    """All price-based factors stacked in long format (sid, date, factor, value)."""
    frames = [fn(prices) for fn in PRICE_FACTORS.values()]
    return pd.concat(frames, ignore_index=True)
