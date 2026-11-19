# Deep-read session 39 — Kanazawa and Sornette, "Exact asymptotic solutions to nonlinear Hawkes processes: a systematic classification of the steady-state solutions"

Library deep-read session 39 (null-time session 43, log entry
## 47; the previous session's closing pointer named x36082b
"Branching ratio approximation for the self-exciting Hawkes
process" (score 30) as the mechanical next UNREAD, but that entry
is already READ: deep-read session 2
(2026-11-16_hawkes_branching_deep_read.md), so per the
honest-skip protocol and a re-read of the live main tail,
DECISIONS_PENDING and the branch/PR set (no open PRs, no branch
claims the queue head) the next unclaimed UNREAD entry was taken:
x20bdef). Kiyoshi Kanazawa (University of Tsukuba / JST PRESTO)
and Didier Sornette (ETH Zurich / SUT Shenzhen), arXiv:2110.01523v2
[cond-mat.stat-mech], v2 dated 9 May 2022, 63 pp. text extract,
page-marked, complete through Table I (PDF p. 63). Read 2026-11-19,
against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/x20bdef_exact_asymptotic_solutions_to_nonlinear_hawkes_pro.txt).
Assigned triage-rank entry (score 30, x20bdef).

## The paper in one paragraph

Pure statistical-physics theory, no data calibration. The paper
maps marked nonlinear Hawkes (NLHawkes) processes, in which the
intensity is a nonlinear map g of a "tension" built from past
marks, onto Markovian field SPDEs and solves the corresponding
field master equations for the steady-state intensity distribution
Pss(λ) (Secs. II-III, PDF pp. 2-13). Three headline asymptotic
regimes, robustly classified in Table I (PDF p. 63): (i)
one-sided positive marks with a ramp (rectified-linear) intensity
map give a non-universal power law Pss(λ) ∝ λ−1−a with any real
exponent a = 2ν1⟨τ⟩/α2 at criticality (η = 1), true tail for
positive ν1 and intermediate asymptotics otherwise, valid for
general memory kernels (Eqs. (193), (227), PDF pp. 31-36); (ii)
zero-mean (symmetric) two-sided marks with fast-accelerating
intensity maps g(ν) ≫ ν2 universally yield Zipf's law Pss(λ) ∝ λ−2,
including the exponential (MSA) map λ0eβν (Eqs. (100), (119),
(230), (254), PDF pp. 20-40), while the quadratic ZHawkes map
recovers exactly the Blanc-Donier-Bouchaud exponent a = 1/2 +
1/(2kDτ) (Eqs. (94), (108), PDF pp. 20-24), confirming their
conjecture for symmetric marks with finite moments; (iii)
negative-mean marks thin the tail continuously away from Zipf,
Pss(λ) ∝ λ−2−β−1u with u set by the positive root of the mark
moment-generating function, vanishing as the mean mark goes to
zero (Eqs. (166), (171), PDF pp. 28-31). Two structural facts
carry the classification: with one-sided marks and exponential
memory, any map growing faster than the ramp is always
non-stationary, the ramp being the exact stationarity boundary
(Eq. (71), PDF p. 16), while with symmetric two-sided marks the
ramp model has no critical point at all, stationary for every η
with an exponential tail (Eq. (88), PDF p. 19). A Kesten-process
heuristic reproduces the exponents (Sec. IX A, PDF pp. 41-43), and
the finance discussion is confined to the observation that many
NLHawkes specifications can reproduce power-law intensity PDFs and
that a model-selection framework is beyond the paper's scope
(Sec. IX B, PDF pp. 43-44).

## Findings, graded

NO kill line changed. NO new candidate sharpening. Default grade;
the paper is a specification-classification worked exhibit of
rules already standing and the burden of proof for a sharpening
was not met. Nothing measured, nothing armed.

1. **[reinforcing, no new item]** Power-law intensity tails are a
   model-class output, produced by specification choice, not by
   any venue: by the paper's own Table I (PDF p. 63) the same
   qualitative object, a power-law Pss(λ), is manufactured at will
   with any exponent by the ramp map with one-sided marks near
   criticality (Eq. (193), PDF p. 31), with universal Zipf by any
   FAI map under balanced marks (Eq. (254), PDF p. 41), or with a
   continuously thinned exponent by pushing the mean mark
   negative (Eq. (171), PDF p. 29), and the authors themselves
   state that "various Hawkes models can be suitable candidate
   models" for the empirical power law and that framework-level
   model selection is out of scope (Sec. IX B, PDF pp. 43-44).
   This is the sixth worked exhibit for the near-critical
   regime-disclosure and specification-versus-discovery family
   (deep-read 17, boundary-solution rule deep-read 5, mean-field
   universality deep-read 38): an observed or fitted heavy-tailed
   intensity distribution is consistent with an entire family of
   mutually incompatible microscopic feedback stories, so it
   identifies nothing. The existing rules govern; nothing added,
   no transfers, no declaration queued.

2. **[interpretation caution]** Stationarity and the existence or
   absence of a critical point are structural artifacts of the
   assumed mark geometry, not empirical findings. With one-sided
   positive marks and exponential memory, any super-ramp
   intensity map (including the MSA exponential map) is always
   non-stationary regardless of parameters (Eq. (69), PDF
   p. 16), and the paper's own simulations of the Zipf regime
   required an artificial intensity cap λmax = 10⁶, with the
   stated admission that simulation results depend sensitively on
   this cutoff (Eqs. (70), (252), PDF pp. 16, 40; Appendix I, PDF
   pp. 60-61): a Zipf slope measured in any simulated or fitted
   exponential-map system carries the fingerprint of the
   regularizer. Conversely, with symmetric two-sided marks the
   ramp process "has no critical point" and is stationary for all
   η by construction (Eq. (88), PDF p. 19). Binds as read
   discipline on any hypothetical future excitation fit: absence
   of criticality in a fitted inhibitory-symmetric class is a
   specification statement, and simulation-borne tail exponents
   inherit their cutoff. Nothing in C1-L2 or C8 currently
   specifies such a fit, so nothing moves.

3. **[reinforcing, no new item]** Where the paper touches the
   programme's existing record, it confirms sideways rather than
   adding: the ZHawkes/quadratic exponent a = 1/2 + 1/(2kDτ)
   (Eqs. (94), (108), PDF pp. 20, 22) is the exact solution of
   the Blanc-Donier-Bouchaud conjecture already in the record's
   cost-survival and reflexivity lines (reference [28], PDF
   p. 62), and the Kesten reduction (Eq. (256), PDF p. 41)
   re-derives it under ⟨ln a⟩ < 0. This corroborates the standing
   reading of the QHawkes line, ammunition not evidence, and
   licenses nothing new.

4. **[source-quality note]** Cond-mat preprint, no data, no
   calibration, no out-of-sample content; the finance motivation
   is a literature review (Sec. II C, PDF pp. 5-6) and the
   implications section is explicitly deferred. Mark distribution
   assumptions (finite moments, existence of the
   moment-generating function, PDF pp. 11, 50-54) exclude
   heavy-tailed marks, and the general-memory-kernel results
   cover only the ramp and FAI classes: the authors state two
   Table I cells remain unsolved for general kernels (Sec. X,
   PDF p. 46). arXiv v2 dated May 2022; a published version is to
   be checked before any formal citation. Extract complete,
   page-marked, symbol degradation confined to formula regions,
   statements anchored to prose.

## What this paper would have killed if we had done it wrong

Had the Zipf universality result been read forward as market
truth ("venue intensity distributions are Zipf, therefore
balanced excitatory-inhibitory nonlinear feedback with an
FAI map is what markets do"), a within-model classification
theorem would have been laundered into an identification claim
the paper itself disclaims by declaring model selection beyond
scope. Had the no-critical-point property of the symmetric-mark
ramp model been ignored, absence of criticality in some future
fitted inhibitory class could have been booked as an empirical
discovery about the venue rather than a deduction from the
assumed mark symmetry. Had the λmax dependence of the simulators
been ignored, a simulated tail exponent would have entered a
future argument as a cutoff-free property. Library-is-ammunition,
the near-critical regime-disclosure rule and nothing-measured
prevented all three.

## Standing caveat

No market, no sample, no period, no costs; seismic and neural
idealizations carried through the bookkeeping, the all-to-all
tension through a scalar kernel. The exact solutions are mostly
for exponential memory; the general-kernel statements are
asymptotic and incomplete by the authors' own listing. Simulation
support in Secs. VII C and VIII C rests on the artificial cap
λmax and an adaptive discretization, and the mark-moment and
moment-generating-function conditions fence off exactly the
heavy-tailed mark cases most natural in finance. Laundering
directions named. INTO — nothing: no tension-intensity map, mark
geometry, regime classification, law (67), (100), (193), (254)
or exponent formula enters any spec, default, calibration,
tolerance or generative null, and the NLHawkes family may not
serve as a null or simulator for any C1-L2 or C8 arm without an
owner-ratified pre-declared derivation of its assumptions on the
programme's venue and fields. OUT — never read backwards as
"markets are nonlinear-balanced Hawkes" (a specification),
"Zipf intensity tails prove inhibitory feedback" (universal
within the class, non-identifying across it), or "no criticality
found" (assumed symmetry, Eq. (88)), and no simulation exponent
from this family is quoted without naming its λmax.
