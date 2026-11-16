"""Chunked Tardis CSV.gz -> parquet conversion with row-count verification.

The C1-L2 pipeline reads data frame style; this converts one day of
incremental_book_L2 (or trades) one chunk at a time so peak memory stays
bounded, and verifies that the parquet row count equals the CSV row count
before declaring success. A truncated or mismatched conversion raises:
the downstream harness must never see silently short data.

Usage:
    python3 src/convert_to_parquet.py data/raw/incremental_book_L2_BTCUSDT_2026-10-01.csv.gz \
        data/processed/incremental_book_L2_BTCUSDT_2026-10-01.parquet
"""

import argparse
from pathlib import Path

import pandas as pd

CHUNKSIZE = 2_000_000


def convert(src: Path, dst: Path, chunksize: int = CHUNKSIZE) -> dict:
    if dst.exists():
        raise FileExistsError(f"refusing to overwrite {dst}; delete it first")
    dst.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    header = True
    for chunk in pd.read_csv(src, compression="gzip", chunksize=chunksize):
        n += len(chunk)
        chunk.to_parquet(dst, index=False, append=not header)
        header = False
    check = pd.read_parquet(dst, columns=None)
    m = len(check)
    if m != n:
        raise AssertionError(
            f"row-count mismatch: csv {n} rows vs parquet {m} rows for {dst}"
        )
    return {"csv_rows": n, "parquet_rows": m, "dst": str(dst)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--chunksize", type=int, default=CHUNKSIZE)
    args = ap.parse_args()
    out = convert(args.src, args.dst, args.chunksize)
    print(f"converted {out['csv_rows']} rows -> {out['dst']} (verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
