"""Macro-event right-censoring for survival spells. EX-ANTE TIMELINE ONLY.

The `surprise_note` column of data/macro_timeline.csv is POST-EVENT
information. It is never read: load_timeline() drops it unconditionally and
asserts it is empty, so no model can consume a surprise.

Windows: [event_time_utc - PRE_BUFFER, expected_resolution_utc] per event,
in int64 UTC microseconds. A spell starting at t0 with horizon h is
right-censored at the first window start strictly after t0 if that start
falls within (t0, t0+h]; a barrier touch after the censor point is discarded
(event=0, duration=window_start - t0). Spells starting inside a window are
dropped (zero exposure).
"""

from pathlib import Path

import numpy as np
import pandas as pd

PRE_BUFFER_US = 15 * 60 * 10**6
DEFAULT_RESOLUTION_MIN = 30


def _parse_ts(date_s: pd.Series, time_s: pd.Series) -> pd.Series:
    dt = pd.to_datetime(
        date_s.astype(str).str.strip() + " " + time_s.astype(str).str.strip(),
        utc=True, errors="raise", format="mixed",
    )
    return (dt.astype("int64") // 1000).astype("int64")


def load_timeline(path) -> pd.DataFrame:
    """Load the ex-ante macro timeline. surprise_note is dropped and asserted
    empty; only scheduled (pre-announced) event times are returned."""
    df = pd.read_csv(path)
    if "surprise_note" in df.columns:
        vals = df["surprise_note"].astype(str).str.strip()
        assert (vals.isin(["", "nan", "None"])).all(), (
            "surprise_note must be empty: it is post-event information and "
            "must never enter an ex-ante model"
        )
        df = df.drop(columns=["surprise_note"])
    req = {"event_id", "event_date_utc", "event_time_utc", "event_type"}
    if not req.issubset(df.columns):
        raise ValueError(f"timeline missing columns: {req - set(df.columns)}")
    out = df.copy()
    out["event_ts_us"] = _parse_ts(df["event_date_utc"], df["event_time_utc"])
    if "expected_resolution_utc" in df.columns and df["expected_resolution_utc"].notna().any():
        res = df["expected_resolution_utc"].astype(str).str.strip()
        # time-only values combine with the event date
        has_date = res.str.contains(r"\d{4}-\d{2}-\d{2}")
        res_dt = pd.to_datetime(
            np.where(has_date, res, df["event_date_utc"].astype(str) + " " + res),
            utc=True, errors="raise", format="mixed",
        )
        out["resolution_ts_us"] = (res_dt.astype("int64") // 1000).astype("int64")
        missing = df["expected_resolution_utc"].isna()
        if missing.any():
            out.loc[missing, "resolution_ts_us"] = (
                out.loc[missing, "event_ts_us"] + DEFAULT_RESOLUTION_MIN * 60 * 10**6
            )
    else:
        out["resolution_ts_us"] = out["event_ts_us"] + DEFAULT_RESOLUTION_MIN * 60 * 10**6
    out["window_start_us"] = out["event_ts_us"] - PRE_BUFFER_US
    out["window_end_us"] = np.maximum(out["resolution_ts_us"], out["event_ts_us"])
    return out.sort_values("event_ts_us").reset_index(drop=True)


def macro_windows(timeline: pd.DataFrame):
    """Sorted (n,2) int64 array of [window_start_us, window_end_us]."""
    w = timeline[["window_start_us", "window_end_us"]].to_numpy(dtype="int64")
    order = np.argsort(w[:, 0])
    return w[order]


def censor_spells(spells: pd.DataFrame, windows: np.ndarray) -> pd.DataFrame:
    """Right-censor spells entering scheduled macro windows.

    spells columns: t0_us, horizon_us, duration_us, event (plus any others).
    Returns a copy with adjusted duration_us/event and a censored_macro flag.
    Spells with t0 inside a window are dropped.
    """
    req = {"t0_us", "horizon_us", "duration_us", "event"}
    if not req.issubset(spells.columns):
        raise ValueError(f"spells missing columns: {req - set(spells.columns)}")
    out = spells.copy()
    t0 = out["t0_us"].to_numpy(dtype="int64")
    starts = windows[:, 0]
    ends = windows[:, 1]
    # drop spells starting inside any window
    i = np.searchsorted(starts, t0, side="right") - 1
    inside = (i >= 0) & (t0 <= ends[np.maximum(i, 0)])
    out = out[~inside].reset_index(drop=True)
    t0 = out["t0_us"].to_numpy(dtype="int64")
    dur = out["duration_us"].to_numpy(dtype="int64")
    ev = out["event"].to_numpy(dtype="int64")
    hor = out["horizon_us"].to_numpy(dtype="int64")
    # first window start strictly after t0
    j = np.searchsorted(starts, t0, side="right")
    j = np.minimum(j, len(starts) - 1) if len(starts) else np.zeros(len(t0), dtype=int)
    next_start = starts[j] if len(starts) else np.full(len(t0), np.iinfo("int64").max)
    eff_h = np.minimum(hor, np.maximum(next_start - t0, 0))
    censor_at = np.minimum(t0 + dur, t0 + eff_h)
    hit_macro = (t0 + dur) > (t0 + eff_h)
    new_dur = np.where(hit_macro, eff_h, dur)
    new_ev = np.where(hit_macro, 0, ev)
    out["duration_us"] = new_dur
    out["event"] = new_ev
    out["censored_macro"] = hit_macro.astype("int8")
    out["horizon_us"] = hor
    return out


def main(argv=None) -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--timeline", type=Path, default=Path("data/macro_timeline.csv"))
    args = ap.parse_args(argv)
    tl = load_timeline(args.timeline)
    print(f"{len(tl)} ex-ante macro events "
          f"({tl['event_ts_us'].min()} .. {tl['event_ts_us'].max()} us)")
    for r in tl.itertuples():
        print(f"  {r.event_id:24s} {r.event_type:20s} "
              f"window [{r.window_start_us}, {r.window_end_us}]")


if __name__ == "__main__":
    main()
