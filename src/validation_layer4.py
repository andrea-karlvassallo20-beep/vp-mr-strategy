"""Layer 4 Validation — DSR, placebo auditing, and panel data-quality screen.

Locked down BEFORE historical L2 arrives, per paper/research/c1_l2_test_spec.md
and the L2 acquisition spec. All machinery is unit-tested on MOCK data only;
nothing here produces a research result until the L2 verification gate passes.

Binding rules:
  1. No single-path Sharpe is ever reportable: deflated_sharpe_ratio refuses
     a one-element CPCV Sharpe distribution.
  2. The multiple-testing correction uses the EFFECTIVE number of trials
     (participation ratio of the correlation eigenvalue spectrum), never the
     nominal trial count.
  3. Placebo trade-sign shuffles are book-preserving: timestamps,
     inter-arrival durations, sizes, and depth profiles are untouched; only
     aggressor signs (and symmetric book side labels, when present) permute.
  4. Panel pairs failing the pre-model data-quality screen are excluded with
     a mandatory audit table naming the exact failure metric per pair.
"""

import numpy as np
import pandas as pd
from scipy import stats

EULER_GAMMA = 0.5772156649015329
MIN_CANCEL_FRACTION = 0.01
DEPTH_BPS = 10.0
MAX_PANEL_EXCLUSION_FRACTION = 0.50


# ------------------------------------------------- effective trial count

def compute_effective_n_trials(trial_returns_matrix) -> float:
    """Effective number of independent trials from the correlation spectrum.

    Parameters
    ----------
    trial_returns_matrix : array-like, shape (n_trials, n_obs)
        Per-trial return paths (one row per configuration/trial evaluated).

    Returns
    -------
    float
        Participation ratio of the eigenvalues of the trial-return
        correlation matrix: (sum lambda)^2 / sum lambda^2. Equals the nominal
        trial count when the paths are uncorrelated, collapses toward 1 as
        the trials become redundant. Always in [1, n_trials].
    """
    m = np.asarray(trial_returns_matrix, dtype=float)
    if m.ndim == 1:
        m = m[None, :]
    if m.shape[0] == 0:
        raise ValueError("empty trial returns matrix")
    m = m[:, ~np.isnan(m).all(axis=0)] if m.size else m
    if m.shape[0] == 1 or m.shape[1] < 2:
        return 1.0
    corr = np.corrcoef(m)
    corr = np.nan_to_num(corr, nan=0.0)
    np.fill_diagonal(corr, 1.0)
    eig = np.linalg.eigvalsh(corr)
    eig = np.clip(eig.real, 0.0, None)
    denom = float(np.sum(eig ** 2))
    if denom <= 0:
        return 1.0
    pr = float(np.sum(eig) ** 2 / denom)
    return float(np.clip(pr, 1.0, float(m.shape[0])))


# ------------------------------------------------- deflated Sharpe ratio

def _expected_max_standard_normal(n_trials: float) -> float:
    """Expected maximum of n_trials standard normals (Bailey & Lopez de Prado)."""
    if n_trials < 2:
        return 0.0
    z1 = stats.norm.ppf(1.0 - 1.0 / n_trials)
    z2 = stats.norm.ppf(1.0 - 1.0 / (n_trials * np.e))
    return float((1.0 - EULER_GAMMA) * z1 + EULER_GAMMA * z2)


def _dsr_probability(sr: float, sr0: float, skewness: float,
                      excess_kurtosis: float) -> float:
    """Deflated Sharpe ratio probability for a single Sharpe observation."""
    denom = 1.0 - skewness * sr + (excess_kurtosis / 4.0) * sr * sr
    denom = max(denom, 1e-12)
    z = (sr - sr0) / np.sqrt(denom)
    return float(stats.norm.cdf(z))


def deflated_sharpe_ratio(oos_cpcv_sharpes, effective_n_trials,
                          skewness, excess_kurtosis):
    """Deflated Sharpe Ratio across the CPCV path distribution.

    Parameters
    ----------
    oos_cpcv_sharpes : array-like
        Out-of-sample Sharpe ratios, one per CPCV path. MUST contain at least
        two paths; a single-path Sharpe is refused (kill line).
    effective_n_trials : float
        Effective number of trials (from compute_effective_n_trials).
    skewness, excess_kurtosis : float
        Skewness and EXCESS kurtosis of the strategy returns.

    Returns
    -------
    dict with keys ``dsr_probability``, ``ci_lower``, ``ci_upper``,
    ``sr_mean``, ``sr_std``, ``effective_n_trials``, ``n_paths``.
    The 95% bounds are the 2.5/97.5 percentiles of the per-path DSR
    probabilities across the CPCV path distribution.
    """
    sharpes = np.asarray(oos_cpcv_sharpes, dtype=float)
    sharpes = sharpes[~np.isnan(sharpes)]
    if sharpes.size < 2:
        raise ValueError(
            "single-path Sharpe reporting refused: DSR requires the CPCV "
            "path distribution (>= 2 OOS paths)"
        )
    if not np.isfinite(effective_n_trials) or effective_n_trials < 1:
        raise ValueError(f"invalid effective_n_trials: {effective_n_trials}")
    sr_mean = float(np.mean(sharpes))
    sr_std = float(np.std(sharpes, ddof=1))
    sr0 = _expected_max_standard_normal(float(effective_n_trials)) * sr_std
    per_path = np.array([
        _dsr_probability(float(s), sr0, float(skewness), float(excess_kurtosis))
        for s in sharpes
    ])
    return {
        "dsr_probability": float(np.mean(per_path)),
        "ci_lower": float(np.percentile(per_path, 2.5)),
        "ci_upper": float(np.percentile(per_path, 97.5)),
        "sr_mean": sr_mean,
        "sr_std": sr_std,
        "sr0_expected_max": float(sr0),
        "effective_n_trials": float(effective_n_trials),
        "n_paths": int(sharpes.size),
    }


# ------------------------------------------------- placebo generator

def shuffle_trade_signs_placebo(events_df: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Book-preserving placebo: permute aggressor signs, keep everything else.

    events_df must carry an aggressor sign column (``aggressor_buy`` in
    {0,1} or {True,False}, or ``aggressor_side`` in {'bid','ask'}). Optional
    symmetric book-side column ``book_side`` (or ``side``) is permuted with
    the SAME permutation so quote labels stay symmetric under the shuffle.

    Preserved exactly: timestamps, inter-arrival durations, trade sizes,
    and every depth column. Only the sign column (and its book-side mirror)
    is permuted.
    """
    df = events_df.copy()
    cols = {str(c).lower(): c for c in df.columns}
    sign_col = None
    sign_kind = None
    for cand in ("aggressor_buy", "aggressor_side", "aggressor_sign"):
        if cand in cols:
            sign_col, sign_kind = cols[cand], cand
            break
    if sign_col is None:
        raise ValueError(
            f"events_df lacks an aggressor sign column (aggressor_buy/"
            f"aggressor_side/aggressor_sign); columns={list(df.columns)}"
        )
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    if sign_kind == "aggressor_buy":
        df[sign_col] = df[sign_col].to_numpy()[perm]
        if "book_side" in cols:
            df[cols["book_side"]] = df[cols["book_side"]].to_numpy()[perm]
    elif sign_kind == "aggressor_sign":
        vals = df[sign_col].to_numpy()
        df[sign_col] = vals[perm]
        if "book_side" in cols:
            df[cols["book_side"]] = df[cols["book_side"]].to_numpy()[perm]
    else:  # aggressor_side in {'bid','ask'}
        df[sign_col] = df[sign_col].to_numpy()[perm]
        if "book_side" in cols:
            df[cols["book_side"]] = df[cols["book_side"]].to_numpy()[perm]
    return df.reset_index(drop=True)


# ------------------------------------------------- panel data-quality screen

def _pair_metrics(df: pd.DataFrame) -> dict:
    cols = {str(c).lower(): c for c in df.columns}
    event_col = cols.get("event_type") or cols.get("operation")
    side_col = cols.get("side") or cols.get("aggressor_side")
    price_col = cols.get("price")
    size_col = cols.get("size") or cols.get("amount")
    mid_col = cols.get("mid")

    ev = (
        df[event_col].astype(str).str.lower().to_numpy()
        if event_col is not None
        else None
    )
    if ev is not None:
        is_cancel = np.isin(ev, ["cancel", "delete", "cancellation"])
        is_trade = np.isin(ev, ["trade", "trades", "fill", "t"])
        is_book_update = is_cancel | np.isin(ev, ["insert", "update", "i", "u"])
    else:
        is_cancel = np.zeros(len(df), dtype=bool)
        is_trade = np.ones(len(df), dtype=bool)
        is_book_update = np.zeros(len(df), dtype=bool)
    n_book_updates = int(is_book_update.sum())
    n_trades = int(is_trade.sum())
    n_cancels = int(is_cancel.sum())
    denom = n_cancels + n_trades
    cancel_frac = n_cancels / denom if denom else 0.0
    trade_frac = n_trades / denom if denom else 0.0

    depth_col = cols.get("depth_10bps")
    if depth_col is not None:
        depth = pd.to_numeric(df[depth_col], errors="coerce").to_numpy()
    elif price_col is not None and mid_col is not None and size_col is not None:
        price = pd.to_numeric(df[price_col], errors="coerce").to_numpy()
        mid = pd.to_numeric(df[mid_col], errors="coerce").to_numpy()
        size = pd.to_numeric(df[size_col], errors="coerce").to_numpy()
        within = np.abs(price - mid) <= (DEPTH_BPS / 10_000.0) * mid
        depth = np.where(within, np.nan_to_num(size), 0.0)
    else:
        depth = None
    median_depth = float(np.median(depth)) if depth is not None else np.nan

    ofi_col = cols.get("ofi")
    if ofi_col is not None:
        ofi = pd.to_numeric(df[ofi_col], errors="coerce").to_numpy()
    elif size_col is not None and side_col is not None:
        size = pd.to_numeric(df[size_col], errors="coerce").to_numpy()
        side = df[side_col].astype(str).str.lower().to_numpy()
        sign = np.where(side == "bid", 1.0, -1.0)
        ofi = sign * size
    else:
        ofi = None
    if ofi is not None and len(ofi) >= 2:
        ofi = ofi[~np.isnan(ofi)]
        if ofi.std() > 0 and len(ofi) >= 2:
            ofi_lag1 = float(np.corrcoef(ofi[:-1], ofi[1:])[0, 1])
        else:
            ofi_lag1 = np.nan
    else:
        ofi_lag1 = np.nan

    return {
        "n_book_updates": n_book_updates,
        "n_cancels": n_cancels,
        "n_trades": n_trades,
        "cancel_frac": cancel_frac,
        "trade_frac": trade_frac,
        "median_depth_10bps": median_depth,
        "ofi_lag1_autocorr": ofi_lag1,
    }


def screen_panel_pairs(panel):
    """Pre-model panel data-quality screen.

    Parameters
    ----------
    panel : mapping pair-name -> DataFrame of L2 event rows with (at least)
        an event/operation column distinguishing cancellations from trades
        (``event_type`` or ``operation``), and either a ``depth_10bps``
        column or (``price``, ``mid``, ``size``) to derive it, plus ``side``
        (or ``ofi``) for order-flow imbalance.

    Exclusion rules (automatic):
      - cancellation fraction < 1% of cancellation+trade activity
      - median 10-bps depth is empty (<= 0 or missing)

    Returns
    -------
    (retained: dict, audit: DataFrame). The audit table lists EVERY pair with
    its exact metrics, an ``excluded`` flag, ``failure_metric`` naming the
    failing metric, plus ``retained_fraction`` and ``panel_fail_flag``
    (True when > 50% of the panel is excluded).
    """
    names = list(panel.keys())
    rows = []
    retained = {}
    for name in names:
        m = _pair_metrics(panel[name])
        failure = None
        if m["cancel_frac"] < MIN_CANCEL_FRACTION:
            failure = "cancel_frac"
        elif not np.isfinite(m["median_depth_10bps"]) or m["median_depth_10bps"] <= 0:
            failure = "median_depth_10bps"
        m["pair"] = name
        m["excluded"] = failure is not None
        m["failure_metric"] = failure
        rows.append(m)
        if failure is None:
            retained[name] = panel[name]
    audit = pd.DataFrame(rows)[[
        "pair", "n_book_updates", "n_cancels", "n_trades", "cancel_frac",
        "trade_frac", "median_depth_10bps", "ofi_lag1_autocorr",
        "excluded", "failure_metric",
    ]]
    n = len(names)
    retained_fraction = (len(retained) / n) if n else 0.0
    audit["retained_fraction"] = retained_fraction
    audit["panel_fail_flag"] = bool(n and retained_fraction <= MAX_PANEL_EXCLUSION_FRACTION)
    return retained, audit
