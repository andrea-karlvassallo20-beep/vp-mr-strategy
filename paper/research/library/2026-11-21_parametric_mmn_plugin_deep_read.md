# Deep-read session 76 (null-time session 87, log ## 100) — the Clinet–Potiron parametric-microstructure-noise plug-in paper read; the entire fast-rate noise-robust machinery shown to stand on the null-residual-noise regime, the noise model φ and its limit-order-book variable set Q shown to be analyst degrees of freedom that move the measured residual-noise share from ~0% to 20-30%, and the plug-in guarantee shown to travel only in its declared configuration; ONE candidate sharpening queued (the noise-model pre-declaration for de-noised inputs)

Simon Clinet, Yoann Potiron (Faculty of Economics, Keio University),
"Estimation for high-frequency data under parametric market
microstructure noise" (arXiv:1712.01479v2 [math.ST], arXiv stamp
17 Sep 2020, title page "This version: September 18, 2020"; 42 pp.
page-marked extract, body, proofs and references complete; zero
recorded citations in the index, acknowledgments thanking two
anonymous referees, no journal version recorded). A high-frequency
statistical-theory paper: the observed log-price is decomposed as
efficient price plus a PARAMETRIC function of observable
limit-order-book state, and the paper proves that a whole family of
standard high-frequency estimators survive microstructure noise
unchanged — same limit law, same rate — once the efficient price is
pre-estimated by plugging in the fitted noise function.

Read 2026-11-21, against ONE question: what here would kill C1-L2 or
C8 faster, or change its kill lines? Source: legally acquired OA copy
(docs/library/text/xdab650_estimation_for_high_frequency_data_under_parametri.txt,
~42 pp., page-marked, complete). Next UNREAD triage-rank entry (score
24, xdab650), per the recorded ## 96/## 97/## 98/## 99 pointer and
re-verified against the live file state this session: the score-24
tier order in docs/library/edge_triage_scores.json is x673148 (read,
## 94), xe0397d (read, ## 96), then xdab650 — the pointer is correct,
no higher-scored entry is unread (the score-25 tier closed at ## 88
and the recovered read-status of every entry above score 24 was
re-checked against the note set and the log tail this session).
Session-state note, per the goal-autonomy conductor protocol (edition
7, ## 95): the declared work choice is the standing deep-read, the
protocol's default, which owes no justification; the synthesis cadence
is NOT due — after this session's read the EDITION-7 counter stands at
TWO of five (deep-reads 75-76 counted from the edition-7 reset at
## 95), with the edition-8 pass due at five; no other front is
claimable by a null-time session (the L2 deployment and its data spend
stay owner-side).

## The paper in one paragraph

The standard martingale-plus-i.i.d.-noise setup Z = X + ε (eq. 1,
PDF p. 1) is recast as the "pure" parametric-noise model Z = X +
φ(Q_t, θ0) with NO residual noise (eqs. 2, 11, PDF pp. 1-5): φ is a
known function of observable limit-order-book state Q with unknown
parameter θ0, the leading forms being Roll's half-spread I_tθ0
(eq. 3, PDF p. 2), Glosten-Harris with trading volume I_tθ0(1) +
I_tV_tθ0(2) (eq. 4, PDF p. 2), and the direction-times-quoted-spread
I_tS_tθ0 (eq. 5, PDF p. 2), with duration, quoted depth and order
flow imbalance named as further candidate Q-variables (PDF p. 5). Any
noise-parameter estimator θ̂ converging at the fast rate N(θ̂−θ0) =
OP(1) (eqs. 6/18, PDF pp. 2, 7-8; the MSE estimator reduces to a
linear regression of price increments on Q-increments when φ is
linear, eq. 22, PDF p. 8, with the rate theorem borrowed as
Proposition 1 from Li et al 2016, PDF p. 8) lets the statistician
pre-estimate the efficient price X̂ = Z − φ(Q, θ̂) (eqs. 19-20,
PDF p. 7) and run a standard high-frequency estimator on X̂ — and the
paper proves across five leading examples — threshold realized
volatility under endogenous sampling and infinite-activity jumps
(Theorem 2, PDF p. 10), threshold bipower variation (Theorem 7,
PDF p. 12), the Hayashi-Yoshida asynchronous high-frequency covariance
under the HBT hitting-boundary endogeneity model (Theorem 9, PDF
p. 13), functionals of volatility (Theorem 11, PDF p. 14), and
volatility of volatility (Theorem 14, PDF pp. 15-16) — that the
plug-in versions enjoy exactly the non-noisy central-limit theory,
same rates, same AVAR, unbiased studentized laws (Corollaries 4, 8,
10, 12, 15, PDF pp. 11-16). The whole machine rests on the empirical
claim that some φ explains the noise completely, and the paper recaps
its own evidence trail for that claim: residual noise is 20-30% of
MMN variance under Roll's form (four stocks, one day), Glosten-Harris
leaves 10-30% absence-of-residual-noise test rejection rates over a
full NYSE year (Chaker), and the direction-times-quoted-spread form
gets residual noise down to ~1% (31 CAC 40 constituents, one month)
and ~0% (50 random S&P 500 names, 2009-2017) — the authors call the
null-residual-noise assumption "quite a strong assumption (at first
glance)" (PDF p. 3), note that the ψi(θ̂) perturbation breaks
adaptedness and must be Taylor-repaired (PDF p. 7), and concede that
beating the i.i.d.-noise rate is "a different game" because the
plug-in consumes supplementary limit-order-book data (PDF pp. 3-4).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING
OWNER RATIFICATION (the noise-model pre-declaration for de-noised
inputs, the forty-first candidate, extending the estimator-
configuration freeze to the preprocessing stage). The other findings
are page-cited reinforcements and cautions, no queue change from
them.

1. [candidate sharpening, PENDING OWNER RATIFICATION] The
   noise-model pre-declaration for de-noised inputs: before the L0
   gate, any C1-L2/C8-adjacent computation, comparator, null or
   baseline that feeds a de-noised, reconstructed or
   "efficient"-price input — replacing the raw price by a plug-in
   de-noised price, or any feature built on one — must pre-declare
   the microstructure-noise functional form φ AND the exact
   limit-order-book variable set Q entering it, with the noise-model
   choice counted in the multiplicity ledger and every deviation a
   dated amendment before the data is touched; a number that survives
   only under a post-hoc swap of the noise model may not enter any
   spec as support. Mechanism, page-cited: the entire fast-rate
   plug-in theory holds only in the null-residual-noise regime, i.e.
   under the assumption that φ(Q,θ0) explains the microstructure
   noise COMPLETELY (eqs. 2, 11, PDF pp. 1-5), and the paper's own
   recount shows the residual-noise share is a function of the
   analyst's choice of φ: 20-30% of MMN variance under Roll's form
   on four stocks one day, 10-30% absence-rejection rates under
   Glosten-Harris over a full year, ~1% and ~0% only under the
   direction-by-quoted-spread form (PDF p. 3) — so a mis-specified
   φ leaves unmodeled residual noise that the theory excludes by
   assumption rather than eliminates, and a comparator could make an
   inconvenient structure dissolve into "noise" or emerge from it by
   silently re-choosing the de-noising form, which the estimator-
   configuration freeze did not reach because the freeze names the
   estimator's fitting configuration, not the preprocessing stage
   that defines its input. Harder-to-pass because a de-noised-input
   number that beats its raw-price counterpart only under a noise
   form chosen after seeing the data now fails at the gate instead of
   surviving as preprocessing; tightens the estimator-configuration
   freeze by extending the pre-commitment from WHICH estimator in
   WHICH exact configuration to WHICH noise model under WHICH book
   variables, and joins the spread-convention declaration rule on the
   same axis — a preprocessing choice is a distinct configuration
   counted in the ledger. QUEUED, not armed; the owner's word is the
   only trigger.

2. [reinforcing, no new item] The guarantee is conditional on the
   declared configuration, example by example: each of the five
   central-limit theorems carries its own declared sampling regime
   (regular observation versus the HBT hitting-boundary endogeneity
   model, eq. 34, PDF p. 13), truncation threshold and tuning
   sequence (w, ω̄, k, block size h, PDF pp. 10-17), the θ̂ fast rate
   itself (eq. 18, PDF p. 8), and the Taylor repair for the
   non-adapted ψi(θ̂) perturbation (PDF p. 7) — the same
   estimator-configuration freeze item (#37) and price-process-family
   invariance item (#38) discipline, page-cited re-exhibited on the
   statistical-theory side: theory travels only in the configuration
   it was proved in. No new axis.

3. [reinforcing, no new item] The paper records that the one-lag
   autocorrelation in mid-price returns is often found positive
   empirically, citing the Andersen et al 2017 two-regime extension
   of the martingale-plus-noise setting (PDF p. 5) — the sign-
   persistence admission null's family (#36): mechanical persistence
   in raw returns is a standing empirical fact acknowledged on this
   shelf before any book state enters, and de-noising choices
   interact with it. No new item.

4. [interpretation caution] "A different game": the parametric
   plug-in beats the i.i.d.-noise estimator family on convergence
   rate only because it consumes supplementary limit-order-book
   data (PDF pp. 3-4) — so a comparison between a de-noised
   statistic and a raw-price statistic is not like-for-like on
   information content either way; any C1-L2/C8-adjacent exhibit
   quoting a de-noised number must name its noise model, its Q-set
   and its θ̂-estimator before the two numbers may be read against
   each other. Reading discipline only; licenses nothing.

5. [cost-survival ammunition] The paper contains no transaction
   costs, no PnL and no execution; if a future K7-style
   cost-survival layer ever estimated friction or volatility-based
   cost proxies from de-noised prices, that layer must carry the
   noise-model pre-declaration as an explicit assumption, because a
   mis-specified φ leaves residual noise contaminating exactly the
   realized-variance-type quantities cost proxies are built from
   (PDF pp. 2-3). Declaration requirements only, never
   operationalized, nothing armed.

6. [source-quality note] arXiv v2 stamped 17 Sep 2020 with the
   venue id carrying the original December 2017 numbering
   (1712.01479); acknowledgments thank "two anonymous referees"
   (PDF p. 17), indicating journal review, but no published version
   is recorded in the index and zero citations; the empirical recaps
   supporting the null-residual-noise regime are equities-only
   (NYSE, CAC 40, S&P 500; PDF pp. 2-3), single-venue, and none of
   them touches crypto perpetual-limit-order-book tape, so nothing
   here establishes the regime transfers to the programme's data.
   Check for the published version before any formal citation;
   regardless, no claim here can serve as support for any programme
   claim.

## What this paper would have killed if we had done it wrong

Had any C1-L2/C8-adjacent statistic ever been computed on a
de-noised, reconstructed or "efficient"-price input whose noise
model was chosen after seeing the data, the programme would have
owned a silent analyst dial with the paper's own measurements as
proof of its range: the residual-noise share moves from ~0% to
20-30% of MMN variance on the same kind of tape with nothing changed
but the functional form of φ (PDF p. 3), which is exactly the
freedom to scrub inconvenient structure into the "noise" term or
leave it in the "efficient" price until a comparison passes. The
estimator-configuration freeze (#37) would have caught a retuned
estimator, but the preprocessing stage that defines its input was
not yet a declared axis on the queue — this read closes that gate as
a queued candidate before it becomes a leak. Had the equities
residual-noise shares been carried into the record as evidence that
de-noising "works" for crypto L2, the library-is-ammunition rule
would have been broken twice: they are another asset class's
context, and they are recaps of other papers, not this paper's own
measurements (PDF p. 3). And had the plug-in rate advantage been
read as a free lunch rather than "a different game" that consumes
supplementary book data (PDF pp. 3-4), a raw-versus-de-noised
comparison could have laundered an information-content difference
into a modeling one. Nothing here was measured, and nothing here
licenses any arming.

## Standing caveat

Pure asymptotic theory paper: no new empirical results of its own —
every empirical number is a recap of Li et al (2016), Chaker (2017)
and Clinet-Potiron (2019a, 2019b), all equities (PDF p. 3); the
null-residual-noise regime the whole machinery stands on is called
"quite a strong assumption (at first glance)" by the authors
themselves (PDF p. 3); every theorem additionally assumes the θ̂ fast
rate (eq. 18, PDF p. 8), a C³ impact function φ on a compact
parameter set and bounded Q (eq. 12, section 2, PDF p. 5), and the
volatility-of-volatility example requires continuous price AND
volatility processes (δ = δ̃ = 0, PDF p. 15), with jumps there an
open question; the page-marked extract mangles some displayed
equation typography (PDF-brace macros render as literal
"/bracehtipupleft"-type strings), so claims were checked against
equation context and surrounding text rather than glyph-exact
display reading. arXiv v2 with referees thanked, no published version
recorded: check for the journal version before any formal citation,
and treat every magnitude and every regime claim as non-transferable
to any C1-L2/C8-adjacent context.
