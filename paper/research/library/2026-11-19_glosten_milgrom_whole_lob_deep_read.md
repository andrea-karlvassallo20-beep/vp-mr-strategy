# From Glosten-Milgrom to the whole limit order book and applications to
# financial regulation — deep-read note

Paper: Weibing Huang (LPSM, Sorbonne Université), Sergio Pulido
(Université Paris-Saclay, CNRS, ENSIIE, LaMME), Mathieu Rosenbaum
(CMAP, École polytechnique, CNRS), Pamela Saliba (CMAP, École
polytechnique, and Autorité des Marchés Financiers), and Emmanouil
Sfendourakis (CMAP, École polytechnique), "From Glosten-Milgrom to the
whole limit order book and applications to financial regulation"
(arXiv:1902.10743v2 [q-fin.TR]; index year 2019; the extracted text is
stamped April 1, 2025 with arXiv v2 stamp 29 Mar 2025, a 2025 revision
of a 2019 preprint). Triage: score 29, slug
x0d8b2a_from_glosten_milgrom_to_the_whole_limit_order_book
(edge_triage_scores.json), the next UNREAD entry in triage order,
selected per the ## 59 closing pointer. Extract: 61 pp., page-marked,
complete, references and parameter appendices included
(docs/library/text/
x0d8b2a_from_glosten_milgrom_to_the_whole_limit_order_book.txt).

Read line: Library deep-read session 50, null-time session 57,
2026-11-19. Selected per the previous session's pointer (score 29,
x0d8b2a), re-verified unread against all 50 library notes on main and
the log at read time — the read-set was recomputed by slug and
normalized title, no note matches this paper; no branch claimed the
slug at read time (the first push-time race check found one open
PR, #227, a parallel corrigendum attempt, later closed unmerged;
the parallel session's landed remainder is log ## 60, mid-flight to
this staging, with the deep-read pointer unchanged — see the
renumbering disclosure below).
Read in full against the ONE question: what here
would kill C1-L2 or C8 faster, or change their kill lines?

Operational disclosure: a fresh main tarball was fetched and the
integrity guard run clean before this read; main was found at log
## 59 (the conductor-protocol corrigendum), and the session was
first numbered deep-read 50 = null-time 56 = log ## 60 against that
tail. Mid-flight renumbering: while the first staging (PR #229) was
polling CI, a parallel session landed log ## 60 on main (the
owner's four-point configuration on the repaired protocol: goal
state edition 2, rotation guidance, the weekly directorate, the
standing order recorded as MADE; the deep-read pointer unchanged,
no deep-read consumed); PR #229 was closed as superseded and this
note's session is renumbered deep-read 50 = null-time session 57 =
log ## 61 per the main-wins protocol. Work choice per
docs/goal_autonomy_protocol.md section 3: the DEFAULT ritual, with
the recorded reason stated in the log entry — a readable UNREAD
head exists (x0d8b2a, score 29) and zero deep-read sessions have
landed since goal-state edition 1 (2026-11-19, log ## 58) or since
edition 2 (2026-11-19, log ## 60), so the cadence rule does not
fire; no override; the edition-2 rotation guidance binds successor
selection.

## The paper in one paragraph

The authors generalize the Glosten-Milgrom adverse-selection
equilibrium from two quotes to the entire limit order book. An
efficient price follows a compound Poisson process (intensity lambda_i,
symmetric jump law f_B, PDF p. 5); an informed trader sees each jump
just before it happens and greedily consumes all liquidity up to the
post-jump efficient price (Assumption 1, PDF p. 7); a noise trader
sends compound-Poisson market orders independent of the efficient
price, and r = lambda_i/(lambda_i + lambda_u) is the fraction of
events that are information jumps (PDF p. 6); risk-neutral
competitive market makers see each jump only after it happens and post
limit orders wherever the expected gain against the efficient price
is non-negative, so that the rear of every queue is exactly
zero-profit (Assumptions 2 and 4, PDF pp. 9, 14). With zero tick the
half-spread mu solves E[max(B/mu, 1)] = (1+r)/2r and the spread is
2mu (Theorem 2.1, PDF p. 10); with tick alpha the average spread is
2mu + alpha, intrinsic spread plus tick, even when the intrinsic
spread exceeds a tick (Corollary 3.1, PDF p. 14). Parameters are
estimated on 103 NYSE/Euronext stocks (10am-3pm local, two six-month
windows, 2022-10 to 2023-03 and 2023-04 to 2023-09, constant-tick
days only) by maximum likelihood on one-minute increments of the
recovered reference price through its characteristic function
(Propositions 4.1-4.2, PDF pp. 15-17), with Levy-stable jump laws
(a around 1.8, PDF p. 17) and the noise size law either Gaussian,
matching the best pile only (PDF pp. 17-18, Fig. 2), or
piecewise-constant, reproducing the average ten-pile shape by
construction (PDF pp. 18-20, Table 3). Four applications: spread
forecasting across MiFID II tick-size changes, better than a
constant-spread prediction on 9 of 11 stocks, 14% versus 39% average
relative error (PDF pp. 22-23, Table 4); reproduction of the
volume-imbalance/next-move probabilities at a 5-second horizon for
large-tick stocks, with zero flow memory (PDF pp. 23-25, Fig. 4);
queue-position valuation, best-queue values of the order of the
spread (Theorem 5.1, Corollary 5.1, Table 5, PDF p. 26); and expected
waiting time until the next trade (Appendix A, PDF pp. 30-31).

## Findings, graded (does any kill line move?)

Verdict: NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] — a static, zero-memory equilibrium
   reproduces the imbalance/price-move relation. For large-tick
   stocks (average spread under 1.5 ticks, mu <= alpha/4), the best-pile
   imbalance I is a strictly increasing bijection of d, the position of
   the latent efficient price inside the tick (PDF p. 23), and the
   empirical 5-second upward-move probabilities conditional on
   imbalance are reproduced by the model with no flow memory whatever,
   the Gaussian noise version fitting best (PDF pp. 23-25, Fig. 4).
   The strongest known high-frequency "book predicts price" stylized
   fact is generated by a discreteness artifact of a static state, not
   by any dynamic signal. This reinforces the dynamics-identification
   rule queued at deep-read 49 (log ## 57, PENDING OWNER
   RATIFICATION) and its placebo precedents: a memoryless static
   equilibrium is a live competing explanation for any imbalance-family
   predictiveness, and shape-or-probability match alone can certify
   nothing about mechanism. Nothing from the paper's fits enters any
   spec.

2. [reinforcing, no new item] — average-shape match is non-identifying
   by construction. Proposition 2.2 (PDF p. 11) shows that essentially
   any increasing LOB shape is attainable through some strictly
   positive symmetric density f_Qu; the piecewise-constant calibration
   reproduces the average ten-pile shape exactly by building f_Qu from
   it (PDF pp. 18-20), while the low-dimensional Gaussian alternative
   fails beyond the best pile (PDF pp. 17-19, Fig. 2) and the fit fails
   outright on small-tick stocks, 23 and 21 of 103, all with spreads
   above 4 ticks (Table 3, PDF p. 20; Tables 6-7, PDF p. 55). A worked
   exhibit for the dynamics-identification rule: when the modeler
   free-fits a density to a static marginal, the static fit carries
   zero identification content. No queue change.

3. [interpretation caution] — equilibrium determinism means L2 book
   features are not independent measurements. The whole equilibrium
   book — spread, depth profile, pile volumes, imbalance, queue values —
   is a deterministic function of a handful of structural objects: r,
   the law of B, the law of Q_u, the tick alpha, and the latent state d
   (Theorem 2.1, PDF pp. 10-11; Theorem 3.1, PDF p. 14; Tables 1-2,
   PDF p. 16). In this model, depth, spread and imbalance are shadows of
   one common state; their co-movement is not evidence of a separate
   mechanism, and a future L2 feature set that treats book-shape
   families as independent signals can be counting one state several
   times. Interpretation discipline only: no spec changes, but any
   future reading of an L2 compression feature must be checked against
   the redundancy possibility before it is described as a distinct
   measurement.

4. [interpretation caution] — the model's own volatility formula is
   invalid under its own calibration. Macroscopic volatility is defined
   as lambda_i E[B^2] for square-integrable jumps (PDF p. 5), but the
   estimation family for f_B is Levy-stable with tail exponent a in
   (1, 2) (PDF pp. 17, 20), whose second moment is infinite; under the
   paper's estimated jump law the volatility expression does not apply.
   No volatility decomposition citing this model may be imported into
   C8's mechanical-versus-exogenous decomposition work; the boundary is
   model-relative in the same family as the ## 51 / ## 57 signed-bias
   conjunction caution, and nothing in the register moves.

5. [cost-survival ammunition] — queue position is a spread-sized
   priced quantity. Zero-profit holds only for a new order at the rear
   of a queue; orders placed earlier earn strictly positive expected
   gain, maximal at the queue top (Assumption 4, PDF p. 14; Theorem
   5.1, PDF p. 26), and the average value of the best-queue position is
   of the same order as the spread (Corollary 5.1, Table 5, PDF p. 26,
   in line with Moallemi-Yuan). Any future K7-style cost layer must
   carry queue position as an explicit pre-declared input; execution
   models that silently assume uniform or random fill positions within
   queues misprice passive fills by a spread-sized quantity, and the
   wrong assumption biases execution-probability estimates upward for
   deep-queue fills.

6. [source-quality note] — read from arXiv:1902.10743v2 as extracted;
   the published version was NOT checked at reading, flagged for
   verification. The extract is stamped April 1, 2025 (arXiv stamp
   29 Mar 2025); the index records year 2019 (first posting), and the
   lead authors overlap with the deep-read 49 lineage (Huang,
   Rosenbaum; ## 57). Venue scope: liquid NYSE/Euronext equities with
   competitive market making under MiFID II tick regimes, sessions
   trimmed to 10am-3pm, constant-tick days only (PDF p. 15). Two
   author-caught boundaries matter for citing: (i) the 5-second
   imbalance application required re-estimation of lambda_i at 5-second
   sampling because one-minute estimates "failed to capture many
   short-term efficient price jumps" (PDF p. 23) — estimated jump
   intensity is horizon-dependent, and cross-horizon transfer is not
   licensed; (ii) at extreme imbalance the empirical upward-move
   probability exceeds the model's theoretical bound e^(-lambda_i
   delta_t) (PDF p. 24) — the authors' own flag that the estimator
   still undercounts very short-term jumps. The spread-forecast skill
   (Table 4, PDF p. 23) is in-venue regulatory evidence, not a
   cross-venue law.

## What this paper would have killed if we had done it wrong

Had the imbalance application been read as "book shape predicts
price" support for any L2 premise, a discreteness artifact of a
memoryless static equilibrium, calibrated on large-tick equities with
a strong market-making sector, would have been laundered INTO the
record as a flow mechanism. The dynamics-identification rule queued
at ## 57 (if ratified) and the interpretation caution above prevent
exactly this.

Had the exact average-shape calibration been read as model
validation, Proposition 2.2's universality would have made the
validation unfalsifiable: the free density f_Qu carries as many
degrees of freedom as the shape it is fitted to, so the match is a
tautology, and a future generative null certified on shape alone
would again be a refutation instrument that cannot refute — the ##
45 synthetic-rebuttal precedent prevented it before it arose.

Had "spread = intrinsic spread + tick" been imported as a market
law, a zero-inventory-cost, zero-processing-cost, competitive-market-
maker equilibrium with informed trades only at jump times would have
become a cross-venue constraint on spread reads. The programme's
instrument is a crypto venue with no market-maker obligations, where
the model's institutional assumptions do not transfer; the finding
stays venue-relative.

Had the macroscopic volatility formula been cited alongside the
Levy-stable calibration, an infinite-variance jump law would have
anchored a finite-volatility decomposition in C8, corrupting any
mechanical-versus-exogenous boundary it touched.

Had lambda_i estimated at one sampling horizon been transferred to
another (one-minute to five-second, or five-second to any C1-L2
clock), the authors' own caught bias — systematic undercount of
short-term jumps at coarse sampling — would have entered calibration
silently. The ## 49 beta-lesson family (excitation estimates are
horizon- and spec-relative) is the standing register entry.

## Standing caveat

The model's applicability boundary is stated by its own assumptions:
no inventory or order-processing costs (the spread is purely
informational), liquidity supplied only by competitive market makers,
an informed trader who trades only at jump times and greedily (no
intraday accumulation), iid compound-Poisson noise trades with no
state dependence — the opposite corner from the queue-reactive model of
deep-read 49, whose intensities are all state-dependent — and instant
quote revision by market makers after every event. The authors
themselves list the mixing of informed and market-making roles in
practice as future work (PDF p. 27). The 5-second imbalance derivation
holds only for large-tick assets (mu <= alpha/4, PDF p. 23). The
empirical scope is equity venues with regulated tick regimes, 10am-3pm,
constant-tick stocks; nothing licenses transfer to crypto venues,
continuous books, or assets without a competitive market-making
sector. arXiv v2 read as-is; the published version was not checked at
reading.

A successor session must re-read the live main tail and the
branch/PR set, consult docs/goal_autonomy_protocol.md (edition 2;
the rotation guidance applies to selection), and record its work
choice and reason in its session-state note.
