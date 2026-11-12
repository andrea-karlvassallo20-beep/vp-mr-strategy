"""THE SMH SALIENCE GRADIENT AND EVENT ANATOMY (charter v3,
sections 6, 7, 14.8 - the fifth and sixth measured ticks).

Two instruments, one frozen episode definition:

THE SALIENCE GRADIENT: all three clock regions measured with the
same ENTRY-ANCHORED first-event clock - an entry is a cross into
the region; the event is a >= 2.5 sigma_w move from the entry close
within 12 weeks (60 daily bars), with NO region censoring (the
armed clock keeps running after the region read changes, exactly as
the charter's anatomy requires). The counterfactual is climatology:
the same clock started from EVERY eligible bar. Kaplan-Meier with
Greenwood 95% bands at the 12-week edge. The charter's claim to
score here: the gradient is monotone (compression > mid >
climatology > stress) and the compression band is disjoint from
climatology - salience is EDGE-LOCAL.

THE EVENT ANATOMY: for every compression-entry first event, the
dissection - in-spell vs escape-week vs post-escape arrival, the
act-dissolved-at-spell-end capture rate, the law-4 volume
signature (event-bar volume over its trailing baseline vs all
bars), the overshoot multiple (|move| / 2.5 sigma_w), and the
up/down volume asymmetry with its flag.

Everything strictly causal: entries, covariates and baselines use
only trailing information.

Usage (nightly, after smh_forward):
    python3 smh_gradient.py --data-dir ../paper/research/data \
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_proof import EVENT_SIG, WARMUP, _series, _weekly_sigma

HORIZON = 60          # 12 weeks of daily bars (charter section 14)
WEEK = 5              # bars per completed week
VOL_BASE = 20          # trailing bars for the volume baseline


def _tercile_states(sig: np.ndarray) -> np.ndarray:
    """Expanding-tercile clock states: 0 compression, 1 mid,
    2 high - strictly causal, identical to the hazard battery."""
    n = len(sig)
    states = np.full(n, -1, dtype=int)
    for t in range(WARMUP, n):
        hist = sig[WARMUP:t + 1][sig[WARMUP:t + 1] > 0]
        if len(hist) < 60 or sig[t] <= 0:
            continue
        q1, q2 = np.quantile(hist, [1 / 3, 2 / 3])
        states[t] = 0 if sig[t] <= q1 else (
            1 if sig[t] <= q2 else 2)
    return states


def first_significant_week(logc: np.ndarray, sig: np.ndarray,
                            t: int) -> int:
    """THE CHARTER'S FROZEN EVENT (section 14): the first
    completed week ending in (t, t+HORIZON] whose 1-week log
    return |r1| >= 2.5 * sigma_w AT ENTRY. Returns the offset of
    the week-ending bar, 0 if the window completed quietly, or a
    negative number = censored at the data edge with duration
    -offset. Strictly causal: the threshold is frozen at the
    decision close."""
    thr = EVENT_SIG * sig[t]
    if thr <= 0:
        return 0
    end = min(t + HORIZON, len(logc) - 1)
    if end <= t:
        return 0
    k = t + WEEK
    while k <= end:
        if abs(logc[k] - logc[k - WEEK]) >= thr:
            return k - t
        k += WEEK
    return -1 if end >= t + HORIZON else -(end - t)


def _first_event_offsets(logc: np.ndarray, sig: np.ndarray,
                          entries: np.ndarray) -> np.ndarray:
    """Entry-anchored first-significant-week offset for each entry
    index (see first_significant_week for the encoding)."""
    out = np.full(len(entries), 0, dtype=int)
    for j, t in enumerate(entries):
        out[j] = first_significant_week(logc, sig, int(t))
    return out


def _entries_by_region(states: np.ndarray) -> dict:
    """Crosses into each region: the decision-close triggers."""
    out = {0: [], 1: [], 2: []}
    for t in range(WARMUP + 1, len(states)):
        if states[t] >= 0 and states[t - 1] >= 0 \
                and states[t] != states[t - 1]:
            out[states[t]].append(t)
    return out


def km_greenwood(durations: np.ndarray, events: np.ndarray,
                 horizon: int) -> dict:
    """Kaplan-Meier to `horizon` with Greenwood variance and the
    complementary log-log 95% band. Durations are capped at the
    horizon; censoring handled properly."""
    surv = 1.0
    var_g = 0.0
    lo = hi = 1.0
    n_events = int(events.sum())
    for t in range(1, horizon + 1):
        d = int(((durations == t) & (events == 1)).sum())
        c = int(((durations == t) & (events == 0)).sum())
        at_risk = int((durations >= t).sum())
        if at_risk <= 0:
            break
        if d > 0:
            surv *= (1.0 - d / at_risk)
            if at_risk > d:
                var_g += d / (at_risk * (at_risk - d))
        # log-log band at this time
        if surv > 0 and surv < 1 and var_g > 0:
            z = 1.96
            cll = np.log(-np.log(surv))
            se = np.sqrt(var_g) / abs(np.log(surv))
            lo = np.exp(-np.exp(cll + z * se))
            hi = np.exp(-np.exp(cll - z * se))
        elif surv >= 1.0:
            lo, hi = 1.0, 1.0
        else:
            lo, hi = 0.0, 1.0
    return {
        "n": int(len(durations)),
        "n_events": n_events,
        "cum_event_12w": round(float(1.0 - surv), 3),
        "ci95_lo": round(float(1.0 - hi), 3),
        "ci95_hi": round(float(1.0 - lo), 3),
    }


def _clock_for_region(data_dir: Path, region: int) -> dict:
    """The entry-anchored first-event clock for one region."""
    durs, evs = [], []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        entries = np.array(_entries_by_region(states)[region],
                           dtype=int)
        if not len(entries):
            continue
        offs = _first_event_offsets(logc, sig, entries)
        for o in offs:
            if o > 0:
                durs.append(int(o))
                evs.append(1)
            elif o == -1:
                durs.append(int(HORIZON))
                evs.append(0)
            elif o < 0:
                durs.append(int(-o))   # censored at the data edge
                evs.append(0)
            # o == 0: no window at all - excluded
    return km_greenwood(np.array(durs), np.array(evs), HORIZON)


def climatology_clock(data_dir: Path) -> dict:
    """The counterfactual: the same clock started from EVERY
    eligible bar (sig_w defined, past warmup)."""
    durs, evs = [], []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        ok = np.where(sig > 0)[0]
        ok = ok[ok >= WARMUP]
        entries = ok[ok + HORIZON < len(logc)]
        offs = _first_event_offsets(logc, sig, entries)
        for o in offs:
            if o > 0:
                durs.append(int(o))
                evs.append(1)
            elif o == -1:
                durs.append(int(HORIZON))
                evs.append(0)
    return km_greenwood(np.array(durs), np.array(evs), HORIZON)


def event_anatomy(data_dir: Path) -> dict:
    """The dissection of compression-entry first events: arrival
    class, act capture at spell end, the law-4 volume signature,
    the overshoot, and the up/down asymmetry (flagged)."""
    classes = {"in_spell": 0, "escape_week": 0, "post_escape": 0}
    acts = spells = 0
    ev_ratios, all_ratios = [], []
    overshoots = []
    up_ratios, down_ratios = [], []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        base = np.zeros(len(v))
        for t in range(VOL_BASE, len(v)):
            base[t] = v[t - VOL_BASE:t].mean()
        # all-bar volume ratio distribution (the null grain)
        for t in range(WARMUP, len(v)):
            if base[t] > 0:
                all_ratios.append(v[t] / base[t])
        entries = np.array(_entries_by_region(states)[0],
                           dtype=int)
        for t in entries:
            thr = EVENT_SIG * sig[t]
            if thr <= 0:
                continue
            end = min(t + HORIZON, len(logc) - 1)
            # spell end: first bar out of compression
            e = end
            for k in range(t + 1, end + 1):
                if states[k] != 0:
                    e = k
                    break
            k = t + 1
            ev = None
            while k <= end:
                if abs(logc[k] - logc[t]) >= thr:
                    ev = k
                    break
                k += 1
            spells += 1
            if ev is not None:
                if ev < e:
                    classes["in_spell"] += 1
                elif ev == e:
                    classes["escape_week"] += 1
                else:
                    classes["post_escape"] += 1
                acts += 1
                overshoots.append(
                    abs(logc[ev] - logc[t]) / thr)
                if base[ev] > 0:
                    r = v[ev] / base[ev]
                    ev_ratios.append(r)
                    if logc[ev] > logc[t]:
                        up_ratios.append(r)
                    else:
                        down_ratios.append(r)

    def med(x):
        return round(float(np.median(x)), 3) if len(x) else None

    n_ev = sum(classes.values())
    return {
        "n_compression_entries": int(spells),
        "n_first_events": int(n_ev),
        "arrival_split": classes,
        "act_capture_at_spell_end": (round(acts / spells, 3)
                                     if spells else None),
        "volume": {
            "median_event_ratio": med(ev_ratios),
            "median_all_bars_ratio": med(all_ratios),
            "pct_event_above_baseline": (round(float(np.mean(
                np.array(ev_ratios) > 1.0)), 3)
                if ev_ratios else None),
            "pct_all_above_baseline": (round(float(np.mean(
                np.array(all_ratios) > 1.0)), 3)
                if all_ratios else None),
            "n_thin_flagged_events": int(sum(
                1 for r in ev_ratios if r < 0.5)),
        },
        "overshoot_median": med(overshoots),
        "up_down_volume_asymmetry": {
            "n_up": len(up_ratios),
            "n_down": len(down_ratios),
            "median_up_ratio": med(up_ratios),
            "median_down_ratio": med(down_ratios),
            "flag": "seductive cell - untrusted until "
                     "forward-scored (doctrine rule 5)",
        },
    }


def run_gradient(data_dir: Path) -> dict:
    comp = _clock_for_region(data_dir, 0)
    mid = _clock_for_region(data_dir, 1)
    stress = _clock_for_region(data_dir, 2)
    clim = climatology_clock(data_dir)
    anatomy = event_anatomy(data_dir)
    # the gradient verdict, pre-committed: monotone point estimates
    # AND the compression band disjoint from climatology
    pts = [comp["cum_event_12w"], mid["cum_event_12w"],
           clim["cum_event_12w"], stress["cum_event_12w"]]
    monotone = pts[0] > pts[1] > pts[2] > pts[3]
    disjoint = (comp["ci95_lo"] > clim["ci95_hi"])
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "gradient": {
            "compression": comp,
            "mid": mid,
            "climatology": clim,
            "stress_events": stress,
        },
        "verdict": {
            "monotone_point_estimates": bool(monotone),
            "compression_disjoint_from_climatology": bool(disjoint),
            "salience_edge_local": bool(monotone and disjoint),
            "point_estimates": pts,
        },
        "event_anatomy": anatomy,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SMH salience gradient + event anatomy")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_gradient(args.data_dir)
    dest = args.research_dir / "smh_gradient.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    v = r["verdict"]
    print(f"smh gradient -> {dest} "
          f"(gradient {v['point_estimates']}, "
          f"monotone {v['monotone_point_estimates']}, "
          f"disjoint {v['compression_disjoint_from_climatology']}, "
          f"edge-local salience {v['salience_edge_local']})")


if __name__ == "__main__":
    main()
