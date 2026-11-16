# 044 — Wasserstein GAN (Arjovsky, Chintala & Bottou, 2017)

**Venue:** ICML / arXiv:1701.07875 | **Category:** Change-point & shift
**Status:** Downloaded legally (arXiv:1701.07875); full text: `docs/library/text/044_arjovsky_chintala_bottou.txt`.

## Summary
Replaces the Jensen-Shannon divergence in GAN training with the
Wasserstein-1 distance, which is continuous and informative even
when the supports of the two distributions are disjoint (where JS
saturates). Introduces the Kantorovich-Rubinstein duality: the
 Wasserstein distance becomes a supremum over 1-Lipschitz critics,
enforced by weight clipping. Training becomes far more stable and
the loss meaningful as a distributional distance.

## The math that matters
$W(P_\theta, P_r) = \sup_{\|f\|_L \le 1} E_{x \sim P_r}[f(x)] -
E_{x \sim P_\theta}[f(x)]$ (Kantorovich-Rubinstein duality);
the training objective alternates maximizing this over critic
parameters and minimizing it over generator parameters.

## Why it matters for the L2 project
Two uses: (1) the KR duality is the practical way to estimate
distributional distance between book states in high dimension;
(2) the paper's core lesson — use a distance that is informative
when distributions barely overlap — applies to regime detection
between a quiet book and a stressed one.

**Caveat:** Verify page numbers against the extracted text before
production.
