"""The misses curriculum, quantified: the honest 2x2 the priming score
has never had (null-time queue item 2, pre-declared protocol).

The existing misses tables (missed_moves*.csv, misses_prestate_profile.csv)
condition on MOVES only: they measure the coverage question "of the moves,
how many were primed the night before?" The question they cannot answer is
the base-rate question, because it needs the silent denominator:

    primed   x  moved      the hits
    primed   x  silent     the false alarms
    unprimed x  moved      the misses (the curriculum's namesake)
    unprimed x  silent     the vast quiet majority

Descriptive protocol (pre-declared, frozen before any run on real klines):

  universe   every cached series in data/raw/top500_klines (crypto) and
             data/raw/eq_commodity_klines (equity/commodity), >= 120 bars.
  state      the sealed C7 priming rule exactly as frozen everywhere else:
             comp_days >= 20 AND rvol_pct <= 33 AND range_pos <= 0.35,
             computed causally at day t from strictly earlier data, with
             the SAME formulas as move_study._pre_move_state (a parity
             test pins this module to that definition; drift is a bug).
  moved      at least one >=4-sigma day (|ret| >= 4x trailing 60d sigma,
             the dormancy metric) STRICTLY INSIDE the next H=10 bars
             (the surprise ledger's horizon; a row exists only when the
             full horizon is past - the same strict gate the ledger uses).
  grain      one row per series-day, all classes pooled per class.
             Overlapping windows are counted as they are lived: every day
             is a decision day. No dedup, no smoothing, no claim.

Outputs: paper/research/clue_scan/misses_2x2.csv (the per-class table)
and a dated markdown report. DESCRIPTIVE ONLY: no direction, no kill
line, no claim tested; the multiplicity caveat binds; the 0.505
direction boundary remains in force.
"""

import argparse
import bisect
import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from move_study import _pre_move_state  # the frozen definitions, pinned

ROOT = Path(__file__).resolve().parents[1]
K500 = ROOT / "data/raw/top500_klines"
KEQ = ROOT / "data/raw/eq_commodity_klines"
CLUE = ROOT / "paper/research/clue_scan"
HORIZON = 10
MIN_BARS = 120
WARM = 60          # _pre_move_state requires i >= 60
RVOL_WIN = 20      # move_study's realized-vol window
SIG_WIN = 60       # the dormancy 4-sigma window


def primed_flags(close: np.ndarray, vol: np.ndarray) -> np.ndarray:
    """Per-day primed state, vectorized over the frozen rule.

    Same math as move_study._pre_move_state evaluated at every index;
    tests/misses_2x2 test asserts per-day parity with the original.
    """
    n = len(close)
    ret = np.concatenate([[0.0], np.diff(np.log(close))])
    rvol = pd.Series(ret).rolling(RVOL_WIN).std().to_numpy()
    out = np.zeros(n, dtype=bool)
    hist_sorted: list[float] = []   # valid rvol history, kept sorted
    for t in range(n):
        v = rvol[t]
        if not np.isnan(v):
            bisect.insort(hist_sorted, float(v))
        if t < WARM or np.isnan(v) or len(hist_sorted) < 40:
            continue
        # exact positional percentile of v within its own valid history
        rank_le = bisect.bisect_right(hist_sorted, float(v))
        rvol_pct = 100.0 * rank_le / len(hist_sorted)
        thresh_pos = 0.33 * (len(hist_sorted) - 1)
        lo = int(np.floor(thresh_pos))
        frac = thresh_pos - lo
        thresh = (hist_sorted[lo] * (1 - frac) +
                  hist_sorted[min(lo + 1, len(hist_sorted) - 1)] * frac)
        comp = 0
        k = t
        while k >= 0 and not np.isnan(rvol[k]) and rvol[k] <= thresh:
            comp += 1
            k -= 1
        win = min(252, t + 1)
        lo, hi = np.min(close[t + 1 - win: t + 1]), np.max(close[t + 1 - win: t + 1])
        range_pos = (close[t] - lo) / (hi - lo) if hi > lo else 0.5
        out[t] = comp >= 20 and rvol_pct <= 33 and range_pos <= 0.35
    return out


def moved_flags(close: np.ndarray) -> np.ndarray:
    """True at t if a >=4-sigma day occurs strictly inside (t, t+H]."""
    ret = pd.Series(close).pct_change()
    sigma = ret.rolling(SIG_WIN).std()
    big = (ret.abs() >= 4.0 * sigma).fillna(False).to_numpy()
    n = len(close)
    csum = np.concatenate([[0], np.cumsum(big)])
    out = np.zeros(n, dtype=bool)
    for t in range(n):
        j0, j1 = min(t + 1, n), min(t + 1 + HORIZON, n)
        out[t] = (csum[j1] - csum[j0]) > 0
    return out


def series_2x2(name: str, cls: str, df: pd.DataFrame) -> dict | None:
    close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
    if len(close) < MIN_BARS or np.isnan(close).any():
        return None
    vol = (df["volume"].fillna(0).to_numpy(float)
           if "volume" in df.columns else np.zeros(len(close)))
    primed = primed_flags(close, vol)
    moved = moved_flags(close)
    n = len(close)
    # only days whose full horizon is strictly past
    last = n - 1 - HORIZON
    if last < WARM:
        return None
    days = np.arange(WARM, last + 1)
    p, m = primed[days], moved[days]
    return {
        "series": name, "class": cls, "n_days": int(len(days)),
        "n_primed": int(p.sum()),
        "primed_moved": int((p & m).sum()),
        "primed_silent": int((p & ~m).sum()),
        "unprimed_moved": int((~p & m).sum()),
        "unprimed_silent": int((~p & ~m).sum()),
    }


def build(k500: Path = K500, keq: Path = KEQ) -> pd.DataFrame:
    rows = []
    for f in sorted(k500.glob("*.csv")):
        r = series_2x2(f.stem, "crypto", pd.read_csv(f))
        if r:
            rows.append(r)
    for f in sorted(keq.glob("*.csv")):
        r = series_2x2(f.stem, "eq_commodity", pd.read_csv(f))
        if r:
            rows.append(r)
    return pd.DataFrame(rows)


def aggregate(per_series: pd.DataFrame) -> pd.DataFrame:
    g = per_series.groupby("class")[["primed_moved", "primed_silent",
                                     "unprimed_moved", "unprimed_silent",
                                     "n_days", "n_primed"]].sum()
    out = []
    for cls, r in g.iterrows():
        pm, ps = r["primed_moved"], r["primed_silent"]
        um, us = r["unprimed_moved"], r["unprimed_silent"]
        n = pm + ps + um + us
        p_move = (pm + um) / n
        p_move_primed = pm / (pm + ps) if (pm + ps) else np.nan
        p_move_unprimed = um / (um + us) if (um + us) else np.nan
        lift = (p_move_primed / p_move_unprimed
                if p_move_unprimed and p_move_unprimed > 0 else np.nan)
        out.append({
            "class": cls, "series_days": int(n),
            "primed_days": int(r["n_primed"]),
            "primed_frac": r["n_primed"] / n,
            "base_rate_move": p_move,
            "p_move_given_primed": p_move_primed,
            "p_move_given_unprimed": p_move_unprimed,
            "lift_primed_vs_unprimed": lift,
            "false_alarm_rate": ps / (pm + ps) if (pm + ps) else np.nan,
            "coverage_of_moves": pm / (pm + um) if (pm + um) else np.nan,
        })
    return pd.DataFrame(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=CLUE)
    args = ap.parse_args()
    per_series = build()
    if per_series.empty:
        print("no series with enough history found (are the klines cached?)")
        return 1
    table = aggregate(per_series)
    per_series.to_csv(args.out_dir / "misses_2x2_per_series.csv", index=False)
    table.to_csv(args.out_dir / "misses_2x2.csv", index=False)
    date = dt.date.today().isoformat()
    lines = [
        f"# The misses curriculum 2x2 - {date}",
        "",
        "DESCRIPTIVE ONLY. The pre-declared protocol is in",
        "`src/misses_2x2.py`'s docstring (frozen priming rule, >=4-sigma",
        "day inside the strict 10-bar horizon, one row per series-day,",
        "parity-pinned to `move_study._pre_move_state`). No direction, no",
        "claim, no kill line touched; multiplicity binds.",
        "",
        table.to_markdown(index=False),
        "",
        "Reading discipline: a lift near 1.0 means the priming state",
        "carries no daily-grain information about whether a significant",
        "move arrives - the reference the C1-L2 spec must confront.",
        "The false-alarm rate is the cost side the coverage tables never",
        "showed. This table is the base-rate spine: a score without its",
        "base rate is a story; with it, it is a measurement.",
        "",
    ]
    md = args.out_dir.parent / f"misses_2x2_{date}.md"
    md.write_text("\n".join(lines))
    print(table.to_string(index=False))
    print(f"\nper-series and aggregate tables -> {args.out_dir}")
    print(f"report -> {md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
