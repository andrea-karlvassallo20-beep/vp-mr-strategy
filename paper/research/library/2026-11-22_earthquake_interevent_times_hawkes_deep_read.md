# Deep-read note — library session 96 ("Theory of earthquakes interevent times applied to financial markets")

- Session: null-time deep-read session 96 (null-time session 106, log ## 127),
  2026-11-22.
- Authors: Maciej Jagielski, Ryszard Kutner, Didier Sornette.
- Title: "Theory of earthquakes interevent times applied to financial markets".
- Venue/id: arXiv:1610.08921v2 [q-fin.ST], 28 Oct 2016, preprint submitted to
  Physica A (slug x97b372, per docs/library/expanded_index.json).
- What it is, one clause: a short applied note fitting the Saichev-Sornette
  closed-form PDF of interevent times of a self-excited Hawkes process with an
  Omori-Utsu power-law memory kernel to daily-grain interevent times between
  loss exceedances on 15 financial records.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x97b372_theory_of_earthquakes_interevent_times_applied_to_.txt,
~9 pp., page-marked). Next UNREAD triage-rank entry (score 20).

## The paper in one paragraph

The paper reinterprets the Saichev-Sornette earthquake-recurrence formalism
for financial loss exceedances: daily negative returns below a threshold -Q
define events, and the PDF of waiting times between successive exceedances is
fitted with the closed-form Hawkes prediction P(τ) ≃ λ f(λτ) under a constant
background ω and a normalized Omori-Utsu kernel Φ(t) = θ t0^θ / (t0+t)^{1+θ}
with p = 1+θ, θ > 0 (PDF pp. 2-4, eqs. 1-6). Thresholds are set so the mean
interevent time ⟨τ⟩ is 2, 5, 10, 30, 70 days; parameters (branching ratio n,
memory exponent θ, average rate λ, microscale t0^θ) are calibrated by maximum
likelihood per asset and then averaged across the 15 assets (IBM, BA, GE, KO,
DJI, FTSE, NASDAQ, S&P 500, BCO, WTI, and five FX pairs; PDF p. 4). The fits
look good on double-log plots (Fig. 1, PDF p. 5); n saturates at its imposed
upper bound 1 for every ⟨τ⟩ ≥ 5 days and θ ≈ 0.2-0.3 (Table 1, PDF p. 4),
which the authors read as compatibility with a critical regime and as
evidence of strong non-Markovian memory (PDF p. 4). The one quantitative
failure: the fitted rate λ does not equal 1/⟨τ⟩ as the Hawkes construction
requires; instead λ(⟨τ⟩) = a + b exp(-⟨τ⟩/τ0) with a = 0.17 ± 0.04, τ0 =
10 ± 2, b = 0.90 ± 0.07 (eq. 7, Fig. 2, PDF pp. 5-6), which the authors
attribute to volatility clustering being multifractal while the Hawkes
process is mono-fractal — and they concede the markets-are-critical
controversy "may be an artefact of its mono-fractal nature" (PDF p. 6).
Conclusions restate the successful phenomenological transplant from
seismology (PDF p. 7). Full references through [55] (PDF pp. 7-9).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The branching ratio saturates at its imposed
   upper bound: Table 1 reports n = 0.78 at ⟨τ⟩ = 2 days and exactly n = 1.00
   at every larger mean interevent time, with the bound explicitly "imposed
   to ensure stationarity" (PDF p. 4). A fitted parameter pinned to a
   constraint boundary means the unconstrained likelihood wanted the
   non-stationary side; the honest reading is that the stationary Hawkes
   moment condition is at detonation on this data, not that "financial
   systems are critical" (the paper itself hedges, citing the Hardiman-
   Bercot-Bouchaud vs Filimonov-Sornette controversy, PDF p. 4 and ref.
   [46, 48]). This is the branching-ratio / self-excitation stationarity
   discipline already in the record (Definition-side n = ∫µ, strict
   0 < n < 1, explosion a.s. for n ≥ 1; deep-read 95's survey note), printed
   as a live borderline case. Votes for the existing family. No queue
   change.
2. [interpretation caution] The λ ≠ 1/⟨τ⟩ violation is a printed instance of
   a fitted rate escaping its own definitional identity, explained post hoc by
   a new two-parameter-plus-offset scaling law (eq. 7) chosen because it
   "imitates a spurious power law" in the presented range (Fig. 2 caption,
   PDF p. 6). A future exceedance-family or interevent-family statistic must
   pre-declare its threshold grid and treat the rate-vs-mean-identity check
   as a diagnostic, not a fit target; both requirements are already carried
   by the estimator-configuration freeze (deep-read 63) as frozen
   configuration. This caution is the paper's main honest content: the
   mono-fractal Hawkes family under-describes the clustering it is fitted to,
   so a good interevent-PDF fit certifies nothing about the underlying
   excitation mechanism (PDF pp. 5-6). No queue change.
3. [interpretation caution] Pooled-parameter fitting hides per-asset
   misfit: parameters are first calibrated per asset by MLE, then averaged
   across the 15 records, and the averaged parameters are what the displayed
   curves use (PDF pp. 4-5). A cross-sectional average presented as a
   universal fit is a declared configuration choice, not evidence of
   universality; the paper's short error-bar range (Table 1 caption, PDF
   p. 4) reports parameter dispersion, not goodness of fit, and no fit
   statistic of any kind is printed. Feeds the existing estimator-mode /
   configuration-freeze discipline (deep-read 63) and the pooled-vs-conditional
   reading rule already standing from the Cox-ratio read (deep-read 59's
   pooled-accuracy lesson). No queue change.
4. [interpretation caution] Daily-grain, loss-exceedance-only events
   (15 assets, closing prices, thresholds set by target mean waiting time;
   PDF p. 4) bear no L2 information: this paper cannot license anything
   about book-level anticipation, and by its own mechanism (loss
   exceedances of fixed thresholds on daily returns) it lives entirely in
   the daily grain the C1-L2 base-rate confrontation (queued) already
   brackets. Its empirical universality claims are recorded here as
   standing context only, never as support for any program claim — the
   library-is-ammunition caveat binds. No queue change.
5. [source-quality note] arXiv v2, 9 pages, effectively a research letter:
   no goodness-of-fit numbers, no model comparison against the Denys et al.
   superstatistics baseline it improves on (beyond visual curves), fit
   quality judged on double-log plots, and the conclusion's universality
   claim rests on the pooled-parameter averages of finding 3. Check for the
   published Physica A version before any formal citation. No queue change.

## What this paper would have killed if we had done it wrong

Without the stationarity discipline already in the record, a future
self-excitation arm could have read Table 1's n = 1.00 exactly as the paper
flirts with reading it — "financial systems may be in or close to a critical
regime" (PDF p. 4) — laundering a parameter pinned to an imposed stationarity
bound into a substantive regime discovery, when the honest statement is that
the stationary model is at the edge of its existence domain and the
unconstrained fit would cross it (PDF pp. 3-4). Without the
frozen-configuration discipline, the eq. 7 scaling law — a three-parameter
functional form selected after seeing that the definitional identity
λ = 1/⟨τ⟩ failed (PDF pp. 5-6) — is exactly the kind of post-hoc repair that
the estimator-configuration freeze forbids: a re-functionalization chosen
after the data, presented as a "novel characterization". And without the
library-is-ammunition caveat, this paper's "universal scaling law of
interevent times" headline would have entered the record as evidence that
self-excitation with long memory is a property of markets, when what the
paper actually prints is that the mono-fractal Hawkes family fails its own
rate identity on the data and the fit's success is a phenomenological curve
match with no printed fit statistic (PDF pp. 5-6).

## Standing caveat

Everything here is daily-grain, single-asset-index level, closing-price
exceedances; nothing transfers to intraday or book-level claims without
independent measurement. Calibration is MLE with parameters averaged
cross-sectionally after per-asset fitting, a choice that trades honesty of
per-asset fit for a universal-looking curve. The threshold-to-⟨τ⟩ mapping is
itself a researcher degree of freedom (thresholds chosen to hit target mean
waiting times), so the "universality across scales" statements are indexed to
that choice. The mono-fractality failure is the authors' own limitation
statement (PDF p. 6) and stands: the fit describes the PDF of waiting times,
not the mechanism, and the criticality reading is contested in the paper's
own citations. arXiv v2; check the published version before formal citation.