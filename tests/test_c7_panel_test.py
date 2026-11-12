import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from c7_panel_test import (
    is_primed, is_matched_control, realized, enforce_kill_lines,
    bootstrap_rate_diff,
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
    with pytest.raises(AssertionError, match="KILL LINE 3"):
        enforce_kill_lines((0.05, 0.15), (0.08, 0.12))


def test_kill_lines_pass_case():
    enforce_kill_lines((0.10, 0.20), (-0.02, 0.02))


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
    mean, lo, hi = bootstrap_rate_diff(panel, n_boot=50, block=10)
    assert -1.0 <= lo <= mean <= hi <= 1.0
    assert np.isfinite(mean)
