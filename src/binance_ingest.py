"""Binance public archive ingestion: aggTrades and bookTicker CSVs -> Parquet.

Free archives from https://data.binance.vision/ (daily or monthly zips/CSVs).
This module ONLY loads, validates, normalizes, and converts. No features, no
models, no L2 reconstruction. bookTicker is a best-bid/ask snapshot stream —
it is NOT full-depth L2 and cannot reconstruct the book; see
docs/data_dictionary.md for what each feed can and cannot measure.
"""

import argparse
import io
import zipfile
from pathlib import Path

import pandas as pd

AGG_TRADES_COLUMNS = [
    "agg_trade_id",
    "price",
    "quantity",
    "first_trade_id",
    "last_trade_id",
    "transact_time",
    "is_buyer_maker",
]

BOOK_TICKER_FUTURES_COLUMNS = [
    "update_id",
    "best_bid_price",
    "best_bid_qty",
    "best_ask_price",
    "best_ask_qty",
    "transaction_time",
    "event_time",
]

BOOK_TICKER_SPOT_COLUMNS = [
    "update_id",
    "best_bid_price",
    "best_bid_qty",
    "best_ask_price",
    "best_ask_qty",
    "transaction_time",
]


def _read_table(path: Path) -> pd.DataFrame:
    """Read a Binance archive file (.csv or .zip containing one csv)."""
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as zf:
            names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not names:
                raise ValueError(f"{path}: zip contains no csv")
            raw = zf.read(names[0])
    else:
        raw = path.read_bytes()
    df = pd.read_csv(io.BytesIO(raw), header=None, dtype=str, low_memory=False)
    first = df.iloc[0].astype(str).str.lower().tolist()
    if "price" in first or "best_bid_price" in first:
        df = pd.read_csv(io.BytesIO(raw), header=0, dtype=str, low_memory=False)
        df.columns = [c.strip().lower() for c in df.columns]
    return df


def _ms_to_us(series: pd.Series) -> pd.Series:
    """Milliseconds epoch -> int64 microseconds UTC. Strict, no NaN."""
    ms = pd.to_numeric(series, errors="raise").astype("int64")
    if ms.isna().any():
        raise ValueError("NaN timestamp after coercion")
    return ms * 1000


def _require_monotonic(df: pd.DataFrame, ts_col: str, path: Path) -> pd.DataFrame:
    if not df[ts_col].is_monotonic_increasing:
        n_bad = int((df[ts_col].diff() < 0).sum())
        df = df.sort_values(ts_col, kind="stable").reset_index(drop=True)
        print(f"WARN {path.name}: {n_bad} out-of-order rows; sorted by {ts_col}")
    return df


def load_agg_trades(path: Path) -> pd.DataFrame:
    """Normalized schema:
    ts_exchange_us  int64  UTC microseconds (transact_time, ms -> us)
    trade_id        int64  agg_trade_id
    price           float64
    size            float64
    aggressor_buy   int8   1 = aggressor buys (is_buyer_maker false), 0 = sells
    """
    df = _read_table(path)
    cols = [str(c).strip().lower() for c in df.columns]
    if "agg_trade_id" not in cols:
        if df.shape[1] != len(AGG_TRADES_COLUMNS):
            raise ValueError(f"{path}: unexpected aggTrades shape {df.shape}")
        df.columns = AGG_TRADES_COLUMNS
    else:
        df = df.rename(columns=str.strip).rename(columns=str.lower)
    out = pd.DataFrame(
        {
            "ts_exchange_us": _ms_to_us(df["transact_time"]),
            "trade_id": pd.to_numeric(df["agg_trade_id"], errors="raise").astype("int64"),
            "price": pd.to_numeric(df["price"], errors="raise").astype("float64"),
            "size": pd.to_numeric(df["quantity"], errors="raise").astype("float64"),
        }
    )
    maker = df["is_buyer_maker"].astype(str).str.strip().str.lower()
    unknown = set(maker.unique()) - {"true", "false", "t", "f", "1", "0"}
    if unknown:
        raise ValueError(f"{path}: non-binary is_buyer_maker values {unknown}")
    out["aggressor_buy"] = (~maker.isin({"true", "t", "1"})).astype("int8")
    if (out["price"] <= 0).any() or (out["size"] < 0).any():
        raise ValueError(f"{path}: non-positive price or negative size")
    return _require_monotonic(out, "ts_exchange_us", path)


def load_book_ticker(path: Path) -> pd.DataFrame:
    """Normalized schema:
    ts_exchange_us  int64  UTC microseconds (event_time if present else transaction_time)
    update_id       int64
    bid_price       float64
    bid_qty         float64
    ask_price       float64
    ask_qty         float64
    """
    df = _read_table(path)
    cols = [str(c).strip().lower() for c in df.columns]
    if "best_bid_price" not in cols:
        expected = (
            BOOK_TICKER_FUTURES_COLUMNS
            if df.shape[1] == 7
            else BOOK_TICKER_SPOT_COLUMNS
        )
        if df.shape[1] != len(expected):
            raise ValueError(f"{path}: unexpected bookTicker shape {df.shape}")
        df.columns = expected
    else:
        df = df.rename(columns=str.strip).rename(columns=str.lower)
    ts_source = "event_time" if "event_time" in df.columns else "transaction_time"
    out = pd.DataFrame(
        {
            "ts_exchange_us": _ms_to_us(df[ts_source]),
            "update_id": pd.to_numeric(df["update_id"], errors="raise").astype("int64"),
            "bid_price": pd.to_numeric(df["best_bid_price"], errors="raise").astype("float64"),
            "bid_qty": pd.to_numeric(df["best_bid_qty"], errors="raise").astype("float64"),
            "ask_price": pd.to_numeric(df["best_ask_price"], errors="raise").astype("float64"),
            "ask_qty": pd.to_numeric(df["best_ask_qty"], errors="raise").astype("float64"),
        }
    )
    bad = (out["bid_price"] <= 0) | (out["ask_price"] <= 0)
    bad |= (out["bid_qty"] < 0) | (out["ask_qty"] < 0)
    bad |= out["bid_price"] > out["ask_price"]
    if bad.any():
        raise ValueError(f"{path}: {int(bad.sum())} rows violate bid<ask, price>0, qty>=0")
    return _require_monotonic(out, "ts_exchange_us", path)


def _output_path(out_dir: Path, stem: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{stem}.parquet"


def convert_files(src_dir: Path, out_dir: Path, kind: str) -> int:
    loader = {"aggtrades": load_agg_trades, "bookticker": load_book_ticker}[kind]
    paths = sorted(p for p in src_dir.rglob("*") if p.suffix in {".csv", ".zip"})
    if not paths:
        print(f"no .csv/.zip files under {src_dir}")
        return 0
    n = 0
    for p in paths:
        df = loader(p)
        out = _output_path(out_dir, p.name.rsplit(".zip", 1)[0].removesuffix(".csv"))
        df.to_parquet(out, index=False)
        print(f"{p.name} -> {out} ({len(df)} rows)")
        n += 1
    return n


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("kind", choices=["aggtrades", "bookticker"])
    ap.add_argument("--src", type=Path, required=True, help="raw archive dir")
    ap.add_argument("--out", type=Path, required=True, help="parquet out dir")
    args = ap.parse_args(argv)
    convert_files(args.src, args.out, args.kind)


if __name__ == "__main__":
    main()
