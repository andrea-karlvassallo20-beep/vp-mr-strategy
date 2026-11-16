"""Exactness tests for the public-math pillars (Task 1 verification).

The OFI formula is tested against a literal transcription of the arXiv
source formula (Cont, Kukanov, Stoikov, arXiv:1011.6402v3, Sec. 2.1) and
the Hawkes log-likelihood against an independent O(N^2) oracle. These
tests are hermetic: no tick dependency (the tick cross-verification is
src/verify_math_library.py, run out-of-band and archived in
paper/research/math_verification.json).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from features import fit_hawkes, hawkes_loglik, top_of_book_ofi


def _ofi_arxiv_literal(pb, qb, pa, qa):
    """The paper formula transcribed with no algebraic shortcut."""
    n = len(pb)
    e = np.zeros(n)
    for k in range(1, n):
        ek = 0.0
        if pb[k] >= pb[k - 1]:
            ek += qb[k]
        if pb[k] <= pb[k - 1]:
            ek -= qb[k - 1]
        if pa[k] <= pa[k - 1]:
            ek -= qa[k]
        if pa[k] >= pa[k - 1]:
            ek += qa[k - 1]
        e[k] = ek
    return e


def _random_book(rng, n=500):
    tick = 0.1
    pb = 100.0 + tick * np.cumsum(rng.integers(-2, 3, n))
    pa = pb + tick * rng.integers(1, 4, n)
    return pd.DataFrame({
        "ts_exchange_us": np.sort(rng.integers(0, 10**9, n)).astype("int64"),
        "update_id": np.arange(n),
        "bid_price": pb,
        "bid_qty": rng.uniform(0, 10, n),
        "ask_price": pa,
        "ask_qty": rng.uniform(0, 10, n),
    })


def test_ofi_matches_arxiv_source_formula():
    rng = np.random.default_rng(0)
    for _ in range(10):
        book = _random_book(rng)
        got = top_of_book_ofi(book)["ofi"].to_numpy()
        want = _ofi_arxiv_literal(
            book["bid_price"].to_numpy(), book["bid_qty"].to_numpy(),
            book["ask_price"].to_numpy(), book["ask_qty"].to_numpy())
        assert np.max(np.abs(got - want)) < 1e-9


def test_ofi_same_price_branch_contributes_queue_change():
    book = pd.DataFrame({
        "ts_exchange_us": np.arange(3, dtype="int64") * 10**6,
        "update_id": np.arange(3),
        "bid_price": [100.0, 100.0, 100.0],
        "bid_qty": [1.0, 3.0, 2.0],
        "ask_price": [100.2, 100.2, 100.2],
        "ask_qty": [5.0, 5.0, 7.0],
    })
    ofi = top_of_book_ofi(book)["ofi"].to_numpy()
    assert ofi[1] == 2.0   # +d(qB) - d(qA) = +2 - 0
    assert ofi[2] == -3.0  # +d(qB) - d(qA) = -1 - 2


def test_ofi_ask_branches_follow_paper_signs():
    # ask drops: the new ask queue is ADDED SUPPLY -> e gets -q^A_n
    book = pd.DataFrame({
        "ts_exchange_us": np.arange(2, dtype="int64") * 10**6,
        "update_id": np.arange(2),
        "bid_price": [100.0, 100.0],
        "bid_qty": [1.0, 1.0],
        "ask_price": [100.4, 100.2],
        "ask_qty": [4.0, 2.0],
    })
    assert top_of_book_ofi(book)["ofi"].iloc[1] == -2.0
    # ask rises: the old ask queue is withdrawn supply -> e gets +q^A_{n-1}
    book["ask_price"] = [100.2, 100.4]
    assert top_of_book_ofi(book)["ofi"].iloc[1] == 4.0  # +q^A_{n-1} = +4


def _hawkes_ll_brute(t, y, T, mu, alpha, beta):
    n, d = len(t), mu.shape[0]
    ll = 0.0
    for k in range(n):
        exc = sum(alpha[y[k], y[i]] * np.exp(-beta * (t[k] - t[i]))
                  for i in range(k))
        lam = mu[y[k]] + exc
        if lam <= 0:
            return -np.inf
        ll += np.log(lam)
    ll -= mu.sum() * T
    for m in range(d):
        for j in range(d):
            tj = t[y == j]
            if len(tj):
                ll -= (alpha[m, j] / beta) * (1.0 - np.exp(-beta * (T - tj))).sum()
    return ll


def test_hawkes_loglik_matches_brute_oracle():
    rng = np.random.default_rng(7)
    for _ in range(5):
        n = 120
        t = np.sort(rng.uniform(0, 100, n))
        y = rng.integers(0, 2, n)
        mu = rng.uniform(0.2, 1.0, 2)
        alpha = rng.uniform(0.0, 0.4, (2, 2))
        beta = rng.uniform(0.5, 3.0)
        T = 100.0
        got = hawkes_loglik(t, y, T, mu, alpha, beta)
        want = _hawkes_ll_brute(t, y, T, mu, alpha, beta)
        assert abs(got - want) < 1e-9 * max(abs(want), 1.0)


def test_hawkes_loglik_no_phantom_first_event():
    # a SINGLE event: its intensity is mu[y_0] only. A phantom t_0 event
    # in every dimension (the fixed defect) would inflate it by the
    # alpha row sum; the compensator is mu.sum()*T (no excitation yet).
    t = np.array([2.0])
    y = np.array([0])
    mu = np.array([0.5, 0.7])
    alpha = np.array([[0.9, 0.8], [0.6, 0.9]])
    beta = 1.0
    T = 10.0
    got = hawkes_loglik(t, y, T, mu, alpha, beta)
    # excitation compensator: the t_0 event excites both dimensions over
    # [t_0, T] whether or not offspring were observed
    comp_exc = (alpha[0, 0] + alpha[1, 0]) / beta * (1.0 - np.exp(-beta * (T - t[0])))
    want = np.log(mu[0]) - mu.sum() * T - comp_exc
    assert abs(got - want) < 1e-9


def _simulate_hawkes(mu, alpha, beta, T, rng):
    d = len(mu)
    t, y = [], []
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


def test_fit_hawkes_branching_is_spectral_radius_of_G():
    """branching_ratio must be rho(alpha/beta), NOT rho(alpha).

    The amplitude convention (kernel alpha*exp(-beta t)) makes the
    branching matrix G = alpha / beta; reporting rho(alpha) overstates
    the branching ratio by the fixed decay beta.
    """
    rng = np.random.default_rng(11)
    mu = np.array([0.2, 0.2])
    alpha = np.array([[0.8, 0.1], [0.1, 0.8]])
    beta = 2.0
    t, y = _simulate_hawkes(mu, alpha, beta, 600.0, rng)
    fit = fit_hawkes(t * 1e6, y, beta=beta)
    planted = float(np.max(np.abs(np.linalg.eigvals(alpha / beta))))
    assert abs(fit["branching_ratio"] - planted) < 0.15
    # and it must NOT be the amplitude spectral radius (0.9)
    assert abs(fit["branching_ratio"] - 0.9) > 0.2
