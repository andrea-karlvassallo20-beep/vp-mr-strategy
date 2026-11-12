"""Lessons suite: synthesis extracted live from research artifacts,
missing-data grace, structure of every lesson. Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lessons import build_lessons

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


# empty paper dir: must not crash, must report honestly
tmp = Path(tempfile.mkdtemp())
empty = build_lessons(tmp)
check("empty paper dir synthesizes without crashing",
      isinstance(empty, dict) and empty["lessons"]
      and empty["inferences"]["universe_series"] == 0)
check("empty paper dir still carries the lessons",
      len(empty["lessons"]) >= 8)

# populated paper dir with the real artifact shapes
paper = tmp / "paper"
res = paper / "research"
res.mkdir(parents=True)
(paper / "state.json").write_text(json.dumps(
    {"invocations": 3}))
(res / "cross_asset.json").write_text(json.dumps([
    {"ticker": "KMD-USD", "asset_class": "crypto",
     "mean_reverting": True, "mr_t_stat": -7.18,
     "half_life_bars": 12.3},
    {"ticker": "BTC-USD", "asset_class": "crypto",
     "mean_reverting": False, "mr_t_stat": -0.9,
     "half_life_bars": 695.0},
    {"ticker": "GCF", "asset_class": "commodity",
     "mean_reverting": False, "mr_t_stat": -1.2,
     "half_life_bars": 400.0},
]))
(res / "tops_bottoms_extended.json").write_text(json.dumps({
    "rows": [{"ticker": "KMD-USD", "topology_buckets": {
        "2": {"long_fwd": 0.01}, "3": {"long_fwd": 0.03}}},
        {"ticker": "BTC-USD", "topology_buckets": {
        "2": {"long_fwd": 0.02}, "3": {"long_fwd": 0.01}}}],
}))
(res / "state_space_study_extended.json").write_text(json.dumps({
    "aggregate": {"bottom_region": {"n": 322, "fwd": 0.0127},
                  "series_beats": 17, "series_with_both": 40},
}))
(res / "state_space_axis.json").write_text(json.dumps({
    "vol_high": {"beats": 20, "series": 50},
}))
(res / "stretch_depth.json").write_text(json.dumps({
    "own_scale_deeper_pays": True, "falling_knife": False}))
(res / "avfi_iterations.json").write_text(json.dumps([
    {"date": "2026-11-12", "deflated_sharpe":
     {"dsr": 0.78, "n_trials": 84}}]))

r = build_lessons(paper)
inf = r["inferences"]
check("universe and MR counts extracted live",
      inf["universe_series"] == 3 and inf["mr_passing_all"] == 1
      and inf["mr_passing_crypto"] == 1)
check("strongest MR leader carries its stats",
      inf["strongest_mr"][0]["ticker"] == "KMD-USD"
      and inf["strongest_mr"][0]["t_stat"] == -7.18)
check("crypto confluence verdict counted from buckets",
      inf["crypto_confluence_holds"] == "1/2")
check("region pooled n and beats extracted",
      inf["region_pooled_n"] == 322 and inf["region_beats"] == "17 / 40")
check("axis beats, depth verdicts and DSR extracted",
      inf["vol_axis_beats"] == "20 / 50"
      and inf["deeper_pays"] is True
      and inf["falling_knife"] is False
      and inf["dsr"] == 0.78 and inf["dsr_trials"] == 84)
check("forward sessions read from live state",
      inf["forward_sessions"] == 3)

check("every lesson has lesson, forced_by and remedy",
      all(set(l) == {"lesson", "forced_by", "remedy"}
          for l in r["lessons"]))
check("lessons text injects the live numbers",
      any("322" in l["lesson"] for l in r["lessons"])
      and any("17 / 40" in l["lesson"] for l in r["lessons"]))
check("generated timestamp present",
      "T" in r["generated_utc"])

shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
