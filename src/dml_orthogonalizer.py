"""Cross-fitted Double/Debiased Machine Learning (DML2) orthogonalization
for Layer 2 microstructure directional effects, per Chernozhukov et al.
(2018). Isolates the partial effect of a candidate order-flow feature D on
the binary trade-touch directional triple-barrier outcome Y, net of the
NONLINEAR confounder matrix W (trailing realized volatility sigma_H,
log-spread, rolling range width, 24h Fourier diurnal harmonics).

WHY. A raw regression of Y on D mixes the flow effect with volatility,
spread, and session-clock confounding - the same tautology family that
killed daily C1 (conditioning on realized volatility alone collapsed the
compression hazard ratio to [0.713, 1.092]). DML2 removes the first-stage
nonlinear dependence of both Y and D on W via purged cross-fitted nuisance
learners, so theta_hat measures only the orthogonalized residual
co-movement.

EPISTEMIC CONTRACT. theta_hat is a PARTIAL EFFECT, not a directional
edge claim. The 0.505 [0.497, 0.513] price-only boundary on P(up) remains
binding; nothing here claims WHICH WAY. Kill asserts are pre-declared and
raise KillLineError - a kill is a recorded death, never a tuning prompt.

Estimator (DML2, pooled):
    Y_tilde = Y - E_hat[Y | W]      (cross-fitted, purged folds)
    D_tilde = D - E_hat[D | W]      (cross-fitted, purged folds)
    theta_hat = sum(D_tilde * Y_tilde) / sum(D_tilde^2)
    SE = HAC (Newey-West) on the moment scores D_tilde * (Y_tilde - theta*D_tilde)

Placebo (pre-declared): trade-sign shuffle - D is recomputed from
sign-shuffled trade signs (or permuted, when D is supplied precomputed),
preserving W and timestamps, then the IDENTICAL DML2 estimator runs. The
placebo must not reach directional accuracy >= 0.52 nor |t| >= 2.0.
"""

import numpy as np
import pandas as pd

from event_clock import purged_cpcv_splits


class KillLineError(AssertionError):
    """Pre-declared kill line fired. The claim is dead; do not tune."""


DEFAULT_NUISANCE = "gradient_boosting"


def _make_nuisance(kind: str):
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.linear_model import RidgeCV

    if kind == "gradient_boosting":
        return lambda: HistGradientBoostingRegressor(
            max_iter=200, learning_rate=0.06, max_depth=3,
            random_state=0, early_stopping=True)
    if kind == "ridge":
        return lambda: RidgeCV(alphas=np.logspace(-3, 3, 13))
    raise ValueError(f"unknown nuisance learner: {kind}")


def _newey_west_hac_se(scores: np.ndarray, max_lag: int) -> float:
    """HAC (Newey-West) standard error of the mean of `scores`, with
    Bartlett-kernel truncation at `max_lag` lags (autocorrelation- and
    heteroskedasticity-consistent)."""
    n = len(scores)
    if n < 3:
        return float("nan")
    s = scores - scores.mean()
    gamma0 = float(s @ s) / n
    vcov = gamma0
    for lag in range(1, min(max_lag, n - 1) + 1):
        w = 1.0 - lag / (max_lag + 1.0)  # Bartlett
        gamma = float(s[lag:] @ s[:-lag]) / n
        vcov += 2.0 * w * gamma
    vcov = max(vcov, 0.0)
    return float(np.sqrt(vcov / n))


def _validate(Y, D, W, row_ts):
    Y = np.asarray(Y, dtype=float)
    D = np.asarray(D, dtype=float)
    W = np.atleast_2d(np.asarray(W, dtype=float))
    row_ts = np.asarray(row_ts, dtype=np.int64)
    n = len(Y)
    if not (len(D) == n and W.shape[0] == n and len(row_ts) == n):
        raise ValueError("Y, D, W, row_ts length mismatch")
    if np.any(np.diff(row_ts) < 0):
        raise ValueError("row_ts must be sorted")
    if not np.isfinite(Y).all() or not np.isfinite(D).all():
        raise ValueError("Y and D must be finite")
    if not np.isfinite(W).all():
        raise ValueError("W must be finite")
    return Y, D, W, row_ts


def dml2_partial_effect(Y, D, W, row_ts, label_horizon_us: int,
                        embargo_us: int = 0, n_folds: int = 5,
                        nuisance: str = DEFAULT_NUISANCE,
                        hac_max_lag: int = 20,
                        return_scores: bool = False):
    """Purged cross-fitted DML2 partial effect of D on Y, net of W.

    Folds come from src/event_clock.py::purged_cpcv_splits on the decision
    row timestamps, so every nuisance fit is label-horizon purged and
    embargoed - no forward-looking label information leaks into the
    orthogonalization.

    Returns a dict with theta_hat, HAC SE, t-stat, per-fold records, and
    the pooled residuals. Raises nothing here - kill asserts live in
    `run_dml2_with_kill_lines`.
    """
    Y, D, W, row_ts = _validate(Y, D, W, row_ts)
    n = len(Y)
    make = _make_nuisance(nuisance)
    Y_tilde = np.full(n, np.nan)
    D_tilde = np.full(n, np.nan)
    fold_records = []
    for split in purged_cpcv_splits(row_ts, n_groups=n_folds,
                                    label_horizon_us=label_horizon_us,
                                    embargo_us=embargo_us,
                                    n_test_groups=1):
        tr, te = split["train_idx"], split["test_idx"]
        if len(tr) < 10 or len(te) == 0:
            continue
        m_y = make().fit(W[tr], Y[tr])
        m_d = make().fit(W[tr], D[tr])
        Y_tilde[te] = Y[te] - m_y.predict(W[te])
        D_tilde[te] = D[te] - m_d.predict(W[te])
        fold_records.append({
            "test_groups": split["test_groups"],
            "n_train": int(len(tr)), "n_test": int(len(te)),
            "purged": int(split["purged"]),
        })
    m = np.isfinite(Y_tilde) & np.isfinite(D_tilde)
    if m.sum() < 20:
        raise ValueError("too few cross-fitted rows for DML2")
    Y_t, D_t = Y_tilde[m], D_tilde[m]
    denom = float(D_t @ D_t)
    if denom <= 0:
        raise ValueError("degenerate D_tilde (D fully explained by W)")
    theta = float(D_t @ Y_t) / denom
    scores = D_t * (Y_t - theta * D_t)
    # HAC SE of theta: var(theta) = NW_var(mean score) / mean(D_tilde^2)^2
    se_mean = _newey_west_hac_se(scores, hac_max_lag)
    se_theta = se_mean / (denom / len(D_t))
    out = {
        "theta_hat": theta,
        "hac_se": float(se_theta),
        "t_stat": float(theta / se_theta) if se_theta > 0 else float("nan"),
        "n_used": int(m.sum()),
        "n_folds_used": len(fold_records),
        "folds": fold_records,
        "Y_tilde": Y_t,
        "D_tilde": D_t,
        "nuisance": nuisance,
    }
    if not return_scores:
        for k in ("Y_tilde", "D_tilde"):
            out[k] = None
    else:
        out["scores"] = scores
    return out


def directional_accuracy(theta_hat: float, D_tilde: np.ndarray,
                         Y_tilde: np.ndarray) -> float:
    """Pooled out-of-fold directional agreement of the orthogonalized
    signal: fraction of cross-fitted rows where sign(theta * D_tilde)
    matches sign(Y_tilde). Descriptive diagnostic for the placebo kill
    line; this is NOT a P(up) claim."""
    z = theta_hat * np.asarray(D_tilde, dtype=float)
    y = np.asarray(Y_tilde, dtype=float)
    if len(z) == 0:
        return float("nan")
    return float(np.mean((z > 0) == (y > 0)))


def shuffle_trade_signs_placebo(Y, D, W, row_ts, label_horizon_us,
                                embargo_us: int = 0, n_folds: int = 5,
                                nuisance: str = DEFAULT_NUISANCE,
                                n_placebo: int = 5, seed: int = 0,
                                hac_max_lag: int = 20) -> dict:
    """Trade-sign shuffle placebo: D is sign-shuffled (permutation of the
    D series, destroying the row-to-flow alignment while preserving its
    marginal distribution, W, and timestamps), then the IDENTICAL DML2
    estimator runs. Pre-declared kill line: no placebo draw may reach
    directional accuracy >= 0.52 or |t| >= 2.0."""
    rng = np.random.default_rng(seed)
    Y = np.asarray(Y, dtype=float)
    D = np.asarray(D, dtype=float)
    accs, ts_ = [], []
    for _ in range(n_placebo):
        D_perm = rng.permutation(D)
        res = dml2_partial_effect(Y, D_perm, W, row_ts,
                                  label_horizon_us, embargo_us,
                                  n_folds, nuisance, hac_max_lag,
                                  return_scores=True)
        acc = directional_accuracy(res["theta_hat"], res["D_tilde"],
                                   res["Y_tilde"]) \
            if res["D_tilde"] is not None else float("nan")
        accs.append(acc)
        ts_.append(abs(res["t_stat"]))
    return {
        "placebo_accuracy_max": float(np.nanmax(accs)) if accs else float("nan"),
        "placebo_abs_t_max": float(np.nanmax(ts_)) if ts_ else float("nan"),
        "n_placebo": len(accs),
    }


def run_dml2_with_kill_lines(Y, D, W, row_ts, label_horizon_us,
                             embargo_us: int = 0, n_folds: int = 5,
                             nuisance: str = DEFAULT_NUISANCE,
                             t_stat_min: float = 2.5,
                             placebo_acc_max: float = 0.52,
                             placebo_abs_t_max: float = 2.0,
                             n_placebo: int = 5, seed: int = 0,
                             hac_max_lag: int = 20) -> dict:
    """DML2 partial effect with PRE-DECLARED kill asserts.

    KILL LINES (declared before testing, raised as KillLineError):
      1. Partial-effect t-statistic < 2.5 (weak/no orthogonalized effect).
      2. Trade-sign shuffle placebo reaching directional accuracy >= 0.52
         or |t| >= 2.0 (the estimator finds structure in shuffled flow).

    A kill is final for the (Y, D, W) specification: it names the dead
    mechanism, it is never a tuning prompt.
    """
    res = dml2_partial_effect(Y, D, W, row_ts, label_horizon_us,
                              embargo_us, n_folds, nuisance, hac_max_lag,
                              return_scores=True)
    acc = directional_accuracy(res["theta_hat"], res["D_tilde"],
                               res["Y_tilde"])
    if not np.isfinite(res["t_stat"]) or res["t_stat"] < t_stat_min:
        raise KillLineError(
            f"KILL LINE 1: partial-effect t-stat {res['t_stat']:.3f} < "
            f"{t_stat_min} - no orthogonalized directional effect of D on Y "
            "net of the nonlinear confounders"
        )
    pl = shuffle_trade_signs_placebo(Y, D, W, row_ts, label_horizon_us,
                                     embargo_us, n_folds, nuisance,
                                     n_placebo, seed, hac_max_lag)
    if (pl["placebo_accuracy_max"] >= placebo_acc_max
            or pl["placebo_abs_t_max"] >= placebo_abs_t_max):
        raise KillLineError(
            f"KILL LINE 2: trade-sign shuffle placebo reached accuracy "
            f"{pl['placebo_accuracy_max']:.3f} / |t| "
            f"{pl['placebo_abs_t_max']:.3f} - the estimator finds "
            "structure in shuffled flow"
        )
    res["directional_accuracy"] = acc
    res["placebo"] = pl
    res["status"] = "SURVIVES (partial effect only, not a P(up) claim)"
    return res
