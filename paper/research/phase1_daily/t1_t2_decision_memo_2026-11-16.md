# Decision memo: run T1 and T2 after T3's death?

**For the owner.** The taker-side falsification harness (PR #111) stopped
at T3's kill line — trades/min HR = 0.9998, 95% CI [0.99977, 0.99983],
p = 4.7e-42 after hour-of-day stratification. Wall-clock exposure does
NOT remove the trade-arrival-density dependence: tested-fail, dead
mechanism named. T1 and T2 are cached and ready (`--claims t1,t2`,
spells already built). One command. This memo lays out both sides so
the call can be made in thirty seconds later.

## The case for stopping (the current protocol)

The runner was pre-registered as stop-at-first-upstream-kill. T3 was
the upstream *clock-validity* test: its purpose was to establish that
the event-clock covariates mean the same thing in physical time before
any downstream hazard claim is interpreted. T3's death means the
clock-invariance premise is false — quiet sessions carry tighter
sigma-scaled barriers, so the density effect is vol-mediated. Under
this reading, T1 (compression duration-dependence) and T2 (Hawkes /
VPIN direction) would be interpreted on a clock whose meaning just
failed its own validity test: results would be uninterpretable, and
running them risks generating numbers we cannot honestly use.

## The case for running (the counter-argument)

T1 and T2 are *separate pre-registered claims*, not corollaries of T3.
T3 asked "does wall-clock exposure remove the arrival-density
artifact?" — answer: no. But T1 asks a different question: does hazard
rise with compression duration on the event clock, with the
scale-invariance null and block-temporal placebo as its own guards?
T2 asks whether 2D Hawkes buy/sell excitation breaks the 0.505
directional boundary. Their kill lines are armed and independent of
T3's verdict. The registry's original directive was "execute T3 →
T1 → T2" — the stop-at-first-kill rule was a runner-design decision,
recorded in PR #111, not a registry amendment.

The strongest form of the counter-argument: T3's death makes T1 MORE
informative, not less. We now know the density effect is vol-mediated.
If T1's compression-duration hazard ALSO survives its scale-invariance
null, we have two vol-adjacent effects and must ask whether "liquidity
compression" is doing any work beyond realized vol — which is exactly
the vol-tautology kill line T1 already carries (HR CI conditioned on
sigma_H). If T1 dies on the tautology line, the whole family collapses
honestly. Either way the ledger gains a real entry.

## My recommendation (non-binding, recorded)

**Run T1. Do not run T2 yet.** T1 is a WHEN-family claim — it tests
the programme's core (duration-dependence of the hazard) and carries
its own tautology guard, so its result is interpretable regardless of
T3. T2 is a DIRECTION-family claim (2D Hawkes directional Brier vs
the 0.505 boundary) on taker-only data with no book — and the
programme has already re-framed its endpoint as a WHEN instrument
(methodology review, W-series). Spending the run on direction before
the L2 book arrives inverts the priority order the review just
established. If T1 survives, the WHEN family advances; T2 can wait
for full L2 where its Hawkes channels (cancellations) actually exist.

**The decision is yours.** Nothing runs until you say so.

## Either way, the next L2-dependent unit is unchanged

C1-L2 remains blocked on the snapshot-coverage decision (paid
book_snapshot_25 for 2026-10-02..04, or the recorded spec amendment).
The four-day raw replay, the gate, and the reconciliation stand as
reported in PR #112.
