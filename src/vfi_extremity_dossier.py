"""The VFI-extremity dossier - the owner's own method, encoded and
measured against the program's current best criteria.

Directive (Andrea, 2026-11-18, in-session): "me marking extremities
on VFI is the best I could do, you are here to find even better
and the right way to do it, but you gotta find it." Owner-
authorized measured descriptive work, third measured session of
the parallel regime.

THE OWNER'S METHOD, ENCODED (declared before the run):
VFI (volume flow index, Fedenko-style, daily, all windows causal):
  - volume ratio v_t = volume_t / mean(volume_{t-1..t-23}) - 1,
    clipped to [0, 3];
  - direction gate: +v_t if close_t >= 1.01*close_{t-1};
    -v_t if close_t <= 0.99*close_{t-1}; else 0;
  - VFI_t = running sum of gated v from series start;
  - extremity read: vfi_z_t = (VFI_t - mean(VFI, prior 252d)) /
    std(VFI, prior 252d), clipped at |z| <= 10;
  - EXTREMITY_LOW  = vfi_z percentile within trailing 756d <= 10;
  - EXTREMITY_HIGH = vfi_z percentile >= 90.

PRE-DECLARED QUESTIONS:
  Q1 (closeness): pooled rank AUC of vfi_z against "a >=4-sigma
    move occurs within K days", K in {5, 20, 60}; context row: the
    closeness dossier's rvol_pct AUCs (0.323/0.376/0.411);
  Q2 (chip): P(first >=4-sigma move within 60d is UP) at
    EXTREMITY_LOW, EXTREMITY_HIGH, the base state (rvol_pct <= 33
    AND range_pos <= 0.15), intersections with the base state,
    and all nights; plus P(move within 5d) for the same groups;
  Q3 (additivity): AUC of vfi_z restricted to base-state nights
    (does the owner's read add ranking-inside-base?).
Descriptive only: no threshold chosen, nothing armed, W2 confirm
split mandatory. No kill line moves; nothing trades live.

Output: paper/research/clue_scan/vfi_extremity_dossier.csv and
paper/research/clue_scan/vfi_extremity_dossier.md
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

CLUE = Path("paper/research/clue_scan")
DATA = Path("paper/research/data")
OUT_CSV = CLUE / "vfi_extremity_dossier.csv"
OUT_MD = CLUE / "vfi_extremity_dossier.md"

SIGMA_WIN = 20
PCT_WIN = 756
RANGE_WIN = 252
VOL_MA = 23
Z_WIN = 252
MOVE_SIGMA = 4.0
HORIZON_KS = (5, 20, 60)
MOVE_HORIZON = 60
GATE = 0.01
NEED = PCT_WIN + SIGMA_WIN + 5


def series_panel(close, volume):
    close = pd.Series(close, dtype=float).reset_index(drop=True)
    volume = pd.Series(volume, dtype=float).reset_index(drop=True)
    n = len(close)
    if n < NEED:
        return None

    ret = close.pct_change()
    sigma = ret.rolling(SIGMA_WIN).std().shift(1)
    move = (ret.abs() >= MOVE_SIGMA * sigma) & sigma.notna()
    move_up = (ret >= MOVE_SIGMA * sigma) & sigma.notna()

    rvol = ret.rolling(SIGMA_WIN).std()
    rvol_pct = rvol.rolling(PCT_WIN).rank(pct=True) * 100.0
    hi = close.rolling(RANGE_WIN).max()
    lo = close.rolling(RANGE_WIN).min()
    rng = (hi - lo).replace(0, np.nan)
    range_pos = (close - lo) / rng

    vol_ma = volume.shift(1).rolling(VOL_MA).mean()
    v = (volume / vol_ma.replace(0, np.nan) - 1.0).clip(0, 3.0)
    up_g = (close >= close.shift(1) * (1 + GATE)).astype(float)
    dn_g = (close <= close.shift(1) * (1 - GATE)).astype(float)
    vfi = (v * (up_g - dn_g)).cumsum()
    vfi_z = ((vfi - vfi.rolling(Z_WIN).mean())
             / vfi.rolling(Z_WIN).std().replace(0, np.nan)).clip(-10, 10)
    vfi_pct = vfi_z.rolling(PCT_WIN).rank(pct=True) * 100.0

    state = {
        "vfi_z": vfi_z,
        "ext_low": (vfi_pct <= 10.0).astype(float),
        "ext_high": (vfi_pct >= 90.0).astype(float),
        "base": (((rvol_pct <= 33.0) & (range_pos <= 0.15)
                  & range_pos.notna()).astype(float)),
    }
    state = {k: s.shift(1) for k, s in state.items()}
    valid = (close > 0.01).astype(float).shift(1).fillna(0.0)

    # event: a >=4-sigma move within K days after the evaluation night
    event_k = {}
    for k in HORIZON_KS:
        rev = move.iloc[::-1]
        rev_max = rev.rolling(k, min_periods=1).max()
        event_k[k] = rev_max.iloc[::-1].shift(-1).astype(float)

    # first-move direction within MOVE_HORIZON
    first_dir = np.full(n, np.nan)
    ret_a = ret.to_numpy()
    move_a = move.to_numpy()
    up_a = move_up.to_numpy()
    for i in range(n - MOVE_HORIZON - 1):
        for j in range(i + 1, min(i + MOVE_HORIZON, n - 1) + 1):
            if move_a[j]:
                first_dir[i] = 1.0 if up_a[j] else -1.0
                break
    return state, event_k, pd.Series(first_dir), valid


def auc(pos, neg):
    pos = pos[~np.isnan(pos)]
    neg = neg[~np.isnan(neg)]
    if len(pos) < 50 or len(neg) < 50:
        return "na", len(pos), len(neg)
    allv = np.concatenate([pos, neg])
    order = np.argsort(allv, kind="mergesort")
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(allv) + 1)
    sorted_vals = allv[order]
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and sorted_vals[j + 1] == sorted_vals[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    rp = ranks[:len(pos)].sum()
    return (round((rp - len(pos) * (len(pos) + 1) / 2.0)
                  / (len(pos) * len(neg)), 4), len(pos), len(neg))


def main():
    acc = {"vfi_z": {k: {"pos": [], "neg": []} for k in HORIZON_KS},
           "vfi_z_base": {k: {"pos": [], "neg": []} for k in HORIZON_KS}}
    groups = ("ext_low", "ext_high", "base", "all",
              "ext_low_x_base", "ext_high_x_base", "base_not_extlow")
    first_acc = {g: [] for g in groups}
    move5_acc = {g: [] for g in groups}

    for data_file in sorted(DATA.glob("*.csv")):
        try:
            df = pd.read_csv(data_file)
        except Exception:
            continue
        if ("close" not in df.columns or "volume" not in df.columns
                or len(df) < NEED):
            continue
        out = series_panel(df["close"].to_numpy(),
                           df["volume"].to_numpy())
        if out is None:
            continue
        state, event_k, first_dir, valid = out
        vc = valid.to_numpy(dtype=float)
        vz = state["vfi_z"].to_numpy(dtype=float)
        el = state["ext_low"].to_numpy(dtype=float)
        eh = state["ext_high"].to_numpy(dtype=float)
        bs = state["base"].to_numpy(dtype=float)
        ok = (vc > 0) & ~np.isnan(vz)
        e5 = event_k[5].to_numpy(dtype=float)
        fd = first_dir.to_numpy(dtype=float)
        grp = {
            "ext_low": (el > 0) & ok & ~np.isnan(e5),
            "ext_high": (eh > 0) & ok & ~np.isnan(e5),
            "base": (bs > 0) & ok & ~np.isnan(e5),
            "all": np.ones_like(ok) & ok & ~np.isnan(e5),
            "ext_low_x_base": ((el > 0) & (bs > 0) & ok
                               & ~np.isnan(e5)),
            "ext_high_x_base": ((eh > 0) & (bs > 0) & ok
                                & ~np.isnan(e5)),
            "base_not_extlow": ((bs > 0) & (el == 0) & ok
                                & ~np.isnan(e5)),
        }
        for g in groups:
            m = grp[g]
            if not m.any():
                continue
            f = fd[m]
            first_acc[g].extend(f[~np.isnan(f)].tolist())
            move5_acc[g].extend(e5[m].tolist())

        okz = (vc > 0) & ~np.isnan(vz)
        for k in HORIZON_KS:
            ek = event_k[k].to_numpy(dtype=float)
            m = okz & ~np.isnan(ek)
            if not m.any():
                continue
            pos = vz[m][ek[m] > 0]
            neg = vz[m][ek[m] == 0]
            acc["vfi_z"][k]["pos"].append(pos)
            acc["vfi_z"][k]["neg"].append(neg)
            mb = m & (bs > 0)
            if mb.any():
                pos = vz[mb][ek[mb] > 0]
                neg = vz[mb][ek[mb] == 0]
                acc["vfi_z_base"][k]["pos"].append(pos)
                acc["vfi_z_base"][k]["neg"].append(neg)

    rows = []
    for k in HORIZON_KS:
        pos = np.concatenate(acc["vfi_z"][k]["pos"]) if acc["vfi_z"][k]["pos"] else []
        neg = np.concatenate(acc["vfi_z"][k]["neg"]) if acc["vfi_z"][k]["neg"] else []
        a, np_, nn_ = auc(np.array(pos), np.array(neg))
        rows.append({"row": "auc_vfi_z", "K": k, "value": a,
                     "n_event": np_, "n_nonevent": nn_})
        pos = np.concatenate(acc["vfi_z_base"][k]["pos"]) if acc["vfi_z_base"][k]["pos"] else []
        neg = np.concatenate(acc["vfi_z_base"][k]["neg"]) if acc["vfi_z_base"][k]["neg"] else []
        a, np_, nn_ = auc(np.array(pos), np.array(neg))
        rows.append({"row": "auc_vfi_z_on_base", "K": k, "value": a,
                     "n_event": np_, "n_nonevent": nn_})
    for g in groups:
        fd = np.array(first_acc[g])
        m5 = np.array(move5_acc[g])
        rows.append({"row": f"P_first_up[{g}]", "K": 60,
                     "value": (round(float((fd > 0).mean()), 4)
                               if len(fd) else ""),
                     "n_event": len(fd), "n_nonevent": ""})
        rows.append({"row": f"P_move5[{g}]", "K": 5,
                     "value": (round(float((m5 > 0).mean()), 4)
                               if len(m5) else ""),
                     "n_event": len(m5), "n_nonevent": ""})

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["row", "K", "value",
                                          "n_event", "n_nonevent"])
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
