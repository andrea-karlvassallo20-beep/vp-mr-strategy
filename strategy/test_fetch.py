"""Fetcher hardening test: retry-with-backoff, empty-frame failure,
MultiIndex handling, synthetic contract. Stubs yfinance; no network.
Harness file."""
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np  # noqa: F401 (fetch_synthetic path)

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def install_yfinance_stub(frames):
    """frames: list returned by successive history() calls."""
    calls = {"n": 0, "sleeps": []}
    yf = types.ModuleType("yfinance")

    class Ticker:
        def __init__(self, t): self.t = t
        def history(self, period, interval):
            calls["n"] += 1
            r = frames[min(calls["n"] - 1, len(frames) - 1)]
            if isinstance(r, Exception):
                raise r
            return r
    yf.Ticker = Ticker
    sys.modules["yfinance"] = yf

    import time as _time
    orig_sleep = _time.sleep
    _time.sleep = lambda s: calls["sleeps"].append(s)
    return calls, orig_sleep


import pandas as pd
from fetch_data import fetch_yfinance, fetch_synthetic

dates = pd.date_range("2024-01-01", periods=5, freq="D", tz="UTC")
good = pd.DataFrame({"Open": [10, 11, 12, 13, 14],
                     "High": [11, 12, 13, 14, 15],
                     "Low": [9, 10, 11, 12, 13],
                     "Close": [10.5, 11.5, 12.5, 13.5, 14.5],
                     "Volume": [100, 200, 300, 400, 500]}, index=dates)

# 1. immediate success
calls, orig = install_yfinance_stub([good])
rows = fetch_yfinance("SPY", base_wait=0)
check("successful fetch returns 5 rows", len(rows) == 5)
check("dates are ISO strings", rows[0][0] == "2024-01-01")
check("close values preserved", rows[0][4] == 10.5)

# 2. retry then success (throttle pattern)
calls, orig = install_yfinance_stub([RuntimeError("429 throttled"), good])
rows = fetch_yfinance("SPY", base_wait=0.01)
check("retry recovers after throttle", len(rows) == 5)
check("backoff sleep used", len(calls["sleeps"]) == 1)

# 3. persistent failure raises loudly
calls, orig = install_yfinance_stub([RuntimeError("429")])
try:
    fetch_yfinance("SPY", max_retries=2, base_wait=0.01)
    ok = False
except RuntimeError as e:
    ok = "after 2 attempts" in str(e)
check("persistent failure raises with attempt count", ok)

# 4. empty frame -> treated as failure, not silent header-only CSV
calls, orig = install_yfinance_stub([pd.DataFrame()])
try:
    fetch_yfinance("SPY", max_retries=1, base_wait=0.01)
    ok = False
except RuntimeError as e:
    ok = "empty frame" in str(e)
check("empty frame fails loudly", ok)

import time
time.sleep = orig

# 5. MultiIndex columns (yfinance schema shift)
multi = good.copy()
multi.columns = pd.MultiIndex.from_product([["Price"], good.columns])
calls, orig = install_yfinance_stub([multi])
rows = fetch_yfinance("SPY", base_wait=0)
check("MultiIndex columns handled", len(rows) == 5 and rows[0][4] == 10.5)
time.sleep = orig

# 6. synthetic contract unchanged
s = fetch_synthetic("SPY", 30, seed=1)
check("synthetic mode unaffected", len(s) == 30 and s[0][4] > 0)

print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
