import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import surprise_ledger as sl
from board_heatmap import build_board
from heatmap_page import build_page, _tile_color


def _scan_row(series, cls, score, comp_days=30, n_days=500,
              artifact=False, **extra):
    row = {
        "series": series, "class": cls, "last_date": "2026-01-10",
        "n_days": n_days, "range_pos": 0.1, "rvol_pct": 5.0,
        "comp_days": comp_days, "evr_m": 10.0, "vol_ratio": 1.0,
        "stretch_z": -1.5, "ret30": 0.0,
        "primed_score": score, "artifact_flag": artifact,
    }
    row.update(extra)
    return row


def _write_tables(tmp):
    eq = pd.DataFrame([
        _scan_row("wheat", "commodity", 0.9, yahoo_symbol="ZW=F"),
        _scan_row("gold", "commodity", 0.2, artifact=True, yahoo_symbol="GC=F"),
        _scan_row("sp500idx", "index", 0.4, yahoo_symbol="^GSPC"),
    ])
    sp = pd.DataFrame([
        _scan_row("aapl", "sp500", 0.8, yahoo_symbol="AAPL"),
        _scan_row("newip", "sp500", 0.95, n_days=100, yahoo_symbol="NEWIP",
                   short_history=True),
    ])
    cr = pd.DataFrame([
        _scan_row("BTCUSDT", "crypto", 0.7, stablecoin=False, venue="perp"),
        _scan_row("NEWUSDT", "crypto", 0.85, n_days=50, stablecoin=False,
                   venue="perp"),
        _scan_row("USDCUSDT", "crypto", 0.6, stablecoin=True, venue="spot"),
    ])
    eq_csv = tmp / "eq.csv"
    sp_csv = tmp / "sp.csv"
    cr_csv = tmp / "cr.csv"
    eq.to_csv(eq_csv, index=False)
    sp.to_csv(sp_csv, index=False)
    cr.to_csv(cr_csv, index=False)
    return eq_csv, sp_csv, cr_csv


def test_board_merges_and_ranks(tmp_path):
    eq_csv, sp_csv, cr_csv = _write_tables(tmp_path)
    board = build_board(eq_csv=eq_csv, sp500_csv=sp_csv, top500_csv=cr_csv,
                        global_csv=tmp_path / "none.csv")
    assert len(board) == 8
    assert set(board["class"]) == {"commodity", "index", "sp500", "crypto"}
    assert list(board["primed_score"]) == sorted(
        board["primed_score"], reverse=True)
    assert list(board["board_rank"]) == list(range(1, 9))
    by = board.set_index("series")
    # artifact-flagged stays but is ineligible
    assert not by.loc["gold", "eligible"]
    assert by.loc["gold", "artifact_flag"]
    # genesis filter: <90d crypto and short-history sp500 ineligible
    assert not by.loc["NEWUSDT", "eligible"]
    assert by.loc["NEWUSDT", "genesis_flag"]
    assert not by.loc["newip", "eligible"]
    # stablecoin ineligible by construction
    assert not by.loc["USDCUSDT", "eligible"]
    # clean series eligible
    assert by.loc["wheat", "eligible"]
    assert by.loc["BTCUSDT", "eligible"]
    # data file paths point at the kline caches
    assert "eq_commodity_klines/ZW_F.csv" in by.loc["wheat", "data_file"]
    assert "top500_klines/BTCUSDT.csv" in by.loc["BTCUSDT", "data_file"]


def _kline_csv(path, dates, closes):
    pd.DataFrame({"date": dates, "close": closes}).to_csv(path, index=False)


def _board(tmp_path):
    eq_csv, sp_csv, cr_csv = _write_tables(tmp_path)
    return build_board(eq_csv=eq_csv, sp500_csv=sp_csv, top500_csv=cr_csv,
                       global_csv=tmp_path / "none.csv")


def test_ledger_seal_verify_and_tamper(tmp_path):
    board = _board(tmp_path)
    ledger = tmp_path / "ledger.jsonl"
    rec = sl.seal_snapshot(board, k_per_class=2, ledger_path=ledger,
                           timestamp_utc_us=1_000)
    assert rec["type"] == sl.SNAPSHOT_RECORD
    assert len(rec["entries"]) > 0
    assert "realized_jump" not in json.dumps(rec)
    assert sl.verify_chain(ledger)
    # tampering refuses all writes
    lines = ledger.read_text().splitlines()
    first = json.loads(lines[0])
    first["entries"][0]["primed_score"] = 0.99
    lines[0] = json.dumps(first)
    ledger.write_text("\n".join(lines) + "\n")
    with pytest.raises(sl.LedgerError):
        sl.seal_snapshot(board, ledger_path=ledger, timestamp_utc_us=2_000)


def test_ledger_monotonicity(tmp_path):
    board = _board(tmp_path)
    ledger = tmp_path / "ledger.jsonl"
    sl.seal_snapshot(board, ledger_path=ledger, timestamp_utc_us=1_000)
    with pytest.raises(sl.LedgerError):
        sl.seal_snapshot(board, ledger_path=ledger, timestamp_utc_us=1_000)


def test_resolution_requires_passed_horizon(tmp_path):
    board = _board(tmp_path)
    ledger = tmp_path / "ledger.jsonl"
    sl.seal_snapshot(board, k_per_class=1, ledger_path=ledger,
                     timestamp_utc_us=1_000)
    # entry last_date 2026-01-10, horizon 10 bars, only 5 future bars
    dates = [f"2026-01-{d:02d}" for d in range(1, 16)]
    closes = [100.0] * 15
    closes[11] = 120.0
    entry = json.loads(ledger.read_text())["entries"][0]
    _kline_csv(tmp_path / "k.csv", dates, closes)
    # point the sealed entry at our kline file (rewrite with a valid
    # rehash - the chain must accept an honest rewrite, refuse tampering)
    rec = json.loads(ledger.read_text())
    rec["entries"][0]["data_file"] = str(tmp_path / "k.csv")
    rec["sha256"] = sl._record_sha256(rec)
    ledger.write_text(sl._canonical_json(rec) + "\n")
    assert sl.verify_chain(ledger)
    assert sl.resolve_pending(ledger_path=ledger) == []
    # now the full horizon exists: 10+ bars after last_date
    dates = [f"2026-01-{d:02d}" for d in range(1, 26)]
    _kline_csv(tmp_path / "k.csv", dates, closes + [100.0] * 10)
    out = sl.resolve_pending(ledger_path=ledger)
    assert len(out) == 1
    assert out[0]["realized_jump"] == pytest.approx(0.2, abs=1e-6)
    assert out[0]["jump_direction"] == "up"
    # double resolution is refused (already resolved)
    assert sl.resolve_pending(ledger_path=ledger) == []


def test_study_from_resolutions(tmp_path):
    board = _board(tmp_path)
    ledger = tmp_path / "ledger.jsonl"
    sl.seal_snapshot(board, k_per_class=5, ledger_path=ledger,
                     timestamp_utc_us=1_000)
    rec = json.loads(ledger.read_text())
    ts = 2_000
    for i, e in enumerate(rec["entries"]):
        body = {
            "type": sl.RESOLUTION_RECORD,
            "timestamp_utc_us": ts + i,
            "snapshot_sha256": rec["sha256"],
            "series": e["series"],
            "class": e["class"],
            "primed_score": float(e["primed_score"]),
            "realized_jump": float(e["primed_score"]) * 0.1,
            "jump_direction": "up",
        }
        body["prev_sha256"] = sl.read_ledger(ledger)[-1]["sha256"]
        body["sha256"] = sl._record_sha256(body)
        with ledger.open("a") as f:
            f.write(sl._canonical_json(body) + "\n")
    study_md = tmp_path / "study.md"
    s = sl.study(ledger_path=ledger, study_md=study_md)
    assert s["n_resolved"] == len(rec["entries"])
    # perfect rank agreement -> rho 1.0
    assert s["overall"]["spearman_rho"] == pytest.approx(1.0)
    assert study_md.exists()
    assert "Surprise study" in study_md.read_text()


def test_heatmap_page_generation(tmp_path):
    board = _board(tmp_path)
    board_csv = tmp_path / "board.csv"
    board.to_csv(board_csv, index=False)
    ledger = tmp_path / "ledger.jsonl"
    sl.seal_snapshot(board, k_per_class=2, ledger_path=ledger,
                     timestamp_utc_us=1_000)
    page = tmp_path / "heatmap.html"
    out = build_page(board_csv=board_csv, ledger_path=ledger, page=page)
    html = page.read_text()
    assert out["n_series"] == 8
    assert html.count('class="tile"') == 8
    # the checkerboard chip: flat horizontal cell, one line, no meta block
    assert 'height: 21px' in html
    assert 'display: none' in html
    assert "wheat" in html and "BTCUSDT" in html
    assert "The surprise ledger" in html
    assert "site.css" in html


def test_board_merges_global_scan(tmp_path):
    eq_csv, sp_csv, cr_csv = _write_tables(tmp_path)
    gl = pd.DataFrame([
        _scan_row("eurusd", "fx", 0.6, yahoo_symbol="EURUSD=X"),
        _scan_row("telaviv125", "world_index", 0.5,
                  yahoo_symbol="^TA125.TA"),
        _scan_row("usdirr_rial", "fx", 0.9, yahoo_symbol="USDIRR=X"),
        _scan_row("newfx", "fx", 0.95, n_days=50, yahoo_symbol="NEWFX=X"),
    ])
    gl_csv = tmp_path / "gl.csv"
    gl.to_csv(gl_csv, index=False)
    board = build_board(eq_csv=eq_csv, sp500_csv=sp_csv, top500_csv=cr_csv,
                        global_csv=gl_csv)
    assert len(board) == 12
    by = board.set_index("series")
    assert by.loc["eurusd", "class"] == "fx"
    assert by.loc["telaviv125", "class"] == "world_index"
    assert by.loc["usdirr_rial", "eligible"]
    # genesis filter applies to the global scan too (<90d)
    assert not by.loc["newfx", "eligible"]
    assert by.loc["newfx", "genesis_flag"]
    assert "eq_commodity_klines/EURUSD_X.csv" in by.loc[
        "eurusd", "data_file"]


def test_tile_color_monotonic():
    c0 = _tile_color(0)
    c1 = _tile_color(0.5)
    c2 = _tile_color(1.0)
    assert c0 != c1 != c2
    assert _tile_color(0) == _tile_color(-0.3)
    assert _tile_color(1) == _tile_color(1.7)
