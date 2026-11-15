"""The board - EVERYTHING on one table, ranked by priming score.

Directive (Andrea, Nov 2026): a heat map of EVERYTHING - all commodities,
all indexes, crypto, and the main 500 stocks - scored by what is most
likely to make the next significant jump, then tracked over time to study
what surprises. This module builds the unified board: the crypto top-500
scan, the commodity/index/equity scan, and the full S&P 500 scan merged
into one table with one priming score and one board rank.

Honesty rules carried over from the constituent scans:
  - The priming score is DESCRIPTIVE. It ranks candidates; it tests
    nothing. The multiplicity warning is binding at its worst here:
    a board of ~1000 series finds extremes by construction.
  - WHICH WAY is refused: priming is directionless by measurement.
  - Genesis filter: crypto with <90 days of listing history and recent
    S&P 500 additions with <150 days are flagged ineligible for
    candidacy (the launch, not a coil).
  - Artifact flag (|30d return| > 20%) marks move-already-happened
    series; they stay on the board but cannot be primed candidates.

The board is the t0 input to the surprise ledger (surprise_ledger.py):
top candidates are sealed with their scores, and once the horizon passes
the realized jump is resolved against the SAME cached klines - the
surprise study is then a sealed-answer-vs-reality comparison, not a
retrospective.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path("paper/research/clue_scan")
BOARD_CSV = OUT / "board_table.csv"

TOP500_CSV = OUT / "top500_scan_table.csv"
EQ_CSV = OUT / "eq_commodity_scan_table.csv"
SP500_CSV = OUT / "sp500_scan_table.csv"

CRYPTO_KLINES = Path("data/raw/top500_klines")
EQ_KLINES = Path("data/raw/eq_commodity_klines")

GENESIS_MIN_DAYS = 90

BOARD_COLUMNS = [
    "series", "class", "venue", "last_date", "n_days", "range_pos",
    "rvol_pct", "comp_days", "evr_m", "vol_ratio", "stretch_z",
    "ret30", "primed_score", "artifact_flag", "genesis_flag",
    "eligible", "data_file", "board_rank",
]

CLASS_ORDER = ["commodity", "index", "equity", "sp500", "crypto"]


def _eq_cache_file(yahoo_symbol):
    return str(EQ_KLINES / f"{yahoo_symbol.replace('=', '_').replace('^', '')}.csv")


def build_board(top500_csv=TOP500_CSV, eq_csv=EQ_CSV, sp500_csv=SP500_CSV):
    """Merge the three scan tables into one ranked board."""
    frames = []

    if Path(eq_csv).exists():
        eq = pd.read_csv(eq_csv)
        eq["venue"] = "yahoo"
        eq["genesis_flag"] = False
        eq["data_file"] = eq["yahoo_symbol"].map(_eq_cache_file)
        frames.append(eq)

    if Path(sp500_csv).exists():
        sp = pd.read_csv(sp500_csv)
        sp["venue"] = "yahoo"
        sp["genesis_flag"] = sp["short_history"].astype(bool) if (
            "short_history" in sp.columns) else False
        sp["data_file"] = sp["yahoo_symbol"].map(_eq_cache_file)
        frames.append(sp)

    if Path(top500_csv).exists():
        cr = pd.read_csv(top500_csv)
        cr["class"] = "crypto"
        cr["venue"] = cr.get("venue", "binance")
        cr["genesis_flag"] = cr["n_days"] < GENESIS_MIN_DAYS
        cr["data_file"] = cr["series"].map(lambda s: str(CRYPTO_KLINES / f"{s}.csv"))
        frames.append(cr)

    if not frames:
        raise SystemExit("no scan tables found - run the constituent scans first")

    board = pd.concat(frames, ignore_index=True, sort=False)
    board["artifact_flag"] = board["artifact_flag"].astype(bool)
    stablecoin_flag = (
        board["stablecoin"].fillna(False).astype(bool)
        if "stablecoin" in board.columns else False)
    board["eligible"] = ~(
        board["artifact_flag"] | board["genesis_flag"] | stablecoin_flag)
    board = board.sort_values("primed_score", ascending=False).reset_index(drop=True)
    board["board_rank"] = range(1, len(board) + 1)
    return board[BOARD_COLUMNS]


def save_board(board, path=BOARD_CSV):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    board.to_csv(path, index=False)
    meta = (
        f"built {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} "
        f"from top500_scan_table.csv, eq_commodity_scan_table.csv, "
        f"sp500_scan_table.csv; {len(board)} series; "
        f"DESCRIPTIVE ONLY - candidates, not claims; multiplicity binds."
    )
    Path(str(path).replace(".csv", ".meta.txt")).write_text(meta + "\n")
    return path


def main():
    board = build_board()
    save_board(board)
    print(f"board: {len(board)} series -> {BOARD_CSV}")
    print("\n=== per-class summary ===")
    for cls in CLASS_ORDER:
        sub = board[board["class"] == cls]
        elig = sub[sub["eligible"]]
        print(f"[{cls}] n={len(sub)}  eligible={len(elig)}  "
              f"deep coils (comp_days>=20)={int((sub['comp_days'] >= 20).sum())}  "
              f"median primed_score={sub['primed_score'].median():.3f}")
    print("\n=== top-20 primed candidates on the whole board (eligible only) ===")
    cols = ["board_rank", "series", "class", "primed_score", "comp_days",
            "rvol_pct", "range_pos", "vol_ratio", "last_date"]
    print(board[board["eligible"]].head(20)[cols].to_string(index=False))
    print("\nDESCRIPTIVE ONLY. WHICH WAY is refused. C7 stays sealed.")


if __name__ == "__main__":
    main()
