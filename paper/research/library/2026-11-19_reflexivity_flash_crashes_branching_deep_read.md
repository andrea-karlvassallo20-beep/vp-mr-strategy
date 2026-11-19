# Deep-read note — "Quantifying reflexivity in financial markets: towards a prediction of flash crashes"

**Session:** null-time session 41 (deep-read session 37, renumbered, parallel-slot substituted read; the
selection trail and one prior supersession are declared in the log entry).
**Authors:** Vladimir Filimonov (ETH Zürich), Didier Sornette (ETH Zürich / Swiss Finance
Institute). **Year:** 2011-2012 (arXiv:1201.3572v2, dated November 27, 2011, revised
April 17, 2012).
**Venue:** arXiv [q-fin.ST]; published record not checked at reading — the extract's
header is the v2 arXiv stamp; the published version (Quantitative Finance) must be
verified before formal citation. What the paper is: the original empirical branching-
ratio study — a one-variable Poisson-background plus exponential-kernel Hawkes model,
maximum-likelihood-calibrated in 10-, 20- and 30-minute windows on the flow of E-mini
S&P 500 futures MID-PRICE CHANGES at the CME, January 1998 to August 2010 (2.43 billion
records, 24.4 million mid-price change events inside Regular Trading Hours), measuring
the branching ratio n (fraction of endogenous events) and its time evolution, and
comparing the May 6, 2010 flash crash against the April 27, 2010 exogenous crash as a
two-event diagnostic of criticality. This is empirical work, but on a single instrument
of a single venue, with second-rounded timestamps and an exponential kernel.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legal-OA page-marked shelf extract
`docs/library/text/xf29859_quantifying_reflexivity_in_financial_markets_towar.txt`
(27 pp.), read in full. Selection trail, declared: assigned paper xc5ba34 verified
covered on main (deep-read 23); TradeFM verified claimed (deep-read 33); this slot's
x5db64b read was superseded by a parallel landing (deep-read 34) and its PR (#199)
closed unmerged; this slot's next read, the Rough Hawkes–Heston microfoundation paper
(xd08813), was verified uncovered at read time and read in full, but ANOTHER slot
holds an open PR covering the slug (identified before this session pushed anything),
so its landing on main will supersede this slot's copy; per the no-duplicate rule this
session then took the next UNREAD entry at re-read time: xf29859 (score 30, "Quantifying
reflexivity in financial markets: towards a prediction of flash crashes", rank 33 of
the triage queue), verified uncovered before the read — no note among the 36 existing
notes in paper/research/library/, no open PR covers the slug.

## Findings, graded (does any kill line move?)

NO kill line changed. NO candidate sharpening queued. Default grade: everything that
matters here is a worked empirical exhibit for rules already standing — the
near-critical regime-disclosure rule, the boundary-solution rule, the estimator-mode
register and the W-ladder (window) register, the per-branch rule, the
conditioning-window discipline, and the sealed-prediction record's own standard for
what counts as a precursor claim. The paper is also the single strongest citable
exhibit for the C8 A3 shuffled-arrival placebo's design. Nothing measured, nothing
armed, nothing trades live.

1. [reinforcing, no new item] The branching-ratio estimate is a KERNEL- AND
   WINDOW-BOUND quantity, and this paper is its cautionary worked example: constant
   background plus exponential kernel, MLE in 10/20/30-minute windows, KS
   goodness-of-fit rejections rise steeply with window length — 0.12% of 10-minute
   calibrations rejected at 5%, 1.64% of 20-minute, 12.64% of 30-minute, and more
   than 50% of one-hour calibrations (PDF pp. 10-11), with the authors attributing
   the rejections to intraday non-stationarity violating the constant-parameter
   assumption. The paper itself concedes the short-window truncation biases n
   DOWNWARD and misattributes endogenous events to the exogenous background µ
   (citing the truncation effect, PDF p. 14) — the estimate is a function of the
   estimator mode, exactly as the estimator-mode register and the per-branch rule
   say: no fitted n from any single estimator mode may serve as a calibration,
   tolerance, or expected value for the programme's venue, and any near-critical
   reading (n → 1) must disclose its kernel family and window ladder before it is
   interpreted (the queued near-critical regime-disclosure rule and boundary-solution
   rule; the Hardiman-Bouchaud power-law-kernel critique of this very estimator is
   already on the programme's shelf and in its record — the kernel-shape freedom is
   the known reason the "distance to criticality" reading is estimator-dependent).

2. [reinforcing, no new item] The paper's own placebo is a worked exhibit for the
   C8 A3 shuffled-arrival amendment, cited as design precedent, never as evidence
   about any market the programme measures: the authors Poissonize the intra-day
   event times while PRESERVING the price trajectory, the daily volume and the daily
   event counts, re-run the identical estimator, and show the branching ratio
   collapses to near zero in the reshuffled series — n is not a proxy for activity
   level but a measure of excitation structure (PDF pp. 13-14, Fig. 4D inset). This
   is precisely the A3 control's shape: destroy the temporal-excitation structure,
   keep everything else, and the reading must die. The paper demonstrates the placebo
   works under its null; it does not license any A3-free reading of the programme's
   venue. Any C8 or C1-L2 arm that reads a branching/excitation statistic must carry
   the shuffled-arrival placebo per the already-queued amendment — this paper is the
   external worked precedent, which is how a library is ammunition.

3. [interpretation caution, no new item] The "precursor" claim is two anecdotes,
   not a forecast: the April 27 vs May 6, 2010 comparison (matched 4.7x vs 5.3x
   volume multiples, n flat vs n spiking to 0.95 at 14:45 EST, PDF pp. 15-16,
   Fig. 5) has no base rate, no coverage analysis, no false-alarm accounting, and
   no out-of-sample evaluation — the title's "towards a prediction" is honest: no
   prediction is demonstrated. Under the programme's standard a precursor claim is
   admissible only from the sealed-prediction record (seal-before-resolve,
   accumulating in the nightly ledger), never from a retrospective two-event
   contrast; this paper may never be cited as evidence that a branching-ratio
   rise precedes anything on the programme's venue, and the misses-curriculum
   2x2 (already queued, null-time) is the honest base-rate design the anecdote
   lacks.

4. [interpretation caution, no new item] Timestamp resolution is load-bearing and
   the paper's handling is a disclosure exhibit for the L0 gate's discipline: the
   CME data are rounded to the nearest second, up to 194 simultaneous mid-price
   changes per second on the flash-crash day, and the authors "solve" this by
   RANDOMLY REDISTRIBUTING simultaneous events within each second, assuming
   within-second independence (PDF pp. 9-10). The assumption is validated by
   simulation of the FITTED Hawkes process itself — a placebo that only tests the
   estimator under its own null, not the market's true within-second structure. If
   the within-second ordering carries excitation structure, the redistribution
   corrupts it in an unknown direction. On the programme's venue the analogous
   discipline already exists and is stricter (the L0 gate's 100-timestamp audit
   and the intake unit asserts); the exhibit is a one-way citation: the programme's
   standard may be cited against this paper's assumption, never this paper's
   assumption as precedent for relaxing it.

5. [reinforcing, no new item] Venue and instrument specificity: E-mini S&P 500
   CME futures, 1998-2010, single most-active quarterly contract (96.7% of volume),
   human-plus-early-algorithmic era, equity-index microstructure with second-grain
   data. The regime narrative (n rising 0.3 → 0.7-0.8 with the growth of HFT, four
   regimes 1998-2010, PDF pp. 13-14) is a single-venue decade-long history; none of
   it transfers to BTCUSDT 24/7 crypto microstructure at the L2 grain, and the
   mid-price-change event definition (free of bid-ask bounce, PDF p. 5) differs
   from any programme event definition a spec may declare — the event-definition
   declaration is already covered by the queued label-conditioning family.

## What this paper would have killed if we had done it wrong

Three launders were live. If the headline ("more than 70% of price moves are
endogenous since 2007") had been imported as background truth about markets in
general, a single-venue, single-instrument, kernel- and window-conditional estimate
would have become a market law — the value of n is an estimator-mode output, and the
standing register forbids exactly that import. If the 1998-2010 trend had been cited
as "markets are approaching criticality, so trade the approach", a descriptive regime
history would have become a predictive claim the paper never tested. If the May 6
precursor anecdote had been cited as evidence that branching-ratio readings can
anticipate crashes on the programme's venue, a two-event contrast with no base rate
would have bypassed the sealed-prediction record — the only instrument through which
a precursor claim is admissible. The standing rules prevented all three, and the
paper's role in the record is fixed: the A3 placebo's external design precedent and
the estimator-mode disclosure family's worked empirical example.

## Standing caveat

Single instrument, single venue, second-rounded timestamps, exponential kernel,
10-30 minute windows, 1998-2010, published record unverified at reading (arXiv v2
stamp; the Quantitative Finance published version must be checked before formal
citation). All numeric values (n ≈ 0.3 in 1998, 0.7-0.8 after 2007, 0.95 at the May 6
peak, the KS rejection fractions, the volume multiples) are properties of this
dataset and this estimator mode; none may serve as any expected value, tolerance,
prior, or trigger on the programme's venue. The queue-reactive/passive-cancel frozen-
book regime the programme cares about (C5) is invisible to this model by construction
(a queue-frozen book stops generating mid-price changes, mechanically distorting any
event-count estimator, and the authors never address it). Laundering directions
named: INTO — nothing; no branching value, no regime dates, no window or kernel
specification, and no KS threshold may enter any spec, default, calibration, or null,
and the paper may not serve as a criticality null or a precursor prior for any C1-L2
or C8 arm without an owner-ratified pre-declared derivation on the programme's venue;
OUT — the paper may never be cited as evidence that endogeneity rises over time, that
markets approach criticality, or that branching readings anticipate crashes on any
market the programme measures; it may be cited only as design precedent for the A3
shuffled-arrival placebo and as the worked example of estimator-mode disclosure.
Nothing measured, no kill line moved, nothing armed, nothing trades live.
