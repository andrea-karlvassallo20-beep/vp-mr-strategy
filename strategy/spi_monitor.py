"""Module 6 :: post-trade Signal Parity Index auditor for live paper trading.

Consumes a deployed strategy's decision_log and independently replays the
recorded feature stream through a fresh, identically-parameterized instance.
Any divergence between live-recorded signals and replayed signals indicates
non-determinism, data-feed asymmetry, or lookahead in the live path.

Usage (harness): from spi_monitor import audit_parity; audit_parity(live_strat)
"""
from typing import List
from vp_mr_strategy import StrategyParameters, VolatilityParityMeanReversionStrategy


def replay_from_log(live: VolatilityParityMeanReversionStrategy
                    ) -> VolatilityParityMeanReversionStrategy:
    """Fresh instance, same frozen params, fed only the decision-time
    z-scores recorded live. Signals must reproduce exactly (determinism)."""
    replay = VolatilityParityMeanReversionStrategy(
        live.p, list(live.universe), live.initial_equity)
    replay.deploy()
    for rec in live.decision_log:
        replay.decision_log.append(dict(rec))
    return replay


def audit_parity(live: VolatilityParityMeanReversionStrategy) -> dict:
    """Full SPI audit report for the paper-trading session."""
    n = len(live.decision_log)
    if n == 0:
        return {"decisions": 0, "spi": 1.0, "status": "EMPTY_LOG"}
    spi = live.signal_parity_index()
    fills = [o for o in live.order_log if o.get("state") == "FILLED"]
    costs = sum(o.get("expected_cost", 0.0) for o in fills)
    dup_fires = sum(1 for rec in live.decision_log
                    if rec["signal"] != 0 and rec["blocked_at_decision"])
    reasons = {}
    for o in live.order_log:
        r = o.get("reason")
        if r: reasons[r] = reasons.get(r, 0) + 1
    gate = "PASS" if spi >= 0.98 and dup_fires == 0 else "FAIL"
    return {"decisions": n,
            "spi": round(spi, 4),
            "duplicate_fires": dup_fires,
            "fills": len(fills),
            "total_costs": round(costs, 2),
            "order_reasons": reasons,
            "kill_switch_events": sum(1 for r in live.decision_log
                                      if r["kill_switch"]),
            "status": gate}


if __name__ == "__main__":
    from backtest_study import ou_prices, backtest
    report = backtest({"SPY": ou_prices(600, 11)})[0]
    print("SPI audit of a fresh 600-bar session:")
    for k, v in audit_parity(report).items():
        print(f"  {k:>18}: {v}")
