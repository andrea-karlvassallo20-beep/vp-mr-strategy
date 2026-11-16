# 017 — Market Microstructure: Microfoundations, Empirical Results, Policy Implications (Biais, Glosten & Spatt, 2005)

**Venue:** Journal of Financial Markets | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
A state-of-the-field review centered on limit-order markets, where
most modern trading happens: the limit order book as a queueing
system, price priority and time priority, the strategic choices
between providing liquidity (limit) and demanding it (market),
and the empirical regularities (intraday volume/volatility U-shape,
spread dynamics, order placement around the touch). Connects the
classic asymmetric-information models to the reality of electronic
books.

## The math that matters
Queueing dynamics: best-quote depth $q(t)$ evolves as a birth-death
process with limit arrivals $\lambda$, cancels $\mu_c$, and market
orders $\mu_m$; price changes occur at hitting times of the queue
($q \to 0$), which is the mechanism CKS's OFI linearizes.

## Why it matters for the L2 project
The L2 data IS a limit-order book: the gate criteria (mid/depth
agreement with snapshots) and the C8 micro features (OFI, depth,
queue depletion) should be interpreted through this queueing lens —
price moves are queue-exhaustion events, and OFI is the linearized
rate of approach to exhaustion.

**Caveat:** Verify against library source before production.
