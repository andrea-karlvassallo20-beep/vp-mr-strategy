import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import misses_2x2 as m2
from move_study import _pre_move_state


def _random_series(n=400, seed=0):
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    vol = np.abs(rng.normal(1000, 300, n))
    return close, vol


def test_parity_with_frozen_pre_move_state():
    close, vol = _random_series()
    flags = m2.primed_flags(close, vol)
    for t in list(range(60, len(close), 13)):
        state = _pre_move_state(close, vol, t)
        rule = (state is not None
                and state["comp_days"] >= 20
                and state["rvol_pct"] <= 33
                and state["range_pos"] <= 0.35)
        assert flags[t] == rule, f"definition drift at t={t}"


def test_moved_flags_horizon_is_strict():
    rng = np.random.default_rng(1)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0, 0.01, 200)))
    t = 150
    spike_day = t + m2.HORIZON          # exactly at the horizon edge: inside
    close2 = close.copy()
    close2[spike_day] *= 1.5
    assert m2.moved_flags(close2)[t]
    close3 = close.copy()
    close3[spike_day + 1] *= 1.5       # one day past the horizon: outside
    assert not m2.moved_flags(close3)[t]


def test_series_2x2_counts_a_primed_hit_and_unprimed_silence():
    rng = np.random.default_rng(2)
    turbulent = 100.0 * np.exp(np.cumsum(rng.normal(0, 0.05, 120)))
    coil = np.linspace(turbulent[-1] * 0.9, turbulent[-1] * 0.85, 120) \
        + rng.normal(0, 0.002, 120)
    close = np.concatenate([turbulent, coil])
    close[-3] *= 1.6                   # a >=4-sigma day inside the coil's horizon
    vol = np.full(len(close), 1000.0)
    df = pd.DataFrame({"close": close, "volume": vol})
    r = m2.series_2x2("synthetic", "crypto", df)
    assert r is not None
    assert r["primed_moved"] >= 1
    assert r["unprimed_silent"] >= 1
    total = (r["primed_moved"] + r["primed_silent"]
             + r["unprimed_moved"] + r["unprimed_silent"])
    assert total == r["n_days"]


def test_never_primed_series_counts_as_unprimed_moved():
    rng = np.random.default_rng(3)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0, 0.06, 300)))
    close[200] *= 1.5
    vol = np.full(len(close), 1000.0)
    df = pd.DataFrame({"close": close, "volume": vol})
    r = m2.series_2x2("wild", "crypto", df)
    assert r["n_primed"] == 0
    assert r["primed_moved"] == 0 and r["primed_silent"] == 0
    assert r["unprimed_moved"] >= 1


def test_aggregate_rates_sum_consistently():
    per = pd.DataFrame([
        {"series": "a", "class": "crypto", "n_days": 100, "n_primed": 40,
         "primed_moved": 10, "primed_silent": 30, "unprimed_moved": 5,
         "unprimed_silent": 55},
    ])
    agg = m2.aggregate(per).iloc[0]
    assert agg["base_rate_move"] == pytest.approx(15 / 100)
    assert agg["p_move_given_primed"] == pytest.approx(10 / 40)
    assert agg["p_move_given_unprimed"] == pytest.approx(5 / 60)
    assert agg["lift_primed_vs_unprimed"] == pytest.approx((10 / 40) / (5 / 60))
    assert agg["false_alarm_rate"] == pytest.approx(30 / 40)
    assert agg["coverage_of_moves"] == pytest.approx(10 / 15)
