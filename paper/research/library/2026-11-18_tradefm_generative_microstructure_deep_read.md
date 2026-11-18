# Library deep-read session 33 — Kawawa-Beaudan, Sood, Papasotiriou,
# Borrajo & Veloso, "TradeFM: A Generative Foundation Model for
# Trade-flow and Market Microstructure" (arXiv:2602.23784v1, 2026;
# J.P. Morgan AI Research; a 524M-parameter generative Transformer
# over 10B+ US-equities trade tokens)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xe7dc7f_tradefm_a_generative_foundation_model_for_trade_fl.txt`,
~29 pp., page-marked). Next UNREAD triage-rank entry (score 31;
verified unread by the read-slug mapping); the industry-pressure-
point face of the ML side the program entered at session 29.

## The paper in one paragraph

TradeFM is a decoder-only Transformer pre-trained on billions of
raw tick-level trade events across >9K US equities (Feb 2024 -
Sep 2025; 19B tokens; temporal hold-out Jan 2025 onward; APAC OOD
hold-out), learning P(event | preceding stream) directly and
generating rollouts through a deterministic market simulator
(PDF pp. 1-5). The cross-asset trick is a SCALE-INVARIANT
construction: EW-VWAP as a time-aware mid-price ESTIMATOR under
partial observability, log-volume, price depth normalized by the
mid in bps rather than ticks, and movement quoted relative to the
day's open — explicitly to enforce homogeneity across assets with
different tick geometries and liquidity profiles (PDF pp. 4-5).
Closed-loop rollouts reproduce the canonical stylized facts (heavy
tails, volatility clustering, ABSENCE of return autocorrelation);
distributional error is 2-3x lower than Compound Hawkes baselines;
zero-shot transfer to Japanese and Chinese APAC markets shows
only moderate perplexity degradation; and the stated endpoints
are synthetic data generation, stress testing, and training
learning-based trading agents (PDF pp. 1-2).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] Industry has independently
   arrived at the construction-triple discipline and made it the
   core of the model.** The paper's scale-invariant features are
   J.P. Morgan's own version of the program's (feed x grain x
   construction) rules: mid-relative price depth instead of tick
   units is precisely the sessions-21/25 lesson (distance units
   decide across tick geometries); EW-VWAP is a DECLARED
   estimator for an unobserved mid under partial observability
   (the estimator-mode family's industrial face); log-volume
   declares the heavy-tail construction. The reinforcement is
   institutional: a 524M-parameter budget was spent BECAUSE
   normalizing constructions across venues/grains was understood
   to be load-bearing. Nothing queued; the program's rules already
   force the declarations.

2. **[reinforcing, no new item] The baseline choice concedes the
   kernel-geometry lesson: Compound Hawkes was the comparison
   class and lost 2-3x on distributional error.** Session 28's
   finding (the exponential-kernel Hawkes cannot express
   non-monotone dependence structure under ANY parameters) is the
   theory behind TradeFM's empirics: a model with geometric
   constraints on its dependence structure loses to an
   unconstrained learner on distributional fidelity. This is NOT
   an endorsement of foundation models as market knowledge — it
   is the estimator-mode family's demonstration at industrial
   scale: model geometry decides what can be captured before any
   data arrives.

3. **[interpretation caution] Stylized-fact reproduction is a
   NECESSARY-but-weak bar, and the paper's own headline fact makes
   the point: absence of return autocorrelation.** Rollouts that
   pass heavy tails, volatility clustering, and NO return
   autocorrelation are by construction rollouts with no
   directional predictability claim attached — the paper never
   claims one. For the program: if any synthetic-market
   environment is ever specified (a future K7-style cost-survival
   layer's test bench, hypothetically), the house bar is
   stylized-fact checks PLUS the label-placebo battery PLUS the
   branching/multi-reading requirements (sessions 16/17/28) —
   distributional error alone, like any model-internal score
   (the session-29 lesson), cannot certify "realism."

4. **[cost-survival ammunition] The declared endpoints are
   synthetic data, stress testing, and RL training environments -
   and "learning-based trading agents" is the pressure point.** If
   a K7-style layer is ever ratified, this is the industrial
   template it would face: agents trained on generative
   microstructure must declare the simulator's construction
   ( tokenizer, scale-invariance choices, simulator rules ) per
   the venue-freeze and disclosure rules — a synthetic-venue
   statement is a construction statement, nothing more. The
   program never trades live; none of this is operationalized.

5. **[source-quality note] Proprietary data, industrial
   incentives, preprint status.** The data is private (J.P.
   Morgan tick archives); the 2-3x claim is against Compound
   Hawkes baselines ONLY — a class session 28 showed to be
   geometry-constrained, so the comparison direction flatters the
   winner; perplexity and distributional error are model-internal
   scores whose evaluation split hygiene looks serious (temporal
   hold-out, tokenizer calibrated on the first 30 days only, OOD
   APAC) but whose publication incentives (cs.LG venue, agents
   endpoint) are structural. arXiv v1, February 2026, cs.LG;
   check for peer review before formal citation. Zero market facts
   licensed; the citable content is the methodology.

## What this paper would have killed if we had done it wrong

If the program had ever evaluated a simulator (or any synthetic
market environment) on stylized facts alone, this paper is the
industrial demonstration of what that bar misses: a 524M model
can reproduce every listed stylized fact while its own headline
includes the ABSENCE of return autocorrelation — realism scores
say nothing about what a strategy trained inside would learn, and
the agent endpoint is exactly where a synthetic artifact could be
launded into a "working" agent. And if any spec had treated an
industry normalizer (tick-based depth, say) as a neutral default,
the scale-invariant construction here is the institutional
counter-argument that the units themselves decide the model. The
program's label-placebo battery, construction declarations, and
simulator cautions predate the read; all are reinforced.

## Standing caveat

Proprietary US-equities tick archive, one 19-month vintage,
partial observability by design (no LOB input — a strength for
deployment, a limitation for validating against book-geometry
mechanisms the model never sees); the deterministic simulator's
rules are the authors' own construction and closed-loop realism
inherits it; zero coverage of the program's venue or grain and
no claim made about either; "agents" is prospective. arXiv v1
unpublished at read time. Nothing here is operationalized;
nothing trades live.
