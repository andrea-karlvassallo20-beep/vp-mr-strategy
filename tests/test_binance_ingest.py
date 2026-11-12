import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from binance_ingest import load_agg_trades, load_book_ticker, convert_files


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text)
    return p


AGG_CSV = (
    "agg_trade_id,price,quantity,first_trade_id,last_trade_id,transact_time,is_buyer_maker\n"
    "0,50000.5,0.25,0,0,1700000000123,false\n"
    "1,50001.0,1.50,1,1,1700000000456,true\n"
    "2,50000.75,0.10,2,2,1700000000789,false\n"
)

AGG_CSV_NOHEADER = (
    "0,50000.5,0.25,0,0,1700000000123,false\n"
    "1,50001.0,1.50,1,1,1700000000456,true\n"
)

BT_FUT_CSV = (
    "update_id,best_bid_price,best_bid_qty,best_ask_price,best_ask_qty,"
    "transaction_time,event_time\n"
    "100,49999.5,2.0,50000.0,1.5,1700000000123,1700000000124\n"
    "101,49999.0,3.0,50000.5,2.5,1700000000456,1700000000457\n"
)

BT_SPOT_CSV_NOHEADER = (
    "100,49999.5,2.0,50000.0,1.5,1700000000123\n"
    "101,49999.0,3.0,50000.5,2.5,1700000000456\n"
)


def test_agg_trades_schema_and_flags(tmp_path):
    df = load_agg_trades(_write(tmp_path, "a.csv", AGG_CSV))
    assert list(df.columns) == ["ts_exchange_us", "trade_id", "price", "size", "aggressor_buy"]
    assert str(df["ts_exchange_us"].dtype) == "int64"
    assert str(df["aggressor_buy"].dtype) == "int8"
    assert df["ts_exchange_us"].iloc[0] == 1700000000123 * 1000
    assert df["aggressor_buy"].tolist() == [1, 0, 1]
    assert df["ts_exchange_us"].is_monotonic_increasing


def test_agg_trades_headerless(tmp_path):
    df = load_agg_trades(_write(tmp_path, "b.csv", AGG_CSV_NOHEADER))
    assert len(df) == 2
    assert df["aggressor_buy"].tolist() == [1, 0]


def test_agg_trades_zip(tmp_path):
    import zipfile
    z = tmp_path / "BTCUSDT-aggTrades-2024-01-01.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("BTCUSDT-aggTrades-2024-01-01.csv", AGG_CSV)
    df = load_agg_trades(z)
    assert len(df) == 3


def test_agg_trades_rejects_bad_flag(tmp_path):
    bad = AGG_CSV.replace("false\n1,", "maybe\n1,") if False else AGG_CSV.replace(
        ",false\n", ",maybe\n"
    )
    with pytest.raises(ValueError):
        load_agg_trades(_write(tmp_path, "c.csv", bad))


def test_book_ticker_futures_uses_event_time(tmp_path):
    df = load_book_ticker(_write(tmp_path, "d.csv", BT_FUT_CSV))
    assert list(df.columns) == [
        "ts_exchange_us", "update_id", "bid_price", "bid_qty", "ask_price", "ask_qty",
    ]
    assert df["ts_exchange_us"].iloc[0] == 1700000000124 * 1000


def test_book_ticker_spot_headerless(tmp_path):
    df = load_book_ticker(_write(tmp_path, "e.csv", BT_SPOT_CSV_NOHEADER))
    assert df["ts_exchange_us"].iloc[0] == 1700000000123 * 1000
    assert len(df) == 2


def test_book_ticker_rejects_crossed(tmp_path):
    bad = BT_FUT_CSV.replace("100,49999.5,2.0", "100,50000.5,2.0")
    with pytest.raises(ValueError):
        load_book_ticker(_write(tmp_path, "f.csv", bad))


def test_book_ticker_sorts_out_of_order(tmp_path):
    lines = BT_FUT_CSV.strip().splitlines()
    rows = [lines[0], lines[2], lines[1]]
    df = load_book_ticker(_write(tmp_path, "g.csv", "\n".join(rows) + "\n"))
    assert df["ts_exchange_us"].is_monotonic_increasing


def test_convert_files_roundtrip(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "BTCUSDT-aggTrades-2024-01-01.csv").write_text(AGG_CSV)
    out = tmp_path / "out"
    n = convert_files(raw, out, "aggtrades")
    assert n == 1
    pq = out / "BTCUSDT-aggTrades-2024-01-01.parquet"
    assert pq.exists()
    import pandas as pd
    df = pd.read_parquet(pq)
    assert len(df) == 3
    assert str(df["ts_exchange_us"].dtype) == "int64"
    assert str(df["aggressor_buy"].dtype) == "int8"
