"""THE SMH TEMPORAL CALIBRATION BATTERY: the forward log's dress
rehearsal.

The forward protocol logs rows in advance and scores them as
windows complete - but no row has resolved yet, so the forecast
instrument itself has never been scored. This battery runs the
rehearsal honestly, on time:

  SPLIT:   for every series, compression entries in the first 70%
           of bars form the TRAIN set; entries in the last 30%
           form the TEST set. The split is temporal within each
           series - the test episodes are strictly LATER than the
           training episodes, so nothing the model fit has seen
           the future it is scored on.
  FIT:     Kaplan-Meier baseline plus the Cox clock covariates
           (momentum, compression depth), on TRAIN only.
  FORECAST: for every TEST episode, the same formula the forward
           log drafts with: p = 1 - (1 - S0(60))^rel_hazard.
  SCORE:   Brier, log score, reliability bins - against the
           outcome the market actually produced.
  CLIMATOLOGY REFERENCE: the same scoring applied to the
           unconditional forecast (the TRAIN event rate from all
           eligible bars), the do-nothing counterfactual. The
           skill score is 1 - Brier/Brier_clim: positive means
           the compression-conditional forecast carries real
           out-of-sample information; zero or negative means it
           does not, and the forward log is scoring noise.

This is the instrument's pre-score. It does not replace the
forward log (doctrine rule 2: only rows logged in advance count);
it tells us, before the rows resolve, whether the thing being
logged is worth logging.

Usage (nightly, after smh_recurrence):
    python3 smh_calibration.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import (HORIZON, _tercile_states,
                          first_significant_week)
from smh_hazard import MOM_BARS, cox_fit, kaplan_meier
from smh_proof import WARMUP, _series, _weekly_sigma

TRAIN_FRAC = 0.70


def build_episodes(data_dir: Path) -> list:
    """Compression-entry episodes under the charter's frozen
    event, tagged with a train/test split (temporal, per series)."""
    eps = []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        cut = int(len(c) * TRAIN_FRAC)
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
                mom = float(logc[t]
                            - logc[max(0, t - MOM_BARS)])
                hist = sig[WARMUP:t + 1][
                    sig[WARMUP:t + 1] > 0]
                sig_pct = (float(np.mean(hist <= sig[t]))
                           if len(hist) else 0.5)
                eps.append({
                    "ticker": name,
                    "split": "train" if t < cut else "test",
                    "momentum": mom,
                    "sigma_pct": sig_pct,
                    "duration": int(dur),
                    "event": ev,
                })
    return eps


def climatology_rate(data_dir: Path) -> float:
    """The unconditional event rate: from every eligible bar in
    the TRAIN portion, the fraction whose 12-week window contains
    a significant week (threshold at that bar's own sigma)."""
    hits = tot = 0
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        cut = int(len(c) * TRAIN_FRAC)
        for t in range(WARMUP, cut - HORIZON):
            if sig[t] <= 0:
                continue
            thr = 2.5 * sig[t]
            tot += 1
            k = t + 5
            while k <= t + HORIZON:
                if abs(logc[k] - logc[k - 5]) >= thr:
                    hits += 1
                    break
                k += 5
    return hits / tot if tot else 0.5


def _baseline_surv(episodes: list, horizon: int) -> float:
    km = kaplan_meier(episodes)
    s = 1.0
    for row in km:
        if row["t"] <= horizon:
            s = row["survival"]
        else:
            break
    return s


def _brier_log(ps, ys):
    ps = np.asarray(ps, dtype=float)
    ys = np.asarray(ys, dtype=float)
    brier = float(np.mean((ps - ys) ** 2))
    logsc = float(np.mean(
        ys * np.log(ps) + (1 - ys) * np.log(1 - ps)))
    return brier, logsc


def _reliability(ps, ys):
    out = []
    ps = np.asarray(ps, dtype=float)
    ys = np.asarray(ys, dtype=float)
    for lo in [0.0, 0.2, 0.4, 0.6, 0.8]:
        m = (ps >= lo) & (ps < lo + 0.2)
        if m.sum() >= 3:
            out.append({
                "bin": f"{lo:.1f}-{lo + 0.2:.1f}",
                "n": int(m.sum()),
                "mean_p": round(float(ps[m].mean()), 3),
                "observed": round(float(ys[m].mean()), 3),
            })
    return out


def run_calibration(data_dir: Path) -> dict:
    eps = build_episodes(data_dir)
    train = [e for e in eps if e["split"] == "train"]
    test = [e for e in eps if e["split"] == "test"]
    if len(train) < 200 or len(test) < 100:
        return {"status": "INSUFFICIENT_EPISODES",
                "n_train": len(train), "n_test": len(test)}
    s0 = _baseline_surv(train, HORIZON)
    cox = cox_fit(train)
    mu = np.array(cox["_mu"])
    sd = np.array(cox["_sd"])
    beta = np.array(cox["_beta_raw"])
    p_clim_train = climatology_rate(data_dir)

    ps, ys = [], []
    for e in test:
        z = (np.array([e["momentum"], e["sigma_pct"]])
             - mu) / sd
        rel = float(np.exp(np.clip(float(beta @ z), -5, 5)))
        p = 1.0 - s0 ** rel
        ps.append(min(max(p, 1e-4), 0.9999))
        ys.append(e["event"])
    brier, logsc = _brier_log(ps, ys)
    rel_bins = _reliability(ps, ys)

    # climatology forecast: the unconditional train rate, the same
    # number for every episode (the do-nothing counterfactual)
    pc = [min(max(p_clim_train, 1e-4), 0.9999)] * len(ys)
    brier_c, logsc_c = _brier_log(pc, ys)
    skill = 1.0 - brier / brier_c if brier_c else None

    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "protocol": "temporal dress rehearsal: train on the first "
            "70% of each series' entries, score the forecast on "
            "the last 30%, against climatology. This does not "
            "replace the forward log (doctrine rule 2); it "
            "pre-scores the instrument being logged.",
        "n_train": len(train),
        "n_test": len(test),
        "train_baseline_p_12w": round(float(1 - s0), 3),
        "climatology_rate_train": round(p_clim_train, 3),
        "scores": {
            "brier": round(brier, 4),
            "log_score": round(logsc, 4),
            "reliability": rel_bins,
        },
        "climatology_scores": {
            "brier": round(brier_c, 4),
            "log_score": round(logsc_c, 4),
        },
        "skill_score": (round(skill, 4)
                        if skill is not None else None),
        "verdict": {
            "beats_climatology_oos": bool(
                skill is not None and skill > 0),
            "statement": ("positive skill means the compression-"
                          "conditional forecast carries real "
                          "out-of-sample information; zero or "
                          "negative means the forward log is "
                          "scoring noise, and the honesty note "
                          "would say so"),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH temporal calibration battery")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_calibration(args.data_dir)
    dest = args.research_dir / "smh_calibration.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    if r.get("status") != "OK":
        print(f"smh calibration -> {dest} ({r})")
        return
    print(f"smh calibration -> {dest} "
          f"(train {r['n_train']} / test {r['n_test']}, "
          f"Brier {r['scores']['brier']} vs clim "
          f"{r['climatology_scores']['brier']}, "
          f"skill {r['skill_score']}, "
          f"beats climatology "
          f"{r['verdict']['beats_climatology_oos']})")


if __name__ == "__main__":
    main()
