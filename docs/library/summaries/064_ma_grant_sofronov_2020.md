# 064 — Multiple Change Point Detection and Validation in Autoregressive Time Series (Ma, Grant & Sofronov, 2020)

**Venue:** Statistical Papers | **Category:** Regime switching & state-space
**Status:** Downloaded legally (Springer OA PDF via OpenAlex); full text: `docs/library/text/064_ma_grant_sofronov.txt`.

## Summary
Methods for detecting MULTIPLE change points in autoregressive
series: dynamic programming and genetic-algorithm segmentation
with AR-segment likelihoods, model-selection criteria (BIC-type
penalties) for the number of changepoints, and validation of
detected segments. Targets series where both the AR parameters
and the innovation variance may shift.

## The math that matters
Segment cost $-\ell(\hat\theta_s; y_{[a,b]})$ minimized over
partitions with penalty $\beta\,\#\{\text{changepoints}\}$:
$\min_{\tau_1 < \dots < \tau_K} \sum_k -\ell_k + \beta K$;
AR-segment likelihood recursions allow $O(n^2)$ DP.

## Why it matters for the L2 project
The macro timeline construction: the project's era/epoch
boundaries and the C7 "quiet" windows are change-point
segmentations. A principled, penalized detector (this paper's
framework) is the defensible alternative to eyeballed eras —
and the era boundaries feed the split manifest, so they must not
be tuned to the answer.

**Caveat:** Verify against library source before production.
