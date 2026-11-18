# Library deep-read session 24 — Ouazzani Chahdi, Rosenbaum &
# Szymanski, "Passive Market Impact: A Point Process Approach"
# (arXiv:2412.07461v2, 2024/2026; CentraleSupélec/École
# Polytechnique/Luxembourg; book-state-dependent information content
# in a Hawkes propagator price, and the impact of passive metaorders)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x43a538_passive_market_impact_a_point_process_approach.txt`,
~39 pp., page-marked). Next UNREAD triage-rank entry (score 33;
verified unread by the read-slug mapping; flagged by the session-29
pointer as squarely in C5's passive-withdrawal family after
session 21's spoofability read — it is the theoretical companion
to that empirical read).

## The paper in one paragraph

In the Jaisson-style Hawkes propagator price — mid-price as the
anticipated future market-order flow, each trade carrying a
CONSTANT information content κ — passive orders produce impact of
the WRONG SIGN: a resting buy metaorder sits on the bid, so its
executions mechanically push the price DOWN on average, against
the empirically established fact that limit-order impact is
comparable to market-order impact with the correct sign (PDF
pp. 1-3). The authors' fix: replace constant κ by a DECREASING
function κ(q) of the volume available at the touched queue — a
price-resistance coefficient, harder to move through a bigger
pile — with queue dynamics in the Queue-Reactive spirit (Huang et
al.): arrivals and cancellations are state-dependent Poissons,
market orders are independent Hawkes processes (PDF pp. 4-6).
They prove the price well-defined, derive scaling limits in the
near-critical Hawkes regime (Mittag-Leffler volatility, the
Jusselin-Rosenbaum machinery), and obtain for a passive metaorder
of intensity f an impact that is MONOTONE during execution and
has NO relaxation phase, converging immediately back through
queue stationarity; at large participation rates the impact grows
like sqrt(gamma) (their V-profile liquidity argument; simulated
exponent 0.54, PDF pp. 10-19, Figures 1-2, eqs. 4-5). Section 4
gives a calibration: κ is estimable by regressing realized
variance on trade counts, with statistical evidence that higher
volatility corresponds to smaller κ (PDF pp. 19-21).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] The wrong-sign artifact is
   model-made — the sign-register rule's cleanest theoretical
   demonstration.** Session 10's queued sign-register rule exists
   because a flow-based price construction can manufacture the
   wrong sign for a whole order class without any data being
   wrong: here it is demonstrated in print — the constant-κ
   propagator assigns resting liquidity-provision flow a
   mechanically perverse sign, and the fault is a MODELING choice
   (state-independence of the trade's information content), not a
   market property (PDF pp. 2-3). This adds the theoretical face
   to the queued rule's empirical motivation (passive executions
   clear against, not with, the motion); the rule's legal content
   is untouched, and the citation lands as reinforcement: any
   future feature built from flow-based constructions states its
   sign register per order class before its values are read.

2. **[reinforcing, no new item] Passive orders move prices — C5's
   passive-withdrawal family gains its theoretical warrant for
   causal-language territory.** The model's core mechanism — an
   additional resting order raises the resistance κ(q), tilting
   the conditional distribution of the next price move toward the
   order's own side, fast enough that a passive metaorder's
   average impact is monotone and ~sqrt(participation) — is the
   equilibrium-side picture of what session 21 measured
   (distance-and-size-aware passive placement shifts the
   predicted next-second distribution) and what the imbalance-
   prediction literature has long shown (PDF pp. 3-4, 14).
   Nothing in C5 changes; the family's insistence that passive
   depth is causal-language territory — never a neutral
   regressor, never "just liquidity" — now rests on both an
   empirical read (session 21) and a solved theoretical model.

3. **[cost-survival ammunition] Passive execution cost schedules
   are qualitatively different from aggressive ones: no relaxation
   phase.** The aggressive metaorder impact is canonically concave
   rise then convex RELAXATION; in this model passive impact is
   monotone with NO post-execution decay — the book re-stations
   and the impact stands (PDF pp. 18-19). Declared as ammunition
   only: any future K7-style cost-survival layer that assumes the
   aggressive impact shape for passive fills would misprice the
   post-execution leg in a known direction, and the paper's
   instantaneous-impact approximation (eq. 4: ~sqrt(c_kappa *
   (mu(1-||phi||))/c_lambda)) is a template the layer would have
   to carry, with its flow model declared per the session-20
   Poisson-mispricing rule. The program never trades live;
   nothing here is operationalized.

4. **[interpretation caution] A fitted κ is a book-state moment,
   not a constant — and it moves with volatility.** The
   calibration section's own punchline: higher volatility
   corresponds to smaller resistance (PDF pp. 19-21). For
   interpretation language: any future price-resistance- or
   depth-elasticity-type estimate on gated windows is a
   state-dependent, regime-moving object — never a free-standing
   venue constant, joining the per-branch rule (session 9), the
   dispersion register (session 14), and the MIHM identity
   (session 20) in the never-read-alone family; the estimation
   itself is a linear regression on a simplified submodel, an
   approximation grain the reading discipline already demands be
   declared.

## What this paper would have killed if we had done it wrong

If the trigger layer had ever been specified with flow-based
features whose sign register was inherited from an aggressive-
order construction — the exact wrong-sign trap this paper isolates
— passive flows would have entered with mechanically perverse
signs and no diagnostic would have flagged it: the model fits, the
backtests run, the signs are simply wrong for a whole order class.
And if any causal claim about passive depth on gated BTCUSDT
windows had been phrased as a description of "liquidity" rather
than routed through C5's passive-withdrawal family, this paper is
the theoretical statement that passive placement moves the
conditional price process itself — the family's whole reason for
existing. The program's sign-register rule and C5 routing predate
the read; both are reinforced, neither changed.

## Standing caveat

A stylized one-queue-per-side model at unit order size, with
market-order arrivals INDEPENDENT of the book state (the authors'
own admission this is "of course an unrealistic assumption," PDF
p. 3 — the very independence the model then partially repairs
through κ); negative queues allowed with small calibrated
probability; metaorder impact derived near the stationary, near-
critical regime; calibration on a linearized submodel with κ²
affine by assumption, non-parametric estimation explicitly out of
scope; the sqrt(γ) large-participation asymptotics rest on the
V-shaped liquidity-profile argument imported from theory, with a
0.54 simulated exponent as illustration, not evidence. arXiv v2
(2026-07 stamp), no published version located at read time — check
before formal citation. No execution strategy is operationalized;
the program never trades live.
