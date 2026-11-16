# 046 — Flow Toxicity and Liquidity in a High-Frequency World (Easley, Lopez de Prado & O'Hara, 2012)

**Venue:** Review of Financial Studies | **Category:** HF data & intraday
**Status:** Synthesized from LLM internal knowledge (Paywalled paper; SSRN preprint exists — script verifies).

## Summary
The VPIN paper: measures order-flow toxicity — the rate at which
informed traders adversely select market makers — by sampling
trade data in the **volume clock** rather than the time clock,
aggregating into volume buckets, classifying each bucket's volume
into buy/sell fractions (bulk volume classification), and
computing the average absolute imbalance over a rolling window.
VPIN rose sharply before the 2010 Flash Crash, and market makers
who cut liquidity in response to high VPIN would have avoided the
worst of it. Contested later (Andersen-Bondarenko) — treat claims
critically.

## The math that matters
Bucket imbalance $OI_i = |V^{buy}_i - V^{sell}_i|/V_i$ with bulk
classification $V^{buy}_i = V_i \Phi(z_i)$, $z_i$ the standardized
price change over the bucket; $\text{VPIN} = \frac{1}{n}\sum_{i=1}^{n} OI_i$.
Full formulas and Python: `docs/math_cheatsheet.md` (Section 5).

## Why it matters for the L2 project
VPIN is the second micro-state candidate for C8 (with OFI and
Hawkes). On perps L2 data, volume buckets and bulk classification
are computable directly from trades + book updates.

**Caveat:** Verify against library source before production.
