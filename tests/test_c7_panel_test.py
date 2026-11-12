import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from c7_panel_test import (
    is_primed, is_matched_control, realized, enforce_kill_lines,
    bootstrap_rate_diff, _ci, _pvalue,
)


def _state(comp=25, rvol=20, rng=0.3, frus=0):
    return {"comp_days": comp, "rvol_pct": rvol, "range_pos": rng,
            "frustration_score": frus}


def test_priming_rule_primary():
    assert is_primed(_state())
    assert not is_primed(_state(comp=19))          # coil too shallow
    assert not is_primed(_state(rvol=40))          # not quiet
    assert not is_primed(_state(rng=0.5))          # not pinned low


def test_priming_rule_variants():
    assert is_primed(_state(comp=15), "S1")
    assert not is_primed(_state(comp=14), "S1")
    assert is_primed(_state(frus=30), "S2")
    assert not is_primed(_state(frus=10), "S2")


def test_matched_control():
    assert is_matched_control(_state(comp=5))
    assert not is_matched_control(_state(comp=25))   # that's primed
    assert not is_matched_control(_state(comp=5, rvol=50))


def test_realized_two_sided():
    n = 200
    rng = np.random.default_rng(1)
    base = 100.0 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))  # sigma > 0
    close = base.copy()
    close[150:170] = base[150] * (1 + 0.5 * np.arange(20) / 20)  # +50% drift
    assert realized(pd.DataFrame({"close": close}), 150) == 1
    close2 = base.copy()
    close2[150:170] = base[150] * (1 - 0.5 * np.arange(20) / 20)  # -50% drift
    assert realized(pd.DataFrame({"close": close2}), 150) == 1  # two-sided
    flat = pd.DataFrame({"close": np.full(n, 100.0)})
    assert realized(flat, 150) is None  # zero sigma -> unmeasurable


def test_kill_line_1_fires():
    with pytest.raises(AssertionError, match="KILL LINE 1"):
        enforce_kill_lines((-0.01, 0.02), (0.1, 0.2))


def test_kill_line_3_fires():
    # kill line 3 = the primed-minus-CONTROL difference CI includes zero
    with pytest.raises(AssertionError, match="KILL LINE 3"):
        enforce_kill_lines((0.05, 0.15), (-0.02, 0.03))


def test_kill_line_3_survives_when_control_diff_excludes_zero():
    # the incident case: two diff CIs may overlap each other; what matters
    # is that the primed-minus-control interval excludes zero
    enforce_kill_lines((0.0637, 0.0932), (0.0561, 0.1004))


def test_kill_lines_pass_case():
    # a true pass: BOTH the climatology diff and the control diff exclude 0
    enforce_kill_lines((0.10, 0.20), (0.05, 0.15))


def test_bootstrap_runs_on_synthetic_panel():
    rng = np.random.default_rng(0)
    days = pd.date_range("2024-01-01", periods=400, freq="D")
    rows = []
    for d in days:
        for s in ("a", "b", "c"):
            primed = (s == "a") and (d.day % 3 == 0)
            realized_ = int(rng.random() < (0.5 if primed else 0.2))
            rows.append({"series": s, "t0": d, "t": d, "primed": primed,
                         "control": (s == "b"), "realized": realized_})
    panel = pd.DataFrame(rows)
    # bootstrap_rate_diff returns an array of differences (climatology path)
    d = bootstrap_rate_diff(panel, n_boot=50, block=10)
    assert isinstance(d, np.ndarray) and len(d) > 0
    mean, lo, hi = _ci(d)
    assert -1.0 <= lo <= mean <= hi <= 1.0
    assert np.isfinite(mean)
    p = _pvalue(d)
    assert 0.0 <= p <= 1.0
    # exercise the control_col path (the kill-line-3 comparison)
    d_ctrl = bootstrap_rate_diff(panel, n_boot=50, block=10,
                                 control_col="control")
    assert isinstance(d_ctrl, np.ndarray) and len(d_ctrl) > 0
    m2, lo2, hi2 = _ci(d_ctrl)
    assert -1.0 <= lo2 <= m2 <= hi2 <= 1.0
    p2 = _pvalue(d_ctrl)
    assert 0.0 <= p2 <= 1.0
