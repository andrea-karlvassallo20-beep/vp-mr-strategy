"""The state-matrix flow theory system - flow as a dynamical system
with attractors (owner-directive: "why not develop a state matrix
flow theory system of flow with attractors and all? whilst waiting
for l2").

PRE-DECLARED (registered BEFORE the run; universe: data_fresh,
min 310 bars, sigma>0 guard; night-to-night transitions pooled
across pairs):
  STATE SPACE (12): flow zone {XB, B, A, XA} x price third of the
  252d range {low, mid, high}.
  THE SYSTEM: the pooled 12x12 Markov transition matrix P
  (night t -> t+1); the stationary distribution pi (dominant
  eigenvector); ATTRACTORS = states with the largest self-loop
  persistence P(s->s) and longest mean residence time
  1/(1 - P(s->s)); BASIN DRAINAGE: P^30 rows (ergodic mixing) -
  which stationary mass each state drains into; MIXING TIME: the
  second-largest eigenvalue modulus, relaxation time
  1/(1-|lambda2|) in nights.
  REWARD FIELD over the states: P(first big move within 60d is UP)
  and mean forward-20d return per state (measured on the same
  nights) - the theory is descriptive geography, not a policy.
  HONEST CAVEATS (built in): first-order time-homogeneous Markov
  is a MODEL (regime drift breaks it); pairs pooled (heterogeneity
  averaged - the per-pair walk of session 56 showed dispersion);
  all in-sample; nothing armed; nothing trades live.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

FRESH = Path("paper/research/data_fresh")
OUT_CSV = Path("paper/research/clue_scan/flow_state_matrix_theory.csv")
OUT_MD = Path("paper/research/clue_scan/flow_state_matrix_theory.md")
VOL_MA, Z_WIN = 23, 252
SIGMA_WIN, MOVE_SIGMA, HORIZON = 20, 4.0, 60
RANGE_WIN = 252
MIN = 310
ZONES = ["XB", "B", "A", "XA"]
THIRDS = ["low", "mid", "high"]
STATES = [f"{z}_{t}" for z in ZONES for t in THIRDS]


def axisz(close, volume):
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    return ((vfi - vfi.rolling(Z_WIN).mean())
            / vfi.rolling(Z_WIN).std().replace(0, np.nan)
            ).clip(-10, 10)


def zone_i(zv):
    if not np.isfinite(zv):
        return -1
    if zv >= 1.5:
        return 3
    if zv >= 0:
        return 2
    if zv > -1.5:
        return 1
    return 0


def main():
    K = len(STATES)
    T = np.zeros((K, K))
    fd_store = {s: [] for s in range(K)}
    f20_store = {s: [] for s in range(K)}
    for f in sorted(FRESH.glob("*.csv")):
        df = pd.read_csv(f).reset_index(drop=True)
        if len(df) < MIN:
            continue
        for c in ("open", "high", "low", "close", "volume"):
            if c not in df.columns:
                df = None
                break
        if df is None:
            continue
        close = pd.Series(df["close"].to_numpy(), dtype=float)
        volume = pd.Series(df["volume"].to_numpy(), dtype=float)
        ret = close.pct_change()
        sigma = ret.rolling(SIGMA_WIN).std().shift(1)
        move = ((ret.abs() >= MOVE_SIGMA * sigma)
                & (sigma > 0)).to_numpy()
        up = ((ret >= MOVE_SIGMA * sigma) & (sigma > 0)).to_numpy()
        rng_hi = close.rolling(RANGE_WIN).max()
        rng_lo = close.rolling(RANGE_WIN).min()
        rp = (((close - rng_lo) / (rng_hi - rng_lo)
               .replace(0, np.nan))).shift(1).to_numpy()
        z = axisz(close, volume).shift(1).to_numpy()
        fwd20 = (close.shift(-20) / close - 1.0).shift(1).to_numpy()
        n = len(df)
        s_arr = np.full(n, -1, dtype=int)
        for i in range(n):
            zi = zone_i(z[i])
            if zi < 0 or not np.isfinite(rp[i]):
                continue
            t = 0 if rp[i] <= 1 / 3 else (2 if rp[i] >= 2 / 3 else 1)
            s_arr[i] = zi * 3 + t
        for i in range(n - 1):
            a, b = s_arr[i], s_arr[i + 1]
            if a >= 0 and b >= 0:
                T[a, b] += 1
        for i in range(n - HORIZON - 1):
            s = s_arr[i]
            if s < 0:
                continue
            fd = None
            for j in range(i + 1, min(i + HORIZON, n - 1) + 1):
                if move[j]:
                    fd = 1.0 if up[j] else -1.0
                    break
            if fd is not None:
                fd_store[s].append(fd)
            if np.isfinite(fwd20[i]):
                f20_store[s].append(float(fwd20[i]))

    rowsum = T.sum(axis=1, keepdims=True)
    P = np.divide(T, rowsum, out=np.zeros_like(T, dtype=float),
                  where=rowsum > 0)
    # stationary distribution
    eigval, eigvec = np.linalg.eig(P.T)
    k = int(np.argmax(eigval.real))
    pi = np.real(eigvec[:, k])
    pi = np.abs(pi)
    pi = pi / pi.sum()
    # second eigenvalue modulus
    mods = np.abs(eigval.real)
    mods_sorted = np.sort(mods)[::-1]
    lam2 = mods_sorted[1]
    relax = 1.0 / (1.0 - lam2) if lam2 < 1 else float("inf")
    # P^30 drainage
    P30 = np.linalg.matrix_power(P, 30)
    diag30 = np.diag(P30).copy()

    rows = []
    for s in range(K):
        fd = np.array(fd_store[s])
        f20 = np.array(f20_store[s])
        p_self = P[s, s]
        res = 1.0 / (1.0 - p_self) if p_self < 1 else float("inf")
        rows.append({
            "state": STATES[s], "self_loop": round(float(p_self), 4),
            "residence_nights": round(float(res), 1),
            "stationary_pi": round(float(pi[s]), 4),
            "drains_to": STATES[int(np.argmax(P30[s]))],
            "P30_stay_share": round(float(np.max(P30[s])), 4),
            "P_first_up": round(float((fd > 0).mean()), 4)
            if len(fd) else "",
            "mean_fwd20": round(float(f20.mean()), 4)
            if len(f20) else "",
            "n": len(fd),
        })
    # transition matrix export
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as fc:
        w = csv.writer(fc)
        w.writerow(["from\\to"] + STATES)
        for s in range(K):
            w.writerow([STATES[s]]
                       + [round(float(x), 4) for x in P[s]])
        w.writerow([])
        w.writerow(["state", "self_loop", "residence", "pi",
                    "drains_to", "P30_stay", "P_first_up",
                    "mean_fwd20", "n"])
        for r in rows:
            w.writerow([r["state"], r["self_loop"],
                        r["residence_nights"], r["stationary_pi"],
                        r["drains_to"], r["P30_stay_share"],
                        r["P_first_up"], r["mean_fwd20"], r["n"]])
    md = ["# The state-matrix flow theory system - flow as a",
          "dynamical system with attractors (12-state Markov",
          "system: flow zone x price third; pooled night",
          "transitions; in-sample descriptive; nothing armed;",
          "nothing trades live.)", "",
          f"Spectral: mixing relaxation time ~{round(relax, 1)}"
          f" nights (lambda2 = {round(float(lam2), 4)}).", "",
          "| state | self-loop | residence | pi | drains to |"
          " P30 stay | P_first_up | fwd20 | n |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['state']} | {r['self_loop']} "
                  f"| {r['residence_nights']} | {r['stationary_pi']} "
                  f"| {r['drains_to']} | {r['P30_stay_share']} "
                  f"| {r['P_first_up']} | {r['mean_fwd20']} "
                  f"| {r['n']} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)
    print("relaxation nights:", round(relax, 1),
          "lambda2:", round(float(lam2), 4))


if __name__ == "__main__":
    main()
