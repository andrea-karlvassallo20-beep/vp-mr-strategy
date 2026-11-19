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
  metric for C1-L2's short-horizon label; their purged  walk-forward with explicit temporal gap as an independent
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


## 17. Null-time session 13 (2026-11-18): deep-read session 11 — the queue-imbalance two-null admission rule, re-earned from the shelf; the reset-loss corrigendum and the numbering reconciliation

- **Corrigendum and record recovery first** (append-only; no earlier entry is edited).
  The state audit this session: main stands at eef409ee with deep-reads 1-10 adopted
  (PR #160 merged 2026-11-18T10:26Z; CI verified green this session: both "test" and
  "engine" check runs success — the CI verification deferred at the last adoption is
  closed). Separately, a parallel conversation lineage reported deep-reads of this same
  queue-imbalance paper, of a CKS-OFI full re-read, of the VPIN/BVC construction, of
  MLOFI, and a blocked Chakrabarty trade-classification attempt, numbering them as
  null-time sessions 23-27. NONE of those readings ever landed in this log, and their
  staged notes were held in a sandbox working tree that an environment reset wiped;
  this session verified the machine library holds only the eleven 2026-11-16 notes.
  Per the honest-error protocol: the lost readings carry ZERO status here, and this
  log's numbering governs (last entry was session 12; this is 13; nothing renumbered).
  The one read re-earned legally from the page-marked shelf this session is the queue
  imbalance paper (below). The lineage's two other claimed sharpenings (an OFI-null
  admission rule from the CKS re-read; proxy-validation baselines from the VPIN/BVC
  read) are NOT queued: this repo already holds the CKS OFI deep-read (session 3) and
  the VPIN review (library ritual paper 3) covering that ground; anything beyond them
  must be earned by fresh page-cited reads. MLOFI (x09d0b5, score 29) and the
  trade-classification dispute papers remain UNREAD queue candidates.
- **Library deep-read session 11** (a RECOVERY READ, declared as such; triage trace 15,
  rank 47 of 500; the queue's next UNREAD pointer is unchanged):
  `paper/research/library/2026-11-18_queue_imbalance_deep_read.md`
  on Gould & Bonart, "Queue Imbalance as a One-Tick-Ahead Price Predictor in a Limit
  Order Book" (arXiv:1512.03492v1, 11 Dec 2015; LOBSTER Nasdaq 2014, 10 liquid stocks,
  logistic and local logistic regression of next-mid-move direction on the normalized
  best-quote imbalance I). Grade: NO kill line changed. ONE candidate sharpening,
  PENDING OWNER RATIFICATION: **the two-null admission rule** — the paper's null is a
  constant 1/2 probability (Eq. 18, PDF p. 14) and every headline improvement is
  measured against it alone, while the paper's own two-line state variable (Eq. 7,
  PDF p. 7; a pure depth snapshot, no events, no signing) achieves out-of-sample AUC
  0.75-0.81 large-tick and 0.58-0.64 small-tick one mid-change ahead (Table 4, PDF
  p. 20) with in-sample ≈ out-of-sample (no overfit, PDF pp. 19-21). Pre-declaration
  text: any C1-L2/C8 short-horizon flow feature is admitted only if it adds value
  beyond BOTH the tautology-controlled top-of-book OFI benchmark AND a pre-registered
  Eq.-7 queue-imbalance comparator; a flow feature that loses to a two-line state
  variable carries no incremental claim. Harder to pass because the feature must now
  survive two structurally different nulls, the second immune to event-flow laundering.
  Interpretation cautions recorded with page cites: the venue expectation band is the
  paper's small-tick band on a maximal-small-tick perp (AUC 0.58-0.64, probabilistic
  improvement 2-6%, Table 5, PDF p. 21; mechanism: spread-pinning, PDF pp. 25-26), not
  the large-tick ceiling; the horizon is a mid-change-count horizon, NOT fixed time
  (Sec. 5.1, PDF pp. 11-12), so any fixed-horizon port must pre-declare its sampling
  convention (the paper names alternatives it never tested, PDF pp. 27-28).
  Reinforcing: percent-of-null improvements are never reported without absolutes (the
  50-60% headline is a percentage of a deliberately dumb null; Tables 4-5, PDF
  pp. 20-21). Source quality: arXiv v1, CFM affiliation acknowledged (PDF p. 28), one
  sign-definition misprint flagged (PDF p. 8), published version to be checked before
  formal citation.

Ratification queue after this session: THIRTEEN candidate sharpenings (the twelve
standing plus the two-null admission rule joined 2026-11-18), zero armed. T1 remains
armed awaiting the owner's word; the blocked list stays blocked. Deep-read queue: the
next UNREAD triage entry is unchanged — "Price-Aware Automated Market Makers: Models
Beyond Brownian Prices and Static Liquidity" (score 39, already on the library text
shelf); with the session-9 triage-audit flag on record, rank is a candidate reading,
and the owner's library policy governs when they diverge.
## 18. Null-time session 14 (2026-11-18): library deep-read session 12 - the ACF-shape gate proposed for the branching-ratio trigger; the CARMA(p,q)-Hawkes shelf entry read and graded theory-only

- **Library deep-read session 12** (parallel slot 19; assigned entry, score 32, x8627c5;
  verified before reading that no note for the slug existed and no other PR covered it):
  `paper/research/library/2026-11-18_carma_hawkes_intensity_deep_read.md`
  on Mercuri, Perchiazzo & Rroji, "A Hawkes model with CARMA(p,q) intensity"
  (arXiv:2208.02659v3, 2022). Grade: NO kill line changed. ONE candidate sharpening,
  PENDING OWNER RATIFICATION: **the ACF-shape (kernel-validity) gate** - the
  exponential-kernel Hawkes fit behind C8's trigger provably implies a strictly
  monotonically decaying count-increment ACF (Eq. 9, PDF pp. 5-6; stated as the
  model's central limitation, PDF p. 2), so a day whose empirical increment ACF
  is significantly non-monotone rejects its own fit and its ML branching ratio is
  a misspecified quantity. Pre-declaration text: no day's branching-ratio trigger
  reading is admissible unless the underlying fit passes a pre-registered
  ACF-shape check at a pre-declared lag ladder; shape-failing days contribute no
  firing (neither positive nor negative) and the failure rate is reported. Harder
  to pass than the standing estimator-at-scale-W item (deep-read session 2): it
  extends estimator discipline from scale to kernel shape, withholding trigger
  bars the old protocol would have fired on. Interpretation cautions recorded
  with page cites: the model is counting-process only, never prices/signs (Def. 2,
  PDF p. 8); the closed-form ACF and inference machinery hold only in the
  stationary regime under negative-real-part eigenvalue conditions (Assumption 1,
  Props. 6-7, PDF pp. 10, 20-21), so stationarity is a precondition, not a
  diagnostic. Reinforcing, no new item: strong mixing at exponential rate and ACF
  asymptotic normality (Props. 8-9, PDF pp. 21-23) support the existing day-block
  inference discipline, provided the stationarity condition holds on the estimated
  segment. Source quality: arXiv v3; Section 6 is simulation-only (PDF pp. 24-27),
  no financial data anywhere; the non-monotone-ACF-for-real-data claim rests on
  citation, not measurement; published version to be checked before formal
  citation.

  Ratification queue after this session: FOURTEEN candidate sharpenings (the
  thirteen standing plus the ACF-shape kernel-validity gate joined 2026-11-18),
  zero armed. T1 remains armed awaiting the owner's word; the blocked list stays
  blocked. Deep-read queue: the standing next UNREAD pointer set at null-time
  session 13 stands - "Price-Aware Automated Market Makers: Models Beyond Brownian
  Prices and Static Liquidity" (score 39, already on the library text shelf); with
  the session-9 triage-audit flag on record, rank is a candidate reading, and the
  owner's library policy governs when they diverge. (This session was a pre-assigned
  parallel slot 19 of 24, so it does not consume the queue's top pointer.)
  Nothing measured, no kill line moved, nothing armed, nothing trades live.
## 19. Null-time session 15 (2026-11-18): deep-read session 13 — the distance-grid sign-invariance rule; spoofers found to avoid the very queue the two-null comparator watches

- **Library deep-read session 13** (pre-assigned parallel-fire slot, verified
  UNREAD before reading: no note for slug x2aee07 existed in `paper/research/library/`
  and no PR, open or merged, covered it at session start):
  `paper/research/library/2026-11-18_spoofability_lob_deep_read.md`
  on Fabre & Challet, "Learning the Spoofability of Limit Order Books With
  Interpretable Probabilistic Neural Networks" (arXiv:2504.15908v1, 23 Apr 2025;
  Coinbase Level-3 BTC-USD/ETH-USD via SUN ZU Lab; multi-scale Hawkes-inspired
  limit-order-flow features with explicit posting-distance kernels, a probabilistic
  NN predicting the skewed-Gaussian law of the one-second mid move, counterfactual
  order-insertion response experiments, and an expected-cost spoofing detector).
  NB: the slot assignment mislabelled the title as "Probabilistic Logic Programming";
  the actual paper and extract are Neural Networks (recorded in the note).
  Triage-rank: score 34, read as a pre-assigned parallel slot (the queue's next UNREAD
  pointer is not consumed).
- Grade: NO kill line changed. ONE candidate sharpening queued, PENDING OWNER
  RATIFICATION: **the distance-grid sign-invariance rule** — any C1-L2/C8 feature built
  from limit-order flow aggregated over book depth must pre-declare its distance
  weighting (or hard depth cutoff) and show its registered sign stable across a
  pre-registered distance grid before admission (mechanism: impact is monotone in
  posting distance and remains significant several bps from touch, Figs. 6–7,
  PDF pp. 10–11; flagged-manipulative depth averages ~6.9 bps from touch vs ~1.0 bp
  for normal flow, Table 1, PDF p. 19; the paper's own verdict that distance-blind
  models are "not suitable to describe the data", PDF p. 10). Tightens the
  sign-register and flow-clock scale-constant rules: a depth-aggregated flow feature
  can no longer inherit significance from one arbitrary aggregation radius, and
  manipulable-depth contamination gains a named, pre-registered test it must fail.
  Harder to pass; reading-side only; the owner's word alone ratifies.
- Reinforcing (no new item): the paper's detection output shows spoofers almost never
  post at the best queue (0% of large suspicious orders at top-of-book vs 4.20% of
  large normal, Table 1, PDF p. 19), giving mechanistic support that the Gould–Bonart
  Eq. 7 top-of-book comparator of the two-null admission rule (null-time session 13)
  is comparatively robust to spoofing: the manipulable pressure is the pressure spoofers
  do not put there. Interpretation caution (extends the sign-register rule to this
  feature family): the paper's market order flow counts sell marketable orders hitting
  the bid, so its "market imbalance predicts a lower expected move" partial dependence
  (Figs. 4–5, PDF pp. 8–10) is a sign-convention statement about aggressive selling,
  not "buy flow predicts down"; any C1-L2 port must fix the initiator-side sign map
  in the pre-registration before estimation. Cost-survival ammunition (relevant only
  if a K7-style layer ever exists): flagged-spoofable depth is followed by
  significantly larger realized one-second moves than normal orders (avg 0.11 bp,
  skew 0.45 vs 0.02/0.02, Table 1, PDF p. 19); a cost model treating all displayed
  depth as real liquidity understates adverse execution on unregulated venues.
  Source quality: N = 10 sampled points per (Q, distance) response cell (PDF p. 10);
  trained on one week of Dec 2022, applied to Dec 2024 with no drift test (PDF pp. 7,
  15); the 31% headline is an expected-gain-conditioned label, not observed
  manipulation (PDF pp. 14–15); no trader IDs, no ground truth (PDF p. 14);
  Assumption 1 (no partial fills) acknowledged false (PDF pp. 11–12); arXiv v1,
  check published version before formal citation.
- Inaccessible/blocked status: none this session. The extract was present, page-marked
  and complete (22 pp.).

Ratification queue after this session: FIFTEEN candidate sharpenings (the fourteen
standing plus the distance-grid sign-invariance rule joined 2026-11-18), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays blocked. Deep-read
queue: the next UNREAD triage entry is unchanged — "Price-Aware Automated Market
Makers: Models Beyond Brownian Prices and Static Liquidity" (score 39, already on the
library text shelf); with the session-9 triage-audit flag on record, rank is a candidate
reading, and the owner's library policy governs when they diverge. (This session was a
pre-assigned parallel slot, so it does not consume the queue's top pointer.) Nothing
measured, no kill line moved, nothing armed, nothing trades live.
## 20. Null-time session 16 (2026-11-18): library deep-read session 14 — the size-state persistence comparator proposed as the third admission null; the fixed-tick structural-bias caution; Swishchuk–Huffman graded theory-heavy, evidence-light

- **Library deep-read session 14** (a PRE-ASSIGNED parallel slot, declared as such — slot 6
  of 24, triage score 36, slug xfeb371, so it does not consume the queue's top pointer;
  verified at session start that no deep-read note for the slug existed and no open or
  unmerged closed PR covered it — the CARMA-Hawkes (session 15 deep-read 12) and
  spoofability (session 15's deep-read 13) slots had not yet landed when this read began;
  this entry's number was taken fresh from the log tail at append time):
  `paper/research/library/2026-11-18_general_compound_hawkes_lob_deep_read.md`
  on Swishchuk & Huffman, "General Compound Hawkes Processes in Limit Order Books"
  (arXiv:1812.02298v1, 6 Nov 2018; compound Hawkes mid-price models with n-state Markov
  chains on mid-move sizes; LLN + diffusion limits proven; LOBSTER level-1 single-day 2012
  fits for AAPL/AMZN/GOOG/MSFT/INTC). Grade: NO kill line changed. ONE candidate
  sharpening, PENDING OWNER RATIFICATION: **the size-state persistence comparator** — the
  paper's diffusion limit factorizes mid-price volatility into an arrival term
  λ/(1−μ̂) and a size-state term σ* (Eq. 34, PDF p. 9; Eq. 36, PDF p. 10), and its own
  quantile Markov chain on mid-move sizes (Sec. 5.3, PDF pp. 16–17; transitions by
  frequency counting, PDF p. 14) recovers 28–60% of the mean residual the intensity-only
  fixed-tick model missed on the multi-tick names (Table 8, PDF p. 18) with nothing but
  the tape. Pre-declaration text: any short-horizon C1-L2/C8 flow feature earns an
  incremental-claim comparison only if it adds value beyond (a) the top-of-book OFI
  benchmark, (b) the Eq.-7 queue-imbalance comparator, AND (c) a pre-registered own-price
  size-state persistence comparator built as the paper's quantile chain on the venue's
  realized mid-move size distribution. Harder to pass than the standing two-null rule
  because the third null never touches the book or event stream — immune to both
  event-flow and depth laundering. Interpretation cautions with page cites: fixed-tick
  constructions are structurally biased on multi-tick venues — 61%/53%/71% of mid changes
  exceed half a tick on AAPL/AMZN/GOOG (PDF p. 15; Fig. 4, PDF p. 24) — and the C1-L2
  venue is maximal-small-tick, so any one-tick convention must be declared against the
  venue's actual move-size distribution; even the size-chain leaves AMZN with 20.8%
  coefficient error (Table 9, PDF p. 18), so a residual is not evidence of a flow
  channel. Reinforcing: implied α/β = 0.41–0.53 across all five names (Table 2, PDF
  p. 14), per-branch estimation is the only legal shape; direction persistence flips sign
  across names (Table 4, PDF p. 15), reinforcing the sign-register rule. Source quality:
  single trading day, five equities, level-1 data, arXiv v1 with placeholder venue
  pagination, N(t) counts mid-price changes not order arrivals — cite the structure,
  never the magnitudes.

  Ratification queue after this session: SIXTEEN candidate sharpenings (the fifteen
  standing plus the size-state persistence comparator joined 2026-11-18), zero armed.
  T1 remains armed awaiting the owner's word; the blocked list stays blocked. Deep-read
  queue: the standing next UNREAD pointer set at null-time session 13 stands —
  "Price-Aware Automated Market Makers: Models Beyond Brownian Prices and Static
  Liquidity" (score 39, already on the library text shelf); with the session-9
  triage-audit flag on record, rank is a candidate reading, and the owner's library
  policy governs when they diverge. (This session was a pre-assigned parallel slot 6 of
  24, so it does not consume the queue's top pointer.) Nothing measured, no kill line
  moved, nothing armed, nothing trades live.
## 21. Null-time session 17 (2026-11-18): deep-read session 15 — the Proof-Of-Human paper read as caution, both laundering directions named

- **Library deep-read session 15** (a PARALLEL-FIRE SLOT ASSIGNMENT, slot 12 of 24,
  declared as such — this paper was pre-assigned to avoid duplicate work across the
  24 simultaneous slots, so it was read out of the standing queue's top-pointer order;
  the standing next-UNREAD pointer is unchanged, see the close; numbering note: this
  entry was drafted by the slot's own session against a stale tail (self-numbered session
  16 / deep-read 14) and was renumbered machine-side to the next free numbers (session
  17 / deep-read 15) after concurrent slots landed sessions 14-16; no existing text edited):
  `paper/research/library/2026-11-18_rise_of_the_machines_deep_read.md`
  on Petukhina, Reule & Härdle, "Rise of the Machines? Intraday High-Frequency
  Trading Patterns of Cryptocurrencies" (arXiv:2009.04200v1, 2020; post-peer-review,
  pre-copyedit version of a European Journal of Finance article; 5-minute CRIX/dyos
  European-market data, 11 coins, Jul–Aug 2018). Grade: NO kill line changed; NO new
  candidate sharpening. Findings, page-cited: (1) GAM diurnal/weekly seasonality with
  highly significant smooth terms explaining only ~1% (PDF p. 15), the human-shaped
  intraday curve (nighttime trough, 17:00–20:00 CET peak, PDF p. 16) and weekend
  decline in returns/volume/volatility (Figs. 8–10, PDF pp. 16–18) — venue
  corroboration for the already-recorded hour-of-day stratification and seasonality
  items, nothing added; (2) interpretation caution: the "24/7 algorithmic trading
  impact is rather negligible" headline (PDF pp. 19–20) is a SHAPE inference from
  ~1%-R² smooths, in one two-month vacation window, at 5-minute grain, with no direct  algorithm-share measurement — agent-mix statements may never be imported from
  seasonality shape alone, and the 2018-spot reading does not date 2024–25 perps in
  either direction (regime-dating the session-6 fragility premise honestly);
  (3) the on-chain/off-chain passage (PDF p. 19) reinforces the proxy-refusal layer:
  on-chain variables are not admissible substitutes for L2 book state; (4) Table 1
  (PDF p. 12): near-zero mostly-negative first-order return autocorrelation with
  strongly positive absolute/squared-return autocorrelation at 5-minute grain —
  consistent with the compression premise's volatility-clustering motivation as
  CONTEXT ONLY (different grain, era, venue; never claim support). The counterfactual
  named both laundering directions this paper invites: its human-driven headline
  could have been read as undermining the L2 motivation, and its speculative
  false-positive-cascade passage (PDF p. 19) could have been read as criticality
  evidence for the trigger line — the no-empirical-claim-from-papers rule prevented
  both.

Ratification queue after this session: SIXTEEN candidate sharpenings (unchanged by
this session — no sharpening was warranted by this source; the sixteen include
concurrent slot 6's size-state persistence comparator), zero armed. T1 remains armed awaiting
the owner's word; the blocked list stays blocked. Deep-read queue: the next UNREAD
triage entry is unchanged — "Price-Aware Automated Market Makers: Models Beyond
Brownian Prices and Static Liquidity" (score 39, already on the library text shelf);
with the session-9 triage-audit flag on record, rank is a candidate reading, and the
owner's library policy governs when they diverge. Nothing measured, no kill line
moved, nothing armed, nothing trades live.

## 22. Null-time session 18 (2026-11-18): deep-read session 16 — the price-aware AMM quoting paper graded pure theory, zero data; both laundering directions named

- **Library deep-read session 16** (the standing queue's top UNREAD pointer, consumed by
  this session — declared as such, not a parallel slot):
  `paper/research/library/2026-11-18_price_aware_amm_deep_read.md`
  on Bergault, Bertucci, Bouba, Guéant & Guilbert, "Price-Aware Automated Market Makers:
  Models Beyond Brownian Prices and Static Liquidity" (arXiv:2405.03496v3, 2024; pure
  HJB/quadratic-Hamiltonian quoting theory for a price-aware AMM under Heston-Bates,
  Stein-Stein-with-jumps, linear Markovian Hawkes and Z-Hawkes price models, plus
  Hawkes-vs-MMPP liquidity modeling; "No data involved in this study", PDF p. 20).
  Triage: score 39, xd1af5a, read as the session's standing-pointer read.
- Grade: NO kill line changed; NO new candidate sharpening. The paper is quoting-strategy
  engineering with no empirical content, and per the standing rule it is recorded as
  context only, never program input. Numbered findings, page-cited in the note: (1)
  [reinforcing] the branching ratio n used matter-of-fact as "the percentage of price
  moves that are purely endogenous" (PDF p. 11) — corroborates that the endogeneity-share
  reading is the field default, which is exactly why the queued estimator-discipline items
  (estimator-at-scale-W with the mean-variance cross-check, bootstrap-CI and
  boundary-solution rules, the W-ladder) govern; (2) [reinforcing] the control literature's
  own honest label for the exponential kernel — "Power law kernels may be more realistic
  than exponential ones, but they do not lead to Markovian setups" (footnote 8, PDF p. 11)
  — first-principles support for the queued ACF-shape kernel-validity gate and the
  kernel-form-declared-with-the-spec discipline; (3) [reinforcing] the Z-Hawkes section
  (PDF pp. 13-15) names the sign-feedback alternative family (Zumbach effect, xi_t driven
  by sign(eta)) that linear exponential-kernel Hawkes cannot represent — concretizes the
  already-queued kernel-family control; (4) [interpretation caution] the
  curse-of-dimensionality verdict on Hawkes liquidity models (PDF pp. 16-18) is a
  control-theoretic solvability statement, NOT a statistical-validity claim, and licenses
  nothing against C8's trigger (which estimates an intensity and solves no HJB); the MMPP
  alternative (p = 2-3 states, PDF p. 17) is a control-side discretization, not
  regime evidence; (5) [interpretation caution] a price-aware AMM manufactures part of its
  own flow endogeneity (markup-dependent arrival intensities, PDF p. 4; markups reacting
  to state, PDF pp. 13-19) — binds only if venue scope ever widens to AMM/on-chain pools,
  since the gated Tardis LOB data contains no AMM quoting loop; (6) [source-quality note]
  arXiv v3, zero data, two Swaap Labs co-authors and funding in partnership with Swaap
  Labs (PDF pp. 1, 20), two equation typos observed (Eq. 15, PDF p. 10, nu-for-sigma in
  the jump integral; Eq. 20, PDF p. 11, duplicated H^{1,0}H^{1,0}); published version to
  be checked before formal citation.
- The counterfactual, named both ways in the note: the Hawkes-for-control rejection could
  have been laundered into an anti-Hawkes authority against the C8 trigger (wrong problem
  class), and the paper's plain n-as-endogeneity-share parameter could have been laundered
  into a license to read threshold crossings as reflexivity without estimator discipline.
  The no-empirical-import rule blocked both; nothing measured, nothing armed.
- Inaccessible/blocked status: none this session; the extract was present, page-marked and
  complete (21 pp.).

  Ratification queue after this session: SIXTEEN candidate sharpenings (unchanged — no
  sharpening was warranted by this source), zero armed. T1 remains armed awaiting the
  owner's word; the blocked list stays blocked. Deep-read queue: the next UNREAD triage
  entry is now Horst & Xu, "Functional Limit Theorems for Hawkes Processes"
  (arXiv:2401.11495v3, slug x47738d, score 38, already on the library text shelf); with
  the session-9 triage-audit flag on record, rank is a candidate reading, and the owner's
  library policy governs when they diverge. Nothing measured, no kill line moved, nothing
  armed, nothing trades live.

## 22b. Null-time session 18 corrigendum (machine-side, 2026-11-18): the session-18 log push was silently truncated; the full tail restored byte-exact

- What happened: the squash merge of PR #168 (session 18) carried a silently TRUNCATED
  copy of this log file to main. The composed full log (base at commit 8e6771d5 plus the
  session-18 entry) was ~74 KB; the file-push path delivered only the first 63,998 bytes
  without any error, cutting the text mid-sentence inside session 16's entry ("## 20") and
  deleting the end of that entry along with two entries that had legitimately landed
  earlier: "## 21. Null-time session 17" (merged with CI green via PR #167 at commit
  8e6771d5) and the freshly composed "## 22. Null-time session 18" entry. Everything else
  in the session-18 merge was correct and landed intact; verified byte-level: the
  deep-read note paper/research/library/2026-11-18_price_aware_amm_deep_read.md (144
  lines, complete through its standing caveat) and docs/DECISIONS_PENDING.md (untouched,
  as the session queued nothing).
- What is restored, byte-exact: the tail of entry ## 20 from the cut point onward, the
  full entry ## 21 exactly as it stood at commit 8e6771d5, and entry ## 22 exactly as
  composed for session 18 (standing-pointer read of the score-39 queue top; grade NO
  kill line change, NO sharpening; queue unchanged at SIXTEEN; next UNREAD pointer
  Horst & Xu). The two versions were verified identical over their common 63,998-byte
  prefix before restoration, and the restored file is sha256-verified against the
  composed original. No existing character of any entry was edited; nothing was
  renumbered; this corrigendum is appended, per the honest-error protocol.
- Root cause and the new machine-side rule: the truncation was invisible at composition
  time because the integrity guard ran on the full pre-push tree (which was correct),
  while the bytes actually delivered to the push were truncated upstream of the push.
  The session's post-merge verification checked the notes directory instead of this log
  file, so the defect survived into the merge — a verification failure, owned here.
  Machine-side rule adopted from this point on: every log or ledger push is verified at
  the raw SHA of the pushed branch BEFORE the PR is merged, byte-compared against the
  composed intended file (length and sha256 plus tail line); a push that fails the
  comparison is re-issued, never merged on trust.
- What was NOT affected: no claim, no kill line, no test, no data, no ratification-queue
  count. The corrupted content was history text only. Ratification queue after this
  corrigendum: SIXTEEN candidate sharpenings (unchanged), zero armed. T1 remains armed
  awaiting the owner's word; the blocked list stays blocked. Nothing measured, no kill
  line moved, nothing armed, nothing trades live.

## 23. Null-time session 19 (2026-11-18): deep-read session 17 — the near-critical regime-disclosure rule for the branching-ratio trigger; the log-restoration corrigendum landed first

- **Restoration first (machine-side, this session)**: the ## 22b corrigendum above was
  composed and landed by this session as PR #169 (squash-merged as df5c852c, CI both
  green): main's log restored byte-exact to 77,253 bytes, sha256-verified at the pushed
  branch's raw SHA BEFORE the merge and re-verified at the merge SHA after; the new
  standing rule (every log push verified at the pushed branch's raw SHA BEFORE its PR
  merges, never merged on trust) held on its first live use. No claim, kill line, test,
  data, or queue count was affected by the incident or the restoration.
- **Library deep-read session 17** (the standing queue's next UNREAD pointer, score 38,
  x47738d, consumed here after session 18 took the score-39 top; NB: this paper was also
  the pre-assigned burst slot 02 paper, that slot produced no repo trace, the consumption
  is declared here, and a late slot-02 landing of the same slug would be superseded per
  the PR #164/#165 pattern):
  `paper/research/library/2026-11-18_functional_limit_theorems_deep_read.md`
  on Horst & Xu, "Functional Limit Theorems for Hawkes Processes"
  (arXiv:2401.11495v3, math.PR, 2024; DFG CRC/TRR 388 B02; theory-only, no data).
  Read: main results Sections 1-2 (PDF pp. 1-21) in full detail; proofs Sections 3-6
  (PDF pp. 21-61) skimmed, Remarks 2.15/2.17 noted; the paper contains no empirical
  content. Grade: NO kill line changed. ONE candidate sharpening queued, PENDING OWNER
  RATIFICATION: **the near-critical regime-disclosure rule** — the long-run behavior is
  fully determined by the offspring mean m AND the child-event dispersion
  sigma = integral s*phi(s) ds (Abstract, PDF p. 1); every exponential kernel (and
  mixture) has finite sigma, so exponential-family criticality is ALWAYS weak
  criticality, where functional limit theorems do NOT hold and the rescaled intensity
  converges to a CIR process WITHOUT mean reversion (Theorem 2.10, PDF p. 14; the
  Jaisson-Rosenbaum near-unstable contrast, PDF pp. 2, 4), while the long-range-dependence
  limits belong exclusively to the strongly critical heavy-tailed regime the declared
  family cannot reach (Theorems 2.14/2.16, PDF pp. 15-16; Remark 2.15, PDF p. 16;
  Sec. 1.2.4, PDF p. 5). Pre-declaration text: a branching-ratio trigger bar fired from
  n-hat inside the pre-declared near-critical band must disclose the limit regime of
  its declared fitted class (exponential => weakly critical => mean-reverting-CIR
  asymptotics, NOT the strongly-critical long-memory story); reading language importing
  criticality-with-long-memory from outside the declared kernel family is inadmissible;
  non-disclosure makes the bar inadmissible. Harder to pass: the near-critical band
  gains a mandatory stated-regime clause the old protocol did not have. Reinforcing,
  no new item: the classical FCLT's sharp boundary Psi_1(t)/sqrt(t) -> 0
  (Theorem 2.9, PDF pp. 12-13) holds trivially for exponentials and the convergence-rate
  constant is exactly zero for the exponential kernel (Theorem 2.12 + Example 2.1,
  PDF p. 15), so the declared family stays in the classical regime and the existing
  day-block inference discipline stands; subcritical increments are always
  asymptotically independent, long-range dependence impossible in the subcritical
  regime regardless of kernel tail (Theorem 2.8, PDF p. 12); any kernel-family widening
  must re-run the regime check; increment correlations at weak criticality decay
  ~C/T (PDF p. 5). Laundering directions named: (1) importing the strongly-critical
  LRD Gaussian limit as the "critical market" narrative smuggles in heavy-tailed-kernel
  theory the declared family structurally cannot reach; (2) reading "no FCLT at weak
  criticality" as "the trigger cannot work near n = 1" applies a long-run asymptotic
  statement about the PROCESS to the finite-window ESTIMATOR distribution the trigger
  actually reads; the two are not the same object. Source quality: arXiv v3,
  theory-only, DFG-funded; typos noted ("Strongly critical Hakes processes", PDF p. 5;
  "bee seen", PDF p. 13); published version to be checked before formal citation.

Ratification queue after this session: SEVENTEEN candidate sharpenings (the sixteen
standing plus the near-critical regime-disclosure rule joined 2026-11-18), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays blocked. Deep-read
queue: the next UNREAD triage entry is "Ergodicity and diffusivity of Markovian order
book models: a general framework" (score 37, xfccac8, already on the library text
shelf); with the session-9 triage-audit flag on record, rank is a candidate reading,
and the owner's library policy governs when they diverge. Nothing measured, no kill
line moved, nothing armed, nothing trades live.

## 24. Null-time session 20 (2026-11-18): deep-read session 18 — the Markovian order-book ergodicity paper graded pure theory, default grade held

- **Library deep-read session 18** (the standing queue's next UNREAD pointer, score 37,
  xfccac8, consumed here; the paper was also the pre-assigned burst slot 04 paper, that
  slot produced no repo trace, the consumption is declared here, and a late slot-04
  landing of the same slug would be superseded per the PR #164/#165 pattern):
  `paper/research/library/2026-11-18_markovian_orderbook_ergodicity_deep_read.md`
  on Huang & Rosenbaum, "Ergodicity and diffusivity of Markovian order book models:
  a general framework" (arXiv:1505.04936, q-fin.TR; theory-only, no data). Read:
  Sections 1-5 in full detail (PDF pp. 1-18); proofs Section 7 skimmed for structure
  (PDF pp. 18-25, Lyapunov/Meyn-Tweedie machinery, no interpretive content). Grade:
  NO kill line changed. NO new candidate sharpening. Findings, page-cited:
  (1) [reinforcing] the macroscopic limit of the entire class is Brownian motion via
  strong mixing of stationary price increments (Theorems 4.1/4.2, Equation 7, PDF
  p. 13) — inside the class there is no long-memory macro price, and any claim that
  a microscopic LOB feature survives to macro scale is a finite-window pre-limit
  claim, exactly what C1-L2's short-horizon benchmarking already tests; nothing here
  licenses relaxing the OFI-benchmark family. (2) [reinforcing] ergodicity is earned,
  not assumed: it is bought with a uniform negative-drift condition on every queue
  above a threshold (Assumption 3.3, Example 2's simple form f - g < -r, PDF
  pp. 10-11), and the stylized LOB shape is an invariant-distribution phenomenon
  (PDF p. 3) — depth-shape readings are licensed only under a drift condition of this
  kind. (3) [reinforcing] the paper's own boundary: a non-Markovian (self-exciting)
  market-order component would force a complete revision of the approach except for
  very specific cases, exponential Hawkes named (Conclusion, PDF p. 18) — the same
  boundary met in deep-read 17, two independent frameworks placing the exponential
  kernel exactly at the edge of tractability, which supports the declared kernel
  family staying declared and reinforces the queued near-critical
  regime-disclosure item's scope. (4) [interpretation caution] the reference price is
  latent (explicitly not necessarily the mid, PDF pp. 3-4) and book updates carry the
  price with a delay at state-dependent rates u/d (PDF pp. 6-9): instantaneous
  event-to-price attribution is barred in this class; C1-L2's existing point-in-time
  lag discipline is consistent cover, not new permission. (5) [source-quality note]
  internal date discrepancy: title page "September 17, 2018" vs arXiv v1 stamp
  "19 May 2015" (PDF p. 1), acquisition index records v1/2015; flagged, not resolved;
  published version to be checked before formal citation. Laundering directions
  named: (1) INTO — quoting the diffusive limit as proof that microstructure always
  washes out, so short-horizon flow edges "cannot exist", is an asymptotic statement
  about a model class under fitted drift conditions, not about finite-window
  real-tape predictability; barred as a kill argument against C1-L2's own tests.
  (2) OUT — reading the ergodicity theorems as "the LOB state is stationary in data,
  so depth-regime features are always admissible": ergodicity is conditional on
  Assumption 3.3's drift, which the tape never checks for free; without it, an
  "equilibrium depth regime" reading is unlicensed. Standing caveat: theory-only,
  large-tick design (K of order 10, PDF pp. 2-3), boundary distributions free
  parameters (PDF p. 7) so the theorems narrow nothing about which specific model
  generated any observed tape; no falsification content for C1-L2 or C8.

Ratification queue after this session: SEVENTEEN candidate sharpenings (unchanged),
zero armed. T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue: the next UNREAD triage entry is "Simulating and analyzing a
sparse order book: an application to intraday electricity markets" (score 37,
x3ff3a4, on the library text shelf; also the pre-assigned burst slot 04 paper, no
slot-04 trace exists); with the session-9 triage-audit flag on record, rank is a
candidate reading, and the owner's library policy governs when they diverge.
Nothing measured, no kill line moved, nothing armed, nothing trades live.

## 24b. Null-time session 20 corrigendum (2026-11-18): the slot-04 attribution in entry ## 24 is wrong

- What is wrong: entry ## 24 says the Huang-Rosenberg ergodicity paper "was also
  the pre-assigned burst slot 04 paper, that slot produced no repo trace". That is
  incorrect. The burst slot 04 assignment was "Simulating and analyzing a sparse
  order book: an application to intraday electricity markets" (score 37, x3ff3a4),
  which entry ## 24's own closing pointer correctly names as the slot-04 paper. The
  burst slot 02 assignment was the Horst-Xu FLT paper (entry ## 23, correct). NO
  burst-slot assignment is on record for the Huang-Rosenberg ergodicity paper; its
  read was the standing queue's next UNREAD pointer (score 37, xfccac8) and nothing
  more.
- What is corrected: the erroneous clause in entry ## 24 is retracted here; the
  wrong text is left unedited above, per the append-only honest-error protocol.
  Nothing else in entry ## 24 is affected: the grade (NO kill line changed, NO new
  candidate sharpening), every page citation, the queue count (SEVENTEEN candidates,
  zero armed, unchanged), and the next-UNREAD pointer all stand as written. The
  PR #171 description and its squash-commit message carried the same wrong clause;
  git history is immutable, so this corrigendum is the correction of record.
- Nothing measured, no kill line moved, nothing armed, nothing trades live.

## 25. Null-time session 21 (2026-11-18): the exploratory channel RATIFIED by the owner; probe E1 queues the volume-conservation reconstruction-admissibility rule

- **Protocol event (owner's word, the only trigger, received in chat
  2026-11-18)**: the exploratory channel is RATIFIED. The owner's directive
  "Go for it while we wait for l2" adopts the proposal as stated: give
  serendipity a declared channel instead of making it smuggle. Channel
  protocol: `docs/exploratory_channel.md`. In force: one exploratory block
  may accompany a session, announced and tagged [exploratory]; probes may
  read and derive anything but may not measure, arm, touch any kill line, or
  carry evidentiary weight; every probe gets a numbered note under
  `paper/research/exploratory/` and every probe counts in the
  multiple-testing discipline; nothing glimpsed exploratorily may ever be
  cited as confirmatory until it survives a test registered AFTER the
  exploration; output goes through the normal PENDING OWNER RATIFICATION
  gate; the owner may revoke the channel at any time.
- **[exploratory] Probe E1**: "volume conservation as a depth-reconstruction
  admissibility rule", `paper/research/exploratory/2026-11-18_E1_volume_conservation.md`.
  Anchors: the owner's question about volume-flow physics and conservation
  mathematics (chat, 2026-11-18), the Huang-Rosenbaum moving-frame
  representation (deep-read 18), own derivation of the event-to-flux map.
  The honest import from the finite-volume method is bookkeeping, not
  metaphor: on a fixed absolute price grid the tape IS q-dot and the balance
  law IS the exact discrete integral form — cell storage change equals
  summed signed event fluxes plus DECLARED boundary terms (beyond the
  K-level window) plus DECLARED source terms (hidden liquidity,
  administrative changes, per-venue map registered before any run). NO
  library paper was consumed by this session: it is a protocol + exploration
  session; the standing next-UNREAD pointer is unchanged.
- **Grade: NO kill line changed. ONE candidate sharpening queued, PENDING
  OWNER RATIFICATION: the volume-conservation reconstruction-admissibility
  rule** — any depth reconstruction used in a C1-L2 (or C8 L2-arm)
  measurement must pass the flux-differencing identity per level per window,
  within a tolerance and source-term budget BOTH pre-registered before the
  first L2 run and calibrated on a calibration window DISJOINT from every
  feature-evaluation window; failing windows are inadmissible and their
  failure log travels with the measurement. Harder to pass: windows that
  would today silently enter a measurement with corrupted depth (double-
  counted executions, feed gaps, timestamp misalignment, wrong-side
  assignment) are excluded before any statistic is computed. It defines no
  signal, changes no kill line, and is validation machinery only
  ([exploratory] provenance, channel E1).
- **Both laundering directions named**: (1) INTO — the physics-flavored
  vocabulary of conservation laws may never be cited as support for any
  flow feature; the rule is bookkeeping, and bookkeeping earns nothing
  predictive; (2) OUT — a passing identity may never be read as evidence of
  data quality beyond the window checked or as validation of the C1-L2
  signal itself; it licenses admissibility of a window, nothing more.

Ratification queue after this session: EIGHTEEN candidate sharpenings (the
seventeen standing plus the volume-conservation reconstruction-admissibility
rule joined 2026-11-18 via exploratory probe E1), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked. Deep-read queue:
the next UNREAD triage entry is unchanged, "Simulating and analyzing a sparse
order book: an application to intraday electricity markets" (score 37,
x3ff3a4, burst slot 04's assignment); with the session-9 triage-audit flag on
record, rank is a candidate reading, and the owner's library policy governs
when they diverge. Nothing measured (no data touched; L2 still awaited), no
kill line moved, nothing armed, nothing trades live.

## 26. Null-time session 22 (2026-11-18): deep-read session 19 — the sparse order book simulator read; the deterministic-clock null arm queued for the branching-ratio trigger

- **Library deep-read session 19** (the standing queue's next UNREAD
  pointer, score 37, x3ff3a4, consumed here; per corrigendum ## 24b this
  slug IS the burst slot 04 assignment, so slot 04 is consumed consistently
  by this same read):
  `paper/research/library/2026-11-18_sparse_orderbook_electricity_deep_read.md`
  on Bergault & Cognéville, "Simulating and analyzing a sparse order book:
  an application to intraday electricity markets" (arXiv:2410.06839v1,
  q-fin.TR, 2024; EPEX Spot German/French intraday electricity, 2021, hour
  products; a simulation paper about a market the programme does not trade).
  Read against the ONE question. **Grade: NO kill line changed. ONE
  candidate sharpening, PENDING OWNER RATIFICATION: the deterministic-clock
  null arm for the branching-ratio trigger** — the paper's simulated books
  display strong event clustering with ZERO self-excitation, all of it
  generated by deterministic calendar-time intensities
  (lambda_M(t,S) = lam_bar_M e^{-kM(T-t)} e^{-bM S} and its siblings, PDF
  pp. 15-16; the Samuelson ramp documented for ALL interactions, PDF p. 4
  Fig. 2), and those clock-driven books still match the empirical spread
  distributions (PDF pp. 18-19) while provably missing the extreme events
  (PDF p. 19: "the main drawback of our Poisson model is the lack of
  extreme events"). Pre-declaration text: no branching-ratio trigger
  reading is admissible unless the apparent branching exceeds an
  inhomogeneous Poisson null whose deterministic intensity carries the same
  calendar-clock profile (hour-of-day, session segments), profile fitted
  on calibration windows DISJOINT from evaluation; the clock-explained
  fraction is reported and clock-explained windows contribute no firing
  (neither positive nor negative). Harder to pass: the standing gates do
  not separate clock from excitation — the shuffled-arrival placebo
  destroys both together, the ACF-shape gate is consistent with an
  inhomogeneous Poisson (independent disjoint-interval counts keep the ACF
  flat or decaying), and a mean-variance-style branching estimate is
  inflated by cross-window clock variance alone (Var(Lambda) > 0 raises
  n-hat above its true value of zero); a bar that survives the
  bootstrap-band, kernel-family, ACF-shape, and wash-audit gates can still
  die here. It generalizes the recorded hour-of-day stratification caution
  (deep-read 3) from an estimation-window caution into an explicit null
  arm, and tightens only the branching-ratio trigger family; no C1-L2
  text moves. Findings, page-cited: reinforcing, no new item — beyond-K
  boundary limits are SYNTHESIZED draws, harmless only around inner limits
  and only for K large enough (PDF pp. 9-10), independent support for the
  E1 declared-boundary-term discipline and the distance-grid
  sign-invariance rule; interpretation caution — the model has NO partial
  cancellations (a partial cancel is approximated as full cancel plus a
  smaller reinsertion at the same limit, PDF p. 9), so depth persistence
  features must never conflate volume reduction at an occupied level with
  level disappearance (the size-state persistence comparator's territory);
  reinforcing — signature-plot model checking (realized volatility depends
  on the sampling step until it stabilizes, PDF pp. 19-20) and the printed
  simulator failure (underdispersed outputs, PDF p. 19) support the
  pre-registered sampling-scale discipline and the negative-result
  culture; source-quality note — arXiv v1 only, one author EDF R&D staff,
  electricity-only scope, symmetric bid/ask by calibration choice (PDF
  p. 15), least-squares on suggested functional forms (PDF pp. 15-16),
  published version to be checked before formal citation. Laundering
  directions named: INTO — the paper's "Poisson reproduces the spread
  distributions" may never be cited to weaken excitation requirements or
  to build flat, clock-free nulls, and its "Hawkes would fix the tails"
  sentence is a discussion-section proposal, not evidence that real
  markets are self-exciting; OUT — the deterministic-intensity
  construction is a model of one electricity market, not a measurement of
  our tape, and may never be cited as proof that clustering in our
  windows is clock-driven; only the registered null arm may say that,
  window by window.

Ratification queue after this session: NINETEEN candidate sharpenings (the
eighteen standing plus the deterministic-clock null arm for the
branching-ratio trigger joined 2026-11-18 via deep-read 19), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays blocked.
Deep-read queue: the next UNREAD triage entry is "Hawkes-Driven OTC Market
Making: Volterra-Riccati Approximation" (score 37, xa868e3, the burst slot
05 assignment); with the session-9 triage-audit flag on record, rank is a
candidate reading, and the owner's library policy governs when they diverge.
Nothing measured, no kill line moved, nothing armed, nothing trades live.

## 27. Null-time session 23 (2026-11-18): deep-read session 20 — the Hawkes-driven OTC market making paper; the latent-common-cause robustness arm queued for the branching-ratio trigger

- **Library deep-read session 20** (the standing queue's next UNREAD
  pointer, score 37, xa868e3, consumed here; also the burst slot 05
  assignment, consumed consistently by this same read):
  `paper/research/library/2026-11-18_hawkes_otc_market_making_deep_read.md`
  on Barzykin, "Hawkes-Driven OTC Market Making: Volterra-Riccati
  Approximation" (arXiv:2608.02002v2, q-fin.RM, 2026; sole author HSBC
  practitioner, views his own; HSBC proprietary spot-FX RFQ data, three
  pairs, three years; an OTC control paper about a market the programme
  does not trade). Read against the ONE question. **Grade: NO kill line
  changed. ONE candidate sharpening, PENDING OWNER RATIFICATION: the
  latent-common-cause (Markov-modulated-baseline) robustness arm for the
  branching-ratio trigger** — the paper states the confound precisely:
  correlated requests "may be reactions to a common unobserved cause ...
  If such exogenous variation is omitted from the baseline intensity, a
  fitted Hawkes model may absorb part of it into the excitation kernel
  and thereby produce a large branching ratio" (PDF p. 2), and its
  conclusion names the discriminating test, "compare pure Hawkes dynamics
  with latent-factor or Cox specifications" (PDF pp. 21-22); its own
  Table 1 shows fitted branching 0.86-0.90 in major FX pairs on three
  years and over 5*10^5 filtered events AFTER deterministic seasonality
  is designed out (PDF pp. 3-5) — exactly the magnitude a naive reading
  would celebrate as near-critical reflexivity, from an author who
  explicitly refuses that reading. This confound is NOT the
  deterministic-clock one queued at deep-read 19 (an observed calendar
  profile is not a stochastic latent driver) and none of the standing
  gates addresses it. Pre-declaration text: every window whose fitted
  branching fires the trigger bar must be re-estimated under a
  registered latent-baseline enrichment — the two-state Markov-modulated
  background already built into C8's MMHP structure — with the baseline
  form pre-registered before the first L2 run; if the excitation mass
  attributed to endogenous branching drops below the bar once the latent
  state is modelled, the window contributes no firing (neither positive
  nor negative); both readings are reported in the register and replace
  any single-number narration. Harder to pass: a window that survives
  every standing gate can still die here, because apparent
  self-excitation absorbed from an omitted common driver is not
  reflexivity. Tightens only the branching-ratio trigger family; no
  C1-L2 text moves. Findings, page-cited: reinforcing, no new item —
  independent practitioner corroboration of the deep-read-19 clock null
  (kernel estimated only in seasonality-adjusted activity time because
  calendar time "would ... confound deterministic seasonality with
  residual serial dependence", PDF pp. 3-4; all rates in one declared
  clock, variance rates included, PDF pp. 4-5), reinforcing the flow-clock
  scale-constant rule; reinforcing — high branching fits are commonplace
  and specification-sensitive (fitted 0.86-0.90 in data, PDF p. 4; 0.92 as
  a synthetic stress regime, PDF p. 14), supporting the near-critical
  regime-disclosure rule's disclosed-regime requirement over
  number-alone narration; interpretation caution — fitted excitation is
  event-set-relative (aggressive pre-fit filters and the
  request-vs-conversion event convention, PDF pp. 3-6), so the trigger's
  event-stream definition and filters must be pre-registered before the
  first L2 run and later changes are new tests, not re-estimates;
  source-quality note — single-author HSBC practitioner paper, arXiv v2,
  proprietary data, no well-posedness theorem (numerical validation only,
  PDF pp. 14-15), market-making results are execution-strategy
  engineering outside programme scope, published version to be checked
  before formal citation. Laundering directions named: INTO — Table 1's
  0.86-0.90 may never be imported as calibration for the C8 trigger bar
  or as evidence that real markets sit near criticality, and the paper's
  regret tables and quote-skew formulas are a dealer's control problem,
  never programme input; OUT — the confound disclaimer may never be read
  backwards as "fitted branching is meaningless": the paper's own
  validation hierarchy shows the fitted memory to be the economically
  relevant state, and the confound limits what a fired bar may CLAIM, not
  whether the forecast content exists.

Ratification queue after this session: TWENTY candidate sharpenings (the
nineteen standing plus the latent-common-cause robustness arm for the
branching-ratio trigger joined 2026-11-18 via deep-read 20), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue: the next UNREAD triage entry is "Limit Order
Book Dynamics and Order Size Modelling Using Compound Hawkes Processes"
(score 34, x798515); with the session-9 triage-audit flag on record, rank
is a candidate reading, and the owner's library policy governs when they
diverge. Nothing measured, no kill line moved, nothing armed, nothing
trades live.
## 28. Null-time session 24 (2026-11-18): deep-read session 21 — the compound Hawkes order-book size-modelling paper graded default, no sharpening; PR #173's dashboard audit landed by supersession

- **Protocol/maintenance event** — PR #173 ("dashboard audited and
  refreshed", branch vibe/dashboard-refresh-984be8) resolved this
  session. Its audit was verified row by row against
  docs/ledger.html and the record, not taken on faith: the L0
  snapshot-coverage decision was MADE 2026-11-16 by the owner
  (amendment on file at
  paper/research/l0_gate/amendment_2026-11-16.md), T2 tested-fail with
  its kill line FIRED under the owner-authorized 2026-11-16 run, T1
  booked sign-inverted; the old pending list carried stale rot. The
  branch's base had diverged from main (both sides rewrote
  docs/DECISIONS_PENDING.md across sessions 21-23), GitHub's
  update-branch refused with a merge conflict, this connector has no
  force-rebase or branch-replace capability, and adding commits
  cannot clear a three-way conflict — so supersession per the
  standing PR pattern was applied. The audit's content landed via PR
  #177 as a single clean diff on current main (squash 623eeefd),
  with ONE correction: the audit's stale approximate queue line
  ("~17+ across 18 deep-reads") restored to the exact count, twenty
  candidates through 20 deep-reads plus probe E1, zero armed — the
  queue line is the owner's ratification interface and may never be
  approximate. Integrity guard clean on the substituted tree; PR
  #177's CI green (test, engine); post-merge blob verified
  byte-identical to the intended resolution (sha256
  6345fabee0ff1dfab014f7dea43dfc95f7c9dba247976ec87c7d50c98ffe0907,
  3,354 bytes); PR #173 closed with the supersession recorded in
  line. docs/DECISIONS_PENDING.md on main is now the audited
  thirty-second dashboard. Nothing measured, no kill line touched,
  nothing armed in any of this.

- **Library deep-read session 21** (the standing queue's next UNREAD
  pointer, score 34, x798515, consumed here):
  `paper/research/library/2026-11-18_compound_hawkes_lob_sizes_deep_read.md`
  on Jain, Firoozye, Kochems, Treleaven, "Limit Order Book Dynamics
  and Order Size Modelling Using Compound Hawkes Process"
  (arXiv:2312.08927v5, 2023, revised 2024; UCL and J.P. Morgan Chase
  & Co., funded by JPMC with a dealer disclaimer; a 12-dimensional
  compound Hawkes simulator for the top of a NASDAQ equity order
  book with calibrated order-size distributions). Read against the
  ONE question. **Grade: NO kill line changed. NO new candidate
  sharpening.** Default grade. The paper's mechanisms are worked
  exhibits of rules already standing in the queue, and the burden of
  proof for a sharpening was not met. Findings, page-cited:
  reinforcing, no new item — the d-dimensional worked example of the
  boundary-solution pathology, queued at deep-read session 5: their
  fitted kernels "occasionally violate" the stationarity constraint
  and are silently rescaled by "multiplying all the kernels by a
  regularizing term to cap the eigenvalue at 1" (PDF p. 6), landing
  the fit exactly on the constraint boundary; under the queued rule
  such a reading is MISSING, not high, not near-critical.
  Reinforcing, no new item — the exogenous share of fitted excitation
  is an estimator-pipeline PRODUCT (cut-off grid, sign-uniformity  constraint, a 0.01-norm threshold zeroing 79 of 144 kernels, PDF
  p. 7, inhibitory flooring, and the post-hoc rebuild of exogenous
  intensity because the raw estimate is "massively overestimated",
  PDF p. 6), a second named exhibit for the near-critical
  regime-disclosure rule: only the disclosed estimate chain is a
  regime. Reinforcing, no new item — a seasonality-naive null is a
  broken null: their Poisson baseline, carrying no U-shape, produces
  a flat signature plot and wholesale shape failures (PDF pp. 8-9),
  so the queued deterministic-clock null arm and the hour-of-day
  stratification rule are corroborated, not amended; any null must
  carry the declared deterministic seasonality or fires for the
  wrong reason. Reinforcing, no new item — time-only excitation is
  formally silent about size/marks: their size-independence
  postulate rests on weak evidence they concede ("albeit with weak
  evidence", Hoeffding 0.00068, one stock, PDF p. 11), their own
  market-impact study then exposes the artifact, impact driven by
  trade COUNT rather than volume, "counter-intuitive to the real
  world phenomenon of adverse selection" and named "a potential
  missing piece" (PDF p. 10), and constant-order-size simulation
  overestimates volatility by ~100x (PDF pp. 8-9) — a worked exhibit
  for the queued size-state persistence comparator: a memory
  measured on event counts alone may not be narrated as volume-flow
  or impact fact. Interpretation caution — in-spread limit-order
  intensity scales empirically as (s-1)^beta, beta around 0.75 for
  their stock (R-squared 0.85, PDF p. 11, Appendix B), so any future
  near-touch reconstruction feature must declare its spread-state
  normalization before the first L2 run or drift with the spread
  distribution, not information flow; reading discipline only, no
  queue change. Source-quality note — practitioner preprint, arXiv
  v5, primary calibration one medium-tick stock (AAPL 2019,
  NASDAQ), the authors themselves report their own model unsuitable
  or misfitted for small-tick names (severely underestimated
  spreads and volatility for TSLA and AMZN, left-tail misfit for
  INTC, PDF pp. 10-11); published version to be checked before
  formal citation. The killed-if-wrong section stands: had a
  simulator's fitted matrices or a homogeneous null ever stood in
  for a registered test, these artifacts (100x volatility
  overestimate, silently rescaled kernels, seasonality-free null
  failures) would have fired or killed on machinery, not markets —
  the library-is-ammunition rule and nothing-measured are what
  prevented it. Standing caveat recorded: six top-of-book queues
  only, order sizes assumed stationary and condition-independent
  ("quite strong", PDF p. 4), the impact study is simulator output,
  and its TWAP/child-order machinery is execution-strategy
  engineering outside programme scope, never programme input.
  Laundering directions named: INTO — the paper's calibrated kernel
  norms, beta exponents, U-shape bins, and impact concavity
  constants may never be imported as calibration or priors for the
  C8 trigger bar or any reconstruction tolerance; OUT — the
  artifact confessions may not be read backwards as "Hawkes
  memory is fake": the failures are about marks and applicability
  (size-silence, small-tick names), not about the existence of
  time-excited clustering; the limits bind what a fitted number may
  CLAIM, not whether the memory content exists.

Ratification queue after this session: TWENTY candidate sharpenings,
unchanged (deep-read session 21 earned none; the twenty standing are
those enumerated through deep-read session 20 plus probe E1), zero
armed. T1 remains armed awaiting the owner's word; the blocked list
stays blocked. Deep-read queue: the next UNREAD triage entry is
"Returns and Order Flow Imbalances: Intraday Dynamics and
Macroeconomic News Effects" (score 34, x5459dc); with the session-9
triage-audit flag on record, rank is a candidate reading, and the
owner's library policy governs when they diverge. Nothing measured,
no kill line moved, nothing armed, nothing trades live.

## 29. Null-time session 25 (2026-11-18): the three deferred engineering events booked — the compound Hawkes engine (PR #179), its site dashboard (PR #180), the nav link (PR #181)

Each of the three commits disclosed "log entry deferred to the next
null-time session per append-only protocol"; this is that session. All
three were owner-ordered engineering builds following deep-read
session 21 (the compound Hawkes order-book size-modelling paper,
arXiv:2312.08927v5, graded default NO sharpening there). They are
demonstration infrastructure. Nothing in them measures anything, and
the synthetic data is the only data any of them ever touched.

- **Protocol/maintenance event — PR #179, the compound Hawkes
  order-flow engine.** From-scratch build, all synthetic, no programme
  dataset touched at any step: `src/ofhawkes.py`, a 12-dimensional
  compound Hawkes point process driving a six-queue top-of-book
  simulator, in the paper's own dimension order (limit, cancel and
  market orders at the touch, one tick deep, and in-spread, both
  sides); signed exponential kernels with heterogeneous decays (144)
  and live inhibition floored at zero intensity; spread gating
  (s-1)^0.75 for in-spread dimensions, zero at s=1; 13-bin U-shape
  time-of-day factors, mean 1 per dimension; order sizes as compound
  marks, geometric body with Dirac masses at the round sizes
  1/10/50/100/200/500; mechanical book transitions (walk-ups on any
  queue depletion including exact consumption, replenishment sampling
  on widening); a discrete-grid simulator with an exact excitation
  bank and a hard hazard guard (peak intensity times dt must stay
  under the grid resolution bound or the run raises); a Poisson
  control day with identical seeds, book and size conditioning and
  zero memory, so the proportional endogenous-share attribution gives
  the control exactly 0.0. The no-silent-capping lesson from
  deep-read session 5 (the boundary-solution pathology the paper
  itself exhibits with its silently rescaled kernels) is implemented
  as `stabilize_norm_matrix`: an unstable kernel-norm matrix is
  either refused or rescaled to a declared target with a
  StabilityDisclosure record — raw eigenvalue, scaled eigenvalue,
  applied factor, action — never quietly repaired. 20/20 tests in
  `tests/test_ofhawkes.py` (kernel-norm analytic vs numeric,
  scripted-event book invariants, exact-consumption walk, in-spread
  guard, seed reproducibility, Hawkes-vs-Poisson clustering, grid
  validity, U-shape). The demo run: five synthetic days plus the
  Poisson control, seed 20261118, ~816,000 events, endogenous share
  13.1 percent with the control exactly 0.0, eigenvalue chain
  0.6349 (raw, above the stationary bound 0.5261) rescaled with
  disclosed factor 0.4143 to 0.2630, excitation halved once more for
  headroom, landing at a simulated eigenvalue 0.1315 — every step in
  the emitted metadata. `docs/compound_hawkes_engine.md` states it on
  its face: demonstration infrastructure, not evidence; the engine
  simulates, it does not estimate, test, or claim. The demo dataset is
  gitignored. Merged by the owner before CI completed; the files were
  verified present and byte-complete on main afterwards, and again in
  this session's fresh re-fetch of the tree.

- **Protocol/maintenance event — PR #180, the site dashboard page.**
  `docs/compound_hawkes.html` (~421 KB), a self-contained dark-theme
  dashboard of the synthetic demo run: embedded dataset (the same
  gitignored JSON the demo emits, in a JSON.parse-chunked embed),
  hand-rolled SVG charts, zero external dependencies, CSP-clean by
  construction. Live at the Salient site alongside the four existing
  standalone pages and following their exact convention: no nav block
  by design, a "back to the Salient site" link instead. Full
  disclosure on the page itself: all data synthetic, nothing measured,
  no claim, no kill line. Integrity disclosure on record: the branch's
  first push arrived truncated by the transport size limit, was caught
  by the pre-push size checks before any merge, and was corrected; the
  PR body disclosed the event rather than letting a corrupted page
  ship silently.

- **Protocol/maintenance event — PR #181, the nav link.**
  `src/site_nav.py` gained the entry ("compound_hawkes.html", "The
  synthetic order flow") in The Board group; all 15 nav-bearing docs
  pages were regenerated from the canonical renderer (heatmap.html via
  fetch-plus-nav-splice, its long single lines being unreadable
  through the file transport); `tests/test_site_nav.py` expected nav
  count 15 → 16. Four commits instead of one, forced by the sandbox
  16 MiB push ceiling, all verified; every blob byte-identical
  pre- and post-merge; CI green (test, engine); squash-merged
  b8913eea; the 15 live pages re-verified in this session's fresh
  re-fetch, each carrying the link exactly once.

Ratification queue after this session: TWENTY candidate sharpenings,
unchanged (these were engineering builds, not deep-reads; the twenty
standing are those enumerated through deep-read session 20 plus probe
E1), zero armed. T1 remains armed awaiting the owner's word; the
blocked list stays blocked. Deep-read queue pointer unchanged: the
next UNREAD triage entry is "Returns and Order Flow Imbalances:
Intraday Dynamics and Macroeconomic News Effects" (score 34, x5459dc).
Nothing measured, no kill line moved, nothing armed, nothing trades
live.

## 30. Null-time session 26 (2026-11-18): deep-read session 22 — the Takahashi returns-OFI intraday paper read; the release-calendar lead component queued for the deterministic-clock null arm

- **Library deep-read session 22** (the standing queue's next UNREAD
  pointer, score 34, x5459dc, consumed here):
  `paper/research/library/2026-11-18_returns_ofi_macro_news_deep_read.md`
  on Takahashi, "Returns and Order Flow Imbalances: Intraday Dynamics
  and Macroeconomic News Effects" (arXiv:2508.06788v4, 8 Oct 2025; a
  Hosei University / Northwestern dissertation chapter): a bivariate
  structural VAR of one-second S&P 500 E-mini returns and Cont-
  Kukanov-Stoikov OFI, identified through heteroskedasticity
  (SVAR-ITH), 1,490 days 2008-2013, fit per 15-minute interval, with
  the structural parameters regressed on macro-announcement dummies.
  Read against the ONE question. **Grade: NO kill line changed. ONE
  new candidate sharpening queued, PENDING OWNER RATIFICATION:** the
  release-calendar component, with a declared pre-release lead, for
  the deterministic-clock null arm of the branching-ratio trigger.
  The queued arm (deep-read 19, log ## 26) enumerates the
  deterministic intensity as hour-of-day and session segments; the
  paper supplies the missing third component with regression
  evidence: the parameter shifts begin BEFORE the release stamp —
  price impact rises on ANN_t-1 (0.129***, PDF p. 11, Table 2), flow
  innovation volatility declines on and before the release
  (-0.039**/-0.057***), so a null whose release handling begins at
  the stamp misses the withdrawal interval itself.
  Pre-declaration: no branching-ratio window reading is admissible
  under the deterministic-clock null unless the null's deterministic
  intensity also carries the scheduled-release calendar (the
  owner-curated macro timeline), each release with a lead window
  frozen from calibration windows disjoint from evaluation;
  release-explained windows contribute no firing and are reported
  separately. Harder to pass: release windows are precisely where
  return innovations spike, price impact jumps and flow
  responsiveness collapses — the extreme-impact, extreme-intensity
  configuration a branching estimator reads as its most excited
  windows; a bar that survives the hour-of-day null can still be the
  release calendar wearing excitation's costume. It tightens only
  the queued deterministic-clock null arm (and through it the T-H
  and T-O families); no C1-L2 text moves.

  Findings, page-cited: reinforcing, no new item — OFI is
  constructible from BBO events alone, with the order-type
  decomposition explicitly reserved for order-typed data (PDF p. 3,
  footnote 6): a worked exhibit for probe E1's reconstruction-
  admissibility rule, BBO-derived OFI admissible as a feature but
  any decomposition-flavoured reading on it inadmissible.
  Reinforcing, no new item — aggregation manufactures simultaneity,
  the coefficient a function of the clock (b_f 0.301 at one second
  toward 0.55 at one minute, b_r the reverse, PDF p. 12;
  Deuskar-Johnson's stale-limit and price-contingent mechanism): a
  worked exhibit for the record's clock discipline, no fitted
  contemporaneous coefficient from one sampling clock pooled with or
  narrated alongside another. Reinforcing, no new item — fitted
  structural point estimates are unstable across windows and mostly
  not significant (b_r significant in only 64 percent of 15-minute
  intervals, Table 3, PDF p. 12): an independent equity-futures
  exhibit for the uncertainty-band-not-point-estimate rule already
  queued from Hardiman-Bouchaud. Interpretation caution — the
  announcement dummies are significant but add little adjusted
  R-squared beyond market activity variables (PDF p. 9): the release
  calendar acts mostly through observable activity, and the null arm
  must declare which carries the release windows, not stack both
  silently. The killed-if-wrong section stands. Standing caveat
  recorded: single instrument (S&P 500 E-mini), 2008-2013, Chicago
  regular hours only, eight US release types; transfer to a 24/7
  BTCUSDT tape mechanism-level only, never numerical. Source-quality
  note: solo-author dissertation chapter, arXiv v4, published version
  to be checked before formal citation. Laundering directions
  named: INTO — the fitted coefficients never imported as
  calibration, priors, or tolerances; OUT — the one-second
  dissipation and simultaneity findings never read backwards as "L2
  flow has no content at the programme's horizons": dissipation is a
  second-scale statement, the programme's compression question is
  multi-hour, and the simultaneity bias binds fitted contemporaneous
  coefficients, not state-definition triggers.

Ratification queue after this session: TWENTY-ONE candidate
sharpenings (the twenty standing plus the release-calendar lead
component joined here through deep-read session 22), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue pointer: the next UNREAD triage entry is
"Packets, Transactions and Queues: Design Principles for HFT Systems
from a Measurement Study of CME Market Data" (score 34, xc5ba34).
Nothing measured, no kill line moved, nothing armed, nothing trades
live.

## 31. Null-time session 27 (2026-11-18): deep-read session 23 — the CME feed measurement study read; graded default, no sharpening

- **Library deep-read session 23** (the standing queue's next UNREAD
  pointer, score 34, xc5ba34, consumed here):
  `paper/research/library/2026-11-18_packets_transactions_queues_deep_read.md`
  on Maciejewski, "Packets, Transactions and Queues: Design Principles for
  HFT Systems from a Measurement Study of CME Market Data"
  (arXiv:2609.32848v2, September 2026): a solo-author measurement study of
  the CME MDP3 NQ front-month feed, 281 sessions 2025-01 to 2026-02, every
  packet and matching-engine transaction followed through engine clock and
  publisher clock to the receiver, with a 53-minute live cross-validation on
  ES/NQ/ZN. Read against the ONE question. **Grade: NO kill line changed. NO
  new candidate sharpening.** Default grade; the queue is unchanged at
  twenty-one through deep-read 22 plus probe E1. Findings, page-cited:
  reinforcing, no new item — the paper's own fitted branching ratio is
  declared not load-bearing (constant-background exponential-kernel fits
  overstate n when the background varies within the window, per the
  Filimonov-Sornette result it cites; "none of the paper's conclusions
  rests on its value", PDF pp. 25-26), resting its claims on model-free
  diagnostics instead: a worked exhibit for the queued estimator-mode
  register and near-critical regime-disclosure rule, which the T-H
  benchmark's Hardiman-Bouchaud pre-conditions already encode.
  Reinforcing, no new item — the branching ratio is a function of event
  definition and clock: packets and transaction starts give the same n
  (0.798 vs 0.795, PDF p. 38) only because 98.3 percent of transactions
  are one packet (PDF p. 36), while the same engine events read on the
  engine clock against the publisher clock are different gap objects
  entirely (17.1 percent within one publisher period versus 1.04 percent,
  tightest percentile 0.18 microseconds, PDF p. 57): a worked exhibit for
  the record's clock discipline. Reinforcing, no new item — a hard
  deterministic infrastructure clock (the publisher's 7.5 microsecond
  period; bursts surface as evenly spaced trains, tail onset independent
  of rate and branching quintiles at short service times, PDF pp. 51-52,
  59, 62) must live in the null, not the signal: the same class of rule as
  the queued deterministic-clock null arm, corroborating it and adding no
  component that exists at the programme's multi-hour horizons; the
  paper's speed-limit conjecture carries its own qualification verbatim -
  "delaying feedback does not reduce the branching ratio" (PDF p. 65) -
  so it may never be cited as a mechanism that tames criticality.
  Interpretation caution — after a trade, microsecond follow-ups are five
  times as often another trade and half again as often a delete (PDF
  pp. 63-64), the signature of a race, whose losers never appear on the
  public feed: fine-scale post-trade clusters may never be narrated as
  informed directional flow; no feature, threshold, or kill line moves.
  Source-quality note: solo author, arXiv v2, zero indexed citations,
  disclosed AI assistance with the author taking sole responsibility (PDF
  p. 11); single instrument, 14 months, RTH; transaction-level
  identification is corpus-only; published version to be checked before
  formal citation. The killed-if-wrong section on record names the import
  error (a feed-granularity n read as corroboration of T-H's threshold),
  the estimator blindness, and the speed-limit misreading, all three
  blocked by standing discipline. Standing caveat recorded: nothing here
  measures anything at the programme's horizons or on its feature
  definitions; transfer to BTCUSDT multi-hour windows is mechanism-level
  only. Laundering directions named: INTO — no coefficient, period, decay
  time, or quantile enters any spec or calibration; OUT — no race-reading
  of post-trade clusters as informed flow, no feed-granularity
  near-criticality read forward into the programme's aggregation, no
  publisher-pacing-tames-cascades citation.

Ratification queue after this session: TWENTY-ONE candidate sharpenings,
unchanged (deep-read session 23 added none), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked. Deep-read queue
pointer: the next UNREAD triage entry is "Dynamic optimal execution in a
mixed-market-impact Hawkes price model" (score 34, x7c5b08). Nothing
measured, no kill line moved, nothing armed, nothing trades live.

## 32. Null-time session 28 (2026-11-18): deep-read session 24 — the mixed-market-impact Hawkes execution paper read; graded default, no sharpening

- **Library deep-read session 24** (the standing queue's next UNREAD
  pointer, score 34, x7c5b08, consumed here):
  `paper/research/library/2026-11-18_mixed_impact_hawkes_execution_deep_read.md`
  on Alfonsi and Blanc, "Dynamic optimal execution in a
  mixed-market-impact Hawkes price model" (arXiv:1404.0648v2, CERMICS
  ENPC): closed-form optimal execution in an Obizhaeva-Wang mixed-impact
  price model whose other-trader flow is a bivariate marked Hawkes
  process, with the no-Price-Manipulation-Strategy conditions solved
  exactly. Read against the ONE question. **Grade: NO kill line changed.
  NO new candidate sharpening.** Default grade; the queue stands at
  twenty-one through deep-read 22 plus probe E1. Findings, page-cited:
  reinforcing, no new item — the model's no-arbitrage equilibrium pins
  the flow's endogeneity ratio to the price model's transient-impact
  share (iota_s/beta = 1-nu when cross-excitation is zero, and
  2*iota_c < nu*rho for stationarity, PDF p. 14): a worked exhibit that
  a branching or endogeneity reading is model-relative, a function of
  the declared kernel family and impact decomposition, with no
  universal near-critical level implied by stability or efficiency —
  reinforcing the estimator-mode register and the uncertainty-band rule
  already standing. Reinforcing, no new item — no PMS iff the price is
  a martingale with the strategic trader absent (Theorem 2.1, PDF p. 5)
  and no weak PMS iff the same parameter identities hold (Proposition
  5.1, Corollary 5.1, PDF pp. 13-15), and the authors themselves call
  exact MIHM calibration "miraculous" with three reasons fitted
  parameters should not be expected to satisfy it, including that
  fitting a PMS-free market has no guarantee of yielding a PMS-free
  model (PDF p. 14): knife-edge equilibria are model objects, never
  market facts, and "stable versus manipulable" statements are
  model-coupled — the mechanism-level-transfer-only rule reinforced.
  Reinforcing, no new item — under purely Poisson flow a robust
  round-trip manipulation is implementable without knowing any model
  parameter (Proposition 5.2, PDF pp. 15-16): what a misspecified null
  returns is structure, not neutrality — the same class of lesson as the
  U-shape seasonality and publisher-clock exhibits; the null arm's
  enumeration is untouched. Cost-survival ammunition — if a K7-style
  execution-assumption layer is ever built, it must not inherit the
  block-book/linear-impact/exponential-decay/exponential-kernel family
  the authors themselves flag against the empirical facts (PDF
  pp. 2, 7, 9); the layer must declare its impact form and decay family
  and carry this falsification record; nothing is operationalized now.
  Source-quality note — two authors, Natixis-linked funding, arXiv v2
  (June 2015 stamp) with a later internal date line, zero indexed
  citations, no published version on the shelf; no data confrontation
  anywhere, estimation "left for future research" (PDF p. 7), the
  no-excitation-from-the-strategic-trader approximation justified by
  the splitting-dominance argument (PDF p. 8) but untested; published
  version to be checked before formal citation. The killed-if-wrong
  section on record names the laundering route: measuring Hawkes decay
  against price decay and declaring the market in or out of the MIHM
  equilibrium, or reading a measured branching value as "the"
  endogenous share because one model class pins it — every
  load-bearing assumption flagged by the authors themselves, blocked in
  advance by the standing discipline. Standing caveat recorded:
  single-asset closed-form theory, no calibration, mechanism-level
  transfer only; laundering directions named INTO (no MIHM condition,
  cost parameter, or strategy formula enters any spec; equilibrium
  identities never become hypotheses without fresh pre-registration
  through the owner) and OUT (no equilibrium-level readings of
  measured branching, no stable-manipulable transfer to any real tape,
  no operationalization of the reaction strategies).

Ratification queue after this session: TWENTY-ONE candidate sharpenings,
unchanged (deep-read session 24 added none), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked. Deep-read queue
pointer: the next UNREAD triage entry is "The Price Impact of Generalized
Order Flow Imbalance" (score 33, xdb066c). Nothing measured, no kill line
moved, nothing armed, nothing trades live.

## 33. Null-time session 29 (2026-11-18): deep-read session 25 — the generalized-OFI paper read; the event-grain OFI accumulation rule queued for the E1 admissibility family

- **Library deep-read session 25** (the standing queue's next UNREAD
  pointer, score 33, xdb066c, consumed here):
  `paper/research/library/2026-11-18_generalized_ofi_price_impact_deep_read.md`
  on Su, Sun, Li and Yuan, "The Price Impact of Generalized Order Flow
  Imbalance" (arXiv:2112.02947v1, December 2021, Xi'an Jiaotong
  University): the Cont-Kukanov-Stoikov OFI generalized to Chinese
  3-second order-book snapshots, where the best quote crosses multiple
  ticks inside one observation window, breaking the one-tick assumption
  of the CKS linear identity; reported out-of-sample R-squared rising
  from about 33-43 percent (OFI) to about 84-86 percent (log-GOFI) on 10
  CSI 500 constituents. Read against the ONE question. **Grade: NO kill
  line changed. ONE new candidate sharpening queued, PENDING OWNER
  RATIFICATION:** the event-grain OFI accumulation rule, extending the
  E1 volume-conservation reconstruction-admissibility family. The
  ratified E1 rule admissibility-checks the depth reconstruction
  (conservation identity per level per window) but is silent on the
  granularity at which accumulated flow features are computed from that
  depth; this paper supplies the page-cited mechanism for why that gap
  matters: the one-tick assumption is load-bearing in the CKS identity,
  and under coarse windows the swept levels' depth changes are
  misattributed with first-order truncation error (PDF pp. 3-4,
  Figure 2). Pre-declaration: any OFI-type flow feature used in a C1-L2
  (or C8 L2-arm) measurement must be accumulated at event grain, each
  event contributing at the book state it acts on; any window-aggregated
  fallback must disclose the per-window best-quote crossing count and
  the declared sweeping convention, and windows with undisclosed
  multi-tick crossings are inadmissible. Harder to pass: it closes the
  one route by which a measurement could pass the conservation gate and
  still rest on a mispriced flow object, and the mispricing is not
  neutral - coarse-grain OFI can inflate apparent flow-price correlation
  and make a compression signal easier to "find". It tightens only the
  E1 admissibility family (and through it the future C1-L2 pipeline and
  C8's L2 arm); T-O's taker-print trigger, no C1-L2 spec text, and no
  kill line are touched; nothing is armed.

  Findings, page-cited: interpretation caution — the reported R-squared
  magnitudes are never importable: the generalized construction weights
  depth changes by the number of ticks the best quote moved, a quantity
  mechanically tied to the regressed mid-price change, so part of the
  gain may be definitional coupling between feature and target, and the
  paper presents no control for it; the train/test protocol is not
  recoverable from the extract and the stock set is a disclosed
  convenience sample ("to facilitate presentation", PDF pp. 1, 5-6).
  Reinforcing, no new item — the construction exists only because
  depth changes at swept levels are informative, citing the multi-level
  OFI line (Xu, Gould and Howison 2018, PDF pp. 1-2): a library-level
  corroboration that BBO-only features coarsen the depth information
  available in full L2, the standing motivation language of C1-L2; no
  number, weight, or level count transfers. Source-quality note — arXiv
  v1 only, zero indexed citations, no published version on the shelf,
  four authors, 10 of the CSI 500 constituents selected for
  presentation, no costs, no strategy layer; the text extract is heavily
  degraded (formula symbols lost), so the construction was reconstructed
  from prose and figure descriptions, not verified symbol-by-symbol;
  published version to be checked before formal citation. The
  killed-if-wrong section on record names both laundering routes:
  importing the 86-percent headline as C1-L2 motivation (a later honest
  event-grain result would then read as programme failure rather than
  definitional difference), and the reverse leak - an undeclared
  tick-move weighting inside the programme would partially embed the
  outcome's own units in the feature and inflate correlations, which is
  what the queued rule makes inadmissible. Standing caveat recorded:
  Chinese CSI 500, 3-second snapshots, 30-second to 5-minute horizons,
  no crypto, no costs; transferable content is the mechanism (window
  grain versus event grain), never any magnitude. Laundering directions
  named: INTO — no coefficient, weight, R-squared, tick-count
  convention, or construction detail enters any spec, default, or
  calibration, and the generalized construction is not adopted anywhere
  without its own pre-registration; OUT — the R-squared claims are never
  cited as evidence that OFI-family features explain price changes in
  any market other than the paper's own sample, and the headline is
  never repeated as C1-L2 motivation.

Ratification queue after this session: TWENTY-TWO candidate sharpenings
(the twenty-one standing plus the event-grain OFI accumulation rule
joined here through deep-read session 25), zero armed. T1 remains armed
awaiting the owner's word; the blocked list stays blocked. Deep-read
queue pointer: the next UNREAD triage entry is "Passive Market Impact:
A Point Process Approach" (score 33, x43a538). Nothing measured, no
kill line moved, nothing armed, nothing trades live.

## 34. Null-time session 30 (2026-11-18): deep-read session 26 — the passive market impact paper read; the queue-state conditioning rule queued for the sign-kill-line template

- **Library deep-read session 26** (the standing queue's next UNREAD
  pointer, score 33, x43a538, consumed here):
  `paper/research/library/2026-11-18_passive_market_impact_point_process_deep_read.md`
  on Ouazzani Chahdi, Rosenbaum and Szymanski, "Passive Market
  Impact: A Point Process Approach" (arXiv:2412.07461v2,
  v2 stamped 4 Jul 2026, CentraleSupélec / École Polytechnique /
  Université du Luxembourg): a Queue-Reactive limit order book whose
  per-trade information content kappa(q) depends on the volume
  available at the touched side (the "price resistance coefficient",
  decreasing in available volume), market orders Hawkes-driven,
  price defined as the conditional expectation of future
  state-weighted trade flow, with scaling limits and closed-form
  passive-metaorder impact approximations. Read against the ONE
  question. **Grade: NO kill line changed. ONE new candidate
  sharpening queued, PENDING OWNER RATIFICATION:** the queue-state
  conditioning disclosure rule for passive-flow features in the
  C1-L2 L2 arm, extending the pending sign-kill-line template rule.
  Mechanism, page-cited: a classical constant-kappa propagator gives
  the opposite sign for the impact of a passive metaorder (PDF p. 3)
  — a passive buy would push the price down — and the sign is
  repaired only by letting the information content depend on the
  book state, with near-stationary unit passive impact proportional
  to c_kappa / (c_lambda · mu/(1 - ||phi||_L1)) (PDF p. 4, eq. (4)).
  Pre-declaration: any passive-execution or passive-cancel feature
  pre-registered in the C1-L2 L2 arm (or any future pre-registration
  under the sign template) must declare its queue-state conditioning
  functional — the pre-event volume at the touched level, or the
  declared alternative — and state-blind passive aggregates are
  inadmissible. Harder to pass: a state-blind passive count could
  correlate with price either way and pass a naive association
  check while the mechanism makes its sign unpredictable, exactly
  the failure the rule forecloses. Scope: the sign-kill-line
  template as it applies to passive features in the C1-L2 L2 arm
  and future pre-registrations; T-H, T-O, the C1-L2 and C8 spec
  texts and every standing kill line are untouched; nothing is
  armed.

  Findings, page-cited: reinforcing, no new item — the propagator
  sign paradox is a worked exhibit for the standing sign-guard
  discipline (the T1 lesson): a mechanically plausible model yields
  a clean, confident, wrong-signed answer for passive flow, and the
  error is a specification error invisible to any within-model
  check (PDF p. 3); no number or formula transfers. Reinforcing, no
  new item — taker prints cannot recover passive impact: the
  constant-kappa trade model "only accounts for active trading
  using market orders" (PDF pp. 19-20) and the state-dependent price
  requires the queue volumes at the touched side at each trade
  (PDF pp. 20-21, eq. (15)); mechanism-level corroboration of the
  standing "aggTrades is taker prints only, no taker proxy"
  constraint and of C1-L2's premise that full-depth L2 carries what
  taker prints cannot see; theory corroboration, never evidence.
  Interpretation caution — the shape results (passive impact
  vanishes when kappa is constant; V-shaped liquidity gives
  sqrt(c·gamma) growth; a simulated power-law fit at exponent 0.54,
  PDF pp. 14-15, Figure 1) sit on the square-root law line of the
  record, but the no-relaxation result (impact stops at the
  metaorder's end because queues revert to the stationary state
  immediately in the scaling limit, PDF pp. 18-19) is a consequence
  of the assumed queue mean-reversion, not an empirical claim, and  the market/limit impact decomposition holds only under the
  declared approximation that market-order volumes are negligible
  against limit and cancel volumes (PDF p. 18); read as shape
  intuition, never read backwards as an expected BTCUSDT property.
  Source-quality note — three authors; pure theory paper: the
  calibration sections propose estimators (constant kappa from
  realised variance with the Hawkes-derived xi(0), PDF pp. 19-20;
  state dependence from a kappa-squared linear-in-q regression,
  PDF pp. 20-21) but no dataset, fit, or empirical confrontation
  appears in this version, and Figures 1-2 are simulations of the
  model itself; zero indexed citations; published version to be
  checked before formal citation; kept at triage score 33; the
  extract is mathematically degraded in formula regions, so
  equation numbering follows prose anchors and no symbol-by-symbol
  verification of Theorem 2.6 was possible. The killed-if-wrong
  section stands: if constant-kappa propagators were later found to
  match passive metaorder impact empirically, the queued rule would
  lose its mechanism and should die back. Standing caveat: no
  market, no sample, no period, no costs; transferable content is
  mechanism only. Laundering directions named: INTO — the sign-flip
  mechanism and the queue-state dependence enter only as
  feature-design discipline (the rule above), and no constant,
  exponent, scaling-limit object, kappa functional, or
  stationary-state formula enters any spec, default, or
  calibration; OUT — the no-relaxation result, the 0.54 exponent,
  and the section-4 calibration methodology are never cited as
  evidence about any real market, never as expected impact shapes
  for BTCUSDT, and never imported as a validated estimation
  procedure.

Ratification queue after this session: TWENTY-THREE candidate
sharpenings (the twenty-two standing plus the queue-state
conditioning rule joined here through deep-read session 26), zero
armed. T1 remains armed awaiting the owner's word; the blocked list
stays blocked. Deep-read queue pointer: the next UNREAD triage entry
is "Optimal Execution with Passive Market Impact" (score 33,
x28ad86). Nothing measured, no kill line moved, nothing armed,
nothing trades live.

## 35. Null-time session 31 (2026-11-18): deep-read session 27 — the passive optimal-execution paper read; default grade, nothing queued

- **Library deep-read session 27** (the standing queue's next UNREAD
  pointer, score 33, x28ad86, consumed here):
  `paper/research/library/2026-11-18_optimal_execution_passive_impact_deep_read.md`
  on Barzykin (HSBC), Boyce, Neuman and Tuschmann (Imperial College
  London), "Optimal Execution with Passive Market Impact"
  (arXiv:2607.28323v1, 30 Jul 2026): a mesoscopic optimal-execution
  model where a liquidating trader posts unit sell limit orders at a
  controlled distance from the midprice, fills arrive with an
  Avellaneda-Stoikov intensity lambda·e^(−k·delta), and each passive
  fill carries permanent impact at rate eta·e^(−m·delta), derived by
  combining the fill intensity with the Cont-Kukanov-Stoikov /
  Xu-Gould-Howison linear response of mid-price changes to
  (multi-level) order flow imbalance; explicit optimal quote for
  m = k, Lambert-W semi-explicit solution for m ≠ k, plus transient
  impact and TWAP-target extensions; calibration on LOBSTER NASDAQ
  2016 (six stocks) and LSEG FX 2026 (five pairs), headline finding
  the impact decay l is much smaller than the fill decay k, so
  m ≈ k in equities, with a visible gap in FX. Read against the ONE
  question. **Grade: NO kill line changed. NO new candidate
  sharpening queued. This is the default grade: nothing here earns a
  rule.**

  Findings, page-cited: reinforcing, no new item — an independent,
  page-cited second mechanism for the queue-state conditioning rule
  queued through deep-read session 26 (still PENDING OWNER
  RATIFICATION, unchanged): for the large-tick NASDAQ stocks the
  exponential distance-decay fit of MLOFI impact coefficients fails
  (slightly negative l) and the authors state their own preferred
  interpretation, that "MLOFI price impact may depend more directly
  on the volume queued ahead of an order than on its distance from
  the midprice" (PDF p. 15); corroboration only, the rule's text,
  scope and status untouched. Interpretation caution — the paper
  sidesteps, and does not test, the passive-impact sign paradox from
  deep-read session 26: the adverse direction of the passive term
  (PDF p. 6, eq. (3.4)) is inherited from the OFI regression identity
  (PDF pp. 4-5), not derived from book state, and the authors'
  limitations section concedes the estimates measure contemporaneous
  aggregate responses, with a stronger test needing trader-tagged or
  order-level data (PDF p. 24); this paper is never cited as evidence
  about passive-impact sign, nor as counter-evidence to the paradox.
  Reinforcing, no new item — depth carries information without fills:
  fill probabilities decay exponentially with distance (k 0.48-3.72
  across the six stocks) while the MLOFI impact coefficients persist
  across book levels, because "limit orders deeper in the book still
  reveal information, thereby moving the price without being filled"
  (PDF p. 14, Table 4): mechanism-level corroboration of C1-L2's
  standing premise that full-depth L2 carries what taker prints
  cannot see, consistent with the standing "aggTrades is taker
  prints only" constraint; no number, level count, or decay rate
  transfers. Interpretation caution — empirical provenance is thin in
  both samples: the equity evidence reuses the ridge coefficients
  published in Table 8 of Xu, Gould and Howison (PDF p. 13) rather
  than re-estimating impact, six NASDAQ names, 2016; the FX evidence
  is conflated L2 snapshots of at least 5 ms with fills proxied
  synthetically by next-bucket aggressor trades reaching a
  hypothetical passive quote (PDF p. 15); no magnitude from either
  sample transfers, ever. Source-quality note — four authors, one
  HSBC practitioner and three Imperial College mathematicians; arXiv
  v1 stamped 30 Jul 2026, roughly four months old at reading; zero
  indexed citations; published version to be checked before formal
  citation; the paper cites deep-read session 26's paper as
  contemporaneous complementary work, the queue-based microscopic
  foundation beside this mesoscopic form (PDF pp. 23-24); extract
  lightly degraded in the HJB and proof regions, load-bearing pages
  4-17 clean. The killed-if-wrong section on record: if the
  large-tick negative-l fit is later shown to be an estimation
  artifact — the authors themselves warn it may partly reflect model
  misspecification rather than genuine amplification (PDF p. 15) —
  the corroboration weakens to nothing and the queued rule stands
  alone on deep-read session 26's mechanism, which is where it
  already stands. Standing caveat recorded: NASDAQ 2016 via LOBSTER
  and borrowed 2018 ridge coefficients; LSEG FX 2026 conflated L2
  with synthetic fill proxies; no crypto, no BTCUSDT, no
  futures; measuring-window conventions unlike the programme's.
  Laundering directions named: INTO — no decay rate (k, l, m), impact
  coefficient (eta, xi, beta), fill intensity (lambda), or
  quote-distance form enters any spec, default, or calibration, and
  the passive-impact direction in the L2 arm stays governed by the
  pending rules and the pre-registered sign guard, never by this
  paper's assumed sign; the model is not adopted anywhere without its
  own pre-registration; OUT — the m ≈ k equity headline, the
  fill-versus-impact decay gap, and the FX estimates are never cited
  as evidence about any real market the programme measures, and the
  deep-level MLOFI persistence is never cited as expected BTCUSDT
  depth behavior.

Ratification queue after this session: TWENTY-THREE candidate
sharpenings, unchanged (deep-read session 27 added none), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue pointer: the next UNREAD triage entry is
"State-dependent Hawkes processes and their application to limit
order book modelling" (score 32, x947263). Nothing measured, no
kill line moved, nothing armed, nothing trades live.

## 36. Null-time session 32 (2026-11-18): deep-read session 28 — the state-dependent Hawkes paper read; the book-state mix disclosure rule queued for the C8 A3 family

- **Library deep-read session 28** (the standing queue's next UNREAD
  pointer, score 32, x947263, consumed here):
  `paper/research/library/2026-11-18_state_dependent_hawkes_lob_deep_read.md`
  on Morariu-Patrichi and Pakkanen (Imperial College London),
  "State-dependent Hawkes processes and their application to limit
  order book modelling" (arXiv:1809.08060v3, 17 September 2021): a
  self- and cross-exciting event process fully coupled with a
  finite-state process that switches at event times, so the
  excitation kernel depends on the book state and the state
  transition depends on the event type; separable likelihood making
  estimation no harder than an ordinary multivariate Hawkes fit;
  estimated on one year of LOBSTER level-I INTC data (two models:
  bid-ask-spread state and queue-imbalance-bin state), finding
  excitation magnitudes and timescales strongly state-dependent
  (0.1-100 milliseconds) and measured endogeneity itself
  state-dependent, systematically at or above the critical spectral
  radius in disequilibrium states. Read against the ONE question.
  **Grade: NO kill line changed. ONE new candidate sharpening queued,
  PENDING OWNER RATIFICATION:** the bar-level book-state mix
  disclosure component for the C8 A3 micro-threshold rule, extending
  the PROPOSED shuffled-arrival placebo amendment. Mechanism,
  page-cited: per-state spectral radii are systematically above the
  critical value in disequilibrium states and below it in equilibrium
  states (ModelS rho(2+) systematically above 1; ModelQI
  sell++/buy++ above 0.9 half the time), so "critical reflexivity"
  is "a largely state-dependent phenomenon, observed only in
  particular circumstances" (PDF pp. 19-21, Figure 10, PDF p. 22).
  Two pre-declarations, both harder to pass. (a) A bar-level,
  book-state-blind n_c conflates the bar's state composition with the
  strength of the excitation mechanism: a bar can clear n_c > 0.8
  because it spent time in disequilibrium states, and the micro
  indicator would then partly encode the bar's book-state mix —
  dangerously close to conditioning on what the macro cell already
  selects; every per-bar n_c reading in the A3 family must be
  accompanied, recorded on TRAIN, by the bar's occupancy distribution
  over a pre-declared state variable computable from the same tape
  (spread regime, queue-imbalance-bin occupancy, or the declared
  alternative), with the state-blind n_c never reported alone.
  (b) The shuffled-arrival placebo severs more than temporal
  excitation: in a state-dependent world the state process jumps at
  event times, so time-shuffling arrivals also destroys the
  event-state sequence and the state-flow feedback that drives the
  endogeneity readings; any production-minus-placebo gap must be
  reported with a declaration of what couplings the shuffle severs,
  and a gap is inadmissible as evidence of "genuine endogeneity"
  without that declaration. Scope: a disclosure requirement on the A3
  family only; A3 and every C8 amendment remain PROPOSED and not
  armed; no kill line touched, no threshold moved, T-H and T-O
  untouched; nothing is armed.

  Findings, page-cited: reinforcing, no new item — timestamp
  discipline corroborated at the source: LOBSTER nanosecond
  timestamps give more than 99 percent unique level-I timestamps,
  accurate event ordering at the shortest timescales is essential
  for Hawkes estimation, and the authors flag and repair the
  tied-timestamp artifact (a market order matched with n limit
  orders recorded as n tied prints, aggregated into one event)
  (PDF p. 13): mechanism-level corroboration of the L0 gate's
  timestamp audit, of A3's pre-declared µs exchange timestamps, and
  a named sibling of the record's multi-print event-grain
  discipline; no parameter transfers. Reinforcing, no new item —
  regime instability of excitation estimates: day-to-day base rates
  mirror day-to-day order counts, suggesting mainly exogenous
  day-to-day variation (PDF p. 15), and the kernel norms break
  structurally at the 5 February 2018 return of volatility, with
  distinct pre- and post-break levels (PDF pp. 16-17, Figure 7,
  PDF p. 19): corroborates the standing MIHM caution against
  endpoint-level readings of a single branching estimate — measured
  excitation moves across regimes and across states within a day;
  never carried across regimes, never read as an equilibrium
  classification. Interpretation caution — a per-state spectral
  radius above 1 is not market instability: the process is
  stationary as a state-dependent whole (PDF p. 6), rho above 1 in a
  disequilibrium state is a within-model excursion, and reading it
  as flash-crash-prone or near-critical would launder a
  model-internal quantity; the state definitions themselves
  (two-state spread, five queue-imbalance bins, PDF pp. 13-14) are
  the authors' constructions on one large-tick stock and none
  transfers; the programme's L2 arm would have to declare its own
  state variable if the queued rule is ratified. Source-quality
  note — two authors (Imperial College; Pakkanen also
  Aarhus/CREATES); arXiv v3, first posted 2018, stamped 17 September
  2021; companion mpoints library published; headline results INTC
  only, with AMD, MU, SNAP and TWTR relegated to results available
  upon request (PDF p. 11); published version to be checked before
  any formal citation; extract clean in the load-bearing sections,
  some figure labels glyph-mangled. The killed-if-wrong section on
  record: if the state-dependence of endogeneity is later shown to
  be an artifact of the state-bin construction, the queued
  component loses its mechanism and should die back to A3 as it
  stands; conversely, A3-family n_c readings published without the
  state-mix disclosure would risk partially embedding the macro
  conditioning, exactly the costume failure K1 exists to catch.
  Standing caveat recorded: one large-tick US stock, level-I
  LOBSTER, June 2017 to May 2018, 12:00-14:30 windows chosen for
  flat intensity, exponential kernels with the authors' own
  power-law caveat, no crypto, no BTCUSDT. Laundering directions
  named: INTO — no spectral radius, kernel norm, state definition,
  bin edge, timescale range, or transition matrix from this paper
  enters any spec, default, or calibration, and the state-dependent
  Hawkes model is not adopted anywhere without its own
  pre-registration; OUT — the per-state critical reflexivity
  readings are never cited as evidence that any market the
  programme measures is near-critical or unstable, and the
  0.1-100 millisecond timescales are never cited as expected
  reaction scales outside this paper's own sample.

Ratification queue after this session: TWENTY-FOUR candidate
sharpenings (the twenty-three standing plus the book-state mix
disclosure rule joined here through deep-read session 28), zero
armed. T1 remains armed awaiting the owner's word; the blocked list
stays blocked. Deep-read queue pointer: the next UNREAD triage entry
is "Forecasting High Frequency Order Flow Imbalance" (score 32,
x78a2e8). Nothing measured, no kill line moved, nothing armed,
nothing trades live.

## 37. Null-time session 33 (2026-11-18): deep-read session 29 — the OFI Hawkes forecasting paper read; default grade, nothing queued

- **Library deep-read session 29** (the standing queue's next UNREAD
  pointer, score 32, x78a2e8, consumed here):
  `paper/research/library/2026-11-18_ofi_hawkes_forecasting_deep_read.md`
  on Aditya Nittur Anantha (SigmaQuant Technologies Pvt. Ltd., Indian
  Institute of Science) and Shashi Jain (Indian Institute of
  Science), "Forecasting high frequency order flow imbalance using
  Hawkes processes" (arXiv:2408.03594v1, 7 August 2024): a
  trade-count OFI defined as the normalized difference of
  SELL-classified and BUY-classified trade counts over a window
  (eq. (3), PDF p. 5), with aggressor side determined
  deterministically from the two exchange order numbers on each NSE
  trade message, no Lee-Ready inference (PDF p. 5); bivariate
  self- and cross-exciting Hawkes processes fitted to one day of
  NIFTY futures trade arrivals (19 September 2018, 375 one-minute
  windows, PDF pp. 5-7), one-minute-ahead OFI distributions
  forecast by 500 thinning simulations per window (PDF pp. 12-13,
  15-16), scored by the probability each empirical forecast
  distribution assigns the realized OFI, and compared across
  exponential, sum-of-exponentials, power-law, conditional-law, EM,
  VAR and Poisson models with White's reality check and Hansen's
  test for superior predictive ability (PDF pp. 7-8, 11, 16);
  sum-of-exponentials (p 0.743) and conditional-law (p 0.257) the
  only non-rejected benchmarks, VAR at 0.101 also not rejected at 95
  percent (Table 4, PDF p. 16), sum-of-exponentials favored on
  computational cost alone; minute OFI stationary and strongly
  non-normal in appendix (PDF p. 20); BUY-BUY and SELL-SELL
  self-excitation dominating with intermittent cross-excitation
  episodes (PDF p. 18). Read against the ONE question. **Grade: NO
  kill line changed. NO new candidate sharpening queued. This is the
  default grade: nothing here earns a rule.**

  Findings, page-cited: interpretation caution — the OFI name
  collision: this paper's OFI is trade-count asymmetry (eq. (3),
  PDF p. 5), not the Cont-Kukanov-Stoikov depth-change OFI of the
  record's line (the paper cites CKS 2014 for a related but distinct
  quantity, PDF p. 3); no result from this paper transfers onto the
  record's CKS-family OFI measurements, and the distinction stays
  live because the next queue entry (x98e019) sits in the same
  count-family. Reinforcing, no new item — aggressor side
  exchange-native never inferred: the stated reason for avoiding
  Lee-Ready and bulk classification is that inference-based rules
  misclassify in volatile, fast-moving markets (PDF p. 4),
  corroborating the standing "aggTrades is taker prints only, no
  taker proxy" constraint at the mechanism level; the NSE order-ID
  mechanism itself is a venue property and transfers nowhere.
  Reinforcing, no new item — aggregation discards event clustering
  (PDF p. 3), but this paper does not prove the recovery: its own
  SPA table cannot reject the VAR at 95 percent (p 0.101, Table 4,
  PDF p. 16), the authors concede the conditional-law and VAR models
  cannot be rejected with 95 percent confidence and flag a possible
  same-day bias favoring sum-of-exponentials (PDF p. 17), so the
  event-grain OFI accumulation rule queued through deep-read session
  25 gains no corroboration here and the record says so. Source-
  quality note — two authors, one practitioner-affiliated
  (SigmaQuant, Indian Institute of Science); arXiv v1 only,
  August 2024, no journal record checked; zero indexed citations;
  single-session single-instrument NSE dataset (PDF p. 5);
  power-law kernel fitted by ad-hoc stochastic gradient descent with
  no convergence guarantees stated (Algorithm 5.1, PDF pp. 11-12);
  no price prediction, no P&L, no costs, regulatory and
  risk-management framing only (PDF p. 3); extract page-marked and
  clean, 21 pp. The killed-if-wrong section on record: nothing in
  the record rests on this paper, no rule was added or amended on
  its basis, so if the SPA ranking is later shown to be an artifact
  of the single-day sample, the loss construction, or the same-day
  bias the authors themselves flag, nothing dies and nothing needs
  repair; conversely, any citation of this paper as confident
  evidence that event-time forecasting beats calendar aggregation
  would launder a non-rejected null (VAR p 0.101, Table 4,
  PDF p. 16) and should die in review. Standing caveat recorded:
  one NSE session, one instrument, NIFTY futures 2018, 375
  one-minute windows, 315 loss observations; deterministic
  classification via NSE order numbers, a venue property; realized
  minute OFI stationary and strongly non-normal (PDF p. 20); no
  crypto, no BTCUSDT. Laundering directions named: INTO — no kernel
  form, no parameterization, no window or simulation parameter, no
  loss construction, and no p-value from this paper enters any spec,
  default, or calibration, and the Hawkes-forecasting construction
  is not adopted anywhere without its own pre-registration; OUT —
  the sum-of-exponentials headline and the SPA p-values are never
  cited as evidence that event-time modeling beats calendar
  aggregation beyond this paper's own single-day NSE sample, never
  as expected behavior of the programme's CKS-family OFI
  quantities, never as expected BTCUSDT behavior, and never as
  evidence about any market the programme measures.

Ratification queue after this session: TWENTY-FOUR candidate
sharpenings, unchanged (deep-read session 29 added none), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue pointer: the next UNREAD triage entry is
"Hybrid Vector Auto Regression and Neural Network Model for Order
Flow Imbalance" (score 32, x98e019). Nothing measured, no kill line
moved, nothing armed, nothing trades live.

## 38. Null-time session 34 (2026-11-18): deep-read session 30 — the hybrid VAR-FNN OFI paper read; default grade, nothing queued; the results recorded as a leakage specimen

- **Library deep-read session 30** (the standing queue's next UNREAD
  pointer, score 32, x98e019, consumed here):
  `paper/research/library/2026-11-18_hybrid_var_fnn_ofi_deep_read.md`
  on Abdul Rahman and Neelesh Upadhye (Department of Mathematics,
  Indian Institute of Technology Madras), "Hybrid Vector Auto
  Regression and Neural Network Model for Order Flow Imbalance
  Prediction in High-Frequency Trading" (arXiv:2411.08382v1,
  13 November 2024): a hybrid forecaster for the same trade-count
  OFI read through deep-read session 29 (eq. (1), PDF pp. 2-3,
  explicitly building on Anantha and Jain [13], PDF p. 3), VAR on
  buy and sell order counts with a feedforward network on the
  residuals, a three-way BUY/SELL/HOLD intensity signal behind a
  threshold T close to zero (PDF pp. 3, 5-8), 10,000 seconds of one
  Binance cryptocurrency, three validation slices of about 3,000
  points (PDF p. 9), 120 hand-evaluated parameter combinations
  (PDF p. 9), headline R2 0.997 and 98.18 percent intensity accuracy
  on BTCUSD against 46.61 percent for VAR-only (Table 4, PDF
  p. 11). Read against the ONE question. **Grade: NO kill line
  changed. NO new candidate sharpening queued. This is the default
  grade: nothing here earns a rule.** The read went further: the
  results section carries the page-cited signature of target
  leakage, recorded so the paper can never be laundered into the
  record.

  Findings, page-cited: interpretation caution — the results are
  inadmissible as evidence, three page-cited signs jointly
  decisive: (a) identity-level predictions: the sample rows of
  Table 5 track the actual OFI to within 0.001 to 0.023 on all six
  displayed rows (hybrid -0.3315 vs actual -0.3454, -0.9203 vs
  -0.9430, 0.2256 vs 0.2269, -0.1203 vs -0.1221, 0.8431 vs 0.8429,
  -0.5581 vs -0.5616; PDF p. 12), second-scale OFI values
  reconstructed to three decimals are the label, not a forecast;
  (b) the linear backbone carries nothing: every appendix VAR lag
  coefficient is statistically zero (L1.buy_orders p 0.706,
  L1.sell_orders p 0.268, L2.buy_orders p 0.957, L2.sell_orders
  p 0.095; Appendix A.1, PDF p. 15) and VAR-only validation R2 is
  -0.002 on BTCUSD (Table 4, PDF p. 11), so the near-perfect hybrid
  metrics cannot come from lag structure that does not exist and
  the network output must overlap the target window; (c) no
  chronological split is ever declared: training and validation
  loss curves are offered as generalization evidence (Appendix A.4,
  PDF p. 17) without the validation data ever being shown later in
  time than training, the three validation datasets being separate
  slices, not declared holdouts (PDF p. 9); every headline number
  is therefore never cited by the record, for any purpose, ever.
  Reinforcing, no new item — ammunition for the leakage-hunting
  culture: the paper is a worked specimen of precisely what the
  record's discipline exists to catch, unlabelled train-test mixing,
  predictions indistinguishable from labels, a missing persistence
  baseline, 120 hand-evaluated parameter combinations with no
  multiple-testing discussion (PDF p. 9), and prose upgrading
  "slightly better performance metrics" (PDF p. 5) into
  "significant improvements" (abstract, PDF p. 1); corroborates by
  counterexample why the deliberately-flawed examples of the
  leakage-resistant backtester and the K1 costume guard exist, and
  no rule is extended because the programme's discipline already
  covers this failure class. Reinforcing, no new item — the OFI
  name collision repeats and closes the count-family bracket opened
  at deep-read session 29: same trade-count asymmetry (eq. (1),
  PDF pp. 2-3, predecessor [13] cited, PDF pp. 3-4), not the
  Cont-Kukanov-Stoikov depth-change OFI of the record's line, and
  nothing in either session transfers onto the CKS-family
  measurements; the VAR-only R2 of -0.002 squares with session
  29's finding that nothing strong was demonstrated at this grain
  but rides on the same undocumented evaluation, corroboration of
  nothing. Source-quality note — two authors, IIT Madras
  mathematics department; arXiv v1 only, 13 November 2024, no
  journal record checked; zero indexed citations; internal naming
  inconsistency: datasets declared BTCUSD and ETCUSDT (PDF p. 9,
  Table 4, PDF p. 11) but the narrative from PDF p. 12 onward and
  the limitations (PDF p. 13) call them ETHUSDT, so the pair used
  is undetermined; the appendix GitHub link is a placeholder (PDF
  p. 17); threshold T never given a value, a reproduction blocker
  (PDF p. 3); the claim that trade classification is "deterministically
  inferred by tracing the origin of the passive order" (PDF p. 2)
  mirrors the NSE order-number mechanism and does not describe
  Binance, where the taker side is native on the aggTrades stream;
  extract page-marked and clean, 17 pp. The killed-if-wrong section
  on record: nothing rests on this paper; if a genuinely
  chronological holdout later surfaced and R2 0.997 survived, any
  result would still have to be re-measured on the programme's own
  tape under the programme's own protocols before anything could
  move, and until then the inadmissibility judgment stands;
  conversely if the leakage reading is right, the paper stands as a
  named specimen of publishable leakage, reinforcing the record's
  refusal to accept headline metrics from any source that does not
  declare its holdout, which is already the rule. Standing caveat
  recorded: 10,000 seconds, roughly 2.8 hours, one Binance
  cryptocurrency, single regime, about 3,000-point slices, data
  stream never specified, threshold undeclared, no costs, no
  execution, no P&L, no L2 depth of any kind. Laundering directions
  named: INTO — no architecture, hyperparameter, lag order,
  threshold, metric, R2, or accuracy figure from this paper enters
  any spec, default, or calibration, and the hybrid VAR-FNN
  construction is not adopted anywhere without its own
  pre-registration under the programme's holdout rules; OUT — the
  R2 values and intensity accuracies are never cited as evidence
  that OFI of any definition is predictable at high frequency,
  never as evidence that hybrid models beat standalone models,
  never as expected BTCUSDT behavior, and never as evidence about
  any market the programme measures.

Ratification queue after this session: TWENTY-FOUR candidate
sharpenings, unchanged (deep-read session 30 added none), zero armed.
T1 remains armed awaiting the owner's word; the blocked list stays
blocked. Deep-read queue pointer: the next UNREAD triage entry is
"Trading in the Sunshine or in the Shade: Market Impact and Adverse
Selection on Hyperliquid" (score 32, xa74970). Nothing measured, no
kill line moved, nothing armed, nothing trades live.

## 39. Null-time session 35 (2026-11-18): deep-read session 31 — the Hyperliquid sunshine-trading paper read; the queue-state anticipation disclosure component queued for the C1-L2 L2 arm

- **Library deep-read session 31** (the standing queue's next UNREAD
  pointer, score 32, xa74970, consumed here):
  `paper/research/library/2026-11-18_hyperliquid_sunshine_trading_deep_read.md`
  on Davide Barone and Fabrizio Lillo (Scuola Normale Superiore,
  Pisa), "Trading in the Sunshine or in the Shade: Market Impact
  and Adverse Selection on Hyperliquid" (arXiv:2606.15715v1,
  14 June 2026): Hyperliquid, a fully on-chain CLOB for
  cryptocurrency perpetual futures with a protocol-native TWAP
  whose parent order is publicly visible from inception, used as
  a natural sunshine-trading laboratory; about 4.3 million hidden
  statistical metaorders reconstructed from same-address same-sign
  trades (30-minute splitting rule, at least 10 children) versus
  about 465,000 visible native TWAPs, on 641 million fills and
  about USD 1.93 trillion notional across 201 markets, 28 July
  2025 to 23 March 2026 (PDF pp. 4-6); hidden metaorders execute
  U-shaped front-loaded schedules with double-inflection
  trajectories and post-completion decay, TWAPs nearly uniform
  with smooth concave paths (PDF pp. 10-12); visible TWAPs face
  about 9 basis points lower temporary impact, leave about
  5 basis points less permanent displacement, and hidden
  metaorders executed in the direction of already-visible
  same-side TWAP flow pay about 0.84-0.92 basis points more per
  10 percentage points of visible dominance, about 6 basis points
  surviving control for the overlapping flow's own price pressure
  (PDF pp. 13-20); during active TWAP windows the displayed book
  tilts toward the absorbing side, depth within five spreads
  rises, sweep costs fall, the touch widens, with negligible
  pre-window leads and size scaling (Figure 7, PDF pp. 22-23;
  Table 4, PDF pp. 24-25); the market-wide adverse-selection
  comparative static tested and honestly reported as a null,
  reframed as conditional and event-level (PDF p. 21). Read
  against the ONE question. **Grade: NO kill line changed. ONE
  new candidate sharpening queued, PENDING OWNER RATIFICATION:**
  the queue-state anticipation disclosure component for the
  queue-state conditioning rule (deep-read session 26, corroborated
  session 27), covering passive-flow features in the C1-L2 L2 arm.
  Mechanism, page-cited: the displayed book state is not exogenous
  scaffold, it is an elastic response to flow information,
  including anticipated flow — the oriented imbalance within five
  spreads jumps at program start and persists to completion, depth
  rises about 4,182 USD, the 10,000 USD sweep cost falls, while
  the touch widens as suppliers rest size behind it at prices
  compensating inventory risk, with negligible pre-window leads
  and imbalance and depth responses scaling with announced size
  (Figure 7, PDF pp. 22-23; Table 4, PDF p. 25); the same tilt
  appears gradually around hidden programs as they become
  inferable from same-address same-direction flow, rising more
  persistently for longer programs, read as market makers learning
  a directional program is underway, with the limitations section
  naming learnability explicitly (PDF pp. 22-23, 26). Consequence
  for the queued rule, harder to pass: a passive-flow feature
  conditioned on queue state may partially encode anticipated or
  in-progress flow programs, so contemporaneous book-state
  conditioning can quietly embed forward-looking flow information,
  the costume failure K1 exists to catch. Two pre-declarations.
  (a) Anticipation-content declaration: every queue-state-
  conditioned passive feature reading in the C1-L2 L2 arm must be  accompanied, recorded on TRAIN, by a declaration of which flow
  programs the declared state variable can respond to on the
  programme's actual venue and fields (protocol-announced flow,
  and statistically learnable from public flow either way), made
  before the L2 data arrives. (b) Pre-window lead bound: the
  conditioning state's measured lead against placebo windows must
  be reported with the feature reading on TRAIN, so
  anticipation-encoding is bounded rather than assumed away; a
  state indistinguishable from placebo on lead carries no
  anticipation content and the disclosure closes, a state with
  positive lead must be declared partially anticipatory or
  replaced. Scope: the C1-L2 L2 arm's queue-state-conditioned
  passive features only, a disclosure requirement on top of the
  queued conditioning rule; no spec text, kill line, threshold,
  T-H or T-O moves; nothing is armed.

  Findings, page-cited: reinforcing, no new item — pre-trend and
  placebo discipline at the source: the book-response claims ride
  an event-time placebo design with event and relative-minute
  fixed effects and an active-window treatment indicator, probed
  with a pre-window lead and a size interaction (Eqs. (10)-(12),
  PDF p. 24; Table 4, PDF p. 25), and the decisive honesty move is
  the relative spread's lead (+0.21 basis points, against a
  +0.28 active window) read as selection into wider-spread states
  rather than a visibility response, cross-checked against
  statistical metaorders (+0.16 lead, +0.05 start) (PDF p. 25):
  mechanism-level corroboration of the A3-family placebo
  discipline queued through deep-read session 28, without the
  lead test the spread result would have been misattributed.
  Reinforcing, no new item — metaorder reconstruction with
  declared thresholds and quantified removal: 30-minute
  inter-arrival splitting, at least 10 children explicitly to
  reduce false positives from coincidental clustering, native
  TWAPs at least 5 children, a 24-hour completion cap removing
  28,904 orders quantified immaterial (0.7 percent count, 1.5
  percent notional) (PDF pp. 5-6), a named sibling of the record's
  event-grain discipline; no threshold transfers. Interpretation
  caution — taker-print reconstruction misclassifies aggressive
  liquidity providers as metaorder executioners, and the
  programme's aggTrades-is-taker-prints-only constraint makes
  this failure mode live on its own tape: 46.2 percent of
  reconstructed metaorders have a same-address maker fill during
  the window, 40.3 percent a same-direction maker fill,
  concentrated in the top 40 passive addresses holding 68 and 65
  percent of that passive volume with both-side fills consistent
  with market-making, 31 percent same-direction after their
  exclusion (PDF p. 26, limitation 1); aggressive market makers
  crossing the spread repeatedly in one direction are
  statistically indistinguishable from execution programs using
  taker data alone, a bound on what taker-only aggregation can
  classify, never a solved problem. Interpretation caution — the
  comparison is an observational equilibrium comparison between
  execution regimes, not a randomized treatment of visibility,
  and the authors say so: a taker-identity prior predicts the
  mechanism choice almost perfectly (AUC 0.998, against 0.685
  adding pre-start book state to a pair-only model at 0.674),
  between-taker variation share about 0.93, 86.6 percent of
  orders from single-mechanism addresses, sub-account aggregation
  to masters (99.7 percent of volume) changing essentially
  nothing (PDF pp. 13, 26); the 9-basis-point discount is a
  property of who chooses TWAP as much as of visibility, and the
  paper is never cited as a causal estimate of transparency;
  adjacent honest null, market state barely predicts native TWAP
  starts (PR-AUC 0.0053 against climatology 0.0033, versus 0.094
  to 0.142 for statistical metaorders), so the paper does not
  show the book forecasting program arrivals (PDF p. 26).
  Cost-survival ammunition — no impact exponent is a stable venue
  constant: TWAP temporary impact is a power law with exponent
  0.303, statistical metaorders a saturating arctangent in
  log-log space, three curve crossings between regimes (PDF
  pp. 8-9); the pooled surface tilts to volume-time duration
  (about 0.31) over participation (about 0.12), against
  Zarinelli et al. both near one-half (PDF p. 9), and the
  participation slope is significant for latent orders and zero
  for TWAPs (Table 1, PDF p. 16); any cost model assuming one
  universal impact law or one exponent per venue inherits
  regime-dependence it cannot see from prints alone. Source-
  quality note — two authors, Scuola Normale Superiore Pisa,
  Fabrizio Lillo a leading microstructure researcher; arXiv v1
  14 June 2026, no journal record checked; 641 million fills,
  USD 1.93 trillion notional, 201 markets, with companion
  Albers-Cucuringu-Howison-Shestopaloff work cited and public
  data via Hydromancer's Reservoir (PDF pp. 4-5, 29); the book
  analysis rests on one-minute snapshots, 20 levels, 15 December
  2025 onward only, so the book results cover about three months
  (PDF p. 5); the limitations section is exemplary, stating the
  misclassification diagnostic, the randomization caveat, the
  learnability of hidden programs, and the arrival-predictability
  null (PDF pp. 26-27); extract page-marked and clean, 31 pp.
  The killed-if-wrong section on record: if the anticipation
  mechanism is later shown to be announcement-specific, a
  Hyperliquid protocol artifact with no analog where flow is not
  protocol-visible, the queued component loses its mechanism and
  should die back to the conditioning rule as it stands; the
  transferable core is the learnable-flow part, the book state
  responding to flow programs as they become inferable from
  public tape, which is venue-independent, and if that also fails
  on the programme's venue and fields the disclosure guards a
  problem that does not exist and should die back; conversely,
  queue-state-conditioned passive readings published without the
  anticipation declaration and the lead bound would risk embedding
  forward-looking flow information into what is presented as
  contemporaneous conditioning, exactly the costume failure K1
  exists to catch, and the queued component is what forecloses
  it. Standing caveat recorded: one venue, Hyperliquid, fully
  on-chain CLOB for perpetual futures, visible addresses,
  protocol-native TWAP, USDC margin, 0.2-second median end-to-end
  latency, an order of magnitude or more slower than any
  centralized exchange, no Binance, no BTCUSDT, no spot equities,
  no anonymous flow; book snapshots one-minute, 20 levels, 15
  December 2025 onward; all magnitudes venue- and period-specific.
  Laundering directions named: INTO — no coefficient, elasticity,
  exponent, basis-point figure, threshold, dominance share, or
  normalization choice (order-anchored 24-hour windows, Parkinson
  volatility, the five-spread depth band) from this paper enters
  any spec, default, or calibration, and the sunshine-trading
  framework is not adopted anywhere without its own
  pre-registration; OUT — the 9-basis-point announcer discount,
  the 5-basis-point permanent gap, the 0.84-0.92-basis-point
  mirror cost, the book-response magnitudes, and the impact
  exponents are never cited as expected behavior of any market
  the programme measures, never as expected BTCUSDT book
  behavior, never as expected impact on any execution the
  programme simulates, and the venue's latency and transparency
  properties are never cited as comparable to the programme's
  venue.

Ratification queue after this session: TWENTY-FIVE candidate
sharpenings (the twenty-four standing plus the queue-state
anticipation disclosure rule joined here through deep-read session
31), zero armed. T1 remains armed awaiting the owner's word; the
blocked list stays blocked. Deep-read queue pointer: the next UNREAD
triage entry is "Order Book Queue Hawkes-Markovian Modeling"
(score 31, xce0ba3). Nothing measured, no kill line moved, nothing
armed, nothing trades live.

## 40. Null-time session 36 (2026-11-18): deep-read session 32 — the Hawkes-Markovian queue paper read; the queue-label convention declaration queued for the queue-state conditioning rule

- **Library deep-read session 32** (the standing queue's next UNREAD
  pointer, score 31, xce0ba3, consumed here):
  `paper/research/library/2026-11-18_order_book_queue_hawkes_markovian_deep_read.md`
  on Philip Protter (Department of Statistics, Columbia
  University), Qianfan Wu (Kelley School of Business, Indiana
  University Bloomington) and Shihao Yang (Georgia Institute of
  Technology), "Order Book Queue Hawkes-Markovian Modeling"
  (arXiv:2107.09629v3, v3 stamped 5 January 2022): a Queue-Reactive
  event taxonomy — trades, insertions and cancellations at each of
  K level-3 queues per side plus six reference-price-change events,
  24 event types in all (PDF pp. 7-10) — modeled as a multivariate
  Hawkes whose baseline intensities are made Markovian through the
  current liquidity state (queue size, or the spread for the two
  spread-crossing events, ten buckets) and a 126-category intraday
  time factor (PDF pp. 10-13); Kirchner's non-parametric binned
  autoregression estimator extended to a varying baseline, LASSO on
  the excitement coefficients only, AIC selection across seven
  nested specifications (PDF pp. 13-22); implemented on 20 trading
  days of LOBSTER-reconstructed NASDAQ ITCH data for Apple, January
  2019, bin-size 0.25 seconds, support 20 seconds, LASSO parameter
  0.0005 (PDF pp. 22-23). Reported: most excitement functions decay
  exponentially with trailing zeros, but non-exponential shapes
  recur for higher-level trade events arriving in wide-spread
  states (PDF pp. 25-27); first-level insertion and cancellation
  kernels similar in shape, the similarity fading at levels 2-3
  (PDF pp. 25-26, 44-45); arrival intensity rising with the
  liquidity state for first-level trades, cancellations and
  insertions but falling for level-2/3 insertions (PDF pp. 27-28);
  a U-shaped intraday intensity with a sharp 15:55-16:00 elevation
  (PDF pp. 28-29); qualitative conclusions robust to ignoring
  order sizes, dropping LASSO and doubling the bin size (PDF
  pp. 30, 48-69); and in-sample AIC ranking the Hawkes part above
  the state parts with the liquidity-state and time-factor
  additions improving on top of the Hawkes part all 20 days
  (Table 1, PDF pp. 31-32). Read against the ONE question.
  **Grade: NO kill line changed. ONE new candidate sharpening
  queued, PENDING OWNER RATIFICATION:** the queue-label convention
  (reference-price tie-break) declaration component for the
  queue-state conditioning rule (deep-read session 26, corroborated
  session 27, extended by the anticipation disclosure at
  deep-read 31), covering passive-flow features in the C1-L2 L2
  arm. Mechanism, page-cited: every queue index in the taxonomy is
  a count of ticks from a reference price that must lie strictly
  between best bid and best ask (PDF pp. 5-7, 12-13), and when the
  spread is an even number of ticks the midpoint lands exactly on
  a valid price position, so the reference is displaced plus or
  minus half a tick toward the side closer to the previous
  reference value (Supplementary A, PDF pp. 38-39); the displaced
  convention silently reassigns which price level counts as the
  first ask, the first bid and every deeper label, so two
  implementations of the same declared conditioning functional read
  different conditioning states from the same book, with the
  divergence concentrated in the wide-spread states where
  conditioning carries its information: the fitted state effects
  differentiate there (PDF pp. 27-28) and the non-exponential
  kernel shapes concentrate there (PDF pp. 26-27). On the
  programme's venue and fields the tie-break is routine, not
  exotic: with BTCUSDT tick sizes and a five-to-six-figure price,
  any even-tick spread puts the quoted mid on the valid price
  grid. Consequence for the queued rule, harder to pass: a
  queue-state-conditioned passive feature can satisfy the
  conditioning declaration — "the pre-event volume at the touched
  level, or the declared alternative" — while its conditioning
  state still depends on an undeclared labeling convention, an
  undisclosed degree of freedom that survives every admissibility
  gate and invites post-hoc selection among equally "declared"
  implementations. One pre-declaration. Queue-label convention
  declaration: whenever a conditioning functional is defined
  relative to a reference price or mid rather than to the event's
  own touch, the pre-registration must declare, recorded on TRAIN
  before L2 data arrives, the reference construction, the
  even-grid tie-break rule (previous-reference anchoring or the
  declared alternative), the level-indexing origin and the
  touched-level identification rule; readings with undeclared
  conventions are inadmissible. Functionals anchored entirely to
  the event's own touch on a feed-native price field satisfy the
  declaration trivially, and if every admissible functional on the
  programme's venue and fields is event-touch-anchored, the
  component guards nothing there and stays dormant on that route.
  Scope: the pending queue-state conditioning rule's declaration
  block only, a disclosure requirement; the C1-L2 and C8 spec
  texts, every kill line, T-H and T-O remain untouched; no
  threshold moves; nothing is armed.

  Findings, page-cited: reinforcing, no new item — queue-state
  conditioning is not redundant with flow excitation, and the
  state effects are event-type-specific: the liquidity state and
  time factor improve the Hawkes-only fit on all 20 days (Model 6
  minus Model 4, median per-sample AIC difference -0.23, 20 of 20
  days, Table 1, PDF pp. 31-32) and the fitted directions run
  opposite by event type, first-level trade, cancel and insertion
  intensities rising with queue state, second- and third-level
  insertion intensities falling (PDF pp. 27-28), a second corpus
  for the conditioning rule's premise that state-blind passive
  aggregates are inadmissible; no parameter transfers.
  Reinforcing, no new item — the accumulation dichotomy is a named
  sibling of the event-grain rule (deep-read session 25): regular
  events additive with sizes summed into the binned counts, the
  six reference-price-changing events pure points because they
  shift the queue distribution (PDF p. 16), with the order-size
  sensitivity run and disclosed afterward, qualitative
  conclusions surviving (PDF pp. 48-49, 55; Table S1, PDF p. 69);
  no threshold transfers. Interpretation caution — exponential
  kernel assumptions are visibly wrong for a class of events:
  non-exponential shapes recur for higher-level trade events in
  wide-spread states and the authors state it may be problematic
  to adopt the exponential shape across all events (PDF
  pp. 26-27, Figure 7; Figure S2, PDF p. 46), so any
  excitation-decay or Hawkes-family reading in a C1-L2 or C8 arm
  carries its kernel-form declaration as convention, and the
  fitted shapes are never cited as expected behavior of any
  market the programme measures. Interpretation caution — every
  "explanatory power" claim is in-sample AIC selection on one
  stock in one month: the decisive differences are minuscule
  per-sample numbers (median -0.58, -0.23, -0.08, Table 1, PDF
  p. 32), no out-of-sample or forecasting test appears anywhere,
  and stationarity and ergodicity are explicitly deferred to
  future research (PDF p. 34); a fitted AIC improvement is
  bookkeeping, not an edge, and the paper is never citable as
  evidence that any programme feature carries information.
  Reinforcing, no new item — intraday time clustering elevating
  the first and last 30 minutes with a sharp 15:55-16:00 increase
  (PDF pp. 11-12, 28-29) corroborates the C1-L2 spec's declared
  hour-of-day strata; the paper's 126-category bucketing never
  transfers. Source-quality note — three authors with Philip
  Protter a leading stochastic-process authority; squarely in the
  Queue-Reactive lineage, the sibling of the state-dependent
  Hawkes LOB paper deep-read at session 28; arXiv v3 from January
  2022, no journal record checked at reading; deliberately modest
  scope, one stock, one month, 20 days, level-3 book, all choices
  honestly disclosed; a solid, narrow, descriptive modelling
  paper graded exactly at that level; published version to be
  checked before formal citation. Killed-if-wrong: if queue
  labels on the programme's venue and fields are later shown to
  be convention-independent on every admissible functional (all
  event-touch-anchored on feed-native prices), the queued
  convention declaration guards nothing and should die back to
  the conditioning rule as it stands; if a conditioning state is
  ever published whose labels rest on an undeclared mid-relative
  convention, the same declared functional could be implemented
  differently post hoc, exactly the undisclosed-degree-of-freedom
  failure the component forecloses. Standing caveat: one stock,
  Apple; one month, January 2019; NASDAQ through LOBSTER ITCH
  reconstruction; level-3 book, regular hours, penny-tick US
  equities microstructure; no crypto, no BTCUSDT, no futures, no
  anonymous flow; all fitted shapes, bucket boundaries, time
  categories, bin size, support and LASSO parameter are dataset-
  and venue-specific. Laundering directions named: INTO — the
  queue-label convention mechanism, the event-type-specific state
  contrasts, the accumulation dichotomy and the time-clustering
  corroboration enter only as feature-design discipline, and no
  kernel shape, bucket boundary, bin size, support length,
  regularization parameter, intensity level, AIC figure or
  end-of-day spike enters any spec, default or calibration; OUT —
  the fitted kernel shapes, the liquidity-state curves, the
  time-factor profile and the AIC rankings are never cited as
  expected behavior of any market the programme measures, never
  as expected BTCUSDT book behavior, and never as evidence that
  any programme feature carries information.

Ratification queue after this session: TWENTY-SIX candidate
sharpenings (the twenty-five standing plus the queue-label
convention declaration rule joined here through deep-read session
32), zero armed. T1 remains armed awaiting the owner's word; the
blocked list stays blocked. Deep-read queue pointer: the next UNREAD
triage entry is "TradeFM: A Generative Foundation Model for
Trade-flow and Market Microstructure" (score 31, xe7dc7f). Nothing
measured, no kill line moved, nothing armed, nothing trades live.

## 41. Null-time session 37 (2026-11-19): deep-read session 33 — the TradeFM generative foundation model read; default grade, nothing queued

- **Library deep-read session 33** (the standing queue's next UNREAD
  pointer, score 31, xe7dc7f, consumed here):
  `paper/research/library/2026-11-19_tradefm_generative_foundation_deep_read.md`
  on Maxime Kawawa-Beaudan, Srijan Sood, Kassiani Papasotiriou,
  Daniel Borrajo and Manuela Veloso (J.P. Morgan AI Research, New
  York), "TradeFM: A Generative Foundation Model for Trade-flow and
  Market Microstructure" (arXiv:2602.23784v1, stamped 27 February
  2026): a 524M-parameter decoder-only Transformer trained on 10.7B
  tokens of raw US-equity trade events across more than 9,000
  tickers, with scale-invariant bps-relative features, an
  EW-VWAP-estimated mid in the deliberately partial trade-only view
  (PDF pp. 4-5, 15-16), mixed-base composite tokenization with bin
  edges calibrated on the first 30 days and 1st/99th-percentile
  outlier bins (PDF pp. 5-7, 20), and a closed-loop deterministic
  simulator; validated only on stylized facts and distributional
  fidelity — 2-3x lower K-S distance than a Compound Hawkes
  baseline on return distributions (Table 2, PDF p. 9), lowest
  distances on most order-flow marginals but losing to Hawkes on
  spreads (Table 3, PDF p. 10), moderate zero-shot perplexity
  degradation on held-out China and Japan (PDF pp. 10-11, 24) —
  with no predictive or edge experiment anywhere in the paper.
  Read against the one question, the verdict is the default grade:
  NO kill line changes, NO new candidate sharpening. Graded
  findings. Reinforcing, no new item — bps-relative feature
  construction shown distributionally stationary across more than
  9,000 assets and a full year of regime change where tick-based
  construction is not (Figures 7, 12, PDF pp. 15, 24-25), a
  corporate-scale second corpus for the already-queued
  scale-constant declaration; no bin edges, halflife or
  liquidity-tier cuts transfer. Reinforcing, no new item — the
  mid-price in a trade-only view is an estimator with a declared
  convention (two coupled EMAs, time-based halflife, PDF pp. 4-5,
  15-16), corroborating the queued estimator-mode component's
  premise; the C1-L2 L2 arm observes the book directly, so nothing
  extends. Interpretation caution — stylized-fact reproduction is a
  marginal-distribution test compatible with zero predictive
  information (the calibrated ZI null both passes and fails parts
  of it, PDF pp. 9, 23); it is the same logic as the C8 shuffled-
  arrival placebo and can never be cited as evidence that a
  programme feature carries information. Interpretation caution —
  perplexity and distributional-fidelity rankings (2-3x over
  Hawkes, zero-shot APAC transfer) are generative smoothness, not
  information content, and the authors themselves flag closed-loop
  model-simulator confounding as unresolved (PDF p. 10); treating
  either as an information ranking is a laundering move.
  Cost-survival ammunition — the paper's synthetic-rollout
  backtesting, stress-injection and RL-training agenda (PDF
  pp. 26, 29) names the failure a future K7-style layer must
  forbid: validating on generated data substitutes the
  generator's smoothed tails for the market's, and the
  simulator's spread behavior is the paper's own acknowledged
  weak point (Table 3, PDF p. 10); declared as assumptions any
  such layer must carry, the layer does not exist, nothing
  operational is touched. Source-quality note — an industry
  research report, arXiv v1 February 2026, unreviewed at reading,
  zero citations at acquisition, JPM disclaimer carried (PDF
  p. 12), proprietary unreproducible training data; a solid,
  well-disclosed generative-engineering paper with no
  claim-bearing material for C1-L2 or C8, graded exactly at that
  level; published version to be checked before formal citation.
  Killed-if-wrong: if the programme had allowed "a large model
  learned universal market structure" to support any claim, this
  paper is exactly the artifact that would have done the
  laundering — a 524M model with a 2-3x fidelity win and zero
  predictive claims; and any future cost-survival layer that
  adopted synthetic-rollout evaluation at face value would rest
  its cost estimates on the simulator's weakest fidelity point.
  The library-is-ammunition rule, the placebo discipline, and the
  declaration above are the inoculation.

Ratification queue after this session: TWENTY-SIX candidate
sharpenings (unchanged from session 36: the twenty-five standing
plus the queue-label convention declaration rule joined through
deep-read session 32), zero armed. T1 remains armed awaiting the
owner's word; the blocked list stays blocked. Deep-read queue
pointer: the next UNREAD triage entry is "Diffusive Limit of
Hawkes Driven Order Book Dynamics With Liquidity Migration"
(score 31, x5db64b). Nothing measured, no kill line moved, nothing
armed, nothing trades live.