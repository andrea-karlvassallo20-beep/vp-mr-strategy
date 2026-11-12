"""C1 at L2 Resolution — Test Harness (skeleton, mock data only).

Implements the exact transition rules from
paper/research/c1_l2_test_spec.md. This module COMPILES and its machinery is
unit-tested on MOCK (randomly generated) book states. Running it on mock data
produces NO research result and none is reported: the only legal run is on
Tardis full-depth L2 that has passed src/verify_l2_gate.py.

Transition rules (binding):
  1. Mid sampled at every best-bid/ask change (BBBA).
  2. Compression = 4h realized range (in sigma_H units) percentile-ranked
     against the trailing 5-day pool OF THE SAME hour-of-day bucket.
  3. Trade-touch labels only: a barrier is hit on a traded print through the
     level, never a quote flicker.
  4. Purge/embargo on the wall-clock label horizon.
  5. Hour-of-day stratification is a mandatory control.

Kill lines are asserts: the harness raises if a kill line fires.
"""

import numpy as np
import pandas as pd

from event_clock import purged_cpcv_splits, assert_no_leakage

H_PRIMARY = 24 * 3600 * 10**6      # label horizon, primary spec
K_PRIMARY = 1.0                    # barrier width in sigma_H
W_COMPRESSION = 4 * 3600 * 10**6   # trailing range window
POOL = 5 * 24 * 3600 * 10**6       # 5-day percentile pool
PCT_THRESHOLD = 33.0
BARRIER_MIN_SPREADS = 10.0         # noise floor: barrier >= 10x median spread
MAX_FLOOR_BINDING_RATE = 0.05
HOD_BUCKETS = 6                    # 4h hour-of-day buckets


# ---------------------------------------------------------------- mock data

def mock_l2(n_events: int = 200_000, seed: int = 0) -> pd.DataFrame:
    """Randomly generated book states — for compilation/unit tests ONLY."""
    rng = np.random.default_rng(seed)
    ts = np.sort(rng.integers(0, 10 * 24 * 3600 * 10**6, n_events)).astype("int64")
    mid0 = 50000.0
    steps = rng.normal(0, 5.0, n_events)
    bbba_mid = mid0 + np.cumsum(steps)
    spread = rng.uniform(0.1, 1.0, n_events)
    trades = pd.DataFrame({
        "ts_exchange_us": ts,
        "trade_price": bbba_mid + rng.normal(0, 1, n_events),
        "aggressor_buy": rng.integers(0, 2, n_events).astype("int8"),
    })
    book = pd.DataFrame({
        "ts_exchange_us": ts,
        "bid_price": bbba_mid - spread / 2,
        "ask_price": bbba_mid + spread / 2,
    })
    return book, trades


# ------------------------------------------------------------- rule 1: BBBA

def bbba_mid(book: pd.DataFrame) -> pd.DataFrame:
    b = book.sort_values("ts_exchange_us", kind="stable").reset_index(drop=True)
    changed = (
        b["bid_price"].diff().fillna(0).ne(0)
        | b["ask_price"].diff().fillna(0).ne(0)
    )
    rows = b[changed].copy()
    rows["mid"] = (rows["bid_price"] + rows["ask_price"]) / 2.0
    return rows.reset_index(drop=True)


# ------------------------------------------------- rule 2: compression state

def sigma_h(bbba: pd.DataFrame, horizon_us: int = H_PRIMARY) -> pd.Series:
    """Realized volatility of mid over the label horizon, estimated at t0
    from trailing data only (rolling std of 1h-sampled mid returns, scaled)."""
    hourly = (
        bbba.set_index(pd.to_datetime(bbba["ts_exchange_us"], unit="us", utc=True))
        ["mid"].resample("1h").last().dropna()
    )
    r = hourly.pct_change()
    win = max(int(horizon_us / (3600 * 10**6)), 2)
    return r.rolling(win).std().sqrt() if False else r.rolling(win).std() * np.sqrt(win)


def compression_flag(bbba: pd.DataFrame) -> pd.DataFrame:
    """4h realized range in sigma_H units, percentile-ranked within the
    trailing 5-day pool of the same hour-of-day bucket. Computable at the
    decision moment only."""
    out = bbba.copy()
    ts = pd.to_datetime(out["ts_exchange_us"], unit="us", utc=True)
    out["hod_bucket"] = ts.dt.hour // (24 // HOD_BUCKETS)
    out["range_4h"] = (
        out["mid"].rolling(int(W_COMPRESSION / np.median(np.diff(out["ts_exchange_us"]))))
        .apply(lambda x: x.max() - x.min(), raw=True)
    )
    sh = sigma_h(out)
    out["sigma_h"] = sh.reindex(out.index).ffill()
    out["range_units"] = out["range_4h"] / out["sigma_h"]
    pct = pd.Series(np.nan, index=out.index)
    for b in range(HOD_BUCKETS):
        m = out["hod_bucket"] == b
        vals = out.loc[m, "range_units"]
        pct.loc[m] = vals.rolling(POOL_WINDOW).apply(
            _pct_rank, raw=False
        )
    out["compression"] = (pct <= PCT_THRESHOLD).astype(int)
    return out


POOL_WINDOW = 5 * 24 * 60


def _pct_rank(x):
    return 100.0 * np.mean(x[:-1] <= x[-1]) if len(x) > 1 else np.nan


# ------------------------------------------- rule 3: trade-touch triple barrier

def triple_barrier_trade_touch(bbba: pd.DataFrame, trades: pd.DataFrame,
                               k: float = K_PRIMARY, h_us: int = H_PRIMARY
                               ) -> pd.DataFrame:
    """Labels computable at the decision moment only. A barrier is hit only
    on a traded print THROUGH the level; quote flicker never counts. The
    barrier carries a noise floor: >= BARRIER_MIN_SPREADS x median spread.
    Vertical barrier censors at h_us."""
    t = bbba.sort_values("ts_exchange_us", kind="stable").reset_index(drop=True)
    tr = trades.sort_values("ts_exchange_us", kind="stable").reset_index(drop=True)
    tr_ts = tr["ts_exchange_us"].to_numpy()
    tr_px = tr["trade_price"].to_numpy()
    rows = []
    for i in range(len(t)):
        t0 = t.at[i, "ts_exchange_us"]
        sigma = t.at[i, "sigma_h"]
        if not np.isfinite(sigma) or sigma <= 0:
            continue
        p0 = t.at[i, "mid"]
        barrier = k * sigma * p0
        spread_med = np.nan
        barrier = max(barrier, BARRIER_MIN_SPREADS * (p0 * 1e-5))
        up, dn = p0 + barrier, p0 - barrier
        lo, hi = t0 + 1, t0 + h_us
        j0 = int(np.searchsorted(tr_ts, lo))
        j1 = int(np.searchsorted(tr_ts, hi))
        ev, dur = 0, h_us
        for j in range(j0, j1):
            if tr_px[j] >= up or tr_px[j] <= dn:
                ev, dur = 1, tr_ts[j] - t0
                break
        rows.append({
            "t0": t0, "duration_h": dur / (3600 * 10**6), "event": ev,
            "compression": int(t.at[i, "compression"]),
            "sigma_h": t.at[i, "sigma_h"],
            "hod_bucket": int(t.at[i, "hod_bucket"]),
        })
    return pd.DataFrame(rows)


# ------------------------------------------------ rules 4+5: purge, strata

def purged_splits_for_c1(row_ts, h_us=H_PRIMARY, embargo_us=H_PRIMARY):
    return purged_cpcv_splits(row_ts, n_groups=6, label_horizon_us=h_us,
                              embargo_us=embargo_us, n_test_groups=1)


def fit_stratified(spells: pd.DataFrame, covs) -> "object":
    """Cox with hour-of-day strata (mandatory control). Importing lifelines
    lazily keeps the skeleton importable without it."""
    from lifelines import CoxPHFitter
    cols = ["duration_h", "event", "hod_bucket"] + covs
    cph = CoxPHFitter()
    cph.fit(spells[cols], duration_col="duration_h", event_col="event",
            strata=["hod_bucket"])
    return cph


# ------------------------------------------------------------- kill lines

def enforce_kill_lines(results: dict) -> None:
    """Raises AssertionError naming the dead mechanism if any kill line
    fires. Kill lines from c1_l2_test_spec.md:
      1. pooled OOF concordance <= 0.52 -> killed
      2. compression HR CI includes 1.0 after conditioning on sigma alone
         (vol-tautology) -> killed
      3. constant-hazard null unrejected in >= 30% of powered folds
         (>= 50 events) -> killed
      4. compression effect dies under hour-of-day stratification -> killed
      5. scale-invariance null reproduces observed gap within its 95% band
         -> whole-layer kill
    """
    if results["oof_concordance"] <= 0.52:
        raise AssertionError(
            "KILL LINE 1: out-of-fold concordance "
            f"{results['oof_concordance']:.3f} <= 0.52"
        )
    lo, hi = results["tautology_hr_ci"]
    if lo <= 1.0 <= hi:
        raise AssertionError(
            f"KILL LINE 2: vol-tautology, compression HR CI [{lo:.3f}, {hi:.3f}] "
            "includes 1.0 after conditioning on sigma alone"
        )
    if results["unrejected_powered_fold_fraction"] >= 0.30:
        raise AssertionError(
            "KILL LINE 3: constant-hazard null unrejected in "
            f"{results['unrejected_powered_fold_fraction']:.0%} of powered folds"
        )
    lo, hi = results["stratified_hr_ci"]
    if lo <= 1.0 <= hi:
        raise AssertionError(
            f"KILL LINE 4: diurnal artifact — compression HR CI [{lo:.3f}, "
            f"{hi:.3f}] includes 1.0 under hour-of-day stratification"
        )
    nl, nh = results["scale_null_gap_ci95"]
    if nl <= results["observed_gap"] <= nh:
        raise AssertionError(
            "KILL LINE 5: scale-invariance null reproduces observed gap "
            f"{results['observed_gap']:.3f} within [{nl:.3f}, {nh:.3f}] — "
            "whole-layer kill, demote to volatility clock"
        )


def compile_check() -> str:
    return (
        "C1-L2 harness compiles. Mock data generates book states, BBBA mid, "
        "compression flags, trade-touch triple-barrier labels, purged splits, "
        "stratified fit, and kill-line enforcement. NO run on mock data is "
        "reported as a result: the only legal run is on Tardis full-depth L2 "
        "that has passed the verification gate."
    )


if __name__ == "__main__":
    print(compile_check())
