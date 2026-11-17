# The Convexity Sizing Framework — from a C8 pass to a position

Status: **DRAFT, pre-registered.** The decision SHAPE is frozen here,
before any economics are measured, so that a C8 pass has somewhere to go
besides celebration. Every symbol below is bound at test time from
measured quantities; no number is invented in this document. Companion
to `paper/research/convexity_economics.md` (the theoretical framework)
and `paper/research/c8_macro_l2_synthesis_spec.md` (the claim whose
pass this document converts).

---

## 1. The problem, stated once

C8 passes means: inside the combined state (macro-primed AND
L2-triggered), the hazard of a breakout within H hours is strictly
greater than either layer alone, with the interaction real. That is
INFORMATION. The question here is the next one: how large a position
does that information justify — given that

- the event is 86% likely to happen anyway within 60 days (the sealed
  C7 baseline: 0.940 vs 0.862), so holding premium to own it is a
  losing trade against theta;
- direction is refused (the 0.505 boundary stands; the endpoint is a
  WHEN instrument sized on MOVE, not UP);
- the payoff is convex: defined risk at entry, open tail at exit.

## 2. The inputs (all measured, none chosen)

| Symbol | Meaning | Source |
|---|---|---|
| `h0` | baseline hourly breakout hazard for the instrument (climatology) | measured from the gated L2 window |
| `HR` | out-of-fold hazard ratio of the trigger INSIDE primed states | C8's interaction term, CPCV distribution |
| `HR_LB` | lower bound of the HR's day-block bootstrap 95% CI | C8's inference, as registered |
| `H` | holding horizon (hours): flow exhaustion or vertical barrier, whichever first | C8's 4h primary clock |
| `R` | risk per unit: premium at risk or stop width, in account-currency terms | the entry structure |
| `G` | expected gross multiple on risk at the lower bound | measured from the trigger's OOF outcome distribution |
| `B` | drawdown budget share for this strategy class | portfolio overlay, owner-set |

## 3. The sizing rule, in order of application

**Step 1 — the refusal gates (any one fires, size = 0):**

- `HR_LB ≤ 1.0`: no measurable lift at the lower bound → **zero**,
  however primed the macro state. (The framework refuses to size
  enthusiasm; C7's sealed edge is occurrence, not timing.)
- The declared-gap iteration: results produced under the L0 amendment's
  known data gap are **paper/shadow only** → size 0 in capital terms
  until the continuous window is acquired.
- Boundary-constrained Hawkes fits (ρ̂ ≥ 0.949) in the trigger window →
  the trigger is measuring the estimator's cap → **zero** for that
  signal (C8's K7 applies at sizing time too).

**Step 2 — the hit probability at the lower bound:**

    p = 1 − exp(−HR_LB · h0 · H)

Inside the combined state the hazard is `HR_LB · h0` (the conservative
bound, never the point estimate). `p` is therefore the probability the
release arrives within the holding window, priced pessimistically.

**Step 3 — the Kelly fraction for a defined-risk convex bet:**

With payoff odds `b = G` (expected gross multiple on risk at the lower
bound), the Kelly fraction is

    f* = (p · b − (1 − p)) / b

and the position risks

    risk_amount = ¼ · f* · B · equity

The quarter-Kelly haircut is the programme's standing haircut; `B`
caps the strategy class inside the drawdown budget so no single
trigger family can consume the account.

**Step 4 — the CVaR overlay (binding, not advisory):**

Simulate the trigger's OOF outcome distribution (the same CPCV paths
C8 produced). The expected loss in the worst decile of simulated
trigger outcomes must satisfy

    CVaR₁₀% (concurrent trigger book) ≤ B

All concurrent trigger positions on the SAME book count as ONE trade
(the book is the asset; BTC's book cannot be diversified by taking
the same signal twice). Cross-instrument concurrency does not exist
yet by the one-instrument-first law.

**Step 5 — the exit (pre-committed, not chosen later):**

The exit is not a size decision but it binds the size: `G` and `H`
must be estimated under the exit rule "flow exhaustion (Hawkes
intensity decaying through its baseline) or the vertical barrier,
whichever comes first." Any exit rule change re-estimates `G` from
scratch; it does not re-fit the entry.

## 4. Why the 86% baseline makes the trigger, not the coil, the trade

The coil says: within 60 trading days, this releases with probability
0.940 — versus 0.862 for quiet controls. The market prices most of
that near-certainty into every instrument that can express it. Paying
weeks of time-value to own an 86%-baseline event burns more premium
than the +7.9 points are worth. **The coil is the validity period of
the conditional probability; the trigger is the trade.** The sizing
rule above therefore prices hours, not weeks, and Step 1's refusal
gate is the exact arithmetic expression of that discipline: a
primed state with no measurable trigger lift is worth exactly zero.

## 5. What this draft deliberately does not contain

- No expected Sharpe, no projected returns, no account growth curves.
  A hazard is information; this document converts it to risk amounts
  and refuses to convert it to forecasts.
- No direction content. If C5 later passes, direction may enter
  through the trigger's sign — until then the structure is two-sided
  or nothing.
- No capital moves before Layer 4 shadow: the first live application
  of this framework is paper, on the forward window, with the ledger
  recording every sizing decision the framework makes.
- No re-estimation of any input on the discovery panel. `h0`, `HR`,
  `G` come from the gated L2 window and the frozen split manifest, or
  they do not exist.

## 6. The one-sentence version

A C8 pass converts to a position by risking a quarter of a
lower-bound Kelly fraction of the drawdown-budget share on the
hours-scale release, at zero size whenever the lift's lower bound
fails, the estimator is at its cap, or the data carries a declared
gap — and never by holding an 86%-baseline event for weeks.
