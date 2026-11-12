import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import verify_l2_gate as gate
import c1_l2_test as c1
from event_clock import assert_no_leakage


def _clean_diffs(n=2000, seed=0):
    rng = np.random.default_rng(seed)
    seq = np.arange(1000, 1000 + n)
    return pd.DataFrame({
        "ts_exchange_us": np.sort(rng.integers(0, 10**10, n)).astype("int64"),
        "seq_u": seq + 1,
        "seq_pu": seq,
        "side": rng.choice(["bid", "ask"], n),
        "price": np.round(np.abs(rng.normal(50000, 5, n)) + 1, 1),
        "size": rng.uniform(0.01, 2.0, n),
    })


def _snapshots_from_states(states, tick=0.1, n=100):
    rng = np.random.default_rng(5)
    rows = []
    for s in states:
        ts, mid, depth = s
        if mid is None or (isinstance(mid, float) and np.isnan(mid)):
            continue
        rows.append({
            "ts_exchange_us": ts + 1,
            "bid_price": mid - tick / 2,
            "ask_price": mid + tick / 2,
            "bid_depth_10bps": depth[0],
            "ask_depth_10bps": depth[1],
        })
    return pd.DataFrame(rows)


def test_gate_passes_on_clean_diffs(tmp_path):
    diffs = _clean_diffs()
    f = tmp_path / "diffs.csv"
    diffs.to_csv(f, index=False)
    code = gate.run_gate(f, snapshot_path=None, tick_size=0.1,
                         out_dir=tmp_path)
    assert code == 0
    assert (tmp_path / "gaps.log").exists()


def test_gate_fails_on_sequence_gap(tmp_path):
    diffs = _clean_diffs()
    diffs.loc[1000, "seq_pu"] = diffs.loc[1000, "seq_pu"] + 7
    f = tmp_path / "diffs.csv"
    diffs.to_csv(f, index=False)
    code = gate.run_gate(f, snapshot_path=None, tick_size=0.1, out_dir=tmp_path)
    assert code == 1


def test_gate_fails_on_mid_disagreement(tmp_path):
    diffs = _clean_diffs()
    f = tmp_path / "diffs.csv"
    diffs.to_csv(f, index=False)
    rc, states = gate.reconstruct(diffs, 0.1)
    snaps = _snapshots_from_states(states)
    bad = snaps.iloc[: len(snaps) // 2]
    bad.loc[:, "bid_price"] -= 5.0
    bad.loc[:, "ask_price"] -= 5.0
    snaps2 = pd.concat([bad, snaps.iloc[len(snaps) // 2:]]).sort_values("ts_exchange_us")
    sf = tmp_path / "snap.csv"
    snaps2.to_csv(sf, index=False)
    res = gate.sample_agreement(states, snaps2, 0.1)
    assert res["mid_agreement"] < 0.99
    code = gate.run_gate(f, snapshot_path=sf, tick_size=0.1, out_dir=tmp_path)
    assert code == 1


def test_gate_rejects_unknown_schema(tmp_path):
    f = tmp_path / "bad.csv"
    pd.DataFrame({"a": [1], "b": [2]}).to_csv(f, index=False)
    with pytest.raises(ValueError):
        gate.load_diffs(f)


def test_gap_logged_to_file(tmp_path):
    diffs = _clean_diffs()
    diffs.loc[500, "seq_pu"] += 3
    rc, _ = gate.reconstruct(diffs, 0.1, tmp_path / "gaps.log")
    assert rc.gaps == 1
    assert "GAP" in (tmp_path / "gaps.log").read_text()


def test_harness_compiles():
    out = c1.compile_check()
    assert "compiles" in out


def test_mock_pipeline_runs_mechanically():
    book, trades = c1.mock_l2(50_000, seed=1)
    bbba = c1.bbba_mid(book)
    assert {"mid", "bid_price", "ask_price"} <= set(bbba.columns)
    assert len(bbba) < len(book)
    small = bbba.iloc[:2000].reset_index(drop=True)
    small["compression"] = np.random.default_rng(0).integers(0, 2, len(small))
    small["sigma_h"] = 0.01
    small["hod_bucket"] = 0
    spells = c1.triple_barrier_trade_touch(small, trades, k=1.0,
                                            h_us=c1.H_PRIMARY)
    assert {"t0", "duration_h", "event", "compression"} <= set(spells.columns)
    assert spells["event"].isin([0, 1]).all()
    assert (spells["duration_h"] > 0).all()
    row_ts = spells["t0"].to_numpy()
    n_leak = 0
    for split in c1.purged_splits_for_c1(row_ts, h_us=c1.H_PRIMARY,
                                        embargo_us=c1.H_PRIMARY):
        assert_no_leakage(split, row_ts, c1.H_PRIMARY, c1.H_PRIMARY)
        n_leak += 0
    assert n_leak == 0


def test_kill_lines_fire():
    good = {
        "oof_concordance": 0.60,
        "tautology_hr_ci": (1.2, 1.5),
        "unrejected_powered_fold_fraction": 0.0,
        "stratified_hr_ci": (1.1, 1.4),
        "scale_null_gap_ci95": (0.001, 0.05),
        "observed_gap": 0.30,
    }
    c1.enforce_kill_lines(good)
    for key, bad in [
        ("oof_concordance", 0.52),
        ("tautology_hr_ci", (0.9, 1.1)),
        ("unrejected_powered_fold_fraction", 0.30),
        ("stratified_hr_ci", (0.95, 1.05)),
        ("scale_null_gap_ci95", (0.10, 0.40)),
    ]:
        with pytest.raises(AssertionError):
            c1.enforce_kill_lines({**good, key: bad})
