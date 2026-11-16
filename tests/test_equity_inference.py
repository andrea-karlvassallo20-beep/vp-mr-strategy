"""Honest-inference tests: HAC t-stats and Fama-MacBeth on known ground truth.

Three kinds of ground truth:
1. Hand-checkable small examples (exact OLS slopes, exact Bonferroni).
2. Autocorrelated series where the NAIVE t-stat provably overstates
   significance and Newey-West must correct it (the instrument's whole
   reason to exist).
3. The momentum world / null world panels from the factor-zoo tests:
   HAC inference must still find the engineered signal and must still
   stay quiet in noise.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from equity_alpha_lab import (
    bonferroni_t_threshold,
    bonferroni_threshold,
    fama_macbeth,
    forward_returns,
    ic_inference,
    momentum,
    newey_west_tstat,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests"))
from test_equity_factor_zoo import _momentum_world, _null_world, _security_master, _fwd


# ---------------------------------------------------------------- NW basics

def test_nw_matches_naive_on_white_noise():
    rng = np.random.default_rng(3)
    x = pd.Series(rng.normal(0, 1, 500))
    out = newey_west_tstat(x)
    # iid data: HAC and naive standard errors must be close
    assert abs(out["nw_se"] / out["naive_se"] - 1.0) < 0.15


def test_nw_corrects_positive_autocorrelation():
    # AR(1) with rho=0.5: the naive se understates the long-run variance
    # by roughly a factor sqrt((1+rho)/(1-rho)) ~ 1.73
    rng = np.random.default_rng(5)
    n, rho = 2000, 0.5
    e = rng.normal(0, 1, n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + np.sqrt(1 - rho * rho) * e[t]
    out = newey_west_tstat(pd.Series(x))
    # HAC must inflate the se relative to naive
    assert out["nw_se"] > 1.2 * out["naive_se"]
    # and therefore shrink the |t|
    assert abs(out["nw_t"]) < abs(out["naive_t"])
    # the inflation must be in the right neighborhood: theory says
    # lr variance ratio = (1+rho)/(1-rho) = 3 -> se ratio ~ sqrt(3) ~ 1.73
    ratio = out["nw_se"] / out["naive_se"]
    assert 1.3 < ratio < 2.3


def test_nw_tstat_hand_check():
    # tiny fixed series, verify the HAC computation against a direct
    # hand-rolled Bartlett-kernel implementation with lags=1
    x = pd.Series([1.0, 2.0, 0.5, -1.0, 0.25, 3.0, -0.5, 1.5])
    out = newey_west_tstat(x, lags=1)
    a = np.asarray(x, dtype="float64")
    c = a - a.mean()
    n = len(a)
    g0 = np.dot(c, c) / n
    g1 = np.dot(c[1:], c[:-1]) / n
    lrv = g0 + 2.0 * (1.0 - 1.0 / 2.0) * g1
    expected_se = np.sqrt(lrv / n)
    assert out["nw_se"] == pytest.approx(expected_se)
    assert out["nw_t"] == pytest.approx(a.mean() / expected_se)


# ---------------------------------------------------------------- FM

def test_fama_macbeth_hand_check_two_dates():
    # 2 dates x 4 names; the factor is a perfect linear predictor of the
    # forward return on both dates -> slope exactly 1 on each date
    d1, d2 = pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-02")
    factor = pd.DataFrame(
        {
            "sid": [f"S{i}" for i in range(4)] * 2,
            "date": [d1] * 4 + [d2] * 4,
            "value": [0.1, 0.2, 0.3, 0.4] * 2,
        }
    )
    fwd = pd.DataFrame(
        {
            "sid": [f"S{i}" for i in range(4)] * 2,
            "decision_date": [d1] * 4 + [d2] * 4,
            "fwd_ret": [0.1, 0.2, 0.3, 0.4] * 2,
        }
    )
    out = fama_macbeth(factor, fwd)
    assert out["factor"]["mean"] == pytest.approx(1.0, abs=1e-8)
    assert out["factor"]["n_dates"] == 2


def test_fama_macbeth_recovers_momentum_world():
    _, px = _momentum_world()
    fwd = _fwd(px, horizon=5)
    mom = momentum(px, window=252, skip=21)
    out = fama_macbeth(mom, fwd)
    assert out["factor"]["mean"] > 0
    # in the engineered world the HAC t must still clear 2
    assert out["factor"]["nw_t"] > 2.0


def test_fama_macbeth_quiet_in_null_world():
    px = _null_world()
    fwd = _fwd(px, horizon=5)
    mom = momentum(px, window=252, skip=21)
    out = fama_macbeth(mom, fwd)
    assert abs(out["factor"]["mean"]) < 0.05
    assert abs(out["factor"]["nw_t"]) < 2.5


def test_ic_inference_reports_both_t_stats():
    _, px = _momentum_world()
    fwd = _fwd(px, horizon=5)
    out = ic_inference(momentum(px, window=252, skip=21), fwd)
    assert {"naive_t", "nw_t", "nw_se", "lags", "hit_rate", "ic_ir"} <= set(out)
    assert out["nw_t"] > 2.0


# ---------------------------------------------------------------- multiplicity

def test_bonferroni_thresholds():
    assert bonferroni_threshold(0.05, 1) == pytest.approx(0.05)
    assert bonferroni_threshold(0.05, 6) == pytest.approx(0.05 / 6)
    with pytest.raises(ValueError):
        bonferroni_threshold(0.05, 0)
    # t-threshold for the 6-factor zoo must exceed the single-test 1.96
    single = bonferroni_t_threshold(0.05, 1)
    zoo = bonferroni_t_threshold(0.05, 6)
    assert single == pytest.approx(1.96, abs=0.01)
    assert zoo > 2.3
