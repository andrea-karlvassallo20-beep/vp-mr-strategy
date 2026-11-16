# 050 — A Simple Implicit Measure of the Effective Bid-Ask Spread (Glosten & Harris, 1988)

**Venue:** Journal of Finance | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Estimates the effective spread from transaction data alone by
regressing price changes on trade-sign indicators and signed
volume. Decomposes the spread into a fixed (order-processing)
component $z$ and a size-dependent (adverse-selection) component,
with the classic result that transitory and permanent components
can be separated by the Roll/GH structure.

## The math that matters
$\Delta P_t = z_0 (Q_t - Q_{t-1}) + z_{1/2}(V_t Q_t -
V_{t-1}Q_{t-1}) + c_0 Q_t + c_{1/2} V_t Q_t + \epsilon_t$ with
$Q_t \in \{\pm1\}$ trade sign, $V_t$ size; the spread components
are $2z$ (transitory) and $2c$ (permanent/adverse-selection).

## Why it matters for the L2 project
The trade-sign regression is the cheap baseline for impact
estimation when full L2 depth is unavailable; on the perps panel
it gives a per-instrument Kyle-type lambda from trades alone,
which C8 can use to cross-validate the book-based OFI lambda.

**Caveat:** Verify against library source before production.
