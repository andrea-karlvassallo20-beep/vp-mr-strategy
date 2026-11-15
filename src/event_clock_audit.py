"""Dual-clock compression-duration audit: wall clock vs volume-filtered
event clock, across the observed 58x hourly arrival-rate swing.

WHY THIS EXISTS. The observed BTCUSDT trade-arrival density swings 58x by
hour of day (9,638 to 563,228 rows/hr). An event-count compression "duration"
therefore measures TWO things at once: (i) genuine liquidity compression
aging in physical time, and (ii) how many top-of-book cancel/replace
flickers the venue happened to emit during the window. Before any T1
duration-dependence test, the two clocks must be separated and their
disagreement measured.

DESCRIPTIVE ONLY. This module computes durations, correlations, and
dispersion diagnostics. It fits NO predictive model, produces NO labels for
direction, and tests NO claim. Kill lines for T1 live in src/c1_l2_test.py.

Definitions (per causal compression episode - a maximal contiguous run of
compression-state rows):
  wall_clock_comp_dur_us    cumulative physical elapsed time in the state,
                            sum of (t_stop - t_start) over the episode.
  vol_filtered_event_dur    cumulative state-change count EXCLUDING
                            zero-volume 1-tick BBO cancel/replace flickers.
                            A row is a flicker iff executed_volume <= 0 AND
                            |depth_change_10bps| < depth_threshold AND
                            |price_move| <= 1 tick: no trade touched the
                            book and nothing moved beyond a quote flicker.
  raw_event_dur             the unfiltered state-change count (the naive
                            event-clock duration, kept for the diagnostics
                            contrast only).
"""

import numpy as np
import pandas as pd

REQ_COLS = {
    "t_start", "t_stop", "in_compression",
    "executed_volume", "depth_change_10bps",
}


def _validate(rows: pd.DataFrame) -> pd.DataFrame:
    missing = REQ_COLS - set(rows.columns)
    if missing:
        raise ValueError(f"event rows missing columns: {missing}")
    r = rows.copy()
    for c in ("t_start", "t_stop"):
        r[c] = pd.to_numeric(r[c], errors="raise").astype("int64")
    if (r["t_stop"] < r["t_start"]).any():
        raise ValueError("t_stop < t_start in some (t_start, t_stop] intervals")
    if (np.diff(r["t_start"].to_numpy()) < 0).any():
        raise ValueError("rows must be sorted by t_start")
    if "price_move" not in r.columns:
        r["price_move"] = 0.0
    return r


def is_flicker(rows: pd.DataFrame, tick: float = 0.1,
               depth_threshold: float = 0.0) -> np.ndarray:
    """Zero-volume 1-tick BBO cancel/replace flicker mask.

    A row is a FLICKER iff it carries NO executed trade volume, its
    net depth change within 10 bps of mid is below the threshold, and its
    price moved at most 1 tick: nothing real happened, only the quote
    flickered. Everything else is a genuine state change.
    """
    r = _validate(rows)
    return (
        (r["executed_volume"].to_numpy() <= 0.0)
        & (np.abs(r["depth_change_10bps"].to_numpy()) < depth_threshold)
        & (np.abs(r["price_move"].to_numpy()) <= tick)
    )


def _episodes(r: pd.DataFrame) -> np.ndarray:
    """Episode id per row: maximal contiguous runs of in_compression=True
    (a False row breaks the run). Non-compression rows get -1."""
    comp = r["in_compression"].to_numpy(dtype=bool)
    eid = np.full(len(r), -1, dtype=np.int64)
    run = 0
    inside = False
    for i, c in enumerate(comp):
        if c:
            if not inside:
                inside = True
                run += 1
            eid[i] = run
        else:
            inside = False
    return eid


def dual_clock_durations(rows: pd.DataFrame, tick: float = 0.1,
                         depth_threshold: float = 0.0) -> pd.DataFrame:
    """Per-episode dual-clock duration decomposition.

    Returns one row per compression episode with:
      episode, t_start_us, t_stop_us, n_rows,
      wall_clock_comp_dur_us, raw_event_dur, vol_filtered_event_dur,
      flicker_rows, flicker_share
    """
    r = _validate(rows)
    eid = _episodes(r)
    flick = is_flicker(r, tick, depth_threshold)
    r = r.assign(_eid=eid, _flick=flick, _dur=r["t_stop"] - r["t_start"])

    mask = eid >= 0
    if not mask.any():
        return pd.DataFrame(columns=[
            "episode", "t_start_us", "t_stop_us", "n_rows",
            "wall_clock_comp_dur_us", "raw_event_dur",
            "vol_filtered_event_dur", "flicker_rows", "flicker_share",
        ])

    g = r[mask].groupby("_eid")
    out = pd.DataFrame({
        "t_start_us": g["t_start"].first(),
        "t_stop_us": g["t_stop"].last(),
        "n_rows": g.size(),
        "raw_event_dur": g.size(),
        "flicker_rows": g["_flick"].sum(),
    }).reset_index(drop=True)
    # wall-clock duration of a compression EPISODE is the physical elapsed
    # span from its first row's start to its last row's stop - the state
    # persists between state-change rows (a frozen book ages in the state,
    # which is exactly what the event count cannot see)
    out["wall_clock_comp_dur_us"] = out["t_stop_us"] - out["t_start_us"]
    out["episode"] = np.arange(1, len(out) + 1)
    out["vol_filtered_event_dur"] = out["raw_event_dur"] - out["flicker_rows"]
    out["flicker_share"] = out["flicker_rows"] / out["raw_event_dur"]
    return out[
        ["episode", "t_start_us", "t_stop_us", "n_rows",
         "wall_clock_comp_dur_us", "raw_event_dur",
         "vol_filtered_event_dur", "flicker_rows", "flicker_share"]
    ]


def duration_diagnostics(rows: pd.DataFrame, tick: float = 0.1,
                        depth_threshold: float = 0.0) -> dict:
    """Correlation and dispersion diagnostics between the three duration
    clocks, per compression episode. NO predictive model is fit.

    Reports Pearson and Spearman correlations of the three pairwise clock
    pairs, plus dispersion (coefficient of variation, IQR/median) of each
    clock, and the wall-clock-per-event interarrival within episodes
    (the direct fingerprint of the 58x arrival-rate swing).
    """
    ep = dual_clock_durations(rows, tick, depth_threshold)
    if len(ep) < 3:
        raise ValueError("need >= 3 compression episodes for diagnostics")
    wc = ep["wall_clock_comp_dur_us"].to_numpy(dtype=float)
    re_ = ep["raw_event_dur"].to_numpy(dtype=float)
    vf = ep["vol_filtered_event_dur"].to_numpy(dtype=float)

    def _safe_corr(a, b):
        if np.std(a) == 0 or np.std(b) == 0:
            return float("nan")
        return float(np.corrcoef(a, b)[0, 1])

    def _spearman(a, b):
        ra = pd.Series(a).rank().to_numpy()
        rb = pd.Series(b).rank().to_numpy()
        return _safe_corr(ra, rb)

    def _disp(x):
        med = float(np.median(x))
        q75, q25 = np.percentile(x, [75, 25])
        return {
            "mean": float(np.mean(x)),
            "median": med,
            "std": float(np.std(x, ddof=1)) if len(x) > 1 else 0.0,
            "cv": float(np.std(x, ddof=1) / np.mean(x)) if len(x) > 1 and np.mean(x) > 0 else float("nan"),
            "iqr_over_median": float((q75 - q25) / med) if med > 0 else float("nan"),
        }

    # interarrival fingerprint: wall-clock seconds per (filtered) event
    per_event_s = wc / np.maximum(vf, 1.0) / 1e6
    return {
        "n_episodes": int(len(ep)),
        "correlations": {
            "wall_vs_raw_event": {
                "pearson": _safe_corr(wc, re_),
                "spearman": _spearman(wc, re_),
            },
            "wall_vs_vol_filtered_event": {
                "pearson": _safe_corr(wc, vf),
                "spearman": _spearman(wc, vf),
            },
            "raw_vs_vol_filtered_event": {
                "pearson": _safe_corr(re_, vf),
                "spearman": _spearman(re_, vf),
            },
        },
        "dispersion": {
            "wall_clock_comp_dur_us": _disp(wc),
            "raw_event_dur": _disp(re_),
            "vol_filtered_event_dur": _disp(vf),
            "wall_seconds_per_filtered_event": _disp(per_event_s),
        },
        "flicker_share_mean": float(ep["flicker_share"].mean()),
        "note": ("descriptive decomposition only; no predictive or "
                 "directional model is fit here"),
    }


def synthesize_diurnal_rows(seed: int = 7, days: int = 3,
                            base_rate_per_s: float = 5.0,
                            burst_multiplier: float = 60.0,
                            frozen_hours: tuple = ((5, 7),),
                            compression_prob: float = 0.35,
                            flicker_prob_burst: float = 0.55,
                            flicker_prob_quiet: float = 0.05,
                            depth_threshold: float = 5.0) -> pd.DataFrame:
    """Synthetic event-clock rows with the two hazards the audit must
    survive: a 60x diurnal activity burst and multi-hour frozen-book dead
    zones. Used by the CPCV leakage stress test and the diagnostics tests.

    Rows carry the full dual-clock schema: exact int64 (t_start, t_stop]
    intervals, in_compression runs, executed_volume, depth_change_10bps,
    price_move. In burst hours the generator injects a high share of
    zero-volume 1-tick BBO flickers; in frozen hours almost no rows are
    emitted at all.
    """
    rng = np.random.default_rng(seed)
    frames = []
    t_us = int(1_730_419_200_000_000)  # 2024-11-01 00:00:00 UTC, µs
    day_us = 86_400_000_000
    hour_us = 3_600_000_000
    in_comp = False
    for _ in range(days):
        for h in range(24):
            frozen = any(lo <= h < hi for lo, hi in frozen_hours)
            if frozen:
                in_comp = False  # dead zone breaks the run
                continue
            burst = 13 <= h < 16  # the session-open burst window
            rate = base_rate_per_s * (burst_multiplier if burst else 1.0)
            n = int(rng.poisson(rate * 3600.0))
            if n == 0:
                continue
            # exponential inter-arrivals, RESCALED to fit strictly inside
            # the hour (no spill into the frozen zone that follows)
            gaps = rng.exponential(1.0 / rate, n).cumsum()
            if gaps[-1] > 0:
                gaps = gaps / gaps[-1] * 3599.0
            ts = t_us + h * hour_us + (gaps * 1e6).astype(np.int64)
            # per-row state draw; contiguous True draws form episodes
            # (a False row breaks the run; frozen hours reset to not-in-comp)
            comp = rng.random(n) < compression_prob
            in_comp = bool(comp[-1])
            flicker_p = flicker_prob_burst if burst else flicker_prob_quiet
            is_flick = rng.random(n) < flicker_p
            vol = np.where(is_flick, 0.0, rng.uniform(0.001, 2.0, n))
            dch = np.where(
                is_flick,
                rng.uniform(0.0, depth_threshold * 0.5, n),
                rng.uniform(depth_threshold, 50.0, n),
            )
            pm = np.where(
                is_flick,
                rng.choice([0.0, 0.1], n),
                rng.choice([0.0, 0.1, 0.2, -0.2, 0.5], n),
            )
            stop = ts + rng.integers(1, 1000, n)
            frames.append(pd.DataFrame({
                "t_start": ts,
                "t_stop": stop,
                "in_compression": comp,
                "executed_volume": vol,
                "depth_change_10bps": dch,
                "price_move": pm,
            }))
        t_us += day_us
    if not frames:
        return pd.DataFrame(columns=[
            "t_start", "t_stop", "in_compression",
            "executed_volume", "depth_change_10bps", "price_move",
        ])
    return pd.concat(frames, ignore_index=True).sort_values(
        "t_start", kind="stable").reset_index(drop=True)


def cpcv_leakage_stress(row_ts: np.ndarray, n_groups: int = 6,
                        label_horizon_us: int = 60_000_000,
                        embargo_us: int = 30_000_000,
                        n_test_groups: int = 1) -> dict:
    """Run purged_cpcv_splits across ALL combinatorial folds and verify the
    three invariants: strictly 0 train/test index intersections, strictly 0
    overlapping forward label windows, and intact post-test embargo buffers.

    Returns a summary record; raises AssertionError on any violation.
    """
    from event_clock import purged_cpcv_splits, assert_no_leakage

    row_ts = np.asarray(row_ts, dtype=np.int64)
    n_folds = 0
    idx_intersections = 0
    label_overlaps = 0
    embargo_violations = 0
    min_train_gap = np.inf
    for split in purged_cpcv_splits(
        row_ts, n_groups=n_groups, label_horizon_us=label_horizon_us,
        embargo_us=embargo_us, n_test_groups=n_test_groups,
    ):
        n_folds += 1
        inter = np.intersect1d(split["train_idx"], split["test_idx"])
        idx_intersections += len(inter)
        # forward-label overlap: a train row whose label window [s, s+H]
        # intersects the test window at all (no embargo slack) would be a
        # hard leak; assert_no_leakage checks the stricter embargo version.
        # intact embargo: nearest surviving train row on either side of the
        # test window must sit outside [lo - embargo, hi + H + embargo].
        assert_no_leakage(split, row_ts, label_horizon_us, embargo_us)
        lo, hi = split["test_bounds"]
        win_lo, win_hi = split["purge_window"]
        s = row_ts[split["train_idx"]]
        if len(s):
            left = s[s < win_lo]
            right = s[s > win_hi]
            gap_l = (win_lo - left.max()) if len(left) else np.inf
            gap_r = (right.min() - win_hi) if len(right) else np.inf
            min_train_gap = min(min_train_gap, gap_l, gap_r)
        # any train label window touching the raw test window is a leak
        e = s + label_horizon_us
        label_overlaps += int(((e >= lo) & (s <= hi)).sum())
        # embargo intactness: no train row inside the purge window at all
        inside = ((s >= win_lo) & (s <= win_hi))
        embargo_violations += int(inside.sum())

    if idx_intersections or label_overlaps or embargo_violations:
        raise AssertionError(
            f"CPCV stress failed: idx_intersections={idx_intersections}, "
            f"label_overlaps={label_overlaps}, "
            f"embargo_violations={embargo_violations}"
        )
    return {
        "n_folds": n_folds,
        "idx_intersections": idx_intersections,
        "label_overlaps": label_overlaps,
        "embargo_violations": embargo_violations,
        "min_train_gap_us": (None if not np.isfinite(min_train_gap)
                             else float(min_train_gap)),
        "status": "PASS",
    }
