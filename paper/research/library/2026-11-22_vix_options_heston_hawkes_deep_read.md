# Deep-read 92 — Zamora Font, "Pricing VIX options under the Heston-Hawkes stochastic
# volatility model"

Deep-read session 92 (null-time session 102). Authors: Oriol Zamora Font (Department
of Mathematics, University of Oslo), 2024, arXiv:2406.13508v1 — a pure-theory
derivation of a semi-analytical European VIX call pricing formula under the
Heston-Hawkes stochastic volatility model of Baños-Ortiz-Latorre-Zamora, a Heston
variance augmented by an independent compound Hawkes jump component.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8 faster,
or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x2b0051_pricing_vix_options_under_the_heston_hawkes_stocha.txt,
~28 pp., page-marked). Next UNREAD triage-rank entry (score 20, second of the
score-20 tier, after the Guo-Swishchuk-Rémillard multivariate Hawkes LOB option
read of deep-read 91 / ## 120).

Session-state note (director step, per docs/goal_autonomy_protocol.md): the live
main tail (through ## 120) and docs/DECISIONS_PENDING.md were read at session
start (ratification line: forty-nine candidates plus probe E1, zero armed); the
open-PR set was read (empty, no race; the branch field holds only merged deep-read
branches); the cadence check was recomputed from first principles — the edition-10
counter stood at THREE of five after deep-read 91 (## 120), so no synthesis pass is
due and the default work choice for this session is the standing deep-read ritual
itself, which needs no justification under the protocol; this read (#92) moves the
counter to FOUR of five. Verified against live state before reading: the triage
file score-sorted, the entry x2b0051 verified note-less against the live library
note listing (the superficially adjacent notes 2026-11-19_rough_hawkes_heston_
microfoundation and 2026-11-21_heston_queue_hawkes_option_pricing are DIFFERENT
papers, both already read; this entry is the VIX-option pricing note of the Oslo
Heston-Hawkes line, unread), and its extract present and page-marked (380,675 bytes,
28 PDF pages, abstract through references complete). This is deep-read 92, the
FOURTH read counted against the edition-10 cadence.

## The paper in one paragraph

The paper derives the pricing formula in four modular steps, each with its own
existence theory. First, the model: Heston variance dv_t driven by a Brownian term
plus η dL_t where L is a compound Hawkes process with exponential-kernel intensity
dλ_t = −β(λ_t − λ_0)dt + α dN_t, α < β, general positive jump-size law J_1 under
Assumption 1 (mgf well defined on (−∞, ε_J), maximal domain) (PDF pp. 3-4). Second,
the measure problem is taken seriously rather than assumed: Theorem 4.3 gives a
family of equivalent (local) martingale measures Q(a) indexed by a real parameter a
with |a| < √(2c_l), c_l an explicit constant depending on κ, σ, η, T, the jump law
and α/β (Proposition 4.2, PDF pp. 5-6), and a strictly smaller subset E_m(Q_1,
2+ε_1) of true martingale measures carrying the needed moment integrability
(Assumption 2, Definition 4.4, Proposition 4.5, PDF pp. 6-7). Third, the joint
transform: generalized Riccati ODEs for G, H, F (Lemma 5.3) solved and shown to
exist on [0,T] ONLY for φ, ψ in an explicit complex domain — 0 < Re(φ) <
min{2κ(a)/σ²(2e^{κ(a)T}−1), L_J} with L_J := (1/η)M_J^{−1}((β/α)exp(α/β−1)), and
Re(ψ) < (β−α)/(αβ) — whose boundary is set by the Hawkes memory ratio α/β and the
jump mgf; the bound sup_t E[e^{η Re(G(t;φ))J_1}] < (β/α)exp(α/β−1) is what keeps
the H-ODE's comparison solution non-explosive (PDF pp. 7-10, 15-20); the
conditional characteristic function then takes exponential-affine form
e^{F+Gv_t+Hλ_t} (Proposition 5.4, PDF pp. 8-11). Fourth, the object: VIX²_t proved
to be a linear combination A(a)v_t + B(a)λ_t + C(a) with A, B, C explicit positive
constants, via the Markov property of the exponential Hawkes and a forward-variance
/variance-swap computation (Propositions 6.2-6.9 and Appendix A.2, PDF pp. 11-13,
20-26), and the call price assembled through the Lewis/erfc integral identity
(3.2), culminating in Theorem 7.1 with the admissible integration contour
φ = φ_R + iφ_I restricted by 0 < φ_R < min{2κ(a)/(σ²A(a))(2e^{κ(a)T}−1),
L_J/A(a), (β−α)/(B(a)αβ)} (PDF pp. 14-15). There are no numerics, no calibration,
no data anywhere in the paper.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The paper proves in
   print, twice over, that a transform-based quantity has a nontrivial DOMAIN
   OF EXISTENCE whose boundary is set by the estimator configuration itself
   (the Hawkes memory ratio α/β and the jump-size mgf), and that the literature
   omits exactly this check: the entire pricing formula is valid only on the
   contour (7.2), whose bound comes from L_J := (1/η)M_J^{−1}((β/α)exp(α/β−1)) —
   the jump-law mgf inverted at a point that depends on the self-excitation
   parameters — and from Re(ψ) < (β−α)/(αβ); the H-ODE comparison argument
   explodes (no solution, no formula) the moment sup_t E[e^{η Re(G)J_1}] crosses
   (β/α)exp(α/β−1) (Lemma 5.3(iii)-(iv) and its proof, PDF pp. 7-8, 18-20), and
   the paper's own Remark 3.1 faults the closest prior model (the SVCIJ-H of
   Ye-Wu-Chen [36]) because "we miss this study in [36, Proposition 2]" — the
   same formal transform formula had been published and used without its domain
   ever being shown to intersect Re > 0 (PDF p. 5). Queued proposed sharpening
   #50, the transform-domain admissibility pre-declaration: BEFORE the L0 gate,
   any C1-L2/C8-adjacent computation, comparator, null or feature whose value
   is computed through a transform of the data or of a fitted model — a
   characteristic-function / Fourier-inversion estimator, an affine-transform
   price or intensity formula, a spectral or Laplace/Fourier representation, a
   moment-generating-function identity — must pre-declare, as frozen
   configuration counted in the multiplicity ledger: (i) the domain of
   existence of the transform as an explicit function of the frozen parameters
   (the region in the evaluation-variable space where the defining expectation
   or integral is finite and the associated ODE/integral solutions exist), or a
   dated derivation of that domain; (ii) a check, recorded before any data is
   touched, that every evaluation point at which the statistic will be computed
   lies inside the pre-declared domain for ALL frozen configurations it may
   take (including the boundary-approach behavior: a statistic computed within
   a declared tolerance of the domain boundary must say so beside its value);
   and (iii) the numerical-tolerance convention for transform-inversion
   truncation/contour choice, as frozen configuration — an evaluation outside
   the proven domain, or a domain that shrinks away from the evaluation point
   under one legal configuration of the frozen set, makes the statistic
   UNDEFINED by rule, not merely inaccurate: an implementation that silently
   returns a finite number (by truncation, damping, or contour shift the text
   never authorized) fails the concordance audit; harder-to-pass because a
   transform-based number computed at an evaluation point where the underlying
   transform provably does not exist — which today could survive as a silent
   numerical artifact of a Fourier or spectral routine, indistinguishable in the
   output from a legitimate value — now fails at the gate, and a claimed
   structure resting on such a number is dead by rule; tightens the
   estimator-implementation concordance rule (deep-read 85), which checks code
   against a written definition but does not require the definition's own
   existence domain to be proven or the evaluation point checked against it,
   and joins the estimator-configuration freeze (deep-read 63) and the
   price-process-family invariance rule (deep-read 66) in extending frozen
   configuration to the existence conditions of the analytic object itself;
   full draft with the killed-if-wrong counterfactual in this note's next
   section.

2. [reinforcing, no new item] The equivalent-martingale-measure family is a
   continuum indexed by a free parameter a (Theorem 4.3, PDF pp. 5-6): every
   price in the paper is Q(a)-dependent, κ(a) = κ + aσ and v̄(a) shift with the
   analyst's measure choice, and the paper itself cites [33, 34] that
   "exposures computed under the risk neutral measure are essentially arbitrary"
   (PDF p. 2) — so any model-implied theoretical quantity is a function of an
   analyst-chosen measure within a family, and two researchers can hold
   different but equally "risk-neutral" values of the same statistic. This
   reinforces the estimator-configuration freeze (deep-read 63: WHICH estimator
   in WHICH configuration, and the measure-indexing parameter is exactly such
   a configuration, to be frozen and counted, never re-picked after the result
   is seen) and, via the same mechanism, the model-inversion identifiability
   pre-declaration (#49): an inversion recovering a latent quantity from an
   observed price under an un-fixed member of a measure continuum is
   under-identified by construction. No queue change.

3. [reinforcing, no new item] The intensity λ_t is a genuine latent state
   variable: VIX²_t is proved to be A(a)v_t + B(a)λ_t + C(a) (Proposition 6.9,
   PDF p. 13), so the model's headline observable-equivalent embeds the
   Hawkes intensity with an explicit positive loading B(a) > 0 — the quantity
   an "implied intensity" inversion would try to recover. The paper never
   inverts: it prices forward from a known state. But the loading's structure
   (observable variance plus unobservable self-excitation state, both entering
   the same scalar) is precisely the split that #49 declares under-identified
   when the split is performed after the fact rather than pre-declared; a future
   C1-L2/C8 use of a Hawkes-implied intensity against a compressed-book
   observable travels the already-queued rule. No queue change.

4. [interpretation caution] The α/β near-criticality sensitivity reappears here
   on the domain side rather than the magnitude side: the admissible Re(ψ)
   bound (β−α)/(αβ) and the L_J bound both tighten toward zero as α/β → 1, so
   the same self-exciting configuration that inflates near-critical magnitudes
   (deep-read 91, ## 120) also shrinks the parameter region in which any
   transform of the process exists at all. Where a future L2-derived
   Hawkes-adjacent statistic is computed near its own spectral boundary, both
   its magnitude interpretation AND its well-definedness require the
   frozen-distance-from-criticality of the self-excitation regime-window
   pre-declaration (deep-read 53); the two disciplines are one mechanism viewed
   from magnitude and from existence. Any magnitudes from this paper are banned
   from the record under the laundering rule (no empirical content exists to
   launder). No queue change.

5. [source-quality note] arXiv v1 preprint, companion to [7] (the change-of-
   measure paper, to appear in Adv. Appl. Probab.) and [6]; no empirical
   calibration anywhere, every parameter symbolic. Internal defects, none
   load-bearing for the domain argument: the two statements of the Lewis/erfc
   identity disagree in form between (1.1) and (3.2) (PDF pp. 2, 4: "1 − erf"
   with a stray bracket vs. erfc; the appendix-free body never reconciles
   them); the Lemma A.6 comparison-inequality line as printed is garbled
   (∫(e^{−k2u} − e^{−k1u})/(k1−k2)du compared to ∫(e^{−k1u} − e^{−k1u}) and
   concluded "= 0", PDF p. 26) though the claim itself is true and another line
   of it is fine; one "Hakwes" typo (PDF p. 3). Check the published version
   before formal citation. No queue change.

## What this paper would have killed if we had done it wrong

Counterfactual for sharpening #50. Had the programme taken a Fourier- or
affine-transform-based comparator, null or statistic from the Hawkes literature
(spectral estimators for the branching ratio, characteristic-function
calibration of a Hawkes family, an OFI-transform benchmark) without demanding
the transform's domain of existence, the exact failure the Ye-Wu-Chen
SVCIJ-H lineage embodies — per this paper's own Remark 3.1, a published
pricing formula used for years with no proof its joint transform domain
intersects Re > 0 — would have been available to us wholesale: a transform
routine evaluated outside its existence domain still returns finite numbers
(truncation, damping and contour defaults are silent), so a comparator could
have "run clean" on the L2 data while its values were artifacts of the
numerical convention, not values of the object the spec named; and because
the domain boundary is a function of the (frozen) α/β and jump-moment
configuration, a post-hoc re-configuration of the memory parameters would
have MOVED the boundary under the evaluation point without touching a single
line of code — a researcher degree of freedom invisible to the
concordance audit (code faithfully implements the written definition in both
configurations) and to the configuration freeze (both configurations are
legally declared). The estimator-configuration freeze of deep-read 63
pins WHICH configuration; sharpening #50 pins that the analytic object
itself exists where the configuration puts it. Under the existing rules
either failure could have surfaced only after a kill-line verdict cited the
number; under the queued rule the spec fails at the gate, before the data.

## Standing caveat

Purely theoretical, single-author, equity-index volatility-derivatives
context (SPX/VIX), zero empirical or numerical content: nothing in this
paper is evidence about crypto L2 microstructure, and the standing caveat
binds absolutely — no magnitudes, no stylized facts, nothing measured here
may enter any spec as support. The model derives VIX² through a
"mathematical simplification" of the CBOE definition (Definitions 3, 6.7,
PDF pp. 4, 13) that the paper itself flags, so even the object being priced
is an idealization. The martingale-measure set E_m(Q_1, 2+ε_1) is maintained
only under Assumption 2's parameter restrictions (PDF p. 6), and all proofs
route through the companion papers [6] and [7], so the pricing formula's
correctness is conditional on those. arXiv v1 (19 June 2024); companion
publication of [7] is listed as to-appear — check published versions before
formal citation.

Nothing measured, no kill line moved, nothing armed, nothing trades live.
