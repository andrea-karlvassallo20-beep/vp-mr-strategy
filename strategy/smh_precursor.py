"""THE SMH PRECURSOR SIGNATURE BATTERY (charter v3, section 11,
open problem 3): can any weekly-observable footprint raise the
event hazard above the tercile table - above the clock itself?

This is where AVFI returns honestly: not as an inevitability, as a
testable signature with a calibration score. Candidate precursors,
pre-committed, all strictly causal at the compression entry:

  momentum    the trailing 20-bar log return (the known clock
              covariate - law 3's prior)
  sigma_pct   the entry sigma_w's percentile in its own expanding
              history (the known clock covariate - compression
              depth, measured 1.45x per SD)
  vol_trend   mean volume over the last 20 bars / last 60 bars:
              is effort DRYING into the compression (VSA's
              accumulation read) or building?
  range_eff   mean absolute 1-bar log move over the last 20 bars
              / last 60: is the path tightening beyond what
              sigma_w alone says?
  kama_eff    the Kaufman efficiency ratio over the last 20 bars,
              |net move| / sum|moves| in [0,1]: a directed, efficient
              approach into compression versus a noisy one

The event is the charter's frozen significant week (|r1| >= 2.5
sigma_w at entry, within 12 weeks), entry-anchored. The honest
hurdle a precursor must clear, pre-declared: the full model must
beat the CLOCK-ONLY model (momentum + sigma_pct) on OUT-OF-FOLD
concordance (ticker-split, no leakage), not merely show a
significant univariate z. The direction split of first events is
measured descriptively and REFUSED as a claim (central theorem);
every small cell stays flagged (doctrine rule 5).

Usage (nightly, after smh_gradient):
    python3 smh_precursor.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import (HORIZON, _tercile_states,
                          first_significant_week)
from smh_hazard import cox_fit
from smh_proof import EVENT_SIG, WARMUP, _series, _weekly_sigma

CLOCK_COVS = ("momentum", "sigma_pct")
NEW_COVS = ("vol_trend", "range_eff", "kama_eff")
ALL_COVS = CLOCK_COVS + NEW_COVS


def _entry_covariates(c, v, logc, sig, t) -> dict:
    mom = float(logc[t] - logc[max(0, t - 20)])
    hist = sig[WARMUP:t + 1][sig[WARMUP:t + 1] > 0]
    sig_pct = (float(np.mean(hist <= sig[t]))
               if len(hist) else 0.5)
    v20 = v[max(0, t - 19):t + 1].mean()
    v60 = v[max(0, t - 59):t + 1].mean()
    vol_trend = float(v20 / v60) if v60 > 0 else 1.0
    rets = np.abs(np.diff(logc[max(0, t - 60):t + 1]))
    r20 = rets[-20:].mean() if len(rets) >= 20 else rets.mean()
    r60 = rets.mean() if len(rets) else 1e-4
    range_eff = float(r20 / r60) if r60 > 0 else 1.0
    path = logc[max(0, t - 20):t + 1]
    net = abs(path[-1] - path[0]) if len(path) > 1 else 0.0
    tot = float(np.abs(np.diff(path)).sum()) if len(path) > 1 \
        else 1e-4
    kama_eff = float(net / tot) if tot > 0 else 0.0
    return {
        "momentum": mom,
        "sigma_pct": sig_pct,
        "vol_trend": vol_trend,
        "range_eff": range_eff,
        "kama_eff": kama_eff,
    }


def build_episodes(data_dir: Path) -> list:
    """Compression-entry episodes under the charter's frozen event,
    with all pre-committed covariates at entry."""
    eps = []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        for t in range(WARMUP + 1, len(c) - 1):
            if states[t] == 0 and states[t - 1] != 0:
                o = first_significant_week(logc, sig, t)
                if o > 0:
                    dur, ev = o, 1
                elif o == -1:
                    dur, ev = HORIZON, 0
                elif o < 0:
                    dur, ev = -o, 0
                else:
                    continue
                row = _entry_covariates(c, v, logc, sig, t)
                row["ticker"] = name
                row["duration"] = int(dur)
                row["event"] = ev
                eps.append(row)
    return eps


def _oof_concordance(eps: list, covs: tuple) -> dict:
    """Ticker-split out-of-fold concordance: fit on one half of
    the tickers, score Harrell's C on the other, and vice versa.
    No episode crosses the split - the leakage the charter's
    holdout lesson demands we close."""
    tickers = sorted({e["ticker"] for e in eps})
    half_a = set(tickers[::2])
    part_a = [e for e in eps if e["ticker"] in half_a]
    part_b = [e for e in eps if e["ticker"] not in half_a]
    cs = []
    for train, test in ((part_a, part_b), (part_b, part_a)):
        if len(train) < 200 or len(test) < 100:
            continue
        cox = cox_fit(train, covs=covs)
        mu = np.array(cox["_mu"])
        sd = np.array(cox["_sd"])
        beta = np.array(cox["_beta_raw"])
        X = np.array([[e[c_] for c_ in covs] for e in test])
        T = np.array([e["duration"] for e in test])
        E = np.array([e["event"] for e in test], dtype=bool)
        risk = ((X - mu) / sd) @ beta
        ev_idx = np.where(E)[0]
        conc = disc = 0
        for i in ev_idx:
            comp = (T > T[i]) | ((T == T[i]) & ~E)
            conc += int((risk[comp] < risk[i]).sum())
            disc += int((risk[comp] > risk[i]).sum())
        if conc + disc:
            cs.append(conc / (conc + disc))
    return {
        "n_folds": len(cs),
        "mean_concordance": (round(float(np.mean(cs)), 3)
                             if cs else None),
    }


def run_precursor(data_dir: Path) -> dict:
    eps = build_episodes(data_dir)
    if len(eps) < 200:
        return {"status": "INSUFFICIENT_EPISODES",
                "n_episodes": len(eps)}

    # univariate hazard ratios for the three candidate precursors
    univariate = {}
    for cov in NEW_COVS:
        c = cox_fit(eps, covs=(cov,))
        univariate[cov] = {
            "coef_per_sd": c["coefficients"][0],
            "z": c["z_stats"][0],
            "hazard_ratio_per_sd": c["hazard_ratios_per_sd"][0],
            "significant": bool(abs(c["z_stats"][0]) > 1.96),
        }

    # the full model vs the clock-only model, out of fold
    oof_clock = _oof_concordance(eps, CLOCK_COVS)
    oof_full = _oof_concordance(eps, ALL_COVS)
    # pre-declared materiality: a precursor must add at least half
    # a point of out-of-fold concordance to count - a 0.001 edge
    # is noise wearing a significant z (law 6's decay watch
    # starts from honest margins)
    MARGIN = 0.005
    beats_clock = (oof_full["mean_concordance"] is not None
                   and oof_clock["mean_concordance"] is not None
                   and oof_full["mean_concordance"]
                   >= oof_clock["mean_concordance"] + MARGIN)

    # the direction split of first events (descriptive, refused)
    # rebuilt from the raw series: sign of the first significant
    # week, with the Wilson band and the doctrine flag
    n_up = n_ev = 0
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        for t in range(WARMUP + 1, len(c) - 1):
            if states[t] == 0 and states[t - 1] != 0:
                thr = EVENT_SIG * sig[t]
                if thr <= 0:
                    continue
                k = t + 5
                end = min(t + HORIZON, len(logc) - 1)
                hit = False
                while k <= end:
                    if abs(logc[k] - logc[k - 5]) >= thr:
                        hit = True
                        break
                    k += 5
                if hit:
                    n_ev += 1
                    if logc[k] > logc[k - 5]:
                        n_up += 1
    p_up = n_up / n_ev if n_ev else None
    wilson = None
    if n_ev:
        z = 1.96
        den = 1 + z * z / n_ev
        ctr = (p_up + z * z / (2 * n_ev)) / den
        hw = z * math.sqrt(
            p_up * (1 - p_up) / n_ev + z * z / (4 * n_ev * n_ev)
        ) / den
        wilson = [round(max(0.0, ctr - hw), 3),
                 round(min(1.0, ctr + hw), 3)]

    verdict = {
        "precursor_beats_clock_oof": bool(beats_clock),
        "clock_oof_concordance": oof_clock["mean_concordance"],
        "full_oof_concordance": oof_full["mean_concordance"],
        "materiality_margin": MARGIN,
        "statement": ("a precursor signature must beat the "
                      "clock-only model OUT OF FOLD by at least "
                      "half a concordance point; a significant "
                      "univariate z with no out-of-fold margin is "
                      "noise wearing a p-value, not a signature"),
    }
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "n_episodes": len(eps),
        "covariates": list(ALL_COVS),
        "univariate_new_covariates": univariate,
        "out_of_fold": {
            "clock_only": oof_clock,
            "full_model": oof_full,
        },
        "verdict": verdict,
        "direction_split_first_events": {
            "n_events": n_ev,
            "n_up": n_up,
            "p_up": round(p_up, 3) if p_up is not None else None,
            "wilson_95": wilson,
            "claim": "REFUSED (central theorem): measured "
                     "descriptively only; the anticipated event is "
                     "a significant MOVE, not a signed one",
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH precursor signature battery")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_precursor(args.data_dir)
    dest = args.research_dir / "smh_precursor.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    v = r.get("verdict", {})
    print(f"smh precursor -> {dest} "
          f"({r.get('n_episodes')} episodes, "
          f"clock OOF {v.get('clock_oof_concordance')}, "
          f"full OOF {v.get('full_oof_concordance')}, "
          f"beats clock {v.get('precursor_beats_clock_oof')})")


if __name__ == "__main__":
    main()
