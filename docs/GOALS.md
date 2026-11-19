# GOALS.md — the fronts status board (operative work-selection companion)

**Status:** the session-facing status board for the goal-state fronts, per
the conductor protocol (goal state **edition 2**, protocol section 2;
rotation guidance, section 3; weekly directorate, section 6; landed
2026-11-19) and the owner's standing order recorded MADE in
`docs/DECISIONS_PENDING.md` (resolved item, 2026-11-19). The protocol's
section 2 is the ranking authority: numbered fronts 1–8, each with entry
criteria, what it feeds, and its own gate. This file does not re-rank
or reinterpret any front. It carries (a) a STATUS line per front,
refreshed as sessions advance them, (b) the rotation rule in operational
form, and (c) three additional standing work-fronts (G1–G3) not in the
goal state, added by session 57 with zero authority over any gate,
claimable per the standing order's carve-outs. Sessions read the live
main tail first, then the protocol's section 2, then this file, then
choose work and record the choice and the reason in their
session-state note. Nothing here overrides any hard gate.

## The rotation rule (operational form of protocol section 3)

1. Front 4 (the synthesis pass) when due outranks everything else, run
   first — as its own session, or before its other work.
2. Otherwise take the lowest-numbered ready front in the protocol's
   section 2 least recently advanced; ties break toward the lower
   number.
3. The deep-read queue (front 2) is one front among the others, not
   the automatic default; repeating it in consecutive sessions needs
   a recorded reason.
4. "Ready" = the front's entry criteria met and the front not blocked.
   A blocked front is advanced only by unblocking bookkeeping, never
   by violating its gate.
5. If no numbered front is ready, a G-front below is claimable,
   lowest number first.
6. Fail-safe: if the protocol or this file is unreachable, truncated,
   unparseable, or internally inconsistent, run the fixed standing
   ritual unchanged and record the failure. The ritual is never
   blocked by either file's condition.

## Status board (protocol section 2, edition 2)

- Front 1 — the gated L2 window. STATUS: blocked on the owner
  (environment + data); the L0 dry run is unblocked by the recorded
  L0 amendment; never claimable by a session.
- Front 2 — the library deep-read queue. STATUS: ACTIVE. Next UNREAD
  at edition time: "From Glosten-Milgrom to the whole limit order book
  and applications to financial regulation" (score 29, x0d8b2a),
  behind it "A Hawkes Microfoundation for Multitype Inverse Gaussian
  Subordinators" (score 29, xf77014); re-read the live tail before
  consuming; the ritual's slug-keyed unread rule applies.
- Front 3 — the misses curriculum. STATUS: built and validated;
  blocked on the codespace/data presence; the tooling refuses to run
  without real klines, and no invented data is substituted.
- Front 4 — the synthesis pass. STATUS: next due when five or more
  deep-read sessions have landed since goal-state edition 2 (deep-read
  #50 onward; edition 2 was recorded with the deep-read counter at
  49).
- Front 5 — gap-driven probes. STATUS: standing, per
  `docs/exploratory_channel.md`; up to one block per session at the
  session's discretion.
- Front 6 — the website honesty pass. STATUS: standing risk,
  periodic; entry when any prose page states a moved claim status.
- Front 7 — the macro-timeline backfill. STATUS: standing;
  owner-curated; proposed rows with sources only.
- Front 8 — instrument upkeep. STATUS: nightly and automated
  (board_refresh.py, surprise_ledger.py); audit by reference only;
  never re-done by hand.

## G-fronts (added session 57, log entry ## 61; zero claim authority)

G1. Sealed-prediction record readouts. ENTRY: the nightly ledger holds
resolved pairs not yet read out at the last recorded readout; a
named, dated readout is due at ~100 resolutions. FEEDS: the honest
verdict on the priming-score ranking at daily grain — the only
running cross-sectional falsefication of it that exists. BOUNDARY:
descriptive bookkeeping of an already-running instrument; nothing
closes, arms, or is cited as evidence at daily grain. STATUS:
RUNNING nightly, automatic; milestone watch on the resolution count.

G2. Ratification-readiness briefs. ENTRY: any session; strongest
claim when front 2 is between reads. FEEDS: the weekly directorate —
one-page accept/reject briefs for the queued TWENTY-NINE sharpenings
plus probe E1, grouped by the precedent they tighten. BOUNDARY:
briefs summarize already-recorded proposals with their sources; a
brief invents nothing, queues nothing new, and arms nothing. STATUS:
not started; the queue is enumerated in the log's latest section.

G3. C8 skeleton coherence. ENTRY: after a synthesis pass with
C8-relevant output, or on finding a gap in the skeleton's
pre-registration bookkeeping. FEEDS: the C8 spec's readiness, so the
moment the gate opens nothing is improvised. BOUNDARY: A1–A5 stay
PROPOSED and owner-gated; sessions maintain coherence records only,
and the spec is edited only through the standing amendment-log rules.
STATUS: waiting on the L2 gate; pre-registration bookkeeping only.

Edition 1, recorded 2026-11-19 (null-time session 57, log entry ## 61).
The status lines above are refreshed by sessions as they advance fronts
and by synthesis passes; rankings and gates live in the protocol,
never here.
