# Deep-read session 37 — Morariu-Patrichi & Pakkanen, "State-dependent Hawkes processes and their application to limit order book modelling"

**Authors:** Maxime Morariu-Patrichi, Mikko S. Pakkanen (Imperial College
London / CREATES). **Venue:** arXiv:1809.08060v3 [q-fin.ST], Sept 2021.
One clause: a Hawkes counting process and a book-state process fully
coupled (excitation kernels depend on the state; events switch the
state), estimated on Nasdaq level-I INTC data — the L2 arena's
state-conditional excitation paper.

**Read-line:** Read 2026-11-18, against ONE question: **what here
would kill C1-L2 or C8 faster, or change their kill lines?** Source:
legally acquired OA copy
(`docs/library/text/x947263_state_dependent_hawkes_processes_and_their_applica.txt`,
~33 pp., page-marked). Next UNREAD triage-rank entry (score 32).

## The paper in one paragraph

State-dependent Hawkes processes couple a multivariate self/cross-exciting
counting process (order events: Limit/Market/Cancellation on bid and
ask sides) with a finite-state process (the book's state — bids–ask
spread in ticks for ModelS, queue-imbalance buckets for ModelQI):
kernels k'e(x-dep), and events switch the state, so excitation and
state co-evolve (PDF pp. 3-6, 140-168). Existence/uniqueness via a
unique-marked-point-process bijection, ML estimation with ordinary
Hawkes likelihood machinery once the state path is recovered from the
data (pp. 91-95), parametric bootstrap CIs tight (p. 29). Empirics on
~2.5-hour Nasdaq windows, INTC, June 2017-May 2018 (pp. 99-110, 610-770):
excitation patterns are STRONGLY state-dependent, and endogeneity
(kernel spectral norm) is systematically more pronounced in
DISEQUILIBRIUM states of the book — in ModelS the wide-spread state's
spectral radius sits systematically ABOVE 1 (apparent super-criticality
in disequilibrium), and in ModelQI extreme-imbalance states exceed 0.9
most days (pp. 19-20).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.**

1. `[reinforcing, no new item]` **Estimator-mode, extended into the L2
   arena: excitation/branching quantities are BOOK-STATE-CONDITIONAL.
   Pooled excitation estimates mix equilibrium and disequilibrium
   regimes (pp. 19-20) — the session-48 regime-mixing bias demonstrated
   at LOB grain with a concrete state axis (spread ticks / queue
   imbalance). Any future L2/T2 measurement of excitation, branching,
   or endogeneity that pools across book states is the exact
   vulnerability this paper measures; the estimator-mode rule already
   forbids it — this read supplies the axis to declare (spread state,
   imbalance bucket) when L2 begins.
2. `[interpretation caution]` **Apparent criticality has a state
   axis.** The wide-spread state's spectral radius > 1 while pooled
   analyses report "near-critical" markets (p. 19-20): pooled
   near-criticality may be a MIXTURE concentrated in disequilibrium
   states rather than a market-wide fact — the apparent-criticality
   lesson (session 48) gains a concrete micro-structure: the
   criticality reading itself is conditional on book state, and any
   fragility claim from L2 must say WHICH state it lives in.
3. `[interpretation caution]` **State-dependence of endogeneity
   rhymes with the flow-zone geometry at the daily grain:** the
   program's measured zone edges (XB entries/exits, extremity bands)
   are informative while the positive-side interior oscillates
   (session 63: 72% of transitions A<->XA); this paper's disequilibrium
   states are the LOB-scale analog — the excitation lives at the state
   edges. Cross-grain rhyme, not evidence: no port from LOB to daily
   constructions is licensed.
4. `[reinforcing, no new item]` Would-have-killed corollary for
   C8's queue imbalance ambitions: imbalance is a STATE (bucketed,
   transition-matrixed, pp. 746) rather than a free continuous
   feature — any C8 imbalance factor must be declared as a state with
   its transition behavior, not a raw regressor; raw-imbalance
   regression would inherit regime-mixing silently.
5. `[source-quality note]` Single stock (INTC), single venue (Nasdaq),
   2.5-hour windows, 2017-2018 vintage; bootstrap CIs tight on
   excitation PROFILES but the near/above-critical spectral radii are
   vintage-and-venue conditional (the origin paper's caution
   verbatim); arXiv v3 2021 — check journal version before formal
   citation; zero portability to the program's perp venue at daily
   grain.

## What this paper would have killed if we had done it wrong

A future L2/T2 spec that fitted a Hawkes or branching measure to the
perp book's order flow POOLED across spread/imbalance states would
have reported "the market is near-critical" as a free-standing fact —
this paper shows such pooling mixes regimes whose excitation
systematically differs, with the disequilibrium states carrying the
near/above-critical readings alone. And a C8 imbalance factor built
as a raw continuous input would have smuggled the same regime mixing
into the macro layer. The house arsenal (estimator-mode,
construction-conditionality) already covers both routes; this read
supplies the concrete axes to declare when L2 work begins. No queue
change.

## Standing caveat

All estimation on one liquid equity stock; crypto perp books differ
(tick sizes, fee/rebate structure, maker-taker tides); "disequilibrium
states more endogenous" is a candidate regularity, not a law — it
would itself need the same state-conditional validation the program
demands of everything else. Nothing here touches the daily dossiers,
the W2 battery, or T1's spell scale.
