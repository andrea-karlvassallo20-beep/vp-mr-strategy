import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from binance_ingest import load_funding_rate, load_metrics, convert_files


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text)
    return p


FUND_CSV = (
    "calc_time,funding_interval_hours,last_funding_rate\n"
    "1722470400000,8,0.00008208\n"
    "1722499200000,8,0.00010000\n"
)

MET_CSV = (
    "create_time,symbol,sum_open_interest,sum_open_interest_value,"
    "count_toptrader_long_short_ratio,sum_toptrader_long_short_ratio,"
    "count_long_short_ratio,sum_taker_long_short_vol_ratio\n"
    "2024-08-05 00:00:00,BTCUSDT,88072.44,5132483149.98,2.65,1.94,2.56,1.10\n"
    "2024-08-05 00:05:00,BTCUSDT,87881.17,5075524244.64,2.64,1.95,2.53,0.56\n"
)


def test_funding_rate_schema(tmp_path):
    df = load_funding_rate(_write(tmp_path, "f.csv", FUND_CSV))
    assert list(df.columns) == ["ts_exchange_us", "interval_hours", "funding_rate"]
    assert str(df["ts_exchange_us"].dtype) == "int64"
    assert df["ts_exchange_us"].iloc[0] == 1722470400000 * 1000
    assert df["funding_rate"].tolist() == [0.00008208, 0.0001]


def test_funding_rate_rejects_bad_schema(tmp_path):
    with pytest.raises(ValueError):
        load_funding_rate(_write(tmp_path, "bad.csv", "a,b\n1,2\n"))


def test_metrics_schema_and_utc_flag(tmp_path):
    df = load_metrics(_write(tmp_path, "m.csv", MET_CSV))
    assert list(df.columns)[0] == "ts_exchange_us"
    assert str(df["ts_exchange_us"].dtype) == "int64"
    assert df["ts_exchange_us"].is_monotonic_increasing
    assert not df.isna().any().any()
    assert df["sum_open_interest"].iloc[0] == pytest.approx(88072.44)


def test_metrics_rejects_nan(tmp_path):
    bad = MET_CSV.replace("88072.44", "")
    with pytest.raises(ValueError):
        load_metrics(_write(tmp_path, "bad.csv", bad))


def test_convert_funding_roundtrip(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "BTCUSDT-fundingRate-2024-08.csv").write_text(FUND_CSV)
    out = tmp_path / "out"
    n = convert_files(raw, out, "fundingrate")
    assert n == 1
    import pandas as pd
    df = pd.read_parquet(out / "BTCUSDT-fundingRate-2024-08.parquet")
    assert len(df) == 2
    assert str(df["ts_exchange_us"].dtype) == "int64"
