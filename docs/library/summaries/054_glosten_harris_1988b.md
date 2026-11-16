# 054 — Inferring Trade Direction from Intraday Data (Glosten & Harris, 1988 record)

**Venue:** Journal of Finance | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper; catalogue flags this as a variant record of 050 — verify).

## Summary
The trade-classification side of the Glosten-Harris program:
assigning trade sign (buyer- vs seller-initiated) from quote and
price data, the prerequisite for effective-spread and impact
estimation. The tick rule and quote rule (later formalized as
Lee-Ready) classify trades; misclassification biases spread and
impact estimates toward zero.

## The math that matters
Tick rule: $Q_t = \text{sign}(P_t - P_{t-1})$ (with
$\text{sign}(P_t - \text{mid}_t)$ as quote rule when quotes are
available); effective spread estimate $S = 2|P_t - m_t|$
averaged over classified trades.

## Why it matters for the L2 project
On the Tardis trades feed, side is given, but the perps panel's
trade-based features (VPIN, imbalance) inherit classifier error
wherever classification is inferred. C8's feature documentation
must state which features use exchange-provided side vs inferred
side.

**Caveat:** Verify against library source before production;
verify the intended identity of this record against 050.
