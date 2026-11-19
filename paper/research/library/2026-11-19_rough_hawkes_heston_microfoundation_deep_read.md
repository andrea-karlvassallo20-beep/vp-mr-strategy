# Deep-read session 35 — A Microstructural Foundation for the Rough Hawkes–Heston Model (xd08813, score 30)

Date: 2026-11-19. Null-time session 39, log entry ## 43.
Paper: Yingli Wang, Yinhao Wu, Lingjiong Zhu, "Microstructural Foundation for the
Rough Hawkes–Heston Model", arXiv:2608.07709v1 [q-fin.MF], 7 Aug 2026 (title page
stamped 11 Aug 2026). Extract: docs/library/text/xd08813_microstructural_foundation_for_the_rough_hawkes_he.txt,
67 PDF pages, extract complete and page-marked, read in full. No shelf gap, no
inaccessibility.

Read line (the ONE question, verbatim from the standing ritual): what here would
kill C1-L2 faster, or change its kill lines?

## Summary

The paper constructs a Poisson-embedded marked Hawkes order-flow model whose
near-critical, heavy-tailed self-excitation converges, along the full sequence, to
the unique complete canonical weak solution of the rough Hawkes–Heston
stochastic-volatility model of Bondi, Pulido and Scotti (2024) (Theorem 5.1,
PDF pp. 23–24; Definition 5.4 and Proposition 5.5, PDF pp. 25–26). Ordinary
(frequent) signed order-flow events generate the continuous martingale price and
the rough volatility component through the nearly unstable Hawkes cascade
(pp. 1–2, 8–9); rare marked events (probability pT of order (1−aT)^2, pp. 11–12)
produce simultaneous downward price jumps of size −Λz and volatility excitation
amplified through the same near-critical resolvent (Lemma 4.2, PDF p. 15). The
limiting coefficient map is explicit (Eq. 55, PDF pp. 24–25): subcriticality of
the marked branching forces the Volterra mean-reversion loading b < 0
(Remark 2.6, PDF p. 8), the limiting jump measure is νJ = 2κFJ with finite
activity (Eq. 41, PDF p. 17), and the leverage correlation
ρ = −(β−1)√q / ((1+q)(1+β²q)) is negative for every β > 1, q > 0 and attains
all of (−1, 0) (Eq. 49, PDF p. 19; Proposition 5.2, PDF pp. 24–25). Numerical
sections verify the convergence law (Wasserstein distances, PDF p. 39, Figure 1,
p. 40) and reproduce the Bondi et al. SPX smile calibration from inverted
microscopic parameters (PDF pp. 40–41, Figure 2, p. 41). This is a pure theory
paper: no data are calibrated, no prediction is claimed, no out-of-sample test
exists.

## Findings

**Grade: NO kill line changed. NO new candidate sharpening.** Default grade.
The paper is a worked exhibit for rules already standing (near-criticality
disclosure, single-fitted-kernel caution, no-import-of-reduced-form-constants)
and the burden of proof for a new sharpening was not met. Findings, page-cited:

- Reinforcing, no new item — near-criticality is the load-bearing assumption
  twice over: the rough fractional memory exists only because the branching
  ratio aT approaches one at rate 1−aT ∼ μ0T^(−α) against a heavy-tailed kernel
  φ(t) = α(1+t)^(−1−α) (Assumption 3.3, Eqs. 18–19, PDF p. 11), and the
  Mittag–Leffler resolvent limit (Proposition 4.1, PDF pp. 13–14) is the sole
  origin of the fractional kernel. Qualitative behavior changes discontinuously
  at the critical boundary: subcritical marked branching is exactly what forces
  b < 0 (Assumption 3.4 and Remark 2.6, PDF pp. 12, 8). A fourth worked exhibit
  for the queued near-critical regime-disclosure rule: any Hawkes fit on the
  programme's venue must disclose its distance from criticality, because a fit
  sitting near the boundary manufactures long-memory structure by scaling
  assumption, and that structure is not a measured property of the data.

- Reinforcing, no new item — the leverage correlation is a deterministic
  function of two free asymmetry parameters and every value in (−1, 0) is
  attainable by construction (ρ formula, PDF p. 19; attainability proof,
  PDF pp. 24–25; the numerical section picks β = 8, q ≈ 0.0416 to recover
  Bondi's ρ = −0.731, PDF p. 40): frequent small up-moves against rarer larger
  down-moves, martingale-balanced by qω+ = ω−, with negative events carrying
  variance loading β > 1 (Eqs. 8–9, PDF pp. 9–10). The paper itself states the
  microscopic parameters are non-identifiable (Remark 5.3, PDF p. 25). A fitted
  negative leverage correlation on any venue is therefore never evidence that
  this asymmetry mechanism produced it; this is the aggregation face of the
  standing single-fitted-kernel and estimator-mode cautions.

- Interpretation caution — the common-shock clustering mechanism is
  variance-proportional thinning, not independent self-excitation of the jump
  measure: every compensator in the model (regular, marked, price-jump) is
  proportional to the same scalar intensity λT (Eqs. 12–13, PDF pp. 9–10), so
  the limiting shock intensity σ²_t νJ(dz)dt inherits its clustering entirely
  from the variance proxy. On the programme's venue, any claimed self-excitation
  of extreme events must be tested against the cheaper alternative that it is
  intensity-proportional thinning of an inhomogeneous Poisson stream; the model
  shows the two produce indistinguishable compensator structure by
  construction. Read discipline only; the C8 shuffled-arrival placebo family
  already occupies this ground and nothing new is queued.

- Interpretation caution — nothing transfers to the programme's venue fields or
  time grain: single instrument, no cross-market or cross-asset coupling, tick
  sizes fixed constants, the pricing measure Q taken as given, and all
  convergence statements on a rescaled horizon [0,1] (PDF pp. 8–11). The
  numerical sections are convergence verification and calibration reproduction,
  not empirical evidence: the smile comparison rebuilds the Bondi et al.
  parameters inside the microscopic model (PDF pp. 40–41); the W1 plateau is
  explicitly called a pre-asymptotic discrepancy (PDF p. 39). The paper claims no
  predictive content for any market.

- Source-quality note — arXiv v1 theory preprint (stamped 7 Aug 2026) by three
  mathematics-department authors, acknowledging Rosenbaum; proofs are present
  and complete in the text (in contrast to the session-34 target): the renewal
  asymptotics (Lemmas A.1–A.4, PDF pp. 43–48), tightness and moment bounds
  (Propositions A.6–A.8, PDF pp. 49–51, 62–64), jump-measure convergence
  (Lemmas A.9–A.16, PDF pp. 51–61) all carry full arguments. References are
  clean and journal-complete (PDF pp. 65–67). Grade at exactly the level of a
  rigorous v1 preprint: citable as a construction, check for a later version
  before formal citation.

## Killed-if-wrong

Had the coefficient map (Eq. 55) been imported into any programme spec,
tolerance, or generative null, the construction's machine assumptions
(subcriticality, pinned kernel form, variance-proportional shock intensity,
pricing-measure normalization) would have been baked into a kill line before
data. Had the convergence result been read as evidence that the programme's
venue is near-critical or that its leverage comes from asymmetric tick sizes,
a pure construction would have been laundered into a market-truth claim. The
library-is-ammunition rule and the nothing-measured invariant prevented both.

## Laundering directions named

- INTO — nothing: no coefficient, kernel form, drift sign restriction, jump
  measure, or correlation formula enters any spec, default, calibration,
  tolerance, or null; the model may not serve as a generative null for any
  C1-L2 or C8 arm without an owner-ratified pre-declared derivation of its
  assumptions on the programme's venue and fields.
- OUT — never read backwards: "markets are nearly unstable" is an assumption
  (Eqs. 18, 21, 23), not a finding; "leverage arises from asymmetric arrival
  rates and tick sizes" is an attainability construction with non-identifiable
  parameters (PDF p. 25), not a measurement; the numerical convergence figures
  are simulation quality, not market behavior, and are never citable as
  expected behavior of any market the programme measures.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never launders.
Read against the ONE question; graded on whether it changed a kill line.

Nothing measured, no kill line moved, nothing armed, nothing trades live.
