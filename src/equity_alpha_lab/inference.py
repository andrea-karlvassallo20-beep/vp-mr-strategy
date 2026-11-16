"""Honest inference for factor evaluation: HAC t-stats and Fama-MacBeth.

DESCRIPTIVE INSTRUMENTS. These do not decide anything; they replace the
NAIVE i.i.d. t-stat (which understates uncertainty when IC is serially
correlated, the normal condition for slow-moving factors) with a
Newey-West HAC version, and they implement the Fama-MacBeth
cross-sectional regression with HAC inference on the coefficient series.

Why this module exists: the factor zoo's evaluation.py deliberately ships
a naive t-stat with its limitation stated. Any pre-registered factor
claim must cite THIS module's numbers, not that one. Multiple-testing
control (Bonferroni threshold for the zoo as a whole) is provided so a
k-factor scan cannot silently shop for the best t-stat.

No statsmodels dependency: HAC is implemented directly (Bartlett kernel).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluation import ic_series, _merge


def _nw_lags(n: int) -> int:
    """Newey-West rule-of-thumb lag order: floor(4*(n/100)^(2/9))."""
    return int(np.floor(4.0 * (n / 100.0) ** (2.0 / 9.0)))


def newey_west_tstat(x: pd.Series | np.ndarray, lags: int | None = None) -> dict:
    """HAC (Newey-West, Bartlett kernel) t-stat for the mean of x.

    Returns dict: mean, naive_se, naive_t, nw_se, nw_t, lags, n.
    The naive numbers are included deliberately — the ratio
    naive_se/nw_se is itself a diagnostic (>>1 means the i.i.d. t-stat
    was overstating significance, the classic backtest trap).
    """
    arr = np.asarray(x, dtype="float64")
    arr = arr[~np.isnan(arr)]
    n = len(arr)
    mean = float(arr.mean()) if n else float("nan")
    if n < 3:
        return {"n": n, "mean": mean, "naive_se": float("nan"),
                "naive_t": float("nan"), "nw_se": float("nan"),
                "nw_t": float("nan"), "lags": 0}
    centered = arr - mean
    # long-run variance of the mean: gamma_0 + 2 * sum_w (1 - w/(L+1)) gamma_w
    lags = _nw_lags(n) if lags is None else int(lags)
    gamma = [float(np.dot(centered[w:], centered[:-w]) / n) for w in range(1, lags + 1)]
    lrv = float(np.dot(centered, centered) / n)
    for w, g in enumerate(gamma, start=1):
        lrv += 2.0 * (1.0 - w / (lags + 1.0)) * g
    nw_var_of_mean = lrv / n
    naive_var_of_mean = float(np.var(centered, ddof=1)) / n
    nw_se = float(np.sqrt(max(nw_var_of_mean, 0.0)))
    naive_se = float(np.sqrt(naive_var_of_mean))
    return {
        "n": n,
        "mean": mean,
        "naive_se": naive_se,
        "naive_t": float(mean / naive_se) if naive_se > 0 else float("nan"),
        "nw_se": nw_se,
        "nw_t": float(mean / nw_se) if nw_se > 0 else float("nan"),
        "lags": lags,
    }


def ic_inference(factor: pd.DataFrame, fwd: pd.DataFrame, lags: int | None = None) -> dict:
    """Rank-IC series with HAC inference (the honest version of ic_summary)."""
    ic = ic_series(factor, fwd).dropna()
    out = newey_west_tstat(ic, lags)
    out["ic_ir"] = float(out["mean"] / ic.std(ddof=1)) if len(ic) > 1 else float("nan")
    out["hit_rate"] = float((ic > 0).mean()) if len(ic) else float("nan")
    return out


def fama_macbeth(
    factor: pd.DataFrame,
    fwd: pd.DataFrame,
    controls: list[pd.DataFrame] | None = None,
    lags: int | None = None,
) -> dict:
    """Fama-MacBeth: per-date cross-sectional OLS, then HAC t on coefficients.

    factor: long frame (sid, date, value). controls: optional list of
    long frames in the same format; each is joined on (sid, date) and its
    coefficient is reported alongside the factor's.
    Returns {name: {mean, naive_t, nw_t, nw_se, lags, n_dates}} per regressor.
    """
    m = _merge(factor, fwd).rename(columns={"factor": "__factor__"})
    for i, c in enumerate(controls or []):
        cname = f"control_{i}" if "factor" in c.columns else c["factor"].iloc[0] \
            if "factor" in c.columns else f"control_{i}"
        c2 = c[["sid", "date", "value"]].rename(columns={"value": cname})
        m = m.merge(c2, on=["sid", "date"], how="left")
    m = m.dropna()
    if m.empty:
        return {}
    regressors = ["__factor__"] + [
        col for col in m.columns
        if col not in {"sid", "date", "__factor__", "fwd_ret"}
    ]
    coefs = {r: [] for r in regressors}
    for _, grp in m.groupby("date"):
        X = np.column_stack([np.ones(len(grp))] + [grp[r].to_numpy() for r in regressors])
        y = grp["fwd_ret"].to_numpy()
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        for r, b in zip(regressors, beta[1:]):
            coefs[r].append(b)
    out = {}
    for r in regressors:
        s = pd.Series(coefs[r])
        stats = newey_west_tstat(s, lags)
        stats["n_dates"] = stats.pop("n")
        out[r if r != "__factor__" else "factor"] = stats
    return out


def bonferroni_threshold(alpha: float = 0.05, n_tests: int = 1) -> float:
    """Family-wise alpha for testing n factors at once."""
    if n_tests < 1:
        raise ValueError("n_tests must be >= 1")
    return alpha / n_tests


def bonferroni_t_threshold(alpha: float = 0.05, n_tests: int = 1) -> float:
    """Approximate two-sided |t| threshold under Bonferroni (normal approx)."""
    from scipy.stats import norm
    return float(norm.ppf(1.0 - bonferroni_threshold(alpha, n_tests) / 2.0))
