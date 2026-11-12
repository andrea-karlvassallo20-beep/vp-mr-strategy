"""THE SMH CONDITIONAL DIRECTION BATTERY (charter v3, sections 3,
8, 11): law 3's directional prior, measured where it is claimed to
live.

The central theorem refuses direction as a CLAIM, and the pooled
split agrees (p(up) = 0.505 at n = 15,386 - a coin flip). But
section 8 PREDICTS one directional quantity: "direction asymmetry
(drift) conditional on trend states (law 3)" - momentum at medium
horizons, valid only inside trend states and only at the right
horizons. This battery measures exactly that, on the first
significant week after every compression entry:

  cells (pre-committed, all strictly causal at entry):
    overall            P(up) - the pooled coin-flip reference
    momentum_20        sign of the trailing 20-bar log return
    momentum_60        sign of the trailing 60-bar (12-week) log
                       return - the charter's own seductive cell
                       (compression after a down 12-week move)
    depth              compression depth tercile at entry
    mom x depth        the joint cell law 3 actually claims

Every cell carries a Wilson 95% band and a flag: cells with n < 100
are seductive by doctrine rule 5 and say so in their own verdict.
The battery's verdict is pre-declared: law 3 earns its place only if
a cell's Wilson band excludes one half AND the cell is not flagged;
otherwise direction stays refused, and the refusal is now measured
per cell rather than asserted.

Usage (nightly, after smh_precursor):
    python3 smh_direction.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
import math
from datetime import datetime, timezone
from statistics import NormalDist
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import HORIZON, _tercile_states
from smh_proof import EVENT_SIG, WARMUP, _series, _weekly_sigma

MIN_CELL = 100          # below this a cell is seductive, flagged


def _wilson(n_up: int, n: int, z: float = 1.96) -> dict:
    if n == 0:
        return {"p": None, "lo": None, "hi": None}
    p = n_up / n
    den = 1 + z * z / n
    ctr = (p + z * z / (2 * n)) / den
    hw = z * math.sqrt(
        p * (1 - p) / n + z * z / (4 * n * n)) / den
    return {"p": round(p, 3),
            "lo": round(max(0.0, ctr - hw), 3),
            "hi": round(min(1.0, ctr + hw), 3)}


def _cell(n_up, n, label, z_adj: float = 1.96) -> dict:
    w = _wilson(n_up, n)
    wa = _wilson(n_up, n, z=z_adj)
    seductive = n < MIN_CELL
    # pre-declared multiple-comparison guard: with many cells, a
    # 95% band excludes one half by pure chance about once per
    # twenty cells - so the exclusion verdict uses a Bonferroni-
    # adjusted band (alpha / n_cells), while the 95% band stays
    # the display number
    excludes_half = (wa["p"] is not None
                     and (wa["hi"] < 0.5 or wa["lo"] > 0.5))
    return {
        "cell": label,
        "n": n,
        "n_up": n_up,
        "p_up": w["p"],
        "wilson_95": [w["lo"], w["hi"]],
        "wilson_adjusted": [wa["lo"], wa["hi"]],
        "seductive_flag": bool(seductive),
        "band_excludes_half": bool(excludes_half and not seductive),
        "verdict": ("LAW-3 CELL: the Bonferroni-adjusted band "
                    "excludes one half on unflagged data"
                    if excludes_half and not seductive else
                    "seductive cell - untrusted until "
                    "forward-scored (doctrine rule 5)" if seductive
                    else "no direction: the adjusted band spans "
                    "one half"),
    }


def run_direction(data_dir: Path) -> dict:
    n_up = n = 0
    up_m20_pos = up_m20_neg = n_m20_pos = n_m20_neg = 0
    up_m60_pos = up_m60_neg = n_m60_pos = n_m60_neg = 0
    depth = {"shallow": [0, 0], "mid": [0, 0], "deep": [0, 0]}
    joint = {}          # (m20 sign, depth tercile) -> [up, n]
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
                if not hit:
                    continue
                up = int(logc[k] > logc[k - 5])
                n += 1
                n_up += up
                m20 = logc[t] - logc[max(0, t - 20)]
                m60 = logc[t] - logc[max(0, t - 60)]
                hist = sig[WARMUP:t + 1][sig[WARMUP:t + 1] > 0]
                sig_pct = (float(np.mean(hist <= sig[t]))
                           if len(hist) else 0.5)
                dter = ("shallow" if sig_pct >= 2 / 3
                        else "deep" if sig_pct <= 1 / 3 else "mid")
                if m20 > 0:
                    n_m20_pos += 1
                    up_m20_pos += up
                else:
                    n_m20_neg += 1
                    up_m20_neg += up
                if m60 > 0:
                    n_m60_pos += 1
                    up_m60_pos += up
                else:
                    n_m60_neg += 1
                    up_m60_neg += up
                depth[dter][0] += up
                depth[dter][1] += 1
                key = ("up" if m20 > 0 else "down", dter)
                j = joint.setdefault(key, [0, 0])
                j[0] += up
                j[1] += 1

    raw_cells = [("overall (pooled reference)", n_up, n),
                 ("momentum_20 > 0", up_m20_pos, n_m20_pos),
                 ("momentum_20 < 0", up_m20_neg, n_m20_neg),
                 ("momentum_60 > 0", up_m60_pos, n_m60_pos),
                 ("momentum_60 < 0 (the charter's seductive cell)",
                  up_m60_neg, n_m60_neg)]
    for dter in ("shallow", "mid", "deep"):
        raw_cells.append((f"depth: {dter}", depth[dter][0],
                          depth[dter][1]))
    for key in sorted(joint):
        u, nn = joint[key]
        raw_cells.append((f"joint: momentum_20 {key[0]}, "
                          f"depth {key[1]}", u, nn))
    m = max(1, len(raw_cells))
    z_adj = NormalDist().inv_cdf(1 - 0.05 / (2 * m))
    cells = [_cell(u, nn, lab, z_adj=z_adj)
             for lab, u, nn in raw_cells]

    law3_cells = [c_ for c_ in cells if c_["band_excludes_half"]]
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "n_first_events": n,
        "cells": cells,
        "verdict": {
            "law3_earned_cells": [c_["cell"] for c_ in law3_cells],
            "direction_claim": ("REFUSED - no unflagged cell's band "
                                "excludes one half" if not law3_cells
                                else "MEASURED in the listed cells "
                                "only - direction remains refused "
                                "as a forward claim until those "
                                "cells are forward-scored"),
            "statement": ("law 3 earns its place only where an "
                          "unflagged cell's Bonferroni-adjusted "
                          "band excludes one half (the "
                          "multiple-comparison guard is "
                          f"z = {round(z_adj, 2)} at {m} cells); "
                          "every small cell stays flagged forever "
                          "(doctrine rule 5)"),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH conditional direction battery")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_direction(args.data_dir)
    dest = args.research_dir / "smh_direction.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    v = r.get("verdict", {})
    print(f"smh direction -> {dest} "
          f"({r.get('n_first_events')} first events, "
          f"law-3 cells: {v.get('law3_earned_cells')})")


if __name__ == "__main__":
    main()
