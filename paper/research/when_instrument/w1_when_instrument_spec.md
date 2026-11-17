# W1 — The WHEN Instrument: straddle-logic sized by the posterior on MOVE, not UP

Status: PLAN + PRE-REGISTRATION, written during null time (no L2 trigger
data exists yet). Nothing here has been measured. This document follows
the pre-registration template (falsifiable core, data and label, estimand,
kill lines, what is deliberately NOT pre-registered, execution order)
and is the single governing document for W1. Per the one-spec-per-claim
rule, any future amendment is appended, dated, and marked.

Author context: drafted by the acting project owner as an independent
deliverable, at the owner's direction ("Build the WHEN instrument",
plan-first, minimal execution constraints). The standing repo rules are
inherited without exception: nothing here will ever trade live; the
asset is the method; every quantitative input is UNKNOWN until the
gated data measures it.

---

## 0. The project-owner analysis (why this, why now)

**Problem.** The programme's endpoint has been re-framed in writing: a
WHEN instrument — straddle-logic, sized by the posterior on MOVE, not
UP. The re-frame is forced by three sealed measurements: direction is a
coin flip (p(up) = 0.505 [0.497, 0.513], n = 15,386, refused per cell);
occurrence is near-certain inside primed states (P(sig move ≤ 60
trading days | primed) = 0.940 vs climatology 0.862, sealed C7); and
T1's second-window result survived all kill lines with its SIGN
INVERTED — the taker-side compression covariate is informative but the
mechanism's direction is wrong at the spell scale. The only honest
product is a timing instrument that refuses direction and sizes on the
posterior of MOVE.

**Audience.** The programme itself (the ledger, the site's instrument
page) and the owner as decision-maker. Secondarily: anyone who wants a
worked, falsifiable example of converting a measured hazard into a
sizing decision without a direction claim.

**Desired outcome.** A pre-registered decision engine — the exact
function from (measured trigger hazard lift, its CPCV uncertainty, the
prevailing cost of the structure, the risk budget) to (position size or
a documented refusal) — implemented, tested, and armed with kill lines
BEFORE the L2 trigger data exists, so that when C8 (or its successor)
produces numbers, the answer is a fill-in, not a design under
excitement.

**What success looks like.** (a) The engine refuses to size when the
lift posterior is uninformative — demonstrated on synthetic inputs,
both directions. (b) Every formula in the engine passes a
machine-checkable test before entering this spec (the math-harness
rule). (c) When real numbers arrive, the instrument produces one
number per trigger event: a size fraction, or zero with a reason, and
the forward log scores it in public.

**Constraints, risks, assumptions.**
- Constraint: no live trading, ever (standing rule). Free data only
  for now; the L0 gate already passed 2026-10-01 on the free day.
- Risk: W1's trigger layer depends on C8, which is blocked-on-data and
  whose amendments are NOT ARMED until the owner accepts them. W1
  therefore pre-registers its own kill lines independently and treats
  the trigger source as swappable.
- Risk: mid-range overconfidence is already flagged in the forward
  log's dress rehearsal — the calibration kill line below is live, not
  decorative.
- Assumption: the convexity sizing framework
  (`phase1_daily/convexity_economics.md`) is the governing sizing
  doctrine; W1 implements it, it does not replace it.
- Unknown: every quantitative input (baseline hazard at trigger
  scale, lift, payoff shape, costs) — marked UNKNOWN throughout.

---

## 1. Approaches considered (and why the chosen one wins)

**A. Long premium (buy straddles/strangles on primed entries, hold the
window).** Feasible only with an options market that this programme has
not acquired data for; and the convexity economics already forbids it:
when the baseline is 86%, holding time-value burns more than the +7.9
point edge. Rejected on cost and on data availability.

**B. Delta-neutral spot/perp replication of the straddle (directionless
spot-vs-perp structure, rebalanced), sized by the posterior.** Trades
the convexity without an options market, and the data (aggTrades, L2)
already exists in-programme. But rebalancing turns a clean convex
payoff into a path-dependent one, and every rebalance is a cost event
and a hidden parameter (band width) that would have to be
pre-registered and defended. Deferred: high implementation risk before
any trigger measurement exists.

**C. The trigger-to-size decision engine (chosen).** Do not build the
exposure yet; build the DECISION. The instrument is the function from
measured quantities to size-or-refuse, pre-registered and tested before
the numbers exist. The exposure (A's economics or B's replication) is a
pluggable payoff model evaluated by the engine, not the engine itself.

Comparison on the programme's own criteria: usefulness (C converts any
surviving trigger into an auditable decision immediately — highest);
feasibility (C needs no new data and no market — highest); originality
(A is the textbook move; B is known replication; C is the programme's
falsification-first method applied to sizing itself); cost/time (C is
null-time work, A and B are blocked); risk (C cannot flatter itself —
the refusal rule fires on synthetic data today); long-term value (C is
the bridge any surviving claim family must cross to become an
endpoint). Trade-off accepted: C alone trades nothing and earns
nothing; its value is realized only when a trigger layer survives. That
is the same trade the whole programme makes.

---

## 2. Falsifiable core

**W1 (the claim):** inside a primed macro state, an L2 trigger
signature (the C8 pair: excitation going critical, or absorption into a
standing counterparty) carries a CONDITIONAL HAZARD LIFT on the
release (a significant move at the instrument's own sigma scale within
H hours) whose CPCV lower bound exceeds 1.0 net of round-trip cost —
i.e., the trigger is a measurable WHEN, and the engine's refusal rule
does not fire. If the lift posterior straddles 1.0, W1 is dead by its
own K1 and the instrument's permanent output is zero.

W1 is deliberately downstream: it inherits the trigger from whichever
microstructure claim survives (C8, or the WATCH/cross-impact leads if
C8 dies its kill lines), and it inherits direction-refusal permanently.

## 3. Data and label

- Trigger-scale data: gated Tardis L2 (L0 gate already passed
  2026-10-01; the other days pending the owner's snapshot-coverage
  decision) plus the free aggTrades windows.
- Label: the release — a move of ≥ 2.5σ_w (the programme's standing
  significant-move scale, sigma units never points) within H hours of
  a trigger, H pre-declared per trigger family before measurement
  (UNKNOWN until the trigger spec fixes it; the C8 spec's short-horizon
  doctrine says hours, not weeks).
- The macro gate: the sealed C7 primed state. Outside a primed state,
  no trigger is a trade (conservative doctrine, unchanged).

## 4. Estimand

The out-of-fold conditional hazard ratio
    lift = P(release ≤ H | trigger, primed) / P(release ≤ H | primed)
as a CPCV distribution (point estimate alone is never sized). Secondary
estimand: the payoff shape — the distribution of move magnitudes
conditional on release, in R-multiples of the structure's defined
risk (UNKNOWN; measured when the trigger runs).

## 5. Kill lines (numbered, armed at declaration)

- **K1 (the refusal line):** the CPCV distribution of the lift
  straddles 1.0 (its lower bound ≤ 1.0) → W1 dead, instrument output
  is zero forever, recorded as the fourth-family-style honest death.
- **K2 (net-of-cost):** the net expected value of the sized structure
  (fee + half-spread at the prevailing book, the harvestable rule)
  is ≤ 0 at the lift LOWER bound → dead even if K1 passes.
- **K3 (calibration):** in the forward log, the realized release
  frequency inside the engine's pre-declared posterior bands must
  stay within the band (90% band coverage); mid-range overconfidence
  already flagged in the dress rehearsal makes this the live risk.
  Dies at the pre-declared miscalibration threshold: more than 1 of
  the first 10 scored rows outside the 90% band.
- **K4 (direction leakage / sign guard):** if any engine input or the
  sized outcome correlates with UP vs DOWN beyond the coin-flip band
  [0.497, 0.513], the instrument is contaminated — booked
  mechanism-refuted (sign), exactly as T1 was, per the T2 sign-guard
  precedent.
- **K5 (placebos):** era shuffle and 24h-shift trigger series must
  show no lift (the standing placebo battery); a lift under placebo
  kills the measurement, not the market.

## 6. What is deliberately NOT pre-registered

- The exposure instrument (options vs replication): a payoff MODEL is
  a pluggable input; choosing it before the payoff shape is measured
  would be fitting. Deferred by design.
- The horizon H per trigger family: fixed by the trigger spec that
  survives, not here.
- Any number: baseline hazard, lift, payoff R-distribution, costs —
  all UNKNOWN and all inputs, never constants, in the engine.

## 7. Execution order

1. This spec + the engine (`strategy/when_instrument.py`) + its test
   harness — null-time, done now.
2. The engine's formulas pass the math-harness rule (machine-checkable
   tests, both-direction ground truth) before any real input exists.
3. When the L2 gate fully passes and a trigger claim survives its own
   kill lines: measure the lift distribution, feed the engine, record
   size-or-refuse in the ledger, open the forward log rows.
4. K1–K5 decide. Either the instrument sizes real trigger events in
   the paper log (never live), or it dies at a documented line and the
   programme's map gains a closed page.

## 8. Plan: milestones, deliverables, timeline, measures, fallbacks

- **M0 (now, null time):** this spec; the engine; the tests. Deliverable:
   code + tests + this document. Success: refusal fires on synthetic
   wide posteriors; sizing fires only on synthetic separated ones.
- **M1 (when L2 data unblocks):** trigger measurement per the
   surviving trigger spec. Deliverable: the lift CPCV distribution in
   `paper/research/when_instrument/`. Success: K1 answerable.
- **M2:** first engine decision on real numbers; forward log rows
   opened. Success: a size fraction or a documented refusal, scored.
- **M3:** the calibration verdict (K3) at 10 scored rows. Success:
   inside the band; failure is a kill, not a tune.
- Timeline: M0 is the only schedulable milestone (everything else is
  gated on data access, which is the owner's call — unknown).
- Fallbacks: if C8 dies, W1 re-targets the surviving L2 leads (WATCH,
  cross-impact) unchanged — the engine is trigger-agnostic. If NO
  trigger survives, the instrument's honest terminal state is zero
  output with K1 booked, and the endpoint remains the completed
  ledger — which the roadmap already defines as a victory.

## 9. Self-review of this plan (weaknesses named)

- The engine's Kelly-flavored cap needs a payoff-odds input that is
  UNKNOWN; the engine must therefore refuse to size on any payoff
  guess, and the tests must prove it does. (Addressed: the payoff
  model is an explicit input with its own refusal on unmeasured
  inputs.)
- K3's "1 of 10 outside the 90% band" threshold: with 10 rows the
  binomial P(≥2 outside) at true 90% coverage is ≈ 26% — this line is
  deliberately strict (the dress rehearsal already flagged
  overconfidence), and the strictness is declared, not hidden.
- The spec cannot pre-register H without smuggling in a guess; that
  deferral is a real analyst degree of freedom and is named as such
  (section 6) rather than buried.
- The 0.940/0.862 C7 numbers travel with their disclosure: the edge is
  +7.9 points of occurrence over matched controls, measured once, on
  a sealed dataset, no second run.
