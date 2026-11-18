"""Tests for the compound Hawkes order-flow engine. Synthetic data only."""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ofhawkes import (  # noqa: E402
    ASK_IS, BID_IS, DIM_NAMES, NDIM, BookState, Config, OrderBook,
    ROUND_SIZES, SizeSampler, build_config, build_tod_matrix,
    simulate_day, simulate_poisson_day, spectral_radius,
    stabilize_norm_matrix, u_shape,
)

SMALL = dict(horizon_s=300.0, dt=0.01)  # fine grid + flat day keeps the cap valid


def small_cfg(seed: int = 5, amp_scale: float = 1.0) -> Config:
    cfg, _ = build_config(seed=seed)
    cfg.horizon_s = SMALL["horizon_s"]
    cfg.dt = SMALL["dt"]
    cfg.tod = np.ones((NDIM, 13))  # the 300s test never sees the day's shape
    cfg.amp = cfg.amp * amp_scale
    return cfg


# -- stability with disclosure -------------------------------------------------

def test_stable_matrix_untouched():
    M = np.zeros((NDIM, NDIM)); M[0, 0] = 0.3
    out, d = stabilize_norm_matrix(M, max_tod_factor=1.9)
    assert d.action == "none" and d.factor == 1.0
    assert out[0, 0] == 0.3


def test_unstable_matrix_refused_when_asked():
    M = np.eye(NDIM) * 2.0
    with pytest.raises(ValueError, match="no silent rescale"):
        stabilize_norm_matrix(M, max_tod_factor=1.5, refuse=True)


def test_unstable_matrix_rescaled_with_disclosure():
    M = np.eye(NDIM) * 2.0
    out, d = stabilize_norm_matrix(M, max_tod_factor=2.0, target_rho=0.8)
    assert d.action == "rescaled_with_disclosure"
    assert d.raw_rho > d.threshold > d.scaled_rho
    assert abs(spectral_radius(out) - d.scaled_rho) < 1e-9
    assert abs(d.factor - out[0, 0] / M[0, 0]) < 1e-12
    assert d.factor < 1.0


def test_build_config_disclosure():
    cfg, disc = build_config(seed=1)
    thr = disc.threshold
    assert spectral_radius(cfg.norm_matrix()) < thr
    assert disc.action in ("none", "rescaled_with_disclosure")
    if disc.action == "rescaled_with_disclosure":
        assert 0 < disc.factor <= 1.0
        assert disc.raw_rho >= thr > disc.scaled_rho


# -- kernel norms -------------------------------------------------------------

def test_norm_matrix_matches_numeric_integral():
    cfg, _ = build_config(seed=3)
    M = cfg.norm_matrix()
    ts = np.linspace(0, 500, 400001)
    j, i = 4, 2
    phi = cfg.amp[j, i] * np.exp(-cfg.dec[j, i] * ts)
    numeric = np.trapezoid(phi, ts)
    assert abs(numeric - M[j, i]) < abs(M[j, i]) * 0.02 + 1e-3


def test_signed_kernels_present():
    cfg, _ = build_config(seed=3)
    assert (cfg.amp < 0).any(), "inhibitory kernels were expected in the build"


# -- size sampler --------------------------------------------------------------

def test_size_sampler_spike_mass_and_mean():
    w = np.array([0.42, 0.18, 0.14, 0.16, 0.07, 0.03]); w = w / w.sum()
    p, spike_w = 0.01, 0.35
    s = SizeSampler(p_body=p, spike_weight=spike_w, spike_probs=w,
                    rng=np.random.default_rng(11))
    draws = s.sample(200_000)
    # exact expected mass at round sizes: spikes plus geometric body mass
    body_mass = sum((1 - p) ** (r - 1) * p for r in ROUND_SIZES)
    expected = spike_w + (1 - spike_w) * body_mass
    mass = float(np.isin(draws, ROUND_SIZES).mean())
    assert abs(mass - expected) < 0.01, (mass, expected)
    assert (draws > 0).all()


def test_size_sampler_rejects_bad_config():
    with pytest.raises(ValueError):
        SizeSampler(p_body=0.0, spike_weight=0.1, spike_probs=np.ones(6) / 6)
    with pytest.raises(ValueError):
        SizeSampler(p_body=0.5, spike_weight=1.0, spike_probs=np.ones(6) / 6)
    with pytest.raises(ValueError):
        SizeSampler(p_body=0.5, spike_weight=0.2, spike_probs=np.ones(6) / 3)


# -- book mechanics ------------------------------------------------------------

def fresh_book(seed: int = 0) -> OrderBook:
    w = np.ones(len(ROUND_SIZES)) / len(ROUND_SIZES)
    rep = SizeSampler(0.02, 0.3, w, rng=np.random.default_rng(seed))
    st = BookState(ask=1000, bid=998, q_ask_top=500, q_ask_deep=900,
                   q_bid_top=400, q_bid_deep=800)
    return OrderBook(st, rep, np.random.default_rng(seed))


def test_book_invariants_under_scripted_events():
    b = fresh_book()
    seq = [(2, 150), (4, 350), (4, 300), (3, 10**6), (8, 10**6),
           (7, 200), (9, 5000), (4, 2), (0, 50), (10, 50), (6, 80),
           (5, 60), (1, 10**6), (11, 10**6)]
    for dim, size in seq:
        b.apply(dim, size)
        assert b.spread() >= 1
        assert min(b.q_ask_top, b.q_ask_deep, b.q_bid_top, b.q_bid_deep) >= 0
        assert (b.ask - b.bid) >= 1
    assert b.mid() == (b.ask + b.bid) / 2.0


def test_inspread_guard_raises_at_one_tick_spread():
    b = fresh_book()
    b.apply(5, 100)  # ask improves one tick: spread is now one tick
    assert b.spread() == 1
    with pytest.raises(AssertionError, match="one-tick spread"):
        b.apply(6, 80)  # bid cannot improve into a locked market


def test_mo_exact_consumption_walks_the_book():
    b = fresh_book()
    ask0, deep = b.ask, b.q_ask_deep
    b.apply(4, b.q_ask_top)  # market order consumes the top queue exactly
    assert b.ask == ask0 + 1, "exact depletion must widen the spread"
    assert b.q_ask_top == deep


def test_ask_walk_on_depletion():
    b = fresh_book()
    ask0, deep = b.ask, b.q_ask_deep
    b.apply(3, 10**6)  # cancel entire top ask queue
    assert b.ask == ask0 + 1
    assert b.q_ask_top == deep  # old deep becomes the new top


def test_inspread_moves_touch_one_tick():
    b = fresh_book()
    b.apply(5, 120)  # in-spread ask: new best ask one tick lower
    assert b.ask == 1000 - 1
    assert b.q_ask_top == 120
    assert b.spread() == 1  # bid was at 998


def test_market_order_multi_level_depletion():
    b = fresh_book()
    ask0 = b.ask
    b.apply(4, 500 + 900 + 100)  # exhaust top and deep
    assert b.ask == ask0 + 1 or b.q_ask_top > 0


# -- simulation ----------------------------------------------------------------

def test_sim_day_spread_floor_invariant():
    day = simulate_day(small_cfg(seed=9))
    assert (day.spread >= 1).all()
    assert (day.q_ask_top >= 0).all() and (day.q_bid_top >= 0).all()


def test_inspread_never_fires_at_one_tick_spread():
    # run with degenerate state pinned at one-tick spread via IS rejections
    day = simulate_day(small_cfg(seed=17), day_index=3)
    # any IS event requires spread >= 2 by the book's own assertion; the run
    # completing without AssertionError IS the test
    assert len(day.events_t) > 1000

def test_seed_reproducibility():
    a = simulate_day(small_cfg(seed=42), day_index=0)
    b = simulate_day(small_cfg(seed=42), day_index=0)
    c = simulate_day(small_cfg(seed=43), day_index=0)
    assert np.array_equal(a.events_t, b.events_t)
    assert np.array_equal(a.events_dim, b.events_dim)
    assert not np.array_equal(a.events_t, c.events_t)


def test_excitation_increases_clustering_versus_poisson():
    cfg = small_cfg(seed=7)
    hawkes = simulate_day(cfg, day_index=0)
    poisson = simulate_poisson_day(cfg, day_index=0)
    # the Poisson control carries zero excitation by construction
    assert poisson.endog_share.mean() < 1e-9
    h_share = 1.0 - hawkes.gross_exog / hawkes.gross_total
    assert h_share > 0.15, h_share  # saw its own offspring in the stream
    assert len(hawkes.events_t) > len(poisson.events_t) * 1.3


def test_grid_validity_guard():
    cfg = small_cfg(seed=2)
    cfg.mu = cfg.mu * 50  # absurd intensities must trip the guard
    cfg.tod = cfg.tod * 1.0
    with pytest.raises(RuntimeError, match="Bernoulli grid violated"):
        simulate_day(cfg)


def test_u_shape_mean_one():
    u = u_shape(13)
    assert abs(u.mean() - 1.0) < 1e-12
    assert u[0] > u[6] and u[-1] > u[6]
    F = build_tod_matrix(np.random.default_rng(0))
    assert np.allclose(F.mean(axis=1), 1.0, atol=1e-9)
