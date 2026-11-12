import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from features import (
    vpin_trade_buckets, fit_hawkes, hawkes_loglik, top_of_book_ofi,
    band_depth_ofi_proxy,
)
from event_clock import (
    trade_clock_rows, bbba_clock_rows, purged_cpcv_splits, assert_no_leakage,
)


def _trades(n=10000, seed=0):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "ts_exchange_us": np.sort(rng.integers(0, 10**12, n)).astype("int64"),
        "trade_id": np.arange(n),
        "price": 50000 + np.cumsum(rng.normal(0, 1, n)),
        "size": rng.uniform(0.001, 2.0, n),
        "aggressor_buy": rng.integers(0, 2, n).astype("int8"),
    })


def test_vpin_bounds_and_no_nan():
    v = vpin_trade_buckets(_trades(), bucket_size=500)
    assert len(v) == 20
    assert v["imbalance"].between(0, 1).all()
    assert v["vpin"].between(0, 1).all()
    assert not v.isna().any().any()
    assert (v["buy_vol"] + v["sell_vol"] > 0).all()


def test_vpin_extremes():
    t = _trades(1000)
    t["aggressor_buy"] = 1
    v = vpin_trade_buckets(t, bucket_size=100)
    assert (v["imbalance"] == 1).all()


def _simulate_hawkes(mu, alpha, beta, T, rng):
    """Exact thinning simulation of a d-dim exponential-kernel Hawkes."""
    d = len(mu)
    t = []
    y = []
    cur = 0.0
    R = np.zeros(d)
    while True:
        lam = mu + alpha @ R
        dt = rng.exponential(1.0 / lam.sum())
        cur += dt
        if cur >= T:
            break
        R *= np.exp(-beta * dt)
        lam_now = mu + alpha @ R
        if rng.random() < lam_now.sum() / max(lam.sum(), 1e-12):
            typ = rng.choice(d, p=lam_now / lam_now.sum())
            t.append(cur)
            y.append(typ)
            R[typ] += 1.0
    return np.array(t), np.array(y, dtype=int)


def test_hawkes_recovers_excitation():
    rng = np.random.default_rng(1)
    mu = np.array([0.2, 0.2])
    alpha = np.array([[0.8, 0.1], [0.1, 0.8]])
    beta = 2.0
    t, y = _simulate_hawkes(mu, alpha, beta, 600.0, rng)
    assert len(t) > 200
    fit = fit_hawkes(t * 1e6, y, beta=beta)
    assert fit["converged"]
    assert fit["branching_ratio"] < 1.0
    assert fit["branching_ratio"] > 0.3
    assert not np.isnan(fit["mu"]).any()
    assert not np.isnan(np.array(fit["alpha"])).any()


def test_hawkes_loglik_finite_on_real_shaped_data():
    rng = np.random.default_rng(2)
    t = np.sort(rng.uniform(0, 100, 500))
    y = rng.integers(0, 2, 500)
    ll = hawkes_loglik(t, y, 100.0, np.array([0.5, 0.5]),
                       np.array([[0.1, 0.0], [0.0, 0.1]]), 2.0)
    assert np.isfinite(ll)


def test_ofi_touch_moves():
    book = pd.DataFrame({
        "ts_exchange_us": np.arange(5, dtype="int64") * 10**6,
        "update_id": np.arange(5),
        "bid_price": [100.0, 100.1, 100.1, 100.0, 100.0],
        "bid_qty": [1.0, 1.0, 2.0, 2.0, 3.0],
        "ask_price": [100.2, 100.2, 100.2, 100.1, 100.1],
        "ask_qty": [1.0, 1.0, 1.0, 1.0, 2.0],
    })
    ofi = top_of_book_ofi(book)
    assert len(ofi) == 5
    assert not ofi["ofi"].isna().any()
    assert ofi["ofi"].iloc[1] == 1.0
    assert ofi["ofi"].iloc[3] == -1.0


def test_band_depth_proxy():
    bd = pd.DataFrame({
        "timestamp": ["2024-08-05 00:00:05"] * 2 + ["2024-08-05 00:00:10"] * 2,
        "percentage": [-1, 1, -1, 1],
        "depth": [1.0, 1.0, 1.0, 1.0],
        "notional": [100.0, 90.0, 120.0, 95.0],
    })
    p = band_depth_ofi_proxy(bd)
    assert len(p) == 1
    assert p["ofi_proxy"].iloc[0] == pytest.approx((120 - 100) - (95 - 90))


def test_trade_clock_self_thins_and_tags():
    t = _trades(1000, seed=3)
    t["price"] = 50000.0
    rows = trade_clock_rows(t)
    assert (rows["state_change_kind"] == "side_flip").all()
    assert len(rows) < len(t)


def test_bbba_clock_rows():
    book = pd.DataFrame({
        "ts_exchange_us": np.arange(6, dtype="int64"),
        "update_id": np.arange(6),
        "bid_price": [1, 1, 1, 1, 1, 1],
        "bid_qty": [1, 1, 2, 2, 2, 2],
        "ask_price": [2, 2, 2, 3, 3, 3],
        "ask_qty": [1, 1, 1, 1, 1, 4],
    }, dtype=float)
    rows = bbba_clock_rows(book)
    assert len(rows) == 3
    assert rows["mid"].iloc[0] == 1.5
    assert rows["spread"].tolist() == [1.0, 2.0, 2.0]


def test_cpcv_zero_leakage_with_toy_labels():
    rng = np.random.default_rng(4)
    n = 6000
    row_ts = np.sort(rng.integers(0, 10**12, n)).astype("int64")
    horizon = int(10**11)
    embargo = int(10**10)
    toy_label = rng.integers(0, 2, n)
    assert len(toy_label) == n
    total_purged = 0
    n_splits = 0
    for split in purged_cpcv_splits(row_ts, n_groups=6,
                                    label_horizon_us=horizon,
                                    embargo_us=embargo, n_test_groups=1):
        assert_no_leakage(split, row_ts, horizon, embargo)
        assert set(split["train_idx"]).isdisjoint(split["test_idx"])
        total_purged += split["purged"]
        n_splits += 1
    assert n_splits == 6
    assert total_purged > 0


def test_cpcv_rejects_unsorted():
    with pytest.raises(ValueError):
        list(purged_cpcv_splits(np.array([3, 1, 2])))
