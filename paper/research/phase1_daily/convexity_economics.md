# The Economics of Convexity — Sizing a C7-Primed Market

Status: THEORETICAL FRAMEWORK, pre-registered before the L2 data arrives.
No code run, no backtest, no numbers beyond the sealed C7 record. This
document exists so that when the trigger layer passes its gates, the
program has a decision context that was declared before any economics were
measured — the same discipline that sealed C7.

## 1. Why the 86% baseline forbids holding premium long

The sealed C7 numbers: P(significant move ≤ 60 trading days | primed) =
0.940, versus climatology 0.862. The edge is +7.9 points of OCCURRENCE
probability over matched quiet controls — measured, real, and sealed.

Now the economics, stated plainly: when an event is 86% likely to happen
anyway, you cannot pay time-value to own it. Anyone can buy a 12-week
"something will happen" exposure in crypto — the market prices near-certain
volatility into every options chain. Holding a plain long position for
weeks inside a primed state pays theta on an event the whole market knows
is near-certain, and the 7.9-point edge is smaller than the premium burned.
**Therefore: the C7 edge is not harvestable by holding; it is harvestable
only by TIMING.** The 12-week window is the validity period of the
conditional probability — never the intended holding period.

## 2. The shape of the exposure: convex, directionless, short-horizon

Direction is refused by measurement (the 0.505 boundary). So the exposure
must be:

- **Convex:** defined-risk on entry (the maximum loss is the premium at
  risk or the stop width), open right tail (the release is not capped in
  advance). Straddle-shaped economics without a direction claim.
- **Directionless in construction:** the trade is "the release has begun,"
  sized to survive being wrong about side. In practice this means either
  symmetric structures, or explicitly two-sided entries where the L2
  trigger's sign (absorption side) is the only directional content — and
  that content is itself an untested claim until C5 faces data.
- **Short-horizon:** hours, not weeks. The entry is the trigger; the exit
  is flow exhaustion (Hawkes intensity decaying back through its baseline)
  or the vertical barrier — whichever comes first.

## 3. The trigger: converting inevitability into an entry

The L2 layer turns the 12-week inevitability into an hours-scale decision.
Two pre-declared trigger signatures (both descriptive until the gated data
says otherwise):

1. **Excitation going critical (the release).** The Hawkes branching ratio
   rising toward criticality within the instrument's book — trades
   provoking trades at an accelerating rate. The dry-run measured branching
   at the 0.95 stationarity cap on real ticks; a trigger is the
   time-local departure from that instrument's own baseline, not an
   absolute level.
2. **Absorption into a standing counterparty (the loading).** One-sided
   order-flow imbalance (OFI) against a flat price with declining impact
   per unit of flow (Kyle's lambda falling on the aggressed side) — someone
   is eating the flow without letting price move. The release tends to come
   when the absorber is exhausted or withdraws.

The entry fires when a trigger signature occurs inside a C7-primed macro
state. Outside a primed state, the same signature is NOT a trade — C8's
interaction question is precisely whether the signature carries more
information inside primed states, and until C8 faces data, the doctrine is
conservative: no primed state, no trigger trade.

## 4. The sizing framework (theoretical, pre-data)

Position size is a function of measured quantities only, per the Layer 4
doctrine (drawdown controlled by refusing to size when the posterior is
wide, not by stacking stops):

1. **The unit of edge:** the trigger's CONDITIONAL HAZARD LIFT — the
   out-of-fold hazard ratio of the release arriving within the next H hours
   given the trigger, versus the same instrument's baseline hazard. This is
   what the L2 test will measure; it is currently UNKNOWN. No sizing
   number is invented here.
2. **Size to the lower confidence bound:** size ∝ the LOWER bound of the
   CPCV distribution of the hazard lift — never the point estimate. A wide
   posterior means a small position or no position; the framework refuses
   to size enthusiasm.
3. **The Kelly-flavored cap:** with edge e = (hazard-lift lower bound −
   baseline) and odds set by the convex payoff's risk/reward, the size is
   a quarter-Kelly of that edge — the repo's standing haircut — and the
   CVaR constraint binds at the portfolio level: the expected loss in the
   worst decile of simulated trigger outcomes must stay inside the
   drawdown budget.
4. **The refusal rule:** if the trigger's CPCV distribution straddles 1.0
   (no measurable lift), the position is ZERO regardless of how primed the
   macro state is. C7's sealed edge is occurrence probability, not timing
   — and un-timed occurrence probability is un-harvestable premium. The
   framework would rather miss the move than pay theta on an 86%-baseline
   event.

## 5. Honest boundaries of this framework

- Every quantity in section 4 is unmeasured until the Tardis data passes
  the verification gate and the L2 tests run. This document pre-registers
  the SHAPE of the decision, not the numbers.
- No Sharpe ratio will ever be reported without a CPCV distribution and a
  Deflated Sharpe Ratio; no simulated profitability is proof of a
  real-world edge; paper trading precedes everything.
- The framework contains no direction claim. If C5 (absorption asymmetry)
  later passes its kill lines, direction content may enter through the
  trigger's sign — until then, two-sided or nothing.
- The 86% baseline disclosure travels with every future citation of C7:
  the edge is +7.9 points of occurrence over matched controls, measured
  once, on a sealed dataset, with no second run.
