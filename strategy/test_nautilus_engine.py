"""Real NautilusTrader engine test: BacktestEngine + adapter end-to-end.
Requires nautilus_trader installed (CI 'engine' job installs it).
Skips with exit 0 if the engine is unavailable."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    import nautilus_trader  # noqa: F401
except ImportError:
    print("nautilus_trader not installed - skipping real-engine test")
    sys.exit(0)

import numpy as np
from nautilus_trader.backtest.engine import BacktestEngine, BacktestEngineConfig
from nautilus_trader.common.config import LoggingConfig
from nautilus_trader.model.data import Bar, BarType, QuoteTick
from nautilus_trader.model.enums import AccountType, OmsType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money, Currency, Price, Quantity
from nautilus_trader.test_kit.providers import TestInstrumentProvider

from nautilus_adapter import VPMeanReversionConfig, VPMeanReversionAdapter

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")


def ou_prices(n, seed, s0=450.0, theta=0.05, sigma=1.2):
    rng = np.random.default_rng(seed)
    p = np.empty(n); p[0] = s0
    for i in range(1, n):
        p[i] = p[i-1] + theta * (s0 - p[i-1]) + rng.normal(0, sigma)
    return p


engine = BacktestEngine(config=BacktestEngineConfig(
    trader_id="VP-MR-TEST", logging=LoggingConfig(log_level="ERROR")))
engine.add_venue(
    venue=Venue("ARCA"),
    oms_type=OmsType.NETTING,
    account_type=AccountType.MARGIN,
    starting_balances=[Money(1_000_000, Currency.from_str("USD"))],
)
instrument = TestInstrumentProvider.equity(symbol="SPY", venue="ARCA")
engine.add_instrument(instrument)

bar_type = BarType.from_str("SPY.ARCA-1-DAY-BID-EXTERNAL")
prices = ou_prices(150, 42)
DAY_NS = 86_400_000_000_000
T0 = 1_700_000_000_000_000_000

bars, quotes = [], []
for i, p in enumerate(prices):
    c = round(float(p), 2)
    ts = T0 + i * DAY_NS
    bars.append(Bar(bar_type, Price(c, 2),
                    Price(round(c * 1.002, 2), 2),
                    Price(round(c * 0.998, 2), 2),
                    Price(c, 2), Quantity(1_000_000, 0), ts, ts))
    quotes.append(QuoteTick(instrument.id,
                            Price(round(c - 0.02, 2), 2),
                            Price(round(c + 0.02, 2), 2),
                            Quantity(100_000, 0), Quantity(100_000, 0),
                            ts, ts))
engine.add_data(bars)
engine.add_data(quotes)

config = VPMeanReversionConfig(
    instrument_ids=("SPY",),
    bar_spec="SPY.ARCA-1-DAY-BID-EXTERNAL",
    min_history_bars=60, lookback_zscore=40, vol_est_lookback=30)
adapter = VPMeanReversionAdapter(config)
engine.add_strategy(adapter)

engine.run()

check("engine run completed", engine.run_finished is not None)
check("core processed every bar", len(adapter.core.decision_log) == 150)
check("engine executed orders (fills reconciled to core)",
      sum(1 for o in adapter.core.order_log
          if o.get("state") == "FILLED") > 0)
check("core SPI intact under real engine", adapter.core.signal_parity_index() >= 0.98)
engine_orders = list(engine.cache.orders())
check("engine saw submitted orders", len(engine_orders) > 0)
check("no orders left open", len(list(engine.cache.orders_open())) == 0)
rejections = [o for o in engine_orders
               if any(type(e).__name__ == "OrderRejected" for e in o.events)]
check("no order rejections", len(rejections) == 0)

engine.dispose()
print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
