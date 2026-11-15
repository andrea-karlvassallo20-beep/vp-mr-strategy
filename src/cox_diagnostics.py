"""Cox diagnostics for the C1-L2 harness: Schoenfeld residual PH audit,
automatic hour-of-day/regime stratification, and powered-fold enforcement.

Everything here runs on SYNTHETIC data only (unit tests, adversarial null
simulations). No output of this module is a research result; the only legal
run on real data is on Tardis full-depth L2 that has passed
src/verify_l2_gate.py, executed by src/c1_l2_test.py.

Design notes:
  - The Cox partial likelihood is implemented directly on counting-process
    (start, stop, event] intervals so time-varying risk sets (the C1-L2 long
    format with refresh rows) are handled exactly. Breslow ties.
  - The Schoenfeld test is the Grambsch-Therneau proportional-hazards test
    (the statistic behind survival::cox.zph): u = sum over deaths of
    (g(t_i) - gbar) * r_i with variance C = sum (g - gbar)^2 V_i, where r_i
    is the Schoenfeld residual and V_i the risk-set weighted covariance at
    the death time. Global chi-square has p df; each covariate 1 df.
  - PH rule (binding): if the global or any covariate Schoenfeld p < 0.05
    (the regime that produced the pooled daily lrvol HR=0.68 violation),
    baseline hazards are automatically stratified by UTC hour-of-day
    s in {0..23} AND the Layer 1 regime. If the violation persists at
    p < 0.01 after stratification, an unresolved-PH kill AssertionError is
    raised: the model is not proportional and no HR from it is reportable.
"""

import numpy as np
import pandas as pd
from scipy import stats

PH_STRATIFY_P = 0.05
PH_KILL_P = 0.01
POWERED_MIN_EVENTS = 50
UNREJECTION_ALPHA = 0.05
UNREJECTED_FOLD_KILL_FRACTION = 0.30

_TIME_TRANSFORMS = ("log", "identity", "rank")


# ----------------------------------------------------- counting-process Cox

def _prep(df, covs, strata):
    covs = list(covs)
    strata = list(strata or [])
    req = {"start", "stop", "event"} | set(covs) | set(strata)
    missing = req - set(df.columns)
    if missing:
        raise ValueError(f"cox data missing columns: {sorted(missing)}")
    start = df["start"].to_numpy(dtype=float)
    stop = df["stop"].to_numpy(dtype=float)
    event = df["event"].to_numpy(dtype=int)
    if np.any(stop <= start):
        raise ValueError("counting-process rows must satisfy start < stop")
    if not np.isin(event, [0, 1]).all():
        raise ValueError("event must be 0/1")
    X = df[covs].to_numpy(dtype=float)
    if strata:
        keys = df[strata].to_numpy()
        if keys.ndim == 1:
            keys = keys.reshape(-1, 1)
        _, codes = np.unique(keys, axis=0, return_inverse=True)
    else:
        codes = np.zeros(len(df), dtype=int)
    return start, stop, event, X, codes.astype(int), covs, strata


def _accumulate(beta, start, stop, event, X, codes, n_strata,
                want=("loglik", "grad", "info")):
    p = X.shape[1]
    eta = X @ beta
    loglik = 0.0
    grad = np.zeros(p)
    info = np.zeros((p, p))
    for s in range(n_strata):
        m = codes == s
        if not m.any():
            continue
        xs, st, sp, ev = X[m], start[m], stop[m], event[m]
        es = eta[m]
        ev_times = np.unique(sp[ev == 1])
        for t in ev_times:
            risk = (st < t) & (sp >= t)
            xr = xs[risk]
            w = np.exp(es[risk])
            S0 = w.sum()
            if S0 <= 0 or not np.isfinite(S0):
                raise FloatingPointError("degenerate risk set in Cox fit")
            S1 = w @ xr
            S2 = (xr * w[:, None]).T @ xr
            dmask = (sp == t) & (ev == 1)
            d = int(dmask.sum())
            xd_sum = xs[dmask].sum(axis=0)
            if "loglik" in want:
                loglik += es[dmask].sum() - d * np.log(S0)
            if "grad" in want:
                grad += xd_sum - d * S1 / S0
            if "info" in want:
                info += d * (S2 / S0 - np.outer(S1, S1) / S0 ** 2)
    return loglik, grad, info


def fit_cox(df, covs, strata=None, max_iter=100, tol=1e-9):
    """Breslow-tie Cox partial likelihood on (start, stop, event] rows,
    optionally stratified. Returns a fit object (dict) carrying beta,
    covariance, and the prep needed by the Schoenfeld residual test."""
    start, stop, event, X, codes, covs, strata = _prep(df, covs, strata)
    n_strata = int(codes.max()) + 1 if len(codes) else 1
    p = X.shape[1]
    beta = np.zeros(p)
    ll, _, _ = _accumulate(beta, start, stop, event, X, codes, n_strata,
                           want=("loglik",))
    for _ in range(max_iter):
        ll, grad, info = _accumulate(beta, start, stop, event, X, codes,
                                     n_strata)
        try:
            step = np.linalg.solve(info, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.pinv(info) @ grad
        t = 1.0
        while t > 1e-8:
            cand = beta + t * step
            ll_c, _, _ = _accumulate(cand, start, stop, event, X, codes,
                                     n_strata, want=("loglik",))
            if ll_c >= ll - 1e-12:
                break
            t /= 2.0
        beta = beta + t * step
        if np.max(np.abs(t * step)) < tol:
            break
    ll, grad, info = _accumulate(beta, start, stop, event, X, codes,
                                 n_strata)
    try:
        cov = np.linalg.inv(info)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(info)
    return {
        "beta": beta, "cov": cov, "covs": covs, "strata": strata,
        "loglik": ll, "n_events": int(event.sum()),
        "_start": start, "_stop": stop, "_event": event, "_X": X,
        "_codes": codes, "_n_strata": n_strata,
    }


def coef_table(fit, alpha=0.05):
    z = stats.norm.ppf(1 - alpha / 2)
    se = np.sqrt(np.diag(fit["cov"]))
    beta = fit["beta"]
    rows = []
    for j, name in enumerate(fit["covs"]):
        lo, hi = beta[j] - z * se[j], beta[j] + z * se[j]
        rows.append({
            "covariate": name, "coef": float(beta[j]), "se": float(se[j]),
            "hr": float(np.exp(beta[j])),
            "hr_lo": float(np.exp(lo)), "hr_hi": float(np.exp(hi)),
            "z": float(beta[j] / se[j]) if se[j] > 0 else np.nan,
            "p": float(2 * stats.norm.sf(abs(beta[j] / se[j])))
                 if se[j] > 0 else np.nan,
        })
    return pd.DataFrame(rows)


def hr_ci(fit, covariate, alpha=0.05):
    """(hr, lo, hi) for one covariate."""
    t = coef_table(fit, alpha=alpha)
    row = t[t["covariate"] == covariate].iloc[0]
    return float(row["hr"]), float(row["hr_lo"]), float(row["hr_hi"])


def concordance(fit):
    """Harrell's c-index on the fit's own rows, within strata (pairs across
    strata have different baseline hazards and are not comparable)."""
    stop, event, X, codes = fit["_stop"], fit["_event"], fit["_X"], fit["_codes"]
    eta = X @ fit["beta"]
    num = den = 0.0
    for s in range(fit["_n_strata"]):
        m = codes == s
        if not m.any():
            continue
        ev = np.where(m & (event == 1))[0]
        for i in ev:
            comparable = m & (stop > stop[i])
            if not comparable.any():
                continue
            higher = eta[comparable] < eta[i]
            equal = eta[comparable] == eta[i]
            num += higher.sum() + 0.5 * equal.sum()
            den += comparable.sum()
    return num / den if den else np.nan


def constant_hazard_lr_pvalue(df, covs, strata=None):
    """Likelihood-ratio p-value for the constant-hazard null beta = 0
    (no covariate effects). This is the fold-level test behind kill line 3."""
    fit = fit_cox(df, covs, strata=strata)
    start, stop, event, X, codes = (fit["_start"], fit["_stop"],
                                    fit["_event"], fit["_X"], fit["_codes"])
    ll0, _, _ = _accumulate(np.zeros(X.shape[1]), start, stop, event, X,
                            codes, fit["_n_strata"], want=("loglik",))
    chi2 = 2.0 * (fit["loglik"] - ll0)
    dof = max(X.shape[1], 1)
    return float(stats.chi2.sf(chi2, dof)), float(chi2)


# ------------------------------------------------- Schoenfeld residual PH

def _time_transform(t, kind):
    t = np.asarray(t, dtype=float)
    if kind == "log":
        return np.log(t)
    if kind == "identity":
        return t
    if kind == "rank":
        order = np.argsort(np.argsort(t))
        return order.astype(float)
    raise ValueError(f"unknown time transform {kind!r}; use {_TIME_TRANSFORMS}")


def schoenfeld_test(fit, time_transform="log"):
    """Grambsch-Therneau Schoenfeld residual PH test for counting-process
    Cox fits (stratified fits are tested within strata, as they must be).

    Returns {"global_p", "global_chi2", "covariate_p": {name: p},
             "covariate_chi2": {name: chi2}, "n_deaths", "time_transform"}.
    """
    if time_transform not in _TIME_TRANSFORMS:
        raise ValueError(f"unknown time transform {time_transform!r}")
    start, stop, event, X, codes = (fit["_start"], fit["_stop"],
                                    fit["_event"], fit["_X"], fit["_codes"])
    beta = fit["beta"]
    eta = X @ beta
    deaths = np.where(event == 1)[0]
    if len(deaths) == 0:
        raise ValueError("no events: PH test undefined")
    g = _time_transform(stop[deaths], time_transform)
    gbar = g.mean()
    p = X.shape[1]
    u = np.zeros(p)
    C = np.zeros((p, p))
    for s in range(fit["_n_strata"]):
        ms = codes == s
        if not ms.any():
            continue
        xs, st, sp, ev = X[ms], start[ms], stop[ms], event[ms]
        es = eta[ms]
        for t in np.unique(sp[ev == 1]):
            risk = (st < t) & (sp >= t)
            xr = xs[risk]
            w = np.exp(es[risk])
            S0 = w.sum()
            S1 = w @ xr
            S2 = (xr * w[:, None]).T @ xr
            xbar = S1 / S0
            V = S2 / S0 - np.outer(xbar, xbar)
            dmask = (sp == t) & (ev == 1)
            for k in np.where(dmask)[0]:
                gi = _time_transform(np.array([t]), time_transform)[0]
                u += (gi - gbar) * (xs[k] - xbar)
                C += (gi - gbar) ** 2 * V
    C = 0.5 * (C + C.T)
    try:
        chi2_global = float(u @ np.linalg.solve(C, u))
    except np.linalg.LinAlgError:
        chi2_global = float(u @ np.linalg.pinv(C) @ u)
    global_p = float(stats.chi2.sf(chi2_global, p))
    cov_p, cov_chi2 = {}, {}
    for j, name in enumerate(fit["covs"]):
        if C[j, j] > 0:
            cj = float(u[j] ** 2 / C[j, j])
        else:
            cj = 0.0
        cov_chi2[name] = cj
        cov_p[name] = float(stats.chi2.sf(cj, 1))
    return {
        "global_p": global_p, "global_chi2": chi2_global,
        "covariate_p": cov_p, "covariate_chi2": cov_chi2,
        "n_deaths": int(len(deaths)), "time_transform": time_transform,
    }


def _worst_p(z):
    return min([z["global_p"]] + list(z["covariate_p"].values()))


def ph_audit(df, covs, hour_col="hour", regime_col="regime",
             base_strata=None, time_transform="log",
             p_stratify=PH_STRATIFY_P, p_kill=PH_KILL_P):
    """Schoenfeld audit with automatic stratification (the binding PH rule).

    1. Fit with the caller's strata and run the Schoenfeld test.
    2. If global or any covariate p < p_stratify, refit with baseline hazards
       stratified by UTC hour-of-day (24 levels) AND the Layer 1 regime.
    3. If the violation persists at p < p_kill after stratification, raise
       the unresolved-PH kill AssertionError.
    """
    covs = list(covs)
    base_strata = list(base_strata or [])
    fit0 = fit_cox(df, covs, strata=base_strata)
    z0 = schoenfeld_test(fit0, time_transform)
    report = {
        "stratified": False, "strata": base_strata,
        "initial_schoenfeld": z0, "final_schoenfeld": z0,
        "worst_p_initial": _worst_p(z0), "worst_p_final": _worst_p(z0),
        "fit": fit0,
    }
    if _worst_p(z0) >= p_stratify:
        return report
    hour_levels = df[hour_col].nunique()
    if hour_levels > 24:
        raise ValueError(f"{hour_col!r} must be UTC hour-of-day in 0..23")
    auto = [c for c in [hour_col, regime_col] if c and c not in base_strata]
    if not auto:
        # already stratified by hour and regime, yet PH still fails
        if _worst_p(z0) < p_kill:
            raise AssertionError(
                "unresolved-PH kill: Schoenfeld "
                f"p={_worst_p(z0):.4g} < {p_kill} even with hour-of-day and "
                "regime strata; the model is not proportional and no HR "
                "from it is reportable"
            )
        report["stratified"] = True
        return report
    strata = base_strata + auto
    fit1 = fit_cox(df, covs, strata=strata)
    z1 = schoenfeld_test(fit1, time_transform)
    report.update({
        "stratified": True, "strata": strata,
        "final_schoenfeld": z1, "worst_p_final": _worst_p(z1),
        "fit": fit1,
    })
    if _worst_p(z1) < p_kill:
        raise AssertionError(
            "unresolved-PH kill: Schoenfeld "
            f"p={_worst_p(z1):.4g} < {p_kill} persists after stratifying "
            f"baseline hazards by UTC hour-of-day and {regime_col}; the "
            "proportional-hazards assumption is dead and no HR is reportable"
        )
    return report


# -------------------------------------------------- powered-fold enforcement

def filter_powered_folds(folds, min_events=POWERED_MIN_EVENTS, merge=True):
    """Flag (or merge) folds holding fewer than `min_events` trade-touch
    barrier events, so constant-hazard non-rejection is judged strictly
    across powered folds — non-rejection in an underpowered fold is a power
    failure, not evidence.

    folds: sequence of dicts with at least "events" (int); optional
      "spells" (DataFrame) and "lr_p" (float).
    merge=True: an underpowered fold is merged into its neighbor (forward,
    falling back to the previous fold at the end) and the merged fold's
    "lr_p" is reset to None — the LR test must be recomputed on the merged
    spell set. Folds that remain underpowered after merging stay flagged
    powered=False and are excluded from the kill-line-3 count.

    Returns a new list of fold dicts, each with "powered" (bool) and,
    for merged folds, "merged_from" (list of source fold ids).
    """
    if min_events < 1:
        raise ValueError("min_events must be >= 1")
    out = []
    for i, f in enumerate(folds):
        rec = dict(f)
        rec.setdefault("fold_id", i)
        rec["powered"] = int(f["events"]) >= min_events
        out.append(rec)
    if not merge:
        return out
    changed = True
    while changed:
        changed = False
        for i, rec in enumerate(out):
            if rec["powered"] or rec["events"] >= min_events:
                continue
            j = i + 1 if i + 1 < len(out) else i - 1
            if j < 0:
                break
            tgt = out[j]
            merged_events = int(rec["events"]) + int(tgt["events"])
            tgt["events"] = merged_events
            tgt["powered"] = merged_events >= min_events
            tgt["lr_p"] = None
            src = rec.get("merged_from", [rec.get("fold_id", i)])
            tgt.setdefault("merged_from", [tgt.get("fold_id", j)])
            tgt["merged_from"] = sorted(set(tgt["merged_from"]) | set(src))
            if "spells" in rec and "spells" in tgt:
                tgt["spells"] = pd.concat([tgt["spells"], rec["spells"]],
                                           ignore_index=True)
            out.pop(i)
            changed = True
            break
    for rec in out:
        if rec["events"] < min_events and rec["powered"]:
            rec["powered"] = False
    return out


def unrejected_powered_fraction(folds, alpha=UNREJECTION_ALPHA):
    """Fraction of POWERED folds whose constant-hazard LR test fails to
    reject (p > alpha). Underpowered folds are excluded by design; the
    kill threshold is >= 0.30 (kill line 3 in src/c1_l2_test.py)."""
    tested = [f for f in folds if f.get("powered")
              and f.get("lr_p") is not None]
    if not tested:
        raise ValueError("no powered folds with a computed lr_p")
    return float(np.mean([f["lr_p"] > alpha for f in tested]))


def enforce_powered_fold_kill(folds, min_events=POWERED_MIN_EVENTS,
                              kill_fraction=UNREJECTED_FOLD_KILL_FRACTION):
    """Convenience wrapper: filter, then raise kill line 3 if the
    unrejected fraction among powered folds reaches the threshold."""
    powered = filter_powered_folds(folds, min_events=min_events)
    frac = unrejected_powered_fraction(powered)
    if frac >= kill_fraction:
        raise AssertionError(
            "KILL LINE 3: constant-hazard null unrejected in "
            f"{frac:.0%} of powered folds (>= {kill_fraction:.0%})"
        )
    return powered, frac
