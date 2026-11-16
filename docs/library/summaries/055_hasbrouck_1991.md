# 055 — Measuring the Information Content of Stock Trades (Hasbrouck, 1991)

**Venue:** Journal of Finance | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Vector autoregression of trade signs and quote revisions: the
long-run impact of a trade innovation on the mid-price measures
the trade's information content. Trades have large, permanent
effects (information); quote revisions have transitory effects
(inventory). Introduces the variance decomposition of price
changes into information (random-walk) and transitory components.

## The math that matters
VAR: $\mathbf{x}_t = \sum_{k=1}^p A_k \mathbf{x}_{t-k} +
\epsilon_t$ with $\mathbf{x} = (r^{mid}_t, Q_t V_t)'$; information
share = the random-walk component of the mid:
$\psi = \frac{\sigma^2_{\epsilon,1}}{...}$ from the Wold
representation — the fraction of mid-price variance attributable
to trade innovations.

## Why it matters for the L2 project
The VAR information-share is the econometric alternative to OFI
for measuring how much the flow moves the price permanently. If
C8's OFI impact coefficient is real, a Hasbrouck-style
decomposition on the perps book should agree on which instruments'
books are informative.

**Caveat:** Verify against library source before production.
