# 065 — Double/Debiased Machine Learning for Treatment and Structural Parameters (Chernozhukov et al., 2018)

**Venue:** Econometrics Journal | **Category:** Statistical learning & causality
**Status:** Downloaded legally (arXiv:1608.00060); full text: `docs/library/text/065_chernozhukov_et_al.txt`.

## Summary
The DML framework: estimate a treatment effect with ML nuisance
models by (1) Neyman-orthogonal moment conditions that are
first-order insensitive to nuisance error, and (2)
cross-fitting (split the sample, train nuisances on one fold,
evaluate on the other). Together these remove the
regularization bias of naive plug-in ML and give root-n valid
inference on the structural parameter.

## The math that matters
Partially linear model $Y = D\theta_0 + g_0(X) + U$; orthogonal
score $\psi(W;\theta, \eta)$ with $\eta = (g, m)$,
$\hat\theta = \frac{\sum (D - \hat m(X))(Y - \hat g(X))}{\sum
(D - \hat m(X))D}$ — the residual-on-residual regression; the
score's Neyman orthogonality
$\partial_\eta E[\psi]_{\eta_0} = 0$ kills first-order nuisance
bias.

## Why it matters for the L2 project
The honest way to measure C8's interaction: the "effect of the
micro state given the macro state" is a treatment-like parameter
with high-dimensional confounders (the vol factor, the market
book factor). The repo already has
`src/dml_orthogonalizer.py`; C8's uplift estimate should be the
cross-fit, orthogonalized reading, not a raw conditional mean
difference.

**Caveat:** Verify page numbers against the extracted text
before production.
