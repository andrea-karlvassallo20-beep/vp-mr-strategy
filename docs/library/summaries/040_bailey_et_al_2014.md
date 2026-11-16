# 040 — The Expected Returns of All Trading Strategies (Bailey, Borwein, Lopez de Prado & Zhu, 2014)

**Venue:** Journal of Computational Finance | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Selection bias at the level of the research enterprise: for any
investor and any horizon, among the (astronomically many) possible
strategies, some subset will have shown spectacular performance by
chance. The paper derives the distribution of the maximum expected
return achievable across the space of all strategies, showing that
"discovered" exceptional backtests are guaranteed by combinatorics
alone.

## The math that matters
For strategy space size $N$ and performance dispersion $\sigma$,
the expected maximum Sharpe grows as
$\sqrt{V[SR]} \cdot \Phi^{-1}(1 - 1/N)$; the Sharpe inconsistency
argument shows nominal Sharpe cannot exceed
$\sqrt{1/\min(\text{holding period})}$-type bounds from trade
frequency and non-normality.

## Why it matters for the L2 project
The philosophical anchor of the ledger: extraordinary claims
require extraordinary deflation. C8's reading will be judged
against the everything-search it emerged from, not against the
beauty of the hypothesis.

**Caveat:** Verify against library source before production.
