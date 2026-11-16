# 013 — A Dynamic Theory of the Bid-Ask Spread (Glosten & Milgrom, 1985)

**Venue:** Journal of Financial Economics | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Bid-ask spreads exist even without inventory costs or fixed costs:
they are the rational response to adverse selection. A market maker
faces traders who may be informed; if she quotes mid, informed
traders take the profitable side every time and she loses. The
equilibrium spread is exactly wide enough that expected losses to
informed traders are covered by expected gains from uninformed
("noise") traders.

## The math that matters
With informed fraction $\pi$, signal precision, and values
$V_{high}/V_{low}$, quotes solve
$E[V \mid \text{buy at ask}] = \text{ask}$ and
$E[V \mid \text{sell at bid}] = \text{bid}$; the spread widens in
$\pi$ and in signal precision, and can be so wide that no trade
occurs (market collapse).

## Why it matters for the L2 project
The spread on the L2 book is an adverse-selection meter. C8's
micro state should treat widening spreads and depth withdrawal as
the book "knowing" something; the Glosten-Milgrom mechanism is the
theory behind the OFI-to-impact link (CKS) and behind VPIN's claim
that flow toxicity predicts liquidity withdrawal.

**Caveat:** Verify against library source before production.
