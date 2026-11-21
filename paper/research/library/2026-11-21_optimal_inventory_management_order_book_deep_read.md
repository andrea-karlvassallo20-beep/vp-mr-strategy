# Deep-read session 79 — Optimal inventory management and order book modeling

**Deep-read session 79** (null-time session 90, second act; first read of
the score-23 tier). Nicolas Baradel, Bruno Bouchard, David Evangelista,
Othmane Mounjid (Université Paris-Dauphine/CNRS, KAUST, École
Polytechnique), "Optimal inventory management and order book modeling"
(arXiv:1802.08135v2 [q-fin.TR], stamp 9 Nov 2018, 40 pp. in the extract).
A structural control-theoretic order-book model: three rational agent
classes (market makers, a stock-futures pair-trading HFT, VWAP- and
volume-schedule institutional brokers) act on a Queue-Reactive-style
best-bid/ask book whose exogenous flow intensities depend on the book's
imbalance, and their optimal strategies are characterized as viscosity
solutions of variational PDEs and then played against each other inside
a closed simulation.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xaf167e_optimal_inventory_management_and_order_book_modeli.txt,
~40 pp., page-marked). Next UNREAD triage-rank entry (score 23).

## The paper in one paragraph

The book is restricted to the best bid and ask queues, spread in {1, 2}
ticks, prices moving only when a queue is depleted by aggressive orders
or by a limit order inserted inside a two-tick spread, queues regenerating
by exogenous law (model eqs. 2.1-2.6, PDF pp. 3-5); the exogenous flow's
compensator is a state-dependent kernel that can condition on the book's
imbalance, following the empirical statistics of Besson et al. [9]
(PDF pp. 2, 5). The market maker maximizes exponential utility of terminal
wealth with inventory bounds, a queue-position state (units ahead of him
in each queue), an action counter and a partial-liquidation penalty;
his value function solves a variational inequality (3.3-3.4, PDF
pp. 8-10) with a convergent explicit time-discretization and an
asymptotically optimal control extracted from it (PDF pp. 12-13). The
HFT is the same problem wrapped around a mean-reverting stock-futures
spread process S, gaining only S's evolution, with the book's mid-price
risk immunized by the symmetric futures position (PDF pp. 18-22). The
brokers are not optimized: a volume-participation chaser and an
Almgren-Chriss-style closed-form optimal VWAP schedule implemented as
discrete book orders with catch-up aggressive flow when behind schedule
(PDF pp. 24-29). The numerical priors are inspired by one large-cap
equity name (Société Générale): aggressive-order direction arrives at
the ask with probability 0.5 + 0.35 x Imb, size a 0.7 + 0.3 x Imb
fraction of the queue, price-move probability 75% on depletion,
two-tick spreads closing with 90% probability (PDF pp. 13-14). The
full-market illustration plays one MM, one HFT and four brokers against
each other under a fixed execution priority (HFT first, then MM, then
brokers, PDF pp. 31-32); the authors call it a first illustration, "a
more thorough study is left for future research" (PDF pp. 3, 32).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [interpretation caution] Imbalance is endogenous strategic output,
   not exogenous state, inside exactly the model class that assumes
   imbalance-sensitivity. The optimal market maker plants limit orders
   that are NOT meant to execute, in order to skew the book's
   imbalance and so shift the exogenous flow's arrival direction and
   size against him ("some limit orders are sent not to be executed
   but to influence the evolution of the price in a favorable
   direction ... he can be sometimes at the limit of a price
   manipulation strategy", PDF p. 15; the imbalance-dependent
   direction/size priors, PDF pp. 13-14). Reading discipline for the
   C1-L2 feature spec: an imbalance-based feature on live tape
   measures a field that strategic agents on the tape may be
   deliberately shaping, because they believe (as the paper's priors
   do) that others condition on it; no imbalance feature may be
   interpreted as a clean exogenous state variable, and heterogeneity
   of imbalance effects across regimes is the default expectation.
   No queue change — the estimator-configuration freeze and the
   frozen-feature reading rules already carry interpretation
   discipline; the session found no mechanism here that makes a
   future test harder to pass beyond the standing constraints, so the
   default grade stands.
2. [reinforcing, no new item] Every positive result in the paper is a
   product of its own priors, closed under the model: the priors are
   inspired by one equity name and borrowed charts (PDF pp. 13-14),
   β and κ are moment-matched inside the model by iterative
   simulation (PDF p. 29 footnote 13), and the VWAP strategy
   "typically performs better than the market" (PDF pp. 29-30) only
   against the book that its own assumptions generate onto the
   simulated broker's own schedule. Simulation output given the
   model's own inputs is not evidence of anything in the world; the
   laundering ban binds and no claim here can enter the record as
   support for any programme claim.
3. [interpretation caution] Touch-only truncation: the model keeps
   only the best bid and ask queues and two spread values, explicitly
   "for numerical tractability" (PDF pp. 2-3), and price impact lives
   entirely at the touch (queue depletion or spread insertion, PDF
   pp. 3-5). Re-exhibits on the control-theory side the
   top-of-book-singularity caution of the ## 102 read: touch-only
   state cannot be presumed to represent the depth state; level count
   must be named in any C1-L2 feature built on queued depth. No
   queue change — the level-count reading discipline is already
   standing; the paper's own truncation is the exhibit, not a new
   rule.
4. [cost-survival ammunition] The broker mechanics declare the
   assumptions a future K7-style cost-survival layer must carry:
   participation-rate volume chasing turns aggressive exactly when
   realized volume falls behind the target band
   (aggressive catch-up above the lower band, standing limit
   inventory above the band pushing the price, PDF pp. 24-25,
   28-29, 31-32 — the simulation shows the broker's own standing
   imbalance "contribut[ing] to push up the price", PDF p. 25).
   Aggressive flow from schedule-driven executors is state-dependent
   on the executor's progress against its calendar, not on
   information; a cost layer that reads aggressive flow as uniformly
   informed overstates adversarial inference. Declaration
   requirements only; nothing armed.
5. [interpretation caution] Round-based multi-agent simulation
   conclusions are artifacts of the chosen intra-round execution
   priority (HFT executed first, then MM, then brokers in random
   order, a convention, PDF pp. 31-32; the authors themselves note
   the HFT's first-move advantage, "since he is executed first ...
   he does not give to the others the opportunity to take this
   position", PDF p. 32). Reading discipline: any future programme
   use of simulator-generated microstructure studies (C8 placebos,
   layer-0 sanity tapes) must pre-declare the intra-round priority
   rule and report conclusions' stability to it; in this discipline
   it joins the simulation-power caveats already standing under the
   no-measurement and laundering-ban rules. No queue change.
6. [source-quality note] arXiv v2 stamped 9 Nov 2018; equities,
   single venue, priors from one large-cap name; queue-regeneration
   laws exogenous and untested; the full-market interaction is "a
   first illustration" with the thorough study left for future
   research (PDF pp. 3, 32); nothing touches crypto perp L2 tape, no
   regime transfer is established, and sticky-flat perp spreads
   violate the paper's two-tick closure prior outright; a published
   version in this lineage must be checked before any formal
   citation. Regardless, no claim here can serve as support for any
   programme claim.

## What this paper would have killed if we had done it wrong

Had the programme taken the paper's headline interaction at face
value — "institutional VWAP schedules beat the market VWAP" and "an
optimal market maker profits by planting imbalance" — it would have
imported into C1-L2's motivation a pair of claims that are true only
inside a model in equilibrium with its own priors: one simulated
stock's book, imbalance-conditioned flow assumed (not measured), and
the optimizing agents' advantages partly manufactured by the arbitrary
intra-round execution priority. A C1-L2 spec motivated that way would
pre-load an imbalance-shaped narrative onto the Tardis tape before a
single feature was measured, and any null result would then be blamed
on "the imbalance signal being gamed by HFTs", exactly the laundering
route the banned-narrative discipline of the ## 101 read prohibits.
The existing discipline — the estimator-configuration freeze, the
frozen feature definitions, the default assumption of no edge, and
the ban on any library claim entering the record as support — is the
artefact that absorbed this paper harmlessly.

## Standing caveat

The paper is a control-theory construction with an illustrative
simulation, not an empirical study; its quantitative content (the
0.5 + 0.35 x Imb direction and 0.7 + 0.3 x Imb size priors, the 75%
price-move probability, the queue-size laws) is borrowed
single-name equity statistics from a broker research source
(Besson et al.) and its parameter estimates are moment-matched
inside the model (PDF pp. 13-14, 29 n. 13). Best-queue-only, two
spread values, no cancellations from the rest of the market in the
MM experiment (PDF p. 14), the futures leg modeled only as a
mean-reverting add-on to the stock mid-price (PDF p. 2), and the
agents' priors treated as the market's true law. Nothing here is
measured on any tape the programme will ever hold; arXiv-version
caution applies before formal citation.
