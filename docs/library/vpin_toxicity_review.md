# Library read — VPIN / order-flow toxicity (Easley, López de Prado & O'Hara, 2011/2012a/2012b)

**Venue:** RFS / JPM | **Category:** HF data & intraday, order-flow toxicity
**Status:** Deep-read from the library summaries (records 046, 047, 048 —
the papers are paywalled; the summaries are LLM-synthesized and flagged
as such, and this review cross-checks every load-bearing claim against
our own implementation and the known contestation literature). Read
2026-11-16 as the library ritual's third paper, against the ritual
question: **what here would kill C1-L2/C8 faster, or change its kill
lines?**

## Summary

VPIN measures order-flow toxicity — the rate at which informed flow
adversely selects market makers — by sampling trades in the VOLUME
clock (fixed-share buckets, not time bars), classifying each bucket's
volume into buy/sell fractions, and averaging the absolute imbalance
over a rolling window: OI_i = |V_buy − V_sell|/V_i, VPIN = mean(OI).
The famous claims: VPIN rose before the 2010 Flash Crash (047), and
liquidity providers monitoring toxicity would have withdrawn first
(046). The volume clock itself (048) is the deeper idea: activity-time
sampling stabilizes the statistics of flow.

## What it gives the programme — four items

**V1 — We hold the thing the paper had to approximate.** The papers use
bulk volume classification V_buy = V·Φ(z) — a PROBABILISTIC assignment
from standardized price changes — because TAQ trade records lack
reliable direction. Our aggTrades carry `is_buyer_maker`: TRUE taker
direction, zero classification error. Consequence, recorded as a
conditional pre-commitment (extending spec amendment A4): if a VPIN
trigger is ever added to C8, it must use true aggressor flags wherever
they exist; BVC may be computed only as a comparison, and the
BVC-vs-true divergence is a free diagnostic of how much of the paper's
signal was classification noise. The Andersen-Bondarenko contestation
makes this non-optional: their critique of the flash-crash claim is
precisely that VPIN's readings are sensitive to the classification
method.

**V2 — The vol-tautology sibling, in its original habitat.** The
contested part of the flash-crash claim is that VPIN's rise reflected
elevated 2008-2010 volatility, not toxicity — toxicity wearing a
volatility costume, the exact trap this programme names everywhere
else. If VPIN ever becomes a trigger, it inherits the same kill-line
discipline as compression: the trigger must survive conditioning on
realized volatility, and the era-shuffled placebo. No VPIN reading is
reportable without its vol-conditioned twin.

**V3 — The clock is the object.** 048's real contribution is the
volume clock: sampling in activity time stabilizes flow statistics.
Our C8 spec amendment A4 already fixes VPIN to the volume-bucket
construction and sends any alternative to the multiplicity ledger —
correct. One honesty note now recorded: the taker harness's
`_vpin_np` (T1/T2) uses TRADE-COUNT buckets (2,000 trades) with EWMA
span 50, not fixed-volume buckets — a different (related) object,
legitimate for the taker claims it served, and NOT silently
interchangeable with A4's construction. If VPIN crosses from the
taker harness into C8, the bucket construction changes and the change
must be logged in the multiplicity ledger, not inherited silently.

**V4 — The precedent cuts both ways, and C8's design already reflects
it.** The flash-crash narrative — a microstructure variable LEADING a
macro event — is the whole C8 hypothesis class; the contestation of
that narrative is why C8 insists on pre-registered kill lines rather
than post-hoc event stories. The lesson restated: the most seductive
result in this literature is the one that did not survive
conditioning. C8's K-line battery (and the A3 placebo, and the T-H
pre-conditions from the Hardiman-Bouchaud read) exists because of
papers like these.

## Verdict for the programme

No defect found in the repo's VPIN machinery: `_vpin_np` is honest
about its construction (trade-count buckets, true flags, EWMA), the
sign-shuffled placebo (`vpin_placebo_t0`) is exactly the right control,
and C8 correctly keeps VPIN as a documented future extension rather
than a trigger. What this read adds is the conditional pre-commitment
(V1: true flags, BVC as diagnostic only), the vol-conditioning rule
(V2), and the clock-construction ledger note (V3) — all recorded
before any L2 data exists.

A library is ammunition, not evidence: the summaries are flagged as
synthesized, the contestation is cited as contested, and nothing here
is laundered into a claim.
