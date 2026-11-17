# SMH Methodology Review v2 — the week that changed the map

Written in null time, 2026-11-16, while the owner sets up the L2
environment and studies medicine. This is the successor to the
2026-11-15 review (`smh_methodology_review_2026-11-15.md`): that review
drew the map; this one redraws it after the week's results and asks what
null time should produce next. Nothing here tests a claim. It is the
programme thinking about itself.

---

## 1. What the week changed

The 11-15 review ended with an unblocked queue. The week executed most
of it, and the results move the map:

1. **T3 died** (arrival density is vol-mediated; wall-clock exposure
   invariance refused). W3 of the last review — two clocks, one
   hypothesis — got its answer: the event clock does NOT emancipate
   taker-arrival features from wall-clock quietness. The event-clock
   questions that remain (compression FROM the book) must be asked on
   book data, not taker prints.
2. **C7-30m died** and the owner confirmed the OHLCV verdict: ALL
   OHLCV-derived edges for forward returns are dead, three independent
   deaths of the compression family. The programme now rests entirely
   on the L2 data — the executive summary's one sentence: the coil is
   not in the candles; if the WHEN clock exists, it lives in the book.
3. **The public math was verified against its sources** (arXiv LaTeX
   for OFI; the `tick` library for Hawkes) — and the verification found
   FIVE defects in our own estimators (D1–D5). The worst: the Hawkes
   branching ratio was overstated by the factor β, meaning the C8
   trigger threshold of 0.8 would have fired on ordinary markets. The
   threshold was frozen only after the fix.
4. **C8 was pre-registered** (`c8_macro_l2_synthesis_spec.md`) with
   eleven armed kill lines, the falsifiable core requiring BOTH
   statistical interaction AND joint superiority over each layer alone.

## 2. New honest weaknesses (the v2 list)

**W6 — Estimator risk is no longer hypothetical; it is demonstrated.**
D1–D5 prove that "the spec is right" and "the code computes the spec"
are different claims, and the second had never been checked. The
programme's kill lines guard against bad inference from good data; D5
was bad inference from good data caused by an unverified estimator.
*Improvement (adopted, recorded in the ledger's epistemic contract):*
no threshold is frozen before the estimator that will measure it is
verified against its source or an independent oracle. The template
exists: `src/verify_math_library.py` + `tests/test_math_exactness.py`.
Every future estimator (the C1-L2 Cox harness, the C8 hazard model)
gets the same treatment BEFORE its kill lines are armed, not after.

**W7 — The ledger was missing its only pass.** The public claims ledger
displayed every death in detail and had NO row for C7-daily — the
programme's single tested-pass claim (+7.9 points of occurrence over
matched controls, sealed). Honesty that displays failures but not
passes is not honesty; it is inverted marketing. *Fixed in this PR:*
the C7 row now leads Layer 1, with its scope sentence travelling with
it (occurrence on daily bars, not timing, not rank, not direction —
and the 86% baseline disclosure: an 86%-likely event cannot be held,
only timed).

**W8 — The critical path is a purchase decision, not analysis.** C1-L2
is blocked on the L0 snapshot-coverage decision (paid
`book_snapshot_25` for 2026-10-02..04, or a recorded spec amendment).
C1-L2 gates C8 (K11: no synthesis on a dead base), and C8 gates the
convexity sizing layer. Nothing in the null-time queue can unblock
this; it is the owner's call, and the memo is written. *Improvement:*
make it the explicit next owner action, in one sentence, in the
executive summary — the programme's scarcest resource is now a
decision, not data.

**W9 — Teaching-page drift risk.** The site now teaches 14 pages while
the discovery panel is sealed. The risk is subtle: a compelling
teaching narrative can quietly become a hypothesis and get "tested" on
sealed data. *Improvement:* the standing rule is that pages DESCRIBE
what happened; any idea born on a page goes to the pre-registration
queue (spec + kill lines first), never to the test queue. So far the
rule holds — C8 was registered before its page existed — but it is now
written down.

**W10 — The C7-daily record needs its reconciliation sentence
everywhere.** 0.940-vs-0.862 (sealed, daily, occurrence) and "all
OHLCV-derived edges are dead" (the verdict) are CONSISTENT — occurrence
is not forward-return rank — but a reader who meets one without the
other meets a contradiction. *Improvement:* every future citation of
0.940 travels with both sentences. The new ledger row does; the
convexity framework's 86% disclosure is extended to carry the OHLCV
verdict alongside it (owner may amend `convexity_economics.md` §5 by
one sentence; not done here to keep that document's sealed status
untouched by null-time edits — flagged instead).

## 3. What null time should produce next (the unblocked queue, v2)

1. **Done in this PR:** the math-verification teaching page (the site's
   13th nav entry, added to all nav-bearing pages); the C7-daily ledger
   row (W7); the verification clause in the epistemic contract (W6);
   the library manifest upgraded from "extracted" to "source-verified".
2. **The data-shape contract: ALREADY BUILT — verified, not re-written.**
   Checked rather than assumed: `l2_data_acquisition_spec.md` defines
   the feed contract (schemas, sequence numbers, coverage), and the
   machine validators exist and have already run on samples
   (`src/tardis_ingest.py`, `src/verify_l2_gate.py`, `src/reconcile_l2.py`;
   gate reports for 2026-10-01..04 in `paper/research/l0_gate/`).
   Null time should NOT duplicate this. What is actually missing is
   the one thing null time cannot supply: the owner's snapshot-coverage
   decision (W8). The hour the data arrives, validation is already one
   command.
3. **NOT recommended: pre-building the C8/C1-L2 model code.** The repo
   pattern is spec-first, harness-after-gate; model code written
   against imagined data shapes gets rewritten anyway and risks
   implying a test ran. The harness gets built when the data passes L0,
   by the same person who can see the real frames.
4. **Reading queue (owner-dependent).** The Bouchaud full copy is still
   a partial upload; the Hawkes/queue chapters are taught on the site
   from what exists. When the full copy arrives, resume at Ch. 2 §2.1.4
   (the KNOWLEDGE.md bookmark).
5. **The watchlist window: discipline only.** Ends 2027-01-11; interim
   readings recorded; no early close, no narrative update between
   readings.
6. **T1/T2 remain the owner's calls.** Memos written; the programme
   does not run pending-decision claims autonomously, even in null
   time — ESPECIALLY in null time, when no one is watching.

## 4. Where this project should move (the direction question)

The endpoint is unchanged and now sharper for the week's deaths: **a
WHEN instrument on the order book, sized by the posterior on MOVE.**
The order of battle is fixed and each step's failure mode is named:
gate decision (W8) → C1-L2 (does the compression clock exist at book
resolution?) → C8 (do the macro and book layers multiply?) → convexity
sizing (information → position, quarter-Kelly on the lower bound) →
Layer 4 shadow. Any pass routes to the next step; any kill line fires
and the claim dies with its mechanism named.

The doctrine null time taught this week, worth keeping as a standing
sentence: **the binding constraint is trust per hour of data.** Paid
L2 data is scarce and one-shot; every hour of it must be spent on a
pre-registered question with verified math and armed kill lines. So
null time is not "waiting" — it is the only time when the trust can
be manufactured: verification, pre-registration, teaching, and the
ledger. The week's five dead defects are what that doctrine is worth:
five ways the first expensive hour would have been spent measuring a
bug.

## 5. The one-sentence version

The candles are dead, the math is verified, C8 is registered with its
kill lines armed — and the next move that matters is the owner's
one-sentence decision on the L0 snapshot coverage, after which null
time's job is to keep manufacturing trust: verify the next estimator,
register the next claim, teach the last result, and refuse to touch
anything sealed.
