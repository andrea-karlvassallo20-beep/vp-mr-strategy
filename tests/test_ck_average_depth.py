"""Kill line 7(b) unit test: the CKS average-depth denominator, hand-checked.

The spec's requirement (paper/research/c1_l2_test_spec.md, kill line 7(b)):
any depth-normalized OFI feature must transcribe CKS's average-depth
formula literally — denominator 2(N(T_i) - N(T_{i-1}) - 1), both sides
summed — and pass a unit test against a hand-built 3-event interval
BEFORE the Tardis data is touched. An implementation failing this test
cannot run.

The hand arithmetic, written out so a reviewer can check it without
running anything:

    3-event interval, depths (q^B, q^A) = (10, 5), (20, 8), (30, 2)
    both sides summed = 10+5 + 20+8 + 30+2 = 75
    denominator = 2 * (N - 1) = 2 * (3 - 1) = 4     [the load-bearing -1]
    AD = 75 / 4 = 18.75

The WRONG implementations this test must catch, each computed explicitly:
    dividing by 2N instead of 2(N-1):  75 / 6  = 12.5   (must NOT match)
    one side only (bid):               60 / 4  = 15.0   (must NOT match)
    one side only (ask):               15 / 4  = 3.75   (must NOT match)
    last snapshot depth (30+2)/2:      16.0              (must NOT match)
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ck_average_depth import average_depth, depth_normalized_ofi


def _three_event_interval():
    return pd.DataFrame(
        {
            "bid_depth": [10.0, 20.0, 30.0],
            "ask_depth": [5.0, 8.0, 2.0],
        }
    )


def test_hand_built_three_event_interval():
    ad = average_depth(_three_event_interval())
    assert ad == pytest.approx(18.75)


def test_denominator_is_two_n_minus_one_not_two_n():
    # the load-bearing off-by-one: 2(N-1) = 4, not 2N = 6
    both_sides = 75.0
    n = 3
    assert both_sides / (2 * (n - 1)) == pytest.approx(18.75)
    assert both_sides / (2 * n) == pytest.approx(12.5)
    assert average_depth(_three_event_interval()) != pytest.approx(12.5)


def test_one_side_only_is_caught():
    events = _three_event_interval()
    bid_only = events["bid_depth"].sum() / 4  # 60/4 = 15.0
    ask_only = events["ask_depth"].sum() / 4  # 15/4 = 3.75
    ad = average_depth(events)
    assert ad != pytest.approx(bid_only)
    assert ad != pytest.approx(ask_only)


def test_last_snapshot_depth_is_caught():
    events = _three_event_interval()
    last_snapshot = (events["bid_depth"].iloc[-1] + events["ask_depth"].iloc[-1]) / 2
    assert average_depth(events) != pytest.approx(last_snapshot)  # 16.0


def test_single_event_interval_raises():
    one = pd.DataFrame({"bid_depth": [10.0], "ask_depth": [5.0]})
    with pytest.raises(ValueError, match="merge the interval"):
        average_depth(one)
    with pytest.raises(ValueError):
        average_depth(pd.DataFrame({"bid_depth": [], "ask_depth": []}))


def test_missing_columns_raise():
    with pytest.raises(ValueError, match="missing columns"):
        average_depth(pd.DataFrame({"bid": [1.0], "ask": [1.0]}))


def test_four_event_interval_hand_check():
    events = pd.DataFrame(
        {"bid_depth": [4.0, 4.0, 4.0, 4.0], "ask_depth": [2.0, 2.0, 2.0, 2.0]}
    )
    # both sides summed = 4*(4+2) = 24; denominator 2*(4-1) = 6; AD = 4
    assert average_depth(events) == pytest.approx(4.0)


def test_depth_normalized_ofi_uses_literal_ad():
    # OFI of 37.5 over the 3-event interval: 37.5 / 18.75 = 2.0
    assert depth_normalized_ofi(37.5, _three_event_interval()) == pytest.approx(2.0)


def test_depth_normalized_ofi_rejects_nonpositive_ad(monkeypatch):
    import ck_average_depth as mod
    monkeypatch.setattr(mod, "average_depth", lambda events: 0.0)
    with pytest.raises(ValueError, match="non-positive"):
        mod.depth_normalized_ofi(1.0, _three_event_interval())
