"""Adversarial null simulations proving every pre-declared C1-L2 kill line
in src/c1_l2_test.py fires on SYNTHETIC null markets, before any real L2
data is ingested. No result here is a research result.

  Test A (Vol-Tautology Trap): pure Student-t GARCH(1,1) returns with NO
  microstructure state. Once trailing sigma_H is in the model, the
  compression HR 95% CI spans 1.0 -> kill line 2 fires.

  Test B (Scale-Invariance Null): a synthetic market carrying a planted
  calendar/volatility-clustering artifact (near-integrated GARCH vol on a
  diurnal sigma schedule: compression then has a REAL barrier-hit hazard
  effect that hour-of-day stratification cannot remove). The 1h
  block-bootstrapped sigma-standardized generator
  r*_t = sigma_hat(t) * z*_t reproduces the observed compression gap within
  its 95% band -> kill line 5 fires (whole-layer kill).

  Plus: Schoenfeld residual audit (detection, auto-stratification by UTC
  hour + regime, unresolved-PH kill), powered-fold enforcement, and kill
  lines 1, 3, 4 firing on their own synthetic nulls.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import c1_l2_test as c1
import cox_diagnostics as cd

# ------------------------------------------------------------ sim constants
PER_HOUR = 4                 # 15-minute grid
DT_H = 1.0 / PER_HOUR
H_HOURS = 24
H_OBS = H_HOURS * PER_HOUR
WARMUP_H = 24 * 7
WARMUP_OBS = WARMUP_H * PER_HOUR
HOD_BUCKETS = 6              # 4h hour-of-day buckets, as in c1_l2_test
POOL_DECISIONS = 5 * HOD_BUCKETS   # 5-day trailing pool, same bucket
POOL_MIN = 10
PCT_THRESHOLD = 33.0
K_BARRIER = 1.0


def simulate_garch_t(n_hours, seed, nu=5.0, alpha=0.10, beta_v=0.75,
                     hourly_var=1.6e-5, diurnal_amp=0.0):
    """Student-t GARCH(1,1) 15-minute returns with an optional hour-of-day
    volatility multiplier (the calendar channel). No microstructure state."""
    n = n_hours * PER_HOUR
    rng = np.random.default_rng(seed)
    z = rng.standard_t(nu, n) / np.sqrt(nu / (nu - 2.0))
    var15 = hourly_var / PER_HOUR
    omega = (1.0 - alpha - beta_v) * var15
    sigma2 = var15
    hours = (np.arange(n) // PER_HOUR) % 24
    diurnal = 1.0 + diurnal_amp * np.sin(2.0 * np.pi * (hours - 3.0) / 24.0)
    ret = np.empty(n)
    sigma = np.empty(n)
    for t in range(n):
        sig = np.sqrt(sigma2) * diurnal[t]
        sigma[t] = sig
        ret[t] = sig * z[t]
        sigma2 = omega + alpha * ret[t] ** 2 + beta_v * sigma2
    return ret, sigma


def trailing_sigma_hat(ret):
    """The SAME trailing 24h realized-vol estimator the barriers use
    (computable at the decision moment only): rolling std of the last 24h
    of 15-minute returns, scaled to the 24h horizon."""
    return pd.Series(ret).rolling(PER_HOUR * 24).std().to_numpy()


def build_spells(ret, sigma_hat, compression="normalized", k=K_BARRIER,
                 pct_threshold=PCT_THRESHOLD):
    """Full synthetic pipeline: hourly decision rows, compression flag
    (percentile-ranked against the trailing 5-day pool of the SAME
    hour-of-day), sigma_H barriers, trade-touch-equivalent barrier labels
    on the synthetic path, Cox long-format (start, stop, event] rows.

    compression="normalized"  : spec-compliant range in sigma_H units.
    compression="raw"        : RAW range percentile (the artifact channel:
                               volatility clustering / diurnal seasonality
                               leaks straight into the flag).
    """
    price = 100.0 * np.exp(np.cumsum(ret))
    n = len(ret)
    sig_h = sigma_hat * np.sqrt(PER_HOUR * 24)
    rows = []
    for i in range(WARMUP_OBS, n - H_OBS, PER_HOUR):
        sh = sig_h[i]
        if not np.isfinite(sh) or sh <= 0:
            continue
        p0 = price[i]
        w = price[i - 4 * PER_HOUR:i]
        range4 = (w.max() - w.min()) / p0
        hour = (i // PER_HOUR) % 24
        rows.append({"i": i, "units": range4 / sh if compression == "normalized"
                     else range4, "sigma_h": sh, "hour": hour,
                     "hod_bucket": hour // (24 // HOD_BUCKETS)})
    dec = pd.DataFrame(rows)
    # percentile within the trailing 5-day pool of the same hour-of-day
    pct = np.full(len(dec), np.nan)
    pct_sh = np.full(len(dec), np.nan)
    units = dec["units"].to_numpy()
    shv = dec["sigma_h"].to_numpy()
    for h in range(HOD_BUCKETS):
        idx = np.where(dec["hod_bucket"].to_numpy() == h)[0]
        for j in idx:
            rank = int(np.searchsorted(idx, j))
            pool_u = units[idx[max(0, rank - POOL_DECISIONS):rank]]
            pool_s = shv[max(0, j - POOL_DECISIONS):j]
            if len(pool_u) >= POOL_MIN:
                pct[j] = 100.0 * np.mean(pool_u <= units[j])
            if len(pool_s) >= POOL_MIN:
                pct_sh[j] = 100.0 * np.mean(pool_s <= shv[j])
    dec["compression"] = (pct <= pct_threshold)
    dec["pct"] = pct
    dec["regime"] = np.where(pct_sh < 0, -1, np.select(
        [pct_sh <= 33.0, pct_sh >= 67.0], [0, 2], default=1))
    # forward barrier spells on the synthetic path
    spells = []
    for r in dec.itertuples():
        i0, p0, sh = r.i, price[r.i], r.sigma_h
        fwd = price[i0 + 1:i0 + H_OBS + 1] / p0 - 1.0
        hit = np.nonzero(np.abs(fwd) >= k * sh)[0]
        if len(hit):
            ev, dur = 1, (hit[0] + 1) * DT_H
        else:
            ev, dur = 0, float(H_HOURS)
        spells.append({
            "start": 0.0, "stop": dur, "event": ev,
            "compression": int(r.compression),
            "log_sigma": float(np.log(r.sigma_h)),
            "hour": int(r.hour), "regime": int(r.regime),
            "t0": int(r.i),
        })
    return pd.DataFrame(spells)


def block_bootstrap_returns(ret, sigma_hat, rng, block_len=PER_HOUR):
    """1h block bootstrap of the sigma-standardized residuals:
    r*_t = sigma_hat(t) * z*_t. sigma_hat(t) is FIXED (it carries the
    calendar/volatility schedule; the null neutralizes exactly the scaling
    the test uses), the block resampling destroys event alignment."""
    s = pd.Series(sigma_hat).ffill().bfill().to_numpy()
    z = ret / s
    n = len(z)
    n_blocks = int(np.ceil(n / block_len))
    starts = rng.integers(0, n - block_len + 1, n_blocks)
    idx = (starts[:, None] + np.arange(block_len)[None, :]).ravel()[:n]
    return s * z[idx]


# ------------------------------------------------- counting-process simulator

def simulate_ph_spells(n, seed, beta_fn, base_fn, x_fn, hour_fn=None,
                       regime_fn=None, joint_fn=None, max_u=24, censor=None):
    """Direct counting-process simulator for PH-audit unit tests: hazard at
    elapsed hour u is base(hour, regime, u) * exp(beta(u) . x) * step, with
    optional censoring. beta_fn(u) makes time-varying effects and
    hour-dependent baseline SHAPES constructible. joint_fn(rng) -> (x, hour, regime) draws covariates jointly (needed to
    correlate the covariate with the hour, the diurnal-artifact channel)."""
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n):
        if joint_fn is not None:
            x, hour, regime = joint_fn(rng)
        else:
            x = x_fn(rng)
            hour = int(hour_fn(rng)) if hour_fn else 0
            regime = int(regime_fn(rng)) if regime_fn else 0
        hour, regime = int(hour), int(regime)
        event, dur = 0, float(max_u)
        cens = censor(rng) if censor else float(max_u)
        for u in range(1, max_u + 1):
            lam = base_fn(hour, regime, u) \
                * float(np.exp(beta_fn(u) @ np.atleast_1d(x)))
            if rng.random() < min(lam, 0.5):
                event, dur = 1, float(u)
                break
            if u >= cens:
                dur = float(u)
                break
        rows.append({"start": 0.0, "stop": dur, "event": event,
                     "x": float(np.atleast_1d(x)[0]), "hour": hour,
                     "regime": regime})
    return pd.DataFrame(rows)


def _results(oof_concordance=0.55, tautology_hr_ci=(0.7, 0.9),
             unrejected=0.0, stratified_hr_ci=(0.7, 0.9),
             scale_null_gap_ci95=(-1.0, -0.5), observed_gap=1.0):
    return {
        "oof_concordance": oof_concordance,
        "tautology_hr_ci": tautology_hr_ci,
        "unrejected_powered_fold_fraction": unrejected,
        "stratified_hr_ci": stratified_hr_ci,
        "scale_null_gap_ci95": scale_null_gap_ci95,
        "observed_gap": observed_gap,
    }


# ------------------------------------------------ Schoenfeld residual audit

def test_cox_recovers_planted_hr():
    rng = np.random.default_rng(7)
    n = 6000
    x = rng.integers(0, 2, n).astype(float)
    lam0, beta = 0.04, 0.7
    ev = rng.random(n) < lam0 * np.exp(beta * x)
    stop = np.where(ev, rng.integers(1, 25, n), 24).astype(float)
    df = pd.DataFrame({"start": 0.0, "stop": stop, "event": ev.astype(int),
                       "x": x, "hour": 0, "regime": 0})
    fit = cd.fit_cox(df, ["x"])
    hr, lo, hi = cd.hr_ci(fit, "x")
    assert abs(np.log(hr) - beta) < 0.25
    assert lo <= np.exp(beta) <= hi


def test_schoenfeld_silent_under_true_ph():
    beta = np.array([-0.4])
    df = simulate_ph_spells(
        4000, seed=11, beta_fn=lambda u: beta,
        base_fn=lambda h, r, u: 0.05,
        x_fn=lambda rng: np.array([1.0 if rng.random() < 0.4 else 0.0]),
        censor=lambda rng: rng.uniform(6, 24),
    )
    fit = cd.fit_cox(df, ["x"])
    z = cd.schoenfeld_test(fit, time_transform="log")
    assert z["global_p"] >= 0.05
    assert z["covariate_p"]["x"] >= 0.05
    rep = cd.ph_audit(df, ["x"])
    assert rep["stratified"] is False


def test_schoenfeld_detects_hour_driven_violation_and_stratifies():
    """Compression correlated with quiet hours whose baseline hazard SHAPE
    differs (front-loaded) from busy hours: the pooled fit is non-PH (the
    pooled-daily lrvol HR=0.68 regime). Automatic stratification by UTC
    hour-of-day and Layer 1 regime must resolve it (true beta constant
    within hour)."""
    beta = np.array([-0.35])
    diurnal = 1.0 + 0.9 * np.sin(2 * np.pi * (np.arange(24) - 3) / 24)
    quiet = diurnal < 1.0

    def joint_fn(rng):
        h = int(rng.integers(0, 24))
        # compression flags concentrate in quiet (low-baseline) hours
        p_x = 0.80 if quiet[h] else 0.15
        x = np.array([1.0 if rng.random() < p_x else 0.0])
        return x, h, int(rng.integers(0, 2))

    def base_fn(h, r, u):
        # quiet hours: front-loaded hazard; busy hours: flat
        return 0.10 * np.exp(-u / 6.0) if quiet[h] else 0.05

    df = simulate_ph_spells(
        8000, seed=23, beta_fn=lambda u: beta,
        base_fn=base_fn,
        x_fn=None, joint_fn=joint_fn,
        censor=lambda rng: rng.uniform(8, 24),
    )
    fit = cd.fit_cox(df, ["x"])
    z0 = cd.schoenfeld_test(fit)
    assert z0["global_p"] < 0.05 or z0["covariate_p"]["x"] < 0.05
    rep = cd.ph_audit(df, ["x"])
    assert rep["stratified"] is True
    assert set(["hour", "regime"]) <= set(rep["strata"])
    assert rep["worst_p_final"] >= cd.PH_KILL_P


def test_unresolved_ph_violation_raises_kill():
    """A genuinely time-varying effect (beta decays within the follow-up):
    hour/regime stratification cannot repair it -> unresolved-PH kill."""
    beta0 = -0.9
    df = simulate_ph_spells(
        6000, seed=31, beta_fn=lambda u: np.array([beta0 * np.exp(-u / 4.0)]),
        base_fn=lambda h, r, u: 0.05,
        x_fn=lambda rng: np.array([1.0 if rng.random() < 0.4 else 0.0]),
        regime_fn=lambda rng: int(rng.integers(0, 2)),
        censor=lambda rng: rng.uniform(8, 24),
    )
    fit = cd.fit_cox(df, ["x"])
    z = cd.schoenfeld_test(fit)
    assert z["global_p"] < 0.01 or z["covariate_p"]["x"] < 0.01
    with pytest.raises(AssertionError, match="unresolved-PH kill"):
        cd.ph_audit(df, ["x"])


# -------------------------------------------------- powered-fold machinery

def test_filter_powered_folds_flags_and_merges():
    folds = [
        {"fold_id": 0, "events": 80, "lr_p": 0.01},
        {"fold_id": 1, "events": 49, "lr_p": 0.40},
        {"fold_id": 2, "events": 55, "lr_p": 0.30},
        {"fold_id": 3, "events": 120, "lr_p": 0.02},
        {"fold_id": 4, "events": 10, "lr_p": 0.90},
    ]
    flagged = cd.filter_powered_folds(folds, merge=False)
    assert [f["powered"] for f in flagged] == [True, False, True, True, False]
    merged = cd.filter_powered_folds(folds, merge=True)
    assert all(f["events"] >= 50 for f in merged), merged
    assert all(f["powered"] for f in merged)
    # fold 1 merged into a neighbor, its underpowered lr_p is not counted
    assert all(f["lr_p"] is not None or "merged_from" in f for f in merged)
    # unrejection is judged strictly across powered folds
    tested = [f for f in merged if f["lr_p"] is not None]
    frac = cd.unrejected_powered_fraction(tested)
    assert frac == pytest.approx(0.0)


def test_powered_fold_kill_fires_on_null_market():
    """Constant-hazard LR on the compression effect, per fold, on a pure
    GARCH-t null: non-rejection in >= 30% of powered folds -> kill line 3."""
    ret, sigma = simulate_garch_t(1400, seed=5, **NULL_GARCH)
    spells = build_spells(ret, trailing_sigma_hat(ret),
                          compression="normalized")
    folds = []
    for fold_idx, chunk in enumerate(np.array_split(
            np.arange(len(spells)), 6)):
        sub = spells.iloc[chunk]
        p, _ = cd.constant_hazard_lr_pvalue(sub, ["compression"])
        folds.append({"fold_id": fold_idx, "events": int(sub["event"].sum()),
                      "lr_p": p})
    powered = cd.filter_powered_folds(folds, min_events=50)
    assert all(f["powered"] for f in powered)
    assert all(f["events"] >= 50 for f in powered)
    frac = cd.unrejected_powered_fraction(powered)
    assert frac >= 0.30
    results = _results(unrejected=frac)
    with pytest.raises(AssertionError, match="KILL LINE 3"):
        c1.enforce_kill_lines(results)


# ------------------------------------------------- kill line 1: concordance

def test_kill_line_1_concordance_floor_on_pure_noise():
    rng = np.random.default_rng(3)
    n = 5000
    x = rng.integers(0, 2, n).astype(float)
    ev = rng.random(n) < 0.05
    stop = np.where(ev, rng.integers(1, 25, n), 24).astype(float)
    df = pd.DataFrame({"start": 0.0, "stop": stop, "event": ev.astype(int),
                       "x": x, "hour": 0, "regime": 0})
    fit = cd.fit_cox(df, ["x"])
    c = cd.concordance(fit)
    assert c <= 0.52
    with pytest.raises(AssertionError, match="KILL LINE 1"):
        c1.enforce_kill_lines(_results(oof_concordance=c))


# ------------------------------------------ Test A: vol-tautology trap

NULL_GARCH = dict(alpha=0.15, beta_v=0.65)


def _garch_t_null_spells():
    ret, _ = simulate_garch_t(2000, seed=123, **NULL_GARCH)
    return build_spells(ret, trailing_sigma_hat(ret),
                        compression="normalized")


def test_kill_line_2_vol_tautology_on_pure_garch_t_null():
    """Test A: pure Student-t GARCH(1,1), no microstructure state. With
    trailing sigma_H in the model the compression HR 95% CI spans 1.0 ->
    the vol-tautology kill assert fires."""
    spells = _garch_t_null_spells()
    assert spells["event"].sum() >= 50
    fit = cd.fit_cox(spells, ["compression", "log_sigma"])
    hr, lo, hi = cd.hr_ci(fit, "compression")
    assert lo <= 1.0 <= hi, (lo, hi)
    with pytest.raises(AssertionError, match="KILL LINE 2"):
        c1.enforce_kill_lines(_results(tautology_hr_ci=(lo, hi)))


def test_kill_line_4_diurnal_artifact_dies_under_hod_stratification():
    """A compression effect that exists pooled but is pure session timing:
    it dies under hour-of-day stratification -> kill line 4 fires."""
    beta = np.array([0.0])          # true within-hour effect: none
    diurnal = 1.0 + 0.9 * np.sin(2 * np.pi * (np.arange(24) - 3) / 24)
    quiet = diurnal < 1.0

    def joint_fn(rng):
        h = int(rng.integers(0, 24))
        p_x = 0.80 if quiet[h] else 0.15
        x = np.array([1.0 if rng.random() < p_x else 0.0])
        return x, h, int(rng.integers(0, 2))

    def base_fn(h, r, u):
        return 0.10 * np.exp(-u / 6.0) if quiet[h] else 0.05

    df = simulate_ph_spells(
        8000, seed=17, beta_fn=lambda u: beta,
        base_fn=base_fn,
        x_fn=None, joint_fn=joint_fn,
        censor=lambda rng: rng.uniform(8, 24),
    )
    pooled = cd.fit_cox(df, ["x"])
    plo, phi = None, None
    strat = cd.fit_cox(df, ["x"], strata=["hour", "regime"])
    hr_p, plo, phi = cd.hr_ci(pooled, "x")
    hr_s, slo, shi = cd.hr_ci(strat, "x")
    assert not (plo <= 1.0 <= phi)          # apparent pooled effect
    assert slo <= 1.0 <= shi                # dies under stratification
    with pytest.raises(AssertionError, match="KILL LINE 4"):
        c1.enforce_kill_lines(_results(
            tautology_hr_ci=(plo, phi), stratified_hr_ci=(slo, shi)))


# ------------------------------------------ Test B: scale-invariance null

def _artifact_market():
    """Synthetic market carrying a calendar/volatility-clustering artifact:
    near-integrated GARCH vol (half-life far beyond the label horizon) on a
    diurnal sigma schedule. The compression flag then carries a REAL
    barrier-hit hazard effect (quiet now -> quiet later -> fewer sigma_H-
    scaled barrier touches) that hour-of-day stratification cannot remove —
    pure volatility clustering wearing a compression costume, with no
    microstructure state anywhere."""
    ret, sigma = simulate_garch_t(2600, seed=99, alpha=0.06, beta_v=0.93,
                                  diurnal_amp=0.6)
    sigma_hat = trailing_sigma_hat(ret)
    spells = build_spells(ret, sigma_hat, compression="normalized")
    return ret, sigma_hat, spells


def _compression_gap(spells):
    fit = cd.fit_cox(spells, ["compression", "log_sigma"])
    hr, lo, hi = cd.hr_ci(fit, "compression")
    return abs(float(np.log(hr))), (lo, hi)


def test_kill_line_5_scale_invariance_null_kills_artifacts():
    """Test B: the 1h block-bootstrapped sigma-standardized generator
    reproduces the observed compression gap within its 95% band -> the
    whole-layer scale-invariance kill fires."""
    ret, sigma_hat, spells = _artifact_market()
    gap, (lo, hi) = _compression_gap(spells)
    # the artifact is real on the raw path (CI excludes 1) ...
    assert not (lo <= 1.0 <= hi), (lo, hi, gap)
    # ... and hour-of-day stratification does NOT repair it (the artifact
    # is volatility clustering, not pure session timing), so the layer
    # reaches the scale-invariance null rather than kill line 4.
    strat = cd.fit_cox(spells, ["compression", "log_sigma"],
                       strata=["hour", "regime"])
    _, slo, shi = cd.hr_ci(strat, "compression")
    assert not (slo <= 1.0 <= shi), (slo, shi)

    rng = np.random.default_rng(2024)
    gaps = []
    for _ in range(100):
        r_star = block_bootstrap_returns(ret, sigma_hat, rng,
                                         block_len=PER_HOUR)
        star_spells = build_spells(r_star, trailing_sigma_hat(r_star),
                                   compression="normalized")
        g_star, _ = _compression_gap(star_spells)
        gaps.append(g_star)
    nl, nh = np.percentile(gaps, [2.5, 97.5])
    assert nl <= gap <= nh, (gap, nl, nh)
    with pytest.raises(AssertionError, match="KILL LINE 5"):
        c1.enforce_kill_lines(_results(
            tautology_hr_ci=(lo, hi),
            stratified_hr_ci=(slo, shi),
            scale_null_gap_ci95=(nl, nh), observed_gap=gap))


# ------------------------------------------------------------- control

def test_enforce_kill_lines_silent_when_all_pass():
    c1.enforce_kill_lines(_results(
        oof_concordance=0.58, tautology_hr_ci=(0.70, 0.90),
        unrejected=0.10, stratified_hr_ci=(0.72, 0.92),
        scale_null_gap_ci95=(0.10, 0.25), observed_gap=0.55))
