"""equity-alpha-lab tests: synthetic panels, leakage traps, and audits.

Every test builds a small synthetic panel where the ground truth is known
by construction, then asserts the pipeline either computes the right thing
or REFUSES in the right way. The leakage tests deliberately construct
cheating snapshots and require the tripwire to fire.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from equity_alpha_lab import (
    LeakageError,
    adjustment_continuity_report,
    assert_no_future_information,
    check_panel,
    forward_returns,
    missingness_report,
    pit_fundamentals,
    survivorship_audit,
    total_return_series,
    universe_asof,
    validate_fundamentals,
    validate_prices,
    validate_security_master,
)

DATES = pd.bdate_range("2024-01-01", periods=10)


def _security_master():
    return pd.DataFrame(
        {
            "sid": ["A", "B", "C"],
            "ticker": ["AAA", "BBB", "CCC"],
            "member_start": [DATES[0], DATES[0], DATES[4]],
            "member_end": [pd.NaT, DATES[7], pd.NaT],
            "exchange": ["XNYS", "XNYS", "XNYS"],
            "delisting_return": [np.nan, -0.55, np.nan],
        }
    )


def _prices():
    rows = []
    for sid, drift in [("A", 0.001), ("B", 0.0), ("C", -0.001)]:
        for i, d in enumerate(DATES):
            rows.append(
                {
                    "sid": sid,
                    "date": d,
                    "open": 100.0 + i,
                    "high": 101.0 + i,
                    "low": 99.0 + i,
                    "close": 100.0 * (1 + drift) ** i,
                    "adj_factor": 1.0,
                    "volume": 1_000.0,
                }
            )
    px = pd.DataFrame(rows)
    # B has a 2:1 split on DATES[5]: unadjusted close halves, factor doubles.
    mask = (px["sid"] == "B") & (px["date"] >= DATES[5])
    px.loc[mask, "close"] = px.loc[mask, "close"] / 2
    px.loc[mask, "adj_factor"] = 2.0
    return px


# ---------------------------------------------------------------- schema

def test_schema_rejects_announce_before_period_end():
    fd = pd.DataFrame(
        {
            "sid": ["A"],
            "field": ["earnings"],
            "period_end": [pd.Timestamp("2024-03-31")],
            "announce_date": [pd.Timestamp("2024-03-30")],
            "value": [1.0],
        }
    )
    with pytest.raises(ValueError, match="announce_date must be >= period_end"):
        validate_fundamentals(fd)


def test_schema_rejects_bad_membership_interval_and_dupes():
    sm = _security_master()
    sm.loc[0, "member_end"] = DATES[0] - pd.Timedelta(days=1)
    with pytest.raises(ValueError, match="member_end < member_start"):
        validate_security_master(sm)
    sm = _security_master()
    sm.loc[len(sm)] = sm.loc[0]
    with pytest.raises(ValueError, match="duplicate"):
        validate_security_master(sm)
    px = _prices()
    px.loc[len(px)] = px.loc[0]
    with pytest.raises(ValueError, match="duplicate"):
        validate_prices(px)


# ---------------------------------------------------------------- universe

def test_universe_asof_is_point_in_time():
    sm = _security_master()
    early = universe_asof(sm, DATES[1])
    assert set(early["sid"]) == {"A", "B"}  # C joined at DATES[4]
    mid = universe_asof(sm, DATES[7])
    assert set(mid["sid"]) == {"A", "C"}  # B's interval ends at DATES[7]
    assert set(universe_asof(sm, DATES[4])["sid"]) == {"A", "B", "C"}


def test_survivorship_audit_counts_the_dropped_names():
    sm = _security_master()
    audit = survivorship_audit(sm, DATES[5])
    assert audit["members_asof"] == 3
    assert audit["exited_before_asof"] == 0
    audit = survivorship_audit(sm, DATES[9])
    assert audit["members_asof"] == 2
    assert audit["exited_before_asof"] == 1  # B, the survivorship trap


# ---------------------------------------------------------------- pit

def _fundamentals():
    return pd.DataFrame(
        {
            "sid": ["A", "A", "A"],
            "field": ["earnings", "earnings", "earnings"],
            "period_end": [
                pd.Timestamp("2023-12-31"),
                pd.Timestamp("2024-03-31"),
                pd.Timestamp("2024-06-30"),
            ],
            "announce_date": [
                pd.Timestamp("2024-02-10"),
                pd.Timestamp("2024-05-01"),
                pd.Timestamp("2024-08-01"),
            ],
            "value": [1.0, 2.0, 3.0],
        }
    )


def test_pit_snapshot_uses_announce_date_not_period_end():
    fd = _fundamentals()
    snap = pit_fundamentals(fd, pd.Timestamp("2024-03-01"))
    # Q1 was announced 2024-05-01: NOT available in March even though its
    # period ended in March. The Q4 value must still be the live one.
    assert snap.loc[0, "value"] == 1.0
    snap = pit_fundamentals(fd, pd.Timestamp("2024-05-01"))
    assert snap.loc[0, "value"] == 2.0
    snap = pit_fundamentals(fd, pd.Timestamp("2024-08-15"))
    assert snap.loc[0, "value"] == 3.0


def test_leakage_tripwire_catches_period_end_cheating():
    fd = _fundamentals()
    # A snapshot built keyed on period_end instead of announce_date would
    # hand the Q1 value (period ends 2024-03-31) to a March decision date.
    cheating = pd.DataFrame(
        {
            "sid": ["A"],
            "field": ["earnings"],
            "value": [2.0],  # announced 2024-05-01, decision date 2024-03-01
        }
    )
    with pytest.raises(LeakageError):
        assert_no_future_information(cheating, fd, pd.Timestamp("2024-03-01"))


def test_leakage_tripwire_passes_honest_snapshot():
    fd = _fundamentals()
    honest = pit_fundamentals(fd, pd.Timestamp("2024-06-01"))
    assert_no_future_information(honest[["sid", "field", "value"]], fd,
                                  pd.Timestamp("2024-06-01"))


# ---------------------------------------------------------------- returns

def test_total_return_series_is_split_continuous():
    px = _prices()
    tr = total_return_series(px)
    b = tr.xs("B", level="sid")
    day_rets = b.pct_change().dropna()
    # B has zero drift: every total return must be ~0, including across the
    # split day where the unadjusted close halves.
    assert day_rets.abs().max() < 1e-9


def test_forward_returns_match_hand_computation():
    px = _prices()
    sm = _security_master()
    fr = forward_returns(px, sm, horizon=2, entry_delay=1)
    a = fr[fr["sid"] == "A"].set_index("decision_date")
    tr = total_return_series(px).xs("A", level="sid")
    d0 = DATES[0]
    expected = tr.loc[DATES[3]] / tr.loc[DATES[1]] - 1.0
    assert a.loc[d0, "fwd_ret"] == pytest.approx(expected)
    assert a.loc[d0, "entry_date"] == DATES[1]
    assert a.loc[d0, "exit_date"] == DATES[3]
    assert not a.loc[d0, "delisted"]


def test_forward_returns_apply_delisting_return():
    px = _prices()
    sm = _security_master()
    fr = forward_returns(px, sm, horizon=5, entry_delay=1)
    b = fr[(fr["sid"] == "B") & (fr["decision_date"] == DATES[5])]
    assert len(b) == 1
    row = b.iloc[0]
    # B stops trading after DATES[6] (member_end DATES[7]); entry DATES[6],
    # horizon 5 runs off the panel -> close at last price then apply -55%.
    assert row["delisted"]
    # B stops trading after DATES[6] (member_end DATES[7]); entry DATES[6],
    # horizon 5 runs off the panel -> close at last price (zero drift) then
    # apply the -55% delisting return.
    assert row["fwd_ret"] == pytest.approx(-0.55)


def test_forward_returns_drop_unexitable_rows_explicitly():
    px = _prices()
    sm = _security_master()
    sm.loc[sm["sid"] == "B", "delisting_return"] = np.nan
    fr = forward_returns(px, sm, horizon=5, entry_delay=1)
    dropped = fr[(fr["sid"] == "B") & fr["dropped"]]
    assert len(dropped) > 0  # counted, never silently filled
    assert dropped["fwd_ret"].isna().all()


def test_forward_returns_reject_same_close_execution():
    with pytest.raises(ValueError, match="entry_delay"):
        forward_returns(_prices(), _security_master(), entry_delay=0)


# ---------------------------------------------------------------- quality

def test_continuity_report_flags_unadjusted_gap_without_factor_change():
    px = _prices()
    # A crashes 30% with no adj_factor change: must be flagged.
    crash = (px["sid"] == "A") & (px["date"] == DATES[3])
    px.loc[crash, "close"] *= 0.70
    flagged = adjustment_continuity_report(px, max_unexplained_daily_ret=0.20)
    assert (flagged["sid"] == "A").any()
    # The split day itself (factor changed) must NOT be flagged.
    split_rows = flagged[flagged["sid"] == "B"]
    assert len(split_rows) == 0


def test_missingness_report_counts_panel_gaps():
    px = _prices()
    px = px.drop(index=px[(px["sid"] == "A") & (px["date"] == DATES[3])].index)
    rep = missingness_report(px).set_index("sid")
    assert rep.loc["A", "missing"] == 1
    assert rep.loc["B", "missing"] == 0


def test_check_panel_raises_on_schema_and_returns_findings():
    sm = _security_master()
    px = _prices()
    # A halves permanently from DATES[3] with no adj_factor change: exactly
    # the -50% day must be flagged (the days after it are flat again).
    crash = (px["sid"] == "A") & (px["date"] >= DATES[3])
    px.loc[crash, "close"] *= 0.50
    fd = _fundamentals()
    findings = check_panel(sm, px, fd)
    assert findings["n_securities"] == 3
    assert findings["n_flagged_continuity"] == 1
    assert findings["fundamentals_without_prices"] == []
    with pytest.raises(ValueError):
        check_panel(sm, px.assign(adj_factor=-px["adj_factor"]), fd)
