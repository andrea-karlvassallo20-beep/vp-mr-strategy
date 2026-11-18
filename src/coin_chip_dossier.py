"""The coin-chip dossier - conditional DIRECTION tilts on the archive
(the owner's "which way is the coin chipped" question, measured).

Directive (Andrea, 2026-11-18, in-session): "everyone gets to flip a
coin, but you wanna make sure you know which way it has been
chipped... after nukes highest likelihood to go up, or after a
base is built." Owner-authorized measured descriptive work in the
parallel regime (programme log sessions 34+).

PRE-DECLARED PROTOCOL (fixed before the run, descriptive only):
  - universe: the cached discovery archive present in this clone,
    paper/research/data/<series>.csv (same as the closeness
    dossier, session 34); every series with >= 781 days;
  - states, evaluated causally at the evaluation night (t-1):
      * post_nuke_down  - a >=4-sigma NEGATIVE day occurred within
        the last 2 days;
      * post_nuke_up    - a >=4-sigma POSITIVE day occurred within
        the last 2 days;
      * primed          - the frozen priming rule (comp_days >= 20,
        rvol_pct <= 33, range_pos <= 0.35);
      * base            - rvol_pct <= 33 AND range_pos <= 0.15
        (quiet + near the base of the 252d range, no compression
        requirement: the owner's "base is built" read);
      * all             - every evaluation night (the baseline);
  - labels:
      drift: mean and median of the K-day forward simple return,
        K in {5, 20, 60}, plus P(forward K-day return > 0);
      first_move_dir: of the >=4-sigma moves occurring within the
        next 60 days, whether the FIRST one is up, plus its mean
        size and the base rate (moves can be absent: label NaN);
      upshare_of_moves: of all >=4-sigma days in the next 60, the
        fraction that are UP;
  - pooling: over all series-days with full causal windows (same
    NaN-free discipline as the closeness dossier); medians pooled
    by simple concatenation (declared: no per-series weighting);
  - DECLARED data-quality filters (fixed before the second run
    after dead-coin artifacts produced inf returns in the first):
    evaluation nights with a non-positive or sub-cent close are
    invalid; forward returns outside [-0.95, +10] are dropped as
    delisting artifacts; the up-share of moves is computed ONLY
    over nights with at least one >=4-sigma move in the window;
  - this is a DESCRIPTION of the discovery archive. No claim is
    tested, no threshold chosen, no instrument armed; the
    confirmation split remains mandatory before any conditional
    becomes evidence. No kill line moves; nothing trades live.

Output: paper/research/clue_scan/coin_chip_dossier.csv and
paper/research/clue_scan/coin_chip_dossier.md
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "coin_chip_dossier.csv"
OUT_MD = CLUE / "coin_chip_dossier.md"

SIGMA_WIN = 20
PCT_WIN = 756
RANGE_WIN = 252
RVOL_PCT_MAX = 33.0
COMP_DAYS_MIN = 20
MOVE_SIGMA = 4.0
NUKE_LOOKBACK = 2
FWD_HORIZONS = (5, 20, 60)
MOVE_HORIZON = 60
NEED = PCT_WIN + SIGMA_WIN + 5

STATES = ("post_nuke_down", "post_nuke_up", "primed", "base", "all")


def series_panel(close):
    close = pd.Series(close, dtype=float).reset_index(drop=True)
    n = len(close)
    if n < NEED:
        return None
    valid_close = (close > 0.01).astype(float).shift(1).fillna(0.0)
    ret = close.pct_change()

    sigma = ret.rolling(SIGMA_WIN).std().shift(1)
    move = (ret.abs() >= MOVE_SIGMA * sigma) & sigma.notna()
    move_down = (ret <= -MOVE_SIGMA * sigma) & sigma.notna()
    move_up = (ret >= MOVE_SIGMA * sigma) & sigma.notna()

    state = {}
    dn = move_down.astype(float)
    up = move_up.astype(float)
    state["post_nuke_down"] = dn.rolling(NUKE_LOOKBACK).max()
    state["post_nuke_up"] = up.rolling(NUKE_LOOKBACK).max()

    rvol = ret.rolling(SIGMA_WIN).std()
    rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
    low_vol = (rvol_pct <= RVOL_PCT_MAX) & rvol_pct.notna()
    comp_days = low_vol.rolling(COMP_DAYS_MIN).sum()
    hi = close.rolling(RANGE_WIN).max()
    lo = close.rolling(RANGE_WIN).min()
    rng = (hi - lo).replace(0, np.nan)
    range_pos = (close - lo) / rng
    state["primed"] = (((comp_days >= COMP_DAYS_MIN)
                        & (range_pos <= 0.35)
                        & range_pos.notna()).astype(float))
    state["base"] = (((rvol_pct <= RVOL_PCT_MAX)
                      & (range_pos <= 0.15)
                      & range_pos.notna()).astype(float))
    for k in ("post_nuke_down", "post_nuke_up", "primed", "base"):
        state[k] = state[k].shift(1)
    state["all"] = pd.Series(np.ones(n))

    # forward K-day return
    fwd = {}
    for k in FWD_HORIZONS:
        fwd[k] = close.shift(-k) / close - 1.0

    # first >=4-sigma move direction within MOVE_HORIZON days
    n_moves = move.rolling(MOVE_HORIZON).max().shift(-MOVE_HORIZON)
    # signed first move: smallest lag j>=1 with move[j], sign of ret[j]
    m = n
    first_dir = np.full(n, np.nan)
    ret_a = ret.to_numpy()
    move_a = move.to_numpy()
    up_a = move_up.to_numpy()
    for i in range(n - MOVE_HORIZON - 1):
        for j in range(i + 1, min(i + MOVE_HORIZON, m - 1) + 1):
            if move_a[j]:
                first_dir[i] = 1.0 if up_a[j] else -1.0
                break
    # share of UPMOVES among all moves in the window (nights with
    # at least one move only): up-days / (up-days + down-days)
    n_up = (move_up.astype(float).rolling(MOVE_HORIZON).sum()
            .shift(-MOVE_HORIZON))
    n_dn = (move_down.astype(float).rolling(MOVE_HORIZON).sum()
            .shift(-MOVE_HORIZON))
    tot = n_up + n_dn
    up_share = (n_up / tot.replace(0, np.nan)).where(tot > 0)

    return state, fwd, pd.Series(first_dir), up_share, valid_close


def main():
    rows = []
    acc = {s: {"fwd": {k: [] for k in FWD_HORIZONS},
               "first": [], "upshare": []} for s in STATES}
    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if "close" not in df.columns or len(df) < NEED:
            continue
        out = series_panel(df["close"].to_numpy())
        if out is None:
            continue
        state, fwd, first_dir, up_share, valid_close = out
        vc = valid_close.to_numpy(dtype=float)
        for s in STATES:
            mask = state[s].to_numpy(dtype=float)
            ok = ~np.isnan(mask) & (mask > 0) & (vc > 0)
            if not ok.any():
                continue
            for k in FWD_HORIZONS:
                v = fwd[k].to_numpy(dtype=float)[ok]
                v = v[(~np.isnan(v)) & (v > -0.95) & (v < 10.0)]
                acc[s]["fwd"][k].extend(v.tolist())
            fd = first_dir.to_numpy(dtype=float)[ok]
            acc[s]["first"].extend(fd[~np.isnan(fd)].tolist())
            us = up_share.to_numpy(dtype=float)[ok]
            acc[s]["upshare"].extend(us[~np.isnan(us)].tolist())

    for s in STATES:
        row = {"state": s}
        for k in FWD_HORIZONS:
            v = np.array(acc[s]["fwd"][k])
            row[f"mean_fwd{k}"] = round(float(v.mean()), 5) if len(v) else ""
            row[f"median_fwd{k}"] = round(float(np.median(v)), 5) if len(v) else ""
            row[f"P_up_fwd{k}"] = round(float((v > 0).mean()), 4) if len(v) else ""
            row[f"n_fwd{k}"] = len(v)
        fd = np.array(acc[s]["first"])
        us = np.array(acc[s]["upshare"])
        row["P_first_move_up"] = (round(float((fd > 0).mean()), 4)
                                  if len(fd) else "")
        row["n_first"] = len(fd)
        row["mean_upshare_60"] = (round(float(us.mean()), 4)
                                  if len(us) else "")
        rows.append(row)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
