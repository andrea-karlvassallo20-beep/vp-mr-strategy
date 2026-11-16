# 015 — Deep Order Flow Imbalance (Kolm, Turiel & Westray, 2023)

**Venue:** Mathematical Finance | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper; arXiv version may exist — `src/library_acquire.py` verifies by title search).

## Summary
Extends CKS's linear OFI-impact relation with deep learning: the
model consumes the raw limit-order-book state (multi-level depths
and prices) and predicts mid-price changes over multiple horizons,
learning the nonlinear aggregation that CKS's fixed linear
decomposition assumes away. The paper reports that learned
representations beat the hand-built OFI, especially at longer
horizons and for books where deeper levels matter.

## The math that matters
$\Delta P_{t+h} = f_\theta(\mathbf{X}_t) + \epsilon$, with
$\mathbf{X}_t$ the normalized multi-level book tensor; $f_\theta$ a
deep net trained with a classification loss on the sign/quantile of
$\Delta P$; benchmarked against $\Delta P = \lambda\, e_t + \epsilon$
(the CKS linear form).

## Why it matters for the L2 project
It is the ML ceiling for the L2 family: if linear OFI carries signal
in the perps panel, the deep version tells us how much nonlinearity
is left on the table. C8 uses linear/quantile OFI as the micro state;
015 bounds what we are leaving behind.

**Caveat:** Verify against library source before production.
