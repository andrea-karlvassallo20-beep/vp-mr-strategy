# 019 — A User's Guide to Optimal Transport (Peyre & Cuturi, 2019)

**Venue:** arXiv:1904.03429 | **Category:** Optimal transport
**Status:** Downloaded legally (arXiv:1904.03429); full text: `docs/library/text/019_peyre_cuturi.txt`.

## Summary
The shorter, pedagogical companion to 011: discrete OT as linear
programming, the geometry of the simplex of coupling matrices,
entropy-regularized OT and Sinkhorn iterations, convergence
properties, and computational tricks (log-domain stabilization,
Greenkhorn, screening). Aimed at practitioners who need to compute
OT distances fast on real data.

## The math that matters
Sinkhorn in the log domain: $f \leftarrow \varepsilon \log a -
\varepsilon\, \text{LSE}\left(\frac{f' - C}{\varepsilon}\right)$
(and symmetrically for $g$), numerically stable for small
$\varepsilon$; the regularized cost converges to the true OT cost as
$\varepsilon \to 0$.

## Why it matters for the L2 project
The implementation reference for the Wasserstein change detector:
if C8 or the WATCH lead uses $W_1$ between book-feature
distributions across a 30m boundary, this is the numerically stable
way to compute it at scale.

**Caveat:** Verify against library source before production.
