"""Backtest-overfitting statistics: Deflated Sharpe Ratio and
Probability of Backtest Overfitting (CSCV).

Implements the Bailey & Lopez de Prado selection-bias corrections
that the project's dual-split robustness gate approximates
homegrown. The edge-seeker (59 candidates) and AVFI grid (84
candidates) run every night; a best-of-N search inflates the
observed Sharpe, and these statistics deflate it honestly:

  PSR  Probabilistic Sharpe Ratio - probability the true Sharpe
       exceeds a benchmark, corrected for skewness and kurtosis
  DSR  Deflated Sharpe Ratio - PSR against the Sharpe you would
       EXPECT from the best of N zero-skill trials
  PBO  Probability of Backtest Overfitting (CSCV) - how often the
       best in-sample config lands in the bottom half out-of-sample

References:
  Bailey & Lopez de Prado (2014), The Deflated Sharpe Ratio.
  Bailey, Borwein, Lopez de Prado & Zhu (2016), The Probability of
  Backtest Overfitting.

numpy only - no new dependencies, AST-sandbox clean.
"""
import math

import numpy as np

GAMMA = 0.5772156649015329  # Euler-Mascheroni


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_ppf(p: float) -> float:
    """Inverse normal CDF (Acklam's rational approximation)."""
    p = min(max(p, 1e-12), 1.0 - 1e-12)
    a = [-3.969683028665376e+01, 2.209460984245205e+02,
         -2.759285104469687e+02, 1.383577518672690e+02,
         -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02,
         -1.556989798598866e+02, 6.680131188771972e+01,
         -1.328068155288572e+01, 2.506628277459239e+00]
    c = [-7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549796535014203e+00,
         4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01,
         2.445134137142996e+00, 3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3])
                 * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q
                 + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3])
                  * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q
                  + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r
             + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r
             + b[2]) * r + b[3]) * r + b[4]) * r + b[5])


def sharpe_stats(returns) -> dict:
    """Sharpe plus the moments PSR needs (all from the same sample)."""
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    n = len(r)
    if n < 3:
        return {"n": n, "sr": 0.0, "skew": 0.0, "kurt": 3.0}
    mu, sd = r.mean(), r.std()
    sr = mu / sd * math.sqrt(252.0) if sd > 0 else 0.0
    z = (r - mu) / sd if sd > 0 else r - mu
    skew = float(np.mean(z ** 3))
    kurt = float(np.mean(z ** 4))
    return {"n": n, "sr": sr, "skew": skew, "kurt": kurt}


def probabilistic_sharpe(returns, sr_benchmark: float) -> float:
    """PSR: probability the true Sharpe exceeds sr_benchmark,
    corrected for skewness and kurtosis (per-bar Sharpe units are
    converted internally)."""
    s = sharpe_stats(returns)
    n = s["n"]
    if n < 3:
        return 0.0
    per_bar = s["sr"] / math.sqrt(252.0)
    bench = sr_benchmark / math.sqrt(252.0)
    denom = 1.0 - s["skew"] * per_bar + \
        (s["kurt"] - 1.0) / 4.0 * per_bar ** 2
    if denom <= 0:
        return 0.0
    z = (per_bar - bench) * math.sqrt(n - 1) / math.sqrt(denom)
    return _norm_cdf(z)


def expected_max_sharpe(trial_sharpes) -> float:
    """E[max SR] of N zero-skill trials given the variance of the
    trial Sharpes (the expected luck of the search)."""
    v = np.asarray(trial_sharpes, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) < 2:
        return 0.0
    n = len(v)
    var = float(v.var())
    if var <= 0:
        return 0.0
    sd = math.sqrt(var)
    return sd * ((1.0 - GAMMA) * _norm_ppf(1.0 - 1.0 / n)
                 + GAMMA * _norm_ppf(1.0 - 1.0 / (n * math.e)))


def deflated_sharpe(best_returns, trial_sharpes) -> dict:
    """DSR: PSR of the best trial against the Sharpe expected from
    the best of N zero-skill trials. The honest question: after
    trying N configurations, is the winner still better than pure
    search luck?"""
    s = sharpe_stats(best_returns)
    benchmark = expected_max_sharpe(trial_sharpes)
    dsr = probabilistic_sharpe(best_returns, benchmark)
    return {"sharpe": round(s["sr"], 3),
            "n_trials": len(trial_sharpes),
            "expected_max_sharpe_zero_skill": round(benchmark, 3),
            "dsr": round(dsr, 4),
            "passes_95": bool(dsr >= 0.95)}


def pbo_cscv(returns_matrix, n_blocks: int = 16) -> dict:
    """Probability of Backtest Overfitting via Combinatorial
    Symmetric Cross-Validation (Bailey et al. 2016). The returns
    matrix is T periods x N configs; it is cut into blocks, every
    IS/OOS split is tested, and PBO is the fraction of splits where
    the best in-sample config ranks in the BOTTOM half
    out-of-sample. PBO > 0.5 means the selection process is worse
    than a coin flip."""
    m = np.asarray(returns_matrix, dtype=float)
    if m.ndim != 2 or m.shape[1] < 2 or m.shape[0] < n_blocks * 2:
        return {"pbo": None, "splits": 0}
    T, N = m.shape
    blocks = [m[i * T // n_blocks:(i + 1) * T // n_blocks]
              for i in range(n_blocks)]
    losses = 0
    splits = 0
    from itertools import combinations
    for is_idx in combinations(range(n_blocks), n_blocks // 2):
        oos_idx = tuple(i for i in range(n_blocks)
                        if i not in is_idx)
        is_r = np.vstack([blocks[i] for i in is_idx])
        oos_r = np.vstack([blocks[i] for i in oos_idx])
        is_rank = np.argsort(np.argsort(is_r.mean(axis=0)))
        oos_rank = np.argsort(np.argsort(oos_r.mean(axis=0)))
        best_is = int(np.argmax(is_rank))
        # relative OOS rank of the IS winner, in [0, 1]
        # (0 = worst OOS). A LOSS is the IS winner landing in the
        # BOTTOM half out-of-sample.
        rel = oos_rank[best_is] / (N - 1)
        if rel < 0.5:
            losses += 1
        splits += 1
        if splits >= 512:  # cap for runtime on wide grids
            break
    pbo = losses / splits if splits else None
    return {"pbo": round(pbo, 4) if pbo is not None else None,
            "splits": splits}
