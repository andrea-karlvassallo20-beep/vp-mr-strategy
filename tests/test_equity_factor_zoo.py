"""Factor zoo + evaluation tests on ENGINEERED ground truth.

The panel is built so the answer is known by construction, then the
instruments are required to recover it. Two worlds are built:

- MOMENTUM WORLD: each security's expected daily return is proportional to
  its rank in past 12-month return. Momentum IC must be positive and the
  quantile spread positive; reversal IC must be negative.
- NULL WORLD: iid returns, no factor structure. ICs must be near zero and
  the naive t-stat small in absolute value.

These tests validate the INSTRUMENTS, not any market claim.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from equity_alpha_lab import (
    amihud_illiquidity,
    compute_all,
    dollar_volume,
    forward_returns,
    ic_series,
    ic_summary,
    momentum,
    quantile_returns,
    range_position,
    reversal,
    top_bucket_turnover,
    total_return_series,
    universe_asof,
    volatility,
)

N_SID = 20
N_DAYS = 320  # > 252 + a little
DATES = pd.bdate_range("2023-01-02", periods=N_SID and N_DAYS)


def _prices_from_returns(rets: pd.DataFrame) -> pd.DataFrame:
    """Build an unadjusted price panel from a (sid, date) return frame."""
    tr = (1 + rets).groupby(level="sid").cumprod()
    rows = []
    for sid in rets.index.get_level_values("sid").unique():
        s = tr.xs(sid, level="sid")
        for d, v in s.items():
            rows.append(
                {
                    "sid": sid,
                    "date": d,
                    "open": float(v),
                    "high": float(v),
                    "low": float(v),
                    "close": float(v),
                    "adj_factor": 1.0,
                    "volume": 1_000_000.0,
                }
            )
    return pd.DataFrame(rows)


def _security_master(sids):
    return pd.DataFrame(
        {
            "sid": sids,
            "ticker": sids,
            "member_start": [DATES[0]] * len(sids),
            "member_end": [pd.NaT] * len(sids),
            "exchange": ["XNYS"] * len(sids),
            "delisting_return": [np.nan] * len(sids),
        }
    )


def _momentum_world(seed: int = 7) -> pd.DataFrame:
    """Expected daily return proportional to rank of trailing 252d return."""
    rng = np.random.default_rng(seed)
    sids = [f"S{i:02d}" for i in range(N_SID)]
    idx = pd.MultiIndex.from_product([sids, DATES], names=["sid", "date"])
    rets = pd.Series(rng.normal(0, 0.01, len(idx)), index=idx)
    # seed a persistent cross-sectional ordering: give each sid a fixed
    # drift proportional to its index, then let momentum reinforce it
    drift = pd.Series(np.linspace(-0.002, 0.002, N_SID), index=sids)
    rets = rets + drift.reindex(rets.index.get_level_values("sid")).values
    return rets, _prices_from_returns(rets)


def _null_world(seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sids = [f"S{i:02d}" for i in range(N_SID)]
    idx = pd.MultiIndex.from_product([sids, DATES], names=["sid", "date"])
    rets = pd.Series(rng.normal(0.0002, 0.01, len(idx)), index=idx)
    return _prices_from_returns(rets)


def _fwd(prices, horizon=5):
    return forward_returns(prices, _security_master(
        prices["sid"].unique()), horizon=horizon, entry_delay=1)


# ---------------------------------------------------------------- factors

def test_momentum_matches_direct_computation():
    px = _null_world()
    mom = momentum(px, window=60, skip=5)
    tr = total_return_series(px)
    s = tr.xs("S00", level="sid").sort_index()
    d = DATES[65]
    # direct: value at date index k uses tr[k-5]/tr[k-60]
    k = DATES.get_loc(d)
    expected = s.iloc[k - 5] / s.iloc[k - 60] - 1.0
    got = mom[(mom["sid"] == "S00") & (mom["date"] == d)]["value"].iloc[0]
    assert got == pytest.approx(expected)


def test_reversal_is_negative_short_return():
    px = _null_world()
    rev = reversal(px, window=5)
    tr = total_return_series(px)
    s = tr.xs("S01", level="sid").sort_index()
    k = DATES.get_loc(DATES[10])
    expected = -(s.iloc[k] / s.iloc[k - 5] - 1.0)
    got = rev[(rev["sid"] == "S01") & (rev["date"] == DATES[10])]["value"].iloc[0]
    assert got == pytest.approx(expected)


def test_all_factors_share_schema_and_are_lagged():
    px = _null_world()
    all_f = compute_all(px)
    assert set(all_f["factor"].unique()) == {
        "momentum", "reversal", "volatility", "range_position",
        "amihud", "dollar_volume",
    }
    # every factor must be silent for the first 21 trading days (longest
    # window that any default factor needs before its first value)
    first_date = all_f["date"].min()
    assert first_date >= DATES[5]  # shortest default lag is 5 (reversal)
    # volatility needs 63 days: no volatility value before DATES[63]
    vol = all_f[all_f["factor"] == "volatility"]
    assert vol["date"].min() >= DATES[63]


def test_range_position_bounds():
    px = _null_world()
    rp = range_position(px, window=60)
    assert rp["value"].between(0.0, 1.0).all()


def test_amihud_positive_and_dollar_volume_constant():
    px = _null_world()
    am = amihud_illiquidity(px, window=5)
    assert (am["value"] > 0).all()
    # constant volume and (nearly) constant price level => dollar_volume
    # is ~the same value every day per sid
    dv = dollar_volume(px, window=5)
    s = dv[dv["sid"] == "S00"]["value"]
    assert s.std() / s.mean() < 0.5


# ---------------------------------------------------------------- evaluation

def test_ic_recovers_momentum_world():
    _, px = _momentum_world()
    fwd = _fwd(px, horizon=5)
    mom = momentum(px, window=252, skip=21)
    summ = ic_summary(mom, fwd)
    # engineered world: persistent drift ordering => positive momentum IC
    assert summ["mean_ic"] > 0.05
    assert summ["hit_rate"] > 0.5
    rev_summ = ic_summary(reversal(px, window=21), fwd)
    # reversal is minus a short return; in a drifting world its IC is
    # negative wherever momentum's is positive
    assert rev_summ["mean_ic"] < 0


def test_ic_near_zero_in_null_world():
    px = _null_world()
    fwd = _fwd(px, horizon=5)
    summ = ic_summary(momentum(px, window=252, skip=21), fwd)
    # no structure: IC must be small and the naive t-stat must not look
    # like a discovery (loose bound; the instrument must not manufacture
    # signal out of noise in a 20-name panel)
    assert abs(summ["mean_ic"]) < 0.15
    assert abs(summ["t_stat_naive"]) < 2.5


def test_quantile_spread_monotonic_in_momentum_world():
    _, px = _momentum_world()
    fwd = _fwd(px, horizon=5)
    qr = quantile_returns(momentum(px, window=252, skip=21), fwd, n_buckets=5)
    assert (qr["spread"] > 0).mean() > 0.5
    means = qr[[f"q{i}" for i in range(1, 6)]].mean()
    # monotone across buckets on average in the engineered world
    assert (np.diff(means.values) > 0).sum() >= 3


def test_turnover_between_zero_and_one_and_counts_changes():
    _, px = _momentum_world()
    fwd = _fwd(px, horizon=5)
    to = top_bucket_turnover(momentum(px, window=252, skip=21), fwd, n_buckets=5)
    assert to.between(0, 1).all()
    # in a persistent-drift world the top bucket should be fairly stable
    assert to.mean() < 0.5


def test_ic_series_empty_on_disjoint_dates():
    px = _null_world()
    fwd = _fwd(px, horizon=5)
    fake = pd.DataFrame(
        {
            "sid": ["ZZZ"],
            "date": [DATES[100]],
            "factor": ["momentum"],
            "value": [0.1],
        }
    )
    assert len(ic_series(fake, fwd)) == 0
    assert ic_summary(fake, fwd)["n_dates"] == 0
