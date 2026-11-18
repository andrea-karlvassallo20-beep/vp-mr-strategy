# Library deep-read session 10 — Sadoghi & Vecer, "Optimum Liquidation
# Problem Associated with the Poisson Cluster Process"
# (arXiv:1507.06514v2, 2015; Frankfurt School; discrete-time MDP/PDMP
# liquidation with Hawkes order arrivals, simulation study)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x47fd73_optimum_liquidation_problem_associated_with_the_po.txt`,
45 pp., page-marked). Next by triage rank (session 11's pointer),
under the triage-audit caveat.

## The paper in one paragraph

A single trader liquidates a large inventory in an illiquid discrete
limit order book; order arrivals carry a Hawkes-type stochastic
intensity d(lambda) = (f(gamma_t) - kappa*lambda) dt + sigma dN_t,
where the trading rate gamma enters the intensity through the price
impact function f and sigma is the magnitude of self-excitation
(PDF pp. 20, 29). The liquidation problem is a multi-stopping
problem solved as a discrete-time Markov Decision Process over a
Piecewise Deterministic Markov Process state, with a quantization
approximation of the value function (PDF pp. 25-28). The central
simulation result: the optimal strategy depends on the market's
excitation SIGN, not just its magnitude — under SELF-DAMPING
(sigma < 0: your selling suppresses subsequent order arrivals) the
algorithm slows down, waits, and accepts offers deeper in the book
to avoid end-of-period inventory penalties; under SELF-EXCITING
(sigma > 0) the opportunities are more profitable and the optimal
rates run higher (Table 1, PDF p. 33: revenues $50,000-ish in the
damping panels vs $62,539-$94,691 in the exciting panels, with the
gain "considerably" dependent on the price-impact-function
specification, PDF pp. 32-33). The authors explicitly map the
negative self-excitation case to strategic behavior — order
submission/cancellation designed to detect hidden liquidity or
manipulate the market, "known as a 'market manipulation'" (PDF
pp. 29-30, citing Cartea et al.).

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. One candidate sharpening is queued, two reinforcing notes
recorded:

1. **[candidate sharpening, PENDING OWNER RATIFICATION] The
   sign-register rule for excitation features.** This paper's core
   result is that DAMPING (sigma < 0) and EXCITATION (sigma > 0)
   are materially different regimes of the same mechanism —
   different optimal behavior, different revenue (Table 1, PDF
   p. 33) — and their model treats the sign as state to be read,
   never clipped. Pre-declaration text for the L2 feature layer:
   every excitation/damping feature is estimated and reported
   TWO-SIDED with its sign and CI; a negative reading is recorded
   in its own register cell as "damping," never flipped, floored at
   zero, or discarded as a failed positive. The program's own
   precedent is T1: the registered mechanism measured with its
   SIGN INVERTED (every compression HR below 1.0), and the honest
   response was to book the inversion, not to clip it — this rule
   makes that discipline prospective and binding on the features,
   in the only legal direction (harder to pass: a feature whose
   readings are one-sided by construction cannot launder a sign).

2. **[reinforcing, no new item] The manipulation signature, in a
   second independent form.** Their negative-self-excitation case
   is explicitly the strategic-submit/cancel behavior (PDF
   pp. 29-30) — the same mechanism family as the queued spoofing
   cautions (session 6's CKS sibling hunt, the wash-trading audit)
   and the C5 passive-withdrawal claim: strategic actors SUPPRESS
   the arrival process around their own activity. It reinforces
   the queued interpretations without changing them: on gated
   windows, a damping reading must be audited (is it ordinary
   queuing suppression or an actor?) before it enters any feature.

3. **[reinforcing, no new item] Cost-survival ammunition, not a
   strategy.** Their headline trade-off — waiting for better
   offers versus the end-of-period inventory penalty, with the
   balance set by pre-declared microstructure parameters (sigma,
   kappa, the spread as the illiquidity proxy, PDF pp. 30-31) —
   is exactly the shape of a K7-style cost-survival amendment
   (an edge that dies at realistic execution in an illiquid book
   is dead, and its death is recorded the same hour). The program
   never trades live; this is the source to cite if the owner ever
   ratifies cost modeling for an instrument spec, not a strategy
   candidate.

## What this paper would have killed if we had done it wrong

If the L2 feature layer had been specified with one-sided
excitation estimators (clamp-at-zero branching, magnitude-only
kernels — the standard implementations), T1's inverted sign would
have been structurally invisible BEFORE it could be honestly
booked: a damping regime would have read "no endogeneity" instead
of "negative endogeneity," and the informative covariate would
have been silently discarded. The sign-register rule in item 1
closes this at the specification layer, where the correction is
cheap; the alternative is discovering it after the data, where the
only legal response is a harder amendment. Grade: **no kill line
changed; one candidate sharpening queued (the sign-register rule
for excitation features), zero armed** — the owner's word remains
the only trigger.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The paper is a simulation study — its parameters are
scenario values, not calibrated to a real book (the authors state
the parameters "can be estimated from the real market data,"
PDF p. 31, but no estimation is performed); the revenue panels
(Table 1) live in the model's own units and should never be read
as magnitudes; the prose is rough in places ("Trad˙rate,"
"favorite offers," several unproven cross-references), it remains
an arXiv preprint (v2, 2015; a 2018 journal-submission stamp with
no published version found — check before formal citation), and
its liquidation-strategy content is irrelevant to a program that
never trades live. Its durable contributions to THIS program are
the sign-as-state reading (item 1) and the manipulation-signature
reinforcement (item 2), both of which stand on the simulation's
structure, not its magnitudes.
