"""Adversarial null-simulation tests proving every pre-declared kill line in
src/c1_l2_test.py actually fires on SYNTHETIC null markets, BEFORE any real
L2 data is ingested. Mock data only: no result here is research output.

Covered kill lines (paper/research/c1_l2_test_spec.md):
  1. concordance floor (pooled OOF concordance <= 0.52)
  2. vol-tautology (compression HR CI includes 1.0 once trailing sigma_H
     is in the model) — Test A, pure Student-t GARCH(1,1) null
  3. constant-hazard null unrejected in >= 30% of POWERED folds
  4. compression effect dies under hour-of-day stratification
  5. scale-invariance null reproduces the observed gap within its 95%
     band — Test B, 1h block-bootstrapped sigma-standardized generator
plus the Schoenfeld residual PH audit with automatic hour-of-day/regime
stratification and its unresolved-PH kill assert.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import c1_l2_test as c1
import cox_diagnostics as cdx

GARCH_KW = {"omega": 2e-6, "alpha": 0.08, "beta": 0.90, "nu": 5.0}


def spells_from_path(returns, sigma_hat, k=6.0, h=24, step=4, warmup=240,
                     pool=5 * 24, pct=33.0):
    """C1-style synthetic null market: barrier = k x trailing sigma_H
    (trade-touch on a print through the level), vertical censoring at h,
    compression = trailing-percentile rank of sigma_H against the 5-day
    pool of the same hour-of-day bucket. No microstructure state."""
    n = len(returns)
    rows = []
    for t0 in range(warmup, n - h, step):
        win = sigma_hat[t0 - pool:t0]
        if not np.isfinite(win).all() or not np.isfinite(sigma_hat[t0]) or sigma_hat[t0] <= 0:
            continue
        rank = 100.0 * np.mean(win <= sigma_hat[t0])
        comp = 1.0 if rank <= pct else 0.0
        barrier = k * sigma_hat[t0]
        cum = np.cumsum(returns[t0 + 1:t0 + 1 + h])
        hit = np.nonzero(np.abs(cum) >= barrier)[0]
        ev, dur = (1, int(hit[0]) + 1) if len(hit) else (0, h)
        rows.append({
            "start": 0.0, "stop": float(dur), "event": ev,
            "compression": comp, "lsig": float(np.log(sigma_hat[t0])),
            "hod": t0 % 24, "regime": 0,
        })
    df = pd.DataFrame(rows)
    df["lsig"] = (df["lsig"] - df["lsig"].mean()) / (df["lsig"].std() + 1e-12)
    return df


def passing_results(**overrides):
    """Results dict in which no kill line fires; individual tests override
    exactly the key their kill line reads, so each assert proves that the
    targeted pre-declared line is what raises."""
    base = {
        "oof_concordance": 0.55,
        "tautology_hr_ci": (1.2, 1.5),
        "unrejected_powered_fold_fraction": 0.10,
        "stratified_hr_ci": (1.2, 1.5),
        "scale_null_gap_ci95": (10.0, 12.0),
        "observed_gap": 0.5,
    }
    base.update(overrides)
    return base


# ------------------------------------------------- estimator cross-check

def test_fit_cox_counting_matches_lifelines():
    lifelines = pytest.importorskip("lifelines")
    from lifelines import CoxPHFitter
    rng = np.random.default_rng(2)
    n = 3000
    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    dur = rng.exponential(1.0 / (0.3 * np.exp(0.5 * x1 - 0.3 * x2)))
    cen = rng.uniform(0, 12, n)
    sp = pd.DataFrame({
        "start": 0.0, "stop": np.minimum(dur, cen), "event": dur <= cen,
        "x1": x1, "x2": x2,
    })
    mine = cdx.fit_cox_counting(sp, ["x1", "x2"])
    cph = CoxPHFitter().fit(sp[["stop", "event", "x1", "x2"]],
                            duration_col="stop", event_col="event")
    assert np.allclose(mine["beta"], cph.params_.values, atol=1e-6)
    assert np.allclose(mine["se"], cph.standard_errors_.values, atol=1e-6)
    assert mine["loglik"] == pytest.approx(cph.log_likelihood_, abs=1e-6)
    null = cdx.fit_cox_counting(sp, [])
    c0 = CoxPHFitter().fit(sp[["stop", "event"]], duration_col="stop", event_col="event")
    assert null["loglik"] == pytest.approx(c0.log_likelihood_, abs=1e-6)
    stat, p = cdx.loglik_ratio(mine, null)
    ref = 2.0 * (cph.log_likelihood_ - c0.log_likelihood_)
    assert stat == pytest.approx(ref, abs=1e-6)
    assert 0.0 < p < 1e-100


# --------------------------------------------------- kill line 1

def test_kill_line_1_concordance_floor_fires():
    with pytest.raises(AssertionError, match="KILL LINE 1"):
        c1.enforce_kill_lines(passing_results(oof_concordance=0.51))
    with pytest.raises(AssertionError, match="KILL LINE 1"):
        c1.enforce_kill_lines(passing_results(oof_concordance=0.52))


def test_no_kill_line_fires_on_passing_results():
    c1.enforce_kill_lines(passing_results())


# ------------------------------------- Test A: vol-tautology trap (kill 2)

def test_kill_line_2_vol_tautology_trap_on_pure_garch_null():
    """Test A: pure Student-t GARCH(1,1) returns, no microstructure state.
    Once the trailing sigma_H level is in the model, the compression HR
    95% CI spans 1.0 — compression adds nothing beyond the volatility it
    was built from — and the pre-declared vol-tautology kill fires."""
    r, sigma = cdx.simulate_garch_t(6000, seed=7, **GARCH_KW)
    sp = spells_from_path(r, sigma)
    assert set(sp["compression"].unique()) == {0.0, 1.0}
    fit_alone = cdx.fit_cox_counting(sp, ["compression"])
    fit_with_sigma = cdx.fit_cox_counting(sp, ["compression", "lsig"])
    lo, hi = cdx.hr_ci(fit_with_sigma, "compression")
    assert lo <= 1.0 <= hi
    effect_alone = abs(float(fit_alone["beta"][0]))
    effect_conditional = abs(float(fit_with_sigma["beta"][0]))
    assert effect_conditional <= effect_alone
    with pytest.raises(AssertionError, match="KILL LINE 2"):
        c1.enforce_kill_lines(passing_results(tautology_hr_ci=(lo, hi)))


# --------------------------- kill line 3: powered folds, constant hazard

def test_filter_powered_folds_merges_and_flags():
    folds = [{"fold": i, "events": e} for i, e in
             enumerate([30, 60, 40, 55, 20, 70, 10])]
    sel = cdx.filter_powered_folds(folds, min_events=50)
    assert [f["events"] for f in sel["powered"]] == [90, 95, 100]
    assert all(f["events"] >= 50 for f in sel["powered"])
    assert sel["flagged"] == []
    assert {m["absorbed"] for m in sel["merged"]} == {0, 2, 4, 6}


def test_filter_powered_folds_flags_lone_underpowered_fold():
    folds = [{"fold": 0, "events": 20}]
    sel = cdx.filter_powered_folds(folds, min_events=50)
    assert sel["powered"] == []
    assert sel["flagged"][0]["fold"] == 0


def test_unrejected_fraction_excludes_underpowered_folds():
    """Non-rejection in an underpowered fold is a power failure, not
    evidence: the fold is merged into its neighbor and its non-rejection
    never enters the kill-line count."""
    fold_stats = [
        {"fold": 0, "events": 20, "lr_p": 0.9},
        {"fold": 1, "events": 60, "lr_p": 0.001},
        {"fold": 2, "events": 55, "lr_p": 0.001},
    ]
    frac, sel = cdx.unrejected_powered_fraction(fold_stats)
    assert frac == 0.0
    assert len(sel["merged"]) == 1 and sel["merged"][0]["absorbed"] == 0
    assert [f["events"] for f in sel["powered"]] == [80, 55]
    c1.enforce_kill_lines(
        passing_results(unrejected_powered_fold_fraction=frac))


def test_kill_line_3_constant_hazard_unrejected_in_powered_folds():
    """Placebo compression (permuted within hour-of-day, so the diurnal
    marginal is preserved but all event alignment is destroyed): the
    constant-hazard null goes unrejected in >= 30% of powered folds and
    the pre-declared kill fires."""
    r, sigma = cdx.simulate_garch_t(12000, seed=7, **GARCH_KW)
    sp = spells_from_path(r, sigma).reset_index(drop=True)
    rng = np.random.default_rng(9)
    comp = sp["compression"].to_numpy().copy()
    for h in range(24):
        m = (sp["hod"] == h).to_numpy()
        comp[m] = rng.permutation(comp[m])
    sp["compression"] = comp
    fold_stats = []
    for g, ix in enumerate(np.array_split(sp.index, 6)):
        te = sp.iloc[ix]
        full = cdx.fit_cox_counting(te, ["compression"])
        null = cdx.fit_cox_counting(te, [])
        _, p = cdx.loglik_ratio(full, null)
        fold_stats.append({"fold": g, "events": int(te["event"].sum()), "lr_p": p})
    assert all(f["events"] >= 50 for f in fold_stats)
    frac, sel = cdx.unrejected_powered_fraction(fold_stats)
    assert frac >= 0.30
    with pytest.raises(AssertionError, match="KILL LINE 3"):
        c1.enforce_kill_lines(
            passing_results(unrejected_powered_fold_fraction=frac))
    with pytest.raises(AssertionError, match="KILL LINE 3"):
        cdx.enforce_constant_hazard_kill(fold_stats)


# --------------------------- kill line 4: diurnal artifact stratification

def _diurnal_artifact_spells(seed=5, m=6000):
    rng = np.random.default_rng(seed)
    hod = rng.integers(0, 24, m)
    active = np.isin(hod, [13, 14, 15, 16])
    quiet = ~active
    comp = np.where(rng.random(m) < 0.15, ~quiet, quiet)
    lam = np.where(active, 0.8, 0.25)
    dur = rng.exponential(1.0 / lam)
    cen = rng.uniform(0, 8, m)
    return pd.DataFrame({
        "start": 0.0, "stop": np.minimum(dur, cen), "event": dur <= cen,
        "compression": comp.astype(float), "hod": hod,
        "regime": rng.integers(0, 2, m),
    })


def test_kill_line_4_compression_dies_under_hour_stratification():
    """Session timing, not liquidity: the hazard is driven by UTC hour and
    compression is merely an hour proxy, so the effect is significant
    unstratified and dies under hour-of-day stratification."""
    sp = _diurnal_artifact_spells()
    unstrat = cdx.fit_cox_counting(sp, ["compression"])
    strat = cdx.fit_cox_counting(sp, ["compression"], strata_cols=["hod", "regime"])
    lo_u, hi_u = cdx.hr_ci(unstrat, "compression")
    lo_s, hi_s = cdx.hr_ci(strat, "compression")
    assert not (lo_u <= 1.0 <= hi_u)
    assert lo_s <= 1.0 <= hi_s
    with pytest.raises(AssertionError, match="KILL LINE 4"):
        c1.enforce_kill_lines(passing_results(stratified_hr_ci=(lo_s, hi_s)))


# ------------------- Test B: scale-invariance null (kill 5, whole layer)

def test_kill_line_5_scale_invariance_null_reproduces_artifact_gap():
    """Test B: a market whose compression gap is a calendar /
    volatility-clustering artifact (diurnal sigma pattern on top of
    GARCH clustering). The 1h block-bootstrapped sigma-standardized
    generator r*_t = sigma_hat(t) * z*_t reproduces the observed gap
    inside its 95% band, so the pre-declared whole-layer kill fires."""
    n = 6000
    hod_pattern = 1.0 + 0.6 * np.sin(2 * np.pi * np.arange(n) / 24)
    r0, s0 = cdx.simulate_garch_t(n, seed=11, **GARCH_KW)
    sigma_obs = s0 * hod_pattern
    r_obs = sigma_obs * (r0 / s0)
    sp_obs = spells_from_path(r_obs, sigma_obs)
    fit_obs = cdx.fit_cox_counting(sp_obs, ["compression"])
    gap_obs = abs(float(fit_obs["beta"][0]))
    lo_hr, hi_hr = cdx.hr_ci(fit_obs, "compression")
    assert not (lo_hr <= 1.0 <= hi_hr)
    nulls = cdx.sigma_standardized_block_null(r_obs, sigma_obs, block=24,
                                              n_rep=40, seed=3)
    gaps = []
    for i in range(nulls.shape[0]):
        sp_null = spells_from_path(nulls[i], sigma_obs)
        fit_null = cdx.fit_cox_counting(sp_null, ["compression"])
        gaps.append(abs(float(fit_null["beta"][0])))
    nl, nh = (float(x) for x in np.percentile(gaps, [2.5, 97.5]))
    assert nl <= gap_obs <= nh
    with pytest.raises(AssertionError, match="KILL LINE 5"):
        c1.enforce_kill_lines(passing_results(
            scale_null_gap_ci95=(nl, nh), observed_gap=gap_obs))


def test_sigma_standardized_block_null_preserves_sigma_hat_marginal():
    r0, s0 = cdx.simulate_garch_t(2000, seed=4, **GARCH_KW)
    nulls = cdx.sigma_standardized_block_null(r0, s0, block=24, n_rep=5, seed=1)
    assert nulls.shape == (5, 2000)
    std = np.std(nulls / s0, axis=1)
    ref = np.std(r0 / s0)
    assert np.all(np.abs(std - ref) < 0.1 * ref)


# ---------------------- Schoenfeld PH audit + automatic stratification

def _tv_interval_rows(n_sub, b_fun, seed, t_max=24, lam0=0.25):
    """Counting-process spells: unit (t, t+1] intervals, one subject-level
    covariate x, covariate effect b(t) that may vary with elapsed time."""
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n_sub):
        x = rng.normal()
        regime = int(rng.integers(0, 2))
        for t in range(t_max):
            lam = lam0 * np.exp(b_fun(t) * x)
            ev = rng.random() < 1.0 - np.exp(-lam)
            rows.append({"start": float(t), "stop": float(t + 1),
                         "event": bool(ev), "x": x, "hod": t % 24,
                         "regime": regime})
            if ev:
                break
    return pd.DataFrame(rows)


def test_schoenfeld_passes_when_ph_holds():
    sp = _tv_interval_rows(1500, lambda t: 0.5, seed=1)
    res = cdx.enforce_ph_rule(sp, ["x"])
    assert res["ph_ok"] is True
    assert res["stratified"] is False
    assert res["test"]["covariate_p"]["x"] > 0.05


def test_ph_violation_resolved_by_automatic_stratification():
    """Session-timing confound: each subject's baseline hazard follows a
    diurnal clock anchored at its UTC entry hour, and x is correlated
    with that hour. The pooled Schoenfeld audit flags p < 0.05;
    stratifying baseline hazards by hour-of-day and Layer 1 regime
    resolves it, so no kill is raised."""
    rng = np.random.default_rng(2)
    rows = []
    for _ in range(2500):
        h = int(rng.integers(0, 24))
        active = h in (13, 14, 15, 16)
        x = (-0.7 if not active else 0.7) + rng.normal(0, 0.5)
        regime = int(rng.integers(0, 2))
        for t in range(48):
            clock = (h + t) % 24
            lam = (0.5 if clock in (13, 14, 15, 16) else 0.12) * np.exp(0.5 * x)
            ev = rng.random() < 1.0 - np.exp(-lam)
            rows.append({"start": float(t), "stop": float(t + 1),
                         "event": bool(ev), "x": x, "hod": h,
                         "regime": regime})
            if ev:
                break
    sp = pd.DataFrame(rows)
    res = cdx.enforce_ph_rule(sp, ["x"])
    assert res["stratified"] is True
    assert res["pooled_test"]["covariate_p"]["x"] < 0.05
    assert res["test"]["covariate_p"]["x"] > 0.01


def test_unresolved_ph_kill_assert_fires_when_stratification_cannot_fix():
    """A covariate effect that flips sign within the hour cannot be fixed
    by hour-of-day/regime stratification: the unresolved-PH kill assert
    must fire (Schoenfeld p < 0.05 pooled AND p < 0.01 stratified)."""
    sp = _tv_interval_rows(1500, lambda t: 1.0 if (t % 2) == 0 else -1.0, seed=3)
    pooled = cdx.schoenfeld_ph_test(sp, ["x"])
    assert pooled["covariate_p"]["x"] < 0.05
    strat = cdx.schoenfeld_ph_test(sp, ["x"], strata_cols=["hod", "regime"])
    assert strat["covariate_p"]["x"] < 0.01
    with pytest.raises(AssertionError, match="unresolved proportional-hazards"):
        cdx.enforce_ph_rule(sp, ["x"])
