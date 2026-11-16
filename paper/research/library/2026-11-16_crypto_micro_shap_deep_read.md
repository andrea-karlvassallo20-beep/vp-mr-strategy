# Library deep-read session 4 — Bieganowski & Slepaczuk, "Explainable
# Patterns in Cryptocurrency Microstructure" (arXiv:2602.00776, 2026)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: the legally
acquired, page-marked extracted text
(`docs/library/text/xf03507_explainable_patterns_in_cryptocurrency_microstruct.txt`);
page cites are to that PDF. Rank 2 of the 500-paper edge triage
(`docs/library/edge_triage_500.md`).

## The paper in one paragraph

On Binance FUTURES PERPETUAL order books and trades (BTC, LTC,
ETC, ENJ, ROSE — an order of magnitude in market cap; 1-second
snapshots, Jan 2022 - Oct 2025), the authors show that engineered
book/trade features (OFI, spreads, depths, trade imbalance) have
STABLE cross-asset predictive importance and SHAP dependence
shapes for short-horizon returns, under CatBoost with purged
walk-forward CV and a direction-aware GMADL objective. They
validate tradability with taker and maker backtests, and their
headline novelty is a natural experiment: the October 10, 2025
flash crash, where the taker strategy profited while the naive
maker was catastrophically adversely selected.

## Findings, graded (does any kill line move?)

**NO kill line changes.** All five C1-L2 lines and C8's eleven
stand. Two candidate sharpenings (owner ratification required) and
several gifts:

1. **[sharpening, owner must ratify] The October 10, 2025 flash
   crash is IN THE TEST YEAR and must be pre-declared.** The
   project's 2025-26 test window contains this event (PDF pp.
   18-22: taker profits, maker destroyed by adverse selection;
   crash dynamics around 23:20-23:27 UTC). If C1-L2/C8 results pool
   the crash silently, an effect that is really "the model went
   short once during a crash" contaminates the whole reading.
   Candidate pre-declaration: name 2025-10-10 in the split
   manifest as an event window to be REPORTED SEPARATELY from the
   pooled test reading (the K4 regime-reproduction line demands
   per-regime honesty anyway; this makes it concrete).
2. **[sharpening, reinforcing session 5's wash-trading audit] The
   spoofing cascade, demonstrated.** "A single, large, non-bona
   fide order could theoretically trigger a cascade of algorithmic
   trades" (PDF p. 20) — their model reacted to a large shallow
   bid with an immediate large prediction (PDF p. 20, Fig. 15).
   OFI-shaped triggers are spoofable BY CONSTRUCTION; this is the
   session-5 candidate gate audit (burst/order-without-price-change
   fraction in trigger windows) now backed by a demonstrated
   mechanism on the same venue. Recorded as reinforcing evidence,
   not a new line.
3. **[support, not a pass] The venue evidence cuts in C1-L2's
   favor — at the WRONG horizon.** Stable, cross-asset OFI
   predictability on Binance perps at 1-second horizons (PDF pp.
   1-2, 5-6) supports the premise that the perp book carries
   signal daily bars cannot see. But their horizons are seconds;
   C1-L2/C8 live at 30m-4h-24h. The paper therefore MOTIVATES the
   gate but tests none of our claims — the horizon gap is exactly
   the C8 hypothesis's unexplored cell, and this paper is the
   citation for "the math works at micro horizons on this venue,"
   which the C8 spec's hypothesis statement can cite.
4. **[gift, free to take] GMADL as a candidate responder metric.**
   The direction-aware, magnitude-weighted loss
   (PDF pp. 6-7) rewards being right when it matters and ignores
   trivial fluctuations — a candidate evaluation metric for
   C1-L2's short-horizon responder label, complementary to the
   rank-Spearman used at 4h. Owner's choice at model-selection
   time; recorded so it is on the menu before the data arrives.
5. **[methodological precedent] Their purged walk-forward** with
   an explicit temporal gap "critical to reduce information
   leakage, especially from features with slow time dynamics"
   (PDF p. 6, Fig. 2) is an independent, same-venue citation for
   the programme's purge/embargo discipline — useful for the
   paper draft, not a change.
6. **[honest caution, systemic not methodological]** Their policy
   reading (PDF p. 20): a market where everyone runs the same
   imbalance signals is fragile; homogenized algorithms were part
   of the crash cascade. For the programme: if C8 passes, its edge
   is the INTERACTION (state x trigger), not the raw trigger the
   crowd already runs — which is both the commercial point and a
   reason the raw-trigger-alone comparison (C8-B) must be the
   honest baseline.

## What this paper would have killed if we had done it wrong

If the test-year reading had pooled the Oct 10, 2025 crash without
naming it, a single well-timed short would masquerade as a
general hazard effect — the exact "one regime artifact" failure
K4 exists to catch. The sharpening in item 1 makes the event a
named, reported window before any model runs. Grade: **no kill
line changed; the split manifest gains a candidate named event,
pending the owner's ratification** — same protocol as sessions
1, 3, 4/4b, 5; nothing is armed by this note.

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
lauanders. Their data is 1-second snapshots (coarser than the
Tardis incremental feed), their strategies are theirs, and their
authors' venue access and ours differ in kind. The Oct 10, 2025
event date is taken from their account and should be verified
against the Binance feed itself when the L2 data arrives — the
L0 gate's audit, not this paper, is the authority on what
actually happened.
