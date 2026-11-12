"""THE MARKET PHILOSOPHER: SMH as a long strategy, AVFI v4 as the
read - when to take a long, decided from measured rules only.

The philosopher answers one question at every decision close: is
there a LONG here that the MEASURED record justifies? Every rule
is pre-declared and traceable to a measured verdict in this
programme - and the refusals are as explicit as the entries:

  THE CRASH ZONE IS A GUIDELINE, NOT A RULE: it raises a
  candidate; it does not fire a trade. The context layers
  modulate every candidate - the asset's own measured record
  (negative cells are flagged, not excluded: excluding on
  in-sample performance is blind-following in reverse), the SMH
  region, the AVFI v4 read - and the judgment log is where the
  human decides, on the record, before the outcome. The
  guideline never overrides; it proposes.

  THE ENTRY CONDITION (measured directional edge, the only one
  in the programme): an ANCHORED asset (a major that cannot go
  to zero and mean-reverts after panics) whose trailing weekly
  return lands in the measured best-buy zone, -5% to -10% -
  the crash-depth battery's T2: +2.0%/+2.2% median forward 4
  weeks, 60-62% positive, n = 709. Deeper crashes do NOT
  qualify (the nuclear-red reads lower: the gradient is not
  monotone).

  THE CLOCK (SMH, Layer 1-2): the region and the Vassallo
  Score are recorded with every verdict - but the central
  theorem REFUSES direction, so compression alone never creates
  a long. The clock says WHEN an event is likely, never WHICH
  WAY; the philosopher says so in the verdict.

  THE READ (AVFI v4, Layer 3): deep stretch (z <= -2) with
  bull-side confirmation (divergence or climax within 3 bars)
  colors the verdict as a precursor note - per the precursor
  battery it does NOT beat the clock out of fold, so it
  annotates, never authorizes.

  THE EXPOSURE (Layer 5, from measured distributions): hold
  the measured forward window (4 weeks); the expected-value
  card is the crash bucket's own measured stats; the stop
  comes from the exposure layer, not the clock (T1's verdict).

  THE BACKTEST (honesty devices): entries at the crash-zone
  cross on anchored assets, 4-week hold, 5 bps costs both
  sides, dual-split gate (the edge must hold at BOTH the
  last-40% and last-50% windows, scored at the worse one),
  dead-coin filter, winsorized returns.

Usage (nightly, after trade_inevitables):
    python3 market_philosopher.py --data-dir ../paper/research/data \\
        --research-dir ../paper/research
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from smh_gradient import _tercile_states
from smh_proof import WARMUP, _series, _weekly_sigma
from tops_bottoms import (detect_climaxes, detect_divergences,
                          rsi)
from v4_study import CONFIRM_LB, LOOKBACK, causal_z

WEEK = 5
ANCHORED = ("BTCUSD", "ETHUSD", "GCF", "CLF", "HGF", "SIF",
            "GSPC", "DJI", "IXIC", "RUT")
ZONE_LO = -0.10       # the measured best-buy zone
ZONE_HI = -0.05
HOLD_WEEKS = 4        # the measured forward window
COST_BPS = 5.0
WINSOR = 0.05
SPLITS = (0.6, 0.5)


def _avfi_v4_read(c, v, t) -> dict:
    """The AVFI v4 read at bar t: deep stretch + bull-side
    confirmation, strictly causal."""
    z = causal_z(c)
    if t >= len(z) or z[t] > -2.0:
        return {"stretch_z": (round(float(z[t]), 2)
                             if t < len(z) else None),
                "bull_confirmed": False}
    h = np.maximum(c, c * 1.0)     # OHLC proxy from closes
    l = np.minimum(c, c * 1.0)
    bull, _ = detect_divergences(c, rsi(c))
    cb, _ = detect_climaxes(h, l, c, v)
    conf = set(bull.tolist()) | set(cb.tolist())
    ok = any(i in conf
             for i in range(max(0, t - CONFIRM_LB), t + 1))
    return {"stretch_z": round(float(z[t]), 2),
            "bull_confirmed": bool(ok)}


def _weekly_return(logc, t):
    if t < WEEK:
        return 0.0
    return float(logc[t] - logc[t - WEEK])


def philosopher_verdicts(data_dir: Path,
                          research_dir: Path = None) -> list:
    """Per-market verdicts at the latest close: LONG_CANDIDATE,
    LONG_CANDIDATE_FLAGGED (the guideline raised it, context
    weighs against - judgment invited), ARMED (clock only,
    direction refused), or REFUSED - each with its measured
    reasons, on the record."""
    # the per-asset measured record, when the artifact exists:
    # negative cells are FLAGGED, never excluded (excluding on
    # in-sample performance is blind-following in reverse)
    record = {}
    timing_card = {}
    region_cards = {}
    if research_dir is not None:
        rp = research_dir / "v4_charts.json"
        if rp.exists():
            try:
                v4 = json.loads(rp.read_text())
                record = v4.get("equity", {}).get(
                    "per_asset", {})
            except Exception:
                record = {}
        tp = research_dir / "timing_battery.json"
        if tp.exists():
            try:
                tb = json.loads(tp.read_text())
                timing_card = tb.get("candidate_timing_card", {})
                region_cards = tb.get("by_region", {})
            except Exception:
                timing_card = {}
    out = []
    for name, c, v in _series(data_dir):
        logc = np.log(c)
        sig = _weekly_sigma(logc)
        states = _tercile_states(sig)
        t = len(c) - 1
        if t <= WARMUP:
            continue
        region = ("compression" if states[t] == 0
                  else "mid" if states[t] == 1 else "stress"
                  if states[t] == 2 else "unassigned")
        wr = _weekly_return(logc, t)
        prev = _weekly_return(logc, t - 1)
        read = _avfi_v4_read(c, v, t)
        anchored = name in ANCHORED
        # the guideline fires on the CROSS into the zone (one
        # proposal per episode), not on every in-zone bar
        crossed = (ZONE_LO <= wr < ZONE_HI
                   and not ZONE_LO <= prev < ZONE_HI)
        if anchored and crossed:
            flags = []
            rec = record.get(name, {})
            if rec.get("positive") is False:
                flags.append(
                    f"negative measured cell "
                    f"({rec.get('n_trades')} trades, median "
                    f"{rec.get('median_fwd')}) - flagged, not "
                    f"excluded")
            if region == "stress":
                flags.append("stress region")
            verdict = ("LONG_CANDIDATE_FLAGGED" if flags
                       else "LONG_CANDIDATE")
            reason = ("the GUIDELINE raised a candidate "
                      "(anchored asset crossing into the "
                      "measured best-buy zone, -5..-10% "
                      "weekly; +1.7% median net 4w at one "
                      "entry per episode, gate-passing)"
                      + ("; context weighs against: "
                         + "; ".join(flags)
                         + " - judgment invited, on the record"
                         if flags else ""))
        elif anchored and ZONE_LO <= wr < ZONE_HI:
            verdict = "ARMED"
            reason = ("in the crash zone but not at the cross "
                      "(the episode already proposed; the "
                      "guideline does not re-fire)")
        elif region == "compression":
            verdict = "ARMED"
            reason = ("the clock is armed (compression) but the "
                      "central theorem REFUSES direction: a "
                      "long needs the measured crash-zone edge, "
                      "not the clock")
        else:
            verdict = "REFUSED"
            reason = (f"region {region}, weekly {wr:.3f}: no "
                      "measured long edge")
        # the timing card rides REGION-SPECIFIC when the
        # region has its own measured card (compression-at-
        # crash peaks at week 2 vs pooled week 3), pooled
        # otherwise; the region n is carried so the small
        # sample stays visible (doctrine rule 5)
        rc = region_cards.get(region)
        card = {
            "median_peak_week":
                (rc or timing_card).get("median_peak_week"),
            "p_positive_week1":
                (rc or timing_card).get("p_positive_week1"),
            "p_positive_week4":
                (rc or timing_card).get("p_positive_week4"),
            "source": ("region" if rc else "pooled"),
            "region_n": (rc or {}).get("n"),
        }
        out.append({
            "ticker": name,
            "verdict": verdict,
            "region": region,
            "weekly_return": round(wr, 4),
            "avfi_v4": read,
            "timing_card": card,
            "reason": reason,
        })
    order = {"LONG_CANDIDATE": 0,
             "LONG_CANDIDATE_FLAGGED": 1,
             "ARMED": 2, "REFUSED": 3}
    out.sort(key=lambda x: (order[x["verdict"]], x["ticker"]))
    return out


def backtest_long_rule(data_dir: Path) -> dict:
    """The philosopher's long rule, measured honestly: enter at
    the crash-zone cross on anchored assets, hold the measured
    4-week window, costs both sides, dual-split gate."""
    trades = []
    for name, c, v in _series(data_dir):
        if name not in ANCHORED:
            continue
        logc = np.log(c)
        last_entry = -10 ** 9
        for t in range(WARMUP, len(c) - WEEK * HOLD_WEEKS):
            wr = _weekly_return(logc, t)
            prev = _weekly_return(logc, t - 1)
            # ONE entry per crash episode: the CROSS into the
            # zone (the trailing week was outside it), and no
            # re-entry while the measured hold runs
            if (ZONE_LO <= wr < ZONE_HI
                    and not ZONE_LO <= prev < ZONE_HI
                    and t >= last_entry + WEEK * HOLD_WEEKS):
                last_entry = t
                fwd = float(logc[t + WEEK * HOLD_WEEKS]
                            - logc[t])
                trades.append({
                    "ticker": name, "t": t,
                    "fwd": fwd,
                    "net": fwd - 2 * COST_BPS / 1e4,
                })
    if not trades:
        return {"verdict": "INSUFFICIENT_TRADES"}
    rets = np.array([tr["net"] for tr in trades])
    w = np.clip(rets, *np.quantile(
        rets, [WINSOR, 1 - WINSOR]))
    med = float(np.median(w))
    hit = float(np.mean(rets > 0))

    def window_stats(lo):
        seg = rets[int(len(rets) * lo):]
        if len(seg) < 10:
            return None
        ws = np.clip(seg, *np.quantile(
            seg, [WINSOR, 1 - WINSOR]))
        return {"n": len(seg),
                "median_net": round(float(np.median(ws)), 4),
                "p_positive": round(float(np.mean(seg > 0)), 3)}

    wins = [window_stats(lo) for lo in SPLITS]
    gate = (all(x is not None
                and x["median_net"] > 0 for x in wins))
    return {
        "n_trades": len(trades),
        "median_net_4w": round(med, 4),
        "p_positive": round(hit, 3),
        "dual_split_windows": wins,
        "dual_split_gate": bool(gate),
        "verdict": ("PASSES the dual-split gate: the crash-zone "
                    "long edge holds in BOTH worse windows, net "
                    "of costs" if gate else
                    "FAILS the dual-split gate: the edge does "
                    "not survive both worse windows - refused"),
    }


def run_philosopher(data_dir: Path,
                    research_dir: Path = None) -> dict:
    verdicts = philosopher_verdicts(data_dir, research_dir)
    backtest = backtest_long_rule(data_dir)
    counts = {}
    for x in verdicts:
        counts[x["verdict"]] = counts.get(x["verdict"], 0) + 1
    return {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "philosophy": "the crash zone is a GUIDELINE, not a "
            "rule: it raises candidates, it does not fire "
            "trades. The context layers modulate every candidate "
            "(the asset's own measured record - negative cells "
            "flagged, never excluded - the SMH region, the AVFI "
            "v4 read), and the judgment log is where the human "
            "decides, on the record, before the outcome. The "
            "SMH clock arms but never authorizes (direction "
            "refused by the central theorem); AVFI v4 colors "
            "but never authorizes (no out-of-fold hazard gain); "
            "exposure from measured distributions - one entry "
            "per episode, 4-week hold, stop from the exposure "
            "layer, not the clock",
        "counts": counts,
        "verdicts": verdicts,
        "backtest": backtest,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="The market philosopher (longs from "
                    "measured rules)")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    args = ap.parse_args()
    r = run_philosopher(args.data_dir, args.research_dir)
    dest = args.research_dir / "market_philosopher.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(r, indent=2))
    bt = r["backtest"]
    print(f"market philosopher -> {dest} "
          f"(verdicts {r['counts']}, backtest "
          f"{bt.get('n_trades')} trades, median net "
          f"{bt.get('median_net_4w')}, gate "
          f"{bt.get('dual_split_gate')})")


if __name__ == "__main__":
    main()
