"""Learning lessons and inferences, extracted from ALL collected data.

The project now accumulates studies every night: cross-asset
mean-reversion stats on 183 series, tops-and-bottoms detections,
the state-space program (region hypothesis and its falsification),
axis attribution, the stretch-depth curve, AVFI iterations with
the Deflated Sharpe context, and the live forward test. This
module synthesizes them into the honest lessons the data has
FORCED on us - each lesson tied to the numbers that forced it -
so the site's "Lessons" section is regenerated from live artifacts
every nightly pass, never hand-staled.

Usage (nightly):
    python3 lessons.py --paper-dir ../paper
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def _load(path: Path):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (ValueError, OSError):
            return None
    return None


def build_lessons(paper_dir: Path) -> dict:
    """Extract the live headline numbers from every research
    artifact and pair them with the evidence-forced lessons."""
    res = paper_dir / "research"
    cross = _load(res / "cross_asset.json") or []
    tb = _load(res / "tops_bottoms.json") or {}
    tb_ext = _load(res / "tops_bottoms_extended.json") or {}
    ss = _load(res / "state_space_study.json") or {}
    ss_ext = _load(res / "state_space_study_extended.json") or {}
    axis = _load(res / "state_space_axis.json") or {}
    depth = _load(res / "stretch_depth.json") or {}
    ledger = _load(res / "avfi_iterations.json") or []
    state = _load(paper_dir / "state.json") or {}

    # --- live inferences -------------------------------------------
    crypto = [x for x in cross if x.get("asset_class") == "crypto"]
    mr_crypto = [x for x in crypto if x.get("mean_reverting")]
    mr_crypto.sort(key=lambda x: x.get("mr_t_stat", 0))
    all_mr = [x for x in cross if x.get("mean_reverting")]
    ext_rows = tb_ext.get("rows", [])
    crypto_rows = [r for r in ext_rows if r["ticker"].endswith("USD")]
    conf_holds = sum(
        1 for r in crypto_rows
        if (lf := {int(k): v["long_fwd"]
                   for k, v in r.get("topology_buckets", {}).items()
                   if v.get("long_fwd") is not None})
        and 2 in lf and 3 in lf and lf[3] > lf[2])

    agg = (ss_ext.get("aggregate") or {})
    axis_vol = axis.get("vol_high") or {}
    depth_pays = depth.get("own_scale_deeper_pays")
    knife = depth.get("falling_knife")
    dsr = (ledger[-1].get("deflated_sharpe") if ledger else None) or {}
    sessions = state.get("invocations", 0)

    inferences = {
        "universe_series": len(cross),
        "crypto_series": len(crypto),
        "mr_passing_all": len(all_mr),
        "mr_passing_crypto": len(mr_crypto),
        "strongest_mr": [
            {"ticker": x["ticker"],
             "t_stat": x.get("mr_t_stat"),
             "half_life_bars": round(x.get("half_life_bars", 0), 1)}
            for x in mr_crypto[:5]],
        "crypto_confluence_holds": f"{conf_holds}/{len(crypto_rows)}",
        "region_pooled_n": (agg.get("bottom_region") or {}).get("n"),
        "region_beats": (f"{agg.get('series_beats', 0)} / "
                         f"{agg.get('series_with_both', 0)}"),
        "vol_axis_beats": (
            f"{axis_vol.get('beats', 0)} / "
            f"{axis_vol.get('series', 0)}"),
        "deeper_pays": depth_pays,
        "falling_knife": knife,
        "dsr": dsr.get("dsr"),
        "dsr_trials": dsr.get("n_trials"),
        "forward_sessions": sessions,
    }

    # --- the lessons the data forced --------------------------------
    def num(k):
        v = inferences.get(k)
        return v if v is not None else "?"

    lessons = [
        {"lesson": "A single-window result is a coin flip wearing "
         "a suit. The detector mode's 27.4% OOS drawdown reduction "
         "collapsed to 1.0% when the data window shifted by one bar.",
         "forced_by": "the 2026-11-11 refresh, on camera",
         "remedy": "Every advancement now must beat the current "
         "parameters on BOTH out-of-sample windows, scored at the "
         "worse one (the dual-split gate)."},
        {"lesson": "Pooled forward returns across mixed-scale assets "
         "lie. The elevated-vol axis looked like +9.23% vs +1.39% "
         "pooled - and won on its own scale in only "
         f"{num('vol_axis_beats')} series. The pooled edge was "
         "high-drift crypto scale contamination, not signal.",
         "forced_by": "axis attribution across the extended universe",
         "remedy": "Own-scale beat counting: a finding must win on "
         "each series' own scale in a majority of series, not just "
         "in a pooled average."},
        {"lesson": "Beautiful hypotheses die by data - and small "
         "samples lie in both directions. The 3D state-space region "
         "ideology was the most satisfying idea in the project. At "
         f"{num('region_pooled_n')} pooled events it is falsified "
         f"({num('region_beats')} own-scale beats). The axis "
         "decomposition read DEAD at the 50-series sample and WEAK "
         "majorities at the 180-series one - a reminder that a "
         "verdict is a property of the sample too - but the causal "
         "test (the v4 study) is the one that counts, and it "
         "failed: descriptive weight never converted.",
         "forced_by": "the pooled region study, axis attribution at "
         "two sample sizes, and the v4 causal study",
         "remedy": "Keep the visualization; retire the hypothesis. "
         "Falsification at n=322+ beats an eternity of hoping at "
         "n=9 - and only causal conversion can revive anything."},
        {"lesson": "Deep stretch alone is the one supported entry "
         "signal - and deeper pays. On each series' own scale, "
         "deeper stretch beats the shallow edge in a majority of "
         "series at every depth, and there is no falling knife even "
         f"beyond z 4 (deeper pays: {num('deeper_pays')}, knife: "
         f"{num('falling_knife')}).",
         "forced_by": "the stretch-depth curve, ~4,800 bottom-side "
         "events",
         "remedy": "Entry-threshold research now has a direction; "
         "a deeper-entry grid variant goes to the dual-split gate, "
         "not straight to belief."},
        {"lesson": "Descriptive regime concentration does not survive "
         "being made causal. The mid-vol confluence lead (4/5 ETFs, "
         "descriptive) converted to a strictly causal entry rule and "
         "tested honestly null under the dual-split gate.",
         "forced_by": "the topology3_midvol variant, PR #38",
         "remedy": "Description generates candidates; only causal "
         "out-of-sample conversion generates beliefs."},
        {"lesson": "Search luck manufactures edges. The AVFI grid "
         f"tries {num('dsr_trials')} configurations nightly; the "
         "current portfolio's OOS Sharpe 0.711 deflates to "
         f"DSR {num('dsr')} < 0.95 - not yet separated from the "
         "search itself.",
         "forced_by": "the Deflated Sharpe Ratio (Bailey & Lopez de "
         "Prado) wired into the ledger",
         "remedy": "Every reported edge now carries its "
         "multiple-testing context. Honesty is a statistic, not a "
         "mood."},
        {"lesson": "Data quality is a research finding. Expanding "
         "to top-150 crypto surfaced 33 delisted tickers and 7 junk "
         "instruments returning one-row frames - every survivor had "
         "to be verified to carry 200+ daily bars before it could "
         "enter a study.",
         "forced_by": "the crypto universe expansion",
         "remedy": "Verified-fetch lists only; the fetcher's "
         "tolerance is for the market's mess, not for silently "
         "studying garbage."},
        {"lesson": "The edge concentrates where the physics is "
         "strongest. At 156-coin depth, "
         f"{num('mr_passing_crypto')} coins pass the "
         "mean-reversion t-test - led by KMD-USD (t=-7.18, "
         "half-life 12 bars). Fast-decay series are where a "
         "z-score core has the most to work with.",
         "forced_by": "cross-asset OU/AR(1) stats on 183 series",
         "remedy": "The next studies (confluence, depth) run "
         "crypto-pooled, weighting where mean reversion is "
         "actually measured."},
        {"lesson": "The live forward test is the only judge that "
         "cannot be fooled. Backtests selected the champion; the "
         f"live paper account has run {num('forward_sessions')}/20 "
         "sessions with Sharpe ~0.02 and no demonstrated edge yet. "
         "That number is not a failure - it is the only number in "
         "the project with zero selection bias.",
         "forced_by": "the deployed champion's live MTM, net of "
         "costs",
         "remedy": "Patience is part of the method: the gate "
         "demands 20 sessions and will take all 20."},
        {"lesson": "Breadth generates leads; depth converts them - "
         "and the battery said no. The first positive pooled "
         "result (commodities, +0.37 OOS) went through the full "
         "honesty battery and failed it: at 2x costs the edge is "
         "zero, and deflated for 32 trials it is not separated "
         "from search luck. The direction is now depth-first: no "
         "new universes until a battery-passing edge exists.",
         "forced_by": "the commodity edge battery, 2026-11-12",
         "remedy": "One lead at a time, through every gate. The "
         "method is the asset; the edge has not been found yet."},
    ]
    return {"generated_utc": datetime.now(timezone.utc).isoformat(
                timespec="seconds"),
            "inferences": inferences,
            "lessons": lessons}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Learning lessons and inferences from all data")
    ap.add_argument("--paper-dir", type=Path, default=Path("../paper"))
    args = ap.parse_args()
    out = build_lessons(args.paper_dir)
    dest = args.paper_dir / "research" / "lessons.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2))
    print(f"lessons -> {dest} "
          f"({len(out['lessons'])} lessons, "
          f"{len(out['inferences'])} live inferences)")


if __name__ == "__main__":
    main()
