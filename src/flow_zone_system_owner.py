"""THE OWNER'S CANONICAL ZONE SYSTEM - the state matrix with the
owner's zones, corrected geometry (owner-directive): "no no, there
are only a few zones: from above, below 0 or above 0, from below
above 0 or below 0 both crossing, extremity top and extremity
bottom, with movement to extremity, that's it."

THE SEVEN STATES (registered, the owner's list verbatim):
  EXT_BOT   z <= -1.5                      (extremity bottom)
  BELOW     -1.5 < z < 0                   (below 0)
  CROSS_UP  transition day below -> above 0
  ABOVE     0 <= z < 1.5                    (above 0)
  EXT_TOP   z >= 1.5                       (extremity top)
  CROSS_DN  transition day above -> below 0
  MOVE_EXT  approaching an extremity: in the 1.1..1.5 band rising
            (toward EXT_TOP) or the -1.5..-1.1 band falling (toward
            EXT_BOT) over the last 5 nights - "movement to
            extremity"
Precedence: extremity bands > crossing days > movement-to-extremity
> the two zero-side zones. THE SYSTEM: pooled 7x7 transition
matrix, stationary pi, self-loop persistence/residence (dwell
states), reward field (P(first big move within 60d is UP) + mean
fwd-20d per state). Crossings are 1-night transition states by
construction. All in-sample descriptive; nothing armed; nothing
trades live.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

FRESH = Path("paper/research/data_fresh")
OUT = Path("paper/research/clue_scan/flow_zone_system_owner.csv")
OUT_MD = Path("paper/research/clue_scan/flow_zone_system_owner.md")
VOL_MA, Z_WIN = 23, 252
SIGMA_WIN, MOVE_SIGMA, HORIZON = 20, 4.0, 60
MIN = 310
STATES = ["EXT_BOT", "BELOW", "CROSS_UP", "ABOVE", "EXT_TOP",
          "CROSS_DN", "MOVE_EXT"]


def axisz(close, volume):
    v = (volume / volume.shift(1).rolling(VOL_MA).mean()
         .replace(0, np.nan) - 1.0).clip(0, 3.0).fillna(0.0)
    up_g = (close >= close.shift(1) * 1.01).astype(float)
    dn_g = (close <= close.shift(1) * 0.99).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    return ((vfi - vfi.rolling(Z_WIN).mean())
            / vfi.rolling(Z_WIN).std().replace(0, np.nan)
            ).clip(-10, 10)


def state_of(z, z_prev, z_5):
    if not np.isfinite(z):
        return -1
    if z >= 1.5:
        return 4
    if z <= -1.5:
        return 0
    if np.isfinite(z_prev) and z_prev < 0 and z >= 0:
        return 2
    if np.isfinite(z_prev) and z_prev >= 0 and z < 0:
        return 5
    if 1.1 <= z < 1.5 and np.isfinite(z_5) and z > z_5:
        return 6
    if -1.5 < z <= -1.1 and np.isfinite(z_5) and z < z_5:
        return 6
    if z >= 0:
        return 3
    return 1


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
        z = axisz(close, volume).shift(1)
        z_a = z.to_numpy()
        z5 = z.shift(5).to_numpy()
        fwd20 = (close.shift(-20) / close - 1.0).shift(1).to_numpy()
        n = len(df)
        s_arr = np.full(n, -1, dtype=int)
        for i in range(n):
            s_arr[i] = state_of(z_a[i],
                                z_a[i - 1] if i > 0 else np.nan,
                                z5[i])
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
    eigval, eigvec = np.linalg.eig(P.T)
    k = int(np.argmax(eigval.real))
    pi = np.abs(np.real(eigvec[:, k]))
    pi = pi / pi.sum()
    mods = np.sort(np.abs(eigval.real))[::-1]
    lam2 = mods[1]
    relax = 1.0 / (1.0 - lam2) if lam2 < 1 else float("inf")

    rows = []
    for s in range(K):
        fd = np.array(fd_store[s])
        f20 = np.array(f20_store[s])
        p_self = P[s, s]
        rows.append({
            "state": STATES[s],
            "self_loop": round(float(p_self), 4),
            "residence": round(float(1.0 / (1.0 - p_self)), 1)
            if p_self < 1 else "inf",
            "pi": round(float(pi[s]), 4),
            "P_first_up": round(float((fd > 0).mean()), 4)
            if len(fd) else "",
            "mean_fwd20": round(float(f20.mean()), 4)
            if len(f20) else "",
            "n": len(fd),
            "top_exits": "; ".join(
                f"{STATES[j]} {round(float(P[s, j]), 2)}"
                for j in np.argsort(-P[s])[:3] if P[s, j] > 0.01),
        })
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as fc:
        w = csv.writer(fc)
        w.writerow(["from\\to"] + STATES)
        for s in range(K):
            w.writerow([STATES[s]]
                       + [round(float(x), 4) for x in P[s]])
        w.writerow([])
        w.writerow(["state", "self_loop", "residence", "pi",
                    "P_first_up", "mean_fwd20", "n", "top_exits"])
        for r in rows:
            w.writerow([r["state"], r["self_loop"], r["residence"],
                        r["pi"], r["P_first_up"], r["mean_fwd20"],
                        r["n"], r["top_exits"]])
    md = ["# THE OWNER'S CANONICAL ZONE SYSTEM (7 states)",
          "",
          f"lambda2 = {round(float(lam2), 4)}, relaxation ~"
          f"{round(float(relax), 1)} nights.",
          "",
          "| state | self-loop | residence | pi | P_first_up |"
          " fwd20 | n | top exits |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['state']} | {r['self_loop']} "
                  f"| {r['residence']} | {r['pi']} "
                  f"| {r['P_first_up']} | {r['mean_fwd20']} "
                  f"| {r['n']} | {r['top_exits']} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    for r in rows:
        print(r)
    print("relax:", round(float(relax), 1))


if __name__ == "__main__":
    main()
