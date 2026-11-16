# 016 — Market Microstructure: A Survey (Madhavan, 2000)

**Venue:** Journal of Financial Markets | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
The standard survey of the field as of 2000: price formation under
asymmetric information (Glosten-Milgrom, Kyle), inventory models
(Amihud-Mendelson, Ho-Stoll), the empirical spread decompositions,
limit-order markets, and market design (call vs continuous,
transparency). Organizes the literature around one question: how do
prices come to reflect information when trading is costly and
information is dispersed?

## The math that matters
The unifying structure: quotes are conditional expectations
$P = E[V \mid \Omega]$ where $\Omega$ includes the order flow
history; spreads decompose into adverse-selection
$\frac{1}{2}\,\text{spread}^{ad} = \alpha\, (V - E[V])$-type terms,
inventory terms, and processing costs (per Roll, Glosten-Harris,
Stoll).

## Why it matters for the L2 project
The map of the territory: every L2 feature the project builds
(OFI, imbalance, depth, spread) corresponds to a term in this
decomposition. The survey keeps the C8 feature set honest about
which economic quantity each feature is proxying.

**Caveat:** Verify against library source before production.
