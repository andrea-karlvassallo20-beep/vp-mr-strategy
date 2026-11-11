from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from typing import Deque, Dict, List, Optional, Tuple

import math
import numpy as np


@dataclass(frozen=True)
class StrategyParameters:
    lookback_zscore: int = 100
    zscore_entry: float = 2.0
    zscore_exit: float = 0.25
    atr_lookback: int = 14
    atr_stop_multiple: float = 3.0
    vol_target_annual: float = 0.12
    vol_est_lookback: int = 60
    fractional_kelly: float = 0.25
    max_trade_risk_pct: float = 0.50
    max_daily_drawdown_pct: float = 0.02
    max_gross_exposure: float = 1.0
    bars_per_year: float = 252.0
    latency_ms: float = 5.0
    half_spread_bps: float = 2.0
    impact_coeff: float = 0.10
    commission_bps: float = 0.50
    min_history_bars: int = 250
    max_open_orders: int = 1
    flatten_at_session_close: bool = True


class OrderState(Enum):
    PENDING_NEW = auto()
    SUBMITTED = auto()
    PARTIALLY_FILLED = auto()
    FILLED = auto()
    CANCELLED = auto()
    REJECTED = auto()
    EXPIRED = auto()


_VALID_TRANSITIONS = {
    OrderState.PENDING_NEW: {OrderState.SUBMITTED, OrderState.CANCELLED},
    OrderState.SUBMITTED: {OrderState.PARTIALLY_FILLED, OrderState.FILLED,
                            OrderState.CANCELLED, OrderState.REJECTED,
                            OrderState.EXPIRED},
    OrderState.PARTIALLY_FILLED: {OrderState.FILLED, OrderState.REJECTED,
                                   OrderState.EXPIRED},
    OrderState.FILLED: set(),
    OrderState.CANCELLED: set(),
    OrderState.REJECTED: set(),
    OrderState.EXPIRED: set(),
}


@dataclass
class OrderTicket:
    order_id: int
    instrument: str
    side: str
    quantity: float
    reason: str
    state: OrderState = OrderState.PENDING_NEW
    filled_qty: float = 0.0
    submitted_ts: Optional[int] = None
    filled_ts: Optional[int] = None
    expected_exec_px: float = 0.0
    expected_cost: float = 0.0

    def transition(self, new_state: OrderState) -> None:
        if new_state not in _VALID_TRANSITIONS[self.state]:
            raise RuntimeError(
                f"Illegal order transition {self.state.name} -> {new_state.name}")
        self.state = new_state


class VolatilityParityMeanReversionStrategy:

    def __init__(self, params: StrategyParameters,
                 universe: List[str],
                 initial_equity: float = 1_000_000.0) -> None:
        self.p = params
        self.universe = list(universe)
        self.initial_equity = initial_equity
        self.equity = initial_equity
        self._deployed = False

        maxlen = max(params.lookback_zscore, params.vol_est_lookback,
                     params.atr_lookback, params.min_history_bars) + 5
        self._close: Dict[str, Deque[float]] = {s: deque(maxlen=maxlen) for s in universe}
        self._high: Dict[str, Deque[float]] = {s: deque(maxlen=maxlen) for s in universe}
        self._low: Dict[str, Deque[float]] = {s: deque(maxlen=maxlen) for s in universe}

        self.position: Dict[str, float] = {s: 0.0 for s in universe}
        self._entry_px: Dict[str, float] = {}
        self._trail_stop: Dict[str, float] = {}
        self._day_start_equity = initial_equity
        self._kill_switch = False

        self._next_oid = 1
        self._pending: Dict[str, OrderTicket] = {}
        self.order_log: List[dict] = []
        self.decision_log: List[dict] = []
        self.equity_curve: List[float] = []

    def deploy(self) -> None:
        if self._deployed:
            raise RuntimeError("Already deployed: parameters frozen (Gate 3).")
        self._deployed = True

    def __setattr__(self, name, value):
        if getattr(self, "_deployed", False):
            allowed = {"equity", "_day_start_equity", "_kill_switch",
                       "position", "_entry_px", "_trail_stop", "equity_curve",
                       "_next_oid", "_pending", "order_log", "decision_log"}
            if name not in allowed:
                raise AttributeError(f"'{name}' frozen post-deployment (Gate 3).")
        object.__setattr__(self, name, value)

    def on_session_start(self) -> None:
        self._day_start_equity = self.equity
        self._kill_switch = False

    def on_session_end(self) -> None:
        if self.p.flatten_at_session_close:
            for s in self.universe:
                if self.position[s] != 0.0:
                    self._submit(s, "SELL" if self.position[s] > 0 else "BUY",
                                 abs(self.position[s]), "SESSION_CLOSE_FLATTEN")

    def _atr(self, s: str) -> Optional[float]:
        h = np.asarray(self._high[s]); l = np.asarray(self._low[s])
        c = np.asarray(self._close[s]); n = self.p.atr_lookback
        if len(c) < n + 1:
            return None
        pc = c[-(n + 1):-1]
        tr = np.maximum(h[-n:] - l[-n:],
                        np.maximum(np.abs(h[-n:] - pc), np.abs(l[-n:] - pc)))
        return float(tr.mean())

    def _realized_vol_ann(self, s: str) -> Optional[float]:
        c = np.asarray(self._close[s]); n = self.p.vol_est_lookback
        if len(c) < n + 1:
            return None
        r = np.diff(np.log(c[-(n + 1):]))
        return float(r.std(ddof=1) * math.sqrt(self.p.bars_per_year))

    def _zscore(self, s: str) -> Optional[float]:
        n = self.p.lookback_zscore
        c = np.asarray(self._close[s])
        if len(c) < n:
            return None
        w = c[-n:]
        sd = w.std(ddof=1)
        if sd <= 0:
            return None
        return float((w[-1] - w.mean()) / sd)

    def _warm(self, s: str) -> bool:
        return len(self._close[s]) >= self.p.min_history_bars

    def _signals(self, s: str) -> Tuple[bool, bool, bool, bool]:
        z = self._zscore(s) if self._warm(s) else None
        pos = self.position[s]
        blocked = (s in self._pending) or self._kill_switch
        if z is None:
            return False, False, False, False
        long_entry = (z <= -self.p.zscore_entry) and pos == 0.0 and not blocked
        short_entry = (z >= self.p.zscore_entry) and pos == 0.0 and not blocked
        long_exit = (pos > 0.0) and (z >= -self.p.zscore_exit)
        short_exit = (pos < 0.0) and (z <= self.p.zscore_exit)
        return long_entry, short_entry, long_exit, short_exit

    def _half_spread_frac(self) -> float:
        return self.p.half_spread_bps / 10_000.0

    def _slippage_px(self, side: str, px: float) -> float:
        hs = self._half_spread_frac()
        return px * (1.0 + hs) if side == "BUY" else px * (1.0 - hs)

    def _impact_bps(self, qty: float) -> float:
        return self.p.impact_coeff * 100.0 * math.sqrt(max(qty, 0.0) / 1e4)

    def _total_cost_bps(self, qty: float) -> float:
        return (2.0 * self.p.half_spread_bps + self._impact_bps(qty)
                + self.p.commission_bps)

    def _expected_cost(self, px: float, qty: float) -> float:
        return self._total_cost_bps(qty) / 10_000.0 * px * qty

    def _gross_exposure(self) -> float:
        total = 0.0
        for s, q in self.position.items():
            if q == 0.0:
                continue
            if len(self._close[s]) > 0:
                px = self._close[s][-1]
            else:
                px = self._entry_px.get(s, 0.0)
            total += abs(q) * px
        return total

    def _size(self, s: str, px: float) -> float:
        vol = self._realized_vol_ann(s)
        if vol is None or vol <= 0:
            return 0.0
        w = min((self.p.vol_target_annual / vol) * self.p.fractional_kelly,
                self.p.max_trade_risk_pct)
        qty = (self.equity * w) / px
        atr = self._atr(s)
        if atr is not None and atr > 0:
            max_risk_notional = self.equity * self.p.max_trade_risk_pct
            qty = min(qty, max_risk_notional / (self.p.atr_stop_multiple * atr))
        return float(math.floor(qty)) if qty >= 1.0 else 0.0

    def _update_trail(self, s: str, close: float, atr: float) -> None:
        d = self.p.atr_stop_multiple * atr
        if self.position[s] > 0:
            t = close - d
            self._trail_stop[s] = max(self._trail_stop.get(s, t), t)
        elif self.position[s] < 0:
            t = close + d
            self._trail_stop[s] = min(self._trail_stop.get(s, t), t)

    def _check_kill_switch(self) -> bool:
        dd = (self._day_start_equity - self.equity) / self._day_start_equity
        if dd >= self.p.max_daily_drawdown_pct:
            self._kill_switch = True
        return self._kill_switch

    def _exposure_ok(self, add_qty: float, px: float) -> bool:
        return (self._gross_exposure() + add_qty * px) <= \
            self.p.max_gross_exposure * self.equity * 1.0001

    def _submit(self, s: str, side: str, qty: float, reason: str) -> Optional[OrderTicket]:
        if qty <= 0:
            return None
        if s in self._pending:
            return None
        t = OrderTicket(self._next_oid, s, side, qty, reason)
        self._next_oid += 1
        t.transition(OrderState.SUBMITTED)
        t.submitted_ts = None
        self._pending[s] = t
        self.order_log.append({"order_id": t.order_id, "instrument": s,
                               "side": side, "qty": qty, "reason": reason,
                               "state": t.state.name})
        return t

    def on_order_fill(self, s: str, px: float) -> None:
        t = self._pending.get(s)
        if t is None:
            return
        exec_px = self._slippage_px(t.side, px)
        t.expected_exec_px = exec_px
        t.expected_cost = self._expected_cost(exec_px, t.quantity)
        t.transition(OrderState.FILLED)
        signed = t.quantity if t.side == "BUY" else -t.quantity
        self.position[s] += signed
        if self.position[s] != 0.0:
            self._entry_px[s] = exec_px
        else:
            self._entry_px.pop(s, None)
            self._trail_stop.pop(s, None)
        self.equity -= t.expected_cost
        self.order_log.append({"order_id": t.order_id, "instrument": s,
                               "state": "FILLED", "exec_px": exec_px,
                               "expected_cost": t.expected_cost})
        del self._pending[s]

    def on_order_reject(self, s: str, reason: str) -> None:
        t = self._pending.pop(s, None)
        if t is not None:
            t.transition(OrderState.REJECTED)
            self.order_log.append({"order_id": t.order_id, "state": "REJECTED",
                                   "reason": reason})

    def on_bar_close(self, s: str, ts: int, o: float, h: float,
                     l: float, c: float, v: float) -> None:
        buf_c = self._close[s]
        le, se, lx, sx = self._signals(s)
        z = self._zscore(s) if self._warm(s) else None
        pos_at_decision = self.position[s]
        blocked_at_decision = (s in self._pending) or self._kill_switch

        if not np.isfinite(c) or c <= 0:
            c = buf_c[-1] if buf_c else c
            h = l = c

        if self.position[s] != 0.0 and s in self._trail_stop:
            stop = self._trail_stop[s]
            if (self.position[s] > 0 and c <= stop) or \
               (self.position[s] < 0 and c >= stop):
                self._submit(s, "SELL" if self.position[s] > 0 else "BUY",
                             abs(self.position[s]), "ATR_TRAILING_STOP")

        if self._check_kill_switch():
            if self.position[s] != 0.0:
                self._submit(s, "SELL" if self.position[s] > 0 else "BUY",
                             abs(self.position[s]), "KILL_SWITCH")
        elif le:
            q = self._size(s, c)
            if q > 0 and self._exposure_ok(q, c):
                self._submit(s, "BUY", q, "ZSCORE_LONG_ENTRY")
        elif se:
            q = self._size(s, c)
            if q > 0 and self._exposure_ok(q, c):
                self._submit(s, "SELL", q, "ZSCORE_SHORT_ENTRY")
        elif lx:
            self._submit(s, "SELL", self.position[s], "ZSCORE_LONG_EXIT")
        elif sx:
            self._submit(s, "BUY", -self.position[s], "ZSCORE_SHORT_EXIT")

        buf_c.append(float(c))
        self._high[s].append(float(h))
        self._low[s].append(float(l))

        if self.position[s] != 0.0:
            atr = self._atr(s)
            if atr is not None:
                self._update_trail(s, c, atr)

        self.decision_log.append({
            "ts": ts, "instrument": s, "zscore": z,
            "atr": self._atr(s), "vol_ann": self._realized_vol_ann(s),
            "signal": int(le) - int(se), "position": self.position[s],
            "pos_at_decision": pos_at_decision,
            "blocked_at_decision": blocked_at_decision,
            "pending": s in self._pending, "kill_switch": self._kill_switch,
            "latency_ms": self.p.latency_ms,
        })
        self.equity_curve.append(self.equity)

    def signal_parity_index(self) -> float:
        if not self.decision_log:
            return 1.0
        match = 0
        for rec in self.decision_log:
            z = rec["zscore"]
            if z is None:
                exp = 0
            else:
                le = (z <= -self.p.zscore_entry) and rec["pos_at_decision"] == 0.0 \
                     and not rec["blocked_at_decision"]
                se = (z >= self.p.zscore_entry) and rec["pos_at_decision"] == 0.0 \
                     and not rec["blocked_at_decision"]
                exp = int(le) - int(se)
            if exp == rec["signal"]:
                match += 1
        return match / len(self.decision_log)


def run_offline_validation() -> dict:
    params = StrategyParameters(min_history_bars=60, lookback_zscore=40,
                                vol_est_lookback=30)
    strat = VolatilityParityMeanReversionStrategy(params, ["SPY", "QQQ"],
                                                  initial_equity=1_000_000.0)
    strat.deploy()

    rng = np.random.default_rng(42)
    n_bars = 600
    prices = {"SPY": 450.0 + np.cumsum(rng.normal(0, 0.9, n_bars)),
              "QQQ": 380.0 + np.cumsum(rng.normal(0, 1.1, n_bars))}

    for t in range(n_bars):
        if t % 252 == 0:
            strat.on_session_start()
        for s in strat.universe:
            c = float(prices[s][t])
            h, l = c * 1.002, c * 0.998
            strat.on_bar_close(s, t, c, h, l, c, 1e6)
            if s in strat._pending and t + 1 < n_bars:
                strat.on_order_fill(s, float(prices[s][t + 1]))
        if t % 252 == 251:
            strat.on_session_end()

    fills = [o for o in strat.order_log if o.get("state") == "FILLED"]
    return {
        "bars_processed": n_bars,
        "orders_logged": len(strat.order_log),
        "fills": len(fills),
        "final_equity": round(strat.equity, 2),
        "positions": dict(strat.position),
        "signal_parity_index": round(strat.signal_parity_index(), 4),
    }


if __name__ == "__main__":
    report = run_offline_validation()
    for k, v in report.items():
        print(f"{k}: {v}")
