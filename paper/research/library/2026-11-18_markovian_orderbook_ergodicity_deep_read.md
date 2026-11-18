# Ergodicity and diffusivity of Markovian order book models — deep-read note

Deep-read session 18 (null-time session 20). Weibing Huang & Mathieu Rosenbaum,
"Ergodicity and diffusivity of Markovian order book models: a general framework"
(arXiv:1505.04936, q-fin.TR; index metadata year 2015, v1): the general
Markovian limit-order-book framework in which the book is indexed around ONE
latent reference price and the shape process is proved ergodic with a
diffusive macroscopic price limit.

Read 2026-11-18, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xfccac8_ergodicity_and_diffusivity_of_markovian_order_book.txt,
~25 pp., page-marked). Next UNREAD triage-rank entry (score 37).

## The paper in one paragraph

The order book is represented by a single reference price pref (a latent
consensus price, explicitly not necessarily the mid, PDF pp. 3-4) plus a 2K
queue-size vector; order flows of random size arrive at state-dependent rates
fi/gi(q,n) (Equation 1, PDF p. 5), and pref jumps one tick at state-dependent
rates u(q), d(q) (Equation 2, PDF p. 6), so book updates affect price with a
delay rather than instantly (PDF pp. 2, 8-9). Under Lyapunov drift conditions
(essentially: uniformly bounded total jump intensities, Assumption 3.2, and a
uniform negative drift of every queue once it is larger than a threshold,
Assumption 3.3 / Example 2, PDF pp. 10-11), the shape process is V-uniformly
ergodic and positive Harris recurrent (Theorem 3.1 continuous time, 3.2
embedded chain, 3.3 with price jumps, PDF pp. 11-12); under a mean inter-event
time bound (Assumption 4.1, PDF p. 13) the rescaled reference price converges
to a Brownian motion in event time (Theorem 4.1, PDF p. 13) and calendar time
(Theorem 4.2, PDF p. 13), with volatility the long-run variance of the
stationary price-increment sequence, sigma^2 = E[c^2] + 2*sum E[c0 cn]
(Equation 7, PDF p. 13), driven by the mixing of increments; the same limit
holds for bid, ask and mid since they differ from pref by at most 2K ticks
(PDF p. 13). Cont-Larrard (K=1), Poisson K>1, Smith-Farmer zero-intelligence
and the Queue-reactive model are special cases (Section 5, PDF pp. 14-17).
No data appears anywhere in the paper.

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The macroscopic limit of this whole class is
   Brownian motion, and it is reached through the strong mixing of stationary
   price increments (Theorem 4.1/4.2, Equation 7, PDF p. 13). Within the
   model class there is no long-memory macro price; any claim that a
   microscopic LOB feature survives to the macro scale is therefore, inside
   this class, a claim about the finite-window pre-limit, which is exactly
   what C1-L2's short-horizon benchmarking already tests. Nothing here
   licenses relaxing the OFI-benchmark family; the diffusive null is the
   class's own boundary.
2. [reinforcing, no new item] Ergodicity of the book shape is earned, not
   assumed: it is bought with a uniform negative-drift condition on every
   queue above a threshold (Assumption 3.3, Example 2's simple form
   f - g < -r, PDF pp. 10-11). The stylized empirical shape of the LOB is
   then an invariant-distribution phenomenon (PDF p. 3). Depth-shape and
   depth-state readings are only licensed under a drift condition of this
   kind; the paper displays the assumption openly rather than smuggling it.
3. [reinforcing, no new item] The paper's own boundary: adding a
   non-Markovian component to the MARKET order flow (self-exciting, Hawkes)
   would require revising the whole mathematical approach, except for very
   specific cases, exponential Hawkes named (Conclusion, PDF p. 18). This is
   the same boundary the programme met in deep-read 17 (Horst-Xu, weak
   criticality of the exponential family): two independent frameworks put
   the exponential kernel exactly at the edge of what is tractable, which
   supports the declared kernel family staying as declared, and reinforces
   the queued near-critical regime-disclosure item's scope line.
4. [interpretation caution] The reference price here is latent and the book
   can update without any instantaneous price response (u/d rates, PDF
   pp. 6-9). This bars reading event-to-price attribution as instantaneous
   in this class: book events carry the price with a delay drawn from state
   dependent rates. Feature timing in C1-L2 already enforces point-in-time
   lags; this paper is consistent cover, not new permission.
5. [source-quality note] Internal date discrepancy in the extract: the title
   page reads "September 17, 2018" while the arXiv stamp on PDF p. 1 reads
   "arXiv:1505.04936v1 19 May 2015"; the acquisition index records v1/2015.
   Not resolved here, only flagged; the published version, if any, must be
   checked before any formal citation. Kept at triage score 37 with the
   session-9 audit flag standing.

## What this paper would have killed if we had done it wrong

Two laundering paths, both closed. (1) INTO the programme: quoting the
diffusive limit (Theorem 4.2, PDF p. 13) as proof that microstructure always
washes out, so short-horizon flow edges "cannot exist": that is an
asymptotic statement about a model class under fitted drift conditions, not
about finite-window real-tape predictability; it would have smuggled a
model-class platitude in as a kill argument against C1-L2's own tests.
(2) OUT of the programme: reading the ergodicity theorems (PDF pp. 11-12) as
"the LOB state is stationary in data, so depth-regime features are always
admissible": ergodicity in this framework is conditional on Assumption 3.3's
drift, which the theorems display and the tape never checks for free;
without the drift condition, an "equilibrium depth regime" reading is
unlicensed. The programme's existing discipline, features traceable to
stated conditions, is the immune system here.

## Standing caveat

Theory-only: every result is a theorem about a specified Markov class; all
empirical content lives in other papers (HLR 2015 named throughout). The
framework targets large-tick assets with K of order 10 limits (PDF pp. 2-3);
small-tick books are outside its design. The boundary distributions
(pi_K, pi_-K, pi_inc, pi_dec, PDF p. 7) are free parameters: ergodicity and
diffusivity hold for many intensity specifications at once, so the theorems
narrow nothing about which specific model generated any observed tape; they
contain no falsification content for C1-L2 or C8 and were read only for
boundary discipline. Nothing measured, no kill line moved, nothing armed,
nothing trades live.
