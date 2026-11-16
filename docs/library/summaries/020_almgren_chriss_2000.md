# 020 — Optimal Execution of Portfolio Transactions (Almgren & Chriss, 2000)

**Venue:** Journal of Risk | **Category:** Price impact & execution
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
The canonical execution model: liquidate $X$ shares over $N$ slices
in a market with linear temporary and permanent impact. The
trader minimizes the mean-variance objective over the trade
schedule; the solution is a family of efficient frontiers between
fast (high impact, low timing risk) and slow (low impact, high
timing risk) execution, parameterized by risk aversion $\lambda$.
The famous special cases are the TWAP schedule (risk-neutral) and
an exponential front-loaded decay (risk-averse).

## The math that matters
Price process with permanent impact $\gamma$ and temporary impact
$\eta$ (plus fee term $\tilde\eta$): total cost mean
$E[X] = \tfrac12 \gamma X^2 + \tilde\eta X^2 + \varepsilon^2(\eta -
\tfrac14 \gamma)X^2/T$-type variance
$\tfrac{\sigma^2 X^2}{2N}$-scaled terms; efficient frontier
$\sigma^2 = \tilde\lambda E^2$-type relation. Key: permanent
impact coefficient $\gamma$ is Kyle's lambda in disguise.

## Why it matters for the L2 project
If C8 ever moves from measurement to execution, the cost model
(Kyle's lambda as permanent impact, spread/fees as temporary) is
the bridge between a signal and a fillable strategy.

**Caveat:** Verify against library source before production.
