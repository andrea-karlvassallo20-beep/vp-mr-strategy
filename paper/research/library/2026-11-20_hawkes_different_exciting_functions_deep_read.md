# Deep-read session 62 (null-time session 73, log ## 80) — the Hawkes process with different exciting functions; generation-varying kernels shown observationally collapsible into multivariate form; boundary-stability results subcritical-only; zero sharpenings queued

Behzad Mehrdad (Courant Institute, NYU) and Lingjiong Zhu (Florida State
University), "On the Hawkes Process with Different Exciting Functions"
(arXiv:1403.0994v3 [math.PR], 3 Sep 2017, v3 of a 2014 preprint). Pure
probability theory for the Fierro-Leiva-Møller (2015) generalized linear
Hawkes model in which each birth GENERATION n carries its own exciting
function γn: convergence to equilibrium, an embedding into multivariate
Hawkes processes, large and moderate deviation principles, and two
finance-flavored applications (microstructure noise / Epps effect
heuristic, and asymptotic ruin probabilities). No estimator, no data, no
numerics anywhere.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xd0ee69_on_the_hawkes_process_with_different_exciting_func.txt,
28 pp., page-marked). Next UNREAD triage-rank entry (score 26).

## The paper in one paragraph

The model under study (PDF pp. 2-3): immigrants arrive as an
inhomogeneous Poisson process N^0 with intensity γ0(t), and each event
of generation n−1 spawns generation-n offspring through its OWN kernel
γn, with the whole superposed counting process N = Σ N^n; if γ0 is
constant and γn ≡ h the classical linear Hawkes process is recovered
(Eq. 1.3, PDF p. 3). Under Assumption 1 — γ0̄ exists and
ρ := sup_n ‖γn‖_{L1} < 1 (PDF p. 3) — the authors prove weak and (under
a first-moment condition on γ1) strong asymptotic stationarity via a
shifted-process coupling (Theorem 1, PDF pp. 4-6), show that
partitioning the generations into d sets Ai produces aggregates
Ni = Σ_{n∈Ai} N^n that are mutually exciting and strictly more general
than the classical multivariate Hawkes process (with the odd/even
partition already giving a bivariate Hawkes pair, Eqs. 3.3-3.9,
PDF pp. 6-8), establish a large deviation principle for Nt/t with an
explicitly recursive scaled cumulant generating function Γ(θ)
(Theorems 3 and 6, PDF pp. 9-11), a moderate deviation principle with
Gaussian rate J(x) = x²/(2σ²) (Theorem 8, with the σ² of
Fierro et al., PDF pp. 12-21), and an LDP for i.i.d.-marked event sums
(Theorem 7, PDF pp. 11-12). Section 5 gives a heuristic signature-plot
and Epps-effect computation for differences of generational aggregates
(Proposition 16 and the O(τ) argument, PDF pp. 21-23) and
Laplace-type asymptotics for ruin probabilities of a risk process with
these arrivals (Theorems 17-19, PDF pp. 25-27).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. The default grade is
earned twice over: this is a theorem paper with no estimation content,
no data, and not one number in it (PDF pp. 1-28), so its findings can
only shape READING DISCIPLINE around models the programme already
declares; and every discipline-relevant mechanism it touches
(stability of the branching structure, family pre-declaration,
asymptotic-in-horizon limits) is already held by standing or queued
rules. The findings below therefore interpret, they do not queue.

1. [interpretation caution] Generation-varying kernels are
   OBSERVATIONALLY COLLAPSIBLE: any realized single-stream Hawkes data
   can be decomposed into latent generations in more than one way, and
   the paper's own multivariate connection is a partition-of-generations
   ARBITRATION (Eqs. 3.10, PDF p. 8) — the aggregate processes
   (N1,...,Nd) are "more general than the classical multivariate Hawkes
   process" exactly because the generational assignment is a modelling
   choice, not an observable. Generation membership of a realized event
   is never identifiable from event times alone. A future C8 trigger
   layer tempted by "each cohort has its own kernel" flexibility must
   therefore treat a generation-partitioned fit as a fully-registered
   analyst degree of freedom: different partitions give different
   branching allocations from the SAME data, the exact laundering
   the pre-declared kernel family, named estimator identity, per-branch
   rule and sign-register rule exist to prevent. Extends those rules'
   reading from kernel shape and branch sign to the latent-branch
   ASSIGNMENT itself; no queue change.

2. [reinforcing, no new item] Every result in the paper — stationarity
   (Theorem 1), the Law of Large Numbers m = γ0(1 + ‖h‖)/(1 − ‖h‖‖g‖)
   for the two-kernel case (Eq. 3.5, PDF pp. 6-7), CLT, LDP, MDP —
   lives strictly BELOW criticality: Assumption 1(ii) requires
   ρ = sup_n ‖γn‖_{L1} < 1 (PDF p. 3), and at ρ ≥ 1 none of these
   limits exist. A C8 criticality reading (branching ratio near unity)
   estimated BY a subcritical-only theory therefore inherits a
   built-in survival-condition bias: the stability assumption is doing
   as much work as the data. This is the page-cited general-form
   backing for the already-queued self-excitation regime-window
   pre-declaration and the standing caution that boundary-near
   criticality estimates are boundary solutions; no new item.

3. [interpretation caution] The stationary version needs a CONSTANT
   immigration rate: γ0(t) ≡ γ0 is assumed for Theorem 1, and the
   authors themselves flag weakening it as open (Remark 2, PDF p. 6).
   Any translation of the LDP rate function Γ(θ), the σ² of the CLT
   (Eq. 1.11, PDF pp. 3-4), or the Epps/signature limits of §5.1 into
   a market window with time-varying baseline intensity (sessions,
   open/close, regime shifts) is licensed for CONSTANT-γ0 stretches
   only; and all deviation results are asymptotic in t with NO
   finite-horizon constants anywhere (PDF pp. 9-21). No magnitude from
   this paper may enter any spec, and no tail bound from it may be
   applied to finite windows. Reinforces the queued clock and
   regime-window pre-declarations; no queue change.

4. [cost-survival ammunition] The ruin application (Theorems 17-19,
   PDF pp. 25-27) converts the arrival LDP into asymptotic ruin
   estimates for a surplus process u + pt − ΣCi with Hawkes arrivals.
   Relevant only if a future K7-style cost-survival layer ever exists
   (one does not today); such a layer must carry every assumption
   verbatim: subcritical ρ < 1, i.i.d. claims independent of the point
   process, the net-profit condition p > mE[C1] (Eq. 5.24, PDF p. 25),
   light or subexponential (not general) tails, and the u → ∞
   horizon; finite-capital, finite-window drawdown bounds are not
   derivable from these theorems. Nothing here is absorbed now.

5. [source-quality note] arXiv-only math.PR preprint, v3 three years
   after v1, acknowledged to the "editor and referees" (which suggests
   a journal submission) but with no published version identified in
   the extract; zero empirical content, zero estimation methodology,
   zero citations recorded in the index (cited: 0). Safe to cite for
   theorems with the arXiv-version caution attached; check for a
   published version before formal citation. Grade honestly: a
   score-26 access-value read, not an evidence source.

## What this paper would have killed if we had done it wrong

Had the programme adopted a generation-varying Hawkes trigger because
the theory blesses per-cohort kernels, the fit would have arbitrated
the latent generational partition post hoc — the same realized stream
decomposes into (h, g, h, g, ...) or into arbitrary Ai-splits with
DIFFERENT implied branching allocations (PDF pp. 6-8) — and an
unregistered choice there would have manufactured whatever
cross-excitation or damping structure the analyst's prior wanted,
laundering the branch-sign evidence the per-branch and sign-register
rules require two-sided and pre-declared. Equally, had the paper been
read as support for a criticality-tolerant trigger, the subcritical
assumption ρ < 1 (PDF p. 3) holding up every theorem would have been
silently imported as if it were a finding about markets rather than a
condition of the model — exactly the boundary-solution laundering the
queued regime-window pre-declaration and the boundary-solution rule
exist to prevent.

## Standing caveat

The paper is asymptotic probability theory, not market science: all
results hold in the t → ∞ (LDP/MDP, ruin) or s → ∞ (stationarity)
limits under constant immigration and subcritical ρ, with no
finite-horizon constants (PDF pp. 3-27). The multivariate connection
is by generational partitioning only and provides no identifiability
result for the partition from data. The finance section (§5.1,
PDF pp. 21-23) is explicitly heuristic (the authors compute
stationary expectations and argue orders in τ), and §5.2 is insurance
ruin, not trading. arXiv v3 caution stands: check the published
version before formal citation.
