"""The closeness dossier - each prestate criterion's separation from
the actual event, in the owner's triad order (price, volume, time).

Directive (Andrea, 2026-11-18, in-session): "look historically all we
saw and start building criteria list by closeness to actual event
starting from price and then volume and then time". Authorized as
MEASURED DESCRIPTIVE work in parallel with the null-time deep-read
queue (the "both in parallel" decision of 2026-11-18).

PRE-DECLARED PROTOCOL (fixed before the run, descriptive only):
  - universe: the cached discovery archive present in this clone,
    paper/research/data/<series>.csv (daily OHLCV, the archive the
    1,461-move census was built from); the mega-board kline cache
    (the misses curriculum's 873-series board) is NOT present in
    this clone, so the run covers the cache-present subset: every
    archive series with >= 781 days of history, class taken from
    the census table where available; the subset difference is
    declared here, never silently ignored;
  - event: |daily simple return| >= 4 x the trailing 20-day return
    std, sigma computed causally on days t-20..t-1 (identical to the
    misses curriculum's move);
  - evaluation point: the night BEFORE each series-day t (state at
    t-1), windows NaN-free only;
  - closeness = lead-time horizons: "a >=4-sigma move occurs within
    K days AFTER the evaluation day", K in {5, 10, 20, 60};
  - criteria variables, computed causally at the evaluation point,
    in the owner's triad order:
      PRICE  - rvol_pct (20d vol percentile in trailing 756d),
               range_pos (close position in trailing 252d range),
               stretch_z ((close - 252d mean) / 252d std),
               ret30 (trailing 30d simple return)
      VOLUME - vol_ratio (volume / trailing 20d median volume)
      TIME   - comp_days (consecutive days rvol_pct <= 33, capped at
               756), days_since_move (nights since the last
               >=4-sigma move, capped at 252)
  - statistic: the rank AUC (Mann-Whitney) of each variable between
    event nights (move within K days) and non-event nights, pooled
    over all series-days; AUC > 0.5 means HIGHER values sit closer to
    the event; 0.5 = no separation. Also computed for the pooled
    crypto-only subset as a secondary column.
  - this is a DESCRIPTION of the sealed discovery panel. No claim is
    tested, no direction is predicted, no threshold is chosen; the
    confirm split (W2) comes LATER on data this run never touches.

Output: paper/research/clue_scan/closeness_dossier.csv and
paper/research/clue_scan/closeness_dossier.md
"""

import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "closeness_dossier.csv"
OUT_MD = CLUE / "closeness_dossier.md"

SIGMA_WIN = 20
PCT_WIN = 756
RANGE_WIN = 252
TREND_WIN = 252
RVOL_PCT_MAX = 33.0
COMP_DAYS_MIN = 20
MOVE_SIGMA = 4.0
HORIZONS = (5, 10, 20, 60)
TIME_CAP = 252
NEED = PCT_WIN + SIGMA_WIN + 5

VARS = ("rvol_pct", "range_pos", "stretch_z", "ret30",
        "vol_ratio", "comp_days", "days_since_move")


def series_state(close, volume):
    """Causal per-night state and forward event labels for one
    series. Returns (dict of arrays at evaluation night t-1 -> used
    for day t forward labels, class info excluded)."""
    close = pd.Series(close, dtype=float).reset_index(drop=True)
    volume = pd.Series(volume, dtype=float).reset_index(drop=True)
    n = len(close)
    if n < NEED:
        return None
    ret = close.pct_change()

    sigma = ret.rolling(SIGMA_WIN).std().shift(1)
    move_day = (ret.abs() >= MOVE_SIGMA * sigma) & sigma.notna()

    rvol = ret.rolling(SIGMA_WIN).std()
    rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
    low_vol = (rvol_pct <= RVOL_PCT_MAX) & rvol_pct.notna()
    comp_days = low_vol.rolling(COMP_DAYS_MIN).sum()

    hi = close.rolling(RANGE_WIN).max()
    lo = close.rolling(RANGE_WIN).min()
    rng = (hi - lo).replace(0, np.nan)
    range_pos = (close - lo) / rng

    mean = close.rolling(TREND_WIN).mean()
    sd = close.rolling(TREND_WIN).std()
    stretch_z = (close - mean) / sd.replace(0, np.nan)
    ret30 = close.pct_change(30)

    vol_med = volume.rolling(SIGMA_WIN).median()
    vol_ratio = volume / vol_med.replace(0, np.nan)

    move_flag = move_day.astype(float)
    move_flag[~move_day & move_day.notna()] = 0.0
    gap = np.full(n, np.nan)
    last = np.nan
    mfa = move_flag.to_numpy()
    for i in range(n):
        if mfa[i] == 1.0:
            last = 0.0
        elif last == last:
            last += 1.0
        gap[i] = last  # NaN until the first move in the series
    # days_since_move at t (capped), shifted to t-1 below
    days_since = pd.Series(gap).clip(upper=TIME_CAP)

    state = {
        "rvol_pct": rvol_pct,
        "range_pos": range_pos,
        "stretch_z": stretch_z,
        "ret30": ret30,
        "vol_ratio": vol_ratio,
        "comp_days": comp_days,
        "days_since_move": days_since,
    }

    out = {}
    for name, s in state.items():
        out[name] = s.shift(1)

    # forward event: a move occurs within K days AFTER the
    # evaluation day; label[i] = any(move_day[j], j in i+1..i+K)
    moved_k = {}
    for k in HORIZONS:
        rev = move_day.iloc[::-1]
        rev_max = rev.rolling(k, min_periods=1).max()
        moved_k[k] = rev_max.iloc[::-1].shift(-1)
    return out, moved_k


def auc(pos, neg):
    """Mann-Whitney AUC of pos vs neg (higher pos -> >0.5)."""
    pos = pos[~np.isnan(pos)]
    neg = neg[~np.isnan(neg)]
    if len(pos) < 50 or len(neg) < 50:
        return float("nan"), len(pos), len(neg)
    allv = np.concatenate([pos, neg])
    order = np.argsort(allv, kind="mergesort")
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(allv) + 1)
    # mid-ranks for ties
    sorted_vals = allv[order]
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and sorted_vals[j + 1] == sorted_vals[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    rp = ranks[:len(pos)].sum()
    return (rp - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)), len(pos), len(neg)


def main():
    census = pd.read_csv(CLUE / "move_study.csv")
    class_lookup = dict(zip(census["series"], census["class"]))
    buckets = {(name, k): {"all": [[], []], "crypto": [[], []]}
               for name in VARS for k in HORIZONS}
    n_series = 0
    failures = []
    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            failures.append(data_file.stem)
            continue
        if "close" not in df.columns or len(df) < NEED:
            continue
        vol = (df["volume"].to_numpy()
               if "volume" in df.columns else np.full(len(df), np.nan))
        out = series_state(df["close"].to_numpy(), vol)
        if out is None:
            continue
        state, moved_k = out
        series_name = data_file.stem
        n_series += 1
        is_crypto = class_lookup.get(series_name, "") == "crypto"

        for name in VARS:
            s = state[name].to_numpy(dtype=float)
            if np.all(np.isnan(s)):
                continue
            for k in HORIZONS:
                lab = moved_k[k].to_numpy(dtype=float)
                ok = ~np.isnan(s) & ~np.isnan(lab)
                if not ok.any():
                    continue
                sv = s[ok]
                lv = lab[ok] > 0
                pos, neg = sv[lv], sv[~lv]
                b = buckets[(name, k)]
                b["all"][0].append(pos)
                b["all"][1].append(neg)
                if is_crypto:
                    b["crypto"][0].append(pos)
                    b["crypto"][1].append(neg)

    rows = []
    for name in VARS:
        for k in HORIZONS:
            b = buckets[(name, k)]
            for subset in ("all", "crypto"):
                pos = (np.concatenate(b[subset][0])
                       if b[subset][0] else np.array([]))
                neg = (np.concatenate(b[subset][1])
                       if b[subset][1] else np.array([]))
                a, np_, nn_ = auc(pos, neg)
                rows.append({".Variable": name, "horizon_k": k,
                             "on": subset, "n_event": np_, "n_nonevent": nn_,
                             "auc": round(a, 4) if a == a else ""})

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    meta = {"n_series": n_series, "failures": failures}
    print(meta)
    print(f"wrote {OUT_CSV} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
