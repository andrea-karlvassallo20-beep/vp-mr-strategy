"""Unit tests for src/event_clock_audit.py: dual-clock compression-duration
decomposition and the purged-CPCV leakage stress test under 60x diurnal
bursts and multi-hour frozen-book dead zones."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from event_clock import purged_cpcv_splits, assert_no_leakage
from event_clock_audit import (
    cpcv_leakage_stress,
    dual_clock_durations,
    duration_diagnostics,
    is_flicker,
    synthesize_diurnal_rows,
)


def _rows(spec):
    """spec: list of (t_start, t_stop, in_comp, vol, dch, pm) tuples."""
    return pd.DataFrame(spec, columns=[
        "t_start", "t_stop", "in_compression",
        "executed_volume", "depth_change_10bps", "price_move",
    ])


# ---------------------------------------------------------------------
# 1. Dual-clock duration decomposition
# ---------------------------------------------------------------------

def test_wall_clock_vs_filtered_event_count_side_by_side():
    """A ~55-minute compression episode: 12 genuine state changes and 48
    zero-volume 1-tick flickers. The two clocks must report the episode
    SPAN in microseconds and the filtered count 12, side by side."""
    t0 = 1_730_419_200_000_000
    spec = []
    # 12 genuine rows, 5 minutes (300e6 us) apart, interval 1s
    for i in range(12):
        s = t0 + i * 300_000_000
        spec.append((s, s + 1_000_000, True, 0.5, 10.0, 0.1))
    # 48 flickers interleaved (zero volume, tiny depth change, <=1 tick)
    for i in range(48):
        s = t0 + i * 60_000_000 + 1_000
        spec.append((s, s + 500_000, True, 0.0, 1.0, 0.1))
    ep = dual_clock_durations(_rows(spec).sort_values("t_start"),
                              tick=0.1, depth_threshold=5.0)
    assert len(ep) == 1
    row = ep.iloc[0]
    # wall clock = physical elapsed span of the episode
    assert row["wall_clock_comp_dur_us"] == 11 * 300_000_000 + 1_000_000
    assert row["raw_event_dur"] == 60
    assert row["vol_filtered_event_dur"] == 12
    assert row["flicker_rows"] == 48
    assert row["flicker_share"] == pytest.approx(0.8)


def test_flicker_mask_definition():
    """Flicker = zero volume AND depth change below threshold AND price move
    <= 1 tick. Every genuine leg (volume, depth, 2-tick move) breaks it."""
    spec = [
        (0, 1, True, 0.0, 1.0, 0.1),   # flicker
        (1, 2, True, 0.5, 1.0, 0.0),   # has volume -> genuine
        (2, 3, True, 0.0, 10.0, 0.0),  # depth change >= threshold -> genuine
        (3, 4, True, 0.0, 1.0, 0.3),   # 3-tick move -> genuine
        (4, 5, True, 0.0, 0.0, 0.0),   # zero-volume flat flicker
    ]
    m = is_flicker(_rows(spec), tick=0.1, depth_threshold=5.0)
    assert m.tolist() == [True, False, False, False, True]


def test_episode_runs_broken_by_non_compression_rows():
    """A non-compression row must split the run into two episodes."""
    t0 = 0
    spec = [
        (t0, t0 + 10, True, 1.0, 10.0, 0.0),
        (t0 + 20, t0 + 30, True, 1.0, 10.0, 0.0),
        (t0 + 40, t0 + 50, False, 1.0, 10.0, 0.0),   # break
        (t0 + 60, t0 + 70, True, 1.0, 10.0, 0.0),
        (t0 + 80, t0 + 90, True, 1.0, 10.0, 0.0),
    ]
    ep = dual_clock_durations(_rows(spec))
    assert len(ep) == 2
    assert ep["episode"].tolist() == [1, 2]
    assert ep["wall_clock_comp_dur_us"].tolist() == [30, 30]  # spans, not interval sums


def test_dead_zone_stretches_wall_clock_not_event_count():
    """A frozen book (multi-hour gap between rows) inflates wall-clock
    duration while the filtered event count stays flat - the exact
    signature the audit exists to expose."""
    t0 = 0
    spec = []
    for i in range(10):
        s = t0 + i * 1_000_000
        spec.append((s, s + 1, True, 1.0, 10.0, 0.0))
    # 4-hour dead zone, then 10 more rows
    for i in range(10):
        s = t0 + 4 * 3_600_000_000 + i * 1_000_000
        spec.append((s, s + 1, True, 1.0, 10.0, 0.0))
    ep = dual_clock_durations(_rows(spec))
    assert len(ep) == 1
    assert ep["vol_filtered_event_dur"].iloc[0] == 20
    assert ep["wall_clock_comp_dur_us"].iloc[0] >= 4 * 3_600_000_000


def test_input_validation():
    with pytest.raises(ValueError, match="missing columns"):
        dual_clock_durations(pd.DataFrame({"t_start": [1]}))
    bad = _rows([(5, 1, True, 0.0, 0.0, 0.0)])
    with pytest.raises(ValueError, match="t_stop < t_start"):
        dual_clock_durations(bad)
    unsorted = _rows([(10, 11, True, 1.0, 1.0, 0.0), (1, 2, True, 1.0, 1.0, 0.0)])
    with pytest.raises(ValueError, match="sorted"):
        dual_clock_durations(unsorted)


# ---------------------------------------------------------------------
# 2. Purged CPCV leakage stress test (60x bursts + frozen dead zones)
# ---------------------------------------------------------------------

def test_cpcv_stress_under_60x_bursts_and_dead_zones():
    """Synthetic rows with 60x diurnal bursts and multi-hour frozen-book
    dead zones; ALL combinatorial folds must show strictly 0 index
    intersections, 0 overlapping forward label windows, and intact embargo."""
    df = synthesize_diurnal_rows(seed=7, days=3, base_rate_per_s=1.0)
    assert len(df) > 10_000

    # the 60x burst and the dead zones must be present in the data itself
    hr = df["t_start"] // 3_600_000_000 % 24
    burst_rate = (hr.isin([13, 14, 15])).sum() / 3.0
    quiet_rate = (~(hr.isin([13, 14, 15]))).sum() / 21.0
    assert burst_rate / quiet_rate > 10.0  # rows/hour, burst vs quiet
    assert (hr.isin([5, 6])).sum() == 0    # frozen hours emit nothing

    res = cpcv_leakage_stress(
        df["t_start"].to_numpy(),
        n_groups=6,
        label_horizon_us=60_000_000,   # 60s forward label
        embargo_us=30_000_000,         # 30s embargo
        n_test_groups=1,
    )
    assert res["n_folds"] == 6
    assert res["idx_intersections"] == 0
    assert res["label_overlaps"] == 0
    assert res["embargo_violations"] == 0
    assert res["status"] == "PASS"


def test_cpcv_stress_multi_test_group_folds():
    df = synthesize_diurnal_rows(seed=11, days=2, base_rate_per_s=1.0,
                                 frozen_hours=((2, 4), (5, 7)))
    res = cpcv_leakage_stress(
        df["t_start"].to_numpy(),
        n_groups=6,
        label_horizon_us=300_000_000,
        embargo_us=120_000_000,
        n_test_groups=2,
    )
    assert res["n_folds"] == 15  # C(6,2)
    assert res["idx_intersections"] == 0
    assert res["label_overlaps"] == 0
    assert res["embargo_violations"] == 0


def test_cpcv_stress_detects_a_broken_split():
    """Negative control: if the leakage check is fed a split whose train
    indices intrude into the test window, it must raise."""
    df = synthesize_diurnal_rows(seed=3, days=1, base_rate_per_s=1.0)
    ts = df["t_start"].to_numpy()
    split = next(purged_cpcv_splits(ts, n_groups=6,
                                    label_horizon_us=60_000_000,
                                    embargo_us=30_000_000))
    # sabotage: force a train row inside the purge window
    lo, hi = split["test_bounds"]
    inside = np.where((ts >= lo - 30_000_000) & (ts <= hi + 90_000_000))[0]
    assert len(inside) > 0
    bad = dict(split)
    bad["train_idx"] = np.concatenate([split["train_idx"], inside[:1]])
    with pytest.raises(AssertionError, match="label-window overlaps"):
        assert_no_leakage(bad, ts, 60_000_000, 30_000_000)


# ---------------------------------------------------------------------
# 3. Correlation / dispersion diagnostics (descriptive only)
# ---------------------------------------------------------------------

def test_diagnostics_report_all_three_clock_pairs():
    df = synthesize_diurnal_rows(seed=5, days=3, base_rate_per_s=1.0)
    diag = duration_diagnostics(df, tick=0.1, depth_threshold=5.0)
    assert diag["n_episodes"] >= 3
    for pair in ("wall_vs_raw_event", "wall_vs_vol_filtered_event",
                 "raw_vs_vol_filtered_event"):
        c = diag["correlations"][pair]
        assert np.isfinite(c["pearson"]) or np.isnan(c["pearson"])
        assert "spearman" in c
    for clock in ("wall_clock_comp_dur_us", "raw_event_dur",
                  "vol_filtered_event_dur",
                  "wall_seconds_per_filtered_event"):
        d = diag["dispersion"][clock]
        assert {"mean", "median", "std", "cv", "iqr_over_median"} <= set(d)
    assert 0.0 <= diag["flicker_share_mean"] <= 1.0
    # descriptive-only marker
    assert "no predictive" in diag["note"]


def test_burst_hours_inflate_raw_but_not_filtered_event_duration():
    """In the synthetic world, burst hours carry a 55% flicker share vs 5%
    in quiet hours - so raw event duration must correlate with the burst
    cycle MORE than the volume-filtered clock does (the audit's whole
    point, verified descriptively)."""
    df = synthesize_diurnal_rows(seed=9, days=3, base_rate_per_s=1.0)
    ep = dual_clock_durations(df, tick=0.1, depth_threshold=5.0)
    hr = (ep["t_start_us"] // 3_600_000_000 % 24)
    burst = hr.isin([13, 14, 15]).to_numpy()
    if burst.any() and (~burst).any():
        raw_gap = (ep["raw_event_dur"].to_numpy()[burst].mean()
                   - ep["raw_event_dur"].to_numpy()[~burst].mean())
        filt_gap = (ep["vol_filtered_event_dur"].to_numpy()[burst].mean()
                    - ep["vol_filtered_event_dur"].to_numpy()[~burst].mean())
        # burst episodes must be flicker-heavier than quiet ones
        assert (ep["flicker_share"].to_numpy()[burst].mean()
                > ep["flicker_share"].to_numpy()[~burst].mean())
        assert raw_gap > filt_gap
