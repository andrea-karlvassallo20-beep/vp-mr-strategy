"""Pre-L2 taker-only falsification harness — Claims T3, T1, T2.

DATA FLAG (binding, printed with every output): the input is Binance
BTCUSDT USDS-M aggTrades = TAKER-SIDE EXECUTED PRINTS ONLY. There is no
visibility into resting limit orders, passive cancellations, queue depth,
or iceberg replenishment. Every feature here is taker-only; nothing in
this run can speak for the passive side of the book (that is C1-L2/C5/C6,
blocked on the L0 gate).

Pre-declared test grid (fixed before any run, not re-tuned after a null):
- decision rows: trade-clock (state-change) minutes thinned to <= 1 per
  DECISION_MIN wall-clock minutes; labels are trade-touch triple barriers
  (a traded print through the level; quote flicker never counts) with a
  hard noise floor barrier >= BARRIER_MIN_SPREADS x trailing median spread
  proxy (taker-only proxy: median |trade-to-trade price step|), primary
  k=1.0 sigma_H, label horizon H=24h wall-clock;
- compression: trailing 4h realized range of the trade price in sigma_H
  units, percentile-ranked (<=33) against the trailing 5-day pool of the
  same hour-of-day bucket (6 buckets);
- survival folds: event_clock.purged_cpcv_splits, 6 contiguous wall-clock
  groups, purge on the wall-clock label horizon, embargo = H; assert 0
  index intersections and 0 label-window overlaps across all folds;
- macro: src/macro_censor.py right-censors spells entering scheduled
  data/macro_timeline.csv windows (ex-ante columns only; surprise_note is
  dropped and asserted empty).

Kill lines are RAISING asserts (c1_l2_test.enforce_kill_lines for T1).
The runner executes T3 -> T1 -> T2 in order and STOPS at the first kill,
naming the dead mechanism. No pivoting to surviving variants.
"""

import argparse
import gc
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import c1_l2_test as c1
from event_clock import purged_cpcv_splits, assert_no_leakage
from features import fit_hawkes
import macro_censor

DATA_FLAG = ("DATA FLAG: aggTrades = taker-side executed prints only; no resting "
             "quote additions/cancellations, no queue depth, no iceberg visibility. "
             "All features in this run are TAKER-ONLY.")

H_US = c1.H_PRIMARY                    # 24h label horizon (wall-clock)
EMBARGO_US = H_US
K = c1.K_PRIMARY                       # barrier width in sigma_H units
DECISION_MIN = 15                      # decision grid: <=1 row / 15 min wall-clock
N_GROUPS = 6
W_MIN = int(c1.W_COMPRESSION // (60 * 10**6))             # 4h in minutes
POOL_MIN = int(c1.POOL // (60 * 10**6) // c1.HOD_BUCKETS)  # 5d pool per HOD bucket
PCT_THRESHOLD = c1.PCT_THRESHOLD
HOD_BUCKETS = c1.HOD_BUCKETS
VPIN_BUCKET = 2000
VPIN_EWMA = 50
NULL_REPS = 40
NULL_BLOCK_MIN = 60
HAWKES_CAP = 20_000
NULL_INTERVAL = (0.497, 0.513)

MIN_US = 60 * 10**6
HOUR_US = 3600 * 10**6


# ---------------------------------------------------------------- data build

def _minute_frame(files):
    """Global 1-minute grid from daily aggTrades parquet: last price, trade
    count, and per-minute median |trade-to-trade price step| (spread proxy)."""
    parts = []
    for f in files:
        t = pd.read_parquet(f, columns=["ts_exchange_us", "price"])
        t["min"] = (t["ts_exchange_us"] // MIN_US) * MIN_US
        d = t["price"].diff().abs().where(lambda s: s > 0)
        g = t.groupby("min")
        parts.append(pd.DataFrame({
            "price": g["price"].last(),
            "n_trades": g.size(),
            "med_dp": d.groupby(t["min"]).median(),
        }).reset_index())
    M = pd.concat(parts, ignore_index=True).sort_values("min").reset_index(drop=True)
    return M


def _add_state(M: pd.DataFrame) -> pd.DataFrame:
    """Causal state on the minute grid: sigma_h, compression, time-in-comp,
    trades/min, spread proxy. Trailing windows only."""
    M = M.copy()
    ts = pd.to_datetime(M["min"], unit="us", utc=True)
    M["hod"] = ts.dt.hour // (24 // HOD_BUCKETS)
    hourly = M.set_index(ts)["price"].resample("1h").last().dropna()
    r = hourly.pct_change()
    sigma_h = r.rolling(H_US // HOUR_US).std() * np.sqrt(H_US // HOUR_US)
    M["sigma_h"] = sigma_h.reindex(ts, method="ffill").to_numpy()
    M["range_4h"] = M["price"].rolling(W_MIN).max() - M["price"].rolling(W_MIN).min()
    M["range_units"] = (M["range_4h"] / M["sigma_h"].replace(0, np.nan)).to_numpy()
    pct = np.full(len(M), np.nan)
    for b in range(HOD_BUCKETS):
        m = (M["hod"] == b).to_numpy()
        pct[m] = (pd.Series(M["range_units"][m])
                  .rolling(POOL_MIN, min_periods=POOL_MIN // 2)
                  .rank(pct=True).to_numpy() * 100.0)
    M["compression"] = (pct <= PCT_THRESHOLD).astype("int8")
    comp = M["compression"].to_numpy()
    run = (pd.Series(comp) != pd.Series(comp).shift()).cumsum().to_numpy()
    tic = pd.Series(np.arange(len(M))).groupby(run).cumcount().to_numpy()
    M["time_in_comp_min"] = np.where(comp == 1, tic, 0.0)
    M["trades_per_min"] = M["n_trades"].rolling(60, min_periods=1).sum() / 60.0
    M["med_spread"] = M["med_dp"].rolling(60, min_periods=5).median().to_numpy()
    return M


def _file_day(f: Path) -> pd.Timestamp:
    return pd.Timestamp(f.stem.split("-aggTrades-")[1], tz="UTC")


def _vpin_np(ts, size, ab, bucket, span, t0):
    """Trade-count-bucket VPIN (EWMA) mapped to decision times. numpy version
    of features.vpin_trade_buckets to keep the per-day chunk memory-lean."""
    n = (len(ts) // bucket) * bucket
    g = np.arange(n) // bucket
    buy = np.where(ab[:n] == 1, size[:n], 0.0)
    sell = np.where(ab[:n] == 0, size[:n], 0.0)
    bv = np.bincount(g, weights=buy)
    sv = np.bincount(g, weights=sell)
    imb = np.abs(bv - sv) / np.maximum(bv + sv, 1e-12)
    v = pd.Series(imb).ewm(span=span).mean().to_numpy()
    bt = ts[:n].reshape(-1, bucket)[:, -1]
    idx = np.maximum(np.searchsorted(bt, t0, side="right") - 1, 0)
    return v[idx]


def _label_chunk(tr_ts, tr_px, dec: pd.DataFrame) -> pd.DataFrame:
    """Trade-touch triple-barrier labels for decision rows `dec`, using the
    chunk's trades for the forward window (chunk spans dec range + H_US)."""
    t0 = dec["t0_us"].to_numpy()
    p0 = dec["price"].to_numpy()
    sig = dec["sigma_h"].to_numpy()
    spread = dec["med_spread"].to_numpy()
    barrier = np.maximum(K * sig * p0, c1.BARRIER_MIN_SPREADS * spread)
    barrier = np.where(np.isfinite(barrier) & (barrier > 0), barrier, np.nan)
    up, dn = p0 + barrier, p0 - barrier
    j0 = np.searchsorted(tr_ts, t0, side="right")
    j1 = np.searchsorted(tr_ts, t0 + H_US, side="left")
    dur = np.full(len(t0), H_US, dtype="int64")
    ev = np.zeros(len(t0), dtype="int8")
    side = np.zeros(len(t0), dtype="int8")  # 1 up touch, -1 down touch
    for i in range(len(t0)):
        if not np.isfinite(up[i]):
            continue
        a, b = j0[i], j1[i]
        if a >= b:
            continue
        seg = tr_px[a:b]
        iu = int(np.argmax(seg >= up[i]))
        idn = int(np.argmax(seg <= dn[i]))
        has_u = bool(seg[iu] >= up[i])
        has_d = bool(seg[idn] <= dn[i])
        if has_u and (not has_d or iu <= idn):
            ev[i], side[i], dur[i] = 1, 1, tr_ts[a + iu] - t0[i]
        elif has_d:
            ev[i], side[i], dur[i] = 1, -1, tr_ts[a + idn] - t0[i]
    out = dec.copy()
    out["duration_us"] = dur
    out["event"] = ev
    out["touch_side"] = side
    out["horizon_us"] = H_US
    out["n_trades_spell"] = (np.searchsorted(tr_ts, t0 + dur, side="left")
                             - j0).astype("int64")
    return out


def build_spells(data_dir: Path, timeline_path: Path, cache_dir: Path):
    files = sorted(Path(data_dir).glob("*.parquet"))
    assert files, f"no aggTrades parquet under {data_dir}"
    cache_dir.mkdir(parents=True, exist_ok=True)
    sp_cache = cache_dir / "taker_spells.parquet"
    min_cache = cache_dir / "taker_minute.parquet"
    haw_cache = cache_dir / "taker_hawkes_samples.parquet"
    if sp_cache.exists() and min_cache.exists() and haw_cache.exists():
        print("loading cached spells/minute/hawkes-sample frames", flush=True)
        return (pd.read_parquet(sp_cache), pd.read_parquet(min_cache),
                pd.read_parquet(haw_cache))

    print(f"building minute grid from {len(files)} daily files ...", flush=True)
    M = _add_state(_minute_frame(files))
    M.to_parquet(min_cache, index=False)

    t0_all = M["min"].to_numpy()
    keep = (t0_all - t0_all[0]) % (DECISION_MIN * MIN_US) == 0
    dec = M[keep].copy()
    dec["t0_us"] = dec["min"]

    print("sampling per-day per-bucket trade slices for Hawkes fits ...",
          flush=True)
    import pyarrow as pa
    import pyarrow.parquet as pq
    day_cap = 10_000  # per (day, HOD bucket); fold fits cap further at HAWKES_CAP
    schema = pa.schema([("ts_exchange_us", pa.int64()),
                        ("aggressor_buy", pa.int8()), ("hod", pa.int8())])
    with pq.ParquetWriter(haw_cache, schema) as w:
        for f in files:
            t = pd.read_parquet(f, columns=["ts_exchange_us", "aggressor_buy"])
            ts = t["ts_exchange_us"].to_numpy()
            ab = t["aggressor_buy"].to_numpy()
            hod = (ts // HOUR_US) % 24 // (24 // HOD_BUCKETS)
            for b in range(HOD_BUCKETS):
                idx = np.flatnonzero(hod == b)[:day_cap]
                if len(idx):
                    w.write(pa.table({
                        "ts_exchange_us": ts[idx],
                        "aggressor_buy": ab[idx].astype("int8"),
                        "hod": np.full(len(idx), b, dtype="int8"),
                    }))
            del t, ts, ab, hod
            gc.collect()
    haw = pd.read_parquet(haw_cache)
    haw = haw.sort_values("ts_exchange_us").reset_index(drop=True)
    print(f"  hawkes samples: {len(haw):,} rows", flush=True)

    print("labeling trade-touch triple barriers (per-day chunks) ...", flush=True)
    tl = macro_censor.load_timeline(timeline_path)
    windows = macro_censor.macro_windows(tl)
    day0 = pd.to_datetime(M["min"].iloc[0], unit="us", utc=True).normalize()
    dayN = pd.to_datetime(M["min"].iloc[-1], unit="us", utc=True).normalize()
    file_days = [(f, _file_day(f)) for f in files]
    spells = []
    rng = np.random.default_rng(20261115)
    d = day0
    while d <= dayN:
        nxt = d + pd.Timedelta(days=2)  # right carry covers the 24h label horizon
        chunk_files = [f for f, fd in file_days if d <= fd <= nxt]
        ts_l, px_l, sz_l, ab_l = [], [], [], []
        for f in chunk_files:
            t = pd.read_parquet(f)
            ts_l.append(t["ts_exchange_us"].to_numpy())
            px_l.append(t["price"].to_numpy())
            sz_l.append(t["size"].to_numpy())
            ab_l.append(t["aggressor_buy"].to_numpy())
            del t
        gc.collect()
        tr_ts = np.concatenate(ts_l)
        tr_px = np.concatenate(px_l)
        tr_sz = np.concatenate(sz_l)
        tr_ab = np.concatenate(ab_l)
        del ts_l, px_l, sz_l, ab_l
        d_lo = int(d.value // 1000)
        d_hi = int((d + pd.Timedelta(days=1)).value // 1000)
        dsel = dec[(dec["t0_us"] >= d_lo) & (dec["t0_us"] < d_hi)]
        if len(dsel):
            lab = _label_chunk(tr_ts, tr_px, dsel)
            lab["vpin_t0"] = _vpin_np(tr_ts, tr_sz, tr_ab, VPIN_BUCKET,
                                      VPIN_EWMA, lab["t0_us"].to_numpy())
            lab["vpin_placebo_t0"] = _vpin_np(
                tr_ts, tr_sz, rng.permutation(tr_ab), VPIN_BUCKET, VPIN_EWMA,
                lab["t0_us"].to_numpy())
            spells.append(lab)
        if (d - day0).days % 14 == 0:
            print(f"  day {d.date()}: cum spells {sum(len(x) for x in spells):,}",
                  flush=True)
        del tr_ts, tr_px, tr_sz, tr_ab
        gc.collect()
        d = d + pd.Timedelta(days=1)

    S = pd.concat(spells, ignore_index=True).sort_values("t0_us").reset_index(drop=True)
    S = macro_censor.censor_spells(S, windows)
    S["dur_h"] = S["duration_us"] / (3600 * 10**6)
    S["dur_ec"] = S["n_trades_spell"].astype("float64")
    S["time_in_comp_h"] = S["time_in_comp_min"] / 60.0
    S.to_parquet(sp_cache, index=False)
    print(f"spells built: {len(S):,} rows, {int(S['event'].sum()):,} events, "
          f"{int(S['censored_macro'].sum()):,} macro-censored. {DATA_FLAG}",
          flush=True)
    return S, M, haw


def make_splits(S: pd.DataFrame):
    row_ts = S["t0_us"].to_numpy()
    splits = list(purged_cpcv_splits(row_ts, n_groups=N_GROUPS,
                                     label_horizon_us=H_US,
                                     embargo_us=EMBARGO_US, n_test_groups=1))
    for s in splits:
        assert_no_leakage(s, row_ts, H_US, EMBARGO_US)
        inter = len(set(s["train_idx"].tolist()) & set(s["test_idx"].tolist()))
        assert inter == 0, f"index intersection {inter} in split {s['test_groups']}"
    print(f"CPCV: {len(splits)} folds, 0 index intersections, 0 label-window "
          f"overlaps (asserted)", flush=True)
    return splits


# ------------------------------------------------------------------- models

def _fit_cox(df, covs, duration_col="dur_h", strata=True):
    from lifelines import CoxPHFitter
    cols = [duration_col, "event", "hod"] + covs
    cph = CoxPHFitter()
    kw = {"strata": ["hod"]} if strata else {}
    cph.fit(df[cols], duration_col=duration_col, event_col="event", **kw)
    return cph


def _hr(cph, name):
    s = cph.summary.loc[name]
    return (float(np.exp(s["coef"])), float(np.exp(s["coef lower 95%"])),
            float(np.exp(s["coef upper 95%"])), float(s["p"]))


def _oof_concordance(S, splits, covs):
    from lifelines.utils import concordance_index
    et, ph, eo = [], [], []
    lr_p, powered, unrejected = [], 0, 0
    for s in splits:
        tr, te = S.iloc[s["train_idx"]], S.iloc[s["test_idx"]]
        cph = _fit_cox(tr, covs)
        ph.append(cph.predict_partial_hazard(te[covs]).to_numpy().ravel())
        et.append(te["dur_h"].to_numpy())
        eo.append(te["event"].to_numpy())
        p = float(cph.log_likelihood_ratio_test().p_value)
        lr_p.append(p)
        if int(te["event"].sum()) >= 50:
            powered += 1
            if p >= 0.05:
                unrejected += 1
    c = float(concordance_index(np.concatenate(et), -np.concatenate(ph),
                                np.concatenate(eo)))
    return c, (unrejected / powered if powered else 0.0), powered, lr_p


def run_t3(S, splits):
    print("\n===== CLAIM T3 — Wall-Clock Exposure Invariance =====", flush=True)
    print(DATA_FLAG, flush=True)
    res = {"exposure_fits": {}}
    for axis, dur_col in (("wall_clock", "dur_h"), ("event_count", "dur_ec")):
        for strata in (False, True):
            cph = _fit_cox(S, ["trades_per_min"], duration_col=dur_col, strata=strata)
            hr, lo, hi, p = _hr(cph, "trades_per_min")
            key = f"{axis}_{'strat' if strata else 'unstrat'}"
            res["exposure_fits"][key] = {"hr": hr, "ci95": [lo, hi], "p": p}
            print(f"  {key:24s} trades/min HR={hr:.4f} 95%CI=[{lo:.4f},{hi:.4f}] "
                  f"p={p:.3g}", flush=True)
    wu = res["exposure_fits"]["wall_clock_unstrat"]
    wst = res["exposure_fits"]["wall_clock_strat"]
    kill = None
    if wst["p"] < 0.01:
        kill = ("KILL: under wall-clock exposure, raw trade-arrival density remains "
                f"significant after HOD stratification (HR={wst['hr']:.4f}, "
                f"p={wst['p']:.3g} < 0.01) — dead mechanism: event-count exposure "
                "conflates arrival sparsity with survival duration")
    elif not (wu["ci95"][0] <= wst["hr"] <= wu["ci95"][1]):
        kill = ("KILL: HOD stratification shifts the trades/min HR "
                f"{wst['hr']:.4f} outside its unstratified 95% CI {wu['ci95']} — "
                "dead mechanism: wall-clock exposure is not diurnally invariant")
    res["kill"] = kill
    return res, kill


def _compression_on_path(price_min: np.ndarray, ts_min: pd.Series):
    """Causal compression features on a (possibly synthetic) minute price path."""
    p = pd.Series(price_min)
    hod = ts_min.dt.hour // (24 // HOD_BUCKETS)
    hourly = pd.Series(price_min, index=ts_min).resample("1h").last().dropna()
    r = hourly.pct_change()
    sigma_h = r.rolling(H_US // HOUR_US).std() * np.sqrt(H_US // HOUR_US)
    sig = sigma_h.reindex(ts_min, method="ffill").to_numpy()
    range_4h = (p.rolling(W_MIN).max() - p.rolling(W_MIN).min()).to_numpy()
    ru = range_4h / np.where(sig > 0, sig, np.nan)
    pct = np.full(len(p), np.nan)
    for b in range(HOD_BUCKETS):
        m = (hod == b).to_numpy()
        pct[m] = (pd.Series(ru[m]).rolling(POOL_MIN, min_periods=POOL_MIN // 2)
                  .rank(pct=True).to_numpy() * 100.0)
    comp = (pct <= PCT_THRESHOLD).astype("int8")
    run = (pd.Series(comp) != pd.Series(comp).shift()).cumsum().to_numpy()
    tic = pd.Series(np.arange(len(p))).groupby(run).cumcount().to_numpy()
    tic = np.where(comp == 1, tic, 0.0)
    return comp, tic


def run_t1(S, splits, M):
    print("\n===== CLAIM T1 — Tick-Trade Compression Duration-Dependence (WHEN) =====",
          flush=True)
    print(DATA_FLAG, flush=True)
    covs = ["compression", "time_in_comp_h", "sigma_h"]
    c_oof, unrej_frac, powered, lr_p = _oof_concordance(S, splits, covs)
    print(f"  pooled OOF Harrell C = {c_oof:.4f}; powered folds={powered}, "
          f"LR-unrejected fraction={unrej_frac:.2%}", flush=True)

    m_strat = _fit_cox(S, covs, strata=True)
    m_taut = _fit_cox(S, ["compression", "sigma_h"], strata=False)
    m_comp = _fit_cox(S, ["compression"], strata=False)
    hr_s, lo_s, hi_s, _ = _hr(m_strat, "compression")
    hr_t, lo_t, hi_t, _ = _hr(m_taut, "compression")
    hr_c, lo_c, hi_c, _ = _hr(m_comp, "compression")
    print(f"  stratified compression HR={hr_s:.3f} CI=[{lo_s:.3f},{hi_s:.3f}]; "
          f"sigma-conditioned HR={hr_t:.3f} CI=[{lo_t:.3f},{hi_t:.3f}]; "
          f"compression-only HR={hr_c:.3f} CI=[{lo_c:.3f},{hi_c:.3f}]", flush=True)
    observed_gap = abs(np.log(hr_c) - np.log(hr_t))

    print(f"  scale-invariance null: {NULL_REPS} reps, {NULL_BLOCK_MIN}min blocks ...",
          flush=True)
    ts_min = pd.to_datetime(M["min"], unit="us", utc=True)
    p = M["price"].to_numpy()
    r = pd.Series(p).pct_change().to_numpy()
    sig = M["sigma_h"].to_numpy()
    z = np.nan_to_num(r / np.where(sig > 0, sig, np.nan), nan=0.0)
    rng = np.random.default_rng(7)
    n = len(z)
    pos = np.searchsorted(M["min"].to_numpy(), S["t0_us"].to_numpy(), side="right") - 1
    gaps = []
    for rep in range(NULL_REPS):
        starts = rng.integers(0, max(n - NULL_BLOCK_MIN, 1), int(np.ceil(n / NULL_BLOCK_MIN)))
        zstar = np.concatenate([z[s:s + NULL_BLOCK_MIN] for s in starts])[:n]
        rstar = np.nan_to_num(sig, nan=0.0) * zstar
        pstar = p[0] * np.cumprod(1.0 + rstar)
        comp_s, tic_s = _compression_on_path(pstar, ts_min)
        Ss = S.copy()
        Ss["compression"] = comp_s[pos]
        Ss["time_in_comp_h"] = tic_s[pos] / 60.0
        mc = _fit_cox(Ss, ["compression"], strata=False)
        mt = _fit_cox(Ss, ["compression", "sigma_h"], strata=False)
        gaps.append(abs(np.log(_hr(mc, "compression")[0])
                        - np.log(_hr(mt, "compression")[0])))
        if (rep + 1) % 10 == 0:
            print(f"    null rep {rep+1}/{NULL_REPS}", flush=True)
    gaps = np.asarray(gaps)
    nl, nh = np.percentile(gaps, [2.5, 97.5])
    print(f"  observed |log HR| gap={observed_gap:.4f}; null 95% band "
          f"=[{nl:.4f},{nh:.4f}]", flush=True)

    results = {
        "oof_concordance": c_oof,
        "unrejected_powered_fold_fraction": unrej_frac,
        "powered_folds": powered,
        "fold_lr_p": lr_p,
        "stratified_hr_ci": [lo_s, hi_s],
        "tautology_hr_ci": [lo_t, hi_t],
        "compression_only_hr_ci": [lo_c, hi_c],
        "observed_gap": float(observed_gap),
        "scale_null_gap_ci95": [float(nl), float(nh)],
    }
    kill = None
    try:
        c1.enforce_kill_lines(results)
    except AssertionError as e:
        kill = str(e)
    return results, kill


def run_t2(S, splits, haw):
    print("\n===== CLAIM T2 — Aggressive Trade-Flow Asymmetry & 2D Hawkes (WHICH WAY) =====",
          flush=True)
    print(DATA_FLAG, flush=True)
    from sklearn.linear_model import LogisticRegression
    from scipy.stats import beta as beta_dist

    E_mask = (S["compression"] == 1) & (S["event"] == 1)
    E = S[E_mask].copy()
    E["up"] = (E["touch_side"] == 1).astype("int8")
    e_rows = E.index.to_numpy()
    print(f"  compression event spells: {len(E):,}, up={int(E['up'].sum()):,} "
          f"({E['up'].mean():.4f})", flush=True)

    def asym_per_fold(haw2):
        """hawkes self-excitation asymmetry (alpha_bb - alpha_ss) per HOD bucket,
        fitted on TRAIN trades only, assigned to TEST rows."""
        asym_full = np.full(len(S), np.nan)
        for s in splits:
            tr_idx = s["train_idx"]
            lo = S["t0_us"].iloc[tr_idx].min()
            hi = S["t0_us"].iloc[tr_idx].max()
            for b in range(HOD_BUCKETS):
                w = haw2[(haw2["hod"] == b) & (haw2["ts_exchange_us"] >= lo)
                         & (haw2["ts_exchange_us"] <= hi)]
                if len(w) == 0:
                    continue
                if len(w) > HAWKES_CAP:
                    w = w.iloc[:HAWKES_CAP]
                fit = fit_hawkes(w["ts_exchange_us"].to_numpy(),
                                 w["aggressor_buy"].to_numpy())
                a = np.asarray(fit["alpha"])
                sel = (S["hod"].to_numpy() == b) & np.isin(
                    S.index.to_numpy(), s["test_idx"])
                asym_full[sel] = a[0, 0] - a[1, 1]
        return asym_full

    def oof_direction(shuffled):
        haw2 = haw
        if shuffled:
            rng = np.random.default_rng(99)
            haw2 = haw.assign(aggressor_buy=rng.permutation(
                haw["aggressor_buy"].to_numpy()))
        asym = asym_per_fold(haw2)
        vp = S["vpin_placebo_t0" if shuffled else "vpin_t0"].to_numpy()
        X = np.column_stack([asym, vp, S["trades_per_min"].to_numpy()])
        oof = np.full(len(S), np.nan)
        for s in splits:
            tr_rows = s["train_idx"]
            tr_e = tr_rows[np.isin(tr_rows, e_rows)]
            te_e = s["test_idx"][np.isin(s["test_idx"], e_rows)]
            Xtr = X[tr_e]
            ytr = E["up"].to_numpy()[np.searchsorted(e_rows, tr_e)]
            ok = np.isfinite(Xtr).all(axis=1)
            clf = LogisticRegression(max_iter=1000)
            clf.fit(Xtr[ok], ytr[ok])
            Xte = X[te_e]
            okte = np.isfinite(Xte).all(axis=1)
            oof[te_e[okte]] = clf.predict_proba(Xte[okte])[:, 1]
        return oof[e_rows]

    p_oof = oof_direction(shuffled=False)
    p_pl = oof_direction(shuffled=True)
    y = E["up"].to_numpy()
    ok = np.isfinite(p_oof)
    brier = float(np.mean((p_oof[ok] - y[ok]) ** 2))
    clim = float(np.mean((y[ok].mean() - y[ok]) ** 2))
    skill = 1.0 - brier / clim
    x, n = int(y[ok].sum()), int(ok.sum())
    cp_lo = float(beta_dist.ppf(0.025, x, n - x + 1))
    cp_hi = float(beta_dist.ppf(0.975, x + 1, n - x))
    asym_e = None  # tercile split on the real asymmetry feature
    haw2 = haw
    asym_real = asym_per_fold(haw2)
    thr = np.nanpercentile(asym_real[e_rows], 66.7)
    hi_mask = ok & (asym_real[e_rows] >= thr)
    xh, nh_ = int(y[hi_mask].sum()), int(hi_mask.sum())
    hi_lo = float(beta_dist.ppf(0.025, xh, nh_ - xh + 1)) if nh_ > xh else 0.0
    hi_hi = float(beta_dist.ppf(0.975, xh + 1, nh_ - xh)) if nh_ > 0 else 1.0
    okp = np.isfinite(p_pl)
    brier_p = float(np.mean((p_pl[okp] - y[okp]) ** 2))
    skill_p = 1.0 - brier_p / clim
    pl_mask = okp & (asym_real[e_rows] >= thr)
    xp, npp = int(y[pl_mask].sum()), int(pl_mask.sum())
    pl_lo = float(beta_dist.ppf(0.025, xp, npp - xp + 1)) if npp > xp else 0.0
    pl_hi = float(beta_dist.ppf(0.975, xp + 1, npp - xp)) if npp > 0 else 1.0
    print(f"  OOF Brier={brier:.4f} climatology={clim:.4f} skill={skill:.4f}", flush=True)
    print(f"  P(up) among compression events: {x}/{n} CP95=[{cp_lo:.4f},{cp_hi:.4f}]",
          flush=True)
    print(f"  P(up) high-asymmetry tercile: {xh}/{nh_} CP95=[{hi_lo:.4f},{hi_hi:.4f}]",
          flush=True)
    print(f"  placebo (sign-shuffled): skill={skill_p:.4f} "
          f"hi-tercile CP95=[{pl_lo:.4f},{pl_hi:.4f}]", flush=True)

    lo_i, hi_i = NULL_INTERVAL
    kill = None
    if skill <= 0:
        kill = (f"KILL: OOF directional Brier skill {skill:.4f} <= 0 against "
                "climatology — dead mechanism: taker asymmetry + VPIN carries no "
                "WHICH-WAY edge within compression")
    elif hi_lo <= hi_i and hi_hi >= lo_i:
        kill = (f"KILL: 95% CI for P(up | taker asymmetry) [{hi_lo:.4f},{hi_hi:.4f}] "
                f"overlaps the price-only null [{lo_i},{hi_i}] — dead mechanism: "
                "direction stays inside the 0.505 ceiling")
    elif not (pl_lo > hi_i or pl_hi < lo_i):
        kill = (f"KILL: trade-sign-shuffled placebo reproduces the directional "
                f"separation (hi-tercile CP95=[{pl_lo:.4f},{pl_hi:.4f}], "
                f"skill={skill_p:.4f}) — dead mechanism: separation is a shuffle "
                "artifact, not information")
    res = {"oof_brier": brier, "climatology_brier": clim, "brier_skill": skill,
           "p_up_ci95": [cp_lo, cp_hi], "n_event_spells": n,
           "p_up_hi_asym_ci95": [hi_lo, hi_hi], "hi_asym_n": nh_,
           "placebo_skill": skill_p,
           "placebo_hi_asym_ci95": [pl_lo, pl_hi],
           "null_interval": list(NULL_INTERVAL)}
    return res, kill


# ------------------------------------------------------------------ report

def contract(claim, mechanism, test, kill_line, status, cannot, extra):
    block = {
        "CLAIM": claim, "MECHANISM": mechanism, "TEST": test,
        "KILL LINE": kill_line, "STATUS": status,
        "WHAT IT CANNOT TELL YOU": cannot, "DATA FLAG": DATA_FLAG,
        "DETAILS": extra,
    }
    print("\n" + "=" * 78, flush=True)
    for k, v in block.items():
        print(f"{k}: {v}", flush=True)
    print("=" * 78, flush=True)
    return block


CONTRACTS = {
    "T3": dict(
        claim="T3 — Wall-Clock Exposure Invariance on Event-Clock Covariates",
        mechanism="An event-count survival clock stretches apparent duration in "
                  "quiet sessions; exact wall-clock (t_start, t_stop] exposure "
                  "should decouple trade-arrival seasonality from time-in-state.",
        test="Identical Cox baseline hazards under wall-clock vs event-count "
             "exposure, unstratified and hour-of-day stratified, on BTCUSDT "
             "aggTrades event-clock spells with purged CPCV and macro censoring.",
        kill_line="Under wall-clock exposure, trades/min significant at p<0.01 "
                  "after HOD stratification, OR HOD stratification shifts HRs "
                  "outside unstratified 95% CIs.",
        cannot="Whether true liquidity aging operates in physical vs event time "
               "once full incremental L2 book updates arrive."),
    "T1": dict(
        claim="T1 — Tick-Trade Compression Duration-Dependence (WHEN only)",
        mechanism="If daily C1 failed only due to calendar-bar aggregation, "
                  "tick-level compression aging on aggTrades raises the "
                  "conditional hazard of a trade-touch triple-barrier excursion.",
        test="Competing-risks Cox (c1_l2_test harness + kill lines) on aggTrades "
             "event-clock spells: wall-clock (t_start,t_stop], noise-floored "
             "trade-touch triple barriers (>=10x median spread proxy), HOD "
             "stratification, macro censoring, purged CPCV, 1h block-bootstrap "
             "sigma-standardized scale-invariance null.",
        kill_line="(a) pooled OOF Harrell C <= 0.52; (b) compression HR CI includes "
                  "1.0 conditioned solely on sigma_H; (c) constant-hazard LR "
                  "unrejected in >=30% of powered folds (>=50 events); (d) effect "
                  "collapses under HOD stratification; (e) scale-invariance null "
                  "reproduces observed |log HR| gap within its 95% band.",
        cannot="Whether a failure stems from missing passive limit-order aging "
               "and cancellation dynamics (only testable in C1-L2), breakout "
               "direction, or sizing."),
    "T2": dict(
        claim="T2 — Aggressive Trade-Flow Asymmetry & 2D Hawkes (WHICH WAY only)",
        mechanism="Persistent one-sided taker aggression during compression "
                  "reflects informed sweep accumulation before price displaces.",
        test="2D (buy/sell) Hawkes self-excitation asymmetry per HOD bucket + "
             "trade-count VPIN within compression spells; OOF logistic P(up) vs "
             "[0.497, 0.513], Brier skill over climatology, Clopper-Pearson CIs, "
             "trade-sign-shuffled placebo preserving timestamps and sizes.",
        kill_line="OOF directional Brier skill <= 0; OR 95% CI for P(up | taker "
                  "asymmetry) overlaps [0.497, 0.513]; OR sign-shuffled placebo "
                  "reproduces the directional separation.",
        cannot="Passive limit-order absorption or quote cancellation dynamics "
               "(require reconciled L2 depth diffs in C5/C6)."),
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=Path("data/processed/aggtrades"))
    ap.add_argument("--timeline", type=Path, default=Path("data/macro_timeline.csv"))
    ap.add_argument("--cache-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--out-dir", type=Path, default=Path("paper/research"))
    ap.add_argument("--claims", default="t3,t1,t2")
    args = ap.parse_args(argv)

    S, M, haw = build_spells(args.data_dir, args.timeline, args.cache_dir)
    # Startup artifact: spells from the window's first day carry an
    # undefined trailing-sigma covariate (the 24h window is incomplete at
    # t0). A spell with an undefined covariate is not interpretable and
    # is dropped - a data-startup exclusion, not a tuning choice; the
    # count is printed, never silent.
    covs = ["sigma_h", "compression", "time_in_comp_h", "dur_h", "hod"]
    n0 = len(S)
    S = S.dropna(subset=covs).reset_index(drop=True)
    if n0 - len(S):
        print(f"dropped {n0 - len(S)} startup spells with undefined trailing "
              f"covariates (first-day incomplete windows)", flush=True)
    splits = make_splits(S)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    order = [c for c in ["t3", "t1", "t2"] if c in args.claims.split(",")]
    summary = {}
    for claim in order:
        if claim == "t3":
            res, kill = run_t3(S, splits)
        elif claim == "t1":
            res, kill = run_t1(S, splits, M)
        else:
            res, kill = run_t2(S, splits, haw)
        c = CONTRACTS[claim.upper()]
        status = ("tested-fail — " + kill) if kill else \
            "survives all pre-declared kill lines (not proof of the claim)"
        block = contract(c["claim"], c["mechanism"], c["test"], c["kill_line"],
                         status, c["cannot"], res)
        summary[claim] = block
        (args.out_dir / f"taker_falsification_{claim}.json").write_text(
            json.dumps(block, indent=2, default=str))
        if kill:
            print(f"\nSTOPPING: {claim.upper()} kill line fired. Dead mechanism "
                  f"named above; no pivot to a surviving variant.", flush=True)
            break
    (args.out_dir / "taker_falsification_summary.json").write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"\nsummary written to {args.out_dir}/taker_falsification_*.json",
          flush=True)
    return 2 if any("tested-fail" in b["STATUS"] for b in summary.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
