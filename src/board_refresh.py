"""One-command board refresh: the daily null-time ritual.

Re-pulls fresh klines (Binance REST + Yahoo, cached; only the newest bar
changes), recomputes the full-universe dormancy table, regenerates the
heat map page, and appends a dated snapshot row to the board history so
every coil's state is tracked through time, not just today.

Usage:  python3 src/board_refresh.py

DESCRIPTIVE ONLY. No claims, no direction, no re-tuning of the sealed
priming rule. The multiplicity caveat binds at 1,300+ series.
"""

import datetime as dt
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLUE = ROOT / "paper/research/clue_scan"
HISTORY = CLUE / "board_history.csv"


def run(script: str) -> bool:
    r = subprocess.run([sys.executable, str(ROOT / "src" / script)],
                       cwd=ROOT)
    return r.returncode == 0


def append_history() -> None:
    """One row per refresh: dated coil census for the record."""
    df = pd.read_csv(CLUE / "mega_dormancy_table.csv")
    row = {
        "date": dt.date.today().isoformat(),
        "n_series": int(len(df)),
        "n_primed": int(df["primed"].sum()),
        "n_deep_coil": int((df["comp_days"] >= 20).sum()),
        "n_quiet_400d": int((df["last_4sigma_days_ago"] >= 400).sum()),
        "median_quiet_days": float(df["last_4sigma_days_ago"].median()),
    }
    for cls, g in df.groupby("class"):
        row[f"primed_{cls}"] = int(g["primed"].sum())
        row[f"n_{cls}"] = int(len(g))
    hist = pd.DataFrame([row])
    if HISTORY.exists():
        old = pd.read_csv(HISTORY)
        old = old[old["date"] != row["date"]]
        hist = pd.concat([old, hist], ignore_index=True)
    hist = hist.sort_values("date")
    hist.to_csv(HISTORY, index=False)
    print(f"board history: {len(hist)} snapshots -> {HISTORY}")
    print(hist.tail(3).to_string(index=False))


def main() -> int:
    ok = True
    for script in ("mega_universe.py", "build_dormancy_page.py",
                   "heatmap_page.py", "surprise_ledger.py",
                   "misses_2x2.py"):
        print(f"=== {script} ===")
        if not run(script):
            print(f"[fail] {script} exited non-zero")
            ok = False
    if ok:
        append_history()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
