# 058 — Trade Co-occurrence, Trade Flow Decomposition and Conditional Order Imbalance (Lu, Reinert & Cucuringu, 2024)

**Venue:** Quantitative Finance | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper; arXiv version may exist — script verifies).

## Summary
Decomposes order flow by trade co-occurrence structure: which
trades happen together (in time or across venues), how aggregate
flow splits into components (informed/uninformed-like clusters),
and how order imbalance conditioned on the co-occurrence state
predicts short-horizon price moves. Uses graph/statistical
decomposition tools on the trade string.

## The math that matters
Flow decomposition: signed flow $F = \sum_c \pi_c F_c$ over
co-occurrence components $c$ (spectral/graph partition of the
trade co-occurrence matrix); conditional imbalance
$OI \mid c$ and its predictive regression onto $\Delta P$.

## Why it matters for the L2 project
A candidate enhancement of the micro state: instead of aggregate
OFI/imbalance per bucket, condition on the trade-cluster state.
For C8 this is a documented future extension, not part of the
pre-registered micro state.

**Caveat:** Verify against library source before production.
