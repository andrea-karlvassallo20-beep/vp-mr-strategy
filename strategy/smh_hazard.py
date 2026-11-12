"""The SMH hazard model: Kaplan-Meier with censoring, and the Cox
proportional-hazards regression the SMH names as the frontier's
first open problem ("Hamilton's states meet Kaplan-Meier and Cox").

The tercile table gives one number per state; the hazard model asks
the sharper question: WITHIN compression, what raises or lowers the
hazard of the significant event? Covariates at compression ENTRY,
pre-committed:

  momentum  the trailing 20-bar log return (law 3's directional
            prior - does a running trend into compression change
            the clock?)
  sigma_pct the entry sigma_w's percentile in its own expanding
            history (how DEEP is the compression?)

Episode definition (frozen): an episode starts when a series enters
the compression tercile from outside it; the EVENT is a >= 2.5
sigma_w move (either direction) from the entry close, at sigma_w
measured at entry; censoring at episode end (state exit) or data
end. The regression is Cox partial likelihood (Breslow ties) by
Newton-Raphson, with Harrell's concordance as the calibration score.

Everything strictly causal: entry covariates use only trailing
information.

Usage (nightly):
    python3 smh_hazard.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from papertrading_runner import load_bars
from smh_proof import WARMUP, _series, _weekly_sigma
from v4_study import causal_z

EVENT_SIG = 2.5
MOM_BARS = 20


def build_episodes(data_dir: Path) -> list:
    """Compression-entry episodes with entry covariates (now
    including the AVFI causal stretch-z at entry, the section-17
    covariate), durations, event flags - strictly causal
    throughout."""
    eps = []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        z = causal_z(c)
        n = len(c)
        states = np.full(n, -1, dtype=int)
        for t in range(WARMUP, n):
            hist = sig[WARMUP:t + 1][sig[WARMUP:t + 1] > 0]
            if len(hist) < 60 or sig[t] <= 0:
                continue
            q1, q2 = np.quantile(hist, [1 / 3, 2 / 3])
            states[t] = 0 if sig[t] <= q1 else (
                1 if sig[t] <= q2 else 2)
        t = WARMUP
        while t < n - 1:
            if states[t] == 0 and states[t - 1] != 0:
                entry = t
                sig_e = sig[entry]
                if sig_e <= 0:
                    t += 1
                    continue
                mom = float(logc[entry] - logc[max(0, entry - MOM_BARS)])
                hist = sig[WARMUP:entry + 1][sig[WARMUP:entry + 1] > 0]
                sig_pct = (float(np.mean(hist <= sig_e))
                           if len(hist) else 0.5)
                thr = EVENT_SIG * sig_e
                dur = None
                event = 0
                k = entry + 1
                while k < n:
                    moved = abs(logc[k] - logc[entry])
                    if moved >= thr:
                        dur = k - entry
                        event = 1
                        break
                    if states[k] != 0:
                        dur = k - entry     # censored at state exit
                        break
                    k += 1
                if dur is None:
                    dur = n - 1 - entry     # censored at data end
                eps.append({
                    "ticker": name,
                    "momentum": mom,
                    "sigma_pct": sig_pct,
                    "stretch_z": round(float(z[entry]), 4),
                    "duration": int(dur),
                    "event": event,
                })
                t = k + 1 if event else k + 1
            else:
                t += 1
    return eps


def kaplan_meier(episodes: list) -> list:
    """The survival curve S(t) with proper censoring: P(no event
    yet) as a function of bars since compression entry."""
    durs = np.array([e["duration"] for e in episodes])
    evs = np.array([e["event"] for e in episodes])
    curve = []
    at_risk = len(durs)
    surv = 1.0
    for t in sorted(set(durs.tolist())):
        d = int(((durs == t) & (evs == 1)).sum())
        c = int(((durs == t) & (evs == 0)).sum())
        if at_risk > 0 and d > 0:
            surv *= (1.0 - d / at_risk)
        curve.append({"t": int(t), "n_at_risk": at_risk,
                      "events": d, "censored": c,
                      "survival": round(surv, 4)})
        at_risk -= d + c
    return curve


def cox_fit(episodes: list, covs=("momentum", "sigma_pct")) -> dict:
    """Cox proportional hazards by Newton-Raphson on the partial
    likelihood (Breslow handling of ties). Returns coefficients,
    standard errors, z-statistics, hazard ratios, and Harrell's
    concordance index - the model's calibration score."""
    X = np.array([[e[c_] for c_ in covs] for e in episodes],
                  dtype=float)
    T = np.array([e["duration"] for e in episodes])
    E = np.array([e["event"] for e in episodes], dtype=bool)
    n, p = X.shape
    # standardize covariates for conditioning
    mu, sd = X.mean(axis=0), X.std(axis=0)
    sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    beta = np.zeros(p)
    ev_idx = np.where(E)[0]
    for _ in range(50):
        eta = Z @ beta
        m = eta.max() if eta.size else 0.0
        w = np.exp(eta - m)            # shifted: always <= 1
        # log of the risk sum for event i: m + log(sum w_j) over the
        # risk set (numerically stable)
        ll_grad = np.zeros(p)
        H = np.zeros((p, p))
        for i in ev_idx:
            R = T >= T[i]
            sw = w[R].sum()
            if sw <= 0:
                continue
            xr = Z[R]
            logrisk = m + np.log(sw)
            s1 = (w[R] @ xr) / sw
            ll_grad += Z[i] - s1
            wr = w[R][:, None] * xr
            V = (wr.T @ xr) / sw - np.outer(s1, s1)
            H -= V
        if np.linalg.norm(ll_grad) < 1e-8:
            break
        # Newton for a MAXIMUM: beta -= H^{-1} g (H is the
        # negative-definite Hessian of the partial log-likelihood)
        step = np.linalg.solve(H - 1e-6 * np.eye(p), ll_grad)
        if not np.all(np.isfinite(step)):
            break
        beta = beta - step
    # standard errors from the observed information
    se = np.sqrt(np.diag(np.linalg.inv(-H + 1e-9 * np.eye(p))))
    z = beta / np.where(se > 0, se, 1e-9)
    # Harrell's concordance (vectorized)
    risk = Z @ beta
    conc = disc = 0
    for i in ev_idx:
        comp = (T > T[i]) | ((T == T[i]) & ~E)
        conc += int((risk[comp] < risk[i]).sum())
        disc += int((risk[comp] > risk[i]).sum())
    c_index = (float(conc / (conc + disc))
               if (conc + disc) else 0.5)
    return {
        "n_episodes": int(n),
        "n_events": int(E.sum()),
        "covariates": list(covs),
        "coefficients": [round(float(b), 4) for b in beta],
        "std_errors": [round(float(s), 3) for s in se],
        "z_stats": [round(float(zz), 2) for zz in z],
        "hazard_ratios_per_sd": [round(float(np.exp(b)), 3)
                                 for b in beta],
        "concordance": round(c_index, 3),
        "significant_covariates": [covs[k]
                                   for k in range(p)
                                   if abs(z[k]) > 1.96],
        # persisted for scoring: the standardization and the fitted
        # betas convert any new episode's covariates into a hazard
        "_mu": [round(float(x), 4) for x in mu],
        "_sd": [round(float(x), 4) for x in sd],
        "_beta_raw": [float(b) for b in beta],
    }


def _concordance_on(episodes: list, cox: dict,
                    covs: tuple) -> float:
    """Harrell's concordance of a FITTED model on a set of
    episodes (no refitting): the out-of-fold referee."""
    X = np.array([[e[c_] for c_ in covs] for e in episodes],
                  dtype=float)
    T = np.array([e["duration"] for e in episodes])
    E = np.array([e["event"] for e in episodes], dtype=bool)
    mu = np.array(cox["_mu"])
    sd = np.array(cox["_sd"])
    sd = np.where(sd == 0, 1.0, sd)
    Z = (X - mu) / sd
    risk = Z @ np.array(cox["_beta_raw"])
    ev_idx = np.where(E)[0]
    conc = disc = 0
    for i in ev_idx:
        comp = (T > T[i]) | ((T == T[i]) & ~E)
        conc += int((risk[comp] < risk[i]).sum())
        disc += int((risk[comp] > risk[i]).sum())
    return (float(conc / (conc + disc))
            if (conc + disc) else 0.5)


def _oof_concordance(episodes: list, covs: tuple,
                     split: float = 0.6) -> dict:
    """Fit on the first `split` of episodes (time-ordered),
    score concordance on the rest - the honest out-of-fold
    comparison the charter's Cox layer demands."""
    k = int(len(episodes) * split)
    if k < 50 or len(episodes) - k < 50:
        return {"verdict": "INSUFFICIENT_SPLIT"}
    fit = cox_fit(episodes[:k], covs)
    c = _concordance_on(episodes[k:], fit, covs)
    return {"fit_n": k, "test_n": len(episodes) - k,
            "c_index_oof": round(c, 3)}


def vassallo_scores(data_dir: Path, cox: dict,
                    baseline_surv_20: float) -> list:
    """THE VASSALLO SCORE: the likelihood of a significant event,
    expected mathematically, per market, at the latest close.

    For every market currently in the compression state, the Cox
    model's fitted coefficients convert its covariates (momentum
    into compression, compression depth) into a RELATIVE hazard;
    the Kaplan-Meier baseline survival at the 4-week horizon turns
    that into an ABSOLUTE probability:

        score = 1 - S0(20)^exp(beta . z)

    Strictly causal: covariates use only trailing information at
    the latest close. The score is a probability of a >= 2.5
    sigma_w move within 4 weeks - never a direction, per the
    central theorem. Ranked descending: the coiled springs with
    the highest mathematical expectation of the event."""
    mu = np.array(cox["_mu"])
    sd = np.array(cox["_sd"])
    beta = np.array(cox["_beta_raw"])
    out = []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        t = len(c) - 1
        hist = sig[WARMUP:t + 1][sig[WARMUP:t + 1] > 0]
        if len(hist) < 60 or sig[t] <= 0:
            continue
        q1, q2 = np.quantile(hist, [1 / 3, 2 / 3])
        state = ("compression" if sig[t] <= q1
                 else "mid" if sig[t] <= q2 else "high")
        if state != "compression":
            continue
        mom = float(logc[t] - logc[max(0, t - MOM_BARS)])
        sig_pct = float(np.mean(hist <= sig[t]))
        z = (np.array([mom, sig_pct]) - mu) / sd
        eta = float(beta @ z)
        rel_hazard = float(np.exp(np.clip(eta, -5, 5)))
        surv = baseline_surv_20 ** rel_hazard
        out.append({
            "ticker": name,
            "vassallo_score": round(float(1.0 - surv), 3),
            "relative_hazard": round(rel_hazard, 2),
            "momentum_20": round(mom, 3),
            "sigma_pct": round(sig_pct, 3),
            "sigma_w_pct": round(float(sig[t]) * 100, 2),
        })
    out.sort(key=lambda x: -x["vassallo_score"])
    return out


def run_hazard_model(data_dir: Path) -> dict:
    eps = build_episodes(data_dir)
    if len(eps) < 200:
        return {"status": "INSUFFICIENT_EPISODES",
                "n_episodes": len(eps)}
    km = kaplan_meier(episodes=eps)
    cox = cox_fit(eps)
    # survival at the 4-week mark (20 bars) - the clock's headline
    s20 = next((row["survival"] for row in km if row["t"] >= 20),
               None)
    scores = (vassallo_scores(data_dir, cox, s20)
              if s20 is not None else [])
    verdict = bool(cox["concordance"] > 0.55
                   and cox["significant_covariates"])

    # THE SECTION-17 COVARIATE QUESTION, out of fold: does adding
    # the AVFI stretch-z to the Cox layer beat the two-covariate
    # production model on held-out episodes? Pre-declared margin:
    # +0.01 concordance AND a significant z. The production
    # Vassallo Score keeps the two-covariate model unless the
    # margin is earned - and even then only until forward-scored.
    covs2 = ("momentum", "sigma_pct")
    covs3 = ("momentum", "sigma_pct", "stretch_z")
    cox3 = cox_fit(eps, covs3)
    oof2 = _oof_concordance(eps, covs2)
    oof3 = _oof_concordance(eps, covs3)
    stretch_earns = False
    if "c_index_oof" in oof2 and "c_index_oof" in oof3:
        stretch_earns = (
            oof3["c_index_oof"]
            >= oof2["c_index_oof"] + 0.01
            and "stretch_z" in cox3.get(
                "significant_covariates", []))
    if "c_index_oof" in oof2 and "c_index_oof" in oof3:
        stretch_verdict = (
            f"THE STRETCH COVARIATE EARNS ITS SLOT, DESIGN "
            f"SAMPLE: OOF concordance "
            f"{oof3['c_index_oof']} vs {oof2['c_index_oof']} "
            f"(duration alone = 0.5), significant z - flagged, "
            f"forward-scored or it stays folklore"
            if stretch_earns else
            f"THE STRETCH COVARIATE DOES NOT EARN ITS SLOT: OOF "
            f"concordance {oof3['c_index_oof']} vs the "
            f"production model's {oof2['c_index_oof']} "
            f"(duration alone = 0.5) - the section-17 cell's "
            f"hazard content rides the clock's own state, not "
            f"the Cox refinement; the two-covariate production "
            f"model stands")
    else:
        stretch_verdict = "INSUFFICIENT_SPLIT"
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "n_episodes": len(eps),
        "event_rate": round(float(np.mean(
            [e["event"] for e in eps])), 3),
        "survival_4_weeks": s20,
        "km_curve_head": km[:25],
        "cox": cox,
        "cox_with_stretch": cox3,
        "stretch_oof": {"production_2cov": oof2,
                        "with_stretch_3cov": oof3,
                        "earns_slot": stretch_earns,
                        "verdict": stretch_verdict},
        "vassallo_scores": scores,
        "verdict": verdict,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH hazard model (KM + Cox)")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_hazard_model(args.data_dir)
    dest = args.research_dir / "smh_hazard.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    print(f"smh hazard -> {dest} "
          f"({r.get('n_episodes')} episodes, "
          f"C-index {r.get('cox', {}).get('concordance')}, "
          f"verdict {r.get('verdict')})")


if __name__ == "__main__":
    main()
