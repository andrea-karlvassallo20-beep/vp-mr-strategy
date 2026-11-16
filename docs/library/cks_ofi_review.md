# 018 — The Price Impact of Order Book Events (Cont, Kukanov & Stoikov, 2014)

**Venue:** Journal of Financial Econometrics | **Category:** Microstructure & order flow
**Status:** Deep-read from the extracted text (`docs/library/text/018_cont_kukanov_stoikov.txt`,
arXiv:1011.6402v3) against ONE question, per the null-time programme's
library ritual: **what here would kill C1-L2 faster, or change its kill
lines?** Read 2026-11-16, after the math verification
(`paper/research/math_verification_2026-11-16.md`) had already made this
paper's OFI formula authoritative in this repo and fixed defects D1-D5.

## Summary

CKS regress 10-second mid-price changes (in ticks) on the order flow
imbalance — the sum of best-quote event contributions over the same
interval, where limit orders add, market orders and cancels subtract,
and same-price queue changes contribute the queue delta. On NYSE TAQ
data for 50 stocks, the relation is linear with average R² ≈ 65%,
robust across stocks, timescales (10 quote updates to 10 minutes) and
seasonality. The impact coefficient β is inversely proportional to
average depth (β = c/AD^λ with λ̂ ≈ 1, unrejected in 35/50 stocks), and
the model plus a scaling argument implies the square-root law. Trade
volume, by contrast, explains price changes poorly. This is the paper
the L2 phase's OFI layer stands on.

## The β-factor bug's siblings — the hunt, and what it found

The D5 lesson (a metric overstated by a silent normalization factor) is
a *class* of defect. The hunt looked for members of that class in the
CKS machinery itself and in our use of it. Five siblings found and
named:

**S1 — The AD denominator's off-by-one.** CKS define average depth as
AD_i = (1/(2(N(T_i)−N(T_{i−1})−1))) Σ(q^B_n+q^A_n): BOTH sides summed
over the interval's events, divided by 2(N−1), not 2N. The −1 is theirs
and it is load-bearing (N−1 consecutive differences exist between N
events). A "normalized OFI" implementation that divides by event count
N, or by one side only, or by the last snapshot depth, silently
rescales the impact coefficient the way D5 rescaled the branching
ratio. **Action for the L2 layer:** when OFI is normalized by depth,
transcribe the AD formula literally and unit-test the denominator
against a hand-built 3-event interval.

**S2 — λ is estimated, never assumed.** β = c/AD^λ with λ̂ close to but
not exactly 1 (rejected for 15/50 stocks). The stylized model says
λ=1, and the paper is explicit that λ=1 is "a good approximation for
most of the stocks" — approximation, not identity. Any L2 feature of
the form OFI/AD carries an exponent choice that must be either
estimated on data we hold out or declared as an approximation with its
bias named. **Kill-line sharpening:** if the C1-L2 OFI feature is
normalized by depth, the λ used must be fixed in the pre-registered
spec before the Tardis data is touched, exactly like every other
parameter.

**S3 — ΔP is in TICKS, β's units are tick/share.** CKS's ΔP_k =
(P_k−P_{k−1})/δ. A regression on dollar or percentage price changes is
a different model with a different β, and cross-venue or cross-time
comparison of impact coefficients is meaningless without the tick-size
normalization. Binance perps have variable tick size by price bracket —
a sibling trap specific to us: the L2 replay must carry the active
tick size per timestamp, and any OFI-impact regression must state
whether ΔP is in ticks of *which* bracket.

**S4 — The paper's own tautology footnote is the vol-tautology kill
line's grandfather.** CKS note (their footnote 3) that OFI includes
price-changing events, creating "a possible tautology in the
regression... inherent to all price impact modeling." Their defense:
excluding price-changing events from OFI, R² stays in 35-60%. This
is EXACTLY the discipline the owner's directive demands of T1 — the
compression hazard must survive conditioning on realized volatility,
just as the OFI-impact relation must survive the exclusion of the
mechanically-price-moving events. The L2 kill-line battery should
include CKS's own control verbatim: **recompute the OFI-impact
relation excluding price-changing events from the OFI aggregate; if the
relation dies, it was book-mechanics wearing a costume.** This is a
stronger, more literal control than a vol covariate and it is
pre-registered in the source paper.

**S5 — Concurrent-flow compensation.** CKS are explicit (their §2.3)
that an order's realized impact depends on the other orders in the
same interval: an order against the concurrent flow may have zero
instantaneous impact. The sibling of D4 (an orientation
inconsistency): any per-event attribution of impact (including our
DML orthogonalization of Layer-2 features) must respect that the unit
of impact is the *interval aggregate*, not the single event. Features
built per-event and summed are fine; features built per-event and
*interpreted* per-event are not.

## What CKS cannot give us (the standing constraint, in their words)

The paper's central result is that quote events — limit orders and
cancellations — carry the price-impact information that trades alone
do not ("the relation between price changes and trade volume is found
to be noisy and less robust than the one based on order flow
imbalance"). This is the taker-only constraint stated from the other
side: aggTrades-based work (T1, T2) is measuring the flow CKS
themselves say is the *worse* regressor. T1's result, whatever it is,
cannot speak for the quote side — and if T1 dies, it dies as a
taker-side claim only; the passive-withdrawal mechanism (C5/C6) remains
exactly as alive as before.

## Verdict for the programme

No new defects found in the repo's verified OFI implementation (it was
re-checked against the source formula branch-by-branch in the math
verification; max abs diff 0.0). Five siblings named; two demand
action in the C1-L2 spec before the Tardis data arrives: the AD
denominator unit test (S1) and the CKS literal tautology control (S4).
Both are kill-line sharpenings, not new claims — they make the L2
test harder to pass, which is the direction the programme prefers.

A library is ammunition, not evidence: this read note cites the source;
it launders nothing.
