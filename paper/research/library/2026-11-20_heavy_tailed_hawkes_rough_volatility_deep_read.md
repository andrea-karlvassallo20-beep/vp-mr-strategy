# Deep-read session 58 — Horst, Xu, Zhang, "Convergence of Heavy-Tailed Hawkes Processes and the Microstructure of Rough Volatility"

- Authors: Ulrich Horst (Humboldt-Universität zu Berlin), Wei Xu (Beijing
  Institute of Technology), Rouyi Zhang (Humboldt-Universität zu Berlin)
- Full title: "Convergence of Heavy-Tailed Hawkes Processes and the
  Microstructure of Rough Volatility"
- Venue: arXiv:2312.08784v3 [q-fin.MF], arXiv stamp 25 Mar 2026 (the acquired
  extract's title page carries the date line "March 26, 2026"; the expanded
  index lists year 2023, the v1 origin — see the source-quality note below)
- What it is: a purely theoretical scaling-limit paper proving the weak
  convergence of the INTENSITY of a nearly-unstable Hawkes process with a
  heavy-tailed (power-law) kernel — not only of its integrated version — to
  the stochastic Volterra equation of a rough Heston model, via a new
  C-tightness criterion for càdlàg processes built on the classical
  Kolmogorov-Chentsov criterion, plus a counterexample proving that
  convergence of the integrated process can in general not identify the
  rate process. No estimation, no data application anywhere in the paper.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x8fc12b_convergence_of_heavy_tailed_hawkes_processes_and_t.txt,
~38 pp., page-marked). Next UNREAD triage-rank entry (score 27).

## The paper in one paragraph

The paper puts order arrivals in a marked Hawkes point measure with a
power-law kernel φ(t) = ασ(1 + σt)^{−α−1}, α ∈ (1/2, 1) (PDF pp. 1-2, 6),
and studies the joint rescaling regime of Assumption 2.4: arrival rate
n → ∞, per-order impact → 0, and the branch ratio approaching one as
n^α(1 − ζn) → b, with the initial residual impact decaying at the kernel
tail Φ(t) = (1 + σt)^{−α} (PDF pp. 8-10). Under that regime the paper
proves the rescaled volatility/intensity V^(n)(t) = Vn(nt)/n^{2α−1} is
C-tight and converges weakly to the unique solution of a stochastic
Volterra equation written both in Mittag-Leffler form (Theorem 2.6,
eq. 2.11, PDF pp. 10-11) and in the fractional/rough Heston form
(Theorem 2.7, eq. 2.12, PDF pp. 11), achieved by identifying the kernel
n^{1−α}Rn(n·) → b^{-1}·f^{α,γ} through its Laplace transform (Prop 3.1,
PDF p. 13) and a new C-tightness criterion: piecewise-linear interpolation
on grids k/n^θ, θ > 2, plus vanishing grid jumps and a polynomial increment
moment condition (Lemma 3.5, PDF pp. 14-16), applied to the stochastic
integral term (Lemmas 3.10-3.11, Cor 3.12, PDF pp. 21-25). The joint
price-volatility limit is a rough Heston model with INDEPENDENT driving
Brownian motions, an artifact of the different spatial scalings and the
conditionally deterministic price changes (Theorem 2.9 and its discussion,
PDF pp. 10-12). The counterexample of Section 3.7 (PDF pp. 33-34) then
shows that under a different initial-impact choice the INTEGRATED process
converges to a perfectly identified limit while the rate process itself
diverges at the origin (Y (t) → ∞ as t → 0+), i.e. integrated convergence
licenses nothing about the rate process, and that a vanishing initial
volatility, the case their example does not cover, would contradict the
very purpose of a Hawkes model (PDF p. 34).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Every mechanism this
paper carries lands on discipline already standing or already queued:
the near-critical regime's null products (apparent roughness and long
persistence) are pre-empted by the near-instability estimator-discipline
family in the ratification queue, and the integrated-statistic trap is
pre-empted by the primary-metric pre-commitment queued at session 55.
A pure-theory sibling of the already-read Jaisson-Rosenbaum lineage adds
reinforcements, not amendments.

1. [reinforcing, no new item] The criticality-scaling law: the rough limit
   exists ONLY inside the precise joint trajectory n^α(1 − ζn) → b with
   Vn,0/n^{2α−1} → V*(0) and µn/n^{α−1} → a (Assumption 2.4, eq. 2.10,
   PDF pp. 9-10). The branch-ratio proximity to one is a statement about
   a RATE OF APPROACH at a scale, not a level: ζ̂ close to 1 on data means
   exactly nothing without the scale at which (1 − ζ) is resolved. This
   is the theoretical core of the already-queued near-instability /
   apparent-criticality calibration items and of the branch-norm reporting
   duties; any C1-L2/C8 readout of "criticality" must carry the
   deficit-minus-scale pair or it is not read at all. No queue change.

2. [reinforcing, no new item] The integrated-statistic trap: Section 3.7's
   counterexample proves the weak convergence of the INTEGRATED volatility
   process can coexist with a rate process that diverges at the window
   origin, and that the limit of the integrated process cannot in general
   be differentiated back to identify the rate process (PDF pp. 4-5,
   pp. 33-34). A cumulative or time-averaged readout of a C1-L2 rate
   feature is therefore not licensable as evidence about the feature
   itself. Reinforces the primary-metric pre-commitment (the
   candidate sharpening queued at deep-read 55, log ## 69): the primary
   metric must be declared on the non-integrated quantity before any
   data arrives. No queue change.

3. [interpretation caution] The limiting price and volatility Brownian
   drivers come out INDEPENDENT, and the paper states the two reasons:
   the two processes are scaled differently in space and the price
   changes are conditionally deterministic in this model class
   (Theorem 2.9 discussion, PDF pp. 11-12; correlation enters only via
   the Remark 2.10 marked-kernel extension, not carried through, PDF
   pp. 11-12). Any apparent correlation between flow features and
   volatility in raw data under near-critical scaling is therefore a
   modelling convention of the marking, not a microstructure law in
   either direction; a C8-adjacent "compression moves volatility with
   sign X" reading must pre-declare its marking convention.

4. [interpretation caution] The initial condition is an assumed decay:
   the residual impact of pre-window events is modelled as Vn,0·Φ(t),
   decaying at the heavy-tail rate, and the paper motivates it as the
   conditional stationary mean (Assumption 2.4(2) and Remark 2.5,
   PDF pp. 9-10; contrasted with a different convention at PDF p. 10).
   Inference near the start of any finite window sits on this boundary
   convention — the window-edge/burn-in caution class the programme
   already carries; any L2 fitted window must declare its initial-impact
   convention and its burn-in, or the first part of the window is
   unmodelled.

5. [source-quality note] The expanded index lists year 2023 (the v1
   origin); the acquired extract is arXiv:2312.08784v3 stamped 25 Mar
   2026 with a title-page date line of "March 26, 2026" (one-day
   mismatch, PDF p. 1). The bibliography carries two Xu references ([59],
   [60]) with IDENTICAL page ranges 34(3):2733-2798 (PDF pp. 37-38), at
   least one of which is a citation slip. Unpublished preprint; check the
   published version before any formal citation outside this note.

## What this paper would have killed if we had done it wrong

Two artifacts were avoided by standing discipline. The roughness death:
reading slow-decaying persistence or apparent roughness in the L2
intensity data and booking it as a genuine long-memory "fixed
characteristic" of the market — when this paper proves the rough
fractional limit is manufactured, exactly and cleanly, by a strictly
stable power-law Hawkes null whose branch ratio approaches one at the
rate the kernel tail prescribes (Assumption 2.4, Theorems 2.6-2.7, PDF
pp. 9-11), i.e. roughness is the null product of the already-armed
near-critical regime, not a signature. The aggregation death: having
read a compression-rate feature through its cumulative or
time-averaged statistic, judged it well-behaved, and booked a claim on
it — when Section 3.7 proves an integrated statistic can converge to a
well-identified limit whose rate process still diverges at the origin,
so integrated smoothness is precisely not evidence about the rate
feature (PDF pp. 33-34). Neither artifact survives the near-instability
estimator-discipline family, the primary-metric pre-commitment, or the
frozen-constant regime-window pre-declaration already in the queue;
neither licenses any change to C1-L2's or C8's kill lines.

## Standing caveat

Everything here is theorem, not measurement: a univariate single-kernel
model, no estimation methodology, no data application, and the main
results require the full joint scaling trajectory of Assumptions 2.4 and
2.8 (sufficient choices are exhibited at PDF p. 33), not merely ζ close
to one. The price process is conditionally deterministic before marking;
the leverage effect is out of scope of the carried proofs (Remark 2.10,
PDF pp. 11-12). The authors themselves point to the open question of
whether estimated roughness is fact or artefact (PDF p. 3, citing
Cont-Das). This is an arXiv v3 with a date-line mismatch and a
bibliography slip on the acquired copy; the published version should be
checked before any formal citation. Nothing here is programme evidence;
under the library invariant it is ammunition, not support.
