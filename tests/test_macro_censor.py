import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import macro_censor as mc


def _timeline(tmp_path, rows):
    p = tmp_path / "macro_timeline.csv"
    header = ("event_id,event_date_utc,event_time_utc,all_day,event_type,"
              "asset_scope,expected_resolution_utc,surprise_note,source,confidence")
    lines = [header] + [",".join(r) for r in rows]
    p.write_text("\n".join(lines) + "\n")
    return p


def test_surprise_note_dropped_and_asserted_empty(tmp_path):
    p = _timeline(tmp_path, [
        ("FOMC-2026-06-17", "2026-06-17", "18:00", "false", "FOMC", "ALL",
         "2026-06-17 19:00", "", "federalreserve.gov", "confirmed"),
    ])
    tl = mc.load_timeline(p)
    assert "surprise_note" not in tl.columns
    assert len(tl) == 1
    assert tl["event_ts_us"].iloc[0] == pd.Timestamp(
        "2026-06-17 18:00", tz="UTC").value // 1000
    assert tl["window_end_us"].iloc[0] == pd.Timestamp(
        "2026-06-17 19:00", tz="UTC").value // 1000
    # 15-minute pre-buffer
    assert tl["window_start_us"].iloc[0] == tl["event_ts_us"].iloc[0] - 15 * 60 * 10**6


def test_surprise_note_nonempty_rejected(tmp_path):
    p = _timeline(tmp_path, [
        ("CPI-2026-06-10", "2026-06-10", "12:30", "false", "CPI", "ALL",
         "2026-06-10 13:00", "hot print", "bls.gov", "confirmed"),
    ])
    with pytest.raises(AssertionError):
        mc.load_timeline(p)


def test_censor_spells_right_censors_at_window_start(tmp_path):
    p = _timeline(tmp_path, [
        ("EV", "2026-06-17", "18:00", "false", "FOMC", "ALL",
         "2026-06-17 19:00", "", "src", "confirmed"),
    ])
    tl = mc.load_timeline(p)
    windows = mc.macro_windows(tl)
    H = 24 * 3600 * 10**6
    t0 = pd.Timestamp("2026-06-17 10:00", tz="UTC").value // 1000
    wstart = tl["window_start_us"].iloc[0]
    spells = pd.DataFrame({
        "t0_us": [t0, t0 + 3600 * 10**6, wstart + 60 * 10**6],
        "horizon_us": [H, H, H],
        "duration_us": [H, 3600 * 10**6, H],
        "event": [0, 1, 0],
    })
    out = mc.censor_spells(spells, windows)
    # spell 0: window starts inside (t0, t0+H] -> censored at window start
    r0 = out.iloc[0]
    assert r0["censored_macro"] == 1 and r0["event"] == 0
    assert r0["duration_us"] == wstart - t0
    # spell 1: event before the window -> untouched
    r1 = out.iloc[1]
    assert r1["censored_macro"] == 0 and r1["event"] == 1
    # spell 2: starts inside the window -> dropped
    assert len(out) == 2
    assert (out["t0_us"] < wstart).all()
