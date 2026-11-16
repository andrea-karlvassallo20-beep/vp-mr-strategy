# Library read — The queue-reactive model (Huang, Lehalle & Rosenbaum, 2014)

**Venue:** arXiv:1312.0563v2 (Quantitative Finance) | **Category:** LOB microstructure
**Status:** Deep-read from the extracted text
(`docs/library/text/x8afb03_simulating_and_analyzing_order_book_data_the_queue.txt`)
against the ritual question: **what here would kill C5 faster, or change
its kill lines?** Read 2026-11-16 as the library ritual's fourth paper —
chosen because the replay days make passive cancellation the most alive
mechanism the gated L2 data will see (91.6–96.8% passive-cancel fraction
on all four days), and C5 ("absorption asymmetry, while price is flat")
is the claim that mechanism belongs to.

## Summary

The book is modeled as a Markov queuing system WITHIN periods of constant
reference price (mid): the intensities of limit insertion (λL),
cancellation (λC) and market orders (λM) at each limit depend only on the
current queue sizes. Estimated from ultra-high-frequency book updates,
the intensities are strongly state-dependent, the system is ergodic
(under two general assumptions), the invariant distribution is
determined by the arrival/departure ratio ρ(n) = λL(n)/(λC(n+1)+λM(n+1)),
and the price process emerges as the alternation of queuing periods and
reference-price jumps ("mechanical volatility").

## What it gives C5 — four items, all sharpenings

**Q1 — The classical linear cancel-rate assumption is empirically wrong.**
Their Figure 2: at the best limit, cancellation intensity is
increasing-CONCAVE for queue sizes 0–25 (average event sizes) and then
FLAT or slightly DECREASING — in explicit contrast to the linear
cancel-rate convention (Cont-Stoikov-Talreja 2010). The mechanism: the
priority value of a queued order rises with its position, and
high-priority orders are less likely to be canceled. Consequence for C5:
any absorption/withdrawal feature computed with a linear cancel-rate
model — or worse, a raw cancel FRACTION — is confounded by the queue-size
distribution. **State-conditioning on queue size is not optional.** The
91.6–96.8% passive-cancel fractions measured on the replay days are
consistent with ORDINARY saturated queuing; a fraction alone cannot
evidence withdrawal.

**Q2 — Front-of-queue and rear-of-queue cancels are different objects.**
The priority-value asymmetry means front orders persist and rear orders
churn. The passive-WITHDRAWAL mechanism C5 cares about (liquidity pulled
near the touch, the Tesla-day anatomy) is a FRONT-of-queue phenomenon;
rear cancels are benign queue management. A C5 feature that pools them
measures churn, not withdrawal. **The feature must separate front-vs-rear
cancels, or the claim is untested against its own mechanism.**

**Q3 — The queue-reactive null.** Within constant-mid periods the book
is an ergodic queuing system whose invariant distribution is fully
determined by the state-conditioned intensity ratios. This hands C5 its
strongest null for free: estimate the state-conditioned intensities on
the gated data itself, and require any "abnormal withdrawal" reading to
EXCEED what ordinary state-dependent queuing produces. The existing
shuffled-signs placebo stays; this null is stronger because it preserves
the book's own state dependence while removing the asymmetry.

**Q4 — The risk-set unit, validated.** C5's "while price is flat" clause
IS the queue-reactive periodization — the paper is the formal warrant
that constant-mid periods are the natural queuing windows, and that the
interesting dynamics are the transitions between them. C5's hazard model
should take the constant-mid queuing period as its risk-set unit, with
the break as the event — the same structure the paper's "mechanical
volatility" decomposition implies.

## Verdict for the programme

C5's kill line (in `paper/research/orderflow_program.md`) is armed but
its feature definitions are not yet state-conditioned. The four items
above are recorded as pre-conditions, added BEFORE the Tardis data passes
the gate: (a) all cancel/absorption features state-conditioned on queue
size and depth level, concave-saturation functional form allowed, never
a linear cancel rate; (b) front-vs-rear separation mandatory; (c) the
queue-reactive null beside the shuffled-signs placebo; (d) the
constant-mid queuing period as the risk-set unit. All are
harder-to-test additions — the only legal direction, per the amendment
discipline.

A library is ammunition, not evidence: this note cites the source; it
launders nothing.
