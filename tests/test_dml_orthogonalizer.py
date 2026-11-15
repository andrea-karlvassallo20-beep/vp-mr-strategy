"""Unit tests for src/dml_orthogonalizer.py (cross-fitted DML2).

Synthetic world: D is a NOISY NONLINEAR function of the volatility
confounder W plus (optionally) a tiny true directional signal. The DML2
orthogonalizer must recover theta_hat without false positives when the
true theta = 0, and the pre-declared kill asserts must fire exactly as
declared.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dml_orthogonalizer import (
    KillLineError,
    _newey_west_hac_se,
    dml2_partial_effect,
    directional_accuracy,
    run_dml2_with_kill_lines,
    shuffle_trade_signs_placebo,
)

H_US = 60_000_000  # 60s label horizon
EMB = 30_000_000


def _synthetic(n=6000, theta_true=0.0, seed=1, signal_scale=1.0):
    """W = [sigma_H, log_spread, range_width, diurnal cos, diurnal sin]
    with a strong diurnal cycle (the 58x arrival swing surrogate).
    D = nonlinear(W) + theta_true*latent + noise.
    Y = nonlinear(W) + theta_true*latent + logit noise (binary outcome).
    """
    rng = np.random.default_rng(seed)
    t = np.sort(rng.uniform(0, n * 30_000, n)).astype(np.int64)
    hour = (t // 3_600_000_000) % 24
    diurnal = 1.0 + 0.9 * np.sin(2 * np.pi * hour / 24)
    sigma = 0.01 * diurnal * rng.lognormal(0, 0.2, n)
    spread = np.exp(-4.0 + 0.5 * np.log(diurnal) + rng.normal(0, 0.1, n))
    width = sigma * rng.uniform(50, 150, n)
    W = np.column_stack([
        sigma, np.log(spread), width,
        np.cos(2 * np.pi * hour / 24), np.sin(2 * np.pi * hour / 24),
    ])
    # latent directional factor, independent of W
    z = rng.normal(0, 1, n)
    # nonlinear confounder map: both Y and D load on it
    g_w = (2.0 * sigma / 0.01) ** 1.5 - 3.0 * np.log(spread) \
        + 0.05 * width + 0.5 * np.sin(4 * np.pi * hour / 24)
    D = g_w + theta_true * signal_scale * z + rng.normal(0, 0.5, n)
    lin = 0.3 * g_w + theta_true * signal_scale * z + rng.normal(0, 1.0, n)
    Y = (lin > np.median(lin)).astype(float)  # binary directional outcome
    return Y, D, W, t


def test_dml2_recovers_nonzero_theta():
    """With a true orthogonal signal in D, the DML2 point estimate must be
    finite with a healthy t-stat, and the placebo must stay quiet."""
    Y, D, W, t = _synthetic(theta_true=0.30, seed=1, signal_scale=2.0)
    res = dml2_partial_effect(Y, D, W, t, H_US, EMB, n_folds=5,
                              nuisance="gradient_boosting")
    assert np.isfinite(res["theta_hat"])
    assert abs(res["t_stat"]) > 1.5  # the signal is present in the estimate
    # theta_hat must be POSITIVE (the injected signal is positive)
    assert res["theta_hat"] > 0
    pl = shuffle_trade_signs_placebo(Y, D, W, t, H_US, EMB, n_folds=5,
                                     n_placebo=3, seed=0)
    assert pl["placebo_abs_t_max"] < 2.0


def test_dml2_no_false_positive_when_theta_zero():
    """TRUE THETA = 0: D is pure nonlinear(W) + noise. The orthogonalized
    t-stat must NOT reach the 2.5 kill threshold - no false positive."""
    tstats = []
    for seed in (2, 3, 4, 5):
        Y, D, W, t = _synthetic(theta_true=0.0, seed=seed)
        res = dml2_partial_effect(Y, D, W, t, H_US, EMB, n_folds=5)
        assert np.isfinite(res["theta_hat"])
        tstats.append(abs(res["t_stat"]))
    # across independent null worlds, none should clear the kill threshold
    assert max(tstats) < 2.5, f"false positive: t-stats {tstats}"


def test_kill_line_1_fires_on_null():
    """run_dml2_with_kill_lines on theta_true = 0 must raise KillLineError
    with the kill-line-1 message."""
    Y, D, W, t = _synthetic(theta_true=0.0, seed=7)
    with pytest.raises(KillLineError, match="KILL LINE 1"):
        run_dml2_with_kill_lines(Y, D, W, t, H_US, EMB, n_folds=5,
                                 n_placebo=2)


def test_kill_line_2_fires_when_placebo_finds_structure():
    """Sabotage: feed a placebo threshold of 0.0 so any placebo draw fires
    kill line 2 - proves the placebo wiring raises."""
    Y, D, W, t = _synthetic(theta_true=0.30, seed=1, signal_scale=3.0)
    with pytest.raises(KillLineError, match="KILL LINE 2"):
        run_dml2_with_kill_lines(Y, D, W, t, H_US, EMB, n_folds=5,
                                 n_placebo=2, placebo_acc_max=-1.0,
                                 placebo_abs_t_max=-1.0)


def test_survivor_passes_both_kill_lines():
    """Strong true signal: both kill lines hold and the run reports a
    partial effect (explicitly NOT a P(up) claim)."""
    Y, D, W, t = _synthetic(theta_true=0.30, seed=1, signal_scale=4.0)
    res = run_dml2_with_kill_lines(Y, D, W, t, H_US, EMB, n_folds=5,
                                   n_placebo=3)
    assert res["t_stat"] >= 2.5
    assert res["placebo"]["placebo_abs_t_max"] < 2.0
    assert "not a P(up) claim" in res["status"]


def test_hac_se_bartlett_kernel():
    """White-noise scores: HAC SE ~ SE of the mean; an AR(1) series with
    strong positive autocorrelation must yield a LARGER HAC SE."""
    rng = np.random.default_rng(0)
    n = 5000
    white = rng.normal(0, 1, n)
    ar = np.empty(n)
    ar[0] = 0.0
    for i in range(1, n):
        ar[i] = 0.8 * ar[i - 1] + rng.normal(0, 1)
    se_w = _newey_west_hac_se(white, 20)
    se_ar = _newey_west_hac_se(ar, 20)
    naive_ar = ar.std(ddof=1) / np.sqrt(n)
    # AR(1) phi=0.8 inflates the SE of the mean by ~1/(1+phi) ~ 1.8x vs iid
    assert se_ar > 1.5 * naive_ar  # HAC catches what iid SE would miss
    assert 0.5 * se_w < se_ar


def test_directional_accuracy_bounds():
    rng = np.random.default_rng(1)
    z = rng.normal(0, 1, 1000)
    y = rng.normal(0, 1, 1000)
    acc = directional_accuracy(1.0, z, y)
    assert 0.0 <= acc <= 1.0
    # perfect agreement
    assert directional_accuracy(1.0, z, z) == pytest.approx(1.0)
    assert directional_accuracy(-1.0, z, z) == pytest.approx(0.0)


def test_input_validation():
    Y, D, W, t = _synthetic(n=500, theta_true=0.1, seed=9)
    with pytest.raises(ValueError, match="sorted"):
        dml2_partial_effect(Y, D, W, t[::-1].copy(), H_US, EMB)
    with pytest.raises(ValueError, match="length mismatch"):
        dml2_partial_effect(Y[:-1], D, W, t, H_US, EMB)
