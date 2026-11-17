# L2 drop-in runbook — Tardis data to C1-L2 verdict, commands only

For the owner with the Tardis L2 environment ready. Every step is a
command plus what its output MEANS. No decisions are needed at any step;
the specs were frozen before the data existed (the programme's rule).
If any step fails, STOP and record the failure — do not tune anything;
a failed gate is a finding, not an obstacle.

## 0. Preconditions (already verified 2026-11-16)

- C1-L2 harness compiles: `make harness-check` — prints the compile
  check and refuses to report mock-data runs as results.
- Kill lines 1-7 are in the spec and pre-declared:
  `paper/research/c1_l2_test_spec.md` (6 = sign guard, 7 = CKS literal
  tautology control).
- Kill line 7(b)'s unit test exists and passes:
  `python3 -m pytest tests/test_ck_average_depth.py` — the CKS
  average-depth denominator (2(N-1), both sides summed) hand-checked
  against a 3-event interval, with the wrong implementations (2N,
  one-side, last-snapshot) each explicitly caught. An implementation
  failing this test cannot run on Tardis data.

## 1. Pull the data (paid days need the key)

```bash
make pull DAY=YYYY-MM-DD            # needs TARDIS_API_KEY
# or the free first-of-month day, no key:
make pull-free DAY=YYYY-MM-DD
```

Files land in `data/raw/` (git-ignored by policy — never committed).

## 2. Run the Layer-0 verification gate (per day, BEFORE anything else)

```bash
make gate DAY=YYYY-MM-DD
```

Means: mid-price reconstruction and depth are checked against the
independent `book_snapshot_25` file. 2026-10-01 PASSED (gap rate 0.00009%,
mid 100%, depth 100%); partial days 10-02..10-04 passed the sequence
criterion only. A day that fails the gate is NOT usable for C1-L2 —
record it and use a gated day.

## 3. Convert to parquet with verified row counts

```bash
make convert DAY=YYYY-MM-DD
```

## 4. Intake audit (timestamp units, schema, normalization)

```bash
python3 src/intake_audit.py   # asserts microsecond timestamps, schema
```

The audit RAISES on violation. The silent-degradation lesson (lxml:
universe 1,326 -> 823 with no error) is why this step is mandatory and
loud.

## 5. Reconcile L2 (book states vs BBBA, per the harness's own clock)

```bash
python3 src/reconcile_l2.py
```

## 6. The C1-L2 run (the only legal run is on gated data)

```bash
make harness-check    # compile + mock-data validation (already passing)
```

HONEST STATUS (2026-11-16): the production run entry point does not
exist yet. `src/c1_l2_test.py` compiles and validates the full battery
on mock data (book states, BBBA mid, compression flags, triple-barrier
labels, purged splits, stratified fit, kill-line enforcement) and
refuses to report mock runs as results. The production entry point is
the remaining build item and must be written against the GATED data's
actual shape, binding the harness UNCHANGED — no re-tuning, no post-hoc
reinterpretation. When it is built, its command lands here and in the
spec. The summary json must be ADDITIVE across runs (the T3-then-T1
overwrite incident: check the json carries every prior record).

## 7. Read the verdict against kill lines 1-7

All seven must pass for the bounded conclusion (a WHEN clock from the
book, no direction claimed — the 0.505 boundary stands). Any failure:
name the dead mechanism, do not pivot, record it in the claims ledger.
Kill line 6 specifically: if the compression HR is < 1.0 with CI
excluding 1.0, the covariate is informative but the mechanism AS
STATED is dead — record the inversion; that is the passive-side
question C1-L2/C5 exist to resolve, and the sign must be resolved
there, not reinterpreted here.

## Standing constraints (the whole programme's rules)

- Spec frozen before data; amendments only in the harder-to-pass
  direction; the owner's word is the only trigger for arming claims.
- Raw data never enters git; only code, specs, and results records.
- Descriptive numbers are never promoted to claims without
  pre-declared kill lines.
- The equity programme (equity_alpha_lab) is data-blocked pending a
  source decision; it shares the discipline, not the claims.
