# paper/research/ layout

The research tree is organized by phase. Two rules govern what moves and
what stays:

1. **Historical, human-authored records** (dated reports, audits, memos,
   completed pre-registrations and their results, run logs) are filed into
   the phase folder where they were produced.
2. **Live machinery stays at the root.** Files that the nightly
   paper-trading workflow rewrites, that scripts read as inputs, or that
   are ACTIVE pre-registrations (C1-L2, C7-L2 integration, C8, the L2 data
   acquisition spec, the orderflow programme, the null-time programme) do
   not move until their claim resolves. Moving a file a robot rewrites
   every night just creates two copies of the truth.

- `phase1_daily/` — Phase 1 (Daily/AVFI), CLOSED: the daily-OHLCV era.
  The C1 daily hazard experiment (failed, all kill lines), the C7-30m
  pre-registration and its tested-fail result, the watchlist interim, the
  night-before criteria registry, the SMH methodology review, the Tesla-day
  case study, the math verification record, and the audits and memos of
  that era.
- `phase2_l2/` — Phase 2 (Crypto L2), ACTIVE: everything produced by or
  about the L2 data program. The taker falsification run (T3), the
  aggTrades second-window memo, the C8 spec review, the L2 gate samples,
  and the C1-L2 dry-run output. New gate samples are written here directly
  by `src/gate_tardis_sample.py`.
- Root — live outputs (`*_report.md`, `*.json` written nightly), the data
  directories (`data/`, `clue_scan/`, `l0_gate/`), and the active specs and
  programme documents listed above.
