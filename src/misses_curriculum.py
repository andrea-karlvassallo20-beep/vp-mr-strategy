"""The misses curriculum — the priming score's base rate, quantified.

Directive (Andrea, 2026-11-16): the quantified misses curriculum from the
null-time programme. The Tesla day proved a move can arrive unprimed;
that was one anecdote. This module makes it a base rate over the whole
board: enumerate every >=4-sigma day on the full-universe klines, look
up the priming state the NIGHT BEFORE each, and build the honest 2x2:

              moved (>=4 sigma)   did not move
    primed          A                  B
    not primed      C                  D

PRE-DECLARED PROTOCOL (fixed before the run, descriptive only):
  - universe: the living board (mega_dormancy_table.csv) - every series
    with a resolvable cached klines file;
  - move: |daily simple return| >= 4 x the trailing 20-day return std,
    sigma computed causally on days t-20..t-1 (the move day excluded);
  - primed at t-1 (the night before): the mega-universe primed rule,
    computed causally at t-1 - comp_days >= 20 consecutive days of
    rvol-percentile <= 33 (percentile within the trailing 756-day
    window) AND range_pos <= 0.35 (position of close in the trailing
    252-day range);
  - a series contributes series-days only where the full trailing
    window exists (no partial windows, no NaN percentiles);
  - the 2x2 is a DESCRIPTION. No claim is tested, no direction is
    predicted, C7's dataset stays sealed. If coverage A/(A+C) is near
    zero, that is the L2 phase's motivation stated as a number.

Output: paper/research/clue_scan/misses_curriculum.md + .json
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from surprise_ledger import _mega_data_file  # noqa: E402

CLUE = Path("paper/research/clue_scan")
MEGA_CSV = CLUE / "mega_dormancy_table.csv"
OUT_MD = CLUE / "misses_curriculum.md"
OUT_JSON = CLUE / "misses_curriculum.json"

SIGMA_WIN = 20
PCT_WIN = 756
RANGE_WIN = 252
RVOL_PCT_MAX = 33.0
COMP_DAYS_MIN = 20
RANGE_POS_MAX = 0.35
MOVE_SIGMA = 4.0


def priming_and_moves(close):
    """Causal per-day priming state and >=4-sigma move flags for one
    series. Returns (primed_night_before, moved) boolean arrays aligned
    to days, NaN-free windows only."""
    close = pd.Series(close, dtype=float).reset_index(drop=True)
    n = len(close)
    if n < PCT_WIN + SIGMA_WIN + 5:
        return None
    ret = close.pct_change()
    sigma = ret.rolling(SIGMA_WIN).std().shift(1)      # t-20..t-1, causal
    moved = (ret.abs() >= MOVE_SIGMA * sigma) & sigma.notna()

    rvol = ret.rolling(SIGMA_WIN).std()
    rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
    low_vol = (rvol_pct <= RVOL_PCT_MAX) & rvol_pct.notna()
    comp_days = low_vol.rolling(COMP_DAYS_MIN).sum()
    hi = close.rolling(RANGE_WIN).max()
    lo = close.rolling(RANGE_WIN).min()
    rng = (hi - lo).replace(0, np.nan)
    range_pos = (close - lo) / rng
    primed = ((comp_days >= COMP_DAYS_MIN)
              & (range_pos <= RANGE_POS_MAX)
              & range_pos.notna())
    primed_night_before = primed.shift(1, fill_value=False)
    valid = primed_night_before.notna() & moved.notna()
    return primed_night_before[valid], moved[valid]


def main():
    mega = pd.read_csv(MEGA_CSV)
    cells = {"A": 0, "B": 0, "C": 0, "D": 0}
    n_series = 0
    n_moves = 0
    failures = []
    for _, r in mega.iterrows():
        data_file = _mega_data_file(r["series"], r.get("venue", ""))
        if not data_file:
            continue
        try:
            df = pd.read_csv(data_file)
        except Exception:
            failures.append(r["series"])
            continue
        if "close" not in df.columns or len(df) < PCT_WIN + SIGMA_WIN + 5:
            continue
        out = priming_and_moves(df["close"].to_numpy())
        if out is None:
            continue
        p, m = out
        n_series += 1
        a = int((p & m).sum())
        b = int((p & ~m).sum())
        c = int((~p & m).sum())
        d = int((~p & ~m).sum())
        cells["A"] += a
        cells["B"] += b
        cells["C"] += c
        cells["D"] += d
        n_moves += a + c

    A, B, C, D = (cells[k] for k in "ABCD")
    N = A + B + C + D
    coverage = A / (A + C) if (A + C) else float("nan")
    p_move_given_prim = A / (A + B) if (A + B) else float("nan")
    p_move_given_unprim = C / (C + D) if (C + D) else float("nan")
    lift = (p_move_given_prim / p_move_given_unprim
            if p_move_given_unprim else float("nan"))
    priming_rate = (A + B) / N if N else float("nan")

    res = {
        "n_series": n_series, "n_series_days": N,
        "n_moves_4sigma": n_moves, "cells": cells,
        "coverage_A_over_AC": coverage,
        "p_move_given_primed": p_move_given_prim,
        "p_move_given_not_primed": p_move_given_unprim,
        "lift": lift, "priming_rate": priming_rate,
        "failures": failures,
        "protocol": {
            "move": f"|daily ret| >= {MOVE_SIGMA} x trailing {SIGMA_WIN}d std (causal)",
            "primed_night_before": (f"comp_days>={COMP_DAYS_MIN} of rvol_pct<={RVOL_PCT_MAX} "
                                    f"(pct in trailing {PCT_WIN}d) and range_pos<={RANGE_POS_MAX} "
                                    f"(trailing {RANGE_WIN}d), evaluated at t-1"),
            "descriptive_only": True,
        },
    }
    OUT_JSON.write_text(json.dumps(res, indent=2, default=float))
    lines = [
        "# The misses curriculum — the priming score's base rate",
        "",
        "Descriptive only. Pre-declared protocol (see src/misses_curriculum.py",
        "docstring); no claim tested, no direction predicted; C7 stays sealed.",
        "",
        f"- Series analyzed: **{n_series}** (living board; {len(failures)} unresolvable)",
        f"- Series-days: **{N:,}**",
        f"- >=4-sigma days: **{n_moves:,}**",
        "",
        "## The honest 2x2",
        "",
        "|              | moved (>=4 sigma) | did not move |     |",
        "|--------------|-------------------|--------------|-----|",
        f"| **primed**   | A = {A:,}         | B = {B:,}     |     |",
        f"| **not primed** | C = {C:,}       | D = {D:,}     |     |",
        "",
        "## The numbers that matter",
        "",
        f"- **Coverage A/(A+C)** — of all >=4-sigma days, the fraction primed the",
        f"  night before: **{coverage:.3f}**",
        f"- P(move | primed) = {p_move_given_prim:.5f}",
        f"- P(move | not primed) = {p_move_given_unprim:.5f}",
        f"- **Lift** = {lift:.2f}",
        f"- Base priming rate on the board: {priming_rate:.3f}",
        "",
        "## Reading",
        "",
        "If coverage is near zero, the answer is stated as a number: the daily",
        "grain cannot rank the future, and the L2 phase is mandatory — the",
        "signal, if it exists, lives where daily scores cannot see it. If the",
        "lift is near 1, priming carries no information about the move. These",
        "are descriptions; the only path to a claim remains C7/C1-L2 kill lines.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"misses curriculum: {n_series} series, {N:,} series-days, "
          f"{n_moves:,} moves -> {OUT_MD}")
    print(f"coverage={coverage:.3f} lift={lift:.2f} "
          f"P(move|primed)={p_move_given_prim:.5f} "
          f"P(move|unprimed)={p_move_given_unprim:.5f}")


if __name__ == "__main__":
    main()
