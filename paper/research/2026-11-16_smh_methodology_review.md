# SMH methodology review — null-time session 5 (2026-11-16)

Owner context: primary studies are medicine; this session is null-time
work while the L2 environment is set up. Nothing here is armed, measured,
or data-dependent. The session's code output (the honest-inference layer)
is DESCRIPTIVE infrastructure for the equity programme; this note is the
thinking output about the SMH programme's own method.

## 1. What the programme has proved about its method (not about markets)

The most defensible asset this repo owns is not a signal — it is a
falsification record. Four lessons the method has taught about itself,
each already paid for:

1. **Kill lines tested magnitude, not sign.** T1 survived all five lines
   with every HR below 1.0 — the battery detected absence of information,
   not violation of the registered direction. The sign-kill-line rule
   (prospective only, never retroactive) is already proposed; this review
   says: ratify it as a standing rule, not a one-off fix.
2. **Amendment discipline works.** "Harder to pass is the only legal
   direction" prevented post-hoc reinterpretation of T1's inversion. Keep
   it; write it into every future spec's header.
3. **Infrastructure fails silently.** The lxml incident (universe silently
   degraded 1,326 → 823 names) and the summary-json overwrite (T1's run
   clobbered T3's record) are the same lesson: any dependency failure or
   shared mutable output must fail LOUDLY. The equity pipeline's
   validators (schema.py raising on every violation, dropped rows counted
   never filled) are the institutionalized version of this lesson.
4. **Descriptive-vs-claim firewall holds.** No descriptive number in this
   repo has ever been promoted to a claim without pre-declared kill lines.
   This is the rule that makes the repo's negative results trustworthy.

## 2. Proposed sharpenings (candidates, zero armed)

The ratification queue convention applies: the owner's word is the only
trigger. Numbered to continue the queue's style.

- **S-r1 (kill-line coverage matrix).** For every registered claim, the
  spec must carry a small table: failure mode → which kill line catches
  it. T1's gap (sign inversion with informative covariate) was a hole in
  exactly this matrix. A claim whose matrix has an empty row (a failure
  mode nothing catches) is not yet armable. This generalizes the sign
  rule: the sign hole was one instance of an incomplete matrix.
- **S-r2 (two-window rule as default).** No claim is "executed" until it
  runs on a second disjoint window, pre-declared at registration, not
  granted afterward as a bonus. T1's second window was authorized
  ad hoc; make disjointness the default so second windows cannot be
  quietly skipped for claims that looked marginal in window one.
- **S-r3 (placebo reference pre-declared).** Before any test runs, the
  spec states the null's shape (shuffled arrivals, scale-invariance null,
  constant-hazard) so "survives" always has a reference distribution, not
  just a threshold. Already done ad hoc (K1's shuffled-arrival placebo,
  T1's scale-invariance null); make it a required spec section.
- **S-r4 (coverage AND lift, both reported).** The misses curriculum's
  honest 2x2 (coverage 0.039, lift 2.07) shows these answer different
  questions: coverage is what an actuarial-inevitability endpoint needs;
  lift is what a WHEN instrument needs. Any future priming-style
  instrument must pre-declare WHICH one the endpoint consumes and report
  both. A signal chosen for its lift cannot be quietly re-sold on
  coverage.
- **S-r5 (programme-level multiplicity ledger).** K3's count exists
  inside C8; generalize to a single ledger counting every hypothesis ever
  tested across the programme. The honest question "does this METHOD
  find edges more often than chance" cannot even be asked without it.
- **S-r6 (cross-programme transfer, stated once).** The equity
  programme's leakage tripwire (assert_no_future_information: a snapshot
  must be reproducible from decision-time information alone) is the
  generic form of the point-in-time discipline SMH already practices
  with macro censoring. Conversely, SMH's kill-line pre-registration is
  what the equity factor zoo must adopt before its first real-data
  evaluation. One sentence each; the two programmes share instruments,
  not claims.

## 3. Null-time queue (L2-independent, ordered by value)

1. **Honest-inference layer** — DONE this session (see section 4). The
   naive IC t-stat was the equity programme's largest unstated
   overstatement risk; it is now replaced by Newey-West HAC + Fama-MacBeth
   + Bonferroni, all tested on engineered ground truth including a
   known-autocorrelation case where the naive t provably overstates.
2. **Sharadar decision** — owner's call; the equity programme's first
   real-data run is gated on it ($499/yr full history; $29/mo 5-year).
   Once chosen: ingestion adapter → check_panel audit → the first
   descriptive factor table on real data.
3. **forward_returns vectorization** — needed before 10k-name panels;
   the loop is correct but O(n) per sid in Python.
4. **Exchange calendar** — the panel's date union is a proxy calendar;
   holiday handling needs a real NYSE calendar before delisting-date
   logic touches real data.
5. **Website: equity programme page** — the site (docs/) has no page for
   the equity programme; a short page mirroring the ledger's honesty
   rules would keep the public record consistent when the first
   real-data descriptive results land.
6. **Library ritual continuation** — the queue's standing item (deep
   reads against "what kills the next claim faster").

## 4. What this session actually did

- `src/equity_alpha_lab/inference.py`: Newey-West HAC t-stat (Bartlett
  kernel, no statsmodels dependency), `ic_inference` (the honest version
  of ic_summary — any pre-registered factor claim must cite this, not
  the naive t), Fama-MacBeth with per-date OLS and HAC inference on the
  coefficient series, Bonferroni thresholds for zoo-level multiple
  testing. The naive/HAC ratio is itself reported as a diagnostic.
- 8 new tests: hand-checked HAC computation, an AR(1) rho=0.5 case where
  the naive se provably understates (theory: se ratio ~ sqrt(3)), exact
  Fama-MacBeth on a hand-built 2-date panel, momentum-world recovery,
  null-world silence, Bonferroni arithmetic. Full suite: 161 green.
- This review note + the ratification-queue additions S-r1..S-r6.

## 5. Where the owner should spend decision-attention (not time)

One decision gates the most edge-seeking per hour: the equity data
source. Everything upstream of it is built, tested, and CI-enforced.
The SMH crypto side's next data-dependent step remains the L2
environment (Tardis full-depth for C1-L2/C5, where T1's sign inversion
must resolve). While medicine takes the owner's hours, the queue above
is ordered so any future null-time session has a next item without
needing a decision.
