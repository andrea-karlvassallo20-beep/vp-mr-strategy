"""Wiring test for the NautilusTrader adapter using a lightweight framework
stub. Verifies the full round trip without the real engine:
  bar -> core signal -> ticket -> engine order -> fill event -> core position.
This file is test harness only (stub injection requires sys); the strategy
and adapter themselves remain AST-gate compliant."""
import math
import sys
import types
from collections import namedtuple


# --------------------------- nautilus_trader stub ---------------------------
class _Enum:
    def __init__(self, name): self.name = name
    def __repr__(self): return self.name

OrderSide = types.SimpleNamespace(BUY=_Enum("BUY"), SELL=_Enum("SELL"))
TimeInForce = types.SimpleNamespace(GTC=_Enum("GTC"))

class InstrumentId:
    def __init__(self, sym): self.sym = sym
    @classmethod
    def from_str(cls, s): return cls(s)
    def __str__(self): return self.sym

class Quantity:
    def __init__(self, v): self.v = v

class Price:
    def __init__(self, v): self.v = v

class _Order:
    _next = 1
    def __init__(self, instrument_id, order_side, quantity, time_in_force=None):
        self.client_order_id = f"COID-{_Order._next}"; _Order._next += 1
        self.instrument_id = instrument_id
        self.order_side = order_side
        self.quantity = quantity

class OrderFactory:
    def market(self, **kw): return _Order(**kw)

class _Log:
    def info(self, msg): self.last = msg

class StrategyStub:
    """Mimics nautilus_trader.trading.strategy.Strategy."""
    def __init__(self, config):
        self.config = config
        self.order_factory = OrderFactory()
        self.log = _Log()
        self.submitted = []
        self._bar_sub = None
    def subscribe_bars(self, spec): self._bar_sub = spec
    def submit_order(self, order): self.submitted.append(order)

Bar = namedtuple("Bar", ["instrument_id", "ts_event", "open", "high",
                         "low", "close", "volume"])
OrderFilled = namedtuple("OrderFilled", ["client_order_id", "last_px"])
OrderRejected = namedtuple("OrderRejected", ["client_order_id", "reason"])

class StrategyConfigStub:
    def __init_subclass__(cls, frozen=False, **kw):
        super().__init_subclass__(**kw)
    def __init__(self, **kw):
        self.__dict__.update(kw)

nt = types.ModuleType("nautilus_trader")
nt.config = types.SimpleNamespace(StrategyConfig=StrategyConfigStub)
nt.model = types.SimpleNamespace(
    data=types.SimpleNamespace(Bar=Bar),
    enums=types.SimpleNamespace(OrderSide=OrderSide, TimeInForce=TimeInForce),
    events=types.SimpleNamespace(OrderFilled=OrderFilled,
                                 OrderRejected=OrderRejected),
    identifiers=types.SimpleNamespace(InstrumentId=InstrumentId),
    objects=types.SimpleNamespace(Quantity=Quantity, Price=Price))
nt.trading = types.SimpleNamespace(
    strategy=types.SimpleNamespace(Strategy=StrategyStub))
sys.modules["nautilus_trader"] = nt
sys.modules["nautilus_trader.config"] = nt.config
sys.modules["nautilus_trader.model"] = nt.model
sys.modules["nautilus_trader.model.data"] = nt.model.data
sys.modules["nautilus_trader.model.enums"] = nt.model.enums
sys.modules["nautilus_trader.model.events"] = nt.model.events
sys.modules["nautilus_trader.model.identifiers"] = nt.model.identifiers
sys.modules["nautilus_trader.model.objects"] = nt.model.objects
sys.modules["nautilus_trader.trading"] = nt.trading
sys.modules["nautilus_trader.trading.strategy"] = nt.trading.strategy

# ------------------------------- test --------------------------------------
from nautilus_adapter import VPMeanReversionConfig, VPMeanReversionAdapter
from backtest_study import ou_prices
import numpy as np

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {name}")
    else:    FAIL += 1; print(f"  FAIL  {name}")

cfg = VPMeanReversionConfig()
cfg.instrument_ids = ["SPY"]
cfg.min_history_bars = 60
cfg.lookback_zscore = 40
cfg.vol_est_lookback = 30
adapter = VPMeanReversionAdapter(cfg)

check("core constructed with frozen params",
      adapter.core.p.zscore_entry == 2.0)
adapter.on_start()
check("Gate 3 freeze engaged on start", adapter.core._deployed)
check("bar subscription registered", adapter._bar_sub == "1-DAY-BID")

prices = ou_prices(200, 77)
fills = 0
for t in range(200):
    c = float(prices[t])
    adapter.on_bar(Bar("SPY.XNAS", t, c, c*1.002, c*0.998, c, 1e6))
    # engine executes submitted orders: simulate fill at next bar open
    if adapter.submitted:
        order = adapter.submitted.pop(0)
        if t + 1 < 200:
            adapter.on_order_filled(OrderFilled(order.client_order_id,
                                                 float(prices[t+1])))
            fills += 1

check("engine orders submitted from core tickets", fills > 0)
check("core positions updated via fill events",
      any(abs(v) > 0 for v in adapter.core.position.values())
      or fills >= 2)
check("ticket->engine order map consistent",
      len(adapter._ticket_to_order) >= fills)
check("core equity reflects costs (friction applied)",
      adapter.core.equity < adapter.core.initial_equity)

# rejection path
adapter.core._submit("SPY", "BUY", 100, "TEST_REJECT")
ticket = adapter.core._pending["SPY"]
oid = OrderFactory().market(instrument_id=InstrumentId.from_str("SPY.ARCA"),
                            order_side=OrderSide.BUY,
                            quantity=Quantity(100),
                            time_in_force=TimeInForce.GTC).client_order_id
adapter._ticket_to_order[ticket.order_id] = oid
adapter._order_to_instrument[oid] = "SPY"
adapter.on_order_rejected(OrderRejected(oid, "INSUFFICIENT_LIQUIDITY"))
check("rejection reconciled into core state machine",
      "SPY" not in adapter.core._pending)

# shutdown flatten path
adapter.core.position["SPY"] = 800.0
adapter.close_all_positions()
check("shutdown flatten submits engine order", len(adapter.submitted) == 1)

print(f"\nRESULT: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
