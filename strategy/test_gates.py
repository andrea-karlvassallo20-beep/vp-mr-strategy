"""Gate verification suite for VP-MR-ETF-D1-001. Run: python3 test_gates.py"""
import math
import numpy as np
from vp_mr_strategy import (
    StrategyParameters, OrderState, OrderTicket,
    VolatilityParityMeanReversionStrategy,
)

PASS, FAIL = 0, 0

def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")

def make_params():
    return StrategyParameters(min_history_bars=40, lookback_zscore=30,
                             vol_est_lookback=20, atr_lookback=10)

def feed(strat, s, ts, c, factor=0.002):
    strat.on_bar_close(s, ts, c, c*(1+factor), c*(1-factor), c, 1e6)
    return c

def gen(n, seed, start=450.0, sd=1.0):
    rng = np.random.default_rng(seed)
    return start + np.cumsum(rng.normal(0, sd, n))


# --- G4: order state machine -------------------------------------------------
print("GATE 4: order state machine")
t = OrderTicket(1, "SPY", "BUY", 100, "TEST")
t.transition(OrderState.SUBMITTED)
check("PENDING_NEW -> SUBMITTED ok", t.state == OrderState.SUBMITTED)
try:
    t.transition(OrderState.SUBMITTED); ok = False
except RuntimeError: ok = True
check("illegal SUBMITTED -> SUBMITTED rejected", ok)
try:
    OrderTicket(2, "SPY", "BUY", 100, "T").transition(OrderState.FILLED); ok = False
except RuntimeError: ok = True
check("illegal PENDING_NEW -> FILLED rejected", ok)
t.transition(OrderState.FILLED)
check("SUBMITTED -> FILLED ok", t.state == OrderState.FILLED)

# --- G4: duplicate-fire protection -------------------------------------------
print("GATE 4: duplicate-fire protection")
p = make_params()
st = VolatilityParityMeanReversionStrategy(p, ["SPY"])
st.deploy()
px = gen(80, 7)
for i in range(80):
    feed(st, "SPY", i, float(px[i]))
st._pending.clear()  # isolate: clear any signal-dispatched ticket first
first = st._submit("SPY", "BUY", 10, "TEST_A")
second = st._submit("SPY", "BUY", 10, "TEST_B")
check("first submission accepted", first is not None)
check("duplicate submission blocked while pending", second is None)

# --- G3: parameter freezing ---------------------------------------------------
print("GATE 3: immutable parameter freezing")
try:
    st.p.zscore_entry = 99.0; ok = False
except Exception: ok = True
check("frozen dataclass params immutable", ok)
try:
    st.zscore_entry = 99.0; ok = False
except AttributeError: ok = True
check("post-deploy attribute write blocked", ok)
try:
    st.lookback_zscore = 5; ok = False
except AttributeError: ok = True
check("mid-run re-optimization write blocked", ok)
st.equity = 999_000.0
check("runtime equity marking still allowed", st.equity == 999_000.0)

# --- G1: zero-lookahead (future-perturbation audit) ---------------------------
print("GATE 1: zero-lookahead audit")
def run_and_hash(seed, mutate_future_from=None):
    strat = VolatilityParityMeanReversionStrategy(make_params(), ["SPY"])
    strat.deploy()
    prices = gen(300, seed)
    if mutate_future_from is not None:
        rng2 = np.random.default_rng(seed + 999)
        prices[mutate_future_from:] += rng2.normal(0, 50.0,
                                                   300 - mutate_future_from)
    for i in range(300):
        feed(strat, "SPY", i, float(prices[i]))
        if "SPY" in strat._pending and i + 1 < 300:
            strat.on_order_fill("SPY", float(prices[i + 1]))
    return [d["signal"] for d in strat.decision_log], \
           [(round(d["zscore"], 10) if d["zscore"] is not None else None) for d in strat.decision_log]

base_sig, base_z = run_and_hash(11)
mut_sig, mut_z = run_and_hash(11, mutate_future_from=150)
check("decisions up to t=150 identical after future mutation",
      base_sig[:150] == mut_sig[:150] and base_z[:150] == mut_z[:150])
check("future mutation does affect later decisions (sanity)",
      base_sig[200:] != mut_sig[200:] or base_z[200:] != mut_z[200:])

# --- G1: no negative shift / centered window patterns (source audit) ----------
print("GATE 1: source pattern audit")
src = open("vp_mr_strategy.py").read()
check("no shift(-1) lookahead", "shift(-1" not in src)
check("no shift(-", "shift(-" not in src)
check("no global scaler pattern", ".fit_transform" not in src and "StandardScaler" not in src)
check("buffers are bounded deques", "deque(maxlen=" in src)

# --- Module 2: imputation on bad bars ------------------------------------------
print("MODULE 2: imputation")
st2 = VolatilityParityMeanReversionStrategy(make_params(), ["SPY"])
st2.deploy()
pxs = gen(60, 3)
for i in range(60):
    c = float(pxs[i])
    if i == 50: st2.on_bar_close("SPY", i, c, math.nan, math.nan, math.nan, 0)
    else: feed(st2, "SPY", i, c)
buf = list(st2._close["SPY"])
offset = len(buf) - 60  # bounded deque drops early bars
check("NaN bar imputed with last known close",
      buf[50 + offset] == buf[49 + offset])
check("no NaN leaked into buffers",
      all(math.isfinite(x) for x in st2._close["SPY"]))

# --- Module 5: kill switch ------------------------------------------------------
print("MODULE 5: risk gates")
st3 = VolatilityParityMeanReversionStrategy(make_params(), ["SPY"])
st3.deploy()
st3.on_session_start()
st3.equity = st3._day_start_equity * (1 - 0.03)   # 3% intraday DD > 2% limit
check("kill switch trips at >=2% daily drawdown", st3._check_kill_switch())
st4 = VolatilityParityMeanReversionStrategy(make_params(), ["SPY"])
st4.deploy(); st4.on_session_start()
st4.equity = st4._day_start_equity * (1 - 0.01)
check("kill switch silent at 1% drawdown", not st4._check_kill_switch())

# --- Module 5: exposure & sizing caps ------------------------------------------
st5 = VolatilityParityMeanReversionStrategy(make_params(), ["SPY", "QQQ"])
st5.deploy()
p5 = gen(50, 21)
for i in range(50):
    feed(st5, "SPY", i, float(p5[i]))
    feed(st5, "QQQ", i, float(p5[i]))
last_px = st5._close["SPY"][-1]
st5.position["SPY"] = 900.0   # ~900 * last_px notional
gross = st5._gross_exposure()
check("gross exposure computed as notional (qty x px)",
      abs(gross - 900.0 * last_px) < 1e-6)
check("exposure cap blocks oversized add",
      not st5._exposure_ok(2000.0, last_px))
check("exposure cap allows small add",
      st5._exposure_ok(100.0, last_px))

# --- Module 1: session-close flatten --------------------------------------------
print("MODULE 1: session rules")
st6 = VolatilityParityMeanReversionStrategy(make_params(), ["SPY"])
st6.deploy()
st6.position["SPY"] = 500.0
st6.on_session_end()
check("session end submits flatten order", "SPY" in st6._pending)
check("flatten order direction correct", st6._pending["SPY"].side == "SELL")

# --- G2: AST sandbox -------------------------------------------------------------
print("GATE 2: AST sandbox")
import ast
BANNED = {"os","sys","subprocess","socket","urllib","requests","ctypes"}
CALLS = {"exec","eval","compile","__import__","open"}
viol = []
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Import):
        viol += [a.name for a in node.names if a.name.split(".")[0] in BANNED]
    elif isinstance(node, ast.ImportFrom) and node.module:
        if node.module.split(".")[0] in BANNED: viol.append(node.module)
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id in CALLS: viol.append(node.func.id)
check("no banned imports/calls", not viol)

print(f"\nRESULT: {PASS} passed, {FAIL} failed")
exit(1 if FAIL else 0)
