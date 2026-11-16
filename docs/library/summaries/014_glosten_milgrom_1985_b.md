# 014 — Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders (Glosten & Milgrom, 1985)

**Venue:** Journal of Financial Economics | **Category:** Microstructure & order flow
**Status:** Synthesized from LLM internal knowledge (Paywalled paper).

## Summary
Companion record to 013 — the same model, emphasizing the sequential
nature: trades arrive one at a time, the specialist updates beliefs
Bayesian-style after each trade, and quotes are conditional
expectations of value given the trade side. Price is a martingale
with respect to the specialist's information; the spread is the cost
of learning from order flow.

## The math that matters
$\text{ask}_t = E[V \mid \Omega_t, \text{buy}]$,
$\text{bid}_t = E[V \mid \Omega_t, \text{sell}]$; after a buy,
$\Omega_{t+1}$ updates by Bayes rule, and
$E[\text{mid}_{t+1} - \text{mid}_t \mid \Omega_t] = 0$ — no free
drift in the mid.

## Why it matters for the L2 project
The mid-price martingale property is the microstructure null the
project tests: features (OFI, imbalance) claim to predict mid
moves, which under GM is only possible if they carry information the
specialist has not yet impounded. The C8 gate should verify the
martingale baseline before crediting any micro feature.

**Caveat:** Verify against library source before production.
