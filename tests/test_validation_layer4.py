"""Unit and integration tests for src/validation_layer4.py (mock data only)."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from validation_layer4 import (
    compute_effective_n_trials,
    deflated_sharpe_ratio,
    shuffle_trade_signs_placebo,
    screen_panel_pairs,
)


# ------------------------------------------------- effective trial count

def test_effective_n_trials_uncorrelated_equals_nominal():
    rng = np.random.default_rng(0)
    m = rng.normal(0, 1, (50, 500))
    eff = compute_effective_n_trials(m)
    assert eff == pytest.approx(50.0, abs=6.0)


def test_effective_n_trials_collapses_for_redundant_paths():
    rng = np.random.default_rng(1)
    base = rng.normal(0, 1, 1000)
    m = np.vstack([base + 0.01 * rng.normal(0, 1, (20, 1000))])
    eff = compute_effective_n_trials(m)
    assert 1.0 <= eff < 5.0


def test_effective_n_trials_single_trial_is_one():
    assert compute_effective_n_trials(np.random.default_rng(2).normal(0, 1, 100)) == 1.0


# ------------------------------------------------- deflated Sharpe ratio

def test_dsr_refuses_single_path():
    with pytest.raises(ValueError, match="single-path"):
        deflated_sharpe_ratio([1.2], 10.0, 0.0, 0.0)


def test_dsr_output_bounds_and_ci():
    rng = np.random.default_rng(3)
    sharpes = rng.normal(0.3, 0.2, 30)
    out = deflated_sharpe_ratio(sharpes, 25.0, -0.5, 3.0)
    assert 0.0 <= out["dsr_probability"] <= 1.0
    assert 0.0 <= out["ci_lower"] <= out["ci_upper"] <= 1.0
    assert out["n_paths"] == 30
    assert out["effective_n_trials"] == 25.0


def test_dsr_penalizes_more_trials():
    rng = np.random.default_rng(4)
    sharpes = rng.normal(0.4, 0.2, 20)
    low = deflated_sharpe_ratio(sharpes, 2.0, 0.0, 0.0)["dsr_probability"]
    high = deflated_sharpe_ratio(sharpes, 500.0, 0.0, 0.0)["dsr_probability"]
    assert high < low


def test_dsr_zero_sharpe_near_half():
    out = deflated_sharpe_ratio(np.array([0.01, -0.02, 0.0, 0.015, -0.01]), 10.0, 0.0, 0.0)
    assert out["dsr_probability"] < 0.6


# ------------------------------------------------- placebo generator

def _events(n=2000, seed=7):
    rng = np.random.default_rng(seed)
    ts = np.sort(rng.integers(0, 10 ** 10, n)).astype("int64")
    assert n % 2 == 0
    signs = np.zeros(n, dtype="int8")
    signs[: n // 2] = 1
    rng.shuffle(signs)  # balanced: exactly 50% buys
    return pd.DataFrame({
        "ts_exchange_us": ts,
        "trade_price": 100.0 + rng.normal(0, 0.1, n),
        "aggressor_buy": signs,
        "size": rng.uniform(0.1, 5.0, n),
        "book_side": np.where(signs == 1, "bid", "ask"),
        "depth_10bps": rng.uniform(10, 100, n),
    })


def test_placebo_is_book_preserving():
    ev = _events()
    plc = shuffle_trade_signs_placebo(ev, seed=42)
    assert len(plc) == len(ev)
    assert (plc["ts_exchange_us"].to_numpy() == ev["ts_exchange_us"].to_numpy()).all()
    dts = np.diff(np.sort(ev["ts_exchange_us"].to_numpy()))
    assert (np.diff(np.sort(plc["ts_exchange_us"].to_numpy())) == dts).all()
    assert (plc["size"].to_numpy() == ev["size"].to_numpy()).all()
    assert (plc["depth_10bps"].to_numpy() == ev["depth_10bps"].to_numpy()).all()
    assert set(plc["aggressor_buy"]) <= {0, 1}
    assert plc["aggressor_buy"].sum() == ev["aggressor_buy"].sum()
    assert (plc["book_side"] == np.where(plc["aggressor_buy"] == 1, "bid", "ask")).all()
    assert not (plc["aggressor_buy"].to_numpy() == ev["aggressor_buy"].to_numpy()).all()


def test_placebo_seed_reproducible_and_sign_column_required():
    ev = _events()
    assert shuffle_trade_signs_placebo(ev, 11)["aggressor_buy"].equals(
        shuffle_trade_signs_placebo(ev, 11)["aggressor_buy"]
    )
    with pytest.raises(ValueError, match="aggressor"):
        shuffle_trade_signs_placebo(ev.drop(columns=["aggressor_buy"]), 0)


def test_placebo_directional_pipeline_null_result():
    """Integration: dummy directional pipeline on placebo data must show
    OOF Brier skill <= 0 and P(up) inside [0.497, 0.513]."""
    ev = shuffle_trade_signs_placebo(_events(4000, seed=9), seed=13)
    y = ev["aggressor_buy"].to_numpy().astype(float)
    p_up = float(y.mean())
    assert 0.497 <= p_up <= 0.513

    rng = np.random.default_rng(21)
    X = rng.normal(0, 1, (len(ev), 3))
    idx = np.arange(len(ev))
    n_splits = 5
    splits = np.array_split(idx, n_splits)
    brier_model, brier_climo = 0.0, 0.0
    for sp in splits:
        train = np.setdiff1d(idx, sp)
        p_train = y[train].mean()
        brier_model += float(np.mean((p_train - y[sp]) ** 2))
        brier_climo += float(np.mean((0.5 - y[sp]) ** 2))
    brier_model /= n_splits
    brier_climo /= n_splits
    skill = 1.0 - brier_model / brier_climo
    assert skill <= 0.0


# ------------------------------------------------- panel screen

def _pair_df(n=3000, cancel_frac=0.3, depth=50.0, seed=0, ofi_rho=0.2):
    rng = np.random.default_rng(seed)
    kinds = rng.choice(["cancel", "trade", "insert"], n, p=[
        cancel_frac, 0.4, 1 - cancel_frac - 0.4])
    price = 100.0 + rng.normal(0, 0.05, n)
    return pd.DataFrame({
        "ts_exchange_us": np.sort(rng.integers(0, 10 ** 10, n)).astype("int64"),
        "event_type": kinds,
        "side": rng.choice(["bid", "ask"], n),
        "price": price,
        "size": rng.uniform(0.1, 2.0, n),
        "mid": 100.0,
        "depth_10bps": rng.uniform(depth, depth + 10, n),
        "ofi": _ar1(rng, n, ofi_rho),
    })


def _ar1(rng, n, rho):
    x = np.zeros(n)
    x[0] = rng.normal()
    for i in range(1, n):
        x[i] = rho * x[i - 1] + rng.normal()
    return x


def test_screen_excludes_low_cancellation_and_empty_depth():
    panel = {
        "good": _pair_df(seed=0),
        "no_cancels": _pair_df(cancel_frac=0.001, seed=1),
        "empty_depth": _pair_df(depth=0.0, seed=2).assign(depth_10bps=0.0),
    }
    retained, audit = screen_panel_pairs(panel)
    assert set(retained) == {"good"}
    a = audit.set_index("pair")
    assert a.loc["no_cancels", "failure_metric"] == "cancel_frac"
    assert a.loc["empty_depth", "failure_metric"] == "median_depth_10bps"
    assert pd.isna(a.loc["good", "failure_metric"])
    assert 0.25 < a.loc["good", "cancel_frac"] < 0.45
    assert a.loc["good", "median_depth_10bps"] > 0
    assert -1.0 <= a.loc["good", "ofi_lag1_autocorr"] <= 1.0
    assert audit["retained_fraction"].iloc[0] == pytest.approx(1 / 3)
    assert bool(audit["panel_fail_flag"].iloc[0]) is True


def test_screen_retains_all_healthy_panel():
    panel = {"a": _pair_df(seed=3), "b": _pair_df(seed=4)}
    retained, audit = screen_panel_pairs(panel)
    assert set(retained) == {"a", "b"}
    assert not bool(audit["panel_fail_flag"].iloc[0])
    assert audit["retained_fraction"].iloc[0] == pytest.approx(1.0)


def test_screen_ofi_lag1_detects_persistence():
    persistent = _pair_df(ofi_rho=0.9, seed=5)
    noisy = _pair_df(ofi_rho=0.0, seed=6)
    _, audit = screen_panel_pairs({"p": persistent, "n": noisy})
    a = audit.set_index("pair")
    assert a.loc["p", "ofi_lag1_autocorr"] > 0.5
    assert abs(a.loc["n", "ofi_lag1_autocorr"]) < 0.2
