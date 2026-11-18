# Deep-read session 28 — Morariu-Patrichi and Pakkanen, "State-dependent Hawkes processes and their application to limit order book modelling"

Library deep-read session 28 (null-time session 32, log entry ## 36).
Maxime Morariu-Patrichi and Mikko S. Pakkanen (Department of
Mathematics, Imperial College London; Pakkanen also Data Science
Institute, Imperial College, and CREATES, Aarhus University),
arXiv:1809.08060v3 [q-fin.ST], 17 September 2021, 33 pp. text
extract, page-marked. Read 2026-11-18, against ONE question: what
here would kill C1-L2 or C8 faster, or change their kill lines?
Source: legally acquired OA copy
(docs/library/text/x947263_state_dependent_hawkes_processes_and_their_applica.txt).
Assigned triage-rank entry (score 32, x947263). Next UNREAD
triage-rank entry (score 32, x78a2e8, "Forecasting High Frequency
Order Flow Imbalance").

## The paper in one paragraph

A state-dependent Hawkes process couples a self- and cross-exciting
multivariate event process with a finite-state process that switches
only at event times: the excitation kernel depends on the state, and
the state transition depends on the event type, mimicking the feedback
loop between order flow and the shape of the limit order book
(Definition 2.1, PDF p. 4; Theorems 2.3-2.4, PDF pp. 5-6). The
likelihood separates so that the state-transition probabilities can
be estimated independently of the point-process parameters, making
estimation no harder than an ordinary multivariate Hawkes fit (PDF
pp. 3, 8-9). On one year of LOBSTER level-I data for INTC (June 2017
to May 2018, 250 days, 12:00-14:30, nanosecond timestamps), two
specifications are estimated: ModelS with the bid-ask spread as state
and ModelQI with queue-imbalance bins as state (PDF pp. 11-14).
Excitation magnitudes and timescales are strongly state-dependent
(effective timescales 0.1 to 100 milliseconds; self-excitation
doubles when the spread widens to 2+ ticks); and the paper's headline:
measured endogeneity — the per-state spectral radius of the excitation
kernel — is itself state-dependent, systematically at or above the
critical value in disequilibrium states (spread 2+, heavy
queue-imbalance bins), so "critical reflexivity" is "a largely
state-dependent phenomenon, observed only in particular
circumstances" (PDF pp. 19-21, Figure 10 on PDF p. 22).

## Findings, graded

NO kill line changed. ONE new candidate sharpening queued, PENDING
OWNER RATIFICATION.

1. **[candidate sharpening, PENDING OWNER RATIFICATION]** The
   bar-level book-state mix disclosure component for the C8 A3
   micro-threshold rule, extending the PROPOSED shuffled-arrival
   placebo amendment (C8 spec, Amendment A3). Mechanism, page-cited:
   endogeneity measured by the Hawkes spectral radius is
   state-dependent — in ModelS the spectral radius in the
   disequilibrium state 2+ is systematically above the critical value
   1 while equilibrium-state values sit below it, and in ModelQI the
   heavy-imbalance states exceed 0.9 half the time and occasionally
   exceed 1 (PDF pp. 20-21, Sec. 4.8, Figure 10, PDF p. 22) — so a
   bar-level, book-state-blind n_c conflates the bar's state
   composition with the strength of the flow's excitation
   mechanism. Two consequences for A3, both harder to pass.
   (a) A bar can clear n_c > 0.8 because it spent time in
   disequilibrium states, not because the excitation mechanism
   changed; the micro indicator would then partly encode the bar's
   book-state mix, which is dangerously close to conditioning on what
   the macro cell already selects. Pre-declaration: every per-bar n_c
   reading in the A3 family must be accompanied, recorded on TRAIN,
   by the bar's declared book-state mix — the occupancy distribution
   over a pre-declared state variable computable from the same tape
   (spread regime, queue-imbalance-bin occupancy, or the declared
   alternative), with the state-blind n_c never reported alone.
   (b) The shuffled-arrival placebo severs more than temporal
   excitation: in a state-dependent world the state process jumps at
   event times, so time-shuffling arrivals also destroys the
   event-state sequence and the state-flow feedback that this paper
   shows drives the endogeneity readings. Pre-declaration: any
   production-minus-placebo gap must be reported with a declaration of
   what couplings the shuffle severs (temporal excitation and
   state-flow feedback), and a gap is inadmissible as evidence of
   "genuine endogeneity" without that declaration. Scope: the A3
   family only, as a disclosure requirement; A3 and every C8
   amendment remain PROPOSED and not armed; no kill line is touched,
   no threshold is moved, T-H and T-O are untouched; nothing is armed.

2. **[reinforcing, no new item]** Timestamp discipline corroborated
   at the source. LOBSTER nanosecond timestamps give more than 99
   percent unique timestamps for level-I orders, and the authors
   state that accurately establishing the order of events at the
   shortest timescales is essential for accurate Hawkes estimation
   (PDF p. 13). They also flag and repair a tied-timestamp artifact:
   a market order matched with n limit orders is recorded as n market
   orders sharing one timestamp, which they aggregate into a single
   event to avoid artificial simultaneous arrivals (PDF p. 13).
   Mechanism-level corroboration of the L0 gate's timestamp audit and
   of A3's pre-declared µs exchange timestamps; the tied-print
   aggregation rule is a named sibling of the record's
   multi-print/multi-fill event-grain discipline. No parameter
   transfers.

3. **[reinforcing, no new item]** Regime instability of excitation
   estimates, on the record's side. The day-to-day evolution of base
   rates mirrors the day-to-day total order counts, suggesting
   day-to-day activity variation is mainly exogenous (PDF p. 15);
   the kernel norms undergo a visible structural break at the 5
   February 2018 "return of volatility" (VIX +116 percent), with
   distinct pre- and post-break levels (PDF pp. 16-17, Figure 7 on
   PDF p. 19). Corroborates the standing MIHM caution against
   endpoint-level readings of a single branching estimate: measured
   excitation moves across regimes and, per this paper, across states
   within a day. Never carried across regimes; never read as an
   equilibrium classification.

4. **[interpretation caution]** A per-state spectral radius above 1
   is not market instability. The estimated process is stationary as
   a state-dependent whole (existence and uniqueness hold under
   bounded kernels, PDF p. 6); rho(x) above 1 in a disequilibrium
   state is a within-model excursion, and reading it as a
   flash-crash-prone or near-critical market would be a laundering of
   a model-internal quantity. Equally, the specific state
   definitions (two-state spread, five queue-imbalance bins, Cartea
   et al. bin edges, PDF pp. 13-14) are the authors' constructions on
   one large-tick stock; none transfers, and the programme's L2 arm
   would have to declare its own state variable if the queued rule is
   ratified.

5. **[source-quality note]** Two authors, Imperial College (Pakkanen
   also Aarhus/CREATES); arXiv v3 of a paper first posted 2018, last
   stamped 17 September 2021; a companion mpoints Python library is
   published; the paper builds on the authors' 2018 hybrid marked
   point process framework. The extract is page-marked and clean in
   the load-bearing sections (definitions pp. 4-6, methodology
   pp. 8-9, results pp. 14-22); some figure labels in the extract
   are glyph-mangled but the prose carries the results. Results are
   headline-reported for INTC only, with AMD, MU, SNAP and TWTR
   studied but relegated to "available from the authors upon request"
   (PDF p. 11); published version to be checked before any formal
   citation.

## Killed if wrong

If the state-dependence of measured endogeneity is later shown to be
an artifact of the state-bin construction — a mechanical coupling
between event rates and the binning itself — then the queued
book-state mix component loses its mechanism and should die back to
A3 as it stands, since the disclosure requirement would then guard a
problem that does not exist. Conversely, if A3-family n_c readings
are ever published without the state-mix disclosure and the bar's
state mix happens to track the macro cells, the micro indicator
would partially embed the macro conditioning, which is exactly the
costume failure K1 exists to catch, and the queued rule is what
forecloses it.

## Standing caveat

One large-tick US equity stock (INTC), Nasdaq level-I LOBSTER data,
June 2017 to May 2018, 12:00-14:30 windows chosen for flat intensity
(PDF p. 12); level-I only, deeper levels discarded (PDF p. 13);
exponential kernels with the authors' own acknowledgment that power
laws may fit better; no crypto, no BTCUSDT, no futures; the record's
own state variables, if ever declared, must come from the
programme's tape under its own rules. Laundering directions named.
INTO: the state-dependence mechanism enters only as the disclosure
discipline of the queued rule; no spectral radius, kernel norm,
state definition, bin edge, timescale range, or transition matrix
from this paper enters any spec, default, or calibration, and the
state-dependent Hawkes model is not adopted anywhere without its own
pre-registration. OUT: the per-state critical reflexivity readings
are never cited as evidence that any market the programme measures is
near-critical or unstable, never as expected BTCUSDT endogeneity, and
the 0.1-100 millisecond excitation timescales are never cited as
expected reaction scales outside this paper's own sample.
