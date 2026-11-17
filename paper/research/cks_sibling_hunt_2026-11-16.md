# The CKS sibling hunt — the public-math family around our two pillars

Status: LITERATURE RECONNAISSANCE, 2026-11-16, written in null time while
T1 ran. Descriptive only: nothing here is a claim, a feature, or a
commitment. Each sibling is recorded with what it measures and whether it
threatens or upgrades our registered specs. The hunt was prompted by the
owner's directive (Task 3): if the edge is the combination of public
math, we should know the whole family the combination comes from.

## A. The OFI family (siblings of Cont, Kukanov & Stoikov 2014)

1. **Xu et al. (2019), "Multi-Level Order-Flow Imbalance in a Limit
   Order Book."** Extends CKS beyond the best quotes: per-level OFIs
   at depth m, regressed jointly. Finding: deeper levels add
   explanatory power beyond the best-level OFI. RELATION TO US: our
   C8 T-O trigger uses top-of-book OFI (the verified exact formula);
   CKS's own Appendix B3 found deeper levels add only marginal power,
   but this sibling disagrees. CANDIDATE (not registered): a
   multi-level OFI variant of T-O, only as a post-primary,
   multiplicity-taxed variant per K5. Not a threat to the primary.

2. **Cont, Cucuringu & Zhang (2023), "Cross-Impact of Order Flow
   Imbalance in Equity Markets" (arXiv:2112.13213).** The closest
   sibling. (a) Integrates multi-level OFIs via PCA into a single
   "integrated OFI" that beats best-level OFI out-of-sample;
   (b) contemporaneous CROSS-asset impact adds nothing once the
   integrated OFI is in the model; (c) LAGGED cross-asset OFI does
   improve short-horizon return forecasting, decaying rapidly.
   RELATION TO US: (b) is a warning against any future cross-asset
   OFI trigger (the one-instrument-first law already refuses it);
   (a) is the strongest documented upgrade path for T-O; (c) is
   short-horizon (HFT-scale) and does not occupy our 4h/24h cell.

3. **Capponi & Cont (2020)** — multi-asset order flow impact,
   in-sample antecedent of #2. Same reading.

4. **Crypto-LOB applications (2023-2026):** Hawkes-based crypto LOB
   forecasting (arXiv:2312.16190; return-sign prediction at the HFT
   clock) and multivariate-Hawkes Bitcoin LOB forecasting (Decisions
   in Economics and Finance, 2026). RELATION TO US: these occupy the
   MILLISECOND/second horizons on crypto books — exactly the cell we
   are NOT in. No sibling was found running OFI/Hawkes at a 4h/24h
   hazard horizon conditioned on a macro state. The C8 cell remains
   unoccupied by the public literature.

## B. The Hawkes family (siblings of Filimonov & Sornette 2012/2014)

1. **Hardiman & Bouchaud (2014), "Branching-ratio approximation for
   the self-exciting Hawkes process."** Nonparametric estimator of
   the branching ratio; documents that FS-style parametric MLE can be
   biased. RELATION TO US: supports the decision (already taken) to
   cross-validate our MLE against tick and an oracle — and offers a
   nonparametric CROSS-CHECK for the T-H trigger. CANDIDATE: a
   Hardiman-Bouchaud-style nonparametric branching estimate as a
   robustness column beside the MLE, not a replacement.

2. **Bacry, Mastromatteo & Muzy (2015), "Hawkes Processes in
   Finance."** The canonical review; nonparametric estimation
   (Bacry-Muzy). Same reading as B1.

3. **Achab, Bacry, Lillo & Muzy (2017, arXiv:1706.03411),
   "Analysis of order book flows using a nonparametric estimation of
   the branching ratio matrix."** Estimates the FULL branching-ratio
   MATRIX G non-parametrically on order-book event streams; finds
   inhibition effects short-lived and excitation dominant.
   RELATION TO US: our fit_hawkes2 estimates G = alpha/beta by
   constrained MLE; this is the nonparametric sibling for the same
   object. CANDIDATE robustness check for C8's rho(G) trigger.

4. **"Hawkes model specification for limit order books" (2020).**
   Documents that MLE branching estimates are significantly biased
   NEAR CRITICALITY. RELATION TO US: this is external, published
   support for C8's K7 — our boundary-constraint flag (rho >= 0.949
   fits are never reported as interior estimates) is exactly the
   guard this paper says the field needs. Our 0.8 trigger threshold
   sits below the critical zone, and the flag catches the zone.

5. **Rambaldi, Bacry & Lillo (2016-17)** — volume's role in book
   dynamics via multivariate Hawkes; **Large (2007)** and
   **Wu, Rambaldi, Muzy & Bacry (queue-reactive Hawkes)** —
   state-dependent intensities. RELATION TO US: the 4D Hawkes (with
   cancellations) under the C5 gate is in this lineage; nothing to
   change in registry, context for the C5 spec.

6. **"Quantifying endogeneity of cryptocurrency markets" (Quantitative
   Finance, 2020).** Hawkes branching ratios ON Bitcoin, at the
   market level. RELATION TO US: confirms crypto endogeneity is
   measurable; operates at tick scale, not our hazard clock.

## C. Findings, condensed

- **No sibling occupies the C8 cell.** The family runs OFI and Hawkes
  at HFT horizons (ms to minutes), or macro states on OHLCV bars at
  daily clocks. The 4h/24h hazard on an L2 book, conditioned on a
  macro primed state, remains unoccupied public math. The combination
  hypothesis is still ours to test or die on.
- **The strongest upgrade path for T-O** is the integrated (PCA)
  multi-level OFI of Cont-Cucuringu-Zhang — but it enters only as a
  pre-registered, multiplicity-taxed variant after the primary, never
  as a post-hoc pivot (K5 discipline).
- **The strongest robustness path for T-H** is a nonparametric
  branching-matrix estimate (Hardiman-Bouchaud / Achab et al.) beside
  the MLE — a cross-check column, not a replacement.
- **K7 has published external support**: MLE branching bias near
  criticality is documented in the literature; our boundary flag is
  the correct guard, and the 0.8 trigger threshold stays below the
  biased zone.
- **A warning absorbed**: contemporaneous cross-asset OFI adds nothing
  once integrated OFI is in the model — one more reason the
  one-instrument-first law is not merely caution but the empirical
  shape of the family.

Nothing in this memo changes any registered spec, threshold, or kill
line. Candidates listed here enter the registry only through
pre-registration with kill lines of their own.
