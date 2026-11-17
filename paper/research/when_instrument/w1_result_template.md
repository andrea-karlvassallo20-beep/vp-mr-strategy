# W1 RESULT — [PASS / REFUSED] — pre-written template (v1, 2026-11-17)

Status: TEMPLATE, pre-written before any W1 measurement exists, per the
null-time playbook (`paper/research/roadmap_to_endpoint.md`, §5) and the
C1-L2 pre-written-result precedent. When the trigger layer produces its
lift CPCV distribution, this page becomes the verdict by fill-in. No
number below is real; every `[___]` is a blank. The governing spec is
`w1_when_instrument_spec.md` — this page reports against it and changes
nothing in it.

---

## 1. The question, restated from the frozen spec

Inside a primed macro state, does the trigger signature carry a
conditional hazard lift on the release whose CPCV LOWER bound exceeds
1.0 net of round-trip cost (K1), with positive net-of-cost expected
value at that lower bound (K2)?

## 2. The measurement (fill in when it exists)

- Trigger source and spec (C8, or the surviving lead if C8 died): `[___]`
- Data window and gate status (L0 verdicts): `[___]`
- Horizon H (pre-declared by the trigger spec): `[___]` hours
- Baseline hazard P(release ≤ H | primed): `[___]` (n = `[___]`)
- Lift point estimate: `[___]`
- Lift CPCV distribution (at least: P10, median, P90): `[___]`
- **Lift LOWER bound (P10): `[___]`** — the only number K1 reads
- Payoff R-distribution (mean, worst decile): `[___]`
- Round-trip cost at the prevailing book (fee + half-spread): `[___]` R
- Engine decision (`strategy/when_instrument.py` output JSON): paste
  verbatim, including any refusal strings — `[___]`

## 3. The kill lines, verdict by verdict

- **K1 (refusal):** lower bound `[___]` vs 1.0 → ARMED/FIRED — `[___]`
- **K2 (net-of-cost):** EV at lower bound `[___]` R vs 0 → `[___]`
- **K3 (calibration):** first 10 scored forward rows, count outside the
  90% band: `[___]` (dies at ≥ 2; verdict deferred until scored)
- **K4 (direction leakage):** correlation of engine inputs/sized
  outcomes with UP beyond [0.497, 0.513]: `[___]`
- **K5 (placebos):** era-shuffle lift `[___]`, 24h-shift lift `[___]`
  (a lift under placebo kills the MEASUREMENT, and this page says so)

## 4. The outcome, in the roadmap's two-victory grammar

- If K1/K2 pass and K3–K5 stay clean: the instrument SIZES. First
  forward-log rows opened: `[___]`. Paper log only; nothing trades live.
- If any line fires: the death is recorded here with the tabulated
  honesty of the compression family's four documented deaths — the
  dead mechanism NAMED (which input failed, at which bound), the
  page published, the family closed. A killed W1 is a completed
  ledger page, which the roadmap defines as a victory.

## 5. Disclosures that travel with the result, pre-committed

- The C7 occurrence numbers travel with their standing disclosure:
  +7.9 points over matched controls, measured once, sealed dataset,
  no second run.
- No Sharpe will be reported without a CPCV distribution and the
  Deflated Sharpe correction.
- No parameter was tuned after seeing any W1 number; any deviation
  from the frozen spec is an appended, dated, marked amendment.
