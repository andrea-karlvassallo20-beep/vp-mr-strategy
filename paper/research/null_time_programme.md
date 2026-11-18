# The null-time programme — what gets done while the L2 environment is being built

Written 2026-11-16, after the math layer verification (math_verification_2026-11-16.md),
the C8 macro-synthesis draft, and the library expansion to 110 OA papers. The owner is
procuring Tardis full-depth L2 data and studying medicine; this document is the standing
answer to "what do we do with the time in between." It is a queue, not a wish list: every
item names what it feeds, whether it is blocked on L2, and how it would be judged.

## 1. The endpoint, restated

The programme's endpoint has not moved: **C1-L2** — does Layer-2 microstructure carry a
compression signal that daily bars could not see — tested behind the L0 gate, kill lines
armed, nothing re-tuned after the fact. Everything in null time either (a) makes the
C1-L2 test sharper when the data arrives, (b) accumulates evidence that does not need
L2 (the sealed-prediction record), or (c) keeps the public instrument honest. Nothing in
null time may touch the sealed C7 panel, fit anything to discovery data, or quietly
expand scope into new claims without pre-declared kill lines.

## 2. What the surprise ledger now does every night (done tonight)

The heat map's time half is now wired into the nightly `board_refresh.py` cycle
(`surprise_ledger.py` runs after the board rebuild). Every night the top-k primed
candidates per class on the LIVING board (mega_dormancy_table) are sealed — hash-chained,
append-only, feature vector frozen, no outcome fields — and every past-horizon entry is
resolved against the same cached klines. This is the cheapest evidence in the whole
programme: it costs nothing, needs no L2, and by the time the L2 environment is ready
there will be weeks of sealed-prediction-vs-reality pairs. The study (Spearman rho
between sealed score and realized 10-bar jump, per class) is descriptive, but it is the
only running falsification of the priming score's RANKING that exists. If after ~100
resolutions the rho is indistinguishable from zero, the priming score's ranking carries
no cross-sectional information at daily grain — that would be a named, dated death,
recorded in the ledger, and it would sharpen C1-L2's motivation (the signal, if any,
lives where daily scores cannot see it).

Honesty note sealed into the adapter: mega-board fields absent from the ledger schema
(evr_m, vol_ratio) are sealed as null, never invented; a primed candidate whose klines
cannot be found is not sealed at all — a score that cannot be resolved against data is
not a prediction.

## 3. The queue (prioritized, each item tagged)

### [null-time, ready now] T1: compression duration-dependence on the second aggTrades window
The owner's memo says run; the second window (2024-08-01 to 2025-02-28, 333,527,416
BTCUSDT aggTrades, 212/212 days, zero missing) was prepared precisely so T1 runs on a
regime the harness never saw during construction. The standing constraint is recorded:
aggTrades is taker prints only — the passive-withdrawal mechanism from the Tesla-day
anatomy is invisible, and no taker proxy may be substituted. T1's question
(duration-dependence of the compression clock) is taker-visible. This is the single
highest-value unblocked item; it needs only the owner's word, which the memo already
leaned toward.

### [null-time, ready now] The misses curriculum, quantified
The Tesla day proved a move can arrive unprimed. That is one anecdote; null time can make
it a base rate. On the cached full-universe klines: enumerate every ≥4-sigma day on the
board, look up the priming state the night before each, and build the honest 2x2 —
primed-vs-unprimed against moved-vs-silent. This measures the priming score's coverage
miss rate (moves that arrive without priming) and its false-alarm rate (priming that
resolves into nothing), descriptively, at daily grain. It feeds directly into what C1-L2
must beat: if daily-grain priming has near-zero coverage, the L2 phase is not refining a
working signal, it is looking for one that daily data provably cannot rank. Pre-declare
the descriptive protocol first; no directional claim, no kill line needed because
nothing is claimed — but the table itself becomes the reference the C1-L2 spec must
confront.

### [null-time, ready now] Library deep-read programme
110 legal-OA papers are downloaded and text-extracted. The null-time ritual: one paper
per session, read against ONE question — "what here would kill C1-L2 faster, or change
its kill lines?" — and the answer written into a dated note (paper/research/library/).
Priority order: (1) CKS 2014 and the deep-OFI line (the math layer was just verified
against them; the verification found a β-factor bug once — re-read for its siblings),
(2) Hawkes branching and excitation stability (the same β lesson), (3) VPIN and
order-flow toxicity (C5's neighborhood), (4) anything on passive-cancel/frozen-book
regimes (the 91.6-96.8% passive-cancel fraction on the replay days makes this the most
live mechanism the L2 data will see). A library is ammunition, not evidence — the
standing caveat binds; the read notes cite, they never launder.

### [null-time, ready now] Website honesty pass
The site is now 12 pages plus the heat map. The standing risk is drift: pages written at
different dates quietly disagree. A null-time pass: read every page against the claims
ledger and fix any sentence that states a claim whose status has moved (C7-30m's death
should be stated as a death everywhere it is mentioned; the compression family now has
three independent kills). The claims ledger is updated with every PR by rule — the prose
pages have no such rule, so they rot. This pass is the rot-remover.

### [needs L2, blocked] Everything behind the gate
C1-L2 itself, C5 (passive cancellation), C6, the macro-synthesis (C8 draft). The block is
solely Tardis full-depth data passing the L0 gate's 100-timestamp audit on every day.
Null time can do exactly one thing for these: keep the verification kit ready so the
data is audited the day it arrives (src/intake_audit.py asserts timestamp units on
arrival; src/verify_l2_gate.py is the gate). Nothing else should be pre-built — the
programme's discipline is that the test specification is frozen before the data, and it
already is.

### [owner-curated, standing] The macro timeline
data/macro_timeline.csv is curated by the owner; it is the regime context for every
censoring decision. Null time can extend it backward (the farther back the event
history, the more censoring windows later hazard work can use) — but every row is
hand-checked or it is worthless. Boring, valuable, endless.

## 4. Methodology review — what I would change about SMH itself, and what I would not

Would not change: falsification-first, kill lines before tests, dead mechanisms named,
the sealed panel, the refusal of WHICH WAY at daily grain. This spine is the asset; the
last month of the record (three independent deaths of the compression family, honestly
recorded) is what makes the programme credible rather than merely active.

Would change, in null time, without touching any claim:

1. **Sealed predictions over retrospective scans.** The clue scans rank; only the
   ledger's sealed-then-resolved record can say whether a ranking ever carried
   information. The nightly seal turns the whole descriptive program from a collection
   of candidate lists into a slow, accumulating measurement. Every future scan should
   ask: does this produce something sealable? If not, it is a tour, not an instrument.

2. **The base-rate discipline.** The programme is very good at finding candidates and
   very good at killing claims; it has been weak on stating base rates — of ~1,300
   series, how many are primed tonight (113), how many move, how many moves arrive
   unprimed. The misses curriculum (above) fixes this. A score without its base rate
   is a story; with it, it is a measurement.

3. **Prose rot as a named enemy.** The heat map once vanished from the site nav because
   nav rewrites used stale lists; prose pages state claim statuses that have since died.
   The fix is mechanical: any page that states a claim must cite the claims ledger, and
   the null-time pass re-verifies them. (The heat map/refresh wiring fixed in PR #126 is
   the same lesson: instruments that are not in the nightly cycle rot silently.)

4. **Reading with a question, not for coverage.** 110 papers is ammunition; the
   programme's edge has never been reading volume, it is reading adversarially — every
   paper interrogated for what would kill the next test faster. The read notes should
   be graded by whether they changed a kill line.

## 5. What was done in this session (so the queue starts from truth)

- `surprise_ledger.py`: `seal_from_mega()` — the living board is sealed into the
  hash-chained ledger (mega schema mapped honestly; absent fields sealed null;
  unresolvable candidates excluded). First mega-board snapshot sealed tonight:
  11 candidates.
- `board_refresh.py`: surprise_ledger.py added to the nightly cycle — seal, resolve,
  study, every night, from now on.
- Tests: 2 new (mega-schema mapping + resolution on mega-sealed entries;
  unresolvable-candidate exclusion), 11 green in the suite.
- This document.

The queue's order is the recommendation: T1 first (it is armed and the data is paid
for), the misses curriculum second (it is the base-rate spine), the library third (it
sharpens kill lines), the website pass fourth (it prevents rot). The owner decides; the
memo rule stands.

## 6. Null-time session 2026-11-16 (second): infrastructure, organization, theory

Executed under the owner's autonomous null-time directive (frozen protocols
honored: no L2 run, no new data, no new claims, no kill lines moved):

- **One-click deployment**: `.devcontainer/devcontainer.json` (Python 3.12 +
  numpy/pandas/pyarrow/scipy/lifelines/scikit-learn/pytest on codespace boot,
  plus the C1-L2 harness compile check), a root `Makefile` wrapping the whole
  gate process (`make env / pull-free / gate / convert / censor /
  harness-check / board / test`), `src/convert_to_parquet.py` (chunked
  csv.gz -> parquet with a binding row-count verification), and
  `CLOUD_DEPLOY.md` section 0 for the one-click path.
- **Tree organization**: `archive/` (the stray KNOWLEDGE (1).md duplicate and
  the root copy of the AVFI research page, byte-identical to the docs copy),
  `paper/research/phase1_daily/` and `paper/research/phase2_l2/` (dated
  reports, audits, memos, completed pre-registrations and their results
  filed by phase; live-automation outputs and the ACTIVE specs stay at the
  root - see `paper/research/README.md`). Every stale path mention in
  README/docs updated the same commit (prose rot rule).
- **Website honesty pass**: the landing page and the clue dossier now state
  the programme status: Phase 1 (Daily/AVFI) CLOSED, Phase 2 (Crypto L2)
  ACTIVE, both citing the claims ledger.
- **Theory**: `docs/smh_paper_draft.md` (the paper skeleton: the three
  deaths, the C7-L2 second life, the C1-L2 transition, the KM/Cox/CPCV
  review notes, the falsification section), `docs/reading_list.md` (the
  adversarial OFI/Hawkes curriculum, library papers cited, candidates
  honestly flagged as unacquired), `docs/roadmap_1_year.md` (the two-branch
  plan and the pre-declared multiplicity rules for any portfolio scaling).
- **Forward-test reminder**: the ex-ante macro timeline
  (`data/macro_timeline.csv`) extended with the three confirmed December
  2026 events (NFP 12-04, FOMC 12-09, CPI 12-10, sources
  federalreserve.gov / bls.gov), verified through `src/macro_censor.py`
  (19 events parse). NOTE for the owner: this repo contains no "Amendment 9
  Sunday macro booking script" - the amendments numbered 1-2 in the tree
  belong to the earlier NQ/AVFI programme record, and the macro machinery
  here is the ex-ante censoring timeline above. Nothing was invented to
  fill the gap; if Amendment 9 lives in another project, it needs its own
  environment check there.
- **Methodology review findings** (recorded in docs/smh_paper_draft.md
  section 4, no code changed): the KM censoring and Breslow-Cox risk sets
  are correct; three honest edge-case notes (unconverged-fit SEs, the
  series-grouped rather than chronological OOF split in the daily harness -
  the L2 harness splits on wall-clock CPCV instead, and the frozen
  episode-builder skip quirk) are stated for the paper, not patched.
- Tests: the full pytest suite green except 5 pre-existing failures caused
  only by scikit-learn being absent from this sandbox (env gaps, not code);
  scikit-learn is now in the devcontainer and `make env` so the codespace
  does not share that gap.

## 7. Null-time session 3 (2026-11-16, post-merge of PR #136): the base-rate spine built, library deep-read session 1 executed

Owner directive: use null time on methodology, reading, and whatever
advances the endpoint. Executed against this queue's own priorities, no
L2, no new claims, no kill lines moved:

- **The misses curriculum 2x2, pre-declared and built** (`src/misses_2x2.py`):
  the existing misses tables condition on MOVES only (coverage); the
  base-rate question needs the silent denominator. The pre-declared
  protocol: one row per series-day over the cached klines universes; the
  frozen C7 priming rule (comp_days >= 20 AND rvol_pct <= 33 AND
  range_pos <= 0.35) computed causally per day, PARITY-PINNED to
  move_study._pre_move_state by a dedicated test (definition drift is a
  bug, not a choice); moved = at least one >=4-sigma day strictly inside
  the next 10 bars (the ledger's horizon, the dormancy sigma); the
  strict-horizon gate the ledger already uses. Outputs the per-class
  table (base rate, P(move|primed), P(move|unprimed), lift,
  false-alarm rate, coverage) plus per-series CSV and a dated report.
  Wired into the nightly board_refresh cycle; ~15s for the whole board
  (bisect-maintained running percentile - numerically identical, parity
  tested). 5 new tests (parity, strict horizon, engineered ground
  truth both ways, rate arithmetic). Its first real run happens in the
  codespace where the klines live - like convert_to_parquet, it refuses
  to invent data and exits 1 where no klines are cached.
- **Library deep-read session 1** (`paper/research/library/
  2026-11-16_cks_ofi_deep_read.md`): CKS "The Price Impact of Order Book
  Events" read against the killing question. Grade: NO kill line changed;
  two sharpenings for the C8 amendment - (1) the review's blocking
  "market-book common factor" now has a theory-named candidate
  definition (depth: beta = c/AD^lambda means depth IS the common
  impact factor by construction), and (2) the "extreme OFI" threshold
  must be pre-declared in depth/tick-normalized units or it is an
  analyst-tunable degree of freedom (the sibling of the beta bug);
  plus the recorded caveat that OFI is cancel-blind by definition, so
  C5's passive-cancellation mechanism is not testable through OFI alone.
- Nothing else: T1 stays armed awaiting the owner's word and the
  codespace; the blocked list stays blocked; the macro timeline stays
  owner-curated.

## 8. Null-time session 4 (2026-11-16): library deep-read session 2 (Hawkes branching) and the website honesty pass executed

- **Library deep-read session 2** (`paper/research/library/
  2026-11-16_hawkes_branching_deep_read.md`): Hardiman & Bouchaud,
  "Branching ratio approximation for the self-exciting Hawkes process"
  (extracted text, page-cited), read against the killing question.
  Grade: NO kill line changed. Three pre-declarations required before
  arming C8: (1) the estimator identity must be named - the MLE path is
  biased UP on short windows (review A3) while the paper's mean-variance
  estimator (1 - sqrt(mu/sigma2)) is biased DOWN on finite windows, so
  silently switching estimators moves n_c across the 0.8 threshold
  without touching a parameter; mandate the mean-variance value as a
  reported cross-check beside the MLE value. (2) The window W must be
  fixed relative to the estimated kernel timescale (their guidance:
  W >> beta^-1, they use 20x) on calibration data BEFORE the threshold
  is armed. (3) The timestamp-bundling trap: their two-minimum
  likelihood pathology comes from exchange-side millisecond bundling -
  the Tardis event stream must pre-declare the clock (exchange
  timestamp) and report the identical-timestamp fraction in the trigger
  window, with the placebo preserving intra-timestamp jitter. Plus the
  scale-sensitivity citation (fixed-W n drifts as latency falls ->
  sharpens the reading of the regime-reproduction kill line) and the
  honest prior that near-critical arrival processes may make n_c > 0.8
  the norm, not the exception - the placebo's 95th percentile is what
  arms the threshold, nothing else.
- **The website honesty pass** (the queue's prose-rot item, executed):
  five pages stated the census's +7.9pp / 0.940-vs-0.862 number as
  "TESTED (C7)", "the spring is real", "the one tested claim of the
  programme... GROUNDED", and - worst - causal.html's claim that the
  vol-tautology question was "asked and answered" YES for the coil,
  when the ledger's TESTED verdict is C7-30m tested-fail (+0.00211, CI
  includes zero) and the family has three recorded deaths. Fixed on
  causal.html (four passages: the census reframed as descriptive with
  the three deaths named and the ledger linked; the GROUNDED tag
  relabeled "GROUNDED (the census)"; the vol-tautology passage now
  carries both the census's yes and the tests' no), clues.html (the
  clue-table row relabeled "CENSUS (descriptive)" with the C7-30m
  death; the night-before gallery caveat), index.html ("the spring is
  real" replaced with the honest status), criteria.html (epigraph
  caveat), v4_charts.html (gallery caveat). The census numbers are kept
  - they are real measurements - but every site now states their
  descriptive status and cites the claims ledger, per the standing rule
  that any page stating a claim must cite the ledger. A repo-wide
  sweep after the pass found zero remaining "TESTED (C7)" /
  "spring is real" / "one tested claim" mentions.
- Tests: 128 green after the pass (no page is regenerated by the suite;
  the edits are durable).

## 8b. Null-time session 4 (convergent second read, 2026-11-16): the branching ratio's scale problem — an independent deep-read of the same paper

Executed under the owner's autonomous null-time directive (frozen
protocols honored: no L2 run, no new data, no new claims, no kill
lines moved, no amendment armed without the owner's word).

- **Library deep-read session 2** (the queue's priority (2), Hawkes
  branching and excitation stability):
  `paper/research/library/2026-11-16_hawkes_branching_deep_read.md`
  on Hardiman & Bouchaud, "Branching ratio approximation for the
  self-exciting Hawkes process" (arXiv:1403.5227v3, extracted
  text, page-cited). Read against ONE question: what kills
  C1-L2/C8 faster. Findings, graded: NO kill line changed — but
  K7 (the Hawkes boundary-constraint line) is materially sharpened,
  PENDING OWNER RATIFICATION: the 0.8 threshold is an
  estimator-at-scale-W statement, not a true-n statement — the
  protocol must pre-declare the estimation window W (ideally a
  W-ladder: 10s/30s/5min reported together), the timestamp-precision
  handling, and that 0.8 binds at the frozen W. The mean-variance
  cross-estimator ñ = 1 − √(μ_W/σ²_W) (model-independent, one line
  of numpy) is the free robustness check: if MLE and mean-variance
  disagree on which bars cross 0.8, the trigger governs nothing.
  Amendment 1's Filimonov-Sornette calibration is honestly
  qualified: this paper reproduces the 0.7-0.8 numbers at fixed W
  AND argues the trend is a fixed-W artifact (scale-invariant
  reflexivity, n → 1 as W → ∞ with 1 − ñ ∝ W^−0.37) — both
  readings put the market near criticality, but they disagree on
  what crossing 0.8 means. The C8 file carries the controversy.
  Gate item recorded: timestamp bundling corrupts the MLE global
  minimum; Tardis microsecond timestamps avoid it, and
  `intake_audit.py`'s timestamp-units assertion is the existing
  guard, to be named in C8's execution order.
- **Session 3's two sharpenings remain unratified**; this session's
  K7 sharpening joins them in the same ratification queue. Three
  candidate amendments, zero armed: the owner's word is the only
  trigger.
- T1 remains armed awaiting the owner's word; the blocked list
  stays blocked. Tests: 128 green on the merged tree before this
  note (documentation only; no code changed in this session).

### Why two session-4 records exist

A second null-time session independently deep-read the SAME
Hardiman-Bouchaud paper against the same killing question, before
seeing this section. Convergence is itself the finding: two
independent reads, same grade (NO kill line changed; K7 sharpened),
same three pre-declarations (estimator identity, frozen W,
timestamp clock). The second read's two contributions not already
above, folded into the ratification queue with the rest:

- **W-ladder reporting**: rather than one frozen W, pre-declare a
  small ladder (e.g. 10s / 30s / 5min) and report n-hat at all
  three together — the paper's own Fig. 5 (1 - n-hat ~ W^-0.37)
  says the W-curve IS the reflexivity measurement; a single W
  reports one point of it. The 0.8 threshold then binds at the
  frozen primary W, with the ladder as the reported context.
- **Amendment 1 qualification, stated against the amendment by
  name**: Amendment 1 grounded 0.8 in Filimonov-Sornette's 0.7-0.8
  modern regime; this paper reproduces those numbers at fixed W
  AND argues the trend is a fixed-W artifact (Moore's-law-rescaled
  W gives an approximately constant branching ratio, Fig. 7).
  Both readings put the market near criticality; they disagree on
  what crossing 0.8 means. The C8 file should carry the
  controversy explicitly, not only the calibration.

The ratification queue now holds four candidate sharpenings
(session 3's two, session 4's three pre-declarations counted as
one K7 sharpening, and the 4b W-ladder/Amendment-1 pair). Zero
armed. The owner's word is the only trigger.


- 2026-11-16 (library ritual, paper 2): Hardiman-Bouchaud branching-ratio
  deep-read (docs/library/hardiman_bouchaud_branching_review.md) — the
  model-independent mean-variance estimator (n ≈ 1 − μ_W/σ²_W), its one-sided
  LOW bias, median-only aggregation (the estimator's mean is −∞), and the
  kernel-misspecification artifact (power-law data fits as critical under an
  exponential kernel). C8's T-H trigger gained three pre-conditions BEFORE
  any L2 data: bootstrap-band firing (not point estimates), the
  kernel-family control, and the mean-variance cross-check as a standing
  diagnostic. Queue next: the VPIN/order-flow-toxicity read, then the
  remaining prose pages against the ledger.

## Progress log

- 2026-11-16 (queue start): surprise ledger wired to the living board, nightly.
- 2026-11-16 (owner authorized T1 + misses + CKS): T1 executed on the second
  window (survives all five kill lines, sign inverted —
  t1_second_window_report.md); the misses curriculum quantified (873 series,
  1,765,316 series-days: coverage 0.039, lift 2.07); CKS deep-read done
  (five siblings named, docs/library/cks_ofi_review.md).
- 2026-11-16 (library ritual, paper 3): VPIN/order-flow-toxicity read
  (docs/library/vpin_toxicity_review.md, records 046/047/048 via the
  flagged summaries + the Andersen-Bondarenko contestation). Four items:
  we hold true aggressor flags the papers had to approximate (BVC becomes
  a diagnostic, never the production classification); the vol-tautology
  sibling in its original habitat (no VPIN reading without its
  vol-conditioned twin); the clock is the object (the taker harness's
  trade-count-bucket VPIN is a different object from A4's volume-bucket
  construction - the crossing is a ledger entry, never silent); and the
  contestation is why C8 insists on pre-registered kill lines. C8 spec
  A4 gained three conditional pre-commitments, BEFORE any L2 data. Queue
  next: the passive-cancel/frozen-book regime read (the mechanism the
  replay days make most alive), then the remaining prose pages.
- 2026-11-16 (this session): C1-L2 spec sharpened BEFORE any Tardis data
  arrived — kill line 6 (sign guard, motivated by T1's inversion: the battery
  had no line to catch an informative-but-inverted covariate) and kill line 7
  (CKS literal tautology control + the AD-denominator unit test), with the
  amendment discipline recorded (harder to pass is the only legal direction).
  Prose-rot pass started: the claims ledger's T1 row and the README's two
  pending-T1 sentences now state the executed verdict and the sign finding.
  Next in the queue: the library ritual's second paper (Hawkes branching —
  the beta lesson's other half), then the remaining prose pages against the
  ledger.


## 9b. Null-time session 5 (convergent record, 2026-11-16): library deep-read session 3 (latent LOB regimes) and the macro timeline extended backward to 2019
- **Library deep-read session 3** (`paper/research/library/
  2026-11-16_latent_regimes_deep_read.md`): Hiremath & Hiremath, "Early
  Detection of Latent Microstructure Regimes in Limit Order Books"
  (arXiv:2604.20949, extracted text, page-cited), read against the
  killing question. Grade: NO kill line changed. The paper is the C1-L2
  hypothesis stated as theory (a stable -> latent build-up -> stress
  DGP; compression is the latent build-up regime; positive lead time
  iff drift-to-noise eta > sqrt(2 log(1/delta)/T1)) - the theory
  citation for why the C1-L2 question is well-posed, and for why its
  honest failure mode may be "below SNR", not "absent". One pre-named
  post-mortem diagnostic (descriptive only, never a new test): their
  46% missed detections concentrate in short-build-up/high-noise
  cells, so a near-kill C1-L2 result should be autopsied by
  compression-duration stratum before the mechanism is named dead.
  Narrative constraint pinned with a citation: OFI/imbalance/volatility
  are reactive BY CONSTRUCTION (their thesis), so C8's OFI trigger is
  contemporaneous, never anticipatory - and their winning channels were
  depth erosion and HMM entropy, the depth family (C6's neighborhood).
  Their "seasonality removal is essential" (depth false-triggers at
  predictable hours) is the empirical citation for our hour-of-day
  stratification. Their 5-event honesty ("order-of-magnitude
  indicators") is a culture citation for our dry-run discipline.
- **The macro timeline extended backward** (the queue's
  owner-curated "boring, valuable, endless" item): every FOMC
  statement day 2019-2026H1 (59 scheduled meetings) + the eight
  tentative 2027 meetings + the two 2020 emergency meetings, ALL
  verified this session against federalreserve.gov's own calendar
  pages (fomccalendars.htm for 2021-2027, fomchistorical2019/2020.htm
  for 2019-2020) - every row hand-checked, per the queue's rule.
  Statement times are 2:00 p.m. ET with DST handled explicitly
  (18:00 UTC in EDT, 19:00 in EST; spot-checked: 2020-11-05 and
  2024-12-18 read 19:00, 2019-03-20 reads 18:00). The two unscheduled
  2020 meetings (Mar 3, Mar 15 - the COVID emergency cuts) do NOT
  carry the regular 2 p.m. time, so they are censored conservatively
  as all-day windows (event_type FOMC_EMERGENCY, 00:00-23:59) rather
  than inventing a precise time. 2027 rows carry confidence
  "tentative" (the Fed's own note: each date is tentative until
  confirmed at the preceding meeting). Notation votes (Mar 19/23/31
  2020, Aug 27 2020, Aug 22 2025) and the Oct 4 2019 unscheduled
  meeting are EXCLUDED as non-decision events - the owner may curate
  them in. CPI/NFP backward extension is NOT attempted: those
  historical schedules are not hand-checkable from the same single
  authoritative page, and a wrong row is worse than a missing row.
  Timeline: 19 -> 87 events, all parse through macro_censor
  (windows verified for first and last rows); 128 tests green.

## 9. Null-time session 5 (2026-11-16): the 500-paper edge triage and deep-read session 3

Owner directive: "go through 500 PDFs for edge." Executed in three
layers, honoring the frozen protocols (no L2 run, no new data, no
new claims, no kill lines armed without the owner's word):

- **Acquisition to 500**: `src/library_expand.py` widened (25 new
  arXiv query families: manipulation/spoofing detection,
  execution, microstructure noise, self-exciting jumps, stablecoin/
  DeFi, tick size, market making, lead-lag, prediction markets,
  deep-learning-on-returns, and more). The expanded library now
  holds **500 papers** (176 previously tracked + 324 new), all
  legal OA, all text-extracted with page markers. The repo-weight
  policy (roadmap improvement 3) was EXECUTED first: new raw PDFs
  land in git-ignored `data/library_pdfs/` (local to the
  codespace); the extracted texts and the index stay versioned.
  Zero off-topic strays (filter re-run).
- **Mechanical edge triage of all 500**
  (`docs/library/edge_triage_500.md`, scores in
  `edge_triage_scores.json`): every text's title/abstract/intro
  region scored for content that could kill or sharpen C1-L2/C8
  (Hawkes/branching/criticality, OFI/LOB, impact, flash events,
  crypto microstructure, overfitting discipline). The result is a
  ranked 40-paper deep-read queue, not a verdict.
- **Deep-read session 3** (rank 1 of the triage):
  `paper/research/library/2026-11-16_mmhp_manipulation_deep_read.md`
  on Fabre & Muni Toke, "High-Frequency Market Manipulation
  Detection with a Markov-modulated Hawkes process"
  (arXiv:2502.04027, 2025; crypto trade data). Grade: NO kill line
  changed; the proxy-refusal/gate layer gains a candidate
  wash-trading audit, PENDING OWNER RATIFICATION — the paper's
  signature is trade bursts WITHOUT price changes (wash trading)
  on a top crypto exchange; if such bursts contaminate the perps
  feed, the branching-ratio trigger measures the manipulator's
  clustering, not reflexivity, and no clean-stretch placebo would
  catch it because the contamination is not random. Candidate
  pre-declaration: audit trigger windows for
  burst-without-price-change events and report the fraction; a
  contaminated window is missing, not zero. Companion evidence
  queued at the top: Aloosh & Li (2024), "Direct evidence of
  bitcoin wash trading" (Management Science). Gifts recorded: the
  MMHP (hidden-Markov-modulated Hawkes, EM + ODE likelihood) is
  C8's structure already built and tested on crypto; their
  seasonality protocol (stable 05:00-12:00 UTC window,
  weekday-matched estimation/testing) is a cheap answer to the
  intraday confound; their own honest limits (the piecewise kernel
  cannot compute endogeneity ratios - so it cannot replace the
  standard Hawkes trigger; indirect detection is false-positive
  prone) protect the C8 layer boundaries.

Ratification queue after this session: six candidate sharpenings
(sessions 3, 4/4b, and this one), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked.

## 10. Null-time session 6 (2026-11-16): deep-read session 4 — the flash crash inside the test year

- **Library deep-read session 4** (rank 2 of the 500 triage):
  `paper/research/library/2026-11-16_crypto_micro_shap_deep_read.md`
  on Bieganowski & Slepaczuk, "Explainable Patterns in
  Cryptocurrency Microstructure" (arXiv:2602.00776, 2026; Binance
  perps, 1s snapshots, 2022-2025, five assets). Grade: NO kill line
  changed. Two candidate sharpenings, PENDING OWNER RATIFICATION:
  (1) the October 10, 2025 flash crash is INSIDE the 2025-26 test
  year - pre-declare it in the split manifest as a named event
  window, reported separately from the pooled reading, so a single
  well-timed short cannot masquerade as a general hazard effect
  (the concrete instance of K4); the event date must be verified
  against the Binance feed at the L0 gate, not trusted from the
  paper. (2) Reinforcing evidence for session 5's spoofing audit:
  their model demonstrably reacted to a single large shallow bid
  with an immediate large prediction - OFI-shaped triggers are
  spoofable by construction on this venue. Gifts recorded: GMADL
  (direction-aware, magnitude-weighted) as a candidate responder
  metric for C1-L2's short-horizon label; their purged
  walk-forward with explicit temporal gap as an independent
  same-venue citation for the programme's purge/embargo
  discipline; and the horizon framing - stable cross-asset OFI
  predictability on Binance perps at 1-SECOND horizons motivates
  the gate but tests none of our claims (C1-L2/C8 live at
  30m-4h-24h; the horizon gap is C8's unexplored cell, and this
  paper is the citable venue evidence). Systemic caution noted:
  a market running homogenized imbalance signals is fragile - if
  C8 passes, the edge is the INTERACTION, not the raw trigger the
  crowd already runs, which is why C8-B (joint superiority over
  trigger alone) must be the honest baseline.

Ratification queue after this session: eight candidate
sharpenings (sessions 3, 4/4b, 5, 6), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked.

## 11. Null-time session 7 (2026-11-16): deep-read session 5 — the boundary-solution rule, documented in the wild

- **Library deep-read session 5** (rank 3 of the 500 triage):
  `paper/research/library/2026-11-16_price_discovery_herding_deep_read.md`
  on Kang, "The Physics of Price Discovery: Deconvolving
  Information, Volatility, and the Critical Breakdown of Signal
  during Retail Herding" (arXiv:2601.11602v2, 2026; Korean
  equities, deconvolution + Hawkes). Grade: NO kill line changed.
  One candidate sharpening, PENDING OWNER RATIFICATION: the
  boundary-solution rule — the paper's own branching-ratio point
  estimate is 0.998 with a bootstrap CI of [0.050, 0.660], and its
  own appendix names the cause: the optimizer "hitting the wall"
  of the stability constraint, the point estimate "likely a
  constrained boundary solution rather than the true underlying
  value." This is K7's pathology with a worked example. Candidate
  pre-declaration for the trigger layer: every branching-ratio
  reading carries its bootstrap CI; a boundary solution (n-hat at
  the constraint within optimizer tolerance) is MISSING, not high
  - it must not fire the trigger, and no placebo on labels can
  catch it because the artifact lives in the FEATURE.
  Reinforcing evidence recorded: (a) session 3's normalized-units
  sharpening - volume normalization is "contaminated by
  volatility artifacts" (their herding/normal signal ratio 0.37
  under volume vs 0.91 under market-cap normalization); (b) the
  trigger's interpretation language - retail surges are the
  near-critical population (0.98-0.999 across thresholds), so on
  a retail-heavy venue the trigger measures self-excited FLOW, not
  "the market is critical"; (c) philosophical support - "market
  efficiency as a state variable" is the C8 premise in another
  market; (d) their non-stationarity caution (trending branching
  ratio, historical training mis-calibrates) matches session
  4/4b's W-ladder and drift-reporting items.

Ratification queue after this session: nine candidate
sharpenings (sessions 3, 4/4b, 5, 6, 7), zero armed. T1 remains
armed awaiting the owner's word; the blocked list stays blocked.
Next in the queue: Aloosh & Li (2024), "Direct evidence of
bitcoin wash trading" - the companion evidence for session 5's
gate audit (to be acquired; Management Science, may be
paywalled - if so, synthesized with the label, per policy).

## 12. Null-time session 8 (2026-11-16): deep-read session 6 — the wash-trading audit gets its ground-truthed toolkit

- **Acquisition**: Aloosh & Li, "Direct Evidence of Bitcoin Wash
  Trading" (Management Science) found legally OA via the DCU
  institutional repository (DORAS); downloaded and text-extracted
  (84 pp., page-marked; PDF local per the weight policy).
- **Library deep-read session 6**:
  `paper/research/library/2026-11-16_wash_trading_deep_read.md`.
  Grade: NO kill line changed. The queued wash-trading audit
  (session 5, pending ratification) gains its sourced statistics,
  validated against leaked ground-truth records: Benford
  chi-squared (wash deviates 69.71, non-wash conforms 7.91),
  unrounded-trade fraction (round-size clustering), lognormality
  deviation, and EDM structural breaks on LOG-transformed
  10-minute volumes (the only one at our 30m grain). The trap
  named and closed: power-law tail fits give OPPOSITE conclusions
  on ground-truthed data - the library's own Clauset-Shalizi-
  Newman heavy-tail recipe would have produced a confidently
  wrong audit, so it is explicitly excluded from the audit's
  statistics. Mechanism refinement: self-self trades are only
  3.35% of an average wash trader's activity (most is trading
  with everyone, which DOES move price), so the audit must not
  rely on the no-price-change signature alone. Scale honesty: the
  direct evidence is a 2011-2013 leaked exchange, not modern
  Binance perps - what transfers is the existence and the
  toolkit, not the fraction; the audit measures our fraction.

Ratification queue after this session: nine candidate
sharpenings (the audit now carries its sourced toolkit), zero
armed. T1 remains armed awaiting the owner's word; the blocked
list stays blocked. Deep-read queue: 3 of the top 3 triage ranks
done plus the companion; next by triage rank: "Modeling
microstructure price dynamics with symmetric Hawkes and
diffusion" and "Optimal Execution with Dynamic Order Flow
Imbalance".


- 2026-11-16 (library ritual, paper 4): Huang-Lehalle-Rosenbaum queue-reactive
  model (docs/library/queue_reactive_review.md) - the deep-read aimed at C5,
  the claim the passive-cancel mechanism belongs to. Four sharpenings, all
  written into C5's entry in orderflow_program.md BEFORE the data:
  (a) cancel intensity is increasing-concave then SATURATING (their Fig. 2,
  explicitly contradicting the classical linear cancel rate) - every
  cancel/absorption feature must be state-conditioned on queue size; a raw
  cancel fraction (the 91.6-96.8% replay readings included) is confounded by
  the queue-size distribution and is not a feature; (b) front-vs-rear
  separation mandatory - the withdrawal mechanism is front-of-queue (priority
  value makes front orders persist, rear orders churn); pooled cancels
  measure churn, not withdrawal; (c) the queue-reactive null beside the
  shuffled-signs placebo - the state-conditioned intensities estimated on the
  gated data itself define what ordinary ergodic queuing produces, and any
  abnormal-withdrawal reading must exceed it; (d) the constant-mid queuing
  period is the risk-set unit (the formal warrant for C5's 'while price is
  flat' clause). The four-paper ritual now stands: CKS -> C1-L2 lines 6-7;
  Hardiman-Bouchaud -> C8 T-H pre-conditions; VPIN -> C8 A4 pre-commitments;
  queue-reactive -> C5 feature pre-conditions. Every spec the L2 data will
  be tested against has been sharpened BEFORE the data exists. Queue next:
  the remaining prose pages against the ledger.

## 13. Null-time session 9 (2026-11-16): deep-read session 7 — the branching matrix, per branch, never by its radius

- **Library deep-read session 7** (next by triage rank, per
  session 8's pointer):
  `paper/research/library/2026-11-16_symmetric_hawkes_diffusion_deep_read.md`
  on Lee & Seo, "Modeling microstructure price dynamics with
  symmetric Hawkes and diffusion model using ultra-high-frequency
  stock data" (arXiv:1908.05089v1, symmetric tick Hawkes on 10
  NYSE S&P 500 names, 2007-2011). Grade: NO kill line changed. One
  candidate sharpening, PENDING OWNER RATIFICATION: the per-branch
  rule — the branching matrix Q = [[q_s, q_c], [q_c, q_s]] is read
  PER BRANCH (self q_s vs cross q_c) with bootstrap CIs, and ONLY
  q_s can carry the cascade interpretation; q_c is the mechanical
  mean-reversion branch. The trigger's justification: their own
  S&P 500 estimates show q_c DOMINATING on ordinary days (GE Jan
  2011: alpha_c 1.3576 vs alpha_s 0.4661 on 0103; the monthly GE
  average has alpha_c > alpha_s), so a pooled branching ratio or
  spectral-radius reading would scream "near-critical cascade" on
  quiet days that were merely fast mean reversion — a false
  trigger in the FEATURE, uncatchable by label placebos. This
  extends (does not replace) the queued CI rule (session 5) and
  boundary-solution rule (session 7): all three live in the
  branching reading, all three make the trigger harder to fire.
  Reinforcing evidence recorded: (a) the moving parameter at
  daily grain is the BASELINE RATE mu, not the excitation
  structure (mu tracks the volatility state with GARCH-like
  persistence; alpha_c "rather stable" through 2008) — the
  drift-reporting item (sessions 4/4b) gains its field
  citation; (b) the SIGN of the tick-grain realized-variance bias
  is itself an excitation fingerprint (their signature plot rises
  toward small tau under mutual dominance, falls under self
  dominance) — any fixed-bias-sign variance check imports their
  Fig. 5 as a counterexample; (c) the Hawkes volatility runs
  15-25% ABOVE TSRV with the gap unexplained, so Hawkes-derived
  volatilities carry a caveat, not a correction.

Ratification queue after this session: TEN candidate sharpenings
(sessions 3, 4/4b, 5, 6, 7, 9), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked. Deep-read
queue: sessions 3-8 of the triage ranks done; next by rank: Bechler
& Ludkovski, "Optimal Execution with Dynamic Order Flow Imbalance"
(the flow-clock session — already acquired, text in the library).

## 14. Null-time session 10 (2026-11-16): deep-read session 8 — the flow clock gains its sourced scale constant; W1's deferred horizon gains its citation

- **Library deep-read session 8** (next by triage rank, per the
  pointer above):
  `paper/research/library/2026-11-16_dynamic_ofi_execution_deep_read.md`
  on Bechler & Ludkovski, "Optimal Execution with Dynamic Order Flow
  Imbalance" (arXiv:1409.2618v2; execution control with an OU
  order-flow imbalance state the trader drifts, endogenous horizon,
  NASDAQ ITCH flow calibration). Grade: NO kill line changed; C8's
  A4 conditional pre-commitments stay frozen as written. One
  candidate sharpening, PENDING OWNER RATIFICATION: the flow-clock
  scale-constant rule — the memory scale of any future flow-state
  estimator is declared BEFORE data as a fraction of daily volume
  (their EWMA flow imbalance: beta = a/V_daily with the cited
  intra-day mesoscopic range a in [10, 100], PDF p. 23), never
  tuned after seeing the gated windows. Reinforcing evidence
  recorded: (a) W1's deferred horizon H is the literature's
  ENDOGENOUS CONTROL, worked: their realized horizon moves up to
  ~50% around the static optimum with the state, and adaptive-
  horizon gains dominate model-form gains (Table 1) — freezing a
  single constant would have pre-registered a guess of a variable
  the field endogenizes, so the deferral already in the W1 spec is
  the only discipline consistent with the citation; (b) market
  orders are <5% of total order flow (Remark 5) — a flow state from
  prints alone reads the taker tip, not the flow, matching the C5
  queue-reactive sharpening from the library ritual's paper 4; (c)
  the model's own drift term (the trader's program enters the flow
  state as dY-drift) is the control-theory form of the wash-trading
  confound: a contaminated window's flow reading measures the
  manipulator's drift, hence "contaminated windows are missing, not
  zero" (session 6) keeps its footing.

Ratification queue after this session: ELEVEN candidate sharpenings
(sessions 3, 4/4b, 5, 6, 7, 9, 10), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked. Deep-read
queue: the top triage ranks stand done through the OFI-execution
paper; next by rank: "Modelling High-Frequency Data with Bivariate
Hawkes Processes: Power-Law vs. Exponential Kernels" (score 41,
below the symmetric-Hawkes/OFI pair, already in the library text
shelf).


## 15. Null-time session 11 (2026-11-16): deep-read session 9 — the triage scorer audited by its own queue; a weak witness recorded honestly

- **Library deep-read session 9** (next by triage rank, per session
  10's pointer):
  `paper/research/library/2026-11-16_bivariate_hawkes_kernels_deep_read.md`
  on Batra, "Modeling High-Frequency Data with Bivariate Hawkes
  Processes: Power-Law vs. Exponential Kernels"
  (arXiv:2503.14814v1, Warwick Finance Societies, 2025). Grade: NO
  kill line changed; NO new candidate sharpening — the honest
  finding is about the QUEUE, not the paper: this was triage rank
  5 of 500 (score 41) and it is an 11-page student-society term
  report (one manually-processed 2-second LOBSTER window of
  AMD/TSLA, "over 200 events", visual comparison of intensity
  plots, no likelihoods, no parameter tables, no out-of-sample,
  no backtest). The triage rubric cannot see quality this deep,
  so: (a) **TRIAGE AUDIT FLAG, recorded for the owner** — future
  triage ranks are candidates, not promises, and the deep-read
  queue falls back to the peer-reviewed entries after this one;
  (b) reinforcing only, no new item: the paper's headline (the
  power-law kernel keeps peaks the exponential kernel's rapid
  decay smooths away) is the SAME mechanism sessions 4/4b recorded
  against peer-reviewed ground (Hardiman-Bouchaud, the branching
  ratio's scale problem), and its method (choosing the kernel
  family by which fits LOOK better on one window) is the
  cautionary exhibit for why the trigger layer's kernel form is
  declared with the spec, BEFORE data. Nothing in the queued
  rules changes; their assumption of a pre-declared kernel form
  gains its negative example.

Ratification queue after this session: ELEVEN candidate sharpenings,
zero armed (unchanged — no sharpening was warranted by this source).
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue: next by triage rank is "Optimum
Liquidation Problem Associated with the Poisson Cluster Process"
(score 39, peer-reviewed line, already on the library text shelf) —
with the triage-audit caveat now on record: the scorer's rank is a
candidate reading, and the owner's library policy (peer-reviewed
first) governs when they diverge.

## 16. Null-time session 12 (2026-11-16): deep-read session 10 — the sign-register rule; T1's honest inversion made prospective

- **Library deep-read session 10** (next by triage rank, per session
  11's pointer, under the triage-audit caveat):
  `paper/research/library/2026-11-16_poisson_cluster_liquidation_deep_read.md`
  on Sadoghi & Vecer, "Optimum Liquidation Problem Associated with the
  Poisson Cluster Process" (arXiv:1507.06514v2, 2015; discrete-time
  MDP/PDMP liquidation, Hawkes order arrivals, simulation study).
  Grade: NO kill line changed. One candidate sharpening, PENDING
  OWNER RATIFICATION: **the sign-register rule for excitation
  features** — the paper's core simulation result is that DAMPING
  (sigma < 0: your selling suppresses subsequent arrivals) and
  EXCITATION (sigma > 0) are materially different regimes of the
  same mechanism, with different optimal behavior and revenue
  (Table 1: $50,000-ish damping panels vs $62,539-$94,691 exciting
  panels). Pre-declaration text: every L2 excitation/damping feature
  is estimated and reported TWO-SIDED with sign and CI; a negative
  reading is recorded in its own register cell as damping, never
  flipped, floored at zero, or discarded as a failed positive. The
  program's precedent is T1 (the registered mechanism measured with
  its SIGN INVERTED — every compression HR below 1.0 — and the honest
  response was to book the inversion, not clip it); this rule makes
  that discipline prospective and binding on the FEATURES, in the
  only legal direction. Reinforcing evidence recorded: (a) their
  negative-self-excitation case is explicitly strategic
  submit/cancel behavior, "known as a 'market manipulation'" (PDF
  pp. 29-30) — the same mechanism family as the queued spoofing
  cautions and the C5 passive-withdrawal claim, so a damping reading
  on a gated window must be audited (ordinary queuing suppression or
  an actor?) before it enters any feature; (b) their
  wait-versus-inventory-penalty balance, set by pre-declared
  microstructure parameters, is the shape of a K7-style
  cost-survival amendment — ammunition if the owner ever ratifies
  cost modeling, and NOT a strategy candidate (the program never
  trades live). Caution on the source: simulation-only, no
  empirical calibration, arXiv preprint with a 2018 journal-
  submission stamp and no published version found — cite the
  structure, never the magnitudes.

Ratification queue after this session: TWELVE candidate sharpenings
(sessions 3, 4/4b, 5, 6, 7, 9, 10, 12), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked. Deep-read
queue: next by triage rank after the liquidation paper is "Price-Aware
Automated Market Makers: Models Beyond Brownian Prices and Static
Liquidity" (score 39, already on the library text shelf); with the
session-9 triage-audit flag on record, rank is a candidate reading,
and the owner's library policy governs when they diverge.

## 17. Null-time session 13 (2026-11-16): deep-read session 11 — the estimator-mode rule; the dimensionality verdict on Hawkes state models

- **Library deep-read session 11** (next by triage rank, per session
  12's pointer, under the triage-audit caveat):
  `paper/research/library/2026-11-16_price_aware_amm_deep_read.md`
  on Bergault, Bertucci, Bouba, Guéant & Guilbert, "Price-Aware
  Automated Market Makers: Models Beyond Brownian Prices and Static
  Liquidity" (arXiv:2405.03496v3, 2024; Dauphine/ILB/Swaap Labs).
  Grade: NO kill line changed. One candidate sharpening, PENDING
  OWNER RATIFICATION: **the estimator-mode rule for state
  variables** — their Hawkes price model needs the current
  intensity to compute quotes, and they NAME the two ways to get
  it: treat it as an observable evolving from a declared initial
  value, or estimate it statistically from recent history
  "similarly to how instantaneous volatility was treated" (PDF
  p. 12). These are different estimators of the SAME window.
  Pre-declaration text: every hidden state variable in a spec
  (intensity, volatility, any flow state) carries, IN THE SPEC,
  its estimator mode — filter-evolution from a declared init, or
  window estimation with a declared window — fixed before data,
  never mixed or switched mid-analysis. It moves a silent analyst
  degree of freedom from the data to the specification, where it
  is cheap and binding — the same police work as the per-branch
  CIs, the boundary-solution rule, and the sign register, from
  another direction. Reinforcing evidence recorded: (a) their
  Markovian Hawkes price carries n in (0,1) as "the percentage of
  price moves that are purely endogenous" (PDF p. 11) — the
  branching ratio AS A NAMED MODEL PARAMETER, an independent
  parametrization of session 4/4b's scale problem (the library
  treats endogeneity as a venue constant; the trigger measures
  it — hence the estimation machinery already queued); (b) their
  explicit dimensionality verdict: Hawkes liquidity states are a
  good statistical fit but CONTROL-TRACTABLE-BROKEN (the value
  function needs 3-5 state variables and the quadratic
  approximation breaks because y and the intensities jump
  simultaneously, PDF p. 17), and a small discrete Markov chain
  (2-3 liquidity states, MMPP) is the tractable alternative (PDF
  pp. 17-19) — the venue citation for preferring a low-state
  regime variable (the MMHP family, triage rank 1) over a
  continuous multi-intensity Hawkes state wherever the two are
  observationally close: fewer hidden states, fewer estimator
  degrees of freedom; (c) an interpretation caution, explicitly
  NOT a rule change: their Z-Hawkes price has a SIGN-DEPENDENT
  quadratic driver (the Zumbach effect, PDF p. 13), so on a
  Zumbach-active window a sign-permuting placebo destroys real
  structure by construction — noted for the interpretation table
  beside any placebo result; it does NOT weaken any queued
  placebo (the legal direction is harder-to-pass, and this points
  the other way). Source cautions: no empirical calibration
  ("No data involved in this study," PDF p. 20); two authors are
  Swaap Labs with disclosed industry funding (read the
  tractability verdicts as engineering, not as claims against
  Hawkes models as such); the AMM market-making content does not
  touch a program that never trades live.

Ratification queue after this session: THIRTEEN candidate
sharpenings (sessions 3, 4/4b, 5, 6, 7, 9, 10, 12, 13), zero
armed. T1 remains armed awaiting the owner's word; the blocked
list stays blocked. Deep-read queue: next by triage rank is
"Functional Limit Theorems for Hawkes Processes" (score 38) — a
theory paper; with the session-9 triage-audit flag on record, note
for the owner: the top-ranked UNREAD triage entry remains
"High-Frequency Market Manipulation Detection with a Markov-
modulated Hawkes Process" (rank 1, score 54, on the shelf), which
may be the higher-value next read given C5/C8's manipulation
line.

## 18. Null-time session 14 (2026-11-16): deep-read session 12 — the dispersion register; a queue-pointer error, corrected

- **Correction of a pointer error, first (the log's honesty is the
  product): session 17's closing note claimed the top-ranked
  UNREAD triage entry was "High-Frequency Market Manipulation
  Detection with a Markov-modulated Hawkes Process" (rank 1,
  score 54). That is wrong. Rank 1 (MMHP, Fabre & Muni Toke) was
  deep-read as session 3 and rank 2 (Explainable Patterns in
  Cryptocurrency Microstructure, Bieganowski & Slepaczuk) as
  session 4 — both notes exist in
  `paper/research/library/2026-11-16_mmhp_manipulation_deep_read.md`
  and `..._crypto_micro_shap_deep_read.md`. The readable queue
  applies to UNREAD entries; the next unread entry was Functional
  Limit Theorems for Hawkes Processes (score 38), which this
  session read. The session-17 pointer text stands unedited above;
  this entry is its correction of record.
- **Library deep-read session 12**:
  `paper/research/library/2026-11-16_functional_limit_hawkes_deep_read.md`
  on Horst & Xu, "Functional Limit Theorems for Hawkes Processes"
  (arXiv:2401.11495v3, 2024; Humboldt/BIT; pure probability
  theory). Grade: NO kill line changed. One candidate sharpening,
  PENDING OWNER RATIFICATION: **the dispersion register** — the
  paper's central theorem is that the long-run behavior of a
  Hawkes process is determined by BOTH the branching ratio m and
  the child-event dispersion sigma = Psi_1(infinity): subcritical
  (m<1) NEVER displays long-range dependence whatever the kernel;
  critical (m=1) bifurcates on sigma (weakly critical: NOT
  asymptotically stationary, no classical FLLN/FCLT, CIR-without-
  mean-reversion limit, C/T correlations; strongly critical:
  FLLN/FCLT hold but the limits are long-range-dependent). The
  consequence for the trigger layer: m-hat near 1 is an
  UNIDENTIFIED object without its dispersion statistic.
  Pre-declaration text: every branching-ratio reading near unity
  carries, beside its bootstrap CI, its estimated child-event
  dispersion Psi_1-hat with its own CI and a finite-vs-divergent
  label under the declared kernel family. This is the rigorous
  completion of the queue's branching machinery: per-branch
  (session 9) fixes WHICH excitation; the dispersion register
  fixes WHICH kernel regime; the CI and boundary-solution rules
  fix WHICH estimate. Reinforcing evidence recorded: (a)
  long-range dependence in arrival counts is ITSELF a
  criticality fingerprint (subcritical never shows it; critical
  cannot avoid it) — a kernel-free cross-check for the
  interpretation table; (b) weakly critical processes are NOT
  asymptotically stationary, which is exactly the initialization
  the filter-evolution estimator modes lean on (session 9's
  stationarity condition; session 13's estimator-mode rule gains
  its limit-theoretic citation: the estimator is not regime-free).
  Caution recorded: the paper is pure theory (no calibration), the
  dispersion statistic is itself estimated on finite windows and
  inherits the same boundary-solution pathology in its tail fit,
  and the fixed-critical limits here are a DIFFERENT object from
  Jaisson-Rosenbaum's nearly-unstable sequences — the queued rules
  must not mix the two regimes when citing.

Ratification queue after this session: FOURTEEN candidate
sharpenings (sessions 3, 4/4b, 5, 6, 7, 9, 10, 12, 13, 14), zero
armed. T1 remains armed awaiting the owner's word; the blocked
list stays blocked. Deep-read queue: with ranks 1-8 and the
Functional Limit Theorems entry (score 38) now read, the next
unread by rank is "Ergodicity and diffusivity of Markovian order
book models: a general framework" (score 37, on the shelf).

## 19. Null-time session 15 (2026-11-16): deep-read session 13 — the queue-reactive null's ergodicity warrant, cited

- **Library deep-read session 13** (next UNREAD triage-rank entry,
  per session 14's pointer):
  `paper/research/library/2026-11-16_ergodicity_lob_deep_read.md`
  on Huang & Rosenbaum, "Ergodicity and diffusivity of Markovian
  order book models: a general framework" (arXiv:1505.04936v1,
  2015; the theoretical companion of the Queue-reactive model
  that produced C5's four feature pre-conditions at the library
  ritual's paper 4). Grade: NO kill line changed, and — said
  plainly — NO new candidate sharpening. This read is the formal
  completion of a warrant the queue already leans on. Recorded:
  (a) **the ergodicity warrant for C5's queue-reactive null** —
  the null ("state-conditioned intensities estimated on the gated
  data define what ordinary ergodic queuing produces; any
  abnormal-withdrawal reading must EXCEED it") needs two facts:
  the invariant distribution exists, and a finite window
  estimates it. Theorem 3.1's V-uniform ergodicity supplies both
  (finite-window estimation of state-conditioned intensities is
  licensed by the mixing; the book's stylized shape is the
  invariant distribution's trace), and the Queue-reactive model
  is verified inside this framework as a special case — the null
  was queued before its warrant was on file; the warrant is now
  cited; (b) volatility is a DERIVED functional of the
  state-conditional flow rates incl. tick-increment
  autocovariances (eq. 7, Theorems 4.1-4.2) — the structural form
  of the deployed vol-tautology check: variance surrogates are
  downstream of the queue's flow rates, never a parallel object;
  (c) event-time vs calendar-time clocks differ by the
  sqrt(expected waiting time) factor (Theorem 4.1 vs 4.2) —
  independent support for A4's frozen volume clock and the
  estimator-mode rule's declared-window requirement; recorded as
  interpretation language, nothing added to A4; (d) the
  framework's delayed (non-instantaneous) reference-price impact
  is the formal shape of the Tesla-day anatomy C5 carries: the
  period break is a competing risk with state-conditioned hazard,
  which is how the C5 harness (d) risk set already treats it.
  Caution recorded: the ergodicity assumptions (bounded
  intensities, downward drift on oversized queues) are sufficient
  conditions on the MODEL, not properties of any real venue — a
  gated window violating them (runaway queues, one actor
  dominating the flow) is outside the warrant, and there the
  manipulation/wash-trading audit items govern, not this
  theorem; and p_ref is a model construct, never a program
  "efficient price" claim.

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (unchanged — no sharpening was warranted).
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue: next unread by rank is "Simulating and
analyzing a sparse order book: an application to intraday
electricity markets" (score 37, on the shelf).

## 20. Null-time session 16 (2026-11-16): deep-read session 14 — the queue machinery is book-shape-specific; the venue freeze gains its warrant

- **Library deep-read session 14** (next UNREAD triage-rank entry,
  per session 15's pointer):
  `paper/research/library/2026-11-16_sparse_lob_electricity_deep_read.md`
  on Bergault & Cognéville, "Simulating and analyzing a sparse
  order book: an application to intraday electricity markets"
  (arXiv:2410.06839v1, 2024; Dauphine/EDF R&D; inhomogeneous-
  Poisson sparse LOB model on EPEX Spot 2021 data). Grade: NO
  kill line changed; NO new candidate sharpening. The paper's
  contribution to the program is a boundary statement — where the
  armed machinery does NOT transfer: (a) **the queue machinery is
  book-SHAPE-specific** — C5's front-vs-rear cancel separation and
  queue-conditioned intensities presuppose a DENSE book (many
  orders per price level, queue priority worth defending); in a
  sparse book there is ONE order per limit (the authors: no
  reason to stack when you can place a tick closer, PDF p. 9) and
  their cancellation intensity showed NO significant state
  dependence — the OPPOSITE of the dense-book queue-conditioning.
  Had the queue features been assumed venue-portable and read as
  a failed mechanism on a sparse venue, the failure would have
  been the spec's, not the market's; the program's BTCUSDT-only
  freeze with all expansion as a new pre-registered family
  (roadmap Q3-4 rules) was already correct, and this is its
  independent warrant; (b) **the maturity clock is a confound the
  program's venue does not have** — in hourly electricity products
  ALL activity intensities grow exponentially toward delivery
  (the Samuelson effect, verified), so any priming/compression
  reading on a finite-maturity contract is entangled with
  time-to-maturity; BTCUSDT perps have no maturity and the
  confound is structurally absent — one more reason the
  expansion-is-a-new-family rule exists before any futures/
  term-structure expansion is priced; (c) interpretation
  language: market-order intensity falls EXPONENTIALLY with the
  spread (beta_M = 0.5 per euro, PDF p. 15) — takers pay for
  width, session 15's cost-gated logic in a second venue family
  and a second mechanism (arrival gating, not horizon choice).
  Cautions: the model is deliberately parsimonious (full cancels
  only, independent marks, no state-dependent cancel intensity),
  the venue has XBID coupling quirks, calibration is
  least-squares against marginal statistics with no CIs; the
  sparse-book claims transfer as STRUCTURE, never as magnitudes.

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (unchanged — no sharpening was warranted;
the venue freeze it would have supported was already on the books).
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue: next unread by rank is "Hawkes-Driven OTC
Market Making: Volterra-Riccati Approximation" (score 37, on the
shelf).

## 21. Null-time session 17 (2026-11-16): deep-read session 15 — the industry's own exogenous-absorption warning; the seasonality treatment extends the drift item

- **Library deep-read session 15** (next UNREAD triage-rank entry,
  per session 16's pointer):
  `paper/research/library/2026-11-16_hawkes_otc_mm_deep_read.md`
  on Barzykin, "Hawkes-Driven OTC Market Making: Volterra-Riccati
  Approximation" (arXiv:2608.02002v2, 2026; HSBC; Hawkes-driven OTC
  RFQ market making on spot-FX data). Grade: NO kill line changed;
  NO new candidate sharpening. Two strong reinforcing citations:
  (a) **the industry's own exogenous-absorption warning** — the
  author, who fitted branching ratios of 0.86-0.90 on EURUSD/
  GBPUSD/USDJPY RFQ flow (> 5*10^5 events per pair, three years),
  states as a first-class caveat that correlated requests "may be
  reactions to a common unobserved cause ... rather than
  consequences of earlier RFQs. If such exogenous variation is
  omitted from the baseline intensity, a fitted Hawkes model may
  absorb part of it into the excitation kernel and thereby
  produce a large branching ratio" (PDF p. 2), and again that the
  ratio "should not be interpreted as direct evidence that one
  client's RFQ causes another client's RFQ" (PDF p. 4). This is
  the false-critical concern behind the queued per-branch rule,
  boundary-solution rule, and drift-reporting item — now stated
  independently by an industry author on his own near-unity
  fitted readings. The queued rules gain their practitioner
  anchor; no new rule was needed. (b) **the seasonality/activity-
  time caution EXTENDS the queued drift-reporting item** — the
  kernel is fitted only after a deterministic time change
  removing the intraday seasonality profile, because fitting in
  calendar time "would confound deterministic seasonality with
  residual serial dependence," and "all rates entering a control
  problem must be expressed in the same clock" (PDF pp. 3-4).
  Recorded as an EXTENSION of sessions 4/4b's drift-reporting
  candidate (from stochastic mu-drift to also cover DETERMINISTIC
  intraday seasonality), not a new queue entry; it independently
  supports session 13's estimator-mode rule and session 16's
  clock statement. (c) Cost-survival ammunition, nothing armed:
  the information value of observing a request priced separately
  from winning it, and the post-request forecast update as a
  first-class state input (PDF pp. 11-12), for IF the owner ever
  ratifies cost modeling. Cautions: private filtered dataset,
  magnitudes never transfer; Volterra-Riccati validated only in
  the exponential benchmark; the two-way RFQ side is a LATENT
  mark (PDF p. 5) — a further warning against treating
  side-signed flow readings as directly observed; single-author
  industry preprint, check for peer review before formal
  citation.

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (the drift-reporting candidate is now
recorded as extended to seasonality; no new entry). T1 remains
armed awaiting the owner's word; the blocked list stays blocked.
Deep-read queue: next unread by rank after the OTC market-making
entry is "General Compound Hawkes Processes in Limit Order Books"
(score 36, on the shelf).

## 22. Null-time session 18 (2026-11-16): deep-read session 16 — the 1/(1-m) volatility amplification; the two-channel volatility decomposition

- **Library deep-read session 16** (next UNREAD triage-rank entry,
  per session 17's pointer):
  `paper/research/library/2026-11-16_compound_hawkes_lob_deep_read.md`
  on Swishchuk & Huffman, "General Compound Hawkes Processes in
  Limit Order Books" (arXiv:1812.02298v1, 2018; Calgary; compound
  Hawkes mid-price models with Markov-chain order marks, diffusion
  limits, one day of level-1 LOBSTER data). Grade: NO kill line
  changed; NO new candidate sharpening. Two reinforcing identities:
  (a) **the 1/(1-mu-hat) amplification** — in every diffusion limit
  proved, the branching ratio enters the price volatility through
  sqrt(lambda/(1-mu-hat)): a fitted branching reading approaching
  one makes the DERIVED long-run volatility unbounded, the same
  instability the queued boundary-solution rule polices at the
  estimator, now visible on the volatility face. A window whose
  branching CI is near unity carries an inflated, unstable
  derived-volatility reading with it; the two readings must be
  reported together, and a near-critical window can never cite its
  derived volatility as independent evidence of anything. Had a
  future instrument spec used a Hawkes-derived long-run volatility
  WITHOUT the branching CI beside it, a single near-critical fit
  would have inflated the estimate without bound and propagated
  downstream as if measured — the boundary pathology wearing a
  volatility costume; the queued rules already require the CI, and
  this read supplies the explicit identity explaining why the
  requirement is not pedantry. (b) **the two-channel volatility
  decomposition, explicit** — the diffusion coefficient factors
  into the arrival channel lambda/(1-mu-hat) (pure clustering/
  endogeneity) times the order-state channel sigma*(ergodic and
  transition probabilities) (pure sign/size persistence): two
  mechanically different sources of volatility multiplied into
  one coefficient — a clean structural citation for the deployed
  vol-tautology family, where a variance-surrogate feature
  conflates the channels and only the tautology checks can say
  which one a reading rode in on; recorded as interpretation
  language, no rule change. Source-quality note: one day, five
  names, level-1, 2012 — the model structure transfers, the
  magnitudes carry nothing; the kernel integrability conditions
  mean the near-critical amplification is an extrapolation
  warning valid in the subcritical regime only (where Horst-Xu's
  critical limits, session 14, govern instead); and the compound
  model assumes the mark chain independent of the arrival process
  — an assumption market data routinely violates (cf. session
  13's Zumbach structure).

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (unchanged). T1 remains armed awaiting
the owner's word; the blocked list stays blocked. Deep-read
queue: next unread by rank is "Limit Order Book Dynamics and
Order Size Modelling Using Compound Hawkes Process" (score 34,
on the shelf).

## 23. Null-time session 19 (2026-11-16): deep-read session 17 — inhibitory kernels fitted, not hypothetical; the wash audit's round-number baseline caution

- **Library deep-read session 17** (next UNREAD triage-rank entry,
  per session 18's pointer):
  `paper/research/library/2026-11-16_compound_hawkes_order_size_deep_read.md`
  on Jain, Firoozye, Kochems & Treleaven, "Limit Order Book
  Dynamics and Order Size Modelling Using Compound Hawkes Process"
  (arXiv:2312.08927v5, 2023-24; UCL & JPMorgan; 12D compound Hawkes
  LOB simulator, twelve months of NASDAQ Level-2 AAPL). Grade: NO
  kill line changed; NO new candidate sharpening. Four reinforcing
  notes: (a) **inhibitory cross-excitation kernels are FITTED, not
  hypothetical** — their norm matrix contains genuinely negative
  entries (in-spread limit orders and opposing-side top cancels
  inhibit each other), with total intensity floored at zero, and
  the classical stability bound (max eigenvalue of the norm matrix
  < 1) is being applied to a matrix that violates the textbook
  sign assumptions, with the authors' own heuristic rescaling when
  it is violated — the cross-branch sign territory of the queued
  sign-register and per-branch rules, now on a year of measured
  NASDAQ data; interpretation language for the trigger layer: a
  fitted branching/norm matrix is READ with its signs, and any
  stability bound applied to it must state its sign regime. (b)
  **THE ROUND-NUMBER BASELINE CAUTION for the queued wash-trading
  audit** — their stylized facts: over 40% of market orders and
  60% of limit orders come at size 100, and outright cancels are
  99.3% of all cancels; ordinary, non-manipulated flow is ALREADY
  massively round-number-clustered, so the audit's round-size and
  unrounded-fraction statistics (from Aloosh-Li's ground truth)
  discriminate on the DEVIATION from the ordinary-flow round-number
  profile, not on the presence of spikes — recorded explicitly so
  the audit, when it runs, is calibrated against the window's own
  ordinary-flow baseline rather than a smooth-size ideal no real
  book satisfies (had it run against such an ideal, EVERY ordinary
  book would have flagged). (c) **power-law kernels selected 100%
  of the time (AIC)** over exponential on twelve months, with
  day-stable kernel shapes — independent venue support for the
  session-9 kernel caution and the dispersion register's
  motivation. (d) **the exogenous-intensity cut-off bias, handled
  explicitly** — non-parametric estimation with finite cut-off
  "massively overestimates" the base rate; the authors back it out
  via (I - Ĝ) Λ̂ — the estimator-hygiene face of the
  drift-reporting item: an uncorrected cut-off inflates the very
  mu the drift rule tracks. Cautions: the simulator is engineering,
  not evidence — parsimony thresholding, heuristic stability
  capping, i.i.d. size marks (their venue-specific finding), US
  equities only, in-sample AIC.

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (unchanged; item (b) extends the queued
wash-audit toolkit's interpretation, it does not change the
audit). T1 remains armed awaiting the owner's word; the blocked
list stays blocked. Deep-read queue: next unread by rank is
"Returns and Order Flow Imbalances: Intraday Dynamics and
Macroeconomic News Effects" (score 34, on the shelf).

## 24. Null-time session 20 (2026-11-16): deep-read session 18 — the macro censor's existence quantified; aggregation endogeneity is grain-dependent

- **Library deep-read session 18** (next UNREAD triage-rank entry,
  per session 19's pointer):
  `paper/research/library/2026-11-16_ofi_macro_news_deep_read.md`
  on Takahashi, "Returns and Order Flow Imbalances: Intraday
  Dynamics and Macroeconomic News Effects" (arXiv:2508.06788v4,
  2025; Hosei/Kellogg dissertation; SVAR-ITH on S&P 500 E-mini
  futures, one-second BBO data, 2008-2013, 34.5 million
  second-observations). Grade: NO kill line changed; NO new
  candidate sharpening. Three reinforcing citations: (a) **THE
  MACRO CENSOR'S EXISTENCE QUANTIFIED** — scheduled macro
  announcements do not merely add noise, they RESHAPE the
  price-flow system: price impact rises, flow impact declines,
  return innovation volatility spikes, flow innovation volatility
  falls (order submission slows — liquidity withdrawal, PDF
  pp. 8-11). The program's deployed ex-ante macro censor excludes
  such windows on principle; this is the measured proof that
  announcement boundaries are REGIME boundaries, not noise
  boundaries — parameters estimated across them are mixtures of
  two systems, and any downstream feature would inherit a
  window-selection artifact no label placebo could catch. The
  censor predates the citation; nothing to change. (b)
  **AGGREGATION ENDOGENEITY IS GRAIN-DEPENDENT** — the feedback
  term that makes OLS inconsistent (their b_f) SHRINKS as the
  sampling interval approaches the event level (mean 0.301 at one
  second vs 0.55 at one minute in Deuskar-Johnson), while price
  impact GROWS at finer grains: both directions of the
  simultaneity are functions of the aggregation, so readings from
  different grains are different objects — never compared, never
  mixed; interpretation language extending the estimator-mode and
  clock statements by one more dimension (grain), already covered
  in spirit by the specs' fixed grains. (c) **SUB-SECOND
  DISSIPATION, measured** — impulse responses die within a second
  (PDF pp. 12-13): the horizon-gap caution flagged in the CKS OFI
  read (1-second OFI results license nothing about 30m-4h
  persistence) is now doubly sourced; C8's unexplored cell remains
  exactly that. Cautions recorded: the venue is a near-constant
  one-tick-spread equity-index future (the depth channel dominates
  the impact channel — a property BTCUSDT perps do not share);
  ITH assumes impact parameters constant WITHIN each 15-minute
  window (the kind of within-window constancy the drift-reporting
  item exists to question); and 37,029 of 38,740 intervals passed
  the rank condition — ~4% of windows silently dropped, a
  window-selection step the program's pre-registered windows would
  have to declare.

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (unchanged). T1 remains armed awaiting
the owner's word; the blocked list stays blocked. Deep-read
queue: next unread by rank is "Packets, Transactions and Queues:
Design Principles for HFT Systems from a Measurement Study of CME
Market Data" (score 34, on the shelf).

## 25. Null-time session 21 (2026-11-16): deep-read session 19 — the delivery pipeline lives in the timestamps; the transport has measured structure

- **Library deep-read session 19** (next UNREAD triage-rank entry,
  per session 20's pointer):
  `paper/research/library/2026-11-16_cme_feed_measurement_deep_read.md`
  on Maciejewski, "Packets, Transactions and Queues: Design
  Principles for HFT Systems from a Measurement Study of CME Market
  Data" (arXiv:2609.32848v2, 2026; M2 Tech; a year of CME NQ
  feed data, ~110 pp.). Grade: NO kill line changed; NO new
  candidate sharpening — the program never trades live, so the
  paper's HFT-engineering content does not touch it; the read is
  for what it implies about RECORDED data's timestamps. Recorded:
  (a) **AN INTERPRETATION CAUTION FOR THE L2 FEATURES: THE DELIVERY
  PIPELINE LIVES IN THE TIMESTAMPS** — the feed between a venue's
  matching engine and any recorded dataset is a QUEUE with its own
  pacing (one packet per ~7.5-microsecond publisher period on CME)
  and its own backlog behavior (more packets, not bigger ones,
  under burst, ~tenfold delay growth), so recorded interarrival
  structure at fine grains is a SUM of market structure and
  delivery-pipeline structure, and any feature reading fine-grain
  arrival timing on the gated BTCUSDT windows measures the PIPE
  until proven otherwise — with the Layer 0 gate's independent
  book_snapshot_25 ground-truth comparison being exactly the
  control that separates the two; CME's ~7.5-microsecond number is
  CME's, and Binance's pipeline geometry must be measured, not
  assumed. (b) Engine-layer near-critical clustering is an
  INFRASTRUCTURE observation, not market evidence — the author is
  explicit that the origin is transactions racing at the engine and
  that market interpretation is out of scope; an arrival-timestamp
  branching reading could carry pipeline/engine structure rather
  than market endogeneity — one more instance of the
  exogenous-absorption caution (session 17), with the absorbing
  layer being hardware. (c) The measured "signature of a race after
  trades" joins the quote-race/front-of-book interpretation family
  carried by C5; interpretation language, nothing armed. Had a
  trigger-layer feature been built on fine-grain arrival timing
  WITHOUT the Layer 0 ground-truth check, the pipeline's queueing
  structure would have been laundered into "market clustering"
  readings — an artifact no label placebo could catch, because it
  lives in the TRANSPORT; the gate and the feature discipline
  already stand between that error and the record.

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (unchanged). T1 remains armed awaiting
the owner's word; the blocked list stays blocked. Deep-read
queue: next unread by rank is "Dynamic optimal execution in a
mixed-market-impact Hawkes price model" (score 34, on the shelf),
with several more score-34/33 entries after it (the triage-audit
flag stands: rank is a candidate reading, not a promise).

## 26. Null-time session 22 (2026-11-16): deep-read session 20 — the MIHM identity: branching and the impact decomposition are locked together in a martingale price

- **Library deep-read session 20** (next UNREAD triage-rank entry,
  per session 21's pointer):
  `paper/research/library/2026-11-16_mixed_impact_hawkes_execution_deep_read.md`
  on Alfonsi & Blanc, "Dynamic optimal execution in a
  mixed-market-impact Hawkes price model" (arXiv:1404.0648v2,
  2014/2015; CERMICS/ENPC; cited within both session 10's and 12's
  reads). Grade: NO kill line changed; NO new candidate sharpening.
  Three reinforcements: (a) **THE MIHM IDENTITY** — in their
  mixed-market-impact Hawkes martingale equilibrium, the endogeneity
  ratio (Hawkes kernel norm) EQUALS the transient-impact fraction
  (iota_s/beta = 1 - nu in the zero-cross-excitation case): the
  price is a martingale even at high frequency when and only when
  self-excitation exactly compensates price resilience. The
  theoretical consequence for the trigger layer: on a venue whose
  high-frequency price is (close to) a martingale — the efficient-
  markets default — a fitted branching ratio is NOT free-standing
  information about endogeneity; it is entangled, by a no-arbitrage
  balance, with the transient/permanent decomposition of impact.
  This joins the exogenous-absorption caution (session 17), the
  per-branch rule (session 9), and the dispersion register (session
  14) as a fourth face of the same discipline: the branching
  reading is never read alone — and this face is theoretical, not
  empirical; no new rule needed, the multi-reading recording
  requirements already force the format. (b) **Poisson flow
  MISPRICES resilience, robustly** — under Poisson order flow the
  model necessarily admits parameter-free price manipulation
  strategies (react with a small opposite-side proportion of each
  incoming order, profitable on average): a flow model that omits
  self-excitation manufactures round-trip "opportunity" out of its
  own omission, so any future K7-style cost-survival layer declares
  its flow model in the spec — Poisson-based cost arithmetic is
  wrong in a known direction; nothing armed (the program never
  trades live). (c) Instant reaction to others' trades is
  equivalent (in their conditions) to manipulation existence —
  chain reactions and instability: the race/feedback family again
  (sessions 21/19), interpretation language only. Cautions: the MIH
  model is deliberately simplified (linear impact, exponential
  decay — their own "not in accordance with empirical facts";
  block-shaped book; the strategic trader does not excite the flow);
  the MIHM identity is a model-internal equilibrium identity, NOT an
  empirical claim about any real venue — it licenses a caution
  about how readings are read, not a prediction; arXiv v2 with a
  2018 stamp, check published version before formal citation.

Ratification queue after this session: FOURTEEN candidate
sharpenings, zero armed (unchanged). T1 remains armed awaiting
the owner's word; the blocked list stays blocked. Deep-read
queue: next unread by rank is "Learning the Spoofability of Limit
Order Books With Interpretable Probabilistic Neural Networks"
(score 34, on the shelf) — directly aimed at C5's
passive-withdrawal family and C8's spoofing cautions, likely the
highest-value remaining entry in its tier.

## 27. Null-time session 23 (2026-11-16): deep-read session 21 — the book is not all intention: spoofable depth measurably moves the conditional price distribution

- **Library deep-read session 21** (next UNREAD triage-rank entry,
  per session 26's pointer):
  `paper/research/library/2026-11-16_spoofability_lob_deep_read.md`
  on Fabre & Challet, "Learning the Spoofability of Limit Order
  Books With Interpretable Probabilistic Neural Networks"
  (arXiv:2504.15908v1, 2025; CentraleSupélec/Paris-Saclay and
  SUN ZU Lab; Level-3 Coinbase BTC-USD/ETH-USD — the triage queue's
  most direct hit yet on C5's passive-withdrawal family). Grade:
  NO kill line changed; NO new candidate sharpening. Findings:
  (a) **[reinforcing]** the round-number baseline caution (session
  17) lands again from the manipulator's side — burst-clusters of
  suspicious orders carry similar ROUND-NUMBER sizes, which the
  authors read as a same-agent fingerprint (PDF pp. 15-17): the
  queued wash-audit gains a citation on exactly the mechanism it
  must control for, with no change to the item's legal content;
  (b) **[interpretation caution]** deep, never-at-the-touch
  passive orders shift the predicted T=1s conditional mid-price
  distribution, and 31% of large orders meet the paper's
  spoofability criterion on a single Coinbase December week —
  depth/imbalance features read a BONA FIDE/manipulation-capable
  mixture whose proportions are venue- and regime-dependent, the
  strongest ammunition yet for the existing depth-describes-
  never-ground-truths discipline, with top-of-book imbalance the
  worst-positioned to see it; (c) **[interpretation caution,
  extending the estimator-mode line]** "suspicious" is a
  model-computed counterfactual against their own network, no ids,
  no labels, and 31% is a threshold artifact of their spec
  (Q >= 4,500 USD, q = 100 USD at touch, their week) — quoted
  nowhere as any venue's spoofing base rate; (d) **[cost-survival
  ammunition]** the probabilistic expected-cost template
  (fees + first-passage fills + liquidation legs of BOTH orders,
  eqs. 27-30, PDF pp. 12-14) any K7-style layer would have to
  carry; (e) **[source-quality note]** trained on 2022-12-01..07,
  applied to 2024-12-04..07, no drift discussion — one more
  instance of the regressed-process caution; arXiv v1, check
  published version before formal citation. Would-have-killed: a
  trigger layer specifying depth/imbalance as BONA FIDE signals
  would have been partially reading manipulative placement on
  exactly the windows that matter, entangled in a way no label
  placebo could catch; any "manipulation is rare" prior written
  into C8 would have been falsified before it armed. Cautions:
  Coinbase SPOT, not Binance perps; T = 1 second only — nothing
  licenses 30m-4h, C8's unexplored cell remains exactly that;
  detection assumes the spoofer optimizes against the paper's own
  impact model (arms-race fragility, their own "first layer"
  admission); round-number and layering observations are eight
  illustrative frames, not a census. Ratification queue after
  this session: FOURTEEN candidate sharpenings, zero armed
  (unchanged). T1 remains armed awaiting the owner's word; the
  blocked list stays blocked. Deep-read queue: next unread by rank
  is the next score-34/33 entry in `edge_triage_scores.json`
  order — check the shelf before reading; the session-9
  triage-audit flag still applies.

## 28. Null-time session 24 (2026-11-18): deep-read session 22 — measured crypto seasonality at the 5-minute grain: the drift item's second seasonality citation, and agent composition is a regime variable

- **Library deep-read session 22** (next UNREAD triage-rank entry,
  per session 27's pointer — verified unread against the note shelf
  by the read-slug mapping, not by title):
  `paper/research/library/2026-11-18_rise_of_machines_crypto_hft_deep_read.md`
  on Petukhina, Reule & Härdle, "Rise of the Machines? Intraday
  High-Frequency Trading Patterns of Cryptocurrencies"
  (arXiv:2009.04200v1, 2020; Humboldt zu Berlin/SMU; post-peer-
  review version of a European Journal of Finance article). GAM
  seasonality on 5-minute CRIX/dyos European-feed data, eleven
  coins, July-August 2018. Grade: NO kill line changed; NO new
  candidate sharpening. Findings: (a) **[reinforcing]** clear daily
  and weekly seasonal structure in volatility AND volume — European
  sleep-hour troughs, 17:00-20:00 peaks, weekend declines (PDF
  pp. 16-17, Figures 7-10) — the queued drift-reporting item's
  second seasonality citation after session 15's Barzykin read, with
  the paper's own caveat that the seasonality is high-significance
  and R^2-around-1% SMALL: a measurement-contamination concern
  (calendar composition folds into naive per-window drift numbers),
  never an exploitable-effect claim; no change to the item's legal
  content; (b) **[interpretation caution]** agent composition is a
  REGIME VARIABLE and its measurement is vintage- and venue-local —
  the "Proof-Of-Human" conclusion (2018 crypto activity shaped
  predominantly by human agents, algorithmic impact "negligible")
  is built on one European vacation-period vintage and explicitly
  against media hype; composition is not portable across vintages or
  venues (this same asset class shows CME engine-transaction races
  in session 19's 2025 study), any future market-structure
  narrative in the record cites its vintage and venue before its
  conclusion — extends the venue-freeze warrant (session 14) and
  the regressed-process caution (session 21) into composition
  drift; (c) **[reinforcing]** the stylized facts (near-zero return
  autocorrelation, positive absolute/squared-return
  autocorrelation, extreme leptokurtosis — BTC excess kurtosis
  49.4, PDF pp. 12-13, Table 1) are the grain's own moments: one
  more citation in the grain-specific-objects family; nothing
  licenses any other grain or venue. Would-have-killed: drift
  reported as a single per-window number would have been a silent
  mixture of calendar composition and drift; and any "crypto is
  algorithm-dominated, calendar effects are dead" narrative in the
  record would have been resting on an unmeasured assumption the
  paper debunks for its vintage. Cautions: 5-minute European-sourced
  index/spot data, one two-month 2018 window — not a perpetual-
  futures order book; R^2 ~ 1% means significance is partly a
  sample-size artifact of the frequency; PoH assumes no algorithms
  mimic human calendars; published EJF version exists, the shelf
  copy is the pre-copyedit arXiv v1, check before formal citation.
  Ratification queue after this session: FOURTEEN candidate
  sharpenings, zero armed (unchanged). T1 remains armed awaiting
  the owner's word; the blocked list stays blocked. Deep-read
  queue: next unread by rank per the read-slug mapping is "The
  Price Impact of Generalized Order Flow Imbalance" (score 33,
  on the shelf).

## 29. Null-time session 25 (2026-11-18): deep-read session 23 — a flow indicator is a (feed x grain x construction) property, quantified: GOFI doubles OFI's apparent power by fixing one aggregation assumption

- **Library deep-read session 23** (next UNREAD triage-rank entry,
  per session 28's pointer — verified unread by the read-slug
  mapping):
  `paper/research/library/2026-11-18_generalized_ofi_deep_read.md`
  on Su, Sun, Li & Yuan, "The Price Impact of Generalized Order
  Flow Imbalance" (arXiv:2112.02947v1, 2021; Xi'an Jiaotong
  University; the CKS-OFI family the program already carries from
  the session-3 CKS review and session 18's Takahashi read).
  Grade: NO kill line changed; NO new candidate sharpening.
  Findings: (a) **[reinforcing]** the entire gain of their
  Generalized OFI over classic Cont-Kukanov-Stoikov OFI on
  China's 3-second snapshot feed (out-of-sample R^2 32.89 ->
  83.57 percent at 30s, 42.57 -> 86.01 percent at 5m, PDF
  pp. 5-6, Tables 1-3) comes from fixing ONE aggregation
  assumption — that the best price moves at most one tick per
  interval: the SAME market and events produce materially
  different OFI series under a different feed grain and
  construction, the cleanest quantified illustration the library
  holds of the aggregation-endogeneity line (session 18) and the
  estimator-mode rule (session 11) — a flow statistic is a
  (feed x grain x construction) property, never a market
  property; the existing grain-declaration and estimator-mode
  rules already force this, nothing new queued; (b)
  **[interpretation caution]** OFI-family R^2 numbers are NOT
  transportable across venues: the 86-percent figure belongs to
  large-tick, price-limit, 3-second-snapshot CSI 500 stocks — BTC
  USDT is small-tick with sub-second depth-diff snapshots and no
  price limits, and a GOFI-style feature on gated windows would
  inherit both the aggregation artifact AND session 21's bona
  fide/manipulation depth mixture; (c) **[source-quality note]**
  thin provenance — arXiv v1 preprint, ten stocks hand-picked "to
  facilitate the presentation", no standard errors, the OA text
  layer garbled (equations and conclusion unreadable), the
  mechanism narrative built from the construction discussion and
  the tables; quote it only for the aggregation mechanism, never
  as evidence of any market fact. Would-have-killed: citing any
  OFI-standard R^2 as a property of "the market" would collapse
  the moment the aggregation assumption breaks (this paper is the
  demonstration), and a trigger layer copying the CKS one-tick
  aggregation verbatim would have mismeasured sub-second
  multi-tick moves by construction, invisibly in backtests because
  the feature and the label share the same cheap construction.
  Cautions: Chinese large-tick equity venue, price limits, linear
  regressions, log-only stationarity treatment, no peer-reviewed
  version located at read time — check before formal citation.
  Ratification queue after this session: FOURTEEN candidate
  sharpenings, zero armed (unchanged). T1 remains armed awaiting
  the owner's word; the blocked list stays blocked. Deep-read
  queue: next unread by rank per the read-slug mapping is
  "Passive Market Impact: A Point Process Approach" (score 33,
  on the shelf) — squarely in C5's passive-withdrawal family
  after session 21's spoofability read.

## 30. Null-time session 26 (2026-11-18): deep-read session 24 — passive orders move prices, and the wrong sign is model-made: the sign-register rule's theoretical demonstration

- **Library deep-read session 24** (next UNREAD triage-rank entry,
  per session 29's pointer — verified unread by the read-slug
  mapping):
  `paper/research/library/2026-11-18_passive_market_impact_deep_read.md`
  on Ouazzani Chahdi, Rosenbaum & Szymanski, "Passive Market
  Impact: A Point Process Approach" (arXiv:2412.07461v2,
  2024/2026; CentraleSupélec/École Polytechnique/Luxembourg) -
  the theoretical companion to session 21's spoofability read.
  Grade: NO kill line changed; NO new candidate sharpening.
  Findings: (a) **[reinforcing]** the paper's starting point IS
  the wrong-sign artifact: in the constant-kappa Hawkes propagator
  price, a resting buy metaorder's executions mechanically push
  the price DOWN - impact of the wrong sign for a whole order
  class, manufactured entirely by a modeling choice
  (state-independent information content), against the empirical
  fact that limit-order impact is comparable to market-order
  impact with the correct sign (PDF pp. 1-3) - the queued
  sign-register rule's (session 10) cleanest theoretical
  demonstration, its empirical motivation untouched; (b)
  **[reinforcing]** the fix - kappa as a DECREASING function of
  the touched queue's volume, a price-resistance coefficient -
  gives passive metaorder impact that is monotone during
  execution, ~sqrt(participation) at large rates (their
  V-profile argument; simulated exponent 0.54), with NO
  relaxation phase; this is the equilibrium-side picture of what
  session 21 measured, and it is C5's passive-withdrawal family's
  theoretical warrant for causal-language territory: passive
  depth is never a neutral regressor (PDF pp. 3-6, 14-19);
  (c) **[cost-survival ammunition]** passive execution cost
  schedules differ QUALITATIVELY from aggressive ones - no
  post-execution relaxation, the book re-stations and the impact
  stands (PDF pp. 18-19); a K7-style layer assuming the
  aggressive impact shape for passive fills would misprice the
  post-execution leg in a known direction, and the instantaneous-
  impact template (eq. 4) would have to declare its flow model
  per the session-20 Poisson-mispricing rule; (d)
  **[interpretation caution]** a fitted kappa is a book-state
  moment, not a constant, and moves with volatility (higher
  volatility <-> smaller resistance; PDF pp. 19-21): any future
  resistance- or depth-elasticity estimate is state-dependent and
  regime-moving, joining the per-branch rule (session 9), the
  dispersion register (session 14), and the MIHM identity
  (session 20) in the never-read-alone family. Would-have-killed:
  flow-based features inheriting an aggressive-order sign
  register would carry mechanically perverse signs for passive
  flows with NO diagnostic flagging it (the model fits, backtests
  run, the signs are wrong); and any causal claim about passive
  depth phrased as a "liquidity description" instead of routed
  through C5 would have predated the theoretical statement that
  passive placement moves the conditional price process itself.
  Cautions: stylized one-queue-per-side model, market orders
  independent of book state (the authors' own "unrealistic"
  admission - the independence the model then partially repairs),
  negative queues allowed, linearized kappa-squared calibration
  with non-parametric estimation out of scope, 0.54 simulated
  exponent as illustration not evidence; arXiv v2 with a 2026
  stamp, no published version located - check before formal
  citation. Ratification queue after this session: FOURTEEN
  candidate sharpenings, zero armed (unchanged). T1 remains armed
  awaiting the owner's word; the blocked list stays blocked.
  Deep-read queue: next unread by rank per the read-slug mapping
  is "Optimal Execution with Passive Market Impact" (score 33,
  on the shelf) - the sibling of this paper's framework.

## 31. Null-time session 27 (2026-11-18): deep-read session 25 — a passive fill is the endpoint of an unseen tactical chain, and impact feeds back into one's own quoting

- **Housekeeping first:** at the owner's request the synthesis
  excursion was REVERTED (commit d77d578, git revert of the
  synthesis commit) — the owner asked to go back to the queue
  routine exactly as it stood; the synthesis file is gone, the log
  ends at session 30 for that purpose, and the queue resumes where
  session 30's pointer left it.
- **Library deep-read session 25** (next UNREAD triage-rank entry,
  per session 30's pointer — verified unread by the read-slug
  mapping):
  `paper/research/library/2026-11-18_passive_execution_optimal_deep_read.md`
  on Barzykin, Boyce, Neuman & Tuschmann, "Optimal Execution with
  Passive Market Impact" (arXiv:2607.28323v1, 2026; HSBC and
  Imperial College London; the sibling of session 24's framework -
  the authors call Ouazzani Chahdi et al. "the closest theoretical
  antecedent"; first author is the same Barzykin as session 15's
  HSBC industry read). A mesoscopic model: exponential fill
  intensity lambda*e^{-k*delta}, per-level MLOFI impact decay
  l, combined into a permanent passive impact rate eta*e^{-m*delta},
  m = k + l; explicit optimal quotes when m = k (NASDAQ: l << k),
  Lambert-W semi-explicit for m != k (LSEG FX: visible gap, Table 5).
  Grade: NO kill line changed; NO new candidate sharpening.
  Findings: (a) **[interpretation caution]** a passive fill in
  recorded data is the ENDPOINT of an unseen tactical chain —
  Remark 2.1: maintaining a quote at distance delta is repeated
  cancel-and-repost, geometrically many more submissions the
  deeper the quote, whose continuous limit IS the fill intensity
  (PDF p. 5) — a fill event underdetermines the strategy that
  produced it, and any feature treating fills as samples from a
  single resting order's lifetime mismeasures its own input; a
  new (tactical-chain) face of the existing C5 depth-measurement
  discipline, nothing queued; (b) **[reinforcing]** distance is
  an informative proxy only in the right tick geometry — the
  authors themselves flag their large-tick MLOFI decay estimates
  as "particular caution" cases where impact depends on volume
  queued ahead and the coarse grid prevents distance from
  substituting (PDF p. 15) — the mirror image of session 21 and
  one more instance of the estimator-mode rule (session 11): the
  same covariate changes information content with tick geometry;
  (c) **[reinforcing]** the m ~ k coincidence is an empirical,
  asset-class-, and construction-specific finding, NOT a law —
  FX breaks it, and the FX estimates are conflated-snapshot,
  synthetic-fill, public-data constructions that "capture only
  part of the total FX liquidity" (PDF pp. 16-17): the
  venue-freeze warrant (session 14) and the construction triple
  (session 23) again; (d) **[cost-survival ammunition]** impact
  feeds back into the agent's own quoting — stronger passive
  impact makes the optimal quote DEEPER, fewer and slower fills,
  implementation shortfall roughly unchanged (PDF pp. 9-11) — so
  any K7-style cost layer must model the feedback of impact onto
  one's own subsequent quoting or price a strategy the optimal
  policy would not trade; (e) **[source-quality note]**
  illustrative hand-set simulation parameters (Table 1) and
  exposure-style synthetic FX fills — a method demonstration, not
  venue facts; arXiv v1, unpublished at read time, check before
  formal citation. Would-have-killed: passive fills treated as
  samples from one order's resting lifetime would have made the
  fill statistics of different distance cohorts incomparable with
  no visible distortion (the chain lives upstream of every
  observable), and static execution schedules under passive impact
  would have missed the feedback the optimal policy exploits.
  Cautions: mesoscopic by construction (no book state, no queue
  priority, adverse selection absorbed into noise), permanent-only
  impact in the core model, mixed tick geometries in the equity
  sample. Ratification queue after this session: FOURTEEN
  candidate sharpenings, zero armed (unchanged). T1 remains armed
  awaiting the owner's word; the blocked list stays blocked.
  Deep-read queue: next unread by rank per the read-slug mapping
  is "Compound Hawkes Processes in Limit Order Books" (score 33,
  on the shelf).
