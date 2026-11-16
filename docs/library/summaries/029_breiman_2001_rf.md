# 029 — Random Forests (Breiman, 2001)

**Venue:** Machine Learning | **Category:** Statistical learning & causality
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Ensembles of de-correlated decision trees: bootstrap samples per
tree, random feature subsets per split, majority vote / averaging.
Breiman shows the generalization error converges as the number of
trees grows, driven by the strength of individual trees and the
correlation between them; introduces the out-of-bag (OOB) error and
variable importance measures.

## The math that matters
PE* $\to \rho\,(1-s^2)/s^2$-type limit: forest error decreases with
tree strength $s$ and increases with inter-tree correlation
$\rho$; OOB error gives an honest internal validation without a
held-out set.

## Why it matters for the L2 project
OOB is a free CPCV-like check for panel models; and variable
importance, used carelessly on a panel with a dominant factor,
re-creates the vol-tautology problem (six correlated features share
the importance). C8's feature accounting must handle importance
inflation under correlated features.

**Caveat:** Verify against library source before production.
