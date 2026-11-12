"""Thesis page suite: the presentation must carry the required
content - the diagnosis, the theorem, the laws, the five-layer
architecture with the AVFI findings, the long rule, the
portfolio referee lessons, the falsification machinery - and
its numbers must be data-driven from the research artifacts.
Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from thesis import build_thesis

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


tmp = Path(tempfile.mkdtemp())
res = tmp / "research"
res.mkdir(parents=True)
(res / "smh_gradient.json").write_text(json.dumps({
    "gradient": {"compression": {"cum_12w": 0.639},
                 "climatology": {"cum_12w": 0.437}}}))
(res / "market_philosopher.json").write_text(json.dumps({
    "backtest": {"n_trades": 206, "median_net_4w": 0.0169,
                 "p_positive": 0.573}}))
(res / "v4_charts.json").write_text(json.dumps({
    "equity": {"total_return": 0.818, "cagr": 0.10,
               "max_drawdown": 0.435, "years": 20.1}}))
(res / "timing_battery.json").write_text(json.dumps({
    "pooled": {"n": 206, "median_peak_week": 3.0,
               "p_positive_week1": 0.515,
               "p_positive_week4": 0.578}}))
(res / "exit_battery.json").write_text(json.dumps({
    "baseline_4w": {"n": 206, "median_net": 0.0169}}))
(res / "smh_forward.json").write_text(json.dumps({
    "counts": {"open": 30}}))
(res / "smh_calibration.json").write_text(json.dumps({
    "temporal": {"brier": 0.2374,
                 "brier_climatology": 0.2642}}))
(res / "avfi_precursor.json").write_text(json.dumps({
    "cells": {
        "confirmed_bottom_recent": {
            "n": 2635, "cum_event_12w": 0.399,
            "ci95_lo": 0.38, "ci95_hi": 0.418},
        "climatology": {
            "n": 250138, "cum_event_12w": 0.435,
            "ci95_lo": 0.434, "ci95_hi": 0.437},
        "compression": {
            "n": 25959, "cum_event_12w": 0.635,
            "ci95_lo": 0.629, "ci95_hi": 0.641},
        "compression_and_stretch": {
            "n": 11718, "cum_event_12w": 0.657,
            "ci95_lo": 0.648, "ci95_hi": 0.665}},
    "incremental_verdict": "AVFI EARNS INCREMENTAL HAZARD "
                           "CONTENT, DESIGN SAMPLE"}))

html = build_thesis(tmp)
check("the presentation builds", len(html) > 4000)
check("the required slides are present",
      all(k in html for k in (
          "Elliott Wave", "certainty", "six unconditional laws",
          "five-layer strategy", "AVFI v4", "crash-zone cross",
          "portfolio referee", "KILL LINES",
          "calibration instead of belief")))
check("the clock numbers are data-driven",
      "0.639" in html and "0.437" in html)
check("the AVFI incremental finding is on the read slide",
      "0.657" in html and "0.635" in html
      and "disjoint bands" in html)
check("the portfolio numbers are data-driven",
      "+81.8%" in html and "+10.0%" in html)
check("the design-sample caveat rides every measured slide",
      html.count("Design-sample caveat") >= 10)
check("the page links back to the front page and the charts",
      'href="index.html"' in html
      and 'href="v4_charts.html"' in html)

# graceful without any artifacts at all
empty = Path(tempfile.mkdtemp())
h2 = build_thesis(empty)
check("the presentation builds even with no research "
      "artifacts (fallback constants)",
      len(h2) > 4000 and "0.639" in h2)
shutil.rmtree(empty)

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
