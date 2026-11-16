# 030 — Regression Shrinkage and Selection via the Lasso (Tibshirani, 1996)

**Venue:** Journal of the Royal Statistical Society B | **Category:** Statistical learning & causality
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
The lasso: minimize residual sum of squares subject to an
$L_1$ bound on the coefficients, which both shrinks and selects —
coefficients hit exactly zero, giving sparse linear models. Solves
the "many correlated predictors" problem by picking (arbitrarily,
among collinear twins) a small subset.

## The math that matters
$\hat\beta = \arg\min_\beta \frac{1}{2}\|y - X\beta\|_2^2
\quad\text{s.t.}\quad \|\beta\|_1 \le t$;
soft-thresholding in the orthogonal case:
$\hat\beta_j = \text{sign}(\hat\beta^{LS}_j)\,(|\hat\beta^{LS}_j| - \lambda)^+$.

## Why it matters for the L2 project
Two-edged for C8: selection under collinearity means a lasso may
pick ONE of the six vol names and drop the other five — useful for
the tautology audit, but the choice among collinear twins is
arbitrary and must not be read as "the true feature".

**Caveat:** Verify against library source before production.
