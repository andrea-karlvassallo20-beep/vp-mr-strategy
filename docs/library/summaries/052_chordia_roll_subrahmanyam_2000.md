# 052 — Commonality in Liquidity (Chordia, Roll & Subrahmanyam, 2000)

**Venue:** Journal of Financial Economics | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper; catalogue notes author-record discrepancy to verify).

## Summary
Liquidity is systematic: changes in quoted spreads, depths, and
order-imbalance are cross-sectionally correlated across stocks and
co-move with market-wide liquidity factors. Individual-asset
liquidity has a strong market (and industry) component —
liquidity dry-ups are common phenomena, not idiosyncratic.

## The math that matters
Market-model style regressions:
$\Delta L_{it} = \alpha_i + \beta_i\,\Delta L_{Mt} + \gamma_i
\Delta L_{ind,t} + \epsilon_{it}$, with average
$R^2$ and significant common $\beta$ across proxies (spread,
depth, order flow).

## Why it matters for the L2 project
Perps L2 features will share a market-wide liquidity factor (BTC
leading everything). If C8's micro state is dominated by a common
factor, cross-sectional claims about individual instruments
require residualizing against the market book state — the same
lesson as the C7 vol factor, one level down.

**Caveat:** Verify against library source before production.
