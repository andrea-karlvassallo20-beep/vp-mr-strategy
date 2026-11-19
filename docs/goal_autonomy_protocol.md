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

## 2. The goal state (edition 2, 2026-11-19, installed under the
owner's dated configuration instruction)

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

The ranked open fronts (what goal autonomy optimizes over; per the
owner's dated configuration each front carries entry criteria, what it
feeds, and its own decision gate):

1. The gated L2 window — the critical path, but owner-gated on both the
   environment and the purchase. Autonomy's job here is reminders and
   readiness, not action. Entry: the owner's environment is up and the
   gated data pass the L0 100-timestamp audit. Feeds: C1-L2, C5, C6, C8.
   Gate: owner-only on data and budget; a session never acts here.
2. The library deep-read queue — default work, exactly as the standing
   ritual performs it. Entry: a readable UNREAD head. Feeds: sharpening
   candidates, kill-line hygiene, C1-L2/C8 spec discipline. Gate: each
   note graded by whether a kill line moved; the laundering rules bind;
   nothing enters a spec from a paper.
3. The misses curriculum (the honest 2x2) — the base-rate table the
   C1-L2 spec must confront. Entry: the descriptive protocol is written
   and dated first; cached klines only. Feeds: coverage-miss and
   false-alarm base rates at daily grain. Gate: descriptive only; no
   claim, no direction, no kill line; all cells reported, none selected.
4. The synthesis pass (section 4) — due at the cadence below; this is the
   piece that makes the task list regenerate itself. Entry: five or more
   deep-reads landed since the current goal-state edition. Feeds: the next
   goal-state edition, triage candidates, probe proposals, sharpening
   candidates. Gate: products only through the sanctioned channels;
   measures nothing, arms nothing.
5. Gap-driven probes inside the exploratory channel — the sanctioned home
   for cross-domain imports and new triage candidates. Entry: a named gap
   against the registered specs and the reading lists. Feeds: triaged
   cross-domain imports. Gate: the exploration channel's own limits
   (docs/exploratory_channel.md).
6. The website honesty pass — the rot-remover for the public instrument.
   Entry: the claims ledger current; the prose pages read against it.
   Feeds: public honesty. Gate: only sentences stating moved claim
   statuses are restated; verifications run before the push; no claim
   content changes.
7. The macro-timeline backfill — owner-curated rows, hand-checked per
   row. Entry: a proposed row with its source, put to the owner. Feeds:
   censoring windows for hazard work. Gate: the owner's standing item;
   sessions propose, never auto-append.
8. Instrument upkeep — already nightly and automated (board_refresh.py,
   surprise_ledger.py); never re-done by hand; audit by reference only.

Edition rule: this section (2) is rewritten ONLY by a synthesis pass, as a
dated edition increment (edition n+1 replaces the previous section whole,
with the log entry recording the change), OR by the owner's direct dated
instruction. Nothing else edits it. Edition 1 (the five-item backlog of
the landing session) is preserved in log entry ## 58 and superseded by
this edition 2, installed under the owner's 2026-11-19 configuration
instruction; nothing in the facts block above changed between editions.

## 3. The director policy (how a session chooses)

At session start, after re-reading the live main tail and the branch/PR set (the main-wins race protocol is unchanged):

1. Default: if the standing deep-read ritual has a readable UNREAD head, the session may run it, exactly as codified. Nothing is revoked.
2. Cadence rule: if five or more deep-read sessions have landed since the current goal-state edition, the session runs the synthesis pass FIRST (as its own session, or before its read).
3. Rotation guidance (the owner's dated instruction, 2026-11-19): the
deep-read default is the floor, not the target. Work type rotates
across the fronts — deep-read one session, misses-curriculum numbers the
next, a probe proposal the next, the website honesty pass the next — and
a session may and should take any lawfully executable
non-deep-read front whenever one is ready; the choice and its reason
are recorded in the session-state note against the section 2 backlog.
4. Overrides: a session may run other work instead of the deep-read
ritual — a corrigendum, an instrument or infrastructure repair, an
exploratory probe, a synthesis product — only with a recorded reason
in its session-state note, tying the choice to the written backlog in
section 2.

5. Fail-safe: if this protocol file is unreachable, truncated, or
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

## 6. The weekly directorate (dated owner instruction, 2026-11-19)

One short sitting on the owner's calendar — the objective is roughly ten
minutes — where the current front ranking and the pending-queue shortlist
are presented and the owner batch-ratifies or kills proposals in one
decision sitting. Sessions never schedule, fire, or preempt the
directorate; their job is to keep the goal state and the
DECISIONS_PENDING shortlist ready and current so any sitting can happen
without preparation. The one-sitting batch replaces dozens of per-item
gates; nothing outside it changes status: arming, amendment signatures,
kill-line moves, sharpening approvals and every other carve-out in
section 1 remain owner-only, and the ratification queue's zero-armed
state holds until the owner acts. The standing order itself is recorded
as MADE in docs/DECISIONS_PENDING.md per the owner's instruction.

## 7. Amendment note (2026-11-19, log entry ## 60)

Installed under the owner's same-day configuration instruction (the
four-point message of 2026-11-19, later refinement of the directive that
ratified this protocol): (1) section 2 replaced whole as goal state
EDITION 2 — the ranked fronts now numbered 1-8, each carrying entry
criteria, what it feeds, and its own decision gate; the facts block
verbatim-unchanged from the corrigendum v2; the edition rule amended to
admit the owner's direct dated instruction (this edition's authority);
edition 1 preserved in log entry ## 58. (2) Section 3 gained item 3,
the rotation guidance, with the former items renumbered 4 and 5, text
otherwise unchanged. (3) Section 6 added: the weekly directorate. The
section 5 corrigendum note is untouched from log entry ## 59's repair
and remains the authority on the verbatim-vs-reconstruction boundary of
this file. The integrity guard's encoding-scope gap named in section 5
remains a candidate improvement, zero status, not implemented here.

## 8. Cross-reference amendment (2026-11-19, log entry ## 64)

Two facts, dated this session (null-time session 60). (1)
`docs/GOALS.md` installed as the session-facing status board: the
protocol's section 2 edition 2 remains the ranking authority (numbered
fronts 1–8 with entry criteria, feeds, and gates); GOALS.md carries
per-front STATUS lines, the rotation rule in operational form, and
three additional standing work-fronts (sealed-prediction record
readouts, ratification-readiness briefs, C8 skeleton coherence) —
zero authority over any gate, claimable only per the standing order's
carve-outs. (2) The integrity guard's encoding-scope gap named in
section 5 and held at candidate status by log entry ## 60 is now
closed: implemented as guard check 3 (reject replacement characters,
non-UTF-8 sequences, and non-printable control characters in
docs/*.md and paper/research/*.md, the section 5 scope, with strict
UTF-8 decode), plus planted-offender and clean-tree tests in
tests/test_integrity_guard.py. Sections 1–7 above stand verbatim.
