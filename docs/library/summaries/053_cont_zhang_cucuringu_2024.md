# 053 — Cross-Impact of Order Flow Imbalance in Equity Markets (Cont, Zhang & Cucuringu, 2024)

**Venue:** preprint (arXiv) | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (preprint; `src/library_acquire.py` verifies the latest arXiv version).

## Summary
Extends single-asset OFI to a cross-asset impact matrix: order
flow imbalance in one asset moves prices in correlated assets, and
the cross-impact matrix improves price-change prediction beyond
own-asset OFI. Uses multi-asset regression with regularization on
the cross-impact coefficients.

## The math that matters
$\Delta \mathbf{P}_n = \Lambda\, \mathbf{e}_n + \epsilon_n$ with
$\mathbf{e}_n$ the vector of per-asset OFIs and $\Lambda$ the
cross-impact matrix (own-impact on the diagonal); estimation by
(ridge-type) regression with sparsity/positivity structure on
$\Lambda$.

## Why it matters for the L2 project
Directly relevant: the perps panel is a cross-asset book system
with BTC/ETH leadership. Cross-impact generalizes the C8 micro
state from "own OFI" to "own + leader OFI" — and the
`lead_btc`/`lead_eth` features in the C7 panel are the OHLCV
shadow of exactly this structure.

**Caveat:** Verify against library source before production.
