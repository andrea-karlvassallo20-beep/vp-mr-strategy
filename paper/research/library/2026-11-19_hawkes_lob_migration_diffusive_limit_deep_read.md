# Diffusive Limit of Hawkes Driven Order Book Dynamics With Liquidity Migration — deep-read

Library deep-read session 34 (null-time session 38). Levon Sarkis Mahseredjian,
"Diffusive Limit of Hawkes Driven Order Book Dynamics With Liquidity Migration"
(arXiv:2511.18117v1 [q-fin.MF], stamped 22 November 2025, dated October 2025): an
entirely theoretical mesoscopic limit-order-book model in which multivariate
Hawkes-driven arrivals, cancellations and liquidity migrations between
neighbouring price levels converge, under diffusive rescaling, to a reflected
SDE system for queue volumes with a discrete Laplacian coupling term and a
Hawkes-structure-determined diffusion covariance.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x5db64b_diffusive_limit_of_hawkes_driven_order_book_dynami.txt,
~18 pp., page-marked). Next UNREAD triage-rank entry (score 31).

## The paper in one paragraph

A single-author theoretical construction: each side of the book is a vector of
FIFO queues indexed by tick distance from a mid held fixed with a two-tick
spread, order arrivals, cancellations and unit-order market removals are
components of a multivariate Hawkes counting process, and each unit of volume
at level i independently attempts Hawkes-modulated migrations to levels i-1 and
i+1 at the same per-unit rate (PDF pp. 7-9). Under time-acceleration by n and
queue normalization by sqrt(n), with stability spectral radius strictly below
one uniformly in n and regularity assumptions adapted from the diffusion-limit
literature (PDF pp. 10-11), the generator of the rescaled process is Taylor
expanded into the generator of a normally reflected diffusion on the positive
orthant with Neumann boundary, whose drift carries a discrete Laplacian
coupling x(k+1) + x(k-1) - 2x(k) scaled by the limiting Hawkes migration
intensity (PDF pp. 12-14, Theorems 4.1 and 5.1). The multivariate Hawkes FCLT
gives the asymptotic event-count covariance (I - K)^{-1} diag(Lambda-bar)
(I - K)^{-T}, and an incidence matrix maps event counts to queue volumes so
the mesoscopic diffusion covariance is C times that quantity times C
transposed (PDF pp. 14-15). Future work names calibration to data, numerical
schemes, continuum (SPDE) limits and nonlinear extensions (PDF pp. 16-17).
The work is entirely theoretical, "without relying on empirical calibration"
(PDF p. 1), and contains no data, no estimation, and no predictive claim.

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. The entire limiting construction is conditional on the stability
   condition, spectral radius of the integrated kernel matrix strictly below
   one, uniformly in n (PDF pp. 10-11, 14-15), and the diffusion covariance
   carries the inverse (I - K)^{-1}, which diverges as the spectral radius
   approaches one. [reinforcing, no new item]: this corroborates the standing
   near-critical regime-disclosure rule (the branching-ratio n less than one
   family): any future reading that leans on effective-excitation or
   endogeneity-type quantities is reading a quantity whose variance structure
   explodes precisely in the regime the programme most cares about, and the
   disclosure that the window's estimated excitation sits far from or near
   criticality belongs in the pre-registered record, not after the fact. The
   paper is a theoretical worked example of the mechanism, not evidence in
   this programme's record and licenses nothing measurable here.

2. The queue indexes are pinned by a fixed mid and a constant two-tick
   spread, adopted explicitly because a moving best bid/ask would change the
   state-space dimension over time and break the tightness and regularity
   conditions the scaling limit needs (PDF pp. 7-8). [reinforcing, no new
   item]: this corroborates the already-queued queue-label convention
   declaration component (deep-read session 32): a real book on the
   programme's venue has no fixed spread, so every conditioning or feature
   state that labels queues by distance from a reference price must declare
   its anchoring and tie-break convention or the same declared functional
   reads different states from the same raw stream. The theoretical paper
   buys its fixed coordinates by assumption; the programme cannot, and
   that is exactly what the queued declaration component forecloses.
   Nothing new is queued; the existing item is unchanged.

3. The migration mechanism is symmetric by construction: the per-unit
   intensity for jumping one tick toward the mid equals the per-unit
   intensity for jumping one tick away (PDF p. 9), all order and
   cancellation sizes are one (PDF p. 8), and the matching rule is FIFO,
   explicitly not pro-rata (PDF p. 3). [interpretation caution]: the
   Laplacian coupling in the mesoscopic limit is a smoothed, symmetric,
   unit-size, fixed-spread artifact of these assumptions, so the model's
   spatial-coupling implication must never be read as expected book
   behaviour of any venue the programme measures — in particular not as an
   anticipated BTCUSDT depth profile, and not as a benchmark a future C1-L2
   feature is graded against. Real asymmetric liquidity repositioning,
   size-clustered orders and pro-rata venues are simply outside the model.

4. The paper makes no return-predictive or market-truth claim of any kind:
   it is zero-intelligence by design, self-described as entirely
   theoretical without empirical calibration (PDF pp. 1, 3, 16-17).
   [reinforcing, no new item]: the programme's generative-null family
   caution (fidelity is not predictivity, seated in the session-33 entry)
   applies a fortiori; nothing here is even generative-fidelity evidence,
   it is a theorem about an assumed microscopic world. Nothing new queued.

5. Theorem statements and the generator/Taylor-expansion machinery are
   presented as standard, with the proofs described as following Ethier and
   Kurtz and the drifted-from references (PDF pp. 12-14), but this
   programme verifies nothing during null time, so the correctness of the
   proofs is unverified by us, and the Lambert-style reference list shows
   item [1] cited as "arXiv:2018" without a number (PDF pp. 17-18).
   [source-quality note]: a single-author preprint, arXiv v1 stamped
   22 November 2025, no journal or peer-review record checked at reading,
   math not independently verified by the programme; graded as a
   theoretical construction whose conclusions are conditional on its
   assumptions, to be re-checked against a published version before any
   formal citation.

## What this paper would have killed if we had done it wrong

Read without the one-question discipline, the seductive failure is
benchmark-by-theorem: adopting "queue volumes smooth toward a Laplacian
profile under Hawkes-modulated migration" as a structural fact about books
and then grading a future C1-L2 conditioning state, feature or diagnostic
against that expectation. That would have laundered a two-tick fixed-spread,
unit-size, symmetric-migration FIFO artifact into a market benchmark for a
floating-spread crypto venue where every one of those assumptions fails,
and a feature that deviated from it would have been quietly killed — or one
that matched it quietly blessed — on grounds that exist only inside the
model. The programme's neutralisation is the standing rule that no
theoretical or empirical structure from any paper enters as expected
behaviour of a measured market, plus the queued queue-label convention and
near-critical disclosure components, which force the two real-world degrees
of freedom this paper assumes away. A second trap is the stability
condition itself: had the near-critical covariance explosion been treated
as an incidental technicality rather than the signature of a regime in
which excitation-based readings become unstable, the programme would have
left undisclosed exactly the regime variable on which any future Hawkes-
flavoured reading depends.

## Standing caveat

Entirely theoretical; no data, estimation, calibration or simulation appears
anywhere in the paper (PDF pp. 1, 16-17). Scope boundaries: fixed two-tick
spread and a fixed mid, justified for large-tick assets and needed only for
the coordinate stability the proof wants (PDF pp. 7-8); unit order and
cancellation sizes (PDF p. 8); symmetric inward/outward per-unit migration
intensity (PDF p. 9); FIFO matching, pro-rata excluded (PDF p. 3);
bid-side derivation with the ask side "defined analogously" (PDF p. 9);
diffusive scaling with time acceleration n and queues of order sqrt(n)
(PDF pp. 10-11); stability spectral radius below one uniformly (PDF
pp. 10, 14-15). The proofs lean on Ethier-Kurtz and Lions-Sznitman
frameworks and are not verified by this programme (nothing measured during
null time). arXiv v1 stamped 22 November 2025; no journal or peer-review
record checked at reading — check the published version before formal
citation. Laundering directions named: INTO — only the stability-condition
mechanism (as corroboration of the near-critical disclosure rule), the
fixed-coordinate exposé (as corroboration of the queue-label convention
component), and the symmetric-migration caution enter as reading and
design discipline. OUT — the Laplacian coupling, the reflected-SDE limit,
the covariance formula and every fitted-style implication are never cited
as expected behaviour of any market the programme measures, never as
expected BTCUSDT book behaviour, and never as evidence that any programme
feature carries information.
