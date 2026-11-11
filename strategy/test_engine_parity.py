"""Engine-parity suite: identical data, two execution paths, one decision core.

Runs the same deterministic OHLCV series through:
  (a) the offline runner (CSV feed, modeled fills)
  (b) the real NautilusTrader BacktestEngine (real matching engine)
and asserts the core strategy's decision stream (z-scores and signals)
is invariant to the execution environment — the strategy-layer statement
of Signal Parity across engines.

Requires nautilus_trader (CI engine job); skips otherwise. Harness file."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def ou_bars(n, seed, s0=450.0, theta=0.05, sigma=1.2):
    rng = np.random.default_rng(seed)
    p = np.empty(n); p[0] = s0
    for i in range(1, n):
        p[i] = p[i-1] + theta * (s0 - p[i-1]) + rng.normal(0, sigma)
    bars = []
    import datetime
    d0 = datetime.date(2024, 1, 1)
    for i in range(n):
        c = float(p[i])
        bars.append(((d0 + datetime.timedelta(days=i)).isoformat(),
                     c, c * 1.002, c * 0.998, c, 1e6))
    return bars


N = 300
BARS = ou_bars(N, 42)

# ---- path (a): offline runner ----
from papertrading_runner import PaperTradingRunner
from vp_mr_strategy import StrategyParameters

tmp = Path(tempfile.mkdtemp())
data_dir = tmp / "data"; data_dir.mkdir()
with open(data_dir / "spy.csv", "w") as f:
    f.write("date,open,high,low,close,volume\n")
    for b in BARS:
        f.write(",".join(str(x) for x in b) + "\n")

params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                            vol_est_lookback=30)
runner = PaperTradingRunner(data_dir, tmp / "state", params=params,
                            universe=["SPY"])
runner.run_session()
core_runner = runner.strat
check("runner processed all bars",
      len(core_runner.decision_log) == N)

# ---- path (b): real NautilusTrader engine ----
try:
    import nautilus_trader  # noqa: F401
except ImportError:
    print("nautilus_trader not installed - skipping engine parity")
    print(f"\nRESULT: {PASS} passed, {FAIL} failed")
    sys.exit(0 if FAIL else 1)

from nautilus_trader.backtest.engine import BacktestEngine, BacktestEngineConfig
from nautilus_trader.common.config import LoggingConfig
from nautilus_trader.model.data import Bar, BarType, QuoteTick
from nautilus_trader.model.enums import AccountType, OmsType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money, Currency, Price, Quantity
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_adapter import VPMeanReversionConfig, VPMeanReversionAdapter

engine = BacktestEngine(config=BacktestEngineConfig(
    trader_id="VP-MR-PARITY", logging=LoggingConfig(log_level="ERROR")))
engine.add_venue(venue=Venue("ARCA"), oms_type=OmsType.NETTING,
                account_type=AccountType.MARGIN,
                starting_balances=[Money(1_000_000, Currency.from_str("USD"))])
instrument = TestInstrumentProvider.equity(symbol="SPY", venue="ARCA")
engine.add_instrument(instrument)

bar_type = BarType.from_str("SPY.ARCA-1-DAY-BID-EXTERNAL")
DAY_NS = 86_400_000_000_000
T0 = 1_700_000_000_000_000_000
nbars, quotes = [], []
for i, b in enumerate(BARS):
    c = round(float(b[4]), 2)
    ts = T0 + i * DAY_NS
    nbars.append(Bar(bar_type, Price(c, 2),
                      Price(round(float(b[2]), 2), 2),
                      Price(round(float(b[3]), 2), 2),
                      Price(c, 2), Quantity(1_000_000, 0), ts, ts))
    quotes.append(QuoteTick(instrument.id,
                            Price(round(c - 0.02, 2), 2),
                            Price(round(c + 0.02, 2), 2),
                            Quantity(100_000, 0), Quantity(100_000, 0),
                            ts, ts))
engine.add_data(nbars)
engine.add_data(quotes)

config = VPMeanReversionConfig(
    instrument_ids=("SPY",), bar_spec="SPY.ARCA-1-DAY-BID-EXTERNAL",
    min_history_bars=60, lookback_zscore=40, vol_est_lookback=30)
adapter = VPMeanReversionAdapter(config)
engine.add_strategy(adapter)
engine.run()
core_engine = adapter.core
engine.dispose()

check("engine processed all bars", len(core_engine.decision_log) == N)

# ---- parity: decision-time features must agree across engines ----
z_runner = [r["zscore"] for r in core_runner.decision_log]
z_engine = [r["zscore"] for r in core_engine.decision_log]
n_common = min(len(z_runner), len(z_engine))
zr = [z for z in z_runner[:n_common] if z is not None]
ze = [z for z in z_engine[:n_common] if z is not None]
check("z-score streams have equal length",
      len(z_runner) == len(z_engine))
# engine prices are quantized to 2 decimals (Price precision); runner uses
# full floats -> z-scores agree up to rounding, signals must agree exactly
max_zdiff = max((abs(a - b) for a, b in zip(zr, ze)), default=0.0)
print(f"  NOTE max |z_runner - z_engine| = {max_zdiff:.2e}")
check("z-score streams agree within price-quantization tolerance",
      max_zdiff < 5e-3)

sig_runner = [r["signal"] for r in core_runner.decision_log[:n_common]]
sig_engine = [r["signal"] for r in core_engine.decision_log[:n_common]]
check("signal streams identical across engines", sig_runner == sig_engine)

check("runner core SPI", core_runner.signal_parity_index() >= 0.98)
check("engine core SPI", core_engine.signal_parity_index() >= 0.98)

# fill counts may differ (modeled vs real fills) — report, don't gate
fr = sum(1 for o in core_runner.order_log if o.get("state") == "FILLED")
fe = sum(1 for o in core_engine.order_log if o.get("state") == "FILLED")
print(f"  NOTE fills: runner={fr}, engine={fe} "
      f"(fill models differ by design; decisions must not)")

import shutil
shutil.rmtree(tmp)
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
