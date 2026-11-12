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

EVENT_SIG = 2.5
MOM_BARS = 20


def build_episodes(data_dir: Path) -> list:
    """Compression-entry episodes with entry covariates, durations,
    event flags - strictly causal throughout."""
    eps = []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
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
        "coefficients": [round(float(b), 3) for b in beta],
        "std_errors": [round(float(s), 3) for s in se],
        "z_stats": [round(float(zz), 2) for zz in z],
        "hazard_ratios_per_sd": [round(float(np.exp(b)), 3)
                                 for b in beta],
        "concordance": round(c_index, 3),
        "significant_covariates": [covs[k]
                                   for k in range(p)
                                   if abs(z[k]) > 1.96],
    }


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
    verdict = bool(cox["concordance"] > 0.55
                   and cox["significant_covariates"])
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
