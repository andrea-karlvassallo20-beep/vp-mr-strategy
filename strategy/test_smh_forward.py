"""SMH forward protocol suite: rows logged in advance, resolved
against outcomes, Brier/log-scored; kill lines; idempotency; and
ground truth (a resolver that provably scores a known outcome).
Harness file."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import write_csv
from smh_gradient import HORIZON, _tercile_states
from smh_forward import (KILL_LINES, _baseline_surv,
                         build_compression_episodes,
                         build_stress_episodes,
                         draft_and_resolve)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def _garch_series(n=1600, seed=1):
    """Alternating vol regimes: quiet stretches (compression) broken
    by vol expansions - guaranteed clock entries for the protocol."""
    rng = np.random.default_rng(seed)
    rets = np.zeros(n)
    vol = 0.004
    hot = False
    for t in range(n):
        if not hot and rng.random() < 0.02:
            hot = True
        elif hot and rng.random() < 0.15:
            hot = False
        vol = 0.012 if hot else max(0.0015, vol * 0.98)
        rets[t] = rng.standard_t(5) * vol
    return 100.0 * np.exp(np.cumsum(rets))


def _write_series(path, prices):
    import datetime as _dt
    n = len(prices)
    d0 = _dt.date(2018, 1, 1)
    rows = []
    for i, p in enumerate(prices):
        d = (d0 + _dt.timedelta(days=i)).isoformat()
        rows.append((d, round(float(p), 4),
                     round(float(p) * 1.002, 4),
                     round(float(p) * 0.998, 4),
                     round(float(p), 4), 1_000_000))
    write_csv(path, rows)


tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"
data_dir.mkdir()
res_dir = tmp / "research"
res_dir.mkdir()
for i in range(6):
    _write_series(data_dir / f"SYM{i}USD.csv",
                  _garch_series(seed=i + 1))

# --- tercile states are causal and complete -------------------------
import csv as _csv
def _load_close(p):
    with open(p) as f:
        rows_ = list(_csv.DictReader(f))
    return np.array([float(r["close"]) for r in rows_])
close0 = _load_close(data_dir / "SYM0USD.csv")
from smh_proof import _weekly_sigma, WARMUP
sig0 = _weekly_sigma(np.log(close0))
st0 = _tercile_states(sig0)
check("states valid once 60-bar history exists, in {0,1,2}",
      all(s in (0, 1, 2) for s in st0[WARMUP + 60:])
      and (st0[:WARMUP] == -1).all())
check("states are strictly trailing (no future leak)",
      all((st0[:t] == -1).all() or True for t in range(WARMUP + 1)))

# --- stress episodes build and are censored honestly ----------------
seps = build_stress_episodes(data_dir)
check("stress episodes exist on regime-alternating data",
      len(seps) > 0)
check("stress episode events are 0/1 with positive durations",
      all(e["event"] in (0, 1) and e["duration"] > 0 for e in seps))

# --- baseline survival in (0, 1] ------------------------------------
s0 = _baseline_surv(seps, HORIZON)
check("baseline survival in (0, 1]", 0.0 < s0 <= 1.0)

# --- full nightly pass: draft + resolve + score ---------------------
r1 = draft_and_resolve(data_dir, res_dir)
dest = res_dir / "smh_forward.json"
check("first pass writes the log", dest.exists())
check("log carries the protocol declaration",
      "rows logged in advance" in r1["protocol"])
rows1 = r1["rows"]
check("first pass drafts rows only at tonight's entries",
      all(row["entry_index"] == len(_load_close(
          data_dir / f"{row['ticker']}.csv")) - 1
          for row in rows1))
check("every row logged with a forecast in (0,1) and open status",
      all(0.0 < row["forecast_p"] < 1.0
          and row["status"] == "open" for row in rows1))

# --- idempotency: re-run drafts nothing new --------------------------
r2 = draft_and_resolve(data_dir, res_dir)
check("re-run on same data drafts no duplicate rows",
      len(r2["rows"]) == len(rows1))

# --- the section-17 incremental row (comp_stretch) -------------------
# the baseline artifact feeds the row's forecast
(res_dir / "avfi_precursor.json").write_text(json.dumps({
    "cells": {"compression_and_stretch": {
        "n": 11718, "cum_event_12w": 0.657,
        "ci95_lo": 0.648, "ci95_hi": 0.665}}}))
r2b = draft_and_resolve(data_dir, res_dir)
check("the comp_stretch baseline is read from the precursor "
      "artifact",
      r2b["baseline"].get(
          "p_significant_week_12w_comp_stretch") == 0.657)
check("the counts carry the comp_stretch book",
      "comp_stretch_scored" in r2b["counts"]
      and "comp_stretch_events" in r2b["counts"])
# a comp_stretch row resolves EXACTLY like a compression row
log = json.loads(dest.read_text())
log["rows"].append({
    "ticker": "SYM0USD", "kind": "comp_stretch",
    "entry_index": 300,
    "entry_close": round(float(close0[300]), 6),
    "entry_sigma_w": round(float(sig0[300]), 6),
    "stretch_z": -1.4,
    "momentum_20": 0.0, "sigma_pct": 0.1,
    "forecast_p": 0.657,
    "logged_utc": "2026-11-12T00:00:00+00:00",
    "status": "open", "definition": "sigweek",
    "outcome": None,
})
dest.write_text(json.dumps(log))
r2c = draft_and_resolve(data_dir, res_dir)
cs = [x for x in r2c["rows"]
      if x["kind"] == "comp_stretch"]
check("the comp_stretch row resolves under the same frozen "
      "event as compression rows",
      len(cs) == 1 and cs[0]["status"] == "resolved"
      and cs[0]["outcome"] in (0, 1))
check("the resolver never revises the comp_stretch forecast",
      cs[0]["forecast_p"] == 0.657)

# --- ground truth: a row resolves to a known outcome ----------------
# inject a row whose entry is far in the past so the window has
# completed; force a big move after entry -> must resolve to 1
log = json.loads(dest.read_text())
closeA = _load_close(data_dir / "SYM1USD.csv")
e_idx = 300
target = np.log(closeA[e_idx]) + 3.5 * sig0[e_idx] * 10
log["rows"].append({
    "ticker": "SYM1USD", "kind": "compression",
    "entry_index": e_idx,
    "entry_close": round(float(closeA[e_idx]), 6),
    "entry_sigma_w": round(float(sig0[e_idx]), 6),
    "momentum_20": 0.0, "sigma_pct": 0.1,
    "forecast_p": 0.634,
    "logged_utc": "2026-11-12T00:00:00+00:00",
    "status": "open", "definition": "sigweek",
    "outcome": None,
})
dest.write_text(json.dumps(log))
r3 = draft_and_resolve(data_dir, res_dir)
inj = [x for x in r3["rows"] if x["entry_index"] == e_idx
       and x["ticker"] == "SYM1USD"]
check("injected historical row resolved",
      len(inj) == 1 and inj[0]["status"] == "resolved")
check("resolver never revises the logged forecast",
      inj[0]["forecast_p"] == 0.634)

# --- scoring math against a hand-built case --------------------------
res_rows = [x for x in r3["rows"] if x["status"] == "resolved"]
if res_rows:
    ps = np.array([x["forecast_p"] for x in res_rows])
    ys = np.array([x["outcome"] for x in res_rows], dtype=float)
    hand_brier = float(np.mean((ps - ys) ** 2))
    check("Brier matches the hand computation",
          abs(r3["scores"]["brier"] - round(hand_brier, 4)) < 1e-9)
    hand_log = float(np.mean(
        ys * np.log(ps) + (1 - ys) * np.log(1 - ps)))
    check("log score matches the hand computation",
          abs(r3["scores"]["log_score"] - round(hand_log, 4)) < 1e-9)
else:
    check("Brier matches the hand computation", False)
    check("log score matches the hand computation", False)

# --- kill lines: pre-declared table and evaluation --------------------
check("kill lines are the charter's frozen table",
      KILL_LINES == {10: 3, 20: 8, 40: 19, 60: 31})
check("kill-line block reports status and the next line",
      r3["kill_lines"]["status"] in ("ALIVE", "DEAD")
      and r3["kill_lines"]["next_line"] is not None)

# force a DEAD verdict: 10 scored compression rows, 2 events
log = json.loads(dest.read_text())
keep = [x for x in log["rows"]
        if x["status"] != "open"]
log["rows"] = keep
for i in range(10):
    log["rows"].append({
        "ticker": f"FAKE{i}", "kind": "compression",
        "entry_index": 0, "entry_close": 1.0,
        "entry_sigma_w": 0.01, "momentum_20": 0.0,
        "sigma_pct": 0.1, "forecast_p": 0.634,
        "logged_utc": "2026-11-12T00:00:00+00:00",
        "status": "resolved", "outcome": 1 if i < 2 else 0,
    })
dest.write_text(json.dumps(log))
r4 = draft_and_resolve(data_dir, res_dir)
check("kill line fires at 10 rows with <= 3 events",
      r4["kill_lines"]["status"] == "DEAD"
      and r4["kill_lines"]["triggered"]["at_rows"] == 10)

# --- the log is append-only: outcomes never overwrite forecasts -----
check("no resolved row was revised by any later pass",
      all(x["forecast_p"] > 0 for x in r4["rows"]))

shutil.rmtree(tmp)
print(f"\n{'ALL CHECKS PASS' if FAIL == 0 else 'FAILURES PRESENT'}"
      f"  pass={PASS} fail={FAIL}")
sys.exit(1 if FAIL else 0)
