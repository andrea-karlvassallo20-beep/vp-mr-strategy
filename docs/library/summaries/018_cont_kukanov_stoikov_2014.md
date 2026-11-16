# 018 — The Price Impact of Order Book Events (Cont, Kukanov & Stoikov, 2014)

**Venue:** Journal of Financial Econometrics 12(1):47-88 | **Category:** Microstructure & order flow
**Status:** Downloaded legally (arXiv:1011.6402v3); full text: `docs/library/text/018_cont_kukanov_stoikov.txt`.
**Page citations below are arXiv v3 PDF pages.**

## Summary
The OFI paper. Using NYSE TAQ data for 50 stocks, the authors show
that over short windows, mid-price changes are driven mainly by the
**order flow imbalance** — the net change in signed size at the best
quotes — and that the relation is linear: $\Delta P = \beta\, OFI +
\epsilon$, with $R^2$ averaging 65%, the slope $\beta$ inversely
proportional to depth, and stability across stocks and time scales
(window sizes 10s to 30s+). Trade volume-based measures are noisier
and less robust than OFI. A scaling argument derives the observed
square-root law between price changes and volume from the linear
OFI model.

## The math that matters (with page cites)
- OFI event decomposition at the best quotes (arXiv PDF **pp. 3-4**,
  Eqs. 2.2-2.4): bid/ask order flow from price-change indicators.
- Linear impact model (arXiv PDF **p. 6**): $\Delta P_k = \beta\,
  OFI_k + \epsilon_k$ with $\beta$ the price impact coefficient.
- Deeper levels (arXiv PDF **p. 16**, appendix): order flow at five
  levels adds only marginal explanatory power.
- Scaling/square-root (arXiv PDF **pp. 19-20**): noisy scaling
  relation, slope $\theta_k = \beta_i \epsilon_k \sigma\sqrt{\varepsilon\pi}$.

## Why it matters for the L2 project
OFI is the micro state of C8. The full formulas and executable
Python are in `docs/math_cheatsheet.md` (Section 1); the extracted
PDF text allows every formula there to be checked against the
source page by page.
