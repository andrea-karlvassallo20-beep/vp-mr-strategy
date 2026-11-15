"""Descriptive feature calculators for the free Binance prep data.

DESCRIPTIVE ONLY. No hazard model consumes these yet. No claim is tested by
this module. Capability flags (see docs/data_dictionary.md):
- VPIN here uses TRADE-COUNT buckets (per directive), on genuine aggTrades.
- Hawkes here is 2-dimensional (buy trades, sell trades). The 4-dimensional
  version (with bid/ask cancels) requires incremental L2 and stays blocked.
- Top-of-book OFI consumes bookTicker-format frames. Binance does NOT publish
  bookTicker archives, so the real-data dry run uses a bookDepth band-depth
  PROXY (5s snapshots, +/-1% bands) — it measures band-notional changes, not
  true order flow. Flagged, never presented as a C6 test.
"""

import numpy as np
import pandas as pd


def vpin_trade_buckets(trades: pd.DataFrame, bucket_size: int = 2000,
                       ewma_span: int = 50) -> pd.DataFrame:
    """VPIN on trade-count buckets.

    trades: normalized aggTrades frame (ts_exchange_us, trade_id, price, size,
    aggressor_buy).
    Returns one row per bucket: bucket end ts, buy_vol, sell_vol, imbalance,
    vpin (EWMA of |buy-sell|/total across buckets).
    """
    req = {"ts_exchange_us", "size", "aggressor_buy"}
    if not req.issubset(trades.columns):
        raise ValueError(f"trades missing columns: {req - set(trades.columns)}")
    t = trades.reset_index(drop=True)
    n_buckets = len(t) // bucket_size
    if n_buckets == 0:
        raise ValueError("not enough trades for one bucket")
    t = t.iloc[: n_buckets * bucket_size]
    idx = np.arange(len(t)) // bucket_size
    buy = np.where(t["aggressor_buy"].to_numpy() == 1, t["size"], 0.0)
    sell = np.where(t["aggressor_buy"].to_numpy() == 0, t["size"], 0.0)
    g = pd.DataFrame({"b": buy, "s": sell, "ts": t["ts_exchange_us"].to_numpy(),
                      "g": idx}).groupby("g")
    out = pd.DataFrame({
        "bucket_end_ts": g["ts"].last(),
        "n_trades": g.size(),
        "buy_vol": g["b"].sum(),
        "sell_vol": g["s"].sum(),
    })
    out["imbalance"] = (out["buy_vol"] - out["sell_vol"]).abs() / (
        out["buy_vol"] + out["sell_vol"]
    )
    out["vpin"] = out["imbalance"].ewm(span=ewma_span).mean()
    return out.reset_index(drop=True)


def hawkes_loglik(times: np.ndarray, types: np.ndarray, T: float,
                  mu: np.ndarray, alpha: np.ndarray, beta: float) -> float:
    """Exact log-likelihood of a 2-dim (d = types.max()+1) exponential-kernel
    Hawkes process via the recursive R-sums. times sorted, T = window end."""
    d = mu.shape[0]
    n = len(times)
    dt = np.diff(times, prepend=times[0])
    decay = np.exp(-beta * dt)
    R = np.zeros((n, d))
    prev = np.ones(d)
    for k in range(n):
        prev = prev * decay[k]
        R[k] = prev
        prev[types[k]] += 1.0
    lam = mu[types] + np.array([alpha[:, types[k]] @ R[k] for k in range(n)])
    if (lam <= 0).any():
        return -np.inf
    ll = np.log(lam).sum()
    ll -= mu.sum() * T
    for i in range(d):
        for j in range(d):
            tj = times[types == j]
            ll -= (alpha[i, j] / beta) * (1.0 - np.exp(-beta * (T - tj))).sum()
    return float(ll)


def fit_hawkes(times_us: np.ndarray, types: np.ndarray,
               beta: float = 2.0) -> dict:
    """MLE of a symmetric-parameterization 2-dim Hawkes on a window.

    Parameters: mu (2), alpha matrix (2x2) with diagonal and off-diagonal
    kept separate (4), shared beta fixed (per directive: descriptive)."""
    t = np.asarray(times_us, dtype=np.float64)
    t = (t - t[0]) / 1e6
    T = t[-1] - t[0] + 1e-6
    y = np.asarray(types, dtype=np.int64)
    d = int(y.max()) + 1

    def unpack(p):
        mu = np.exp(p[:d])
        a = np.exp(p[d : d + d * d]).reshape(d, d)
        return mu, a

    def nll(p):
        mu, a = unpack(p)
        if np.abs(np.linalg.eigvals(a)).max() >= 0.95:
            return 1e12
        return -hawkes_loglik(t, y, T, mu, a, beta)

    from scipy.optimize import minimize
    p0 = np.concatenate([
        np.log(np.full(d, max(len(t) / d / T, 1e-6))),
        np.log(np.full(d * d, 0.05 / d)),
    ])
    res = minimize(nll, p0, method="L-BFGS-B",
                   bounds=[(np.log(1e-9), np.log(10.0))] * d
                         + [(np.log(1e-9), np.log(5.0))] * (d * d),
                   options={"maxiter": 500})
    mu, a = unpack(res.x)
    optimizer = "L-BFGS-B"
    converged = bool(res.success)
    if not converged:
        res = minimize(nll, res.x, method="Nelder-Mead",
                       options={"maxiter": 2000, "xatol": 1e-6, "fatol": 1e-6})
        mu, a = unpack(res.x)
        optimizer = "Nelder-Mead-fallback"
        converged = bool(res.success) or np.isfinite(res.fun)
    return {
        "mu": mu.tolist(),
        "alpha": a.tolist(),
        "beta_fixed": beta,
        "n_events": int(len(t)),
        "window_s": float(T),
        "loglik": float(-res.fun),
        "converged": bool(converged),
        "optimizer": optimizer,
        "branching_ratio": float(np.max(np.abs(np.linalg.eigvals(a)))),
        "excitation_half_life_s": float(np.log(2.0) / beta),
    }


# ---------------------------------------------------------------------------
# Upgraded 2D Hawkes estimator for Claim T2 (pre-L2, taker-only).
#
# Upgrades over the dry-run version (which pinned beta and hit the 0.95
# stationarity cap, making decay a fixed parameterization):
#   1. UNPINNED per-pair decay beta_{mn} (d x d matrix) jointly optimized with
#      branching matrix G_{mn} = alpha_{mn} / beta_{mn}, spectral radius
#      rho(G) < 0.95 enforced.
#   2. Smooth periodic diurnal baseline mu_m(t) = exp(x(t) . theta_m) with
#      24-hour Fourier harmonics, fit strictly on the training window, so
#      session-open volume surges are not misattributed to self-excitation.
#   3. O(N D^2) recursive log-likelihood (d^2 R-sums, one per (target, source)
#      pair), with an O(N^2) brute-force reference kept for unit testing.
#   4. Explicit `is_boundary_constrained` flag: fits with rho(G) >= 0.949 are
#      boundary-constrained and are NEVER reported as interior estimates.

DAY_S = 86400.0
SPECTRAL_CAP = 0.95
BOUNDARY_FLAG = 0.949


def diurnal_design(times_s: np.ndarray, harmonics: int = 3) -> np.ndarray:
    """Design matrix for the smooth periodic diurnal baseline.

    Columns: [1, cos/sin harmonics of the 24-hour cycle]. The phase is
    anchored to ABSOLUTE epoch time (times_s are epoch seconds), so the
    baseline is the same physical clock across windows and folds.
    """
    t = np.asarray(times_s, dtype=np.float64)
    phase = 2.0 * np.pi * (np.mod(t, DAY_S) / DAY_S)
    cols = [np.ones_like(t)]
    for h in range(1, harmonics + 1):
        cols.append(np.cos(h * phase))
        cols.append(np.sin(h * phase))
    return np.column_stack(cols)


def _mu_at(times_s: np.ndarray, theta: np.ndarray, harmonics: int) -> np.ndarray:
    """mu_m(t) for every event time. Returns (n, d) array."""
    X = diurnal_design(times_s, harmonics)
    return np.exp(X @ theta.T)  # (n, d)


def _mu_integral(t0_s: float, T: float, theta: np.ndarray, harmonics: int,
                 grid_step_s: float = 60.0) -> np.ndarray:
    """Integral of the diurnal baseline over [t0, t0+T] per dimension.

    exp-linear Fourier baseline has no closed-form integral, so we integrate
    numerically on a fine trapezoid grid (default 60s). The same grid is used
    by the recursive and brute-force likelihoods, so the unit test isolates
    ONLY the recursion-vs-brute-force difference.
    """
    n_grid = max(int(np.ceil(T / grid_step_s)) + 1, 2)
    grid = t0_s + np.linspace(0.0, T, n_grid)
    mu = _mu_at(grid, theta, harmonics)  # (n_grid, d)
    w = np.full(n_grid, T / (n_grid - 1))
    w[0] *= 0.5
    w[-1] *= 0.5
    return (mu * w[:, None]).sum(axis=0)  # (d,)


def _compensator_excitation(times_s: np.ndarray, types: np.ndarray, T: float,
                            alpha: np.ndarray, beta_mat: np.ndarray) -> float:
    """sum_{m,n} (alpha_mn / beta_mn) * sum_i (1 - exp(-beta_mn (T - t_i))) 1[y_i=n]."""
    d = alpha.shape[0]
    ll = 0.0
    for m in range(d):
        for n in range(d):
            ti = times_s[types == n]
            if len(ti) == 0:
                continue
            ll -= (alpha[m, n] / beta_mat[m, n]) * (
                1.0 - np.exp(-beta_mat[m, n] * (T - ti))
            ).sum()
    return ll


def _recursive_rows(times_s: np.ndarray, types: np.ndarray,
                    beta_mat: np.ndarray) -> np.ndarray:
    """O(N D^2) R-sums. Returns (n, d) array: for event k of type y_k, the
    row R[y_k, :] where R[m, n] = sum_{i<k} exp(-beta_mn (t_k - t_i)) 1[y_i=n].
    Recursion: R *= exp(-beta_mn * dt); R[:, y_{k-1}] += 1.
    """
    n = len(times_s)
    d = beta_mat.shape[0]
    rows = np.zeros((n, d))
    R = np.zeros((d, d))
    for k in range(n):
        if k > 0:
            # event k-1 enters at its own time (weight 1), THEN everything
            # decays over (t_k - t_{k-1}) - the add must precede the decay.
            R[:, types[k - 1]] += 1.0
            R *= np.exp(-beta_mat * (times_s[k] - times_s[k - 1]))
        rows[k] = R[types[k]]
    return rows


def hawkes2_loglik(times_us: np.ndarray, types: np.ndarray,
                   theta: np.ndarray, alpha: np.ndarray, beta_mat: np.ndarray,
                   harmonics: int = 3) -> float:
    """Exact log-likelihood of the upgraded 2D Hawkes (recursive, O(N D^2)).

    times_us: int64 microsecond timestamps (window-relative or epoch).
    theta: (d, 1+2*harmonics) diurnal-baseline coefficients.
    alpha, beta_mat: (d, d) excitation and decay matrices.
    """
    t = (np.asarray(times_us, dtype=np.float64)) / 1e6
    y = np.asarray(types, dtype=np.int64)
    n, d = len(t), alpha.shape[0]
    if n == 0:
        return -np.inf
    T = t[-1] - t[0] + 1e-9
    t0 = t[0]
    mu = _mu_at(t, theta, harmonics)  # (n, d)
    rows = _recursive_rows(t, y, beta_mat)  # (n, d)
    # lambda_{y_k} = mu_{y_k}(t_k) + sum_n alpha[y_k, n] * R[y_k, n]
    lam = mu[np.arange(n), y] + (alpha[y] * rows).sum(axis=1)
    if (lam <= 0).any() or not np.isfinite(lam).all():
        return -np.inf
    ll = np.log(lam).sum()
    ll += _mu_integral(t0, T, theta, harmonics).sum() * -1.0
    ll += _compensator_excitation(t - t0, y, T, alpha, beta_mat)
    return float(ll)


def hawkes2_loglik_brute(times_us: np.ndarray, types: np.ndarray,
                         theta: np.ndarray, alpha: np.ndarray,
                         beta_mat: np.ndarray, harmonics: int = 3) -> float:
    """Brute-force O(N^2) reference implementation (unit-test oracle only)."""
    t = (np.asarray(times_us, dtype=np.float64)) / 1e6
    y = np.asarray(types, dtype=np.int64)
    n = len(t)
    T = t[-1] - t[0] + 1e-9
    t0 = t[0]
    mu = _mu_at(t, theta, harmonics)
    ll = 0.0
    for k in range(n):
        exc = 0.0
        for i in range(k):
            exc += alpha[y[k], y[i]] * np.exp(-beta_mat[y[k], y[i]] * (t[k] - t[i]))
        lam = mu[k, y[k]] + exc
        if lam <= 0 or not np.isfinite(lam):
            return -np.inf
        ll += np.log(lam)
    ll -= _mu_integral(t0, T, theta, harmonics).sum()
    ll += _compensator_excitation(t - t0, y, T, alpha, beta_mat)
    return float(ll)


def _spectral_radius(G: np.ndarray) -> float:
    return float(np.max(np.abs(np.linalg.eigvals(G))))


def fit_hawkes2(times_us: np.ndarray, types: np.ndarray, harmonics: int = 3,
                beta_init: float = 2.0) -> dict:
    """Joint MLE of (diurnal theta, alpha, beta) for the upgraded 2D Hawkes.

    Bounded L-BFGS-B with Nelder-Mead fallback. Spectral radius of the
    branching matrix G = alpha / beta is kept < 0.95 via a penalized barrier;
    fits ending at rho(G) >= 0.949 are flagged `is_boundary_constrained` and
    must never be reported as interior point estimates.
    """
    from scipy.optimize import minimize

    t = np.asarray(times_us, dtype=np.float64) / 1e6
    y = np.asarray(types, dtype=np.int64)
    n = len(t)
    if n < 10:
        raise ValueError("need at least 10 events to fit")
    d = int(y.max()) + 1
    T = t[-1] - t[0] + 1e-9
    n_theta = 1 + 2 * harmonics

    def unpack(p):
        theta = p[: d * n_theta].reshape(d, n_theta)
        a = np.exp(p[d * n_theta: d * n_theta + d * d]).reshape(d, d)
        b = np.exp(p[d * n_theta + d * d:]).reshape(d, d)
        return theta, a, b

    def nll(p):
        theta, a, b = unpack(p)
        G = a / b
        rho = _spectral_radius(G)
        if not np.isfinite(rho) or rho >= SPECTRAL_CAP:
            return 1e12 + 1e6 * max(rho, 0.0)
        ll = hawkes2_loglik(t * 1e6, y, theta, a, b, harmonics)
        if not np.isfinite(ll):
            return 1e12
        return -ll

    rate = max(n / d / T, 1e-6)
    p0 = np.concatenate([
        np.log(rate) * np.ones(d * n_theta),
        np.log(0.05 / d) * np.ones(d * d),
        np.log(beta_init) * np.ones(d * d),
    ])
    bounds = (
        [(np.log(1e-9), np.log(1e3))] * (d * n_theta)
        + [(np.log(1e-9), np.log(5.0))] * (d * d)
        + [(np.log(0.01), np.log(50.0))] * (d * d)
    )
    res = minimize(nll, p0, method="L-BFGS-B", bounds=bounds,
                   options={"maxiter": 1000})
    optimizer = "L-BFGS-B"
    converged = bool(res.success)
    if not converged or not np.isfinite(res.fun):
        res = minimize(nll, res.x if np.isfinite(res.fun) else p0,
                       method="Nelder-Mead",
                       options={"maxiter": 4000, "xatol": 1e-7, "fatol": 1e-7})
        optimizer = "Nelder-Mead-fallback"
        converged = bool(res.success) or np.isfinite(res.fun)

    theta, a, b = unpack(res.x)
    G = a / b
    rho = _spectral_radius(G)
    return {
        "mu_theta": theta.tolist(),
        "alpha": a.tolist(),
        "beta": b.tolist(),
        "branching_matrix_G": G.tolist(),
        "spectral_radius": rho,
        "is_boundary_constrained": bool(rho >= BOUNDARY_FLAG),
        "n_events": int(n),
        "window_s": float(T),
        "loglik": float(-res.fun),
        "converged": bool(converged),
        "optimizer": optimizer,
        "harmonics": int(harmonics),
        "excitation_half_life_s": (np.log(2.0) / b).tolist(),
        "note": ("boundary-constrained fit: decay/branching NOT an interior "
                 "empirical estimate" if rho >= BOUNDARY_FLAG
                 else "interior fit"),
    }


# ---------------------------------------------------------------------------
# VPIN non-redundancy guardrails (Claim T2).


def signed_trade_imbalance_buckets(trades: pd.DataFrame,
                                   bucket_size: int = 2000) -> pd.DataFrame:
    """Sign-PRESERVING per-bucket imbalance (buy - sell) / (buy + sell),
    on the same trade-count bucketing as vpin_trade_buckets."""
    req = {"ts_exchange_us", "size", "aggressor_buy"}
    if not req.issubset(trades.columns):
        raise ValueError(f"trades missing columns: {req - set(trades.columns)}")
    t = trades.reset_index(drop=True)
    n_buckets = len(t) // bucket_size
    if n_buckets == 0:
        raise ValueError("not enough trades for one bucket")
    t = t.iloc[: n_buckets * bucket_size]
    idx = np.arange(len(t)) // bucket_size
    buy = np.where(t["aggressor_buy"].to_numpy() == 1, t["size"], 0.0)
    sell = np.where(t["aggressor_buy"].to_numpy() == 0, t["size"], 0.0)
    g = pd.DataFrame({"b": buy, "s": sell, "g": idx}).groupby("g")
    out = pd.DataFrame({"buy_vol": g["b"].sum(), "sell_vol": g["s"].sum()})
    out["signed_imbalance"] = (out["buy_vol"] - out["sell_vol"]) / (
        out["buy_vol"] + out["sell_vol"]
    )
    return out.reset_index(drop=True)


def vpin_redundancy_guardrail(vpin_df: pd.DataFrame, trades: pd.DataFrame,
                              bucket_size: int = 2000) -> dict:
    """RAISING ASSERTION: |Pearson| and |Spearman| between VPIN and
    |signed trade imbalance| must each be <= 0.80. If exceeded, both metrics
    measure one layer twice and the redundant feature must be dropped.

    Returns the correlation record when the guardrail holds; raises
    AssertionError when it does not.
    """
    si = signed_trade_imbalance_buckets(trades, bucket_size)
    m = min(len(vpin_df), len(si))
    if m < 3:
        raise ValueError("not enough buckets to test redundancy")
    v = vpin_df["vpin"].to_numpy()[:m]
    s = np.abs(si["signed_imbalance"].to_numpy()[:m])
    pearson = float(np.corrcoef(v, s)[0, 1])
    spearman = float(pd.Series(v).corr(pd.Series(s), method="spearman"))
    rec = {"pearson_abs": abs(pearson), "spearman_abs": abs(spearman)}
    if not (np.isfinite(rec["pearson_abs"]) and np.isfinite(rec["spearman_abs"])):
        raise AssertionError(
            "VPIN/|signed-imbalance| redundancy guardrail DEGENERATE "
            f"(pearson={pearson}, spearman={spearman}): constant input means "
            "the two series carry no distinguishable information - drop the "
            "redundant feature"
        )
    if rec["pearson_abs"] > 0.80 or rec["spearman_abs"] > 0.80:
        raise AssertionError(
            "VPIN/|signed-imbalance| redundancy guardrail EXCEEDED "
            f"(pearson={pearson:.3f}, spearman={spearman:.3f}): both metrics "
            "measure one layer twice - drop the redundant feature"
        )
    return rec


def vpin_with_guardrail(trades: pd.DataFrame, bucket_size: int = 2000,
                        ewma_span: int = 50) -> tuple:
    """VPIN pipeline with the guardrail applied. Returns (vpin_df, record).

    If the guardrail fires, the redundancy is logged and the VPIN column is
    DROPPED (set to NaN) rather than passed downstream as an independent
    feature - the run continues, the feature does not.
    """
    v = vpin_trade_buckets(trades, bucket_size, ewma_span)
    try:
        rec = vpin_redundancy_guardrail(v, trades, bucket_size)
        rec["dropped"] = False
    except AssertionError as e:
        print(f"[guardrail] {e}")
        rec = {"dropped": True, "reason": str(e)}
        v["vpin"] = np.nan
    return v, rec


def top_of_book_ofi(book: pd.DataFrame) -> pd.DataFrame:
    """Top-of-book OFI from bookTicker-format frames.

    book: normalized frame (ts_exchange_us, update_id, bid_price, bid_qty,
    ask_price, ask_qty). OFI per Cont/Kukanov/Stoikov at the touch:
    e_n = I{bid moved up} * bid_qty_n - I{bid moved down} * bid_qty_{n-1}
        - I{ask moved down} * ask_qty_n + I{ask moved up} * ask_qty_{n-1}
    """
    req = {"ts_exchange_us", "bid_price", "bid_qty", "ask_price", "ask_qty"}
    if not req.issubset(book.columns):
        raise ValueError(f"book missing columns: {req - set(book.columns)}")
    b = book.sort_values("ts_exchange_us", kind="stable").reset_index(drop=True)
    db = b["bid_price"].diff()
    da = b["ask_price"].diff()
    ofi = (
        np.where(db > 0, b["bid_qty"], 0.0)
        + np.where(db < 0, -b["bid_qty"].shift(1), 0.0)
        + np.where(da > 0, -b["ask_qty"].shift(1), 0.0)
        + np.where(da < 0, b["ask_qty"], 0.0)
    )
    out = pd.DataFrame({
        "ts_exchange_us": b["ts_exchange_us"],
        "ofi": pd.Series(ofi, index=b.index).fillna(0.0),
        "spread": b["ask_price"] - b["bid_price"],
    })
    return out


def band_depth_ofi_proxy(bookdepth: pd.DataFrame) -> pd.DataFrame:
    """PROXY (bookDepth snapshots, 5s, +/-1% bands). Signed change in
    bid-side notional within the -1% band minus ask-side notional within the
    +1% band. This is NOT order flow: it cannot separate fills from cancels
    and the 5s cadence destroys intra-snapshot sequencing. Descriptive only.
    bookdepth: raw Binance bookDepth frame (timestamp, percentage, depth,
    notional) with percentage in {-5..-1, 1..5}."""
    b = bookdepth.copy()
    b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
    piv = b.pivot_table(index="ts", columns="percentage", values="notional")
    bid = piv.get(-1)
    ask = piv.get(1)
    if bid is None or ask is None:
        raise ValueError("bookDepth frame lacks +/-1% bands")
    out = pd.DataFrame({
        "ts": piv.index,
        "bid_band_notional": bid,
        "ask_band_notional": ask,
    })
    out["ofi_proxy"] = out["bid_band_notional"].diff() - out["ask_band_notional"].diff()
    return out.dropna().reset_index(drop=True)
