# Deep-read session 34 — Mahseredjian, "Diffusive Limit of Hawkes Driven Order Book Dynamics With Liquidity Migration"

Library deep-read session 34 (null-time session 38, log entry
## 42). Levon Sarkis Mahseredjian, solo author, arXiv:2511.18117v1
[q-fin.MF], v1 stamped 22 November 2025, title page October 2025,
18 pp. text extract, page-marked. Read 2026-11-19, against
ONE question: what here would kill C1-L2 or C8 faster, or change
their kill lines? Source: legally acquired OA copy
(docs/library/text/x5db64b_diffusive_limit_of_hawkes_driven_order_book_dynami.txt).
Next UNREAD triage-rank entry (score 31, x5db64b), after the
TradeFM paper consumed at deep-read session 33.

## The paper in one paragraph

An entirely theoretical mesoscopic limit-order-book model: each
side of the book is a vector of integer queues indexed by tick
distance from a fixed mid under a constant two-tick spread (PDF
pp. 7-8), with limit arrivals, cancellations-plus-market-removals,
and a new event class, migration of one unit of volume between
neighbouring price levels, each driven by multivariate Hawkes
intensities with exponential kernels (PDF pp. 8-9). Under
diffusive rescaling, time accelerated by n and queues renormalised
by root n (PDF pp. 10-11), the generator of the rescaled process
is Taylor-expanded (PDF pp. 11-13) and converges to a generator of
a reflected diffusion with normal reflection at zero (PDF
pp. 13-14, Theorems 4.1 and 5.1), whose per-level drift and
state-dependent diffusion are coupled across levels by a discrete
Laplacian term with a Hawkes-modulated strength — the footprint of
the migration events (PDF pp. 5, 9, 14). The paper then derives
the mesoscopic covariance from the multivariate Hawkes FCLT: with
integrated kernel matrix K under the stability condition
spectral radius(K) < 1, the asymptotic event-count covariance is
(I-K)^-1 diag(Lambda-bar) (I-K)^-transpose, mapped to queue-volume
covariance through an incidence matrix C (PDF pp. 14-15). The work
states it relies on no empirical calibration anywhere and defers
kernel estimation and validation to future research (PDF
pp. 1, 16-17).

## Findings, graded

NO kill line changes. NO new candidate sharpening.

1. **[reinforcing, no new item]** The Laplacian coupling is a
   second corpus for the queue-state conditioning family's
   premise, at one remove. In the limit, a queue level's own
   evolution carries a term proportional to the sum of its
   neighbours minus twice itself (PDF pp. 11, 14, eq. 18), so
   even in a zero-intelligence Hawkes world a per-level reading
   is structurally incomplete without the adjacent levels: the
   migration mechanism exists precisely because liquidity state
   propagates across levels, the same premise already standing
   behind the queued queue-state conditioning rule (deep-read
   sessions 26-27) and the book-state mix disclosure (deep-read
   28). The paper is theory, and its Laplacian never enters any
   spec as a functional; no parameter transfers.

2. **[reinforcing, no new item]** The fixed-spread, mid-anchored
   coordinate grid is assumed exactly because moving labels break
   the machinery. The constant two-tick spread is imposed so that
   queue indices remain fixed tick distances from the mid; the
   author states plainly that without it the queue vectors would
   change dimension as the spread fluctuates and the regularity
   and tightness conditions required for the scaling-limit theorem
   would fail (PDF pp. 7-8). This is the queue-label convention
   lesson (deep-read session 32) restated from the modelling side:
   mid-anchored labels are a convention whose stability is an
   assumption, not a property of any book. On the programme's
   venue the spread moves, so no derivation premised on a frozen
   mid grid transfers; the already-queued declaration components
   cover this and nothing here tightens them further.

3. **[reinforcing, no new item]** The covariance derivation is a
   sibling of the branching-ratio lesson already sealed into the
   math layer. The mesoscopic fluctuation covariance is
   (I-K)^-1 diag(Lambda-bar) (I-K)^-transpose through C (PDF
   pp. 14-15, eqs. 19-20): the (I-K)^-1 amplification is the same
   near-criticality magnification that the Hawkes branching
   family uses, with the stability condition spectral
   radius(K) < 1 stated twice (PDF pp. 7, 15). A misread
   beta-family kernel inflates the estimated covariance the same
   way it inflated the deep-OFI beta factor the math verification
   caught; the record already carries that guard. No new item.

4. **[interpretation caution]** The paper's own derivation is
   asserted at joints, and nothing in it licenses a numerical or
   structural expectation on any market. The equilibrium intensity
   expansions (eqs. 12-14, PDF p. 11) are assumed with the
   effective coefficients declared "determined by the Hawkes
   kernels (see Section 6)" — but Section 6 derives only the
   FCLT covariance, not sigma-squared, f, g or the migration
   baseline; Theorem 4.1 (PDF p. 11) is stated before the
   Section-5 generator machinery it rests on, with full proofs
   delegated to a section that derives the limit generator rather
   than the theorem's tightness and uniqueness claims; and key
   algebraic steps are asserted as "one checks" (PDF p. 12). Any
   future citation of this lineage must cite the assumption stack,
   never the theorems as facts about books. Applied to the
   record: nothing here can kill C1-L2 or C8 faster and nothing
   can change a kill line, because the paper carries no empirical
   claim at all.

5. **[source-quality note]** Solo-author arXiv v1 stamped 22
   November 2025, under a month old at reading; no journal record
   or peer review checked at reading; the framework is an
   acknowledged assembly of Hambly-Kalsi-Newbury and
   Hambly-Ledger scaling arguments, the Horst-Paul Hawkes
   diffusion limit, Ethier-Kurtz generator convergence and the
   Bacry-Gaiffas-Muzy FCLT, with the novel element being the
   symmetric Hawkes-modulated migration events and their Laplacian
   footprint (PDF pp. 4-5, 12-13). Graded as a young-theorist
   theoretical draft: coherent in intent, incompletely verified at
   joints, zero empirical content, honest about the calibration
   debt (PDF pp. 16-17). Published version to be checked before
   any formal citation. Triage score 31 is an access-value rank,
   not a promise.

## What this paper would have killed if we had done it wrong

If the programme had read a diffusion-limit theorem as a statement
about markets, it could have imported two silent assumptions as
properties of BTCUSDT: first, that queue labels anchored to the mid
form a stable coordinate grid — an assumption the author freezes
the spread to guarantee and that fails by construction on any
venue where the spread moves; second, that liquidity migration is
a symmetric neighbour-coupling with Hawkes-decaying strength — a
mechanism invented for tractability, with no empirical corpus
anywhere in the paper and calibration explicitly deferred. A
future C1-L2 or C8 arm citing either as motivation would have
laundered a modelling convenience into a market-truth claim. The
standing discipline forecloses both without any new rule: the
queue-label convention declaration requires the reference
construction declared on TRAIN, and the library-is-ammunition
caveat bars any paper's structure, fitted or unfitted, from
entering the record as evidence for a programme claim.

## Standing caveat

Entirely theoretical; zero empirical calibration, zero data, zero
stylized-fact verification, zero forecasting content. Constant
two-tick spread, fixed mid, unit order and cancellation sizes,
FIFO queues, exponential Hawkes kernels, symmetric migration,
large-tick asset framing (PDF pp. 7-9); no crypto, no BTCUSDT, no
futures, no anonymous flow. The Laplacian coefficient, the
intensity expansions, the covariance formulas and both theorems
are properties of the assumed microscopic specification, not of
any market. Laundering directions named. INTO — nothing enters any
spec, default or calibration; the note's only residue is
corroboration, already covered: neighbour-level structure matters
(queue-state conditioning family), mid-anchored labels are a
convention (queue-label convention declaration), and the
(I-K)^-1 covariance amplification is the branching-ratio lesson.
OUT — the Laplacian term, the migration mechanism, the theorems,
the covariance expressions and any implication that queue
dynamics are diffusive at any horizon are never cited as expected
behavior of any market the programme measures, never as expected
BTCUSDT book behavior, and never as evidence that any programme
feature carries information.
