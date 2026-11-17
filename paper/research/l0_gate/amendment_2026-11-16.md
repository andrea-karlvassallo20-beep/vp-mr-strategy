# L0 snapshot-coverage amendment — recorded 2026-11-16

**Owner decision, recorded verbatim** (critical-path unblock, per the
directive of 2026-11-16):

> "For the initial C1-at-L2 dry run, the L0 gate will be validated using
> the available October 01 (free) and October 10 (verified) snapshots.
> The missing intervening days (Oct 02-09) are declared a known data gap
> for this iteration. No claims will be finalized until the full
> continuous window is acquired."

## What this changes

- The L0 gate verdict for the C1-at-L2 dry run is now **PASS WITH
  DECLARED GAP**: validated on 2026-10-01 (full 100-timestamp audit:
  gap rate 0.00009%, mid 100%, depth 100%) and 2026-10-10 (verified);
  2026-10-02..09 are a KNOWN DATA GAP for this iteration, not silent
  coverage.
- C1-L2 is **unblocked to run its dry run** on this basis.
- **Finalization remains gated**: no claim is finalized (no
  tested-pass/tested-fail entry is closed as evidence for the endpoint)
  until the full continuous window is acquired — either the paid
  `book_snapshot_25` backfill for the gap days or a self-recorded
  forward window that covers them.

## What this does NOT change

- The standing rule that a purchased "clean" feed without raw-diff
  verification is excluded from trust: the amendment declares a gap, it
  does not declare the gap days verified.
- The K-kill lines of C1-L2 (five, armed) and C8 (eleven, armed): every
  result produced inside the declared-gap iteration carries the gap
  flag in its evidence line.
- The one-instrument-first law and the panel gate.

## Ledger effect

The C1-L2 row moves from "blocked on the L0 snapshot-coverage decision"
to "unblocked for the dry run by recorded amendment; finalization
gated on the continuous window."
