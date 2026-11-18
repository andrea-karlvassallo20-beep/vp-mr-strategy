# Library deep-read session 16 — Swishchuk & Huffman, "General Compound
# Hawkes Processes in Limit Order Books" (arXiv:1812.02298v1, 2018;
# Calgary; compound Hawkes mid-price models, diffusion limits, LOBSTER
# data)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xfeb371_general_compound_hawkes_processes_in_limit_order_b.txt`,
~17 pp., page-marked). Next UNREAD triage-rank entry (score 36).

## The paper in one paragraph

Mid-price changes are modeled as a COMPOUND process: S_t = S_0 +
sum_{i=1}^{N(t)} a(X_k), where N(t) is a (non-)linear Hawkes
process counting price changes and X_k is an ergodic n-state
Markov chain of state-dependent order/price-change types —
dependent orders, with a(X) taking tick-valued or n-valued
markups (PDF pp. 6-7). For each variant (non-linear compound,
n-state, 2-state, fixed-tick), LLNs and diffusion limits are
proved: the rescaled price converges to sigma* * sqrt(lambda /
(1 - mu-hat)) * W(t), where mu-hat = integral of the excitation
kernel is the branching ratio and sigma* is a variance functional
of the Markov chain's ergodic probabilities and transition
probabilities (Theorems 4.1/4.3, Corollaries 1-3, PDF pp. 7-13).
Empirically: one day (2012-06-21) of level-1 LOBSTER data for
AAPL/AMZN/GOOG/MSFT/INTC, with inter-arrival clustering checked
against Poisson and model parameters fitted to the intraday price
changes (PDF pp. 13-15).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand. The read supplies
two reinforcing identities for the interpretation table:

1. **[reinforcing, no new item] The 1/(1-mu-hat) amplification —
   the volatility-side face of the near-critical pathology.** In
   every diffusion limit the branching ratio enters the price
   volatility through the factor sqrt(lambda/(1 - mu-hat))
   (PDF pp. 7, 9-13): a fitted branching reading approaching one
   makes the DERIVED long-run volatility unbounded — the
   same instability the queued boundary-solution rule (session 5)
   polices at the estimator, now visible on the volatility face.
   Consequence for the interpretation table: any window whose
   branching CI is near unity carries an INFLATED, unstable
   derived-volatility reading with it — the two readings must be
   reported together, and a near-critical window can never cite
   its derived volatility as independent evidence of anything.
   This is the amplification the queued CI and dispersion-register
   rules exist to catch before it launders into an argument.

2. **[reinforcing, no new item] A two-channel volatility
   decomposition, explicit.** The diffusion coefficient factors
   into (a) the arrival channel — lambda/(1-mu-hat), pure
   clustering/endogeneity — and (b) the order-state channel —
   sigma*(ergodic probabilities, transition probabilities), pure
   sign/size persistence of successive price changes (PDF
   pp. 7-10). Two MECHANICALLY DIFFERENT sources of volatility,
   multiplied together in one coefficient. This is a clean
   structural citation for the deployed vol-tautology family: a
   variance-surrogate feature conflates the clustering channel
   with the order-persistence channel, and only the deployed
   tautology checks (and the per-branch machinery) can say which
   channel a given reading rode in on. Recorded as
   interpretation language; no rule change.

3. **[source-quality note] One day, five names, level-1, 2012.**
   The empirical content is a single trading day of level-1 data
   with parameters fitted session-by-session — magnitudes carry
   nothing; the model structure (compound counts over Markov
   marks) is the transferable object. The triage-audit flag
   (session 11) stands: mid-rank entries are candidates, not
   promises.

## What this paper would have killed if we had done it wrong

If a future instrument spec had used a Hawkes-derived long-run
volatility as an input WITHOUT carrying the branching CI beside
it, a single near-critical fit would have inflated the volatility
estimate without bound and propagated it downstream as if
measured — the boundary pathology wearing a volatility costume.
The queued rules already require the CI; this read adds the
explicit 1/(1-m) identity explaining WHY the requirement is not
pedantry. Grade: **no kill line changed; no candidate sharpening;
two reinforcing identities and one source-quality note; the
ratification queue stands at FOURTEEN candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The diffusion limits assume the kernel integrability
conditions (mu-hat < 1, finite first moment, PDF pp. 7, 9) — the
subcritical regime only — so the near-critical amplification in
item 1 is an extrapolation warning, not a licensed approximation
at mu-hat near 1 (where Horst-Xu's critical limits, session 14,
govern instead); the empirical fits are one-day, one-venue,
level-1; and the compound model treats the mark chain as
independent of the arrival process — an assumption Financial
market data routinely violates (the sign of a price change is
hardly independent of clustering intensity; cf. session 13's
Zumbach structure). arXiv v1 (2018), apparently an AIMS-series
manuscript; check the published version before formal citation.
