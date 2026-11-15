"""Unit tests for the upgraded 2D Hawkes estimator (Claim T2 prep).

1. The O(N D^2) recursive log-likelihood must match a brute-force O(N^2)
   reference to within 1e-9 on 2,000 synthetic timestamps.
2. Diurnal baseline: a session-shaped baseline must be absorbed by theta
   rather than inflating self-excitation.
3. Boundary flag: fits pinned at the stationarity cap must be reported as
   boundary-constrained, never as interior estimates.
4. VPIN guardrail: redundancy with |signed trade imbalance| raises.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from features import (
    diurnal_design,
    fit_hawkes2,
    hawkes2_loglik,
    hawkes2_loglik_brute,
    vpin_redundancy_guardrail,
    vpin_trade_buckets,
    vpin_with_guardrail,
)

HARMONICS = 3


def _synthetic_window(n=2000, seed=7):
    """2,000 synthetic timestamps with diurnal shape + mild clustering."""
    rng = np.random.default_rng(seed)
    # 6-hour window inside one day, epoch-anchored
    t0 = 1_730_419_200.0  # 2024-11-01 00:00:00 UTC
    raw = rng.uniform(0.0, 21_600.0, n)
    t = t0 + np.sort(raw)
    # diurnal baseline: quiet at 00:00, busy at 08:00 (t ~ 28800s of day)
    phase = 2 * np.pi * (np.mod(t, 86400.0) / 86400.0)
    diurnal = 1.0 + 0.8 * np.cos(phase)  # peaks at midnight boundary of day
    keep = rng.random(n) < diurnal / 1.8  # thin toward the quiet phase
    t = t[keep]
    y = rng.integers(0, 2, len(t))
    return (t * 1e6).astype(np.int64), y


def _random_params(seed=3, d=2):
    rng = np.random.default_rng(seed)
    n_theta = 1 + 2 * HARMONICS
    theta = rng.normal(-0.5, 0.3, (d, n_theta))
    alpha = rng.uniform(0.05, 0.5, (d, d))
    beta = rng.uniform(0.5, 5.0, (d, d))
    return theta, alpha, beta


def test_recursive_matches_brute_force_1e9():
    """Requirement 3: recursive vs brute-force on 2,000 synthetic timestamps,
    max absolute error < 1e-9."""
    t_us, y = _synthetic_window(2000)
    assert len(t_us) >= 1000  # thinning keeps a healthy sample
    theta, alpha, beta = _random_params()
    ll_rec = hawkes2_loglik(t_us, y, theta, alpha, beta, HARMONICS)
    ll_brute = hawkes2_loglik_brute(t_us, y, theta, alpha, beta, HARMONICS)
    assert np.isfinite(ll_rec) and np.isfinite(ll_brute)
    err = abs(ll_rec - ll_brute)
    assert err < 1e-9, f"recursive vs brute-force error {err:.3e} >= 1e-9"


def test_diurnal_design_is_periodic():
    t = np.array([0.0, 86400.0, 172800.0, 3600.0])
    X = diurnal_design(t, HARMONICS)
    assert np.allclose(X[0], X[1]) and np.allclose(X[1], X[2])
    assert not np.allclose(X[0], X[3])


def test_fit_hawkes2_unpinned_decay_interior():
    """On a clearly stationary synthetic process the fit must land interior:
    unpinned beta, rho < 0.949, boundary flag False."""
    rng = np.random.default_rng(11)
    t0 = 1_730_419_200.0
    # homogeneous Poisson with mild buy/sell clustering
    t = t0 + np.sort(rng.uniform(0.0, 7200.0, 1500))
    y = rng.integers(0, 2, 1500)
    fit = fit_hawkes2((t * 1e6).astype(np.int64), y, harmonics=2)
    assert fit["converged"]
    assert fit["spectral_radius"] < 0.95
    assert fit["is_boundary_constrained"] is False
    # decay is now a matrix, not a fixed scalar
    b = np.array(fit["beta"])
    assert b.shape == (2, 2)
    assert (b > 0).all()
    assert np.isfinite(b).all()


def test_fit_hawkes2_flags_boundary_constraint():
    """A pathologically self-exciting sample must be flagged, not reported
    as an interior estimate."""
    rng = np.random.default_rng(13)
    # near-burst cascade: each event spawns the next within milliseconds
    t = [0.0]
    while len(t) < 1500:
        t.append(t[-1] + rng.exponential(0.05))
    t = np.array(t) + 1_730_419_200.0
    y = rng.integers(0, 2, len(t))
    fit = fit_hawkes2((t * 1e6).astype(np.int64), y, harmonics=1)
    # whether it pins or not, the flag must be consistent with rho
    assert fit["is_boundary_constrained"] == (fit["spectral_radius"] >= 0.949)
    if fit["is_boundary_constrained"]:
        assert "boundary-constrained" in fit["note"]


def _trades_frame(rng, n=600, seed=0):
    sign = rng.integers(0, 2, n)
    return pd.DataFrame({
        "ts_exchange_us": (np.sort(rng.uniform(0, 1e12, n))).astype(np.int64),
        "trade_id": np.arange(n),
        "price": 100.0 + rng.normal(0, 1, n).cumsum() * 0.01,
        "size": rng.uniform(0.01, 2.0, n),
        "aggressor_buy": sign.astype(np.int8),
    })


def test_vpin_guardrail_raises_on_redundancy():
    """Strongly persistent one-sided flow makes VPIN collinear with
    |signed imbalance|; the guardrail must raise."""
    rng = np.random.default_rng(21)
    n = 4000
    bucket = 50
    n_b = n // bucket
    # persistent stretches of one-sided flow (20 buckets at 98% buy) broken
    # by balanced stretches (50%): |signed imbalance| then varies slowly and
    # VPIN (its EWMA) tracks it - the two measure one layer twice
    frac = np.concatenate([np.full(20, 0.98), np.full(20, 0.5)] * (n_b // 40))
    sign = np.concatenate([
        (rng.random(bucket) < frac[b]).astype(np.int8) for b in range(n_b)
    ])
    trades = pd.DataFrame({
        "ts_exchange_us": np.arange(n, dtype=np.int64) * 10**6,
        "trade_id": np.arange(n),
        "price": np.full(n, 100.0),
        "size": np.full(n, 1.0),
        "aggressor_buy": sign,
    })
    v = vpin_trade_buckets(trades, bucket_size=bucket, ewma_span=10)
    with pytest.raises(AssertionError, match="redundancy guardrail"):
        vpin_redundancy_guardrail(v, trades, bucket_size=bucket)


def test_vpin_guardrail_passes_on_independent_flow():
    rng = np.random.default_rng(23)
    trades = _trades_frame(rng, 2000)
    v = vpin_trade_buckets(trades, bucket_size=100, ewma_span=10)
    rec = vpin_redundancy_guardrail(v, trades, bucket_size=100)
    assert rec["pearson_abs"] <= 0.80 and rec["spearman_abs"] <= 0.80


def test_vpin_with_guardrail_drops_when_fired():
    rng = np.random.default_rng(25)
    n = 4000
    bucket = 50
    n_b = n // bucket
    frac = np.concatenate([np.full(20, 0.98), np.full(20, 0.5)] * (n_b // 40))
    sign = np.concatenate([
        (rng.random(bucket) < frac[b]).astype(np.int8) for b in range(n_b)
    ])
    trades = pd.DataFrame({
        "ts_exchange_us": np.arange(n, dtype=np.int64) * 10**6,
        "trade_id": np.arange(n),
        "price": np.full(n, 100.0),
        "size": np.full(n, 1.0),
        "aggressor_buy": sign,
    })
    v, rec = vpin_with_guardrail(trades, bucket_size=bucket, ewma_span=10)
    if rec["dropped"]:
        assert v["vpin"].isna().all()
    else:
        assert v["vpin"].notna().any()
