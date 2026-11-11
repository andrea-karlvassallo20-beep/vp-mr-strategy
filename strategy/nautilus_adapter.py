"""
NautilusTrader adapter for VP-MR-ETF-D1-001.

Bridges the engine-agnostic core strategy (vp_mr_strategy.py) to the
NautilusTrader event-driven framework. The core class owns all decision
logic, gates, and risk; this adapter only translates events:

  NautilusTrader                       Core strategy
  -------------                        ------------
  on_bar(bar)                    -->   on_bar_close(...)      [t-1 rule preserved]
  on_order_filled(event)         -->   on_order_fill(...)     [GATE 4 reconciliation]
  on_order_rejected(event)       -->   on_order_reject(...)
  on_event(session start/end)     -->   on_session_start/end()

No lookahead can enter here: the adapter passes only the closed bar's OHLCV
to the core, which computes signals from strictly prior buffer state.
"""
from typing import Dict, List

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.events import OrderFilled, OrderRejected
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.objects import Quantity
from nautilus_trader.trading.strategy import Strategy

from vp_mr_strategy import StrategyParameters, VolatilityParityMeanReversionStrategy


class VPMeanReversionConfig(StrategyConfig, frozen=True):
    """Declarative config -> frozen StrategyParameters (Gate 3)."""
    instrument_ids: List[str] = ["SPY", "QQQ"]
    bar_spec: str = "1-DAY-BID"
    initial_equity: float = 1_000_000.0
    zscore_entry: float = 2.0
    zscore_exit: float = 0.25
    lookback_zscore: int = 100
    atr_lookback: int = 14
    atr_stop_multiple: float = 3.0
    vol_target_annual: float = 0.12
    vol_est_lookback: int = 60
    fractional_kelly: float = 0.25
    max_trade_risk_pct: float = 0.50
    max_daily_drawdown_pct: float = 0.02
    min_history_bars: int = 250


class VPMeanReversionAdapter(Strategy):
    """
    NautilusTrader Strategy wrapping the sandboxed core. Order flow:
    core submits an internal OrderTicket -> adapter translates to a real
    NautilusTrader MarketOrder -> fills reconcile back into the core's
    order state machine.
    """

    def __init__(self, config: VPMeanReversionConfig) -> None:
        super().__init__(config)
        self._config = config
        params = StrategyParameters(
            zscore_entry=config.zscore_entry,
            zscore_exit=config.zscore_exit,
            lookback_zscore=config.lookback_zscore,
            atr_lookback=config.atr_lookback,
            atr_stop_multiple=config.atr_stop_multiple,
            vol_target_annual=config.vol_target_annual,
            vol_est_lookback=config.vol_est_lookback,
            fractional_kelly=config.fractional_kelly,
            max_trade_risk_pct=config.max_trade_risk_pct,
            max_daily_drawdown_pct=config.max_daily_drawdown_pct,
            min_history_bars=config.min_history_bars,
        )
        self.core = VolatilityParityMeanReversionStrategy(
            params, list(config.instrument_ids), config.initial_equity)
        # Map core ticket -> engine client_order_id for reconciliation
        self._ticket_to_order: Dict[int, object] = {}
        self._order_to_instrument: Dict[object, str] = {}

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def on_start(self) -> None:
        self.core.deploy()  # Gate 3 freeze
        self.subscribe_bars(self._config.bar_spec)

    def on_stop(self) -> None:
        self.close_all_positions()

    # ------------------------------------------------------------------
    # Market data -> core (t-1 signal rule preserved end-to-end)
    # ------------------------------------------------------------------
    def on_bar(self, bar: Bar) -> None:
        instrument = self._instrument_str(bar.instrument_id)
        ts = int(bar.ts_event)
        self.core.on_bar_close(
            instrument, ts,
            float(bar.open), float(bar.high),
            float(bar.low), float(bar.close), float(bar.volume))
        self._drain_pending_tickets(instrument, bar)

    # ------------------------------------------------------------------
    # Core -> engine orders
    # ------------------------------------------------------------------
    def _drain_pending_tickets(self, instrument: str, bar: Bar) -> None:
        ticket = self.core._pending.get(instrument)
        if ticket is None:
            return
        instrument_id = InstrumentId.from_str(f"{instrument}.ARCA")
        qty = Quantity(float(ticket.quantity))
        side = OrderSide.BUY if ticket.side == "BUY" else OrderSide.SELL
        order = self.order_factory.market(
            instrument_id=instrument_id,
            order_side=side,
            quantity=qty,
            time_in_force=TimeInForce.GTC,
        )
        self._ticket_to_order[ticket.order_id] = order.client_order_id
        self._order_to_instrument[order.client_order_id] = instrument
        self.submit_order(order)
        self.log.info(
            f"Submitted {ticket.side} {ticket.quantity} {instrument} "
            f"[{ticket.reason}] ticket={ticket.order_id}")

    # ------------------------------------------------------------------
    # Engine events -> core state machine (Gate 4 reconciliation)
    # ------------------------------------------------------------------
    def on_order_filled(self, event: OrderFilled) -> None:
        instrument = self._order_to_instrument.get(event.client_order_id)
        if instrument is None:
            return
        self.core.on_order_fill(instrument, float(event.last_px))
        self.log.info(f"Filled {instrument} @ {event.last_px}")

    def on_order_rejected(self, event: OrderRejected) -> None:
        instrument = self._order_to_instrument.pop(event.client_order_id, None)
        if instrument is None:
            return
        self.core.on_order_reject(instrument, str(event.reason))

    # ----------------------------------------------------------------    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _instrument_str(instrument_id) -> str:
        return str(instrument_id).split(".")[0]

    def close_all_positions(self) -> None:
        """Shutdown flatten: submit engine orders directly (no bar drain)."""
        for instrument, qty in self.core.position.items():
            if qty == 0.0:
                continue
            self.core._submit(instrument, "SELL" if qty > 0 else "BUY",
                              abs(qty), "ADAPTER_SHUTDOWN_FLATTEN")
            ticket = self.core._pending.get(instrument)
            if ticket is None:
                continue
            instrument_id = InstrumentId.from_str(f"{instrument}.ARCA")
            side = OrderSide.BUY if ticket.side == "BUY" else OrderSide.SELL
            order = self.order_factory.market(
                instrument_id=instrument_id,
                order_side=side,
                quantity=Quantity(float(ticket.quantity)),
                time_in_force=TimeInForce.GTC)
            self._ticket_to_order[ticket.order_id] = order.client_order_id
            self._order_to_instrument[order.client_order_id] = instrument
            self.submit_order(order)
