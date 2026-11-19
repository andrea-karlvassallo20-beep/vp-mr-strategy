# Deep-read session 34 — null-time session 38: the Hawkes
liquidity-migration diffusive limit graded pure theory, default

Levon Sarkis Mahseredjian, "Diffusive Limit of Hawkes Driven Order Book
Dynamics With Liquidity Migration" (arXiv:2511.18117v1, 22 Nov 2025,
single author, October 2025 stamp). An entirely theoretical mesoscopic
model: a multivariate Hawkes-driven limit order book whose per-level
dynamics include Hawkes-modulated migration of unit liquidity between
adjacent tick levels, shown under diffusive rescaling to converge to a
reflected SDE system with a discrete-Laplacian coupling across levels,
with the mesoscopic covariance expressed in closed form through the
Hawkes kernel matrix by the multivariate Hawkes FCLT.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x5db64b_diffusive_limit_of_hawkes_driven_order_book_dynami.txt,
18 pp., page-marked). Next UNREAD triage-rank entry not covered by an
open PR or a landed note (score 31; see the log entry for the pointer
state and the in-flight parallel claims on the two entries above it).

## The paper in one paragraph

Each side of the book is a vector of integer queues indexed by tick
distance from a fixed mid, with the spread pinned at two ticks so the
state space keeps constant dimension ("Without this assumption, the
best bid and best ask queues would shift position as the spread
fluctuates... violating the regularity and tightness conditions
required for the scaling limit theorem", PDF pp. 7-8); all order and
cancellation sizes equal one (PDF p. 8). Arrivals, removals, and
unit-volume migrations between neighbouring levels are driven by
multivariate Hawkes intensities (exponential kernels, PDF pp. 6-9), the
migration intensity symmetric inward and outward per unit of queue
volume, a^{i->i-1} = a^{i->i+1} (PDF p. 9), so migration enters the
limit as a discrete Laplacian smoothing term. Under diffusive
rescaling (time by n, volumes by sqrt(n), equilibrium intensity
expansions assumed, PDF pp. 10-11), the generator converges to that of
a reflected diffusion: drift = Hawkes arrival-minus-removal drift plus
the Laplacian coupling, reflection at zero via a Skorokhod term
(Theorem 4.1 and eqs. 16-18, PDF pp. 11-14). The diffusion covariance
is derived from the multivariate Hawkes FCLT under the stability
condition rho(K) < 1: Sigma_N = (I-K)^{-1} diag(Lambda-bar)
(I-K)^{-T} (eq. 19), hence the queue-volume covariance Sigma_X =
C Sigma_N C^T through an incidence matrix C mapping event types to
queue increments (eq. 20, PDF pp. 14-15). The paper is explicitly
"entirely theoretical... without relying on empirical calibration"
(PDF p. 1); calibration, cross-side coupling, continuum-level SPDE
limits, and state-dependent kernels are all future research (PDF
pp. 16-17).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Default grade; the
paper is a clean-theory worked exhibit of rules already standing in
the ratification queue, and the burden of proof for a sharpening was
not met.

1. [reinforcing, no new item] Queue-volume dispersion is a
   deterministic functional of the fitted branching structure,
   reinforcing the dispersion register and the estimator-mode and
   per-branch rules. The closed form Sigma_X = C(I-K)^{-1}
   diag(Lambda-bar)(I-K)^{-T}C^T (eqs. 19-20, PDF pp. 14-15) makes
   cross-level queue covariance exactly the kind of quantity the
   already-queued rules govern: it moves with every choice in the
   kernel-fitting pipeline (kernel form, cut-offs, thresholding) the
   same way the branching share does, and a dispersion reading is
   therefore an estimator-pipeline product, cross-readable with
   branching readings only under the declared estimator mode and
   per-branch discipline. Nothing new queued; the register as drafted
   governs. The formula licenses no import of any fitted covariance as
   a tolerance for any C1-L2 or C8 quantity.

2. [reinforcing, no new item] Stationarity is load-bearing twice, and
   the limit explodes toward criticality, reinforcing both the
   boundary-solution rule (deep-read session 5) and the near-critical
   regime-disclosure rule (deep-read session 17). Stability
   rho(K) < 1 is assumed uniformly in the scaling (PDF pp. 7, 10), and
   every covariance term carries (I-K)^{-1}: as the fitted kernel
   matrix approaches the boundary, the diffusion limit's covariance
   inflates by construction, not by information. A dispersion or
   covariance reading computed on a fit pinned at or rescaled to the
   boundary is a boundary artifact under the queued rules; the queued
   disclosure chain is the only admissible regime statement. Worked
   exhibit number three for the boundary lesson; nothing added.

3. [interpretation caution] The model's coordinate system exists only
   under a pinned spread and fixed mid, a second worked exhibit for
   the queued queue-label convention declaration (deep-read session
   32). The author states plainly that without the two-tick pinned
   spread the queue vectors change dimension and the scaling limit
   fails (PDF pp. 7-8). On any floating-spread venue (the C1-L2 venue
   included), tick-distance labels are convention-dependent exactly as
   the queued declaration component requires; a theory derived in
   pinned coordinates can never serve as the specification of a
   floating-spread feature, and any future borrowing of this model's
   level-indexed quantities must carry the same declaration the queued
   rule demands. Reading discipline; no queue change.

4. [interpretation caution] Migration symmetry is an assumption, not
   a market fact, and the model is size-silent. The inward and outward
   per-unit migration rates are set equal by construction (PDF p. 9),
   so the Laplacian is pure smoothing and the model is structurally
   silent about the pre-touch withdrawal asymmetry the C5 neighborhood
   cares about; all order and cancellation sizes equal one (PDF p. 8),
   so excitation is time-only, as in the prior compound-Hawkes reads.
   Neither the symmetric-Laplacian shape nor any harmonic depth
   profile it induces may be narrated as the expected spatial
   behavior of any market the programme measures, and a migration
   measured on event counts alone may not be narrated as volume flow
   (the size-state persistence comparator already governs that
   reading). No queue change.

5. [source-quality note] Single-author arXiv v1 preprint (22 Nov
   2025), explicitly entirely theoretical with no empirical
   calibration anywhere (PDF p. 1); one side of the book derived with
   the ask side "defined analogously" and no cross-side coupling
   (PDF p. 9); unit sizes, pinned spread, exponential kernels,
   equilibrium intensity expansions (12)-(14) as assumptions doing the
   limit's work (PDF pp. 10-11). Citation lapses on the record: refs
   [4] (Cont and de Larrard) and [9] (Abergel and Jedidi) both carry
   the identifier arXiv:1104.4596, and Hambly, Kalsi and Newbury is
   cited as "arXiv:2018" (PDF pp. 17-18). Grade at exactly that
   level; check for later versions before formal citation.

## What this paper would have killed if we had done it wrong

Had this clean derivation been quoted as support that liquidity
migration smooths the book on the C1-L2 venue, a no-calibration,
unit-size, pinned-spread abstraction would have been laundered into a
market mechanism: the very symmetry that produces the model's
Laplacian is an assumption the author needed for tractability (PDF
pp. 7-9), not a finding. Had the closed-form covariance (eq. 20, PDF
p. 15) been imported as a null, tolerance, or expected dispersion for
the C8 trigger bar or any C1-L2 depth feature, three machine
assumptions of the derivation — stationarity, pinned spread,
symmetric unit migration — would have been baked into a kill line
before any data arrived, and the line could then fire on the venue's
violation of assumptions rather than on the hypothesis. The
library-is-ammunition rule and the nothing-measured rule are what
prevented both.

## Standing caveat

Entirely theoretical; no calibration, no data, no out-of-sample
anything, by the author's own statement (PDF p. 1). The queue state
space requires a pinned two-tick spread and a fixed mid (PDF pp.
7-8); order sizes are units (PDF p. 8); migration is symmetric by
assumption (PDF p. 9); the ask side is analogous and uncoupled
(PDF p. 9); kernels are exponential (PDF pp. 6, 8-9); the limit
rests on assumed equilibrium intensity expansions (PDF pp. 10-11).
Nothing in the paper is applicable to a 24/7 crypto venue without
complete re-derivation, and nothing in it is citable as expected
book behavior of any market the programme measures. Laundering
directions named: INTO — nothing; no coefficient, Laplacian form,
covariance expression, or scaling regime enters any spec, default,
calibration, or tolerance, and the model may not be used as a
generative null for any C1-L2 or C8 arm without an owner-ratified,
pre-declared derivation of its assumptions on the programme's venue
and fields; OUT — the paper may not be read backwards as "migration is
symmetric" or "dispersion reveals the kernel" — the first is assumed,
and the second is an identification statement valid only under the
derivation's full assumption set, not a measurement claim about any
market.
