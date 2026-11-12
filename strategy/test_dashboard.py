"""Dashboard test: generation from a synthetic session + empty-state
grace. Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_synthetic, write_csv
from papertrading_runner import PaperTradingRunner
from dashboard import (build_html, build_site, drawdown_svg,
                       price_charts_html, race_svg, _avfi_chart_svg,
                       _charts_html,
                       _avfi_html, _avfi_pine_html)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
for i, t in enumerate(["SPY", "QQQ"]):
    write_csv(data_dir / f"{t.lower()}.csv", fetch_synthetic(t, 300, seed=7 + i))
runner = PaperTradingRunner(data_dir, tmp / "state", universe=["SPY", "QQQ"])
runner.run_session()

html = build_html(tmp / "state" and tmp)
check("html generated", len(html) > 4000)
check("metric cards present", html.count('class="card"') == 8)
check("equity curve SVG rendered", "<svg" in html and "polyline" in html)
check("verification matrix present", "Cross-engine parity" in html)
check("autonomous loop section present", "edge-seeker" in html)
check("no unescaped script injection", "<script" not in html)

_fr_seed = tmp / "research"
_fr_seed.mkdir(parents=True, exist_ok=True)
(_fr_seed / "v4_chart_frags.json").write_text(json.dumps({
    "status": "OK", "n_charts": 1, "per_class": {"index": 1},
    "charts": ['<div class="chart"><svg></svg></div>']}))
(_fr_seed / "v4_charts.json").write_text(json.dumps({"equity": {
    "status": "OK", "n_trades": 3, "years": 1.0,
    "total_return": 0.1, "cagr": 0.1, "max_drawdown": 0.05,
    "concurrent_cap": 10,
    "equity_curve_monthly": [1.0, 1.05, 1.1]}}))
site = build_site(tmp)
check("salient site generated", len(site) > 6000)
check("front page faces forward: hypothesis, proof, work, score",
      all(k in site for k in ("The hypothesis",
                             "certainty-timing-direction triangle",
                             "The new work", "The Vassallo Score")))
check("front page carries no past sections",
      all(k not in site for k in ("Build log", "Session journal",
                                  "falsification archive",
                                  "aria-label=\"equity curve\"")))
check("charts section on the main page embeds the universe "
      "and the equity curve",
      'id="charts"' in site and 'class="cgrid"' in site
      and 'class="chart"' in site and 'class="eqsvg"' in site)
check("charts section is graceful when no fragments exist",
      _charts_html(tmp / "nonexistent") == "")
_fr_tmp = Path(tempfile.mkdtemp())
_fr_res = _fr_tmp / "research"
_fr_res.mkdir(parents=True)
(_fr_res / "v4_chart_frags.json").write_text(json.dumps({
    "status": "OK", "n_charts": 1, "per_class": {"index": 1},
    "charts": ['<div class="chart"><svg></svg></div>']}))
(_fr_res / "v4_charts.json").write_text(json.dumps({"equity": {
    "status": "OK", "n_trades": 3, "years": 1.0,
    "total_return": 0.1, "cagr": 0.1, "max_drawdown": 0.05,
    "concurrent_cap": 10,
    "equity_curve_monthly": [1.0, 1.05, 1.1]}}))
_ch = _charts_html(_fr_tmp)
check("charts section renders from the artifacts",
      'id="charts"' in _ch and "<svg" in _ch
      and "class=\"eqsvg\"" in _ch and "3 trades" in _ch)
shutil.rmtree(_fr_tmp)
check("drawdown chart in site", drawdown_svg(tmp).startswith("<svg"))
check("drawdown empty-state graceful",
      "no session data yet" in drawdown_svg(tmp / "nonexistent"))
prices = price_charts_html(tmp)
check("per-instrument price charts", prices.count("<svg") == 2
      and "SPY" in prices and "QQQ" in prices)
check("trade entry markers rendered",
      "long entry" in prices or "short entry" in prices)
check("race chart without challenger is graceful",
      "not yet" in race_svg(tmp))
(tmp / "challenger").mkdir(exist_ok=True)
shutil.copy(tmp / "state" / "session_state.json",
            tmp / "challenger" / "session_state.json")
race = race_svg(tmp)
check("race chart overlays two curves",
      race.count("<polyline") == 2 and "Challenger" in race)

avfi_chart = {"ticker": "SPY", "dates": ["d1", "d2", "d3", "d4"],
              "close": [10.0, 10.5, 10.2, 10.8], "sp_z": [0.0, -0.5,
              -1.5, -0.2], "trigger": -1.0, "throttle": 0.5,
              "entries": [[1, 1], [3, -1]], "throttled_bars": 1}
svg_avfi = _avfi_chart_svg(avfi_chart)
check("AVFI chart renders price + spread panels",
      svg_avfi.count("<polyline") == 2 and "spread z" in svg_avfi)
check("AVFI chart marks trade entries with tooltips",
      "long entry d2" in svg_avfi and "short entry d4" in svg_avfi)
check("AVFI chart shades throttled zones",
      svg_avfi.count("<rect") >= 1)
check("AVFI section graceful without data",
      "appears here after" in _avfi_html(tmp / "nonexistent"))

empty = build_html(tmp / "nonexistent")
check("empty state graceful", "no session data yet" in empty)

# AVFI v4 Pine: rewritten from scratch on the evidence — must
# render as the primary source, with the falsified components
# explicitly documented as absent
pine_html = _avfi_pine_html()
check("AVFI v4 Pine renders as the primary source",
      "AVFI v4" in pine_html and "Stretch + Confirmation" in pine_html
      and "//@version=5" in pine_html)
check("v4 documents its evidence decisions",
      "falsified" in pine_html and "tripling filter" in pine_html
      and "AVFI v3.2" in pine_html)
_v4_code = "\n".join(
    ln for ln in (Path(__file__).parent / "avfi_v4.pine").read_text()
    .splitlines() if not ln.strip().startswith("//"))
check("v4 excludes the falsified components in code",
      all(k not in _v4_code for k in ("percentile", "percentrank",
                                      "quantile")))

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
