# 009 — The Probability of Backtest Overfitting (Bailey, Borwein, Lopez de Prado & Zhu, 2017)

**Venue:** Journal of Computational Finance | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
The PBO framework: run a strategy search under combinatorial purged
cross-validation (CPCV), rank each configuration's performance in
every fold, and measure how often the configurations that were best
in-sample end up below median out-of-sample. PBO is the probability
that the selected strategy underperforms the median OOS — a direct,
interpretable overfitting gauge that does not rely on distributional
assumptions.

## The math that matters
For each CPCV path, compute the rank $\omega_{n,\phi}$ of the chosen
configuration $n^*$ among all $N$ configurations on the $\phi$-th
validation path, mapped to $(0,1)$ via
$\omega_{n,\phi} = \frac{rank_{n,\phi}}{N} - \frac{1}{2N}$. Then
$\text{PBO} = \int_{-\infty}^{0} f(\omega) d\omega$, the mass of the
rank distribution below the median.

## Why it matters for the L2 project
C8's threshold search (which branching-ratio cutoff, which OFI
quantile) is exactly a configuration search. PBO over the CPCV paths
is the right summary of how much of C8's tuning is curve-fitting; a
PBO above 0.5 kills.

**Caveat:** Verify against library source before production.
