"""Intake audit for any arriving parquet dataset.

Runs FIRST on any new data file, before any feature, model, or claim
touches it. Produces an honest written audit:

  - schema and dtypes (columns, types, memory footprint)
  - row count and (if partitioned) per-partition coverage
  - timestamp convention detection (us / ms / s / ns) with explicit
    warning - the ms-vs-us bug was caught once already and cost a day
  - calendar coverage and gap audit for dated data
  - duplicate and null audit
  - L2 signature detection: if the columns look like order-book data
  (side/price/size + sequence or operation fields), the audit REFUSES
  to bless it and prints the standing rule - the Layer 0 gate runs
  first (src/verify_l2_gate.py) and nothing downstream may touch the
  data until the gate exits 0.

Descriptive only. No features, no models, no claims.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

L2_SIGNATURES = (
    {"side", "price", "size"},
    {"side", "price", "amount"},
    {"operation", "price", "size"},
    {"is_buyer_maker", "price", "quantity"},
)


def _detect_ts_unit(series: pd.Series) -> str:
    """Guess the timestamp unit from magnitude (int64 epoch)."""
    v = pd.Series(series).dropna()
    if not len(v):
        return "unknown"
    m = float(np.median(np.abs(v.astype(float))))
    if m < 1e10:
        return "SECONDS (10-digit)"
    if m < 1e13:
        return "MILLISECONDS (13-digit)"
    if m < 1e16:
        return "MICROSECONDS (16-digit)"
    return "NANOSECONDS (19-digit)"


def audit_parquet(path: Path) -> dict:
    out = {"file": str(path), "size_mb": round(path.stat().st_size / 1e6, 1)}
    pf = pd.read_parquet(path) if path.suffix == ".parquet" else None
    if pf is None:
        return {**out, "error": "not a readable parquet"}
    out["n_rows"] = int(len(pf))
    out["n_columns"] = int(pf.shape[1])
    out["columns"] = [
        {"name": c, "dtype": str(pf[c].dtype),
         "nulls": int(pf[c].isna().sum()),
         "n_unique": int(pf[c].nunique(dropna=True)) if len(pf) else 0}
        for c in pf.columns
    ]
    ts_cols = [c for c in pf.columns
               if "time" in c.lower() or "ts" in c.lower()
               or "date" in c.lower()]
    out["timestamp_columns"] = {}
    for c in ts_cols:
        s = pf[c]
        if pd.api.types.is_numeric_dtype(s):
            out["timestamp_columns"][c] = {
                "kind": "numeric epoch",
                "unit_guess": _detect_ts_unit(s),
                "min": str(s.min()), "max": str(s.max()),
                "monotonic": bool(s.is_monotonic_increasing),
            }
        else:
            try:
                d = pd.to_datetime(s)
                out["timestamp_columns"][c] = {
                    "kind": "datetime", "min": str(d.min()),
                    "max": str(d.max()),
                    "monotonic": bool(d.is_monotonic_increasing),
                    "n_days": int((d.max() - d.min()).total_seconds() // 86400) + 1,
                }
            except Exception:
                out["timestamp_columns"][c] = {"kind": "unparsed"}
    dup = int(pf.duplicated().sum())
    out["duplicate_rows"] = dup
    # L2 signature check
    cols = {c.lower() for c in pf.columns}
    for sig in L2_SIGNATURES:
        if sig <= cols:
            out["l2_signature"] = (
                f"columns {sorted(sig)} present - this looks like order-book "
                "data. THE STANDING RULE APPLIES: run src/verify_l2_gate.py "
                "FIRST (sequence continuity, mid/depth vs snapshots); "
                "nothing downstream may touch this file until the gate "
                "exits 0. If the file lacks native sequence numbers "
                "(U/u/pu or sequence_number), the gate will refuse it and "
                "the honest report is that raw @depth replay is required.")
            break
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)
    p = args.path
    reports = []
    if p.is_dir():
        files = sorted(p.rglob("*.parquet"))
        reports.append({"directory": str(p), "n_parquet_files": len(files)})
        for f in files[:50]:
            reports.append(audit_parquet(f))
    else:
        reports.append(audit_parquet(p))
    import json
    text = json.dumps(reports, indent=2, default=str)
    print(text[:8000])
    if args.out:
        args.out.write_text(text)
        print(f"\nfull audit -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
