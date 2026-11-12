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
