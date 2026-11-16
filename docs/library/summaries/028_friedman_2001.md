# 028 — Greedy Function Approximation: A Gradient Boosting Machine (Friedman, 2001)

**Venue:** Annals of Statistics | **Category:** Statistical learning & causality
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
The founding paper of gradient boosting: stagewise fitting of weak
learners (typically shallow trees) to the negative gradient of a
loss function, with shrinkage, subsampling (stochastic gradient
boosting), and the role of interaction depth. Establishes the
bias-variance mechanics that make boosted trees the default
tabular-data model in finance and beyond.

## The math that matters
$h_m(x) = \arg\min_h \sum_i L\left(y_i, F_{m-1}(x_i) + h(x_i)\right)$
approximated by fitting to pseudo-residuals
$g_i = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F=F_{m-1}}$;
update $F_m = F_{m-1} + \nu\, h_m$ with learning rate $\nu$.

## Why it matters for the L2 project
If the C7/C8 models use boosted trees on the panel, every
hyperparameter ($\nu$, depth, subsample) is a trial for DSR
deflation. Boosting's appetite for interactions is exactly what the
vol-tautology check (K1) guards against: the tree finds the vol
factor under six names.

**Caveat:** Verify against library source before production.
