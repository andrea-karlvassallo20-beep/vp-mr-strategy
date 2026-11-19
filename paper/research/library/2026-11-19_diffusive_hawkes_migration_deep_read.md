# Deep-read note — "Diffusive Limit of Hawkes Driven Order Book Dynamics With Liquidity Migration"

**Session:** null-time session 38 (deep-read session 34, parallel-slot read; the
substitution below explains why this slot did not read its pre-assigned paper).
**Author:** Levon Sarkis Mahseredjian. **Year:** 2025.
**Venue:** arXiv:2511.18117v1 [q-fin.MF], 22 Nov 2025. What the paper is: a purely
theoretical mesoscopic limit-order-book model — microscopic Hawkes-driven per-level
birth/death dynamics plus a mathematically defined liquidity-migration event between
neighbouring price levels, taken through an Ethier-Kurtz diffusive rescaling to a
reflected SDE system for queue volumes with a discrete-Laplacian coupling term, plus a
functional central limit theorem (FCLT) pinning the mesoscopic diffusion covariance to
the Hawkes branching structure. No data, no calibration, no empirical claim anywhere.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legal-OA page-marked shelf extract
`docs/library/text/x5db64b_diffusive_limit_of_hawkes_driven_order_book_dynami.txt`
(18 pp.). Selection, declared: this slot was pre-assigned Maciejewski, "Packets,
Transactions and Queues" (score 34, xc5ba34); a note and log entry for that slug were
verified already on main (null-time session 31, deep-read session 23, default grade),
so it was not re-read. This slot's verification found the standing next UNREAD pointer,
TradeFM (score 31, xe7dc7f), claimed by two other slots' open PRs (both readings have
since landed on main as deep-read session 33); per the no-duplicate rule this session
took the next UNREAD entry after it, triage rank 31 (score 31, slug x5db64b). Verified
before the read: no note for the slug among the 34 existing notes in
paper/research/library/ and no open PR covers it.

## Findings, graded (does any kill line move?)

NO kill line changed; ONE candidate sharpening queued, PENDING OWNER RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] **The covariance-projection
   control for spatial-propagation readings.** Mechanism, proven in the text: under
   the paper's stability condition (spectral radius of the integrated kernel strictly
   below 1, uniformly in n, PDF p. 10), the FCLT gives the multivariate event-count
   fluctuation covariance ΣN = (I − K)−1 diag(Λ̄) (I − K)−⊤ (Eq. 19, PDF pp. 14-15),
   and because every mesoscopic queue volume is a linear functional of the event counts —
   an incidence matrix C mapping each event type to its queue increments (PDF p. 15) —
   the entire cross-level queue-fluctuation covariance is the projection ΣX = C ΣN C^T
   (Eq. 20, PDF p. 15), with spatial migration entering only the DRIFT: the Laplacian
   coupling term A(X_{i+1} + X_{i−1} − 2X_i) in the limiting reflected SDE (Thm 4.1,
   PDF pp. 10-11; generator Eq. 17, PDF p. 13; SDE Eq. 18, PDF p. 14). Consequence: on
   any stable endogenous event flow, cross-level depth co-movement in covariance carries
   zero spatial information — a common branching structure projects level-correlated
   queue fluctuations through the incidence matrix with no migration mechanism at all.
   Pre-declaration text: any C1-L2 L2-arm or C8 arm that cites cross-level depth
   covariance as liquidity migration, depth reinforcement, or spatial propagation must
   first declare and control the temporal-excitation projection channel — an
   excitation-only null (branching fit with the migration channel removed, per the
   already-queued per-branch rule with bootstrap CIs) must fail to reproduce the cited
   cross-level structure before a spatial reading is admissible; a spatial reading that
   does not survive the projection null is recorded as projection, never as migration.
   Harder to pass because a depth-coupling feature must now survive an
   excitation-projection null, not only the shuffled-arrival placebo and the sign
   placebos; it hardens the queued market-book first-PC factor (C8 A5) and the
   queue-state conditioning rule by naming the exact mathematical channel through which
   common-factor laundering enters the second moments. No kill line moves; nothing is
   armed by this note.

2. [reinforcing, no new item] The scaling limit exists ONLY under a fixed two-tick
   spread: the paper holds the spread constant precisely because a moving spread changes
   the dimension of the queue vectors over time and breaks the tightness/regularity
   conditions of the limit (Section 3.1, PDF p. 7). A venue-model exhibit for the
   already-queued queue-label convention declaration rule (deep-read session 32) and
   the const-mid queuing-period risk-set rule (the library ritual's queue-reactive
   paper): fixed tick indices are not bookkeeping pedantry, they are an existence
   condition for cross-level statements — a feature defined on fixed level indices
   silently changes its conditioning state when the spread moves.

3. [reinforcing, no new item] Migration is built SYMMETRIC by assumption — the
   per-unit rate toward the mid equals the rate away from it (PDF p. 9), producing the
   clean Laplacian. The queue-reactive literature (front-vs-rear priority asymmetry,
   saturating cancel intensities) says real liquidity relocation is priority-driven and
   asymmetric. The Laplacian is a model choice, never a market law; the queued
   front-vs-rear separation rule stands, and no coefficient from this paper transfers.

4. [reinforcing, no new item] The branch kernel K determines BOTH the stationary mean
   event rates, Λ̄ = (I − K)−1 μ (Eq. 7, PDF p. 7), and the entire fluctuation
   covariance (Eq. 19, PDF pp. 14-15) — a worked mathematical exhibit for the queued
   per-branch rule (session 9) and the W-ladder/estimator-mode register: the same
   branching object propagates into every moment, so an estimator-mode change moves
   all downstream readings together, never one at a time.

5. [source-quality note] Entirely theoretical: the abstract and the conclusions state
   it without embarrassment ("without relying on empirical calibration", PDF p. 1;
   calibration is future research, PDF pp. 16-17). Single author, arXiv v1, no journal
   record checked at reading; heavy reliance on Ethier-Kurtz [10], Lions-Sznitman [11],
   and the Horst-Paul / Hambly-Ledger scaling-limit lineage [6][7], correctly credited.
   Two internal citation inconsistencies visible in the reference list alone: [4]
   (Cont-de Larrard) and [9] (Abergel-Jedidi) carry the SAME arXiv number (1104.4596),
   and [5] ("Queue-reactive Hawkes processes for limit order books") and [12]
   ("A generalized method for multivariate Hawkes processes") carry the SAME arXiv
   number (1502.04592) under two different titles — at least one member of each pair
   is wrong, and both sit in the same citation families the programme's record cites;
   flagged for verification before any formal citation of this paper or of [4][5][9][12].

## What this paper would have killed if we had done it wrong

If a C1-L2 depth feature had ever cited cross-level covariance as evidence of liquidity
migration or depth-reinforcement propagation without the projection control, pure
endogenous event flow would have been booked as a spatial market mechanism — a durable,
regime-stable-looking artefact (the projection is a theorem, so it holds in every
window), uncaught by label placebos because it lives entirely in the features, and
laundered by the same market-book common-factor channel C8's A5 first-PC control
already suspects. The control makes that channel inadmissible as a positive claim:
excitation-projection is the default explanation of cross-level covariance, and only
its failure licenses a migration reading.

## Standing caveat

Theory only: no market, no venue, no instrument, no parameter values, no empirical
regularity measured; large-tick two-tick-spread boundary model; everything is an
existence-and-form result. Nothing in it licenses any measured or live activity; the
paper enters the record as feature-design discipline and nothing else. No fitted
value from this paper or from its cited lineage enters any spec, default, or
calibration, and no cross-level covariance claim from any future gated window may be
narrated as spatial propagation without the projection null. arXiv v1: check for a
published version before formal citation, and check [4][5][9][12] against arXiv before
citing this paper's own references anywhere in the record.
