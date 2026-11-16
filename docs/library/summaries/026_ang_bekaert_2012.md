# 026 — Regime Changes and Financial Markets (Ang & Bekaert, 2012)

**Venue:** Annual Review of Financial Economics | **Category:** Regime switching & state-space
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
A review of regime-switching evidence in asset returns: bear regimes
with high volatility and crashes, regime-dependent correlations
(which rise in bear markets), international diversification benefits
that shrink exactly when needed, and the asset-allocation
consequences. Emphasizes that regime models capture the
non-normality of returns (crash risk) that single-state models
must otherwise handle with fat-tailed innovations.

## The math that matters
Regime-conditional moments drive allocation:
$E[R]$ and $\text{Cov}(R)$ are probability-weighted mixtures;
portfolio choice solves a dynamic program with
$V(W, s)$ depending on the regime.

## Why it matters for the L2 project
Supports the C8 premise that a macro regime label can change the
distribution of outcomes, not just their mean — but also warns that
regime-conditional estimates are noisy with few regime episodes.
C8's kill lines must demand regime reproduction in both validation
years precisely because regime samples are small.

**Caveat:** Verify against library source before production.
