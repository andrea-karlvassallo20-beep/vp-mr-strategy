# Deep-read session 59 — "A buffer Hawkes process for limit order books"

**Session:** deep-read session 59 = null-time session 70 = programme log entry
## 74 (2026-11-20). **Authors:** Ingemar Kaj (Uppsala University) and Mine
Caglar (Koc University, Istanbul). **Title:** "A buffer Hawkes process for
limit order books". **Venue:** arXiv:1710.03506v1 [math.PR], stamp 10 Oct
2017, 23 pp. A pure-theory probability paper that reorganizes the
Hawkes mechanism so the market-order intensity is driven by the current
book size rather than by a memory kernel over past events.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x6ed313_a_buffer_hawkes_process_for_limit_order_books.txt,
~23 pp., page-marked). Next UNREAD triage-rank entry (score 27).

## The paper in one paragraph

The model is a Markov process Xt = (Λt, Γt, Nt) in which the classical
Hawkes shot-noise Λ (eq. 1, PDF p. 1) is no longer the intensity of the
market orders; it is the arrival intensity of LIMIT orders feeding an
M/M/∞-style book Γ (arrival process L, exponential order cancellation at
rate d, storage-process form eq. 5, PDF pp. 6-7), and the counting process
N of market-order executions carries stochastic intensity cΓt−, a
multiple of the instantaneous buffer size (eq. 3, PDF p. 5; generator
eq. 8, PDF p. 8). The stability condition is ac < b(c+d) (eq. 7, PDF
p. 7). The resulting N admits a branching-process-with-immigration
representation with mean offspring ν = ac/(b(c+d)) (eqs. 10-13, PDF
pp. 11-12), ultimate progeny Borel-distributed, with the Lambert-W
moment-generating machinery (PDF pp. 12-13). First and second moments
are explicit (Props 2.1-2.2, PDF pp. 9-10), the centered scaled market
order process converges to Brownian motion with variance λ0c·(c+d)⁻¹·
(1−ν)⁻³ (Theorem 4.2, PDF p. 17), and with two INDEPENDENT copies N±
the mid-price S = (N+ − N−)α/2 flows to Brownian motion with volatility
β = α²λ0c/(2(c+d)(1−ν)³) (PDF pp. 18-19). A stationary-increments
version with an explicit covariance formula is constructed (PDF
pp. 19-21). The outlook sketches moment estimation of ν from the
coefficient of variation of counts (PDF p. 21), an inverse-Γ impact
price model (PDF p. 21), and non-Markovian power-law and two-sided
contagious extensions that are named but not analyzed (PDF pp. 22-23).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [candidate sharpening, PENDING OWNER RATIFICATION] Level-versus-memory
   disambiguation for self-excitation claims. In this model the
   market-order intensity is cΓt−, the instantaneous book size, with NO
   temporal kernel on N (eq. 3, PDF p. 5; generator eq. 8, PDF p. 8) —
   yet N still shows genuine temporal clustering through mutual
   excitation around the buffer (branching representation, section 3,
   PDF pp. 11-12) and inflated count dispersion V(Nt) ∼ λ0c/(c+d)·
   (b(c+d)/(b(c+d)−ac))³·t (Prop 2.2, PDF p. 10). The mechanism:
   count statistics from a buffer-driven book are IDENTICAL in form to
   the statistics of a memory-kernel Hawkes process (cluster progeny
   Borel-distributed either way, PDF pp. 12-13), and the (Λt, Nt)
   marginal is provably not Markovian (PDF p. 8), the unobserved book
   size Γ being the confounder. So an elevated conditional count rate, a
   clustering measure, or a branching-ratio estimate computed on counts
   ALONE cannot distinguish temporal self-excitation from a concurrent
   liquidity-level effect; on so-calibrated data a naive Hawkes fit
   misattributes a size effect to a memory mechanism. Proposal: before
   the L0 gate, any C1-L2/C8-adjacent spec interpreting elevated
   conditional count rates, clustering, or branching-ratio/contagion
   estimates as TEMPORAL self-excitation must pre-declare a concurrent
   book-depth control arm that separates the level effect from the
   memory effect, with both directions reported before the data; an
   excitation-style structure observed only without that arm may not
   enter any spec as support. This tightens rule 1 of the
   pre-registration discipline, the same family as the self-excitation
   regime-window pre-declaration (queued 2026-11-19, deep-read 53) and
   the primary-metric pre-commitment (deep-read 55); it is
   harder-to-pass because it adds a mandatory control arm to every
   future self-excitation claim, arming nothing and moving no threshold.
   Killed-if-wrong counterfactual: without the rule, a count-based
   branching-ratio calibration on the L2 window could book a thick book
   as "excitation", and the C8 self-excitation arm plus the queued
   near-instability calibration items would then launder a liquidity
   level into a temporal mechanism — a false mechanism with a clean
   record behind it, the most dangerous artifact this programme can
   build.

2. [reinforcing, no new item] Near-instability inflation is again a
   parameter-space fact, not a market fact: asymptotic volatility β ∝
   (1−ν)⁻³ with ν = ac/(b(c+d)) (PDF p. 19), the mean rate Nt/t →
   λ0c/((c+d)(1−ν)) (PDF pp. 9, 15-16), and both diverge only as ν → 1,
   with the diffusion limit itself remaining Brownian at every stable
   parameter point (Theorem 4.2, PDF p. 17). Reinforces the queued
   near-instability / apparent-criticality calibration items and the
   branch-norm reporting duties. No queue change.

3. [reinforcing, no new item] The estimation sketch confirms the
   estimator-discipline family: the paper's own proposal for ν is a
   coefficient-of-variation moment match on observed counts, explicitly
   left as "a separate investigation" with no bias/variance analysis
   (PDF p. 21). A first-moment match on near-critical parameters, whose
   volatility consequence is cubic in (1−ν), is exactly the fragile
   estimator mode the queued items fence. No queue change.

4. [interpretation caution] The price limit is Brownian by
   construction: N+ and N− are assumed independent copies and each
   executed order moves the mid-price a constant α/2 (PDF pp. 18-19),
   the same family as the marking-convention caveat of the rough-
   volatility read (deep-read 58, log ## 73): any signed-flow/price
   correlation in raw data is a convention of the mark, not a
   microstructure law; a C8-adjacent signed reading must pre-declare its
   marking convention.

5. [source-quality note] A pure-theory paper: zero empirical
   calibration, zero data, 0 citations in the library index, arXiv v1
   in math.PR rather than a finance venue; the excitation chain uses a
   single exponential shot-noise profile and collapses the whole book
   into one scalar depth Γ; the power-law and two-sided contagious
   extensions are named and not analyzed (PDF pp. 22-23). Check the
   published version before formal citation.

## What this paper would have killed if we had done it wrong

If the programme had ever taken a count-based branching-ratio calibration
at face value — exactly what the estimation sketch on PDF p. 21 invites —
then on a buffer-shaped book the calibration would read book thickness as
excitation: the C8 self-excitation arm or the queued regime-window item
would have "identified" a mechanism that was simply a deep limit order
book, and the near-criticality calibration family would have turned a
liquidity-level regularity into a plausible temporal mechanism with a
clean-seeming record. The standing discipline is what blocked this:
nothing is measured during null time, no estimator is built from a
paper's own sketch, the dynamics-identification rule requires flow
statistics (not marginals) from any refutation instrument, and no
empirical claim from any paper enters the record as programme support.
A library is ammunition, not evidence; this paper is the sharpest
ammunition yet for why the level-versus-memory arm must exist before the
L2 data is ever touched.

## Standing caveat

The mechanism is demonstrated inside one specific Markov model: a single
aggregated depth Γ, one exponential kernel family, executions Vs. cancellations split by a constant ratio c/(c+d), and independence
of the buy and sell sides by assumption. None of these is a property of
a real two-sided limit order book; they are the model's conventions.
Read as evidence about the world, the paper licenses exactly one thing:
the POSSIBILITY that count statistics alone conflate level and memory —
which is why finding 1 is queued as a sharpening (a rule about how the
programme must look), not as a discovery about markets. arXiv v1, math.PR
stamp; verify against any published version before formal citation.
