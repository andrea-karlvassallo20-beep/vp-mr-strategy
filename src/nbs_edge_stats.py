"""The mathematics of the NBS edge - is the crash-protection finding a
statistical edge, or a pooled illusion?

Directive (Andrea, Nov 2026): "Can we test mathematiques of any
statistical edge."

The night-before score test (night_before_test.py) found the composite
marks roughly half the short-term crash hazard (z = -7.29). This study
applies the project's full honesty mathematics to that finding:

  1. MULTIPLICITY DEFLATION. The test scanned 6 buckets x 4 outcomes;
     the confirmatory comparison was pre-declared, but the Bonferroni-
     adjusted p (x24) is reported regardless - an edge that dies at
     x24 was scan luck.
  2. OWN-SCALE BEATS. Pooled hazards mix scales across 156 series -
     the failure mode that faked the elevated-vol axis. The honest
     count: in how many series does the high-score state (NBS >= 4)
     carry a LOWER crash hazard than the low-score state (NBS <= 1),
     among series with enough samples in both groups? A sign test on
     the per-series hazard differences follows.
  3. EFFECT SIZE. Relative risk with 95% CI (log-normal approx),
     absolute risk reduction, and the number-needed-to-treat reading.
  4. EXPECTANCY. A crash filter is only an edge if forward returns
     differ. Mean/median forward 30d returns by NBS bucket, pooled
     and own-scale; then the filter as a strategy - always-long vs
     long-only-on-NBS>=4 - Sharpe of each, and the Deflated Sharpe
     Ratio of the filtered variant (deflated for the 24 scanned
     comparisons, via strategy/overfit_stats.py).

Pre-declared verdict rule (the project's convention): the finding is
an EDGE only if it survives (a) Bonferroni x24, (b) an own-scale
majority, and (c) a positive pooled AND own-scale expectancy sign.
Anything less is descriptive.

DESCRIPTIVE UNTIL DUAL-SPLIT GATED AND FORWARD LOGGED. C7 sealed.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, "strategy")
from move_study import _pre_move_state, load_universe
from night_before_test import nbs_from_state, MIN_HIST, FWD
from overfit_stats import sharpe_stats, deflated_sharpe, probabilistic_sharpe

OUT = Path("paper/research")
EDGE_JSON = OUT / "nbs_edge_stats.json"

SHORT_DN = -0.30          # the tested crash outcome
N_SCANNED = 24            # 6 buckets x 4 outcomes scanned in the source test
MIN_PER_GROUP = 5         # series needs >=5 samples in BOTH groups to count


def sample(name, df, cls):
    close = df["close"].to_numpy(float)
    vol = df["volume"].fillna(0).to_numpy(float)
    n = len(close)
    rows = []
    for i in range(MIN_HIST, n - FWD - 1, 30):
        s = _pre_move_state(close, vol, i)
        score = nbs_from_state(s)
        if score is None:
            continue
        fwd_max = float(np.max(close[i + 1:i + 1 + FWD]) / close[i] - 1.0)
        fwd_min = float(np.min(close[i + 1:i + 1 + FWD]) / close[i] - 1.0)
        fwd_ret = float(close[min(i + FWD, n - 1)] / close[i] - 1.0) \
            if close[i] > 0 else float("nan")
        if not (math.isfinite(fwd_ret) and math.isfinite(fwd_min)
                and math.isfinite(fwd_max)):
            continue
        rows.append({"series": name, "nbs": score,
                     "crash": int(fwd_min <= SHORT_DN),
                     "fwd_ret": fwd_ret, "fwd_min": fwd_min,
                     "fwd_max": fwd_max})
    return rows


def rr_ci(k1, n1, k2, n2):
    """Relative risk (group1/group2) with 95% CI, log-normal approx."""
    p1, p2 = k1 / n1, k2 / n2
    if p1 == 0 or p2 == 0:
        return None
    rr = p1 / p2
    se = math.sqrt(1 / k1 - 1 / n1 + 1 / k2 - 1 / n2)
    lo, hi = rr * math.exp(-1.96 * se), rr * math.exp(1.96 * se)
    return {"rr": round(rr, 3), "ci95": [round(lo, 3), round(hi, 3)],
            "p1": round(p1, 4), "p2": round(p2, 4)}


def sign_test(wins, totals):
    """Two-sided binomial sign test across series."""
    n, k = totals, wins
    if n == 0:
        return None
    from math import comb
    tail = sum(comb(n, i) for i in range(0, min(k, n - k) + 1))
    p = min(1.0, 2.0 * tail / 2 ** n)
    return {"wins": k, "n": n, "p": round(p, 5)}


def main():
    universe = [(n, d, c) for n, d, c, vf in load_universe()
                if c == "crypto" and len(d) >= MIN_HIST + FWD + 2]
    rows = []
    for name, df, cls in universe:
        rows.extend(sample(name, df, cls))
    df = pd.DataFrame(rows)
    print(f"series: {len(universe)}, samples: {len(df)}")

    hi = df[df["nbs"] >= 4]
    lo = df[df["nbs"] <= 1]

    # 1. multiplicity deflation
    k1, n1 = int(hi["crash"].sum()), len(hi)
    k2, n2 = int(lo["crash"].sum()), len(lo)
    p1, p2 = k1 / n1, k2 / n2
    pp = (k1 + k2) / (n1 + n2)
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    p_raw = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
    p_bonf = min(1.0, p_raw * N_SCANNED)
    print(f"\n1. crash hazard: NBS>=4 {p1:.3%} (n={n1}) vs NBS<=1 {p2:.3%} (n={n2})")
    print(f"   z={z:.2f}, p_raw={p_raw:.2e}, Bonferroni x{N_SCANNED}: {p_bonf:.2e}")

    # 2. own-scale beats
    wins, played, diffs = 0, 0, []
    per_series = []
    for name, g in df.groupby("series"):
        gh = g[g["nbs"] >= 4]
        gl = g[g["nbs"] <= 1]
        if len(gh) < MIN_PER_GROUP or len(gl) < MIN_PER_GROUP:
            continue
        hz_h, hz_l = gh["crash"].mean(), gl["crash"].mean()
        played += 1
        win = hz_h < hz_l
        wins += int(win)
        diffs.append(hz_h - hz_l)
        per_series.append({"series": name, "hazard_hi": round(float(hz_h), 3),
                           "hazard_lo": round(float(hz_l), 3),
                           "n_hi": len(gh), "n_lo": len(gl), "hi_lower": bool(win)})
    st = sign_test(wins, played)
    print(f"\n2. own-scale: NBS>=4 hazard < NBS<=1 hazard in {wins}/{played} "
          f"series (sign test p={st['p']})")
    print(f"   median per-series hazard difference: {np.median(diffs):+.3%}")

    # 3. effect size
    rr = rr_ci(k1, n1, k2, n2)
    arr = p2 - p1
    print(f"\n3. effect: RR={rr['rr']} (95% CI {rr['ci95']}), "
          f"ARR={arr:.2%}, NNT={1/arr:.1f}")

    # 4. expectancy
    by_score = []
    for score in range(6):
        d = df[df["nbs"] == score]
        if len(d) == 0:
            continue
        by_score.append({"nbs": score, "n": len(d),
                         "mean_fwd30d": round(float(d["fwd_ret"].mean()), 4),
                         "median_fwd30d": round(float(d["fwd_ret"].median()), 4),
                         "crash_rate": round(float(d["crash"].mean()), 4)})
    own_scale_ret = sum(
        1 for name, g in df.groupby("series")
        if len(g[g["nbs"] >= 4]) >= MIN_PER_GROUP and
        len(g[g["nbs"] <= 1]) >= MIN_PER_GROUP and
        g[g["nbs"] >= 4]["fwd_ret"].mean() > g[g["nbs"] <= 1]["fwd_ret"].mean())
    own_played = sum(
        1 for name, g in df.groupby("series")
        if len(g[g["nbs"] >= 4]) >= MIN_PER_GROUP and
        len(g[g["nbs"] <= 1]) >= MIN_PER_GROUP)
    print("\n4. expectancy (forward 30d return by score):")
    for r in by_score:
        print(f"   NBS={r['nbs']}: n={r['n']:4d} mean={r['mean_fwd30d']:+.2%} "
              f"median={r['median_fwd30d']:+.2%} crash={r['crash_rate']:.1%}")
    print(f"   own-scale mean-return wins (hi>lo): {own_scale_ret}/{own_played}")

    # filter as a strategy: always-long vs long-only-on-NBS>=4
    all_rets = df["fwd_ret"].to_numpy()
    filt_rets = hi["fwd_ret"].to_numpy()
    s_all = sharpe_stats(all_rets)
    s_filt = sharpe_stats(filt_rets)
    # DSR: the filtered Sharpe versus the Sharpe the best of N_SCANNED
    # zero-skill trials would manufacture. Trial Sharpes approximated by
    # the per-bucket Sharpes of the scanned grid (the honest available
    # proxy; a single-value list would give E[max]=0 and no deflation).
    bucket_srs = [sharpe_stats(df[df["nbs"] == sc]["fwd_ret"].to_numpy())["sr"]
                  for sc in range(6) if len(df[df["nbs"] == sc]) >= 30]
    trials = (bucket_srs + [s_all["sr"]]) * 4   # 6 buckets x 4 outcomes proxy
    dsr = deflated_sharpe(filt_rets, trials)
    psr_vs_always = probabilistic_sharpe(filt_rets, s_all["sr"])
    print(f"\n   always-long: Sharpe {s_all['sr']:.3f} "
          f"(n={s_all['n']})")
    print(f"   NBS>=4 filter: Sharpe {s_filt['sr']:.3f} "
          f"(n={s_filt['n']}), PSR vs always-long {psr_vs_always:.3f}, "
          f"DSR {dsr['dsr']:.3f} (deflated for {dsr['n_trials']} trials, "
          f"passes 0.95: {dsr['passes_95']})")

    results = {
        "generated": str(pd.Timestamp.now("UTC").date()),
        "question": "is the NBS crash-protection a statistical edge?",
        "multiplicity": {"z": round(z, 3), "p_raw": p_raw,
                         "p_bonferroni_x24": p_bonf,
                         "survives": bool(p_bonf < 0.05)},
        "own_scale": {"wins": wins, "played": played, "sign_p": st["p"],
                      "median_hazard_diff": round(float(np.median(diffs)), 4),
                      "survives": bool(wins > played / 2),
                      "per_series": per_series},
        "effect_size": {**rr, "arr": round(arr, 4),
                        "nnt": round(1 / arr, 1) if arr > 0 else None},
        "expectancy": {"by_score": by_score,
                       "own_scale_mean_wins": own_scale_ret,
                       "own_scale_played": own_played,
                       "always_long_sharpe": s_all["sr"],
                       "filter_sharpe": s_filt["sr"],
                       "psr_filter_beats_always": round(psr_vs_always, 4),
                       "filter_dsr": dsr},
        "verdict_rule": "EDGE only if: Bonferroni x24 survives AND "
                        "own-scale majority AND positive pooled+own-scale "
                        "expectancy sign",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    EDGE_JSON.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nwritten: {EDGE_JSON}")


if __name__ == "__main__":
    main()
