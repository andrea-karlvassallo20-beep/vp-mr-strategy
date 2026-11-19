# Variance-Hawkes Process and its Application to Energy Markets —
# deep-read note

Paper: Joshua McGillivray and Anatoliy Swishchuk (both University of
Calgary), "Variance-Hawkes Process and its Application to Energy
Markets" (arXiv:2410.08420v1 [q-fin.MF], dated 14 October 2024, stamp
10 Oct 2024; zero citations). Triage: score 29, slug
x618573_variance_hawkes_process_and_its_application_to_ene
(edge_triage_scores.json). Extract: 24 pages, page-marked, complete
(docs/library/text/x618573_variance_hawkes_process_and_its_application_to_ene.txt).

Read line: Library deep-read session 46, null-time session 50,
2026-11-19. Selected per the previous session's pointer (score 29,
x618573), re-verified unread against all library notes on main at read
time; no open PR covers it. Read in full against the ONE question:
what here would kill C1-L2 or C8 faster, or change their kill lines?

Session-state note declared before the read: this session is parallel
slot 24 of 24, assigned the liquidity-migration paper (x5db64b). At
write time the assigned paper was already covered on main by deep-read
session 34 (log entry ## 42, note
2026-11-19_liquidity_migration_diffusive_limit_deep_read.md), which
declared the slot-24 landing superseded per the burst-slot precedent.
Per the standing rule, this session consumed the queue's next UNREAD
entry instead; the dormant branch slot24-liquidity-migration-deep-read
carries one superseded note commit and must never be merged.

## The paper in one paragraph

The authors define the "variance-Hawkes" process, a standard Brownian
motion time-changed by a simple exponential-kernel Hawkes count
process, V_t = B(N_t) (Definition 1, PDF p. 6), argue that a
discontinuous (pure-jump) subordinator is natural when prices update
at trade arrivals (PDF pp. 5-6), and hand-fit the composition to 2018
and 2019 WTI crude and NYMEX natural gas front-month futures log
returns using log-returns = a + b*sigma-hat*B(N_t) with parameters
chosen "by hand using trial and error" because "we have not yet
derived and vetted calibration techniques for B(N_t)" (PDF pp. 7-9,
Figs. 2-5; the authors' own words). Supporting evidence is two
exhibits: per-minute trade volume quantiles deviating from simulated
exponential quantiles (Figs. 6-7, PDF p. 10), and intraday volume
clustering toward midday and late afternoon (Figs. 8-9, PDF p. 11),
both read as favouring a Hawkes arrival model over a Poisson one. They
derive the generator of the triplet (lambda_t, N_t, B(N_t)) term by
term (Eqs. 11-22, PDF pp. 12-14), obtain Var(B(N_t)) = E(N_t) by
conditioning (PDF p. 13), give the Ito formula dB^2(N_t) =
2B(N_t)dB(N_t) + dN_t (Theorem 1, PDF p. 14), state the distribution
B(N_t) =d sqrt(N_t)*N(0,1) as an unproven Conjecture 1 backed only by
Monte-Carlo density overlay (PDF p. 15, Fig. 14, PDF p. 20), and close
with explicit second/cross moments of lambda_t and N_t via MATLAB
symbolic algebra (Appendix B, PDF p. 24, Eqs. 24-32). Simulation
agreement between the two sides of the Ito formula carries
percentage errors mostly within +/-20 percent with spikes above 100
percent attributed to the discretization (Figs. 15-17, PDF pp. 15,
21-23).

## Findings, graded (does any kill line move?)

NO kill line changed. NO new candidate sharpening. The paper is a
price-model construction note with illustrative, hand-calibrated fits
on a venue family (daily front-month energy futures closes, Marketwatch
data, PDF p. 17) that shares no observable with the programme's L2
perp replay; nothing in it bears on C1-L2's seven lines or C8's
K1-K11, and no finding met the burden for a sharpening. All findings
are reinforcement of standing rules and reading cautions:

1. [reinforcing, no new item] Var(B(N_t)) = E(N_t) and dB^2 =
   2B dB + dN: under event-clock subordination, price variance IS the
   event count, algebraically (PDF pp. 13-14). The paper's own
   construction is the cleanest possible statement of what C1-L2 kill
   lines 2 and 5 and C8's K8 exist to catch in the wild: whenever a
   zero-mean return process is driven through an event-count clock,
   the "volatility feature" and the "flow-clock feature" are the same
   variable in two costumes, and conditioning one on the other is
   conditioning a variable on itself. Nothing new is needed; the
   vol-tautology battery and the flow-clock family (queued items)
   already bind exactly this.

2. [interpretation caution] Overdispersion does not identify Hawkes.
   The paper's entire empirical case for a Hawkes arrival law is
   quantile plots of per-minute trade volume against simulated
   exponential quantiles (Figs. 6-7, PDF p. 10) plus intraday volume
   clustering (Figs. 8-9, PDF p. 11): both exhibits show only that
   arrivals are overdispersed relative to Poisson and diurnally
   clustered. Renewal processes with non-exponential interarrivals,
   any mixed-Poisson, and any diurnally-inhomogeneous Poisson produce
   the same two exhibits. The inference "quantiles reject exponential,
   therefore self-excitation" is necessary-not-sufficient reasoning,
   stated nowhere in the paper as a limitation. Discipline: no
   program document may cite QQ-type overdispersion as evidence of
   endogeneity/branching; identification requires the kernel-fit
   disciplines already queued (per-branch readings, ACF-shape gates,
   estimator disclosure). This paper is never citable as support for
   any self-excitation claim on the programme's venue.

3. [interpretation caution] The hand-fitted regime sits near the
   boundary: fitted parameters v0 = 401, v = 400, beta = 800,
   alpha = 700 (Figs. 2-5, PDF pp. 8-9) give a branching ratio
   alpha/beta = 0.875, and the fit was produced by trial and error
   against distributional overlay only, with no test statistic, no
   likelihood, no held-out data (the authors say so themselves, PDF
   pp. 7-8). A near-critical branching regime reproduces clustering
   shapes trivially, which is exactly why K7 and the queued
   boundary-solution rules exist; and an unvetted subjective
   calibration cannot anchor any threshold. No parameter, no
   alpha/beta reading, and no fitted figure transfers anywhere.

4. [reinforcing, no new item] The paper's own caveat that B(N_t) "is
   not intended to model prices outright" but "as a tool that can be
   easily added onto other models" (PDF p. 8), with the log-return model
   containing no mean reversion, illustrates the direction-versus-
   machinery discipline the programme already applies: a
   volatility-shape model with no directional content licenses
   nothing about WHEN or WHICH WAY. The Favetto-style inference chain
   "if arrivals follow Hawkes, price spikes may too" (PDF p. 5,
   speculative, from one European intraday electricity Q-Q study) is
   a caution, not evidence.

5. [source-quality note] arXiv v1, two authors, zero citations, dated
   14 October 2024; the headline distributional claim is a CONJECTURE
   (Conjecture 1, PDF p. 15), unproven, verified only by simulation
   overlay; the Appendix B moment expressions are symbolic-algebra
   dumps with typos in the extract (E(N_t^2) labeled via "E_t" and
   "F_t" identical to the cross-moment's C_t/D_t, PDF p. 24), and the
   text carries typographical slips ("simulaitons", "-%20 and %20",
   PDF pp. 15, 23). None of this needs repair for the programme's
   purposes because nothing is cited from the empirical side at all;
   check for a published version before any formal citation of the
   generator or Ito results.

## What this paper would have killed if we had done it wrong

Two specific failure modes, both already foreclosed. First, if any
future spec step had cited this paper's quantile exhibits as evidence
that "trade arrivals are Hawkes, therefore the compression clock
measures endogeneity", the programme would have laundered
Poisson-overdispersion plus diurnal seasonality into a self-excitation
claim; the paired findings 2 and 3 of this note exist so that no
successor session can, and the queue's identification rules are the
standing guard. Second, if B(N_t)-style subordinated constructions had
been used to motivate a flow-clock volatility feature and that feature
then evaluated against a variance target, the paper's own algebra
(Var = E(N), the dN_t quadratic-variation term) says the feature and
its target are one variable: the fit would have been guaranteed and
meaningless, the exact laundering kill lines 2/5 and K8 are armed
against. A third, smaller counterfactual: the hand-fitted alpha/beta =
0.875 near-critical regime could have been quoted as "energy markets
sit near criticality, and so does our venue by analogy"; the trial-
and-error origin of that number, in the authors' own text, kills the
analogy before it starts. Grade: no kill line changed; no candidate
sharpening; zero armed.

## Standing caveat

A library is ammunition, not evidence. The empirical content is four
hand-calibrated distributional overlays on one year each (2018, 2019)
of front-month WTI and NYMEX natural gas futures daily closing prices
obtained via Marketwatch (PDF pp. 7-9, 17), two quantile exhibits and
two volume-profile exhibits on 2024 data, and simulation experiments
with acknowledged discretization artifacts (PDF pp. 15, 21-23). No
statistical test appears anywhere; no calibration method is vetted;
the distributional identity is conjectural; exponential kernel only;
no crypto, no perps, no limit order book, no L2 observables; and the
paper's own framing targets model-building convenience, not
prediction. Nothing in it enters any spec, default, kill line,
threshold, or calibration; it charges warnings only. arXiv v1 with
no published version found at reading (uncertain, flagged for
verification).
