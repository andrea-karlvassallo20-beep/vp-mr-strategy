# Library deep-read session 20 — Alfonsi & Blanc, "Dynamic optimal
# execution in a mixed-market-impact Hawkes price model"
# (arXiv:1404.0648v2, 2014/2015; CERMICS, ENPC; the MIH price model and
# its martingale equilibrium, explicit optimal execution)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x7c5b08_dynamic_optimal_execution_in_a_mixed_market_impact.txt`,
~40 pp., page-marked). Next UNREAD triage-rank entry (score 34;
note: cited within both Sadoghi-Vecer (session 10's read) and the
price-aware AMM suite).

## The paper in one paragraph

An Obizhaeva-Wang execution framework — linear impact, block-shaped
book, proportion nu permanent and 1-nu transient impact with
exponential resilience speed rho — where the OTHER traders' market
order flow is a symmetric two-dimensional marked Hawkes process with
volume-dependent self- and cross-excitation (iota_s, iota_c), so
the optimal execution problem is solved EXPLICITLY, including how to
react to observed orders (PDF pp. 1-10). Three headline results
(PDF pp. 8-9): (1) Poissonian order flow NECESSARILY admits robust
price manipulation strategies — trading a small proportion of each
incoming order in the opposite direction is profitable on average,
implementable without knowing the model's parameters; (2) with
Hawkes flow, whether to trade with or against an observed order
depends on parameters and size — resilience pushes one way,
self-excitation the other; and (3) a specific equilibrium, the
MIHM (mixed-market-impact Hawkes martingale) model, exists in which
self-excitation EXACTLY COMPENSATES price resilience, the price is
a martingale even at high frequency, manipulation strategies
vanish, and the optimal strategy collapses to Obizhaeva-Wang. The
MIHM conditions (iota_s > iota_c, nu < 1, beta = rho) imply, when
iota_c = 0, that the Hawkes kernel norm iota_s/beta — "the
endogeneity ratio of the market" in Filimonov-Sornette terms —
EQUALS 1 - nu, the transient fraction of the impact (PDF pp. 8-9).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand. The read yields one
structural identity and two cost-side cautions:

1. **[reinforcing, no new item] The MIHM identity: branching and
   the impact decomposition are LOCKED TOGETHER in a martingale
   price.** In their equilibrium, the endogeneity ratio (Hawkes
   kernel norm) equals the transient-impact fraction: iota_s/beta
   = 1 - nu (in the iota_c = 0 case; PDF pp. 8-9). The theoretical
   consequence for the trigger layer's branching readings: on a
   venue whose high-frequency price is (close to) a martingale —
   the efficient-markets default — a fitted branching ratio is NOT
   free-standing information about endogeneity; it is entangled,
   by a no-arbitrage balance, with the transient/permanent
   decomposition of impact. This joins the exogenous-absorption
   caution (session 17), the per-branch rule (session 9), and the
   dispersion register (session 14) as a fourth face of the same
   discipline: the branching reading is never read alone. No new
   rule — the identity reinforces the existing recording
   requirements with a theoretical (not empirical) linkage.

2. **[reinforcing, cost-survival caution] Poisson flow MISPRICES
   resilience — robustly.** Under Poisson order flow the model
   admits parameter-free manipulation strategies (PDF pp. 8-9,
   Prop. 5.2): a model that omits self-excitation systematically
   manufactures round-trip "opportunity" out of its own omission.
   For any future K7-style cost-survival layer or instrument cost
   model: the flow model is not a convenience — Poisson-based cost
   or opportunity arithmetic is arithmetically wrong in a known
   direction, and the flow model is declared with the spec. Nothing
   armed (the program never trades live).

3. **[reinforcing, no new item] Instant reaction to others' trades
   <-> manipulation existence.** Their result: "the conditions
   under which it is profitable for the strategic trader to react
   instantaneously to other trades are quite equivalent to the
   existence of PMS" (PDF p. 9) — chain reactions and instability.
   The same race/feedback interpretation family as session 21's
   race-after-trades signature and C5's front-of-book withdrawal
   anatomy; interpretation language only.

## What this paper would have killed if we had done it wrong

If a trigger-layer reading had treated "branching near 0.9" as a
free-standing measure of market endogeneity, the MIHM identity is
the closed-form counterexample: in equilibrium that reading is
carrying the transient fraction of impact with it, and two venues
with identical endogeneity but different impact decompositions
would read differently. And if any future cost layer had been
built on Poisson flow for convenience, the manipulation result is
the proof that the convenience is not conservative — it invents
profit. The queued recording rules (per-branch CIs, dispersion
register, drift/seasonality reporting) already force the
multi-reading format; this read supplies the identity explaining
why the format is the shape of the object. Grade: **no kill line
changed; no candidate sharpening; one structural identity and two
cost-side cautions; the ratification queue stands at FOURTEEN
candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The MIH model is deliberately simplified and its authors
say so: linear impact and exponential decay are "not in accordance
with empirical facts" (PDF pp. 2, 8-9), the book is block-shaped,
and the strategic trader's own orders do not excite the flow (their
tractability choice, justified by Toth et al.'s splitting evidence,
PDF pp. 7-8). The MIHM identity is a model-internal equilibrium
identity, NOT an empirical claim that any real venue sits at it —
it licenses a caution about how branching readings are read, not a
prediction. The paper's execution content is for a program that
never trades live. arXiv v2, a 2018 journal-version stamp on a
2014/2015 preprint; check the published version before formal
citation.
