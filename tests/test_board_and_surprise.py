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
    board = build_board(eq_csv=eq_csv, sp500_csv=sp_csv, top500_csv=cr_csv)
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
    return build_board(eq_csv=eq_csv, sp500_csv=sp_csv, top500_csv=cr_csv)


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
    # rehash - the chain must accept an honest rewrite, refuse tampering).
    # ALL OTHER entries must point at nonexistent files: build_board's
    # default data_file points at the real kline caches, and when those
    # exist on disk the fixture entries resolve against REAL market data,
    # making the test environment-dependent (it failed on any checkout
    # that had data/raw/top500_klines present).
    rec = json.loads(ledger.read_text())
    for i, e in enumerate(rec["entries"]):
        e["data_file"] = (str(tmp_path / "k.csv") if i == 0
                           else str(tmp_path / "missing.csv"))
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
    out = build_page(mega_csv=tmp_path / "none.csv", board_csv=board_csv,
                     ledger_path=ledger, page=page)
    html = page.read_text()
    assert out["n_series"] == 8
    assert html.count('class="tile"') == 8
    assert "wheat" in html and "BTCUSDT" in html
    assert "The surprise ledger" in html
    assert "site.css" in html


def test_heatmap_page_prefers_living_board(tmp_path):
    # the mega dormancy table is the living board; the page must read it
    # in preference to the stale clue-scan board table
    mega = pd.DataFrame({
        "series": ["a", "b", "c"], "class": ["etf", "etf", "crypto"],
        "venue": ["yahoo"] * 3, "n_days": [500, 400, 300],
        "comp_days": [10, 40, 5], "rvol_pct": [50.0, 10.0, 60.0],
        "range_pos": [0.5, 0.2, 0.7], "stretch_z": [0.0, -1.0, 0.5],
        "ret30": [0.0, 0.0, 0.0], "last_4sigma_days_ago": [10, 400, 3],
        "primed": [False, True, False],
        "dormancy_score": [1.0, 5.0, 0.5],
    })
    mega_csv = tmp_path / "mega.csv"
    mega.to_csv(mega_csv, index=False)
    board_csv = tmp_path / "stale.csv"
    board_csv.write_text("series,class\nold,crypto\n")
    page = tmp_path / "heatmap.html"
    out = build_page(mega_csv=mega_csv, board_csv=board_csv,
                     ledger_path=tmp_path / "no-ledger.jsonl", page=page)
    html = page.read_text()
    assert out["n_series"] == 3
    assert out["source"] == "mega_dormancy_table.csv"
    assert html.count('class="tile"') == 3
    # the etf class gets a section - no class is silently dropped
    assert "ETFs" in html
    # the stale board's series never renders as a tile
    assert ">old<" not in html


def test_heatmap_page_sections_data_driven(tmp_path):
    # an unknown class still renders: first-appearance order, no drop
    board = _board(tmp_path)
    board.loc[len(board)] = board.iloc[0]
    board.loc[board.index[-1], "series"] = "weird_thing"
    board.loc[board.index[-1], "class"] = "frontier_thing"
    board_csv = tmp_path / "board.csv"
    board.to_csv(board_csv, index=False)
    page = tmp_path / "heatmap.html"
    build_page(mega_csv=tmp_path / "none.csv", board_csv=board_csv,
               ledger_path=tmp_path / "no-ledger.jsonl", page=page)
    html = page.read_text()
    assert "frontier_thing" in html
    assert html.count('class="tile"') == 9


def test_tile_color_monotonic():
    c0 = _tile_color(0)
    c1 = _tile_color(0.5)
    c2 = _tile_color(1.0)
    assert c0 != c1 != c2
    assert _tile_color(0) == _tile_color(-0.3)
    assert _tile_color(1) == _tile_color(1.7)


def test_seal_from_mega_maps_living_board(tmp_path, monkeypatch):
    # the nightly cycle seals the LIVING board: mega schema -> ledger schema
    klines = tmp_path / "klines"
    klines.mkdir()
    dates = [f"2026-01-{d:02d}" for d in range(1, 26)]
    pd.DataFrame({"date": dates, "close": [100.0] * 25}).to_csv(
        klines / "BTCUSDT.csv", index=False)
    mega = pd.DataFrame({
        "series": ["BTCUSDT", "ETHUSDT", "AAPL"],
        "class": ["crypto", "crypto", "etf"],
        "venue": ["perp", "perp", "yahoo"],
        "n_days": [500, 500, 500],
        "comp_days": [40, 3, 60],
        "rvol_pct": [10.0, 50.0, 5.0],
        "range_pos": [0.2, 0.9, 0.1],
        "stretch_z": [-1.0, 0.0, -1.5],
        "ret30": [0.0, 0.0, 0.0],
        "last_4sigma_days_ago": [400, 10, 500],
        "primed": [True, False, True],
        "dormancy_score": [5.0, 1.0, 6.0],
    })
    mega_csv = tmp_path / "mega.csv"
    mega.to_csv(mega_csv, index=False)
    monkeypatch.setattr(sl, "BINANCE_KLINES", klines)
    monkeypatch.setattr(sl, "YAHOO_KLINES", klines)
    ledger = tmp_path / "ledger.jsonl"
    rec = sl.seal_from_mega(mega_csv=mega_csv, k_per_class=5,
                            ledger_path=ledger, timestamp_utc_us=1_000)
    # only primed candidates are sealed; ETHUSDT (not primed) is absent
    sealed = {e["series"] for e in rec["entries"]}
    assert sealed == {"BTCUSDT"}
    entry = rec["entries"][0]
    assert entry["primed_score"] == 5.0
    assert entry["last_date"] == "2026-01-25"
    assert entry["data_file"].endswith("BTCUSDT.csv")
    # absent mega fields are sealed null, never invented
    assert entry["evr_m"] is None and entry["vol_ratio"] is None
    assert rec["board_source"] == "mega_dormancy_table.csv"
    assert sl.verify_chain(ledger)
    # resolution machinery works on the mega-sealed entry
    # (future bars APPENDED past the sealed last_date, base intact)
    pd.DataFrame({
        "date": dates + [f"2026-02-{d:02d}" for d in range(1, 12)],
        "close": [100.0] * 25 + [100.0] * 5 + [130.0] + [100.0] * 5,
    }).to_csv(klines / "BTCUSDT.csv", index=False)
    out = sl.resolve_pending(ledger_path=ledger)
    assert len(out) == 1
    assert out[0]["realized_jump"] == pytest.approx(0.3, abs=1e-6)


def test_seal_from_mega_unresolvable_excluded(tmp_path, monkeypatch):
    # a primed candidate whose klines cannot be found is NOT sealed:
    # a score that cannot be resolved against data is not a prediction
    mega = pd.DataFrame({
        "series": ["GHOSTUSDT"], "class": ["crypto"], "venue": ["perp"],
        "n_days": [500], "comp_days": [40], "rvol_pct": [10.0],
        "range_pos": [0.2], "stretch_z": [-1.0], "ret30": [0.0],
        "last_4sigma_days_ago": [400], "primed": [True],
        "dormancy_score": [5.0],
    })
    mega_csv = tmp_path / "mega.csv"
    mega.to_csv(mega_csv, index=False)
    monkeypatch.setattr(sl, "BINANCE_KLINES", tmp_path / "nope")
    monkeypatch.setattr(sl, "YAHOO_KLINES", tmp_path / "nope")
    with pytest.raises(sl.LedgerError):
        sl.seal_from_mega(mega_csv=mega_csv,
                          ledger_path=tmp_path / "ledger.jsonl",
                          timestamp_utc_us=1_000)
