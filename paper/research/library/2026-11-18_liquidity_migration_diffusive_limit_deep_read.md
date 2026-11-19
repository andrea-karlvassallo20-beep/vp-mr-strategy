# Diffusive Limit of Hawkes Driven Order Book Dynamics With Liquidity
# Migration — deep-read note

Paper: Levon Sarkis Mahseredjian, "Diffusive Limit of Hawkes Driven
Order Book Dynamics With Liquidity Migration" (arXiv:2511.18117v1
[q-fin.MF], dated October 2025, stamp 22 Nov 2025; single-author
theoretical preprint, zero citations). Triage: score 31, slug
x5db64b_diffusive_limit_of_hawkes_driven_order_book_dynami
(edge_triage_scores.json). Parallel-fire slot 24 assignment, verified
at read time: no deep-read note for this slug existed and no open or
merged PR covered it. Extract: 18 pages, page-marked, complete
(docs/library/text/x5db64b_diffusive_limit_of_hawkes_driven_order_book_dynami.txt).

Read line: Library deep-read session 34, null-time session 38. Read in
full (the paper is 17 pages of content plus references; every section,
including the generator algebra, was read against the ONE question:
what here would kill C1-L2 or C8 faster, or change their kill lines?
Source: legally acquired OA copy, page-marked shelf extract as above.
The queue's next-UNREAD pointer is untouched by this session (the
pre-assigned slot paper was read instead of consuming the pointer).

## The paper in one paragraph

A purely theoretical mesoscopic model of the FIFO limit order book in
which every microscopic event type — limit arrivals,
cancellations/market removals, and a newly introduced event class of
LIQUIDITY MIGRATION between neighbouring price levels — is driven by
a multivariate Hawkes process with exponential kernels (PDF pp. 5-9).
The mid is held fixed and the spread pinned at two ticks so queue
indices are fixed tick distances from the mid; the paper states
explicitly that without the constant spread the queue vectors change
dimension and the tightness conditions for the scaling limit fail (PDF
pp. 7-8). Under Ethier-Kurtz-style diffusive rescaling (time x n,
volumes / sqrt(n)), a Taylor expansion of the microscopic generator
yields a reflected SDE per queue level in which Hawkes-driven
migration enters ONLY as a discrete Laplacian drift term
alpha_b(x_{k-1}+x_{k+1}-2x_k) with a history-dependent coefficient
(Eq. 17, PDF p. 13; Theorem 4.1 and Eq. 18, PDF pp. 10-11, 14), and
the diffusion covariance of queue volumes is pinned in closed form by
the Hawkes branching structure through a functional CLT:
Sigma_X = C(I-K)^{-1} diag(Lambda) (I-K)^{-T} C^T, with rho(K) < 1 the
stability condition (Eqs. 19-20, PDF pp. 14-15). The work is "entirely
theoretical" with no calibration anywhere (PDF p. 1); calibration,
numerical schemes, a continuum-level SPDE limit and enriched kernels
are all named as future research (PDF pp. 16-17).

## Findings, graded (does any kill line move?)

NO kill line changed. NO new candidate sharpening. The paper contains
no empirical result anywhere — no dataset, no fit, no estimate — and
uncalibrated theory licenses reading disciplines and reinforcement of
standing rules only, which is its honest ceiling. All seven C1-L2 kill
lines and C8's K1-K11 stand exactly as frozen. Findings, page-cited:

1. [interpretation caution] The paper's own mathematics forecloses a
   "liquidity migration" directional feature: migration is symmetric by
   construction — the per-unit migration rate toward the mid equals the
   rate away from it, a^{b,+} = a^{b,-} = a^{b,i} (PDF p. 9) — and after
   scaling it survives only as the discrete Laplacian term in the
   drift (Eq. 17, PDF p. 13; Theorem 4.1, PDF pp. 10-11). Depth
   draining at level k and reappearing at k plus-or-minus 1 is, in
   this framework, drift-neutral depth redistribution; directional
   content can live only in the arrival-versus-removal imbalance
   h_i = f_i - g_i (PDF p. 13, Eq. 17). Discipline recorded here
   BEFORE any C5/C6 depth feature exists, in the same spirit as C1-L2
   kill line 7(a): any future depth-panel feature narrating
   "liquidity migrating away from the touch" must beat a
   pre-declared symmetric-Laplacian null built from the same depth
   panel (a depth-smoothing process with no direction) before any
   directional claim is written into a pre-registration; a feature that
   adds nothing beyond that null is depth smoothing wearing a costume.
   This is the depth-panel analogue of the OFI-layer CKS tautology
   control; it creates no new spec text now, it binds a future
   pre-registration that does not exist yet.

2. [reinforcing, no new item] The queue-volume covariance is a
   closed-form common factor built by the branching matrix: Sigma_X =
   C(I-K)^{-1} diag(Lambda) (I-K)^{-T} C^T (Eq. 20, PDF p. 15), with the
   shared (I-K)^{-1} amplifier forcing correlated fluctuation across
   ALL tracked price levels of a side whenever excitation is present.
   This supplies the mechanistic reason a market-book first principal
   component exists at all, and therefore why amendment A5's first-PC
   definition is the correct nuisance control for K8: a trigger whose
   information lives only in the depth common mode must be expected to
   die there, and K8 killing it would be the model-consistent outcome,
   not a surprise. The A5/K8 texts bind as written; nothing queued.

3. [reinforcing, no new item] The diffusion limit and its FCLT exist
   only under strict stationarity: the stability condition rho(K) < 1
   is imposed "uniformly in n" for non-explosion, stationary
   intensities and the functional CLT (PDF pp. 7, 10, 14-15). This
   reinforces K7 as written: a T-H window read at the estimator's cap
   (rho-hat >= 0.949) is a window where the stationary theory through
   which branching is interpreted has no licence — the reading
   measures the estimator's boundary, not a near-critical market. It
   also corroborates the queued ACF-shape/estimator rules from the
   Functional Limit Theorems read (deep-read 17): subcritical
   asymptotics and near-critical behavior are different regimes with
   different limits, and readings near the boundary inherit the
   ambiguity, not a clean cascade number.

4. [interpretation caution] The fixed two-tick spread is load-bearing,
   not decorative: "Without this assumption, the best bid and best ask
   queues would shift position as the spread fluctuates, causing the
   queue vectors to change dimension over time" (PDF pp. 7-8). The
   programme's venue is the opposite regime — a maximal-small-tick
   perp with a breathing spread (the queue-imbalance note's
   spread-pinning mechanism). On such a venue, a level index defined
   relative to the mid and one defined relative to the best quote
   coincide when the spread is pinned and silently DIVERGE —
   re-defining "level-2 depth" — whenever the spread moves a tick.
   Discipline for the future C5/C6 pre-registration (and any depth
   covariate recorded from t0 in C1-L2): the level-indexing convention
   (mid-relative vs best-relative) must be declared before the feature
   exists. This converges with the queue-label convention declaration
   queued at deep-read session 32 from the tie-break side; it is
   recorded as a caution here, adding no new spec text.

5. [source-quality note] arXiv v1, single author, zero citations, no
   calibration; the intensity expansions that seed the generator
   (Eqs. 12-14, PDF p. 11) are asserted, not derived from the Hawkes
   specification in the extract, and Theorem 4.1 is stated ahead of
   the section-5 material it points to (PDF pp. 10-11). The reference
   list is defective: [1] Hambly-Kalsi-Newbury cited to "arXiv:2018"
   (a year, not an identifier), [4] Cont-de-Larrard and [9]
   Abergel-Jedidi cited to the same arXiv ID 1104.4596, and [12]
   duplicates [5] (PDF pp. 17-18). None of this falsifies the
   derivations, but nothing here may be cited as established theory
   until a published or revised version is checked; more importantly,
   no empirical claim can be laundered from a paper that contains none.

## What this paper would have killed if we had done it wrong

If the C5/C6 feature library had been written from this paper's
vocabulary, it would have reached for "liquidity migration" as a
FEATURE: depth leaving the touch for deeper levels sounds exactly like
an anticipatory signal ("the book rearranges before the move"). The
paper's own mathematics says the opposite: built symmetrically,
migration is depth smoothing with zero directional drift content, and
the cross-level covariance it generates is common-mode variation that
A5's first-PC control exists to strip. A depth-migration feature
admitted without a pre-declared symmetric-Laplacian null would have
been laundered smoothing — the same failure mode kill line 7(a) was
armed against in the OFI layer, rediscovered one layer up in the depth
panel, and this time caught before the feature library exists. The
counterfactual reinforces why cautions are recorded against FUTURE
pre-registrations while they are still cheap.

## Standing caveat

A library is ammunition, not evidence. This paper has no empirical
content whatsoever, so it licenses reading disciplines and mechanistic
reinforcement only, never support for any program claim. Its scope is
narrower than its title: static mid, pinned two-tick spread, unit order
sizes, FIFO, symmetric migration, best-quote queues excluded from the
state (PDF pp. 7-9), bid side developed in full with the ask side
"defined analogously" (PDF p. 9) — quote pegging, iceberg refresh,
spoof-cancel and asymmetric re-placement are all outside the model.
Buffer boundary migrations are "blocked consistently with the pinning
conditions" (PDF p. 10), an assumption stated without elaboration.
arXiv v1 (22 Nov 2025 stamp), single author, zero citations: check for
a revised or published version before any formal citation of the
theorems.
