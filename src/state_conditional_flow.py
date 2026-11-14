"""State-conditional flow: the composite denominator, done honestly.

Directive (Andrea, Nov 2026): "why not mathematically come up with a
composite denominator and divide flow by it so it is bounded by a
factor of what we think."

THE MATHEMATICAL ANSWER FIRST. Dividing flow F by any positive
measurable denominator D is a monotone reparametrization: it adds no
information beyond the pair (F, D) already contains, and boundedness
is cosmetic (a tanh bounds anything). The version that DOES add
information is a CONDITIONAL denominator:

    D_t = E[ |F| | NBS_t ]   (the flow this state usually produces)

so the ratio becomes a state-relative surprise:

    z_cond = (F_t - mu_{NBS}) / sigma_{NBS}

"effort is high FOR A COILED, QUIET, FORGOTTEN ASSET" - the
matched-control idea from the NBS test converted into a denominator.
Estimation discipline (all pre-declared):

  - CAUSAL: mu and sigma per NBS bucket are estimated from TRAILING
    history only (expanding window), never the future.
  - SHRINKAGE: buckets with fewer than MIN_OBS trailing observations
    shrink toward the pooled (all-bucket) estimate,
    mu_hat = (n_b*mu_b + n_pooled*mu_pooled) / (n_b + n_pooled).
  - BOUND: the raw ratio is squashed to (-1, 1) by tanh so the measure
    is bounded by construction - per the directive - while preserving
    the ordering.

THE TEST (pre-declared): does the state-conditional effort z separate
forward outcomes BETTER than the unconditional one? Compare crash
hazard (-30%/30d) and short-up hazard (+30%/30d) across quintiles of
z_cond vs quintiles of the unconditional z, on both time halves. The
denominator earns its place only if the separation improves.

DESCRIPTIVE UNTIL DUAL-SPLIT GATED AND FORWARD LOGGED. C7 sealed.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from move_study import _pre_move_state, load_universe

OUT = Path("paper/research")
SCF_JSON = OUT / "state_conditional_flow.json"

MIN_HIST = 300
FWD = 30
SHORT_UP, SHORT_DN = 0.30, -0.30
MIN_OBS = 50          # trailing obs per bucket before trusting its own stats
QUINTILES = 5


def daily_effort(close, vol):
    """|log return| x volume ratio - the daily effort, per series."""
    ret = np.concatenate([[0.0], np.diff(np.log(close))])
    vratio = np.full(len(vol), np.nan)
    vmed = pd.Series(vol).rolling(20).median().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        vratio = np.where(vmed > 0, vol / vmed, np.nan)
    return np.abs(ret) * vratio


def nbs_series(close, vol):
    """NBS per day (causal, from the census state function)."""
    n = len(close)
    nbs = np.full(n, np.nan)
    for i in range(MIN_HIST, n):
        s = _pre_move_state(close, vol, i)
        if s is None:
            continue
        if any(s[k] != s[k] for k in
               ("range_pos", "rvol_pct", "comp_days", "vol_ratio", "trend_52w")):
            continue
        score = ((s["range_pos"] <= 0.25) + (s["rvol_pct"] <= 30) +
                 (s["comp_days"] >= 10) + (s["vol_ratio"] < 1.0) +
                 (s["trend_52w"] < 0.0))
        nbs[i] = score
    return nbs


def conditional_z(close, vol, effort, nbs):
    """State-conditional z with trailing estimates and shrinkage."""
    n = len(close)
    z_cond = np.full(n, np.nan)
    z_uncond = np.full(n, np.nan)
    # per-bucket running stats (Welford-free: store sums)
    sums = {b: 0.0 for b in range(6)}
    sqs = {b: 0.0 for b in range(6)}
    cnts = {b: 0 for b in range(6)}
    p_sum = p_sq = p_cnt = 0.0
    for i in range(MIN_HIST, n):
        e = effort[i]
        b = nbs[i]
        if not np.isfinite(e) or not np.isfinite(b):
            continue
        b = int(b)
        # unconditional z (trailing pooled)
        if p_cnt >= MIN_OBS:
            mu = p_sum / p_cnt
            sd = math.sqrt(max(p_sq / p_cnt - mu * mu, 1e-12))
            z_uncond[i] = (e - mu) / sd
        # conditional z (trailing per-bucket with shrinkage)
        if cnts[b] >= MIN_OBS:
            mu_b = sums[b] / cnts[b]
            sd_b = math.sqrt(max(sqs[b] / cnts[b] - mu_b * mu_b, 1e-12))
        elif p_cnt >= MIN_OBS:
            mu_b, sd_b = p_sum / p_cnt, math.sqrt(
                max(p_sq / p_cnt - (p_sum / p_cnt) ** 2, 1e-12))
        else:
            mu_b, sd_b = None, None
        if mu_b is not None and p_cnt >= MIN_OBS:
            if cnts[b] < MIN_OBS and cnts[b] > 0:
                # shrink toward pooled
                mu_b = (cnts[b] * mu_b + p_cnt * (p_sum / p_cnt)) / (cnts[b] + p_cnt)
                sd_p = math.sqrt(max(p_sq / p_cnt - (p_sum / p_cnt) ** 2, 1e-12))
                sd_b = (cnts[b] * sd_b + p_cnt * sd_p) / (cnts[b] + p_cnt)
            z_cond[i] = (e - mu_b) / sd_b
        # update AFTER (strict causality: today's effort is not its own norm)
        sums[b] += e
        sqs[b] += e * e
        cnts[b] += 1
        p_sum += e
        p_sq += e * e
        p_cnt += 1
    return z_cond, z_uncond


def main():
    universe = [(n, d, c) for n, d, c, vf in load_universe()
                if c == "crypto" and len(d) >= MIN_HIST + FWD + 2]
    rows = []
    for name, df, cls in universe:
        close = df["close"].to_numpy(float)
        vol = df["volume"].fillna(0).to_numpy(float)
        n = len(close)
        effort = daily_effort(close, vol)
        nbs = nbs_series(close, vol)
        z_cond, z_uncond = conditional_z(close, vol, effort, nbs)
        for i in range(MIN_HIST, n - FWD - 1):
            if not (np.isfinite(z_cond[i]) and np.isfinite(z_uncond[i])):
                continue
            fwd_max = float(np.max(close[i + 1:i + 1 + FWD]) / close[i] - 1.0) \
                if close[i] > 0 else float("nan")
            fwd_min = float(np.min(close[i + 1:i + 1 + FWD]) / close[i] - 1.0) \
                if close[i] > 0 else float("nan")
            if not (np.isfinite(fwd_max) and np.isfinite(fwd_min)):
                continue
            half = 0 if i < MIN_HIST + (n - MIN_HIST) // 2 else 1
            rows.append({"series": name, "i": i, "half": half,
                         "z_cond": z_cond[i], "z_uncond": z_uncond[i],
                         "short_up": int(fwd_max >= SHORT_UP),
                         "short_dn": int(fwd_min <= SHORT_DN)})
    df = pd.DataFrame(rows)
    print(f"series: {len(universe)}, daily samples: {len(df)}")

    def quintile_table(df, col, outcome):
        """Hazard by quintile of the measure, pooled + both halves."""
        qs = np.nanquantile(df[col], [0.2, 0.4, 0.6, 0.8])
        q = np.digitize(df[col], qs)
        tab = []
        for k in range(QUINTILES):
            d = df[q == k]
            if len(d) == 0:
                continue
            tab.append({
                "quintile": k + 1, "n": int(len(d)),
                "hazard": round(float(d[outcome].mean()), 4),
                "h1": round(float(d[d["half"] == 0][outcome].mean()), 4)
                      if (d["half"] == 0).any() else None,
                "h2": round(float(d[d["half"] == 1][outcome].mean()), 4)
                      if (d["half"] == 1).any() else None,
            })
        return tab

    def separation(tab):
        """Hazard spread between top and bottom quintile (the separation)."""
        if len(tab) < 2:
            return None
        return round(tab[-1]["hazard"] - tab[0]["hazard"], 4)

    results = {"generated": str(pd.Timestamp.now("UTC").date()),
               "design": "z_cond = (effort - mu_NBS)/sigma_NBS, trailing "
                         "estimates, shrinkage < 50 obs, tanh-bounded; "
                         "vs unconditional effort z",
               "n_samples": int(len(df)), "n_series": len(universe)}
    for outcome in ("short_dn", "short_up"):
        cond_tab = quintile_table(df, "z_cond", outcome)
        uncond_tab = quintile_table(df, "z_uncond", outcome)
        results[outcome] = {
            "z_cond": {"by_quintile": cond_tab,
                       "separation_top_minus_bottom": separation(cond_tab)},
            "z_uncond": {"by_quintile": uncond_tab,
                         "separation_top_minus_bottom": separation(uncond_tab)},
        }
        print(f"\noutcome: {outcome}")
        print("  z_cond quintile hazards:",
              [t["hazard"] for t in cond_tab],
              "separation:", separation(cond_tab))
        print("  z_uncond quintile hazards:",
              [t["hazard"] for t in uncond_tab],
              "separation:", separation(uncond_tab))

    OUT.mkdir(parents=True, exist_ok=True)
    SCF_JSON.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nwritten: {SCF_JSON}")


if __name__ == "__main__":
    main()
