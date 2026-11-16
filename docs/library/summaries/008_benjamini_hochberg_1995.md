# 008 — Controlling the False Discovery Rate (Benjamini & Hochberg, 1995)

**Venue:** Journal of the Royal Statistical Society B | **Category:** Backtesting & FML
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Replaces the family-wise error rate (FWER) with the **false discovery
rate**: the expected proportion of false rejections among all
rejections. Controlling FWER at level $\alpha$ when testing hundreds
of features kills power; controlling FDR allows the researcher to make
some false discoveries in exchange for many true ones, at a known
rate. The BH procedure is a one-line sorting rule and is the default
multiple-testing control in modern genomics and ML research.

## The math that matters
Sort p-values $p_{(1)} \le \dots \le p_{(m)}$; find the largest $k$
with $p_{(k)} \le \frac{k}{m}\alpha$; reject the hypotheses
corresponding to $p_{(1)},\dots,p_{(k)}$. This controls
$FDR = E[V/R]$ at $\alpha$ under independence (and proven valid under
some dependence).

## Why it matters for the L2 project
When C8 scans many (macro state x micro state) combinations, the
per-combination p-values should be BH-adjusted before any cell of the
board is called a hit. The board heat-map work already needs this; C8
must not read raw p-values.

**Caveat:** Verify against library source before production.
