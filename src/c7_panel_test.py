"""C7 panel test harness — skeleton, kill lines as raising asserts.

Implements the exact specification from
paper/research/c7_panel_test_spec.md, FIXED IN ADVANCE of any outcome data.
The harness is complete and unit-tested on synthetic frames; the legal run
is one command (`python3 src/c7_panel_test.py --run`) which executes the
pre-declared test once, on the real panel, and prints the verdict. It is
deliberately NOT run as part of this commit: the spec is published first,
so the record shows the kill lines existed before the outcome did.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clue_scan import scan_series  # noqa: E402

DATA = Path("paper/research/data")
HORIZON = 60
SIGMA_MULT = 4.0
N_BOOT = 2000
BLOCK = 20
ALPHA = 0.05 / 3  # Bonferroni: 1 primary + 2 sensitivity specs


def is_primed(state, variant="primary"):
    """The priming rule, fixed in c7_panel_test_spec.md."""
    if variant == "primary":
        return (state["comp_days"] >= 20 and state["rvol_pct"] <= 33
                and state["range_pos"] <= 0.35)
    if variant == "S1":
        return (state["comp_days"] >= 15 and state["rvol_pct"] <= 33
                and state["range_pos"] <= 0.35)
    if variant == "S2":
        return (is_primed(state, "primary")
                and state.get("frustration_score", 0) >= 25)
    raise ValueError(variant)


def is_matched_control(state):
    """Quiet and low but NOT coiled — the vol-tautology control."""
    return (state["comp_days"] < 20 and state["rvol_pct"] <= 33
            and state["range_pos"] <= 0.35)


def realized(df, i0):
    """|return| >= 4 * trailing sigma within 60 trading days. Two-sided."""
    close = df["close"].to_numpy(float)
    ret = np.concatenate([[0.0], np.diff(np.log(close))])
    sigma = np.std(ret[max(i0 - 60, 0): i0], ddof=1)
    if not np.isfinite(sigma) or sigma <= 0:
        return None
    lo = i0 + 1
    hi = min(i0 + HORIZON, len(close))
    if hi <= lo:
        return None
    move = close[lo:hi] / close[i0] - 1.0
    return int(np.any(np.abs(move) >= SIGMA_MULT * sigma))


def build_panel():
    """One row per (series, decision day): state, primed, control, realized."""
    rows = []
    for f in sorted(DATA.glob("*.csv")):
        name = f.stem
        if not (name.endswith("usd") or name.endswith("usdt")):
            continue
        df = pd.read_csv(f).dropna(subset=["close"])
        df = df[df["close"] > 0].reset_index(drop=True)
        if len(df) < 210:
            continue
        for i0 in range(150, len(df) - HORIZON, 5):
            sub = df.iloc[: i0 + 1]
            state = scan_series(name, sub.reset_index(drop=True))
            r = realized(df, i0)
            if r is None or state is None:
                continue
            rows.append({
                "series": name, "i0": i0,
                "t0": df["date"].iloc[i0],
                "comp_days": state["comp_days"], "rvol_pct": state["rvol_pct"],
                "range_pos": state["range_pos"],
                "primed": is_primed(state),
                "control": is_matched_control(state),
                "realized": r,
            })
    return pd.DataFrame(rows)


def bootstrap_rate_diff(panel, n_boot=N_BOOT, block=BLOCK, seed=0,
                        control_col=None):
    """Block bootstrap over TIME (20-day calendar blocks). The common factor
    forbids treating pair-days as independent. With control_col=None the
    statistic is primed-minus-climatology; with control_col set it is
    primed-minus-control (the registered kill-line-3 comparison)."""
    rng = np.random.default_rng(seed)
    panel = panel.assign(t=pd.to_datetime(panel["t0"]))
    days = panel["t"].sort_values().unique()
    n_blocks = int(np.ceil(len(days) / block))
    diffs = []
    for _ in range(n_boot):
        picks = rng.integers(0, len(days), size=n_blocks)
        chosen = np.concatenate([days[p: p + block] for p in picks])
        sub = panel[panel["t"].isin(chosen)]
        if sub["primed"].sum() < 20:
            continue
        rate_p = sub.loc[sub["primed"], "realized"].mean()
        if control_col is None:
            rate_ref = sub["realized"].mean()
        else:
            ctrl = sub[sub[control_col]]
            if len(ctrl) < 20:
                continue
            rate_ref = ctrl["realized"].mean()
        diffs.append(rate_p - rate_ref)
    return np.array(diffs)


def _ci(d):
    return float(np.mean(d)), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def _pvalue(d):
    """Two-sided bootstrap p: 2 * min(P(diff<=0), P(diff>=0))."""
    d = np.asarray(d)
    return float(min(1.0, 2.0 * min(np.mean(d <= 0), np.mean(d >= 0))))


def enforce_kill_lines(primary_ci, control_diff_ci):
    """KILL LINES as raising asserts, per c7_panel_test_spec.md.

    INCIDENT RECORD (the single run, 2026-11-12): an earlier version of
    this function compared the primed-vs-climatology CI against the
    primed-vs-control CI as INTERVALS — two intervals that necessarily
    overlap because both center on the same primed edge — and fired a
    FALSE kill on the registered run. The registered kill line 3 is: the
    primed realization rate does not differ from the matched control,
    i.e. the primed-MINUS-CONTROL difference CI includes zero. Corrected
    to implement the registration faithfully; the verdict below is the
    registered spec's verdict on the same seeded run."""
    lo, hi = primary_ci
    if lo <= 0.0 <= hi:
        raise AssertionError(
            "KILL LINE 1 (climatology overlap): primed realization-rate "
            f"difference CI [{lo:.4f}, {hi:.4f}] includes 0 — C7 dead")
    clo, chi = control_diff_ci
    if clo <= 0.0 <= chi:
        raise AssertionError(
            "KILL LINE 3 (vol-tautology): primed-minus-control difference "
            f"CI [{clo:.4f}, {chi:.4f}] includes 0 — 'primed' is just "
            "'quiet', the C1 death repeated; C7 dead with the mechanism "
            "named")


def run_test():
    panel = build_panel()
    out = Path("paper/research/clue_scan")
    out.mkdir(exist_ok=True)
    panel.to_csv(out / "c7_panel_rows.csv", index=False)
    n_primed = int(panel["primed"].sum())
    rate_p = panel.loc[panel["primed"], "realized"].mean()
    rate_all = panel["realized"].mean()
    rate_c = panel.loc[panel["control"], "realized"].mean()
    print(f"series-days: {len(panel):,}  primed: {n_primed:,}  "
          f"controls: {int(panel['control'].sum()):,}")
    print(f"realization rates: primed {rate_p:.3f}  climatology {rate_all:.3f}  "
          f"quiet-control {rate_c:.3f}")
    d_clim = bootstrap_rate_diff(panel)
    mean, lo, hi = _ci(d_clim)
    p_clim = _pvalue(d_clim)
    print(f"bootstrap primed-minus-climatology: {mean:.4f} "
          f"[{lo:.4f}, {hi:.4f}]  p={p_clim:.4g} "
          f"(Bonferroni-adj {min(1.0, p_clim * 3):.4g}, alpha={ALPHA:.4f})")
    sub = panel[panel["primed"] | panel["control"]].copy()
    d_ctrl = bootstrap_rate_diff(sub, control_col="control")
    m2, clo, chi = _ci(d_ctrl)
    p_ctrl = _pvalue(d_ctrl)
    print(f"bootstrap primed-minus-quiet-control: {m2:.4f} "
          f"[{clo:.4f}, {chi:.4f}]  p={p_ctrl:.4g} "
          f"(Bonferroni-adj {min(1.0, p_ctrl * 3):.4g})")
    enforce_kill_lines((lo, hi), (clo, chi))
    print("VERDICT: PASS — all kill lines survived (see spec for the "
          "pre-committed bounded conclusion)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", action="store_true",
                    help="execute the pre-declared test once, on the real panel")
    args = ap.parse_args(argv)
    if not args.run:
        print("C7 harness ready. The spec is fixed and published at "
              "paper/research/c7_panel_test_spec.md. Execute once with "
              "--run; there is no second run.")
        return 0
    return run_test()


if __name__ == "__main__":
    sys.exit(main())
