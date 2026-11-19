# The goal-autonomy conductor protocol (ratified 2026-11-19)

**Status: ACTIVE, ratified by the owner's word in chat on 2026-11-19.** The
owner's directive: null-time sessions must not merely repeat the standing
deep-read task; they must advance and redirect the programme toward the
terminal goal — the Salient Market Hypothesis — by choosing objectives that
they themselves rank from the programme's own recorded state. The owner may
revoke or amend this protocol at any time; its installation is logged in
`paper/research/null_time_programme.md` (the landing session's entry, same
push as this file). This document follows
the precedent of `docs/exploratory_channel.md` (ratified 2026-11-18): a
declared channel for a standing mode of work, with its limits written down.

## 1. What autonomy is granted, and what it is not

Granted: selection and invention of the next unit of null-time work. Which
paper is read, when a synthesis pass runs, what probe is proposed, what gap
is named — these become session decisions, made against a written goal
state, recorded with reasons, and contestable in the log.

NOT granted, unchanged, owner-only (the carve-outs):

- Arming any claim, test, or spec; the armed list stays owner-fired.
- Signing, amending, or withdrawing any dated amendment.
- Spending data, budget, or sealed windows (the L2 purchase, the
  cross-market holdouts, the watchlist windows).
- Moving any kill line, frozen constant, or frozen default.
- Approving sharpening candidates: they queue as PENDING OWNER
  RATIFICATION, exactly as before.

Any product of autonomy that falls in these classes routes to
`docs/DECISIONS_PENDING.md` (if a sharpening) or to the log (everything
else) and is inert until the owner acts.

## 2. The goal state (edition 1, 2026-11-19)

Terminal goal: the SMH as defined in `KNOWLEDGE_SMH.md` (charter v3). This
protocol never restates, reinterprets, or rewrites the charter; it points at
it.

Where the theory stands (facts recomputed from the live record on
2026-11-19):

- Phase 1 (Daily/AVFI): CLOSED. Three independent deaths of the
  OHLCV-compression family.
- Phase 2 (Crypto L2): ACTIVE, blocked on the owner's data acquisition
  (`paper/research/l2_data_acquisition_spec.md`); the L0 dry run is
  unblocked; the gate-day machinery is ready.
- Standing sealed instruments: the nightly board/surprise ledger
  (`logs/board_surprise_ledger.jsonl`, hash-chained); the watchlist forward
  test open until 2027-01-11; the second-generation rule frozen until a
  2027 forward window.
- Library: 50 deep-read notes through deep-read session 49; the
  ratification queue holds TWENTY-NINE candidate sharpenings plus probe E1,
  zero armed; T1 is armed awaiting the owner's word in its booked state
  (sign inverted); T2 tested-fail; the blocked list stats blocked.
- Deep-read queue pointer: next UNREAD is "From Glosten-Milgrom to the whole
  limit order book and applications to financial regulation" (score 29,
  x0d8b2a), then "A Hawkes Microfoundation for Multitype Inverse Gaussian
  Subordinators" (score 29, xf77014).

The ranked backlog (what goal autonomy optimizes over):

1. The gated L2 window — the critical path, but owner-gated on both the
   environment and the purchase. Autonomy's job here is reminders and
   readiness, not action.
2. The library deep-read queue — default work, exactly as the standing
   ritual performs it.
3. The synthesis pass (section 4) — due at the cadence below; this is the
   piece that makes the task list regenerate itself.
4. Gap-driven probes inside the exploratory channel — the sanctioned home
   for cross-domain imports and new triage candidates.
5. Instrument upkeep — already nightly and automated; never re-done by
   hand.

Edition rule: this section (2) is rewritten ONLY by a synthesis pass, as a
dated edition increment (edition n+1 replaces the previous section whole,
with the log entry recording the change). Nothing else edits it.

## 3. The director policy (how a session chooses)

At session start, after re-reading the live main tail and the branch/PR set (the main-wins race protocol is unchanged):

1. Default: if the standing deep-read ritual has a readable UNREAD head, the session may run it, exactly as codified. Nothing is revoked.
2. Cadence rule: if five or more deep-read sessions have landed since the current goal-state edition, the session runs the synthesis pass FIRST (as its own session, or before its read).

3. Overrides: a session may run other work instead of the deep-read
ritual — a corrigendum, an instrument or infrastructure repair, an
exploratory probe, a synthesis product — only with a recorded reason
in its session-state note, tying the choice to the written backlog in
section 2.

4. Fail-safe: if this protocol file is unreachable, truncated, or
internally inconsistent, the session falls back to the fixed deep-read
ritual and logs the fallback with the reason. The ritual is never
blocked by this protocol's condition.

## 4. The synthesis pass

The synthesis pass re-reads the live record and names gaps: against
the registered specs and the reading lists, it asks what the record
now lacks and what the next unit of work should be. Its products
travel ONLY through the sanctioned channels:

- Catalogued-paper triage candidates for the library queue.
- Sharpening candidates to the pending ratification queue, exactly as
  deep-read notes queue them (PENDING OWNER RATIFICATION, never
  self-armed).
- Probe proposals for the exploratory channel, at zero status until
  the owner fires them.
- The next dated edition of the goal state (section 2), which only
  this pass may rewrite.

The synthesis pass measures nothing, arms nothing, and launders
nothing INTO any spec.

## 5. Corrigendum note (2026-11-19, log entry ## 59)

This file landed corrupted in PR #224 (log entry ## 58): from the
middle of section 3, item 2, the byte stream degenerated into
encoding garbage and the file ended mid-garbage, with the remainder of
section 3, section 4, and the fail-safe text lost or unreadable on
main. Log entry ## 58 itself landed clean and records the protocol's
intent in its own words; this corrigendum is reconstructed from that
record. What is verbatim below the cut line: nothing. What is
verbatim above it: sections 1 and 2 and section 3's items 1 and 2
through the phrase "(as its own session, or before its read". The
terminal period of item 2, items 3 and 4, section 4, and
this section are reconstructions, faithful to the
landing entry's recorded summary, not restorations of lost wording; the
original wording cannot be recovered and is not guessed at beyond the
recorded phrases. The integrity guard passed the corrupted file
because it sweeps conflict markers and library provenance labels,
not byte-level encoding sanity; a proposed guard extension (reject
replacement characters and non-printable garbage in docs/*.md) is
recorded in log entry ## 59 as a named gap for the next infrastructure
session, not implemented by this corrigendum. The goal state
(section 2, edition 1) was untouched by the corruption and stands.
