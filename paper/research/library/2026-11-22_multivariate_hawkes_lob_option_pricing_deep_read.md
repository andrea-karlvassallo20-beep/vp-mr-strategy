# Deep-read note 91: "Multivariate Hawkes-based Models in LOB: European, Spread and Basket Option Pricing"

Deep-read session 91 (null-time session 101, log ## 120). Qi Guo, Anatoliy
Swishchuk, Bruno Rémillard (University of Calgary; HEC Montréal), 2022,
arXiv:2209.07621v1 — a theory-assembly paper that prices European, spread and
basket options off a mid-price modeled as a multivariate general compound
Hawkes process (MGCHP), exponentiated (EMGCHP) to keep prices positive, pushed
through LLN/FCLT diffusion limits into geometric Brownian motion, and closed
under Black-Scholes / Margrabe / Gentle-basket formulas, ending in an
"implied order flow" construction.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xaace1f_multivariate_hawkes_based_models_in_lob_european_s.txt,
28 pp., page-marked). Next UNREAD triage-rank entry (score 20).

## The paper in one paragraph

The mid-price is the Hawkes-count sum of Markov-chain jump sizes,
S_{i,t} = S_{i,0} + sum_{k<=N_{i,t}} a(X_{i,k}) with independent per-asset
Hawkes processes of exponential excitation (eqs. 1-3, PDF pp. 2-3). Because
that process is not bounded below, prices are exponentiated into the EMGCHP
A_{i,t} = exp(S_{i,t}) (Definition 3.1, PDF p. 3). LLN and two FCLTs (stochastic
centralization conditioned on the realized count, deterministic centralization
conditioned on the intensity) are stated for the exponential version (Theorems
3.2-3.7, PDF pp. 4-8), the honest caveat being that the stochastic version
"cannot provide us a model for prediction tasks since we cannot observe the
order flow N_t in advance" (PDF p. 6). The deterministic-centralization limit
yields, for large n, a multivariate geometric Brownian motion (eqs. 20-21,
PDF pp. 6-7), and the paper then prices a European call by a Girsanov change
into a Black-Scholes PDE whose volatility is the Hawkes/Markov composite
(eqs. 29-33, PDF pp. 9-10), computes greeks including the flow-operator
sensitivities c_{σ*}, c_{a*}, c_{μ̂} (eqs. 34-39, PDF pp. 12-13), prices
Margrabe spread options on two Hawkes assets and on one 2D EMGCHP with
model-endogenous correlation ρ (Sections 5-6, PDF pp. 15-21), prices a three-
stock basket by Gentle's geometric-average approximation (Section 7, PDF
pp. 21-24), writes the minimal hedge (Section 8, PDF pp. 24-26), and closes
with the "implied order flow" inversion: since the limiting volatility
decomposes as σ̂² = σ*²E(N_t) + a*²Var(N_t) (eqs. 41, 45, PDF pp. 13-14), an
option-implied volatility plus "some estimation about α/β" can be re-split
into implied expectation and variance of the order flow (eqs. 44-47, PDF
pp. 14-15), which the authors advertise as "more market forecast information
than the classical Black-Scholes model" (PDF pp. 1, 14, 26-27). Every
numerical example uses invented parameters, with no data fit anywhere
(PDF pp. 10, 18, 21, 23-26), and the implied-flow simulation is circular:
"Since we don't have actual high frequency option data, we applied the
option values computed from Figure 1" (PDF p. 14).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

  1. [reinforcing, no new item] The option price is nearly flat in α/β at
     small values and explodes as α/β → 1 (Figure 2, PDF pp. 10-11): any
     Hawkes-adjacent statistic is acutely sensitive to the memory ratio near
     criticality, so the branching/memory configuration and the distance from
     spectral radius 1 are research degrees of freedom that could manufacture
     a "regime" or "stress" result by post-hoc re-tuning. This reinforces the
     estimator-configuration freeze (deep-read 63) and the self-excitation
     regime-window pre-declaration (deep-read 53): distance-from-criticality
     counts as frozen configuration, not a free dial. No queue change.

  2. [reinforcing, no new item] The paper states in print that the
     count-conditioned limit "cannot provide us a model for prediction tasks
     since we cannot observe the order flow N_t in advance" (PDF p. 6), and
     prices only under the deterministic centralization (FCLT II, PDF pp.
     6-8): a flow-conditioned theoretical quantity must condition only on
     flow verifiably observable at the evaluation instant. This is the same
     availability discipline the same-period-aggregate feature availability
     rule (deep-read 84) and the cross-stream synchronization and
     single-source-count pre-declaration (#48, deep-read 89) already demand,
     now stated by a Hawkes pricing paper against its own theorem. No queue
     change.

  3. [candidate sharpening, PENDING OWNER RATIFICATION] The implied
     order-flow construction is an under-identified, circular inversion
     (eqs. 44-47, PDF pp. 14-15). One observed scalar (option-implied
     volatility, eqs. 42-43, PDF pp. 13-14) is algebraically split between
     two unknowns, E(N_t) and Var(N_t), through an analyst-supplied α/β or
     λ∞ taken from unspecified "historical estimation" (PDF p. 14) — the same
     observed σ̂²implied maps to a continuum of (E, Var) pairs as α/β
     varies, so the recovered "forecast information" is created by the
     split, not measured — and the numerical demonstration is explicitly
     circular, feeding the model's own computed option values back as the
     observed input (PDF p. 14). Queued proposed sharpening #49, the
     model-inversion identifiability pre-declaration: BEFORE the L0 gate,
     any C1-L2/C8-adjacent computation, comparator, null or feature that
     inverts a parametric model onto an observed quantity — implied
     volatility onto order-flow moments, a measured compression score onto
     a latent priming intensity, an observed spread onto a book-state
     parameter — must pre-declare, as frozen configuration counted in the
     multiplicity ledger: (i) which model parameters are FROZEN, and from
     where (a dated estimation source or a declared generic default), every
     deviation a dated amendment before the data is touched; (ii) an
     identifiability statement proving the observed quantity admits a
     unique split over the unknowns given the frozen set, or the inversion's
     reported quantity is declared under-identified with its null surfaces
     reported across the pre-declared frozen-set grid; and (iii) an
     input-provenance trace proving the "observed" input is not itself
     generated by the model family being inverted — a self-fed inversion
     (the paper's own Figures 4-5) is inadmissible at the gate. Harder to
     pass because a recovered latent quantity that can be re-split
     arbitrarily after seeing the data, or whose input is circularly
     model-generated, now fails by rule instead of surviving as an
     inverse-problem find. It tightens the estimator-configuration freeze
     (deep-read 63) by extending pre-commitment from WHICH estimator in
     WHICH configuration to the identifiability of the inversion's parameter
     split, and the dynamics-identification rule for generative nulls
     (null-time session 58) on the input-provenance axis; joins the
     noise-model pre-declaration (deep-read 76) in extending frozen
     configuration into the model-input chain. Full draft with the
     killed-if-wrong counterfactual below.

  4. [interpretation caution] The EMGCHP-to-GBM chain is a large-n
     trading-frequency asymptotic with uniform integrability of payoffs
     assumed for the pricing limit (PDF pp. 8-9), resting on a mid-price
     model that the authors themselves had to exponentiate to avoid
     non-positive prices (Definition 3.1, PDF p. 3). Any future L2-derived
     diffusion-limit input to a null or comparator is an asymptotic
     approximation to the book, not book law, and its magnitudes are banned
     from the record as support under the laundering rule. No queue change.

  5. [source-quality note] arXiv v1 preprint, companion to a PhD thesis
     (Guo 2022, PDF pp. 2, 28); no empirical calibration anywhere — every
     parameter list is invented (PDF pp. 10, 18, 21, 23); and the paper
     carries internal defects: the text labels the diffusion approximation
     (eq. 20) as the "solution of equation (30)" (eq. 31, PDF p. 9), which
     is not the option-price solution; and it claims "Since Φ and φ are
     always non-negative, delta and theta are always positive" (PDF p. 12),
     contradicting its own theta formula (a negative-signed term, PDF p. 12)
     and classical option theory. Treat as ammunition on inversion
     identifiability and availability discipline only; check the published
     version before formal citation. No queue change.

## What this paper would have killed if we had done it wrong

Had the programme accepted an implied-volatility-to-order-flow inversion, or
any score-to-latent-intensity inversion, as a C8 input without an
identifiability gate, an apparent "flow forecast" could have been manufactured
after the fact by silently re-choosing the frozen-looking parameter (α/β
"from historical data") — a research degree of freedom the estimator-
configuration freeze does not catch, because the estimator here is exact; it
is the INVERSION that is under-determined. The paper demonstrates the failure
class in print: its own headline product (Figures 4-5, PDF pp. 15) is not a
measurement at all, being computed from option prices the same model
produced. The programme's existing discipline (falsification-first, the
laundering rule, the honest β-factor-bug record of the math verification)
is what would have caught this on the write side; the sharpening adds the
read-side gate so it never needs to.

## Standing caveat

The paper is pure theory assembly with invented parameters: no data, no fits,
no out-of-sample anything; the pricing sections inherit every assumption of
classical Black-Scholes/Margrabe plus the Hawkes/Markov structure, with a
risk-neutral change applied to a finite-horizon approximation; near-
criticality behaviour (α/β → 1) is explored only as a price surface, never
with empirical α/β levels, which matters because the diffusion plateau and
the explosion sit inside the same parameter the inversion needs frozen.
arXiv-version caution: check the published version before formal citation.
