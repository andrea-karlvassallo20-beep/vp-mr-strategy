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
goal state, added by session 60 with zero authority over any gate,
claimable per the standing order's carve-outs. Sessions read the live
main tail first, then the protocol's section 2, then this file, then
choose work and record the choice and the reason in their
session-state note. Nothing here overrides any hard gate.

## BOARD DIRECTIVE, 2026-11-19 (freeze, archive, launch — the Board's
## dated word; it overrides the protocol's ranking for work selection)

**The NQ Weekly OHLCV track is ARCHIVED.** The thesis v1.0's own honest
timeline is 5-29 years of forward record to prove the weekly claim; the
programme does not have that time, and the Board's word archives the
track. Archived is NOT falsified: the weekly claims stand published,
unfalsified, and unproved; every kill line stays frozen; the forward log
stays empty by directive; the BTC arm (Amendment 13 C-W1), the A9 macro
booking and the stage-7 paper track are archived with it, not killed.
Re-opening the track takes the owner's dated word.

**THE ONLY ACTIVE RESEARCH FRONT IS THE L2 TRACK: C1-L2 → C8 → Convexity
Sizing.** Within the fronts below, Front 1 (the gated L2 window) is the
critical path and carries the whole chain. Fronts 2–8 remain as standing
supports (the library, the probes, the site honesty, the macro timeline,
the instrument upkeep) in service of the L2 chain; nothing that produces
NQ-track forward rows is claimable while the archive stands. The thesis
itself is frozen at the repo root (v1.0, PDF) and adds zero status by
construction.

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
7. Board directive above: while the archive stands, any work whose
   output is an NQ-track forward row is not claimable, regardless of
   readiness; L2-chain work takes precedence over all fronts that
   serve it.

## Status board (protocol section 2, edition 2)

- Front 1 — the gated L2 window. STATUS: THE CRITICAL PATH (Board
  directive, 2026-11-19). Still blocked on the owner (environment + data:
  a paid Tardis key as a Codespaces secret, then the 2-4 week window per
  `paper/research/l2_data_acquisition_spec.md`); the L0 dry run is
  unblocked by the recorded L0 amendment; never claimable by a session.
- Front 2 — the library deep-read queue. STATUS: ACTIVE. Next UNREAD
  after the ## 61, ## 63, ## 66, ## 67, ## 68 and ## 70 landings
  (2026-11-19; x0d8b2a, xf77014, xb710f4, x77c554, xdb216a and
  x72c407 consumed):
  "Forecasting duration in high-frequency financial data using a
  self-exciting flexible residual point process" (score 28, x72c407);
  behind it "Optimal trade execution and price manipulation in order
  books with time-dependent liquidity" (score 28, x95643a); re-read
  the live tail before consuming; the ritual's slug-keyed unread rule
  applies. NOTE ## 68: the deep-read counter since goal-state edition
  2 reached FIVE (deep-reads 50-54). NOTE ## 69 (null-time session
  65): the due synthesis pass RUN — goal-state EDITION 3 recorded by
  the first synthesis pass (statuses recomputed; four named gaps;
  cadence reset); the pass's work-selection guidance names G2 below as
  the strongest next non-deep-read choice. NOTE ## 70 (null-time
  session 66): deep-read 55, the FIRST since edition 3 — the
  self-exciting flexible residual duration-forecasting paper read
  (x72c407 consumed, NO sharpening, NO kill line change); the counter
  since edition 3 stands at ONE.
- Front 3 — the misses curriculum. STATUS: built and validated;
  blocked on the codespace/data presence; the tooling refuses to run
  without real klines, and no invented data is substituted.
- Front 4 — the synthesis pass. STATUS: RUN as ## 69 (2026-11-19):
  goal-state EDITION 3 recorded (protocol section 2 rewritten whole by
  the first synthesis pass; fronts unchanged in order, statuses
  recomputed; four named gaps at zero status; cadence reset). Next due
  when five or more deep-read sessions have landed since edition 3
  (deep-read #55 onward).
- Front 5 — gap-driven probes. STATUS: standing, per
  `docs/exploratory_channel.md`; up to one block per session at the
  session's discretion.
- Front 6 — the website honesty pass. STATUS: standing risk,
  periodic; entry when any prose page states a moved claim status. The
  thesis-freeze banner (v1.0 published, NQ archived, L2 engaged) landed
  2026-11-19 with this directive.
- Front 7 — the macro-timeline backfill. STATUS: standing;
  owner-curated; proposed rows with sources only. The A9 macro BOOKING
  task is archived with the NQ track (Board directive, 2026-11-19);
  macro rows are owner-curated only while the archive stands.
- Front 8 — instrument upkeep. STATUS: nightly and automated
  (board_refresh.py, surprise_ledger.py); audit by reference only;
  never re-done by hand.

## G-fronts (added session 60, log entry ## 64; zero claim authority)

G1. Sealed-prediction record readouts. ENTRY: the nightly ledger holds
resolved pairs not yet read out at the last recorded readout; a
named, dated readout is due at ~100 resolutions. FEEDS: the honest
verdict on the priming-score ranking at daily grain — the only
running cross-sectional falsification of it that exists. BOUNDARY:
descriptive bookkeeping of an already-running instrument; nothing
closes, arms, or is cited as evidence at daily grain. STATUS:
RUNNING nightly, automatic; milestone watch on the resolution count.
NOTE 2026-11-19: this G-front's readouts belong to the archived NQ
track's instrumentation; its descriptive bookkeeping stays lawful,
its verdicts stay frozen, and nothing here re-opens the archive.

G2. Ratification-readiness briefs. ENTRY: any session; strongest
claim when front 2 is between reads. FEEDS: the weekly directorate —
one-page accept/reject briefs for the queued THIRTY-TWO sharpenings
plus probe E1, grouped by the precedent they tighten. BOUNDARY:
briefs summarize already-recorded proposals with their sources; a
brief invents nothing, queues nothing new, and arms nothing. STATUS:
not started; the queue is enumerated in the log's latest section.
NOTE ## 69 (the edition 3 work-selection guidance): this G-front is
the strongest non-deep-read choice for the next work-selecting
session — the directorate has not yet sat and no brief exists.

G3. C8 skeleton coherence. ENTRY: after a synthesis pass with
C8-relevant output, or on finding a gap in the skeleton's
pre-registration bookkeeping. FEEDS: the C8 spec's readiness, so the
moment the gate opens nothing is improvised. BOUNDARY: A1–A5 stay
PROPOSED and owner-gated; sessions maintain coherence records only,
and the spec is edited only through the standing amendment-log rules.
STATUS: waiting on the L2 gate; pre-registration bookkeeping only.
NOTE 2026-11-19: C8 is now the SECOND link of the Board's only active
front (C1-L2 → C8 → Convexity Sizing); this G-front's coherence work is
L2-chain critical.

Edition 1, recorded 2026-11-19 (null-time session 60, log entry ## 64).
The status lines above are refreshed by sessions as they advance fronts
and by synthesis passes; rankings and gates live in the protocol,
never here. Board directive block added 2026-11-19 at the owner's
freeze/archive/launch word.