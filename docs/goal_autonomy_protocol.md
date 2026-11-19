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
2. Cadence rule: if five or more deep-read sessions have landed since the current goal-state edition, the session runs the synthesis pass FIRST session, before any deep-read that sitting.)

<!-- REPAIR NOTE 2026-11-19: the text from this point down is a
     reconstruction, not the original landing. The landing commit
     17c4035 truncated this file: the original cut off mid-sentence
     (section 3, item 2, stopped at "(as its own ") and was followed by
     roughly 712 bytes of binary mojibake; the rest of section 3 and
     section 4 were lost. The reconstruction is built strictly from the
     installing session's own record of this protocol's design (log
     entry ## 58 in paper/research/null_time_programme.md) and the
     repair is logged as a corrigendum (log entry ## 59). The owner's
     ratification (chat directive, 2026-11-19) is unaffected and
     unabridged. Intact original text above this marker is preserved
     verbatim. -->

3. Overrides: a session departs from the default mode (the deep-read
   ritual) or the cadence rule only with a reason recorded in its
   session-state note, tied to the written backlog above.
4. Fail-safe: if this protocol file is unreachable, unreadable, or
   internally inconsistent, the session falls back to the fixed
   deep-read ritual and logs the defect. Nothing in this file licenses
   any departure from the hard gates: every hard gate in the log binds
   every mode.

## 4. The synthesis pass

The synthesis pass names gaps: it reviews the programme's recorded
state against the registered specs and the reading lists, and states
what evidence the programme still lacks, which catalogued papers carry
it, which sharpenings the reading has earned, and what the next
edition of the goal state (section 2) must say. It measures nothing,
arms nothing, and launders nothing INTO any spec. Its products move
ONLY through the sanctioned channels:

- new catalogued-paper triage candidates for the deep-read queue;
- sharpening candidates to the ratification queue
  (docs/DECISIONS_PENDING.md), PENDING OWNER RATIFICATION as always;
- probe proposals inside the exploratory channel
  (docs/exploratory_channel.md);
- the next dated edition of the goal state (section 2), per the
  edition rule above.

A synthesis pass is logged like any other session: which gaps it
named, where each proposal landed, and the queue count after it.
