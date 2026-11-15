"""Cox diagnostics for the C1-L2 harness: Schoenfeld residual PH audit,
automatic hour-of-day/regime stratification, powered-fold enforcement, and
adversarial null simulators.

Purpose: prove, on SYNTHETIC null markets only, that every pre-declared kill
line in src/c1_l2_test.py actually fires BEFORE any real Tardis L2 data is
ingested. Nothing in this module is a research result.

Counting-process convention: spells are (start, stop] intervals with an
`event` indicator and per-interval covariate values, so time-varying
covariates are first-class. Ties are handled à la Breslow. Only numpy /
pandas / scipy are required.
"""

import numpy as np
import pandas as pd
from scipy import stats as sps

START_COL = "start"
STOP_COL = "stop"
EVENT_COL = "event"
HOUR_COL = "hod"        # UTC hour-of-day stratum, s in {0..23}
REGIME_COL = "regime"   # Layer 1 regime stratum

PH_ALPHA = 0.05         # trigger automatic stratification below this
PH_HARD_ALPHA = 0.01    # unresolved-PH kill assert below this
MIN_EVENTS = 50         # powered-fold threshold (trade-touch barrier events)
REJECT_ALPHA = 0.05     # per-fold constant-hazard LR-test rejection level
KILL_FOLD_FRACTION = 0.30


# ------------------------------------------------ counting-process Cox fit

def _stratum_arrays(g):
    return (
        g[START_COL].to_numpy(dtype=float),
        g[STOP_COL].to_numpy(dtype=float),
        g[EVENT_COL].to_numpy(dtype=bool),
    )


def _risk_sums(start, stop, w, X, ev_times):
    """Risk-set weighted sums S0, S1, S2 at each event time, via difference
    arrays + cumsum: a row is in the risk set at event time t iff
    start < t <= stop."""
    ne = len(ev_times)
    p = X.shape[1]
    lo = np.searchsorted(ev_times, start, side="right")
    hi = np.searchsorted(ev_times, stop, side="right")
    active = lo < hi
    if not np.any(active):
        return np.zeros(ne), np.zeros((ne, p)), np.zeros((ne, p, p))
    start, stop, lo, hi, w, X = (start[active], stop[active], lo[active],
                                 hi[active], w[active], X[active])
    D0 = np.zeros(ne)
    D1 = np.zeros((ne, p))
    D2 = np.zeros((ne, p, p))
    np.add.at(D0, lo, w)
    np.add.at(D1, lo, w[:, None] * X)
    np.add.at(D2, lo, w[:, None, None] * X[:, :, None] * X[:, None, :])
    keep = hi < ne
    np.add.at(D0, hi[keep], -w[keep])
    np.add.at(D1, hi[keep], -w[keep, None] * X[keep])
    np.add.at(D2, hi[keep], -w[keep, None, None] * X[keep, :, None] * X[keep, None, :])
    return np.cumsum(D0), np.cumsum(D1, axis=0), np.cumsum(D2, axis=0)


def _stratum_score(start, stop, ev, X, beta):
    """Score, information, log partial likelihood, and per-event Schoenfeld
    ingredients for one stratum at the given beta."""
    eta = X @ beta
    shift = np.max(eta)
    w = np.exp(eta - shift)
    ev_times = np.unique(stop[ev])
    if len(ev_times) == 0:
        p = X.shape[1]
        return np.zeros(p), np.zeros((p, p)), 0.0, None
    S0, S1, S2 = _risk_sums(start, stop, w, X, ev_times)
    ie = np.where(ev)[0]
    ti = np.searchsorted(ev_times, stop[ie])
    xbar = S1[ti] / S0[ti][:, None]
    V = S2[ti] / S0[ti][:, None, None] - xbar[:, :, None] * xbar[:, None, :]
    U = X[ie].sum(axis=0) - xbar.sum(axis=0)
    I = V.sum(axis=0)
    ll = float((X[ie] @ beta).sum() - (np.log(S0[ti]) + shift * np.ones(len(ti))).sum())
    return U, I, ll, {"t": stop[ie], "x": X[ie], "xbar": xbar, "V": V}


def _groups(spells, strata_cols):
    g = spells.groupby(strata_cols, sort=False, observed=True) if strata_cols else [(None, spells)]
    out = []
    for _, sub in g:
        out.append(sub)
    return out


def fit_cox_counting(spells, covs, strata_cols=None, max_iter=100, tol=1e-9):
    """Breslow-tie Cox partial-likelihood fit on counting-process spells.
    Returns dict with beta, se, covariance matrix, log-likelihood and names."""
    covs = list(covs)
    p = len(covs)
    beta = np.zeros(p)
    subs = []
    for sub in _groups(spells, strata_cols):
        start, stop, ev = _stratum_arrays(sub)
        subs.append((start, stop, ev, sub[covs].to_numpy(dtype=float)))
    if p == 0:
        ll = 0.0
        for start, stop, ev, X in subs:
            _, _, l, _ = _stratum_score(start, stop, ev, X, beta)
            ll += l
        return {"beta": beta, "se": beta.copy(), "cov": np.zeros((0, 0)),
                "names": [], "loglik": ll, "n_iter": 0}
    ll = np.nan
    for it in range(max_iter):
        U = np.zeros(p)
        I = np.zeros((p, p))
        ll = 0.0
        for start, stop, ev, X in subs:
            u, infm, l, _ = _stratum_score(start, stop, ev, X, beta)
            U += u
            I += infm
            ll += l
        step = np.linalg.solve(I, U)
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            break
    covm = np.linalg.inv(I)
    return {
        "beta": beta,
        "se": np.sqrt(np.diag(covm)),
        "cov": covm,
        "names": covs,
        "loglik": ll,
        "n_iter": it + 1,
    }


def hr_ci(fit, cov, z=1.959963984540054):
    """95% (default) hazard-ratio confidence interval for one covariate."""
    i = fit["names"].index(cov)
    b, s = fit["beta"][i], fit["se"][i]
    return float(np.exp(b - z * s)), float(np.exp(b + z * s))


def loglik_ratio(fit_full, fit_null):
    """LR statistic and chi2 p-value of full vs nested null fit."""
    stat = 2.0 * (fit_full["loglik"] - fit_null["loglik"])
    df = len(fit_full["names"]) - len(fit_null["names"])
    return float(stat), float(sps.chi2.sf(stat, df))


# ------------------------------------------- Schoenfeld residual PH test

def _km_transform(spells):
    """g(t) = 1 - KM(t) evaluated at every event time (pooled)."""
    start, stop, ev = _stratum_arrays(spells)
    ev_times = np.unique(stop[ev])
    n_risk = np.empty(len(ev_times))
    d = np.empty(len(ev_times))
    for i, t in enumerate(ev_times):
        n_risk[i] = np.sum((start < t) & (stop >= t))
        d[i] = np.sum(ev & (stop == t))
    surv = np.cumprod(1.0 - d / np.maximum(n_risk, 1.0))
    return dict(zip(ev_times, 1.0 - surv))


def _time_transform(times, kind, spells):
    times = np.asarray(times, dtype=float)
    if kind == "identity":
        return times
    if kind == "log":
        return np.log(np.maximum(times, 1e-12))
    if kind == "rank":
        return sps.rankdata(times) / max(len(times), 1)
    if kind == "km":
        km = _km_transform(spells)
        return np.array([km[t] for t in times])
    raise ValueError(f"unknown transform {kind!r}")


def schoenfeld_ph_test(spells, covs, strata_cols=None, transform="km"):
    """Grambsch-Therneau proportional-hazards test on Schoenfeld residuals
    of a counting-process Cox model. Returns global and per-covariate
    chi2 statistics and p-values."""
    covs = list(covs)
    p = len(covs)
    fit = fit_cox_counting(spells, covs, strata_cols=strata_cols)
    beta = fit["beta"]
    res_t, res_r, res_V = [], [], []
    for sub in _groups(spells, strata_cols):
        start, stop, ev = _stratum_arrays(sub)
        X = sub[covs].to_numpy(dtype=float)
        _, _, _, ing = _stratum_score(start, stop, ev, X, beta)
        if ing is None:
            continue
        res_t.append(ing["t"])
        res_r.append(ing["x"] - ing["xbar"])
        res_V.append(ing["V"])
    if not res_t:
        return {"global_p": 1.0, "global_stat": 0.0, "covariate_p": {c: 1.0 for c in covs},
                "covariate_stat": {c: 0.0 for c in covs}, "n_events": 0, "transform": transform}
    t = np.concatenate(res_t)
    r = np.concatenate(res_r)
    V = np.concatenate(res_V)
    g = _time_transform(t, transform, spells)
    gd = g - g.mean()
    u = (gd[:, None] * r).sum(axis=0)
    Vu = np.einsum("k,kij->ij", gd * gd, V)
    global_stat = float(u @ np.linalg.solve(Vu, u))
    cov_stat = {c: float(u[j] ** 2 / Vu[j, j]) for j, c in enumerate(covs)}
    return {
        "global_p": float(sps.chi2.sf(global_stat, p)),
        "global_stat": global_stat,
        "covariate_p": {c: float(sps.chi2.sf(cov_stat[c], 1)) for c in covs},
        "covariate_stat": cov_stat,
        "n_events": int(len(t)),
        "transform": transform,
    }


def enforce_ph_rule(spells, covs, hour_col=HOUR_COL, regime_col=REGIME_COL,
                    ph_alpha=PH_ALPHA, hard_alpha=PH_HARD_ALPHA,
                    transform="km"):
    """Automatic stratification rule (pre-declared):
    1. Run the Schoenfeld residual PH test on the pooled model.
    2. If the global p or ANY covariate p < ph_alpha, automatically
       stratify baseline hazards by UTC hour-of-day s in {0..23} and the
       Layer 1 regime, and re-run the test.
    3. If the stratified model still shows p < hard_alpha, raise the
       unresolved-PH kill assert.
    """
    base = schoenfeld_ph_test(spells, covs, transform=transform)
    worst = min([base["global_p"]] + list(base["covariate_p"].values()))
    if worst >= ph_alpha:
        return {"ph_ok": True, "stratified": False, "test": base}
    strat = schoenfeld_ph_test(spells, covs, strata_cols=[hour_col, regime_col],
                               transform=transform)
    worst_strat = min([strat["global_p"]] + list(strat["covariate_p"].values()))
    if worst_strat < hard_alpha:
        offenders = {c: p for c, p in strat["covariate_p"].items() if p < hard_alpha}
        raise AssertionError(
            "KILL: unresolved proportional-hazards violation — worst Schoenfeld "
            f"p {worst_strat:.4g} < {hard_alpha} even after stratifying baseline "
            f"hazards by {hour_col} (UTC hour-of-day 0..23) and {regime_col} "
            f"(Layer 1 regime); offending covariates: {sorted(offenders)}"
        )
    return {"ph_ok": True, "stratified": True, "test": strat, "pooled_test": base}


# ------------------------------------------------------ powered folds

def filter_powered_folds(folds, min_events=MIN_EVENTS):
    """Flag or merge underpowered folds (< min_events trade-touch barrier
    events) so the constant-hazard null is evaluated strictly across
    powered folds. Underpowered folds are merged into the adjacent fold
    with the fewest events; anything still underpowered after all merges
    is flagged insufficient-power and excluded from the count (a power
    failure is not evidence).

    folds: sequence of dicts with keys 'fold' and 'events' (barrier-event
    count), in temporal order. Returns dict with 'powered', 'flagged',
    'merged'.
    """
    items = [dict(f) for f in folds]
    merged = []
    changed = True
    while changed:
        changed = False
        for i, f in enumerate(items):
            if f["events"] >= min_events:
                continue
            left = items[i - 1] if i > 0 else None
            right = items[i + 1] if i < len(items) - 1 else None
            cands = [nb for nb in (left, right) if nb is not None]
            if not cands:
                break
            nb = min(cands, key=lambda x: x["events"])
            j = i - 1 if nb is left else i + 1
            merged.append({"into": items[j]["fold"], "absorbed": f["fold"],
                           "events": f["events"]})
            items[j]["events"] += f["events"]
            items[j].setdefault("absorbed", []).append(f["fold"])
            items.pop(i)
            changed = True
            break
    powered = [f for f in items if f["events"] >= min_events]
    flagged = [f for f in items if f["events"] < min_events]
    return {"powered": powered, "flagged": flagged, "merged": merged}


def unrejected_powered_fraction(fold_stats, min_events=MIN_EVENTS,
                                 reject_alpha=REJECT_ALPHA):
    """Fraction of POWERED folds that fail to reject the constant-hazard
    null (per-fold LR-test p > reject_alpha). fold_stats: dicts with
    'fold', 'events', 'lr_p'. Returns (fraction, filter details)."""
    sel = filter_powered_folds(fold_stats, min_events=min_events)
    powered = sel["powered"]
    if not powered:
        return 0.0, sel
    unrejected = [f for f in powered if f["lr_p"] > reject_alpha]
    return len(unrejected) / len(powered), sel


def enforce_constant_hazard_kill(fold_stats, min_events=MIN_EVENTS,
                                 reject_alpha=REJECT_ALPHA,
                                 kill_fraction=KILL_FOLD_FRACTION):
    """Kill line 3 as a standalone assert (mirrors c1_l2_test kill line 3)."""
    frac, sel = unrejected_powered_fraction(fold_stats, min_events=min_events,
                                            reject_alpha=reject_alpha)
    if frac >= kill_fraction:
        raise AssertionError(
            "KILL LINE 3: constant-hazard null unrejected in "
            f"{frac:.0%} of powered folds"
        )
    return {"fraction": frac, "filter": sel}


# --------------------------------------------- adversarial null simulators

def simulate_garch_t(n, omega=2e-6, alpha=0.08, beta=0.90, nu=5.0, seed=0):
    """Pure Student-t GARCH(1,1) returns with NO microstructure state.
    Returns (returns, conditional_sigma)."""
    rng = np.random.default_rng(seed)
    dof_scale = np.sqrt(nu / max(nu - 2.0, 1e-9))
    z = rng.standard_t(nu, size=n) / dof_scale
    r = np.empty(n)
    sigma = np.empty(n)
    s = np.sqrt(omega / max(1.0 - alpha - beta, 1e-9))
    for t in range(n):
        sigma[t] = s
        r[t] = s * z[t]
        s = np.sqrt(omega + alpha * r[t] ** 2 + beta * s * s)
    return r, sigma


def sigma_standardized_block_null(returns, sigma_hat, block=24, n_rep=100,
                                  seed=0):
    """1h block-bootstrapped sigma-standardized null: z_t = r_t / sigma_hat_t,
    z* resampled in circular blocks of `block` consecutive standardized
    residuals, r*_t = sigma_hat_t * z*_t. Preserves the volatility and
    calendar structure, destroys event alignment. Returns (n_rep, n)."""
    z = np.asarray(returns, dtype=float) / np.asarray(sigma_hat, dtype=float)
    n = len(z)
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    out = np.empty((n_rep, n))
    for rep in range(n_rep):
        starts = rng.integers(0, n, n_blocks)
        idx = np.concatenate(
            [(np.arange(block) + s0) % n for s0 in starts]
        )[:n]
        out[rep] = sigma_hat * z[idx]
    return out


def trailing_sigma_hat(returns, window=24):
    """Trailing realized-vol estimate sigma_hat(t), computable at t only."""
    return pd.Series(returns).rolling(window).std().to_numpy()
