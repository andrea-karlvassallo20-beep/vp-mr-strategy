# Independent review: T1 second-window result (PR #138)

**Reviewer:** the null-time session. **Date:** 2026-11-16.
**Reviewed artifact:** `paper/research/t1_second_window_report.md`,
`taker_falsification_t1.json`, `src/run_taker_falsification.py`,
`src/c1_l2_test.py::enforce_kill_lines` — all as committed on branch
`vibe/t1-misses-cks-56e234` (PR #138).

**Verdict up front: the run is honest and the numbers check out. Merge the PR
as a record. But the ledger booking matters more than the verdict, and the
booking must not say the compression story advanced.**

---

## 1. What was verified

- The five kill lines as pre-declared (in `enforce_kill_lines` and the
  contract text) contain **no direction requirement anywhere**. Lines (b)
  and (d) test only *exclusion of 1.0* from the HR confidence interval;
  line (a) tests concordance magnitude; lines (c)/(e) test null behavior.
  "Survives all five" is therefore true **to the letter** of the
  pre-registration.
- The numbers in the PR body match the committed JSON exactly (OOF C
  0.6590; stratified HR 0.738 [0.702, 0.776]; vol-tautology HR 0.590
  [0.566, 0.615]; compression-only 0.516 [0.496, 0.538]; 0/6 unrejected
  powered folds; observed gap 0.1328 vs null band [0.1354, 0.2018]).
- The 96 startup-spell exclusion is a printed data-startup exclusion, not
  a tuning choice; acceptable.
- The harness ran unchanged from the first window; no per-window
  adaptation detected.

## 2. The central finding: the registered mechanism is refuted, not supported

The registered MECHANISM text is directional: *"compression aging **raises**
the conditional hazard of a trade-touch excursion."* Every measured HR is
**below 1.0** — including the sigma-conditioned one (0.590). The data say
the opposite of the registered story: deeper taker-measured compression is
associated with **lower** within-spell hazard.

So the honest booking is three-part, and all three parts must appear
together:

1. **tested-pass as registered** — the kill lines, as written before the
   data, did not fire. The record is clean.
2. **mechanism direction REFUTED** — the coil-exit story ("the longer the
   compression, the closer the move") is contradicted at the spell scale
   on taker data. T1 may NOT be cited as support for the WHEN story.
3. **what actually survives is an inverted information claim**: taker
   compression carries real, vol-robust information about the hazard —
   pointing the *other way*. That is a fact worth having, and it is
   exactly the question C1-L2/C5 were designed to resolve on the passive
   side.

## 3. The pre-registration gap, named (prospective fix only)

The kill lines tested **magnitude, not sign**. This is a spec defect in
the pre-registration template, not a fault of the run. The fix is
prospective and must never be applied retroactively (moving a kill line
after seeing the data is the one forbidden move):

> **Proposed rule (template-level):** any claim whose registered mechanism
> states a direction must carry a sign kill line — the pre-registered
> coefficient's CI must lie entirely on the pre-registered side of the
> null. A result on the wrong side of the null is booked
> "mechanism-refuted (sign)" even if every magnitude line passes.

If the owner accepts this rule, it should be added to the pre-registration
template and to the C1-L2 spec (PR #140's sharpening pass is the natural
vehicle — its author's call).

## 4. Fragility flag: the scale-invariance margin

The observed gap (0.1328) sits **below** the null band's lower edge
(0.1354) by 0.0027 — the pass rests on a margin thinner than typical
bootstrap-seed noise. This is NOT grounds for a re-run (re-running until
a line flips is tuning, and the line passed), but it must be recorded as
fragile: a same-spec replication on new data should be expected to be able
to land either side of this line.

## 5. The three unresolved readings — my ranking

The run records three readings of the inversion; I rank them:

1. **The taker-only constraint (strongest).** CKS's own words, already in
   the repo's deep-read: the impact information lives in quote events.
   The passive-withdrawal mechanism — the actual SMH story — is
   *invisible by construction* in aggTrades. The inversion may be an
   artifact of watching only half the flow. This is precisely what
   C1-L2/C5 resolve, and it is the correct reason the L2 phase proceeds.
2. **Barrier geometry.** A noise-floored trade-touch barrier on a
   compressed (quiet) book is mechanically harder to touch — the
   excursion threshold scales with the same quietness that defines the
   state. The vol-tautology line conditioned on sigma_H, but the
   *barrier* itself remains vol-coupled. Worth one paragraph in the C1-L2
   spec: barrier thresholds must be state-independent, not quietness-scaled.
3. **Scale mismatch (weakest).** Daily vs 15-min clock is a real
   difference but is the least specific of the three.

## 6. The misses 2x2 (Task 2) — sound

Coverage 0.039 with lift 2.07 is the honest pair of numbers: priming
doubles the conditional move probability while missing 96% of moves. The
protocol was pre-declared, parity-pinned, and descriptive-only. No
objection. This belongs on the website's misses section as-is.

## 7. Recommendation to the owner

- **Merge PR #138** — the run is faithful and the record is valuable.
- **Book T1 in the ledger** as: *"tested-pass as registered; mechanism
  direction refuted (sign inverted); not usable for the WHEN story until
  the sign is resolved on L2 passive data."*
- **Accept or reject the sign-kill-line rule** (§3) before any further
  claim is armed — it costs nothing now and prevents this ambiguity from
  recurring on C1-L2, where direction is the whole point.
- Note the fragility flag (§4) in the ledger row.

**What this review cannot tell you:** whether the inversion survives on
full L2 data — that is C1-L2's job, gated on the L0 verification gate.
