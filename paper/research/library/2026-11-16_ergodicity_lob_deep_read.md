# Library deep-read session 13 — Huang & Rosenbaum, "Ergodicity and
# diffusivity of Markovian order book models: a general framework"
# (arXiv:1505.04936v1, 2015; LPMA/UPMC & Kepler-Cheuvreux; the
# theoretical companion of the Queue-reactive model)

Read 2026-11-16, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/xfccac8_ergodicity_and_diffusivity_of_markovian_order_book.txt`,
~25 pp., page-marked). Next UNREAD triage-rank entry (score 37).

## The paper in one paragraph

A general Markovian framework for limit order book modeling: the
book is represented by K queues on each side of a single REFERENCE
price p_ref — a "market consensus about the underlying efficient
price" that is NOT necessarily the mid and is not directly
observable from the book state (PDF pp. 1-4). Order flow
insertions/cancellations/market orders carry state-dependent
intensities f_i(q,n), g_i(q,n); p_ref moves by one tick with
state-dependent rates u(q), d(q), and — departing from most
existing models — the impact of order book updates on the
reference price is NOT assumed instantaneous (PDF pp. 3-4). Main
results: under bounded-intensity and downward-drift assumptions on
oversized queues, the queue process is non-explosive, V-uniformly
ergodic, positive Harris recurrent (Theorem 3.1); the embedded
chain (book state, tick increment) is likewise ergodic (Theorem
3.3); and the rescaled reference price converges to a Brownian
motion with macroscopic variance a FUNCTIONAL OF THE FLOW RATES
(Theorems 4.1-4.2): sigma^2 = E_pi*[c_0^2] + 2*sum E_pi*[c_0*c_n] in
event time, with a calendar-time correction carrying the expected
inter-arrival time E[tau] (PDF pp. 12-13). The Cont-de Larrard,
Zero-intelligence, and Queue-reactive models are all exhibited as
special cases with verifiable assumptions (PDF pp. 14-17).

## Findings, graded (does any kill line move?)

**NO kill line changes. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four sharpened feature
pre-conditions stand. This read is the formal completion of a
warrant the queue ALREADY leans on; its gifts are recorded as
reinforcing evidence:

1. **[reinforcing, no new item] The ergodicity warrant for C5's
   queue-reactive null.** The null queued at the library ritual's
   paper 4 — "the state-conditioned intensities estimated on the
   gated data itself define what ordinary ergodic queuing
   produces; any abnormal-withdrawal reading must EXCEED it" —
   needs exactly two theoretical facts: that the book's invariant
   distribution EXISTS, and that a finite window estimates it.
   This paper supplies both: V-uniform ergodicity (Theorem 3.1)
   is precisely the mixing that licenses finite-window estimation
   of the state-conditioned intensities, and the empirical
   stylized shape of the book (Bouchaud-Mézard-Potters regularity)
   is the invariant distribution's trace (PDF p. 3). The null was
   queued honestly before its warrant was on file; the warrant is
   now cited. The Queue-reactive model itself is verified inside
   this framework as a special case (PDF pp. 16-17).

2. **[reinforcing, no new item] Volatility is a DERIVED functional
   — the C1 vol-tautology warning, formalized.** The macroscopic
   sigma^2 is not a primitive: it is the long-run variance of
   tick-increments OF THE BOOK'S OWN FLOW RATES, including their
   autocovariance terms (eq. 7, PDF p. 13). This is the exact
   structure the deployed vol-tautology check guards: any
   compression/priming feature built from variance SURROGATES is
   measuring a functional of state-conditional flow rates, and the
   check's insistence that features survive the tautology filter
   now has its structural citation — the efficient price's
   volatility is DOWNSTREAM of the queue's flow rates, never a
   parallel object.

3. **[reinforcing, no new item] The clock is part of the
   specification.** The same embedded chain yields different
   macroscopic parameters under different clocks: event time and
   calendar time differ by the factor sqrt(E_pi**[tau]) waiting
   time (Theorem 4.1 vs 4.2, PDF p. 13). This aligns with, and
   independently supports, the two already-frozen/queued clock
   decisions: A4's fixed volume clock and the estimator-mode
   rule's declared-window requirement. The clocks are never
   switched mid-analysis, and any cross-paper comparison of
   readings must first reconcile clocks — recorded as
   interpretation language, not a new rule (A4 is frozen; nothing
   is added to it).

4. **[reinforcing, no new item] Delayed, not instantaneous,
   impact.** The framework's explicit departure — book updates
   shift the reference price with state-dependent rates, not
   instantly (PDF pp. 3-4) — is the formal shape of the Tesla-day
   anatomy C5 carries (withdrawal at the touch shifts the hazard
   of the period break, with delay between the book change and the
   price change). The "while price is flat" clause's break event
   is a competing risk with state-conditioned hazard here, which
   is exactly how the C5 harness (d)'s risk set already treats it.

## What this paper would have killed if we had done it wrong

If the queue-reactive null had been armed as an estimated
state-conditioned baseline WITHOUT an ergodicity warrant, its
first failure would have been blamed on the estimator, not the
theory — an unfalsifiable escape hatch. The warrant (item 1)
closes it: the null's finite-window estimation is now licensed by
a theorem, and its failure would rightly reflect on the mechanism.
Beyond that, this paper changes nothing, and honesty requires
saying so plainly. Grade: **no kill line changed; no candidate
sharpening; four reinforcing notes; the ratification queue stands
at FOURTEEN candidates, zero armed.**

## Standing caveat

A library is ammunition, not evidence. This note cites; it never
launders. The ergodicity assumptions (bounded intensities,
downward drift on oversized queues — Assumptions 3.1-3.5) are
sufficient conditions on the MODEL, not properties proven of any
real venue: a gated window that violates them (runaway queues,
state-dependent intensity blowups, one actor dominating the flow)
is outside the warrant, and the null must not be lectured from
this paper on such a window — the wash-trading and manipulation
audit items govern there. The reference price p_ref is a model
construct (not observable); it is not, and must not be cited as,
a program "efficient price" claim. arXiv v1 (2015, theoretical
companion of the peer-reviewed Queue-reactive line); check for
the published version before formal citation.
