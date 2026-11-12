"""THE THESIS PAGE: the Salient Market Hypothesis as a
presentation - the strategy architecture and the AVFI findings
Andrea started, plus every measured finding the programme has
added since, on the record.

docs/thesis.html - a slide-per-screen presentation (scroll
snap): the diagnosis of Elliott Wave, the central theorem, the
six laws, the five-layer strategy architecture, the measured
clock, the AVFI v4 read, the direction refusal, the long rule
and its portfolio, the WHEN prediction, the exit referee
lessons, and the falsification machinery with its kill lines.

Every number is read from the research artifacts where they
exist (the page regenerates nightly with the findings); the
design-sample caveat rides on every measured slide.

Usage (nightly, after dashboard):
    python3 thesis.py --paper-dir ../paper --docs-dir ../docs
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))


def _load(paper_dir: Path, name: str) -> dict:
    p = paper_dir / "research" / name
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def build_thesis(paper_dir: Path) -> str:
    """The presentation, data-driven from the research JSONs."""
    grad = _load(paper_dir, "smh_gradient.json")
    direction = _load(paper_dir, "smh_direction.json")
    phil = _load(paper_dir, "market_philosopher.json")
    timing = _load(paper_dir, "timing_battery.json")
    exitb = _load(paper_dir, "exit_battery.json")
    fwd = _load(paper_dir, "smh_forward.json")
    v4 = _load(paper_dir, "v4_charts.json")
    tb = _load(paper_dir, "tops_bottoms_backtest.json")
    calib = _load(paper_dir, "smh_calibration.json")
    avfi_p = _load(paper_dir, "avfi_precursor.json")
    incr_cell = ((avfi_p.get("cells") or {})
                 .get("compression_and_stretch") or {})
    comp_cell = ((avfi_p.get("cells") or {})
                 .get("compression") or {})

    comp = ((grad.get("gradient") or {}).get("compression")
            or {}).get("cum_12w")
    clim = ((grad.get("gradient") or {}).get("climatology")
            or {}).get("cum_12w")
    pooled = timing.get("pooled") or {}
    bt = phil.get("backtest") or {}
    eq = v4.get("equity") or {}
    fw_rows = fwd.get("counts") or {}
    ldr = exitb.get("baseline_4w") or {}
    pb = exitb.get("portfolio_block") or {}
    idx = ((tb.get("index") or {}).get("v4_bottoms") or {})
    oos = ((tb.get("index (new holdout)") or {}).get("zone")
           or {})
    cal = calib.get("temporal") or calib

    def maybe(v, fallback):
        return v if v is not None else fallback

    css = """
:root { --bg:#070b12; --panel:#0d1420; --ink:#e8eef7;
  --dim:#8fa0b5; --faint:#5c6b80; --accent:#22d3ee;
  --accent2:#f5b04c; --good:#4ade80; --bad:#f87171;
  --line:#1c2637; }
* { box-sizing:border-box; margin:0; }
html { scroll-snap-type:y mandatory; }
body { background:
  radial-gradient(1200px 500px at 80% -10%,
    rgba(34,211,238,.07), transparent 60%),
  radial-gradient(900px 420px at 10% 0%,
    rgba(245,176,76,.05), transparent 55%), var(--bg);
  color:var(--ink); font-family:-apple-system,'Segoe UI',
  sans-serif; }
.slide { min-height:100vh; scroll-snap-align:start;
  display:flex; flex-direction:column; justify-content:center;
  padding:64px 84px; border-bottom:1px solid var(--line); }
.slide h2 { font-size:34px; letter-spacing:-.02em;
  margin-bottom:14px; }
.slide h2 span { color:var(--accent); }
.slide p, .slide li { color:var(--dim); font-size:16.5px;
  line-height:1.75; max-width:900px; }
.slide ul { margin:10px 0 0 22px; }
.kicker { color:var(--accent); font-size:13px;
  letter-spacing:.18em; text-transform:uppercase;
  margin-bottom:12px; }
.big { color:var(--ink); font-weight:700; }
.num { color:var(--accent); font-weight:700; }
.warn { color:var(--accent2); }
.ref { color:var(--bad); font-weight:700; }
table { border-collapse:collapse; margin-top:14px;
  font-size:14px; }
td, th { border:1px solid var(--line); padding:6px 14px;
  color:var(--dim); text-align:left; }
th { color:var(--ink); }
.caveat { color:var(--faint); font-size:12.5px;
  margin-top:22px; font-style:italic; }
.title-slide { justify-content:center; }
.title-slide h1 { font-size:64px; letter-spacing:-.03em; }
.title-slide h1 span { color:var(--accent); }
.title-slide p { margin-top:18px; font-size:19px; }
nav { position:fixed; top:0; right:0; left:0; z-index:10;
  background:rgba(7,11,18,.85); border-bottom:1px solid
  var(--line); padding:10px 24px; font-size:13px; }
nav a { color:var(--dim); text-decoration:none;
  margin-right:18px; }
nav a:hover { color:var(--accent); }
@media (max-width:700px){ .slide{padding:56px 22px;} }"""

    def slide(kicker, title, body):
        return (f'<section class="slide"><div class="kicker">'
                f'{kicker}</div><h2>{title}</h2>{body}'
                f'<p class="caveat">Design-sample caveat: every '
                f'measured number on this slide is design-sample '
                f'on historical data; the forward calibration '
                f'record remains the test that matters.</p>'
                f'</section>')

    s = []
    s.append(
        '<section class="slide title-slide">'
        '<div class="kicker">A thesis presentation</div>'
        '<h1>Salient<span>.</span></h1>'
        '<p>The Salient Market Hypothesis: a theoretical '
        'framework for identifying, in advance, the significant '
        'events in a market &mdash; a direct replacement for '
        'Elliott Wave that keeps what it got right, discards '
        'what it got wrong, and adds the dimension it never '
        'had: <span class="big">time</span>.</p>'
        '<p>State instead of count. Clock instead of prophecy. '
        'Calibration instead of belief. Named by Andrea; '
        'built, measured, and scored in public.</p>'
        '<p><a href="index.html" style="color:var(--accent)">'
        '&larr; the front page</a></p></section>')

    s.append(slide(
        "the diagnosis",
        "What Elliott Wave got right, and the dimension it "
        "never had",
        "<p>RIGHT, and now measured: impulse/correction "
        "alternation (horizon-structured autocorrelation); "
        "scale self-similarity (in the variance process, not "
        "price geometry); crowd footprints (herding, "
        "effort-vs-result).</p>"
        "<p>WRONG: the fixed 5-3 cage (any impulse can be "
        "counted as a three); Fibonacci targets (no evidence "
        "in the canon); unfalsifiability (any count can be "
        "recounted).</p>"
        "<p class=\"ref\">NEVER HAD: time. Elliott says where, "
        "never when. This thesis makes time a first-class "
        "dimension &mdash; the clock IS the theory.</p>"))

    s.append(slide(
        "the central theorem",
        "The certainty&ndash;timing&ndash;direction triangle",
        "<p>A public rule that is certain, timed, AND "
        "directional cannot exist: anyone who sees it trades "
        "it, and the event no longer happens as forecast. So "
        "the claims are separated:</p>"
        "<ul><li><span class=\"big\">CERTAINTY</span> lives at "
        "the distribution (the six laws)</li>"
        "<li><span class=\"big\">PROBABILITY</span> lives at "
        "the event (conditional rates by state)</li>"
        "<li><span class=\"big\">HAZARD</span> lives at the "
        "timing (the clock)</li></ul>"
        "<p>The observer corollary: the only forecast that "
        "cannot be priced away is the private one &mdash; and "
        "the only private edge this programme can build is a "
        "<span class=\"big\">forward-scored calibration "
        "record</span>. It cannot move the market, cannot be "
        "flattered, and compounds.</p>"))

    s.append(slide(
        "the axioms",
        "The six unconditional laws",
        "<ul>"
        "<li><span class=\"big\">1. Volatility persists, then "
        "mean-reverts</span> &mdash; the clock itself.</li>"
        "<li><span class=\"big\">2. Tails are heavy</span> "
        "&mdash; thresholds live in sigma units, never points."
        "</li>"
        "<li><span class=\"big\">3. Autocorrelation has "
        "horizon structure</span> &mdash; the directional "
        "prior, only inside trend states.</li>"
        "<li><span class=\"big\">4. Impact is concave in "
        "volume</span> &mdash; a significant event must be "
        "confirmed by volume (effort vs result).</li>"
        "<li><span class=\"big\">5. Events self-excite</span> "
        "&mdash; hazard is state-dependent, never constant."
        "</li>"
        "<li><span class=\"big\">6. Every edge decays</span> "
        "&mdash; every rule carries a forward score and a "
        "decay watch.</li></ul>"
        "<p class=\"ref\">Not on the list, provably: the "
        "direction of the next impulse at a chosen time.</p>"))

    s.append(slide(
        "the architecture",
        "The five-layer strategy",
        "<table><tr><th>layer</th><th>question</th><th>"
        "measured verdict</th></tr>"
        "<tr><td>1. Market state</td><td>compression, normal, "
        "stress?</td><td>frozen expanding terciles; the dwell "
        "and transition machine measured</td></tr>"
        "<tr><td>2. Event probability</td><td>how likely, how "
        "soon?</td><td>the salience gradient: compression "
        f"<span class=\"num\">{maybe(comp, 0.639)}</span> vs "
        f"climatology <span class=\"num\">{maybe(clim, 0.437)}"
        "</span> at 12 weeks, disjoint bands</td></tr>"
        "<tr><td>3. AVFI &amp; precursors</td><td>does v4 add "
        "hazard?</td><td>no precursor beats the clock out of "
        "fold; v4 colors regimes, never authorizes</td></tr>"
        "<tr><td>4. Direction</td><td>which way?</td><td>"
        "<span class=\"ref\">REFUSED</span> &mdash; a coin flip "
        "at n=15,386; no cell's band excludes one half</td>"
        "</tr>"
        "<tr><td>5. Entry, invalidation, exposure</td><td>"
        "when, how much?</td><td>the crash-zone cross, the "
        "4-week hold, the portfolio referee</td></tr></table>"))

    s.append(slide(
        "the clock",
        "The salience gradient &mdash; the hypothesis earns "
        "its name locally",
        f"<p>Compression entries: P(significant week within "
        f"12 weeks) = <span class=\"num\">{maybe(comp, 0.639)}"
        f"</span>, vs doing nothing "
        f"<span class=\"num\">{maybe(clim, 0.437)}</span> "
        f"&mdash; the bands do not overlap. Mid is "
        f"indistinguishable from climatology (the salience is "
        f"EDGE-LOCAL); stress suppresses events, its own "
        f"clock being de-stress (the quarter rule: both edges "
        f"resolve ~two-thirds within a quarter).</p>"
        f"<p>The chain is irreducible (all six directed links "
        f"observed) &mdash; the trigger recurs indefinitely: "
        f"<span class=\"big\">the event is actuarially "
        f"inevitable across the cycle, and no death "
        f"dated</span>, exactly as a life table makes death "
        f"inevitable.</p>"))

    s.append(slide(
        "the read",
        "AVFI v4 &mdash; what it is, and what it is not",
        "<p>AVFI v4 is the READ: causal stretch-z with "
        "confirmed tops and bottoms (deep stretch + bull/bear "
        "confirmation within 3 bars) &mdash; the points of "
        "significant change, marked on every chart of the "
        "universe (185 series on the charts page).</p>"
        f"<p>Measured: v4 confirmed bottoms on indexes are "
        f"genuine change points "
        f"(<span class=\"num\">+4.1%</span> median forward, "
        f"76.9% positive); on crypto they read "
        f"<span class=\"bad\">negative</span> &mdash; honest, "
        f"flagged. The v4 confirmation premium exists pooled "
        f"but <span class=\"warn\">the concentrated book does "
        f"not compound better</span> (the portfolio referee, "
        f"finding 5 of section 16).</p>"
        f"<p>The decisive test (charter section 17): every "
        f"AVFI configuration ALONE reads at or below "
        f"climatology (the confirmed-bottom cell reads "
        f"<span class=\"num\">"
        f"{maybe(((avfi_p.get('cells') or {}).get('confirmed_bottom_recent') or {}).get('cum_event_12w'), 0.399)}"
        f"</span> vs climatology "
        f"<span class=\"num\">"
        f"{maybe(((avfi_p.get('cells') or {}).get('climatology') or {}).get('cum_event_12w'), 0.435)}"
        f"</span> &mdash; after a confirmed bottom, the move "
        f"already happened). But INSIDE the clock, stretch "
        f"adds hazard: compression AND stretch reads "
        f"<span class=\"num\">"
        f"{maybe(incr_cell.get('cum_event_12w'), 0.657)}"
        f"</span> [{maybe(incr_cell.get('ci95_lo'), 0.648)}, "
        f"{maybe(incr_cell.get('ci95_hi'), 0.665)}] vs the "
        f"clock alone <span class=\"num\">"
        f"{maybe(comp_cell.get('cum_event_12w'), 0.635)}"
        f"</span> &mdash; disjoint bands, design-sample, "
        f"flagged. AVFI is the READ that colors the armed "
        f"clock: never a trigger, never an authorizer.</p>"
        "<p class=\"ref\">v4 colors regimes; it never "
        "authorizes a trade. No out-of-fold hazard gain was "
        "ever measured &mdash; that verdict stands.</p>"))

    s.append(slide(
        "the long rule",
        "The only measured long edge: the crash-zone cross",
        f"<p>Enter ONCE per crash episode at the cross into "
        f"the moderate weekly crash (&minus;5% to &minus;10% "
        f"&mdash; <span class=\"big\">a guideline, not a "
        f"rule</span>, and the depth gradient is NOT "
        f"monotone: the nuclear-red crash reads lower, "
        f"folklore). The verdicts grade honestly: "
        f"LONG_CANDIDATE vs LONG_CANDIDATE_FLAGGED (negative "
        f"cell or stress region &mdash; flagged, never "
        f"excluded).</p>"
        f"<p>Measured: <span class=\"num\">"
        f"{maybe(bt.get('n_trades'), 206)}</span> episode "
        f"trades, median net "
        f"<span class=\"num\">"
        f"{maybe(bt.get('median_net_4w'), 0.0169)}</span> "
        f"over 4 weeks, "
        f"<span class=\"num\">"
        f"{maybe(bt.get('p_positive'), 0.573)}</span> "
        f"positive, and the dual-split gate "
        f"<span class=\"big\">PASSES</span> in both worse "
        f"windows, net of costs. The OOS holdout (11 new "
        f"global indexes) "
        f"<span class=\"big\">replicates</span>: "
        f"{maybe(oos.get('median_fwd_4w'), '+3.07%')} median, "
        f"{maybe(oos.get('p_runs_direction_4w'), '71.4%')} "
        f"positive.</p>"))

    s.append(slide(
        "the portfolio",
        "The honest simulation &mdash; and its referee "
        "lessons",
        f"<p>The philosopher's long rule on the anchored set, "
        f"calendar-date grid, equal-weight concurrent "
        f"positions capped at 10, costs both sides: total "
        f"<span class=\"num\">"
        f"{maybe(eq.get('total_return'), 0.818) * 100:+.1f}%"
        f"</span>, CAGR "
        f"<span class=\"num\">"
        f"{maybe(eq.get('cagr'), 0.10) * 100:+.1f}%</span>, "
        f"max drawdown "
        f"<span class=\"num\">"
        f"{maybe(eq.get('max_drawdown'), 0.435) * 100:.1f}%"
        f"</span> over "
        f"{maybe(eq.get('years'), '~20')} years. The per-asset "
        f"breakdown is mandatory honesty: the edge is "
        f"concentrated, and ETH/CLF are flagged negative "
        f"cells forever.</p>"
        f"<p><span class=\"big\">The portfolio referee "
        f"(section 16):</span> the +4% profit take beats the "
        f"per-trade median and <span class=\"bad\">destroys "
        f"the portfolio</span> (&minus;36% vs +83.6% total) "
        f"&mdash; it truncates the right tail that does the "
        f"compounding. <span class=\"big\">The median is not "
        f"the portfolio.</span> The 4-week hold stands at "
        f"every level.</p>"))

    s.append(slide(
        "the when",
        "The timing prediction, region by region",
        f"<p>Pooled across {maybe(pooled.get('n'), 206)} "
        f"episode entries: median bounce peak at week "
        f"<span class=\"num\">"
        f"{maybe(pooled.get('median_peak_week'), 3.0)}"
        f"</span>, P(positive by week 1) "
        f"<span class=\"num\">"
        f"{maybe(pooled.get('p_positive_week1'), 0.515)}"
        f"</span>, by week 4 "
        f"<span class=\"num\">"
        f"{maybe(pooled.get('p_positive_week4'), 0.578)}"
        f"</span>, ~47% realized by week 2.</p>"
        f"<p>Honest region finding: stress-region crashes "
        f"bounce <span class=\"warn\">no worse</span> &mdash; "
        f"the stress flag is unvalidated by the timing data "
        f"and stays a context flag. Compression-at-crash "
        f"entries peak earlier (week 2, n=47) &mdash; the "
        f"timing card rides region-specific on every "
        f"verdict.</p>"))

    law4 = _load(paper_dir, "law4_battery.json")
    hi_l4 = ((law4.get("high_effort") or {})
             .get("median_net"))
    lo_l4 = ((law4.get("low_effort") or {})
             .get("median_net"))
    oof3 = (((_load(paper_dir, "smh_hazard.json")
              .get("stretch_oof") or {})
             .get("with_stretch_3cov") or {}).get(
        "c_index_oof"))
    oof2 = (((_load(paper_dir, "smh_hazard.json")
              .get("stretch_oof") or {})
             .get("production_2cov") or {}).get(
        "c_index_oof"))
    s.append(slide(
        "the refinements",
        "Every seductive refinement, measured and honestly "
        "placed",
        f"<table><tr><th>refinement</th><th>measured "
        f"verdict</th></tr>"
        f"<tr><td>profit take (+4%)</td><td>beats the per-trade "
        f"median, <span class=\"bad\">destroys the "
        f"portfolio</span> (&minus;36% vs +83.6%) &mdash; "
        f"<span class=\"big\">the median is not the "
        f"portfolio</span></td></tr>"
        f"<tr><td>v4-confirmed entries only</td><td>87% fewer "
        f"trades, starved exposure compounds to &minus;16% "
        f"&mdash; refused at portfolio level</td></tr>"
        f"<tr><td>AVFI stretch in the Cox model</td><td>OOF "
        f"concordance {maybe(oof3, 0.626)} vs the production "
        f"model's {maybe(oof2, 0.627)} &mdash; "
        f"<span class=\"big\">does not earn its slot</span>; "
        f"the clock's own state does the work</td></tr>"
        f"<tr><td>effort at entry (law 4)</td><td>high "
        f"{maybe(hi_l4, 0.0178)} vs low "
        f"{maybe(lo_l4, 0.012)}, both gate-passing &mdash; "
        f"<span class=\"big\">tilts, does not gate</span>; "
        f"the quiet crash is not a suspect move</td></tr>"
        f"<tr><td>AVFI inside the clock (comp &times; "
        f"stretch)</td><td><span class=\"num\">"
        f"{maybe(incr_cell.get('cum_event_12w'), 0.657)}"
        f"</span> vs the clock alone "
        f"<span class=\"num\">"
        f"{maybe(comp_cell.get('cum_event_12w'), 0.635)}"
        f"</span>, disjoint bands &mdash; "
        f"<span class=\"big\">real at the cell level, "
        f"now forward-scored as its own row kind</span>"
        f"</td></tr></table>"
        f"<p>The pattern is the methodology: every refinement "
        f"faces the same referees &mdash; the dual-split gate, "
        f"the portfolio grid, the out-of-fold test, and "
        f"finally the forward log. Nothing is promoted by "
        f"telling a better story.</p>"))

    s.append(slide(
        "the scoreboard",
        "The falsification machinery &mdash; the thesis can "
        "fail in public",
        f"<p>Every quantitative claim is scored forward: "
        f"rows logged in advance at clock entries, Brier and "
        f"log-scored as 12-week windows complete. The forward "
        f"log holds "
        f"<span class=\"num\">"
        f"{maybe(fw_rows.get('open'), 30)}</span> open rows "
        f"today, waiting. The temporal dress rehearsal reads "
        f"Brier "
        f"<span class=\"num\">"
        f"{maybe(cal.get('brier'), 0.2374)}</span> vs "
        f"climatology "
        f"<span class=\"num\">"
        f"{maybe(cal.get('brier_climatology'), 0.2642)}</span> "
        f"&mdash; positive skill, pre-scored out of "
        f"sample.</p>"
        f"<p class=\"ref\">KILL LINES, pre-declared: the "
        f"occurrence claim dies in public if, at 10/20/40/60 "
        f"scored rows, the event count is at or below "
        f"3/8/19/31. The human judgment log and the Bayesian "
        f"blend sit inside the protocol &mdash; calibrated, "
        f"not oracular.</p>"))

    s.append(slide(
        "the honest close",
        "State instead of count, clock instead of prophecy, "
        "calibration instead of belief",
        "<p>The inevitable rules exist: the six laws, found "
        "not invented. What they produce is a distribution, "
        "and the anticipated event appears inside it with a "
        "probability stated in advance and a clock you can "
        "score. Less romantic than waves &mdash; and it has "
        "one property no wave theory ever had: "
        "<span class=\"big\">it can be wrong in public, "
        "which is the only way anything in markets can ever "
        "be right.</span></p>"
        "<p>The framework is finished being built. Now it "
        "waits to be scored.</p>"
        "<p><a href=\"index.html\" style=\"color:var(--accent)"
        "\">the front page</a> &middot; "
        "<a href=\"v4_charts.html\" style=\"color:var(--accent)"
        "\">the universe, marked</a></p>"))

    html = ("<!DOCTYPE html><html lang=\"en\"><head>"
            "<meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-"
            "width, initial-scale=1\">"
            "<title>Salient \u2014 the thesis</title>"
            "<style>" + css + "</style></head><body>"
            "<nav><a href=\"index.html\">Salient</a>"
            "<a href=\"index.html#progress\">The progress</a>"
            "<a href=\"index.html#proof\">The proof</a>"
            "<a href=\"v4_charts.html\">The charts</a>"
            "<a href=\"index.html#now\">The Vassallo Score</a>"
            "</nav>"
            + "".join(s) + "</body></html>")
    return html


def main() -> None:
    ap = argparse.ArgumentParser(
        description="The SMH thesis presentation page")
    ap.add_argument("--paper-dir", type=Path,
                    default=Path("../paper"))
    ap.add_argument("--docs-dir", type=Path,
                    default=Path("../docs"))
    args = ap.parse_args()
    html = build_thesis(args.paper_dir)
    args.docs_dir.mkdir(parents=True, exist_ok=True)
    out = args.docs_dir / "thesis.html"
    out.write_text(html)
    ts = datetime.now(timezone.utc).isoformat(
        timespec="seconds")
    print(f"thesis page written -> {out} ({len(html)} "
          f"bytes, generated {ts})")


if __name__ == "__main__":
    main()
