# Library deep-read session 11 — Bergault, Bertucci, Bouba, Guéant &
# Guilbert, "Price-Aware Automated Market Makers: Models Beyond
# Brownian Prices and Static Liquidity" (arXiv:2405.03496v3, 2024;
# Dauphine/ILB/Swaap Labs; a suite of HJB market-making models for
# DeFi)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xd1af5a_price_aware_automated_market_makers_models_beyond_.txt`,
20 pp., page-marked). Next by triage rank (session 12's pointer),
under the triage-audit caveat.

## The paper in one paragraph

A suite of stochastic-control models for a price-aware AMM quoting
both sides of a crypto pool against a reference price, maximizing
expected excess PnL over the Hodl benchmark with a variance penalty
(PDF pp. 3-5). Price dynamics beyond log-normal: Heston-Bates
(stochastic variance + jumps), Stein-Stein with jumps, a simple
Markovian Hawkes pure-jump price whose intensity is excited by its
own jumps with n IN (0,1) "corresponding to the percentage of price
moves that are purely endogenous" (PDF p. 11), and a Z-Hawkes
extension (quadratic Hawkes per the Zumbach effect: a linear
self-excitation h plus a SIGN-DEPENDENT quadratic driver xi
excited by sign(eta)-weighted jumps, PDF pp. 13-14). All are
solvable via the quadratic Hamiltonian approximation, which turns
the HJB into triangular PDE/ODE systems in coefficients A and B
(PDF pp. 7-15). For liquidity, Hawkes-driven arrival intensities
are shown to be statistically natural but CONTROL-INTRACTABLE: the
value function needs time plus three to five state variables and
the quadratic approximation BREAKS because y and the intensities
jump simultaneously (PDF p. 17); the proposed alternative is a
Markov-modulated Poisson process — two or three discrete liquidity
states with a rate matrix Q, which collapses the curse of
dimensionality and keeps the problem a system of ODEs (PDF
pp. 17-19).

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. One candidate sharpening is queued, three reinforcing notes
recorded:

1. **[candidate sharpening, PENDING OWNER RATIFICATION] The
   estimator-mode rule for state variables.** Their Hawkes-price
   model needs the current intensity lambda-bar to compute quotes,
   and they name TWO ways to get it — treat it as an observable
   evolving in real time from a declared initial value, or
   estimate it statistically from recent historical price data,
   "similarly to how instantaneous volatility was treated" in the
   stochastic-volatility models (PDF p. 12). These are different
   ESTIMATORS of the same window, and a reader of a result must
   know which one produced it. Pre-declaration text: every hidden
   state variable in a spec (intensity, instantaneous volatility,
   any flow state) carries, IN THE SPEC, its estimator mode —
   filter-evolution from a declared initial value, or window
   estimation with a declared window — fixed before data; the
   modes are never mixed or switched mid-analysis, and any figure
   produced under one mode is never compared against a figure
   produced under the other. This makes every future reading
   reproducible and closes a silent analyst degree of freedom
   (the same freedom the trigger layer's per-branch CIs and the
   boundary-solution rule already police from other directions).

2. **[reinforcing, no new item] n IS the branching ratio, as a
   named model parameter.** Their Markovian Hawkes price carries
   n in (0,1) as "the percentage of price moves that are purely
   endogenous" (PDF p. 11) — the same object the trigger layer's
   queued branching rules govern, here treated as a fixed
   structural constant of a venue model rather than a reading to
   be measured. Independent parametrization of session 4/4b's
   scale problem: the library treats endogeneity as a parameter,
   the trigger measures it — the reading must therefore carry the
   estimation machinery, which is exactly what the queued rules
   (bootstrap CIs, boundary-solutions, per-branch, sign-register)
   supply.

3. **[reinforcing, no new item] The dimensionality verdict on
   Hawkes state models.** Their explicit engineering finding:
   Hawkes liquidity states are a good statistical fit but
   control-intractable, and a SMALL discrete Markov chain (2-3
   liquidity states) is the tractable alternative (PDF pp. 16-19).
   For C8 and any trigger state machinery this is the venue
   citation for preferring a low-state regime variable (the MMHP
   line, triage rank 1, is the same family) over a continuous
   multi-intensity Hawkes state, wherever the two are
   observationally close — fewer hidden states, fewer estimator
   degrees of freedom, per item 1's logic.

4. **[interpretation caution, explicitly NOT a rule change] The
   Zumbach structure and sign-permuting nulls.** Their Z-Hawkes
   price has a SIGN-DEPENDENT quadratic driver (xi excited by
   sign(eta)-weighted jumps, PDF p. 13) — past DIRECTIONAL structure
   raises future intensity regardless of sign of the future move.
   Consequence, recorded as interpretation language only: on a
   window exhibiting Zumbach structure, a sign-permuting placebo
   destroys real structure by construction, so a null built on
   sign-exchangeability is mis-specified in the direction of FALSE
   KILLS. This is noted for the record; it does NOT weaken any
   queued placebo (a harder-to-pass amendment would be the only
   legal change, and this observation points the other way — the
   shuffled-signs null stays, and a window's Zumbach reading joins
   the interpretation table beside its placebo results, like any
   other fingerprint).

## What this paper would have killed if we had done it wrong

If a spec had left its state variable's estimator mode undeclared,
two analysts — or one analyst, twice — could produce different
branching or flow readings from the SAME gated window (one
filtering from a declared init, one estimating from a trailing
window), and any disagreement would surface as a data question
when it is actually a specification question. The estimator-mode
rule in item 1 moves that question to the spec, where it is cheap
and binding. The program's existing specs fix their estimators
implicitly; the rule makes it explicit and uniform. Grade: **no
kill line changed; one candidate sharpening queued (the
estimator-mode rule), zero armed** — the owner's word remains the
only trigger.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The paper is a modeling suite with no empirical
calibration ("No data involved in this study," PDF p. 20) — its
state-space and tractability findings transfer; its Venue-specific
AMM content (Hodl benchmarks, pool reserves) does not touch a
program that never trades live; two authors are Swaap Labs (DeFi
industry) with funding from a Swaap-partnered research program
(disclosed, PDF p. 20) — read the tractability verdicts as
engineering, not as claims against Hawkes models as such; and the
arXiv v3 (May 2024) should be checked against the published version
before formal citation.
