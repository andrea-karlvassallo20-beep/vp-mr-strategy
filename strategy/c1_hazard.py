"""C1 hazard test: compression duration-dependence on daily bars.

Spec (fixed before running, per director's instruction):
- Instruments: BTC then ETH, individually.
- Labels: triple-barrier, ATR(20)-scaled, computed at t0 from data <= t0.
  Two separate specs: (k=1.0, h=28) and (k=2.5, h=84). Censored retained.
- Cox, counting-process spells (one spell per decision day, cluster-robust SE
  by t0 month). Covariates at t0: compression flag (rvol percentile <= 33
  over trailing 60d), time-in-compression, trailing 12-week momentum,
  realized-vol level (log rvol20, standardized).
- Validation: purged 6-fold CV with CPCV concordance (all 15 test-pair splits),
  purge on label horizon, embargo = h.
- Placebo: block-temporal shuffle (circular shift of joint (r, vol) series;
  real states, surrogate labels), 100 reps.
- Scale-invariance null: block bootstrap of r/sigma residuals, full pipeline
  re-run on synthetic series, 100 reps.
"""

import json
import sys

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from lifelines.statistics import proportional_hazard_test

SEED = 20261112
N_PLACEBO = 100
N_SCALE = 100
BLOCK = 20
WARMUP = 60
PCT_THRESH = 33.0


def build_features(close, high, low):
    n = len(close)
    ret = np.full(n, np.nan)
    ret[1:] = close[1:] / close[:-1] - 1.0
    tr = np.full(n, np.nan)
    tr[1:] = np.maximum(
        high[1:] - low[1:],
        np.maximum(np.abs(high[1:] - close[:-1]), np.abs(low[1:] - close[:-1])),
    )
    rvol = np.full(n, np.nan)
    atr = np.full(n, np.nan)
    for t in range(WARMUP, n):
        rvol[t] = np.std(ret[t - 19 : t + 1], ddof=1)
        atr[t] = np.mean(tr[t - 19 : t + 1])
    pct = np.full(n, np.nan)
    for t in range(WARMUP, n):
        pct[t] = 100.0 * np.mean(rvol[t - 59 : t + 1] <= rvol[t])
    comp = pct <= PCT_THRESH
    tic = np.zeros(n)
    run = 0
    for t in range(WARMUP, n):
        run = run + 1 if comp[t] else 0
        tic[t] = run
    mom = np.full(n, np.nan)
    mom[WARMUP:] = close[WARMUP:] / close[WARMUP - 60 : n - 60] - 1.0
    return ret, rvol, atr, comp, tic, mom


def spells(close, high, low, comp, tic, mom, rvol, atr, k, h):
    n = len(close)
    rows = []
    for t0 in range(WARMUP, n - h):
        b = k * atr[t0]
        if not np.isfinite(b) or b <= 0:
            continue
        up = close[t0] + b
        dn = close[t0] - b
        ev, dur = 0, h
        for j in range(t0 + 1, t0 + h + 1):
            if high[j] >= up or low[j] <= dn:
                ev, dur = 1, j - t0
                break
        rows.append(
            {
                "t0": t0,
                "duration": dur,
                "event": ev,
                "compression": int(comp[t0]),
                "tic": tic[t0],
                "mom": mom[t0],
                "lrvol": np.log(max(rvol[t0], 1e-12)),
                "month": t0 // 21,
            }
        )
    df = pd.DataFrame(rows)
    for c in ("tic", "mom", "lrvol"):
        df[c] = (df[c] - df[c].mean()) / (df[c].std() + 1e-12)
    return df


COVS = ["compression", "tic", "mom", "lrvol"]


def fit_cox(df, covs=COVS):
    cph = CoxPHFitter()
    cph.fit(
        df[["duration", "event"] + covs + ["month"]],
        duration_col="duration",
        event_col="event",
        cluster_col="month",
        robust=True,
    )
    return cph


def gap(cph):
    return abs(float(cph.params_["compression"]))


def lr_vs_null(df, covs):
    ll_full = fit_cox(df, covs).log_likelihood_
    c0 = CoxPHFitter()
    c0.fit(df[["duration", "event"]], duration_col="duration",
           event_col="event")
    stat = 2 * (ll_full - c0.log_likelihood_)
    from scipy.stats import chi2
    return stat, float(chi2.sf(stat, len(covs)))


def purged_cv(df, h):
    t0s = df["t0"].to_numpy()
    n_groups = 6
    edges = np.linspace(t0s.min(), t0s.max() + 1, n_groups + 1)
    gid = np.clip(np.searchsorted(edges, t0s, side="right") - 1, 0, n_groups - 1)
    df = df.copy()
    df["gid"] = gid
    oof = []
    fold_stats = []
    for g in range(n_groups):
        te = df[df.gid == g]
        tr = df[(df.gid != g)]
        lo, hi = te["t0"].min(), te["t0"].max()
        keep = ~((tr["t0"] + h >= lo - h) & (tr["t0"] <= hi + h))
        tr = tr[keep]
        if len(tr) < 100 or te["event"].sum() < 10:
            fold_stats.append({"fold": int(g), "events": int(te["event"].sum()),
                               "insufficient": True})
            continue
        cph = fit_cox(tr)
        ph = -cph.predict_partial_hazard(te).to_numpy().ravel()  # higher = longer life
        oof.append((te["duration"].to_numpy(), ph, te["event"].to_numpy()))
        stat, p = lr_vs_null(te, COVS)
        fold_stats.append({"fold": int(g), "events": int(te["event"].sum()),
                           "lr_stat": stat, "lr_p": p, "insufficient": False})
    durs = np.concatenate([x[0] for x in oof])
    scores = np.concatenate([x[1] for x in oof])
    evs = np.concatenate([x[2] for x in oof])
    c = concordance_index(durs, scores, evs)
    # CPCV concordance over all 15 test-pair splits
    pair_c = []
    for i in range(n_groups):
        for j in range(i + 1, n_groups):
            te = df[(df.gid == i) | (df.gid == j)]
            lo, hi = te["t0"].min(), te["t0"].max()
            tr = df[(df.gid != i) & (df.gid != j)]
            keep = ~((tr["t0"] + h >= lo - h) & (tr["t0"] <= hi + h))
            tr = tr[keep]
            if len(tr) < 100 or te["event"].sum() < 10:
                continue
            cph = fit_cox(tr)
            ph = -cph.predict_partial_hazard(te).to_numpy().ravel()
            pair_c.append(concordance_index(te["duration"].to_numpy(), ph,
                                            te["event"].to_numpy()))
    return float(c), fold_stats, pair_c


def placebo(df_real, close, high, low, comp, tic, mom, rvol, atr, k, h, rng):
    n = len(close)
    ret = np.concatenate([[0.0], np.diff(np.log(close))])
    gaps = []
    for _ in range(N_PLACEBO):
        off = rng.integers(60, n - 60)
        r_shift = np.roll(ret, off)
        logp = np.log(close[WARMUP]) + np.cumsum(r_shift[WARMUP + 1 :])
        sur = np.concatenate([np.log(close[: WARMUP + 1]), logp])
        p = np.exp(sur)
        hi = p * (high / close)
        lo = p * (low / close)
        df_s = spells(p, hi, lo, comp, tic, mom, rvol, atr, k, h)
        if df_s["event"].sum() < 50:
            continue
        gaps.append(gap(fit_cox(df_s)))
    return np.array(gaps)


def scale_null(close, high, low, k, h, rng):
    n = len(close)
    ret = np.concatenate([[0.0], np.diff(np.log(close))])
    _, rvol, _, _, _, _ = build_features(close, high, low)
    sig = np.nan_to_num(rvol, nan=np.nanmedian(rvol))
    sig = np.maximum(sig, 1e-8)
    gaps = []
    idx = np.arange(1, n)
    idx = idx[: (len(idx) // BLOCK) * BLOCK]
    blocks = [idx[i : i + BLOCK] for i in range(0, len(idx), BLOCK)]
    n_blocks_needed = int(np.ceil((n - 1) / len(blocks)))
    for _ in range(N_SCALE):
        eps = np.concatenate([[0.0], ret[1:] / sig[1:]])
        chosen = rng.integers(0, len(blocks), size=len(blocks) * n_blocks_needed)
        new_eps = np.concatenate([eps[blocks[c]] for c in chosen])[: n - 1]
        new_eps = np.concatenate([[0.0], new_eps])
        r_new = sig * new_eps
        logp = np.log(close[0]) + np.cumsum(r_new)
        p = np.exp(logp)
        hi = p * (high / close)
        lo = p * (low / close)
        f = build_features(p, hi, lo)
        df_s = spells(p, hi, lo, f[3], f[4], f[5], f[1], f[2], k, h)
        if df_s["event"].sum() < 50:
            continue
        gaps.append(gap(fit_cox(df_s)))
    return np.array(gaps)


def run(path, name):
    rng = np.random.default_rng(SEED)
    d = pd.read_csv(path)
    close = d["close"].to_numpy(float)
    high = d["high"].to_numpy(float)
    low = d["low"].to_numpy(float)
    ret, rvol, atr, comp, tic, mom = build_features(close, high, low)
    out = {"instrument": name, "n_days": len(close), "specs": {}}
    for k, h in [(1.0, 28), (2.5, 84)]:
        df = spells(close, high, low, comp, tic, mom, rvol, atr, k, h)
        cph = fit_cox(df)
        summ = cph.summary[["coef", "exp(coef)", "exp(coef) lower 95%",
                            "exp(coef) upper 95%", "p"]].to_dict("index")
        cph_nc = CoxPHFitter()
        cph_nc.fit(df[["duration", "event"] + COVS], duration_col="duration",
                   event_col="event")
        ph_test = proportional_hazard_test(
            cph_nc, df[["duration", "event"] + COVS], time_transform="rank")
        taut = fit_cox(df, ["compression", "lrvol"])
        taut_ci = [float(taut.summary.loc["compression", "exp(coef) lower 95%"]),
                   float(taut.summary.loc["compression", "exp(coef) upper 95%"])]
        conc, folds, pair_c = purged_cv(df, h)
        obs_gap = gap(cph)
        pl = placebo(df, close, high, low, comp, tic, mom, rvol, atr, k, h, rng)
        sc = scale_null(close, high, low, k, h, rng)
        out["specs"][f"k{k}_h{h}"] = {
            "n_spells": int(len(df)),
            "n_events": int(df["event"].sum()),
            "compression_hazard_low": float(summ["compression"]["exp(coef) lower 95%"]),
            "compression_hazard_high": float(summ["compression"]["exp(coef) upper 95%"]),
            "compression_p": float(summ["compression"]["p"]),
            "coefficients": {c: {kk: float(vv) for kk, vv in summ[c].items()} for c in COVS},
            "ph_test_p": {c: float(ph_test.summary.loc[c, "p"]) for c in COVS},
            "vol_tautology_hr_ci": taut_ci,
            "oof_concordance": conc,
            "cpcv_pair_concordance_median": float(np.median(pair_c)) if pair_c else None,
            "fold_lr": folds,
            "observed_gap_log_hr": obs_gap,
            "placebo_gap_median": float(np.median(pl)) if len(pl) else None,
            "placebo_gap_p95": float(np.percentile(pl, 95)) if len(pl) else None,
            "placebo_reproduces_50pct": bool(
                len(pl) and np.median(pl) >= 0.5 * obs_gap),
            "scale_null_gap_median": float(np.median(sc)) if len(sc) else None,
            "scale_null_gap_ci95": [float(np.percentile(sc, 2.5)),
                                    float(np.percentile(sc, 97.5))] if len(sc) else None,
            "scale_null_reproduces": bool(
                len(sc) and np.percentile(sc, 2.5) <= obs_gap <= np.percentile(sc, 97.5)),
            "scale_null_reps": int(len(sc)),
            "placebo_reps": int(len(pl)),
        }
    return out


if __name__ == "__main__":
    res = run(sys.argv[1], sys.argv[2])
    with open(sys.argv[3], "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
