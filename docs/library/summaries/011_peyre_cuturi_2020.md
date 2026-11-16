# 011 — Computational Optimal Transport (Peyre & Cuturi, 2020)

**Venue:** Foundations and Trends in Machine Learning | **Category:** Change-point & shift
**Status:** Downloaded legally (arXiv:1803.00567); full text: `docs/library/text/011_peyre_cuturi.txt`.

## Summary
The modern reference on OT: Kantorovich's linear program, the
Wasserstein distances $W_p$, and — the paper's central contribution to
practice — **entropy-regularized OT** and the Sinkhorn algorithm,
which turns a quadratic assignment problem into an iterated
matrix-scaling that is GPU-friendly and differentiable. Also covers
Wasserstein barycenters, gradient flows, and the use of OT as a loss
in ML.

## The math that matters
$W_p(\mu, \nu)^p = \min_{\gamma \in \Pi(\mu,\nu)} \int \|x-y\|^p d\gamma$;
entropic relaxation
$L_C^\varepsilon(\mu,\nu) = \min_\gamma \langle C, \gamma \rangle +
\varepsilon \, \text{KL}(\gamma)$, solved by Sinkhorn scaling
$u \leftarrow a / (Kv)$, $v \leftarrow b / (K^T u)$ with
$K = e^{-C/\varepsilon}$. Sinkhorn divergence
$\bar W_\varepsilon = L^\varepsilon_C - \tfrac{1}{2}L^\varepsilon_C(\mu,\mu) - \tfrac{1}{2}L^\varepsilon_C(\nu,\nu)$
removes the entropic bias.

## Why it matters for the L2 project
WATCH-style change detection (paper 043) compares pre/post-event
distributions of book features; the Wasserstein distance is the right
metric for distribution shift when mean/variance tests are blind to
shape change. Sinkhorn makes it computable per 30m bar.

**Caveat:** Verify against library source before production (page
numbers for the Sinkhorn section: see extracted text, ch. 4).
