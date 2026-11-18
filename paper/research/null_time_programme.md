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
  ~1%-R² smooths, in one two-month vacation window, at 5-minute grain, with no direct
  algorithm-share measurement — agent-mix statements may never be imported from
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
