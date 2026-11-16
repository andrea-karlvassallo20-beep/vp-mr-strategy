# 010 — Trading Is Hazardous to Your Wealth (Barber & Odean, 2000)

**Venue:** Journal of Finance | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Six years (1991–1996) of brokerage account data for 66,465
households: the most active traders earn annual net returns 6.5
percentage points below the market, while the least active beat it by
1.0 point after costs. Overtrading is driven by overconfidence, and
transaction costs turn modest gross underperformance into large net
underperformance. The paper is the canonical evidence that activity
itself, not information, drives retail volume.

## The math that matters
Net return decomposition: $R^{net} = R^{gross} - 2 \cdot \text{turnover}
\cdot c$, where $c$ is the per-trade cost; the cost term dominates the
gross skill term for high-turnover accounts.

## Why it matters for the L2 project
The cost discipline: any C8 result must survive a per-trade cost
assumption before it means anything. The project's perps have
taker fees and spread costs; a signal whose edge is smaller than
round-trip cost is a Barber-Odean account, not a strategy.

**Caveat:** Verify against library source before production.
