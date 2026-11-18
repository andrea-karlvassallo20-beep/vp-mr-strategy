# Library deep-read session 32 — Mahseredjian, "Diffusive Limit of
# Hawkes Driven Order Book Dynamics With Liquidity Migration"
# (arXiv:2511.18117v1, October 2025; single-author theoretical
# preprint; Hawkes order flow + level-to-level liquidity migration
# under a diffusive limit)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x5db64b_diffusive_limit_of_hawkes_driven_order_book_dynami.txt`,
~16 pp., page-marked; text layer contains null bytes — read with a
null-strip, harmless to content). Next UNREAD triage-rank entry
(score 31; verified unread by the read-slug mapping).

## The paper in one paragraph

A wholly theoretical mesoscopic LOB model: order arrivals,
cancellations, and — the novelty — MIGRATION events between
neighbouring price levels, each with Hawkes-modulated intensities
(temporal self-excitation, cross-excitation, decay; PDF pp. 5-6).
Under diffusive rescaling with a Taylor expansion of the
microscopic generator, the queue volumes converge to a reflected
multi-dimensional SDE whose spatial coupling is a DISCRETE
LAPLACIAN: liquidity migration induces diffusion-like spreading
across adjacent levels, and the limiting diffusion covariance
matrix is connected to the Hawkes branching structure through a
functional central limit theorem for event counts (PDF pp. 5, 10-
15). The author states plainly that the work "is entirely
theoretical and lays a foundation... without relying on empirical
calibration" (PDF p. 1).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] The book is SPATIALLY COUPLED:
   queue levels are not independent queues.** The paper's central
   mechanism — migration intensities that move liquidity between
   adjacent levels, surviving into the limit as a Laplacian term
   — is the formal statement of what sessions 13/14/24's
   queue-machinery line implies: a depth reading at one level is
   entangled with its neighbours' migration state, and a feature
   that treats each level as isolated inherits crosslevel
   contamination by construction. The existing depth construction
   declarations cover it; nothing queued.

2. **[reinforcing, no new item] Cross-level queue covariance is
   BRANCH-DRIVEN — the never-read-alone family's spatial face.**
   The FCLT link (diffusion covariance tied to the Hawkes
   branching structure, PDF pp. 14-15) formalizes that
   cross-level depth correlations are endogeneity readings:
   covariances observed across book levels are functions of the
   excitation tree, not free-standing market facts. Joins the
   per-branch rule (session 9), dispersion register (session 12),
   MIHM (session 20), and near-critical limits (session 31);
   nothing new — the multi-reading requirements enforce the
   format already.

3. **[source-quality note] Development-stage single-author draft:
   cite for structure only.** Entirely theoretical, explicitly
   without calibration or numerics; first-person voice ("my
   model"); one supporting citation is a doctoral thesis (Chen)
   described loosely; the claims about existing models omitting
   spatial propagation are asserted, not tested against the
   queue-reactive lineage (Huang et al.'s state-dependence and
   session 13's ergodicity framework are adjacent without being
   engaged). Useful content: the migration mechanism and the
   Laplacian limit as a POSSIBLE structure; ZERO market facts
   licensed. arXiv v1, November 2025, no published version,
   no peer review — check before formal citation.

## What this paper would have killed if we had done it wrong

If the L2 feature layer had ever computed per-level depth features
as if levels were independent (the natural vector treatment), the
migration mechanism is the formal statement that neighbouring
levels share liquidity dynamics through an explicit coupling —
per-level features carry their neighbours' migration by
construction, and backtests on per-level signals would carry the
coupling whether or not anyone declared it. And if cross-level
depth correlations had ever been read as free-standing liquidity
facts, the covariance-to-branching link is the statement that they
are endogeneity readings in the never-read-alone family. The
program's construction declarations and multi-reading rules
predate the read; the paper reinforces both without a change.

## Standing caveat

A preprint at foundation stage: no calibration, no simulation
studies visible in the extract, stationarity/stability conditions
carried by assumption, and the diffusive limit is a formal
asymptotic — no evidence any market sits in its scaling regime;
migration is a theoretically attractive candidate mechanism, not a
measured phenomenon. Nothing here touches the daily prestate grain
of the dossiers (sessions 34/37/40). Nothing to operationalize;
nothing trades live.
