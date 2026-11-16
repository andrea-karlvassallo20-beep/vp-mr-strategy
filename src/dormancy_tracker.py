"""Dormancy heat map + missed-move tracker.

Two questions, asked honestly (descriptive only, no claims tested):

1. DORMANCY: across crypto (top-500 universe), commodities, indexes and
   equities - which assets have NOT made a move in a while? Metric:
   days since the last >=4 sigma day (|ret| >= 4x trailing 60d sigma),
   alongside the causal compression state (comp_days, rvol_pct,
   range_pos) and the sealed C7 priming rule (comp_days >= 20 AND
   rvol_pct <= 33 AND range_pos <= 0.35).

2. THE MISSES: of the 1,461 census episodes, which moves did our priming
   score NOT flag beforehand? These are the moves the score was blind to -
   they are the curriculum. We record their pre-move state signatures so
   they can be studied, not explained away.

Multiplicity caveat binding: scanning hundreds of series for dormancy finds
dormant series by construction. Nothing here is a claim, an edge, or a
prediction. The 0.505 direction boundary remains in force.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLUE = ROOT / "paper/research/clue_scan"
K500 = ROOT / "data/raw/top500_klines"
KEQ = ROOT / "data/raw/eq_commodity_klines"

PRIMED = "comp_days_ge_20_rvol_le_33_rangepos_le_035"


def _days_since_4sigma(csv_path: Path, min_hist: int = 90) -> dict | None:
    """Days since the last day with |ret| >= 4x trailing 60d sigma."""
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return None
    if "close" not in df.columns or len(df) < min_hist:
        return None
    c = pd.to_numeric(df["close"], errors="coerce").dropna()
    if len(c) < min_hist:
        return None
    ret = c.pct_change()
    sigma = ret.rolling(60).std()
    big = ret.abs() >= 4.0 * sigma
    big = big.fillna(False)
    n_days_since = int(len(c) - 1 - big.values.nonzero()[0][-1]) if big.any() else int(len(c) - 1)
    return {
        "n_hist": int(len(c)),
        "last_4sigma_days_ago": n_days_since,
        "n_4sigma_days_1y": int(big.iloc[-365:].sum()) if len(c) > 365 else int(big.sum()),
        "last_ret1d": float(ret.iloc[-1]),
    }


def build_dormancy_table() -> pd.DataFrame:
    """One row per series across all classes, ranked by dormancy."""
    rows = []
    top = pd.read_csv(CLUE / "top500_scan_table.csv")
    for _, r in top.iterrows():
        if bool(r.get("stablecoin", False)):
            continue
        k = _days_since_4sigma(K500 / f"{r['series']}.csv")
        if k is None:
            continue
        rows.append({
            "series": r["series"], "class": "crypto",
            "venue": r.get("venue", ""),
            **{c: r.get(c) for c in
               ("comp_days", "rvol_pct", "range_pos", "ret30", "primed_score")},
            **k,
            "primed": bool(r["comp_days"] >= 20 and r["rvol_pct"] <= 33
                           and r["range_pos"] <= 0.35),
        })
    eq = pd.read_csv(CLUE / "eq_commodity_scan_table.csv")
    for _, r in eq.iterrows():
        fname = r["yahoo_symbol"].replace("=", "_").replace("^", "")
        k = _days_since_4sigma(KEQ / f"{fname}.csv")
        if k is None:
            continue
        rows.append({
            "series": r["series"], "class": r["class"],
            "venue": "yahoo",
            **{c: r.get(c) for c in
               ("comp_days", "rvol_pct", "range_pos", "ret30", "primed_score")},
            **k,
            "primed": bool(r["comp_days"] >= 20 and r["rvol_pct"] <= 33
                           and r["range_pos"] <= 0.35),
        })
    df = pd.DataFrame(rows)
    # dormancy rank: long silence + coil state outranks mere quiet
    df["dormancy_score"] = (
        np.log1p(df["last_4sigma_days_ago"]) * 0.5
        + np.log1p(df["comp_days"].clip(lower=0)) * 0.3
        + (1.0 - df["rvol_pct"] / 100.0) * 0.2
    )
    df = df.sort_values("dormancy_score", ascending=False).reset_index(drop=True)
    return df


def build_missed_moves() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Episodes the priming score did NOT flag, plus detection stats."""
    ms = pd.read_csv(CLUE / "move_study.csv")
    ms["primed_before"] = (
        (ms["comp_days"] >= 20) & (ms["rvol_pct"] <= 33) & (ms["range_pos"] <= 0.35)
    )
    ms["study_worthy"] = ~ms["primed_before"] & ~ms["artifact"].astype(bool)
    misses = ms[ms["study_worthy"]].copy()
    misses = misses.sort_values(["class", "move30d"], ascending=[True, False])
    stats = []
    for cls, g in ms.groupby("class"):
        det = g[g["primed_before"]]
        mis = g[g["study_worthy"]]
        stats.append({
            "class": cls,
            "n_moves": int(len(g)),
            "n_detected_primed": int(len(det)),
            "n_missed": int(len(mis)),
            "detection_rate": float(len(det) / max(len(g), 1)),
            "miss_median_comp_days": float(mis["comp_days"].median()) if len(mis) else np.nan,
            "miss_median_rvol_pct": float(mis["rvol_pct"].median()) if len(mis) else np.nan,
            "miss_median_range_pos": float(mis["range_pos"].median()) if len(mis) else np.nan,
            "miss_median_stretch_z": float(mis["stretch_z"].median()) if len(mis) else np.nan,
            "det_median_comp_days": float(det["comp_days"].median()) if len(det) else np.nan,
            "det_median_rvol_pct": float(det["rvol_pct"].median()) if len(det) else np.nan,
        })
    return misses, pd.DataFrame(stats)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=CLUE)
    args = ap.parse_args(argv)

    dorm = build_dormancy_table()
    dorm.to_csv(args.out_dir / "dormancy_table.csv", index=False)
    print(f"dormancy table: {len(dorm)} series across "
          f"{dorm['class'].nunique()} classes -> dormancy_table.csv")

    misses, stats = build_missed_moves()
    misses.to_csv(args.out_dir / "missed_moves.csv", index=False)
    stats.to_csv(args.out_dir / "missed_moves_stats.csv", index=False)
    print(f"missed moves: {len(misses)} of {len(misses) + int(stats['n_detected_primed'].sum())} "
          f"episodes not flagged by the priming score -> missed_moves.csv")
    print(stats.to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
