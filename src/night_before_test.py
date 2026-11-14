"""The night-before score (NBS) - the first causal predictability test.

Directive (Andrea, Nov 2026): "Can we create a short term indicator of
such criteria and test then of predictability."

The census counted what movers looked like the night before. It could
not test predictability because it had no denominator: no matched
control days that shared the state and did not move. This study builds
that denominator and answers ONE question:

  Does the night-before state RAISE the measured probability of a
  significant move in the next 30 days, versus all other days?

INDICATOR (pre-declared, from the registry - paper/research/
night_before_criteria.md, the composite forgotten-and-pinned signature
decomposed into additive points). NBS = number of criteria met on the
state day, 0-5, one point each:
    range_pos <= 0.25      (A1: at the range bottom)
    rvol_pct  <= 30        (A2: quiet, vol at/below its 30th pct)
    comp_days >= 10        (A3: coiled)
    vol_ratio <  1.0       (A5: volume dry-up)
    trend_52w <  0.0       (A6: down on the year)
State variables are computed by the SAME causal function the census
used (move_study._pre_move_state, trailing windows only).

OUTCOME (pre-declared, strictly forward from the state day):
    up-move   : close rises >= +100% above the state-day close within
                the next 30 trading days (crypto census threshold)
    down-move : close falls <= -70% below the state-day close within
                the next 30 trading days
    short-up  : >= +30% within 30 days (the short-term secondary)
    short-dn  : <= -30% within 30 days (the short-term secondary)

SAMPLING (pre-declared): one state day per series per non-overlapping
30-day window (stride 30), so samples are approximately independent.
Days with insufficient history (<300 bars) or NaN state are skipped.
Artifacts of the census kind cannot contaminate the OUTCOME here (no
rolling 30d return is used; the forward window is anchored at the
state day), but launch-era bases are still excluded via the 300-bar
history requirement.

HONESTY:
  - Time split: every hazard is reported on the FIRST half and SECOND
    half of each series separately as well as pooled; a real effect
    must hold in both halves (the dual-split spirit).
  - Multiplicity: 6 buckets x 4 outcomes are reported; the confirmatory
    test is declared as ONE comparison - NBS >= 4 vs NBS <= 1 for the
    up-move outcome - and its z-score/p-value is reported alongside all
    descriptive buckets. p-values are normal-approximation two-proportion
    z-tests; treat them as descriptive context, not proof.
  - The TVC panel's volume is synthetic (relative ratios only); the
    vol_ratio criterion inherits that limitation.
  - Whatever the result: descriptive until it passes the dual-split
    gate and the forward log. C7 stays sealed until then.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from move_study import _pre_move_state, load_universe, TVC

OUT = Path("paper/research")
NBS_JSON = OUT / "night_before_test.json"

UP_THR, DN_THR = 1.0, -0.70          # census crypto thresholds
SHORT_UP, SHORT_DN = 0.30, -0.30     # short-term secondary
MIN_HIST = 300                       # bars of history before the state day
FWD = 30                             # forward window (trading days)


def nbs_from_state(s):
    """The night-before score: 0-5, one point per registry criterion."""
    if s is None:
        return None
    if any(s[k] != s[k] for k in
           ("range_pos", "rvol_pct", "comp_days", "vol_ratio", "trend_52w")):
        return None
    score = 0
    if s["range_pos"] <= 0.25:
        score += 1
    if s["rvol_pct"] <= 30:
        score += 1
    if s["comp_days"] >= 10:
        score += 1
    if s["vol_ratio"] < 1.0:
        score += 1
    if s["trend_52w"] < 0.0:
        score += 1
    return score


def sample_series(name, df, cls):
    """Non-overlapping state days with forward outcomes for one series."""
    close = df["close"].to_numpy(float)
    vol = df["volume"].fillna(0).to_numpy(float)
    n = len(close)
    rows = []
    for i in range(MIN_HIST, n - FWD - 1, 30):   # stride 30: ~independent
        s = _pre_move_state(close, vol, i)
        score = nbs_from_state(s)
        if score is None:
            continue
        fwd_max = float(np.max(close[i + 1:i + 1 + FWD]) / close[i] - 1.0)
        fwd_min = float(np.min(close[i + 1:i + 1 + FWD]) / close[i] - 1.0)
        rows.append({
            "series": name, "class": cls, "idx": i,
            "half": 0 if i < MIN_HIST + (n - MIN_HIST) // 2 else 1,
            "nbs": score,
            "up": int(fwd_max >= UP_THR),
            "dn": int(fwd_min <= DN_THR),
            "short_up": int(fwd_max >= SHORT_UP),
            "short_dn": int(fwd_min <= SHORT_DN),
        })
    return rows


def two_prop_z(k1, n1, k2, n2):
    """Two-proportion z-test (normal approximation), two-sided."""
    if n1 == 0 or n2 == 0:
        return None
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return None
    z = (p1 - p2) / se
    pval = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
    return {"z": round(z, 3), "p": round(pval, 5),
            "hazard1": round(p1, 4), "hazard2": round(p2, 4),
            "n1": n1, "n2": n2, "k1": k1, "k2": k2}


def bucket_table(rows, outcome):
    df = pd.DataFrame(rows)
    tab = []
    for score in range(6):
        d = df[df["nbs"] == score]
        if len(d) == 0:
            continue
        tab.append({
            "nbs": score, "n": int(len(d)),
            "hits": int(d[outcome].sum()),
            "hazard": round(float(d[outcome].mean()), 4),
            "hazard_h1": round(float(d[d["half"] == 0][outcome].mean()), 4)
                         if (d["half"] == 0).any() else None,
            "hazard_h2": round(float(d[d["half"] == 1][outcome].mean()), 4)
                         if (d["half"] == 1).any() else None,
        })
    return tab, df


def main():
    universe = [(n, d, c) for n, d, c, vf in load_universe()
                if c == "crypto" and len(d) >= MIN_HIST + FWD + 2]
    print(f"crypto universe with >= {MIN_HIST}+ bars: {len(universe)} series")

    rows = []
    for name, df, cls in universe:
        rows.extend(sample_series(name, df, cls))
    print(f"state-day samples (stride 30): {len(rows)}")

    results = {
        "generated": str(pd.Timestamp.utcnow().date()),
        "indicator": "night-before score (NBS 0-5), registry composite",
        "criteria": ["range_pos<=0.25", "rvol_pct<=30", "comp_days>=10",
                     "vol_ratio<1", "trend_52w<0"],
        "outcomes": {
            "up": f"close >= +{UP_THR:.0%} vs state day within {FWD}d",
            "dn": f"close <= {DN_THR:.0%} vs state day within {FWD}d",
            "short_up": f"close >= +{SHORT_UP:.0%} within {FWD}d",
            "short_dn": f"close <= {SHORT_DN:.0%} within {FWD}d",
        },
        "n_samples": len(rows),
        "n_series": len(universe),
    }

    for outcome in ("up", "dn", "short_up", "short_dn"):
        tab, df = bucket_table(rows, outcome)
        base = float(df[outcome].mean())
        hi = df[df["nbs"] >= 4]
        lo = df[df["nbs"] <= 1]
        confirm = two_prop_z(int(hi[outcome].sum()), len(hi),
                             int(lo[outcome].sum()), len(lo))
        results[outcome] = {
            "baseline_hazard": round(base, 4),
            "by_score": tab,
            "confirmatory_nbs4plus_vs_nbs1less": confirm,
        }
        print(f"\noutcome: {outcome} (baseline {base:.3%})")
        for r in tab:
            print(f"  NBS={r['nbs']}: n={r['n']:4d}  "
                  f"hazard={r['hazard']:.3%}  "
                  f"h1={r['hazard_h1']}  h2={r['hazard_h2']}")
        print(f"  confirmatory (NBS>=4 vs NBS<=1): {confirm}")

    OUT.mkdir(parents=True, exist_ok=True)
    NBS_JSON.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nwritten: {NBS_JSON}")
    print("DESCRIPTIVE UNTIL DUAL-SPLIT GATED + FORWARD LOGGED. "
          "Multiplicity binds; C7 sealed.")


if __name__ == "__main__":
    main()
