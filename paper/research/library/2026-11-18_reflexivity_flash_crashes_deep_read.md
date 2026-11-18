# Library deep-read session 34 — Filimonov & Sornette,
# "Quantifying reflexivity in financial markets: towards a
# prediction of flash crashes" (arXiv:1201.3572v2, 2012, v2 stamp
# 2024; ETH Zurich / Swiss Finance Institute; the ORIGIN paper of
# the branching-ratio-as-endogeneity literature the whole queue
# descends from)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xf29859_quantifying_reflexivity_in_financial_markets_towar.txt`,
~27 pp., page-marked). Next UNREAD triage-rank entry (score 30;
verified unread by the read-slug mapping). Lineage flag: session 2
(Hardiman & Bouchaud) was a direct RE-EXAMINATION of this paper's
reflexivity results; the queued-but-unread "Apparent criticality
and calibration issues in the Hawkes self-excited point process
model" (score 30) is the critique paper — the queue is now reading
the origin AFTER its descendants, and that order is recorded.

## The paper in one paragraph

The paper that made the Hawkes branching ratio n a market
endogeneity measure: calibrating a self-excited Hawkes model with
constant background mu and exponential kernel to mid-price changes
of the E-mini S&P 500 futures (CME, 1998-2010, 10/20/30-minute
intraday windows), the authors find the fraction of endogenously-
generated price changes rose from ~70% exogenous in 1998 (n ~ 0.3)
to less than 30% exogenous since 2007 (n near criticality), in four
regimes coinciding with the dot-com run-up, the post-burst
rallies-and-panics period, the mid-2000s calm, and the 2007-2010
crisis era; growth coincident with the rise of algorithmic/HFT
trading (PDF pp. 8, 12-15). Robustness checks: agreement across
window sizes, and a POISSON RESHUFFLING placebo — same number of
daily price changes redistributed as an within-day Poisson process
— under which estimated n collapses, rejecting "n is just an
activity measure" (PDF pp. 13-14). A seasonality observation:
daily activity and the background intensity mu are strongly
U-shaped while the branching ratio n is NOT — endogenous impact
does not ride the intraday calendar (PDF p. 12). The proposal:
n as "distance to criticality," a nuclear-plant-safety-style
fragility metric for flash crashes (PDF pp. 1, 15-17).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] The origin paper's own printed
   limitations ARE the queue's caution architecture.** In their
   own words: short intra-day windows and a short-memory
   exponential kernel mean pre-window price moves are excluded, so
   the calibrated n values "are most likely UNDERESTIMATIONS" of
   the real ones (PDF p. 14) — the kernel-geometry constraint
   (session 28) and the exogenous-absorption caution (session 17),
   admitted by the founders in 2012. Never-read-branching-alone
   (per-branch rule, session 9; dispersion register, session 12;
   MIHM, session 20) descends from this paper's measured
   instabilities. Nothing queued; the house rules already encode
   the lessons, and this read adds the origin citation.

2. **[interpretation caution] "Towards a prediction" measured
   REGIME COINCIDENCE, not validated prediction — and the
   apparent-criticality critique is still on the shelf.** The
   four-regime n progression is descriptive alignment with
   narrative epochs (dot-com, post-burst, calm, crisis); no
   out-of-sample crash forecast was tested. The queued
   "Apparent criticality and calibration issues" (score 30) is
   the paper that showed near-critical estimates can be KERNEL
   artifacts (exponential kernel mis-specified against power-law
   decay) — until that read happens, the record treats this
   paper's near-critical post-2007 levels as a
   (construction x vintage)-conditional reading, not a market
   fact, exactly per the estimator-mode rule. Time-varying n is
   also composition drift's (session 22) direct ancestor.

3. **[reinforcing, no new item] The Poisson-reshuffling placebo is
   an early instance of the house label-placebo battery — and a
   good one.** Holding the daily event count fixed and destroying
   temporal structure collapses estimated n: the branching ratio
   measures dependence structure, not activity. This is the
   session-27/joint-family discipline's ancestor, and it
   reinforces the program's requirement that every fitted reading
   survive a null-structure placebo, not merely reproduce
   plausible values.

4. **[reinforcing, no new item] The seasonality split is a
   calendar-discipline ancestor: EFFECTS RIDE THE CALENDAR WHILE
   STRUCTURE DOES NOT.** mu (and volume, volatility) are strongly
   U-shaped across the day; n is not (PDF p. 12): calendar
   composition folds into rate-level statistics but not (measured
   here, at this grain) into the endogeneity structure — the
   sessions 15/22 calendar declarations gain their lineage
   citation, applied per-statistic: each statistic declares which
   calendar channel contaminates it.

5. **[source-quality note] Vintage-declared, single-venue lineage.**
   One contract (E-mini), one exchange, 1998-2010; the HFT-
   coincidence attribution is narrative-contingent (dated to SEC
   1998 order-handling changes); the distance-to-criticality
   proposal is prospective in this paper. arXiv v2 carries a 2024
   restamp of the 2012 work (published descendant exists in the
   quantitative-finance literature; the shelf copy is the arXiv
   version — check the published version before formal citation).
   Quote for the origin of the measure and its own caveats; zero
   portability to the program's venue, grain, or vintage.

## What this paper would have killed if we had done it wrong

If any spec had ever read a fitted branching ratio as a
free-standing market fact — the vulnerability this paper's own
caveats flag — the whole caution family exists because the
literature (this paper's descendants, sessions 2/9/17/28) showed
how badly such readings distort with kernel choice, window, and
exogeneity assumptions. And if a flash-crash fragility claim had
been built on near-critical n levels before the
apparent-criticality critique was read, it would rest on a
possibly-artifactual level; the queue's order (descendants first,
origin now) is recorded as an irony and a lesson: the founder's
admissions printed in 2012 were the seed of every protective rule
the program now enforces.

## Standing caveat

Single venue/contract and one 13-year vintage (1998-2010);
exponential kernel in 10/20/30-minute windows with the founders'
own underestimation admission; near-critical post-2007 levels
conditional on that construction (the critique paper remains
unread on the shelf — flagged as the imminent follow-up);
the HFT attribution is coincidental narrative, not causal
evidence; "towards a prediction" is aspiration, not result.
Nothing here touches the program's Binance perp venue, the daily
dossiers' grain, or T1's spell scale. Nothing trades live.
