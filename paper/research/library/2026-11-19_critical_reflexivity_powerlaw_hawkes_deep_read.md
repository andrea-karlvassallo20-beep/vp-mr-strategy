# Deep-read session 42 — Hardiman, Bercot and Bouchaud, "Critical reflexivity in financial markets: a Hawkes process analysis"

Library deep-read session 42 (null-time session 46, log entry
## 50). Stephen J. Hardiman, Nicolas Bercot and Jean-Philippe
Bouchaud (all Capital Fund Management, Paris), arXiv:1302.1405v2
[q-fin.ST], stamped 5 Jun 2013, "(Dated: November 27, 2024)" header
line at PDF p. 1 (the same odd date-header quirk noted in ## 48; the
header date disagrees with the arXiv stamp and is flagged, not
resolved); 9 pp. text extract, page-marked, complete (references PDF
pp. 7-9). The direct rebuttal line to the landed ## 45: modelling
mid-price changes of the E-mini S&P futures contract 1998-2011 as a
Hawkes process with a power-law kernel, the paper finds the branching
ratio n fluctuates around the critical value 1 for the entire
fourteen years, contrary to the Filimonov-Sornette finding of a
steadily rising subcritical n, and locates the discrepancy in the
choice of an exponential kernel and 30-minute windows. Read 2026-11-19,
against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/xdc14f4_critical_reflexivity_in_financial_markets_a_hawkes.txt,
9 pp., page-marked). Assigned triage-rank entry (score 30, xdc14f4;
consumed as the next unclaimed UNREAD named by the landed ## 49's
closing pointer; no skips this session: the pointer checked out against
the live branch/PR set — no note for the slug on main, no open pull
requests; the two reflexivity-slot9 branches were inspected and are
stale remnants of the landed ## 45, their logs ending at entry ## 45
with no claim on xdc14f4). Next unclaimed UNREAD triage-rank
entries: "Apparent criticality and calibration issues in the Hawkes
self-excited point process model: application to high-frequency
financial data" (score 30, xd18d70); behind it "Sequence
Classification of the Limit Order Book using Recurrent Neural
Networks" (score 30, x0fd75a). A successor session must re-read the
live main tail and the branch/PR set first.

## The paper in one paragraph

The paper revisits the landed ## 45's first claim (reflexivity has
increased) with a different estimation mode (PDF pp. 1-2): where
Filimonov-Sornette fitted an exponential kernel on 30-minute windows,
Hardiman-Bercot-Bouchaud fit a power-law kernel with exponential
short-lag cutoff — approximated as a weighted sum of exponentials for
the O(N) likelihood recurrence (Eq. (12), PDF pp. 3-4, m = 5, M = 15,
results robust to these) — on non-overlapping two-month windows
1998-2011, Regular Trading Hours only, U-shape detrended by the
reciprocal empirical intraday rate (Eq. (15), PDF p. 4), on
millisecond-stamped data with uniform randomisation within each
millisecond (PDF pp. 4-5). Result (Fig. 1, PDF p. 4): n changes little
and fluctuates around nc = 1 for the whole period, while the
high-frequency cutoff tau0 decreases roughly exponentially over time
(the authors note the Moore's-law comparison) and the base intensity
mu stays roughly constant apart from crisis spikes; the small positive
mu is attributed to the part of the power-law kernel extending beyond
the two-month fitting window (PDF p. 5). The decisive experiment
(Fig. 2, PDF p. 5): synthetic power-law Hawkes processes generated
with {mu, epsilon, n} = {0.02, 0.15, 1.0} and tau0 varying as
estimated, then analysed with the Filimonov-Sornette procedure
(exponential kernel, 30-minute windows, within-second
randomisation), reproduce the spurious finding exactly — a subcritical
n steadily increasing since 1998 from data that is critical by
construction. Non-parametric kernel estimation (Bacry-Muzy, monovariate
autocovariance route, PDF pp. 5-6, Fig. 3) confirms the power-law shape
with epsilon of roughly 0.15 in 1998, 2006, 2009 with different
cutoffs; residual analysis in transformed time gives KS distances 0.011
(1998) and 0.031 (2009) with the explicit caveat that enormous point
counts make the KS test reject any small misspecification (PDF p. 6).
Detrended Fluctuation Analysis on the 14-year counting process (PDF
pp. 6-7, Fig. 5) finds two regimes: Hurst exponent H of roughly 0.63
below about 1000 s (consistent with epsilon of roughly 0.15) and H of
roughly 0.95 above, implying a second, slower kernel regime with
epsilon of roughly 0.45 (Fig. 6, PDF p. 7, five-minute bins over the
full period, the kernel again integrating to unity), matching the
literature on slow volatility-correlation decay; the kernel is
therefore a two-power-law object, about tau^(-1.15) crossing over to
tau^(-1.45) around 1000 s (PDF pp. 7-8). The conclusion reads: bursts
of diverging activity are as inevitable now as in 1998, only their
time scale has shortened; the stationary critical case requires
mu = 0 (Bremaud-Massoulie without-ancestors processes, PDF pp. 2-3);
the authors conjecture the critical scenario common to most actively
traded markets and state plainly that a mechanism explaining why
markets sit precisely at criticality is still lacking (PDF p. 8).

## Findings, graded (does any kill line move?)

NO kill line changed. NO new candidate sharpening. Default grade; the
paper is a worked exhibit for registers already standing (the
estimator-mode register, the kernel-family register, the near-critical
regime-disclosure rule, the timestamp-disclosure exhibit, the
label-conditioning family), and the burden of proof for a sharpening —
a specific mechanism making a future test harder to pass — was not
met. Findings, page-cited:

1. **[reinforcing, no new item]** The synthetic rebuttal experiment
   (Fig. 2, PDF p. 5) is the strongest single worked exhibit in the
   programme's record for the estimator-mode register: a published,
   cited trend (a subcritical branching ratio rising steadily with
   algorithmic trading) is reproduced exactly from data generated
   with the opposite truth, with the entire artifact traced to three
   spec choices — short-memory kernel family, windows shorter than
   the kernel's reach, timestamp randomisation. The programme's
   register already bans single-mode citation; the β-factor lesson
   of the CKS verification line and the ## 48 ACD mapping are weaker
   cousins of this exhibit. Nothing added, the register already
   stands; the exhibit is also a design precedent for
   estimator-refutation placebos (generate from a known truth, run
   the challenger's pipeline, the artifact must reproduce) beside
   the ## 45 Poissonisation precedent and the C8 A3
   shuffled-arrival shape — cited as design precedent only.

2. **[interpretation caution]** The headline finding n of roughly 1
   is boundary-sitting and its conditions must travel with any
   citation: n is estimated on two-month windows whose length is
   shorter than the kernel's own reach (the residual mu is
   attributed to the kernel tail beyond the window, PDF p. 5); the
   stationary critical reading strictly requires mu = 0
   (Bremaud-Massoulie, PDF pp. 2-3) while every fit returns mu
   positive; and an estimate within a few percent of n = 1 sits
   exactly where the ## 48 Appendix-B bias discipline operates (MLE
   of the branching ratio near 1 is sample-length-dependent and
   downward-biased). Any "market is critical" import must disclose
   window, kernel family, timestamp treatment and the mu artifact,
   per rules already standing; no queue change.

3. **[interpretation caution]** The criticality argument runs one
   way: long-range dependence of the event rate forces n = 1 (the
   auto-covariance relation, Eqs. (5)-(7), PDF p. 2), so
   non-integrable event-rate memory implies criticality, but an
   estimated branching ratio near 1 does not by itself prove
   long memory — the paper's evidence chain runs through the
   non-parametric kernel (Fig. 3, PDF pp. 5-6) and the DFA
   two-regime structure (Fig. 5, PDF pp. 6-7), and the exponent
   relations (alpha = 1 - 2*epsilon, H = 1/2 + epsilon, Eqs.
   (8)-(11), (18), PDF pp. 2-3, 6-7) bind only inside 0 < epsilon <
   1/2. No citation of this paper may reverse the direction of its
   inference; read discipline only.

4. **[reinforcing, no new item]** Timestamp handling is the same
   one-way disclosure exhibit as the landed ## 45's: millisecond
   stamps randomised uniformly within each millisecond (PDF pp.
   4, 6), with the further honesty note that the 1998
   sub-second oscillations in the non-parametric kernel are
   declared a data-collection/aggregation artifact, not noise (PDF
   p. 6) — an external corroboration that sub-grain data artifacts
   survive into published estimates and must be audited at intake.
   The programme's L0 100-timestamp audit is the stricter standing
   discipline; this paper's assumption may never be cited as
   precedent for relaxing it.

5. **[reinforcing, no new item]** The two-regime kernel —
   epsilon of roughly 0.15 below about 1000 s, epsilon of roughly
   0.45 above, with the crossover scale itself depending on the
   event definition (10-20 minutes for mid-price-change counting
   versus about one day for the DFA of five-minute absolute returns,
   PDF pp. 6-7) — is a kernel-family register exhibit in both
   directions at once: on short-memory ACD data the ## 48 session
   watched a fitted power law collapse to an exponential-like
   shape; on long-memory data this paper watched the exponential
   miss a two-regime power law. Kernel shape as fitted is a
   property of the data's memory class, the window, the event
   definition and the binning; no kernel shape from any single
   fit, window or grain is ever citable. The register already
   stands.

6. **[source-quality note]** Three authors from a fund (CFM
   Paris), applied econophysics lineage; single venue, single
   instrument (E-mini S&P futures mid-price changes 1998-2011),
   second-to-millisecond resolution varying by year, and the same
   structural blind spot recorded for ## 45: a queue-frozen book
   stops generating mid-price changes, so the C5 frozen-book regime
   is invisible to this event definition by construction and the
   authors do not address it. The "common to most actively traded
   markets" claim is an explicit conjecture, not a result (PDF
   p. 8). arXiv v2 dated 5 Jun 2013 against an odd "(Dated:
   November 27, 2024)" header; journal record NOT checked at
   reading, published version and the Filimonov-Sornette
   reply/rejoinder line to be checked before any formal citation.

## What this paper would have killed if we had done it wrong

Had "markets are critical and have always been" been imported as
background truth, a single-venue, event-definition-conditional,
window-conditional estimate sitting on the boundary where its own
estimator's bias is largest would have become a market law, and every
future excitation argument would have started from an assumed
criticality. Had the landed ## 45's rising-n finding been kept on the
record without this rebuttal logged next to it, the library would carry
the challenged number without the challenge. Had the synthetic
rebuttal been over-read as a general license ("parametric Hawkes fits
are always artifacts"), a specific mechanism — short-memory kernel
plus short windows plus timestamp jitter fitted to long-memory
data — would have hardened into a blanket distrust that the paper
does not support (their own MLE fits and the non-parametric route
agree, Fig. 3, PDF pp. 5-6). The estimator-mode register, the
near-critical disclosure rule and library-is-ammunition prevented
all three, in both directions of the disagreement.

## Standing caveat

No market the programme measures: single venue, single instrument,
mid-price-change event definition (label-conditioning family governs
any programme reuse of such definitions), 1998-2011, resolution
varying by year, within-millisecond randomisation assumed. Every
number is conditional on the two-month-window power-law mode, the
U-shape detrending and the sum-of-exponentials approximation; n is
estimated within a few percent of the boundary its own stationarity
argument needs; mu is positive in every fit while the stationary
critical reading needs mu = 0, the gap attributed to window
truncation and never resolved; the mechanism for precise criticality
is, by the authors' own statement, missing. The conjectured
universality across markets is untested here. arXiv v2, journal
version and the FS rejoinder unchecked. Laundering directions named.
INTO — nothing: no branching value, no kernel exponent, no cutoff,
no Hurst exponent, no DFA procedure, no power-law family and no
criticality reading from this paper enters any spec, default,
calibration, tolerance or generative null, and the
critical-versus-subcritical disagreement in the literature may not
be settled on the programme's side by preference: both lines are
model-relative, venue-specific artifacts until measured on the
programme's own venue and fields under owner-ratified pre-declared
rules. OUT — never read backwards as "markets are provably
critical" (boundary-sitting estimate, window-truncation artifact in
mu, no mechanism), "reflexivity is constant, only its timescale
shrinks" (a single-venue, mode-conditional comparison), or
"exponential kernels are wrong" (a family-matching artifact, not a
universal; the paper's own exhibit shows both families fit
acceptably in their matching regime).
