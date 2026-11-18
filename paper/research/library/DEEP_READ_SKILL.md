# Null-time article-research skill — the library deep-read ritual

This is the working protocol for every null-time deep-read session,
written down so that any successor runs the ritual identically. It is
the codification of the method used for deep-read sessions 1-20
(logged as programme sessions 7-26). Read it together with
`docs/DECISIONS_PENDING.md` (the ratification queue), the house rules
in `docs/` (nothing measured during null time, no kill-line changes,
nothing trades live), and the triage audit recorded in the session-9
note (`2026-11-16_bivariate_hawkes_kernels_deep_read.md`): ranks are
candidates, not promises.

## The one question

Every paper is read against ONE question, stated verbatim in the
note's read-line:

> **What here would kill C1-L2 or C8 faster, or change their kill
> lines?**

Anything in the paper that does not bear on that question is context,
not content. Execution-strategy engineering, portfolio layers, venue
architecture, and "impressive empirical results" claims are recorded
(if at all) as standing caveats or cost-survival ammunition — never
as program input. **A library is ammunition, not evidence.**

## Legal source acquisition

- Text comes only from the legal OA shelf:
  `docs/library/text/<slug>.txt` — page-marked extracts produced under
  the acquisition protocol (`docs/library/acquisition_log.json`).
- Metadata (title, authors, year, venue) comes from
  `docs/library/expanded_index.json` via the slug. Never invent or
  guess bibliographic fields; if the extract is absent or unreadable,
  skip the entry and say so in the log.
- Cite by PDF page ("PDF p. N") whenever the note makes a claim the
  source supports — every finding in a note is traceable to a page or
  it does not go in the note.

## Selection: the triage queue

1. Load `docs/library/edge_triage_scores.json` and sort by score
   descending.
2. The next read is the next UNREAD entry in that order. Unread =
   no deep-read note exists for its slug in
   `paper/research/library/`.
3. Respect the session-9 triage-audit flag: scores rank access
   value, they do not promise relevance. If a top-ranked entry is a
   student term-report or otherwise low-grade relative to its score,
   read it, grade it plainly, and record a `[source-quality note]`
   — do not silently skip it and do not promote it beyond what it is.

## The note (one file per paper)

Filename:
`paper/research/library/YYYY-MM-DD_<short_name>_deep_read.md`, where
the date is the date of the reading session (all sessions on this
branch used 2026-11-16; keep the convention of one date per session
and never let one note carry a different date from its log entry).

Structure, in order:

1. **Title header** — session number, authors, full title, venue/
   arXiv id, one clause on what the paper is.
2. **Read-line** — "Read YYYY-MM-DD, against ONE question: **what
   here would kill C1-L2 or C8 faster, or change their kill lines?**
   Source: legally acquired OA copy (`docs/library/text/<slug>.txt`,
   ~N pp., page-marked). Next UNREAD triage-rank entry (score S)."
3. **"The paper in one paragraph"** — the honest compressed summary,
   page-cited.
4. **"Findings, graded (does any kill line move?)"** — opens with the
   verdict in bold: either "NO kill line changes. NO new candidate
   sharpening." or "NO kill line changed; ONE (or N) new candidate
   sharpening(s) queued, PENDING OWNER RATIFICATION." Each numbered
   finding carries exactly one tag (below), cites PDF pages, and
   states what it does or does not license.
5. **"What this paper would have killed if we had done it wrong"** —
   the counterfactual: which artifact the program avoided by having
   its existing discipline. This section is the program's immune
   system and is never omitted.
6. **"Standing caveat"** — the paper's own limitations and
   applicability boundaries, plainly stated; arXiv-version cautions
   ("check published version before formal citation") when relevant.

### Tag taxonomy (exactly one per finding)

- `[reinforcing, no new item]` — supports an existing rule, warrant,
  or caution; nothing added to any queue.
- `[candidate sharpening, PENDING OWNER RATIFICATION]` — a proposed
  amendment. Only harder-to-pass amendments are legal; the note must
  say which existing rule it tightens and how it makes a future test
  harder to pass. The owner ratifies; nobody else arms anything.
- `[interpretation caution]` — a reading discipline (how a future
  feature or estimate may be interpreted), no queue change.
- `[cost-survival ammunition]` — relevance only if a future K7-style
  cost-survival layer exists; declares assumptions that layer must
  carry.
- `[source-quality note]` — bibliographic or grade concerns about
  the paper itself.

### Grade rules

- Default grade: NO kill line changes, NO sharpening. A candidate
  sharpening is rare and must be earned in the text with a specific
  mechanism, not a mood.
- Kill lines are never changed by deep-reads, ever.
- Nothing measured during null time: no experiments, no fits, no
  data runs accompany a deep-read.
- Corrigenda: if a past note or log entry is wrong, append the
  correction as a new log entry and leave the wrong text unedited
  (honest-error protocol; see log session 18). Filename slips and
  typos may be fixed in place with a commit message that says
  exactly what moved.

## The programme log (append-only)

Each session appends one entry to the end of
`paper/research/null_time_programme.md`:

- Header `## N.` with the null-time session number (deep-read session
  n is logged under its null-time session number; the two series run
  offset — keep the mapping stated once, then honor it).
- The paper, the grade, findings with page cites, cautions.
- Closing block, always: inaccessible/blocked status if any;
  ratification-queue count ("Ratification queue after this session:
  N candidate sharpenings, zero armed"); T1 status ("T1 remains armed
  awaiting the owner's word; the blocked list stays blocked"); and
  the next-queue pointer naming the next unread paper by title and
  score.

## The ratification queue (`docs/DECISIONS_PENDING.md`)

- Only when a candidate sharpening is queued: update the
  ratification-queue line with the new count and a parenthetical
  naming every queued item ("twelve candidates (per-branch rule,
  flow-clock scale-constant, sign-register, estimator-mode,
  dispersion register), zero armed").
- If nothing sharpened, the file is not touched.

## Verification loop (every session)

1. `python3 src/integrity_guard.py` — must run clean before commit.
2. Commit with the house style: one long narrative commit message
   that states the session, the verdict, the findings, the queue
   count, the next pointer, "Guard clean. Nothing measured, no kill
   line moved, nothing armed, nothing trades live."
3. Push to the working branch.
4. Verify CI with
   `gh run list --branch <branch> --limit 2`
   (`gh pr checks` can show stale runs; a "cancelled" run under
   `concurrency: cancel-in-progress` is supersession, not failure).
5. Report to the user: the paper, the grade, the findings in one
   or two lines each, the queue count, the next pointer.

## Hard invariants (restated, non-negotiable)

- Nothing measured during null time.
- No kill-line changes; only harder-to-pass amendments may be
  queued, and only as PENDING OWNER RATIFICATION.
- Nothing trades live — execution-strategy content in a paper is
  never operationalized.
- The blocked list stays blocked; T1's arming belongs to the owner.
- The library is ammunition, not evidence: no empirical claim from
  any paper enters the record as support for any program claim.
