"""Open-source verification of the two public-math pillars (Task 1).

Pillar A - OFI: the exact event-contribution formula extracted from the
arXiv LaTeX source of Cont, Kukanov & Stoikov, "The Price Impact of Order
Book Events" (arXiv:1011.6402v3, Sec. 2.1), verified literally:

    e_n = I{P^B_n >= P^B_{n-1}} q^B_n - I{P^B_n <= P^B_{n-1}} q^B_{n-1}
          - I{P^A_n <= P^A_{n-1}} q^A_n + I{P^A_n >= P^A_{n-1}} q^A_{n-1}

The literal loop below is the paper formula transcribed with no algebraic
shortcut; `top_of_book_ofi` (src/features.py) must reproduce it exactly on
randomized synthetic books. NOTE: this verification FOUND AND FIXED two
discrepancies in the previous implementation (ask-side branches sign-flipped;
same-price queue changes dropped). The formula is authoritative, not the code.

Pillar B - Hawkes: the repo's 2D exponential-kernel MLE (src/features.py)
cross-verified against the `tick` library (X-Data initiative, v0.8.0.2) on
exact simulations with known ground truth. CONVENTION BRIDGE: the repo
uses the amplitude convention phi_mn(t) = alpha_mn exp(-beta t) with
branching matrix G = alpha / beta; tick uses phi_mn(t) = G_mn beta
exp(-beta t), i.e. its `adjacency` parameter IS G. All comparisons below
convert through G. Checks:
  B1. log-likelihood exactness: the repo's O(N) recursion vs an independent
      O(N^2) brute-force oracle, on tick-simulated data (exact ground truth);
  B2. branching-ratio recovery: repo fit vs tick's HawkesExpKern fit on
      tick-simulated 2D data, both against the planted spectral radius rho(G);
  B3. 1D Filimonov-Sornette branching ratio: the cheatsheet's fit_hawkes
      vs tick's HawkesExpKern on tick-simulated 1D data.

Environment note: tick's Base metaclass requires `numpydoc` (its attribute
registry is built from docstrings); without it every tick learner raises
AttributeError on __init__. tick 0.8.0.2's ModelHawkesExpKernLogLik.loss
was probed on handcrafted Poisson data and does not expose an interpretable
absolute log-likelihood, so B1 uses the brute-force oracle instead.

Writes paper/research/math_verification.json and prints the verdict.
tick is an optional dependency: if unavailable, Pillar B is reported as
NOT RUN and the script exits nonzero (the verification is not optional).
"""

import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "src")
from features import fit_hawkes, fit_hawkes2, hawkes_loglik, top_of_book_ofi  # noqa: E402


def cheatsheet_1d_hawkes():
    """Execute the 1D Hawkes code from docs/math_cheatsheet.md verbatim.

    The cheatsheet is the documented library-as-code; verifying it means
    running THE CODE THAT IS WRITTEN THERE, not a transcription.
    """
    import re
    with open("docs/math_cheatsheet.md") as f:
        md = f.read()
    blocks = re.findall(r"```python\n(.*?)```", md, re.DOTALL)
    ns = {"np": np}
    for b in blocks:
        if "_hawkes_ll" in b or "def fit_hawkes" in b:
            exec(b, ns)
    return ns["fit_hawkes"]

REPORT_PATH = "paper/research/math_verification.json"


def ofi_reference_literal(pb, qb, pa, qa):
    """The paper formula, transcribed literally (one event at a time).

    pb, qb, pa, qa: (T,) best bid/ask price and size after each event.
    Returns e: (T,) with e[0] = 0 (no previous observation exists).
    """
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


def synthetic_book(rng, n=2000):
    """Randomized top-of-book sequence exercising every branch of e_n."""
    tick = 0.1
    pb = 100.0 + tick * np.cumsum(rng.integers(-2, 3, n))
    pa = pb + tick * rng.integers(1, 4, n)
    qb = rng.uniform(0, 10, n)
    qa = rng.uniform(0, 10, n)
    ts = np.sort(rng.integers(0, 10**9, n)).astype("int64")
    return pd.DataFrame({
        "ts_exchange_us": ts,
        "update_id": np.arange(n),
        "bid_price": pb,
        "bid_qty": qb,
        "ask_price": pa,
        "ask_qty": qa,
    })


def verify_ofi(n_books=25, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    worst = 0.0
    for b in range(n_books):
        book = synthetic_book(rng, n)
        got = top_of_book_ofi(book)["ofi"].to_numpy()
        want = ofi_reference_literal(
            book["bid_price"].to_numpy(), book["bid_qty"].to_numpy(),
            book["ask_price"].to_numpy(), book["ask_qty"].to_numpy())
        worst = max(worst, float(np.max(np.abs(got - want))))
    return {"max_abs_diff_over_books": worst,
            "n_books": n_books, "n_events_per_book": n,
            "pass": bool(worst < 1e-9)}


def _merge_2d(timestamps):
    t, y = [], []
    for i, ts in enumerate(timestamps):
        t.extend(np.asarray(ts, dtype=float))
        y.extend([i] * len(ts))
    t = np.array(t)
    y = np.array(y, dtype=int)
    o = np.argsort(t, kind="stable")
    return t[o], y[o]


def hawkes_loglik_brute(times, types, T, mu, alpha, beta):
    """Independent O(N^2) oracle: the log-likelihood written directly from
    the intensity definition, no recursion, no shared code with the repo."""
    n, d = len(times), mu.shape[0]
    ll = 0.0
    for k in range(n):
        exc = sum(alpha[types[k], types[i]] * np.exp(-beta * (times[k] - times[i]))
                  for i in range(k))
        lam = mu[types[k]] + exc
        if lam <= 0:
            return -np.inf
        ll += np.log(lam)
    ll -= mu.sum() * T
    for m in range(d):
        for j in range(d):
            tj = times[types == j]
            if len(tj):
                ll -= (alpha[m, j] / beta) * (1.0 - np.exp(-beta * (T - tj))).sum()
    return ll


def verify_hawkes_loglik(seed=1, n_paths=10):
    """B1: repo recursive log-likelihood vs the independent O(N^2) oracle.

    The comparison is run on tick-simulated 2D data (exact ground-truth
    generation) plus randomized parameter draws. NOTE: tick 0.8.0.2's
    ModelHawkesExpKernLogLik.loss does not expose an interpretable absolute
    log-likelihood (probed on handcrafted Poisson data: loss = 0 where the
    documented formula gives -loglik = mu*T), so the sharp likelihood check
    is made against this independent brute-force derivation instead; tick
    enters the verification through its simulator and, in B2/B3, its
    HawkesExpKern estimator.
    """
    from tick.hawkes import SimuHawkesExpKernels
    rng = np.random.default_rng(seed)
    diffs = []
    for p in range(n_paths):
        mu = rng.uniform(0.2, 1.0, 2)
        alpha = rng.uniform(0.1, 0.6, (2, 2))
        beta = rng.uniform(1.0, 4.0)
        sim = SimuHawkesExpKernels(adjacency=alpha / beta, baseline=mu,
                                   decays=beta, end_time=500.0,
                                   seed=int(rng.integers(1e6)))
        sim.simulate()
        t, y = _merge_2d(sim.timestamps)
        ll_repo = hawkes_loglik(t, y, 500.0, mu, alpha, beta)
        ll_brute = hawkes_loglik_brute(t, y, 500.0, mu, alpha, beta)
        diffs.append(abs(ll_repo - ll_brute) / max(abs(ll_brute), 1.0))
    return {"max_rel_diff_vs_brute_oracle": float(max(diffs)),
            "n_paths": n_paths, "pass": bool(max(diffs) < 1e-9)}


def verify_hawkes_branching_2d(seed=2, n_paths=10):
    """B2: branching-ratio recovery, repo MLE vs tick MLE, vs planted rho.

    tick's simulator takes the branching matrix G directly as `adjacency`
    (kernel = G * beta * exp(-beta t)), so the planted spectral radius is
    rho(G) with no conversion on the tick side; the repo fit is converted
    through G_hat = alpha_hat / beta.
    """
    from tick.hawkes import HawkesExpKern, SimuHawkesExpKernels
    rng = np.random.default_rng(seed)
    out = []
    for p in range(n_paths):
        mu = rng.uniform(0.3, 1.0, 2)
        G = rng.uniform(0.05, 0.3, (2, 2))
        beta = rng.uniform(1.5, 3.0)
        planted = float(np.max(np.abs(np.linalg.eigvals(G))))
        sim = SimuHawkesExpKernels(adjacency=G, baseline=mu, decays=beta,
                                   end_time=3000.0, seed=int(rng.integers(1e6)))
        sim.simulate()
        t, y = _merge_2d(sim.timestamps)
        t_us = (t * 1e6).astype("int64")
        fit = fit_hawkes(t_us, y, beta=beta)
        rho_repo = fit["branching_ratio"]
        learner = HawkesExpKern(beta, penalty="none", max_iter=1000)
        learner.fit(sim.timestamps)
        rho_tick = float(np.max(np.abs(np.linalg.eigvals(learner.adjacency))))
        out.append({"planted": planted, "repo": rho_repo, "tick": rho_tick})
    return {"runs": out,
            "max_abs_err_repo": float(max(abs(r["repo"] - r["planted"]) for r in out)),
            "max_abs_err_tick": float(max(abs(r["tick"] - r["planted"]) for r in out)),
            "max_abs_repo_vs_tick": float(max(abs(r["repo"] - r["tick"]) for r in out)),
            "pass": bool(max(abs(r["repo"] - r["planted"]) for r in out) < 0.15
                         and max(abs(r["tick"] - r["planted"]) for r in out) < 0.15
                         and max(abs(r["repo"] - r["tick"]) for r in out) < 0.15)}


def verify_hawkes_1d(seed=3, n_paths=10):
    """B3: 1D branching ratio, cheatsheet fit_hawkes vs tick MLE.

    tick's `adjacency` is the branching ratio itself (kernel = G beta
    exp(-beta t)), so the 1D planted n_c goes in directly.
    """
    from tick.hawkes import HawkesExpKern, SimuHawkesExpKernels
    rng = np.random.default_rng(seed)
    out = []
    for p in range(n_paths):
        mu = rng.uniform(0.3, 1.0)
        n_c = rng.uniform(0.3, 0.7)
        beta = rng.uniform(1.5, 3.0)
        sim = SimuHawkesExpKernels(adjacency=np.array([[n_c]]),
                                  baseline=np.array([mu]), decays=beta,
                                  end_time=4000.0,
                                  seed=int(rng.integers(1e6)))
        sim.simulate()
        t = np.sort(np.asarray(sim.timestamps[0], dtype=float))
        theta, br_cheat = _FIT_HAWKES_1D(t)
        learner = HawkesExpKern(beta, penalty="none", max_iter=500)
        learner.fit(sim.timestamps)
        nc_tick = float(learner.adjacency[0, 0])
        out.append({"planted": n_c, "cheatsheet": float(br_cheat),
                    "tick": nc_tick})
    return {"runs": out,
            "max_abs_err_cheatsheet": float(max(abs(r["cheatsheet"] - r["planted"]) for r in out)),
            "max_abs_err_tick": float(max(abs(r["tick"] - r["planted"]) for r in out)),
            "pass": bool(max(abs(r["cheatsheet"] - r["planted"]) for r in out) < 0.1
                         and max(abs(r["tick"] - r["planted"]) for r in out) < 0.1)}


def main():
    global _FIT_HAWKES_1D
    _FIT_HAWKES_1D = cheatsheet_1d_hawkes()
    report = {"ofi": verify_ofi()}
    try:
        import tick  # noqa: F401
        report["hawkes_loglik_vs_tick"] = verify_hawkes_loglik()
        report["hawkes_branching_2d_vs_tick"] = verify_hawkes_branching_2d()
        report["hawkes_1d_vs_tick"] = verify_hawkes_1d()
        tick_status = "verified"
    except ImportError as e:
        tick_status = f"NOT RUN ({e})"
    report["tick_status"] = tick_status
    ok = all(v.get("pass", False) for k, v in report.items() if isinstance(v, dict))
    report["verdict"] = "PASS" if ok and tick_status == "verified" else "FAIL"
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({k: (v if not isinstance(v, dict) else
                          {kk: vv for kk, vv in v.items() if kk != "runs"})
                      for k, v in report.items()}, indent=2))
    print(f"\nVERDICT: {report['verdict']}  (full report: {REPORT_PATH})")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
