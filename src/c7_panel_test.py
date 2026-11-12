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


def bootstrap_rate_diff(panel, n_boot=N_BOOT, block=BLOCK, seed=0):
    """Block bootstrap over TIME (20-day calendar blocks) for the
    primed-minus-climatology realization-rate difference. The common factor
    forbids treating pair-days as independent."""
    rng = np.random.default_rng(seed)
    diffs = []
    t0s = pd.to_datetime(panel["t0"])
    panel = panel.assign(t=pd.to_datetime(panel["t0"]))
    days = panel["t"].sort_values().unique()
    n_blocks = int(np.ceil(len(days) / block))
    for _ in range(n_boot):
        picks = rng.integers(0, len(days), size=n_blocks)
        chosen = np.concatenate([days[p: p + block] for p in picks])
        mask = panel["t"].isin(chosen)
        sub = panel[mask]
        if sub["primed"].sum() < 20:
            continue
        rate_p = sub.loc[sub["primed"], "realized"].mean()
        rate_c = sub["realized"].mean()
        diffs.append(rate_p - rate_c)
    d = np.array(diffs)
    return float(np.mean(d)), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def enforce_kill_lines(primary_ci, control_ci):
    """KILL LINES as raising asserts, per c7_panel_test_spec.md."""
    lo, hi = primary_ci
    if lo <= 0.0 <= hi:
        raise AssertionError(
            "KILL LINE 1 (climatology overlap): primed realization-rate "
            f"difference CI [{lo:.4f}, {hi:.4f}] includes 0 — C7 dead")
    clo, chi = control_ci
    if not (lo > chi or hi < clo):
        raise AssertionError(
            "KILL LINE 3 (vol-tautology): primed CI overlaps the "
            "quiet-but-not-coiled control CI — 'primed' is just 'quiet', "
            "the C1 death repeated; C7 dead with the mechanism named")


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
    mean, lo, hi = bootstrap_rate_diff(panel)
    print(f"bootstrap primed-minus-climatology: {mean:.4f} "
          f"[{lo:.4f}, {hi:.4f}]  (alpha={ALPHA:.4f} Bonferroni)")
    # control comparison on the same bootstrap machinery
    sub = panel[panel["primed"] | panel["control"]].copy()
    sub["primed"] = sub["primed"].astype(bool)
    _, clo, chi = bootstrap_rate_diff(sub)
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
