"""Tests for src/forward_log.py — the append-only forward calibration log."""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from forward_log import (
    GENESIS_PREV_SHA256,
    append_decision_entry,
    calibration_metrics,
    feature_vector_sha256,
    resolve_matured_entries,
    verify_hash_chain,
)


def _dec(ledger, entry_id, ts, p_up=0.6, horizon_us=10_000_000,
         instrument="BTCUSDT", features=None, phase="compression"):
    return append_decision_entry(
        ledger,
        entry_id=entry_id,
        timestamp_utc_us=ts,
        instrument=instrument,
        layer1_phase=phase,
        layer2_p_up=p_up,
        layer2_ci_95=[max(0.0, p_up - 0.05), min(1.0, p_up + 0.05)],
        layer3_hazard_ratio=1.45,
        horizon_end_utc_us=ts + horizon_us,
        feature_vector=features if features is not None
        else {"z20": -1.2, "mom": 0.3},
    )


def test_genesis_entry_links_to_zero_hash(tmp_path):
    ledger = tmp_path / "forward_calibration.jsonl"
    rec = _dec(ledger, "e1", 1_000_000)
    assert rec["prev_entry_sha256"] == GENESIS_PREV_SHA256
    state = verify_hash_chain(ledger)
    assert state["n_decisions"] == 1 and state["n_resolutions"] == 0
    assert state["head_sha256"] == rec["entry_sha256"]


def test_chain_links_and_strict_monotonicity(tmp_path):
    ledger = tmp_path / "l.jsonl"
    r1 = _dec(ledger, "e1", 1_000_000)
    r2 = _dec(ledger, "e2", 2_000_000)
    assert r2["prev_entry_sha256"] == r1["entry_sha256"]
    with pytest.raises(ValueError, match="strictly"):
        _dec(ledger, "e3", 2_000_000)
    with pytest.raises(ValueError, match="strictly"):
        _dec(ledger, "e3", 1_500_000)
    assert verify_hash_chain(ledger)["n_records"] == 2


def test_label_field_refused_at_decision_moment(tmp_path):
    ledger = tmp_path / "l.jsonl"
    _dec(ledger, "e1", 1_000_000)
    with pytest.raises(ValueError, match="Rule 3"):
        append_decision_entry(
            ledger, entry_id="e2", timestamp_utc_us=2_000_000,
            instrument="BTCUSDT", layer1_phase="compression",
            layer2_p_up=0.6, layer2_ci_95=[0.55, 0.65],
            layer3_hazard_ratio=1.4, horizon_end_utc_us=12_000_000,
            feature_vector={"a": 1}, resolved_outcome_up=1,
        )
    with pytest.raises(ValueError, match="Rule 3"):
        append_decision_entry(
            ledger, entry_id="e2", timestamp_utc_us=2_000_000,
            instrument="BTCUSDT", layer1_phase="compression",
            layer2_p_up=0.6, layer2_ci_95=[0.55, 0.65],
            layer3_hazard_ratio=1.4, horizon_end_utc_us=12_000_000,
            feature_vector={"a": 1}, realized_return=0.03,
        )


def test_tampered_line_detected(tmp_path):
    ledger = tmp_path / "l.jsonl"
    _dec(ledger, "e1", 1_000_000)
    _dec(ledger, "e2", 2_000_000)
    lines = ledger.read_text().splitlines()
    rec = json.loads(lines[0])
    rec["layer2_p_up"] = 0.9
    lines[0] = json.dumps(rec, sort_keys=True, separators=(",", ":"))
    ledger.write_text("\n".join(lines) + "\n")
    with pytest.raises(ValueError, match="tampered"):
        verify_hash_chain(ledger)
    with pytest.raises(ValueError):
        _dec(ledger, "e3", 3_000_000)


def test_feature_vector_hash_is_content_canonical(tmp_path):
    a = feature_vector_sha256({"z": 1.0, "y": [1, 2]})
    b = feature_vector_sha256({"y": [1, 2], "z": 1.0})
    assert a == b
    assert feature_vector_sha256({"z": 1.0}) != a
    assert len(a) == 64


def test_resolution_only_after_horizon_and_append_only(tmp_path):
    ledger = tmp_path / "l.jsonl"
    _dec(ledger, "e1", 1_000_000, horizon_us=1_000)
    _dec(ledger, "e2", 2_000_000, horizon_us=10_000_000)
    before = ledger.read_text()
    df = pd.DataFrame({
        "instrument": ["BTCUSDT", "BTCUSDT"],
        "entry_timestamp_utc_us": [1_000_000, 2_000_000],
        "outcome_up": [1, 0],
    })
    summary = resolve_matured_entries(ledger, df, current_utc_us=3_000_000)
    assert summary["n_newly_resolved"] == 1
    assert summary["n_scored"] == 1
    text = ledger.read_text()
    assert text.startswith(before)
    lines = text.splitlines()
    assert len(lines) == 3
    res = json.loads(lines[2])
    assert res["record_type"] == "resolution"
    assert res["entry_id"] == "e1"
    assert res["prev_entry_sha256"] == json.loads(lines[1])["entry_sha256"]

    summary2 = resolve_matured_entries(ledger, df, current_utc_us=5_000_000)
    assert summary2["n_newly_resolved"] == 0
    assert summary2["n_scored"] == 1
    summary3 = resolve_matured_entries(ledger, df, current_utc_us=20_000_000)
    assert summary3["n_newly_resolved"] == 1
    assert summary3["n_scored"] == 2
    summary4 = resolve_matured_entries(ledger, df, current_utc_us=99_000_000)
    assert summary4["n_newly_resolved"] == 0
    assert summary4["n_scored"] == 2
    assert verify_hash_chain(ledger)["n_resolutions"] == 2


def test_missing_outcome_is_skipped_not_invented(tmp_path):
    ledger = tmp_path / "l.jsonl"
    _dec(ledger, "e1", 1_000_000, horizon_us=1_000)
    _dec(ledger, "e2", 2_000_000, horizon_us=1_000)
    df = pd.DataFrame({
        "instrument": ["BTCUSDT"],
        "entry_timestamp_utc_us": [1_000_000],
        "outcome_up": [1],
    })
    s = resolve_matured_entries(ledger, df, current_utc_us=9_000_000)
    assert s["n_newly_resolved"] == 1
    assert s["n_unresolved_missing_outcome"] == 1


def test_brier_skill_and_clopper_pearson(tmp_path):
    ledger = tmp_path / "l.jsonl"
    ps = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
    ys = [1, 1, 1, 1, 1, 1, 1, 0]
    for i, (p, y) in enumerate(zip(ps, ys)):
        _dec(ledger, f"e{i}", 1_000_000 + i, p_up=p, horizon_us=1)
    df = pd.DataFrame({
        "instrument": ["BTCUSDT"] * len(ys),
        "entry_timestamp_utc_us": [1_000_000 + i for i in range(len(ys))],
        "outcome_up": ys,
    })
    s = resolve_matured_entries(ledger, df, current_utc_us=10_000_000)
    assert s["n_scored"] == 8
    assert s["brier_score"] == pytest.approx(
        np.mean([(0.8 - y) ** 2 for y in ys]))
    assert s["hit_rate_up"] == pytest.approx(7 / 8)
    from scipy import stats
    lo = stats.beta.ppf(0.025, 7, 2)
    hi = stats.beta.ppf(0.975, 8, 1)
    assert s["hit_rate_up_cp95_low"] == pytest.approx(lo)
    assert s["hit_rate_up_cp95_high"] == pytest.approx(hi)
    assert s["hit_rate_up_cp95_low"] < 7 / 8 < s["hit_rate_up_cp95_high"]
    assert s["brier_skill_score_vs_rolling_climatology"] > 0


def test_rolling_climatology_first_entry_uses_half(tmp_path):
    ledger = tmp_path / "l.jsonl"
    _dec(ledger, "e0", 1_000_000, p_up=0.9, horizon_us=1)
    df = pd.DataFrame({
        "instrument": ["BTCUSDT"],
        "entry_timestamp_utc_us": [1_000_000],
        "outcome_up": [0],
    })
    s = resolve_matured_entries(ledger, df, current_utc_us=10_000_000)
    assert s["n_scored"] == 1
    assert s["brier_score"] == pytest.approx(0.81)
    assert s["brier_climatology_score"] == pytest.approx(0.25)
    assert s["brier_skill_score_vs_rolling_climatology"] == pytest.approx(
        1.0 - 0.81 / 0.25)


def test_calibration_metrics_on_empty_ledger(tmp_path):
    s = calibration_metrics(tmp_path / "none.jsonl")
    assert s["n_scored"] == 0
    assert s["brier_score"] is None
    assert s["hit_rate_up_cp95_low"] is None
