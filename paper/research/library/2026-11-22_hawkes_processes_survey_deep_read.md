# Deep-read session 95: Patrick J. Laub, Thomas Taimre, Philip K. Pollett, "Hawkes Processes"

Session: null-time session 105 (log entry ## 126), 2026-11-22.
Authors: Patrick J. Laub, Thomas Taimre, Philip K. Pollett (University of
Queensland; Laub also Aarhus University), per docs/library/expanded_index.json.
Full title: Hawkes Processes.
Venue: arXiv:1507.02822v1 [math.PR], last edited 13 July 2015, article id
xf8b5bc (topic arxiv-hawkes2). One clause: a pedagogical survey of the linear
Hawkes process — definitions, the immigration-birth (branching)
representation, covariance and power spectral density, the nonlinear and
mutually-exciting generalisations, financial applications (contagion,
mid-price change modelling), maximum-likelihood estimation, goodness-of-fit
via the random time change theorem, and exact simulation methods.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/xf8b5bc_hawkes_processes.txt, ~28 pp., page-marked).
Next UNREAD triage-rank entry (score 20, fifth of the score-20 tier).

## The paper in one paragraph

A survey written for accessibility, not for novelty: counting/point
processes, conditional intensity and compensator (PDF pp. 2-4); the linear
Hawkes definition with lambda* = lambda + integral of mu dN, exponential and
power-law excitation kernels (PDF pp. 5-6); the immigration-birth branching
representation with branching ratio n = integral of mu over (0,inf), n =
alpha/beta for the exponential kernel, asymptotic normality under 0 < n < 1
and a.s. explosion for n >= 1 (Theorem 1 and surrounding, PDF pp. 6-8);
covariance density R(tau) = alphabeta*lambda(2beta-alpha)/(2(beta-alpha)^2)
e^{-(beta-alpha)tau} and the shifted-scaled-Cauchy power spectral density
for alpha < beta (Theorem 2, PDF pp. 9-11 and Appendix A, PDF pp. 26-27);
nonlinear (Bremaud-Massoulie) and mutually-exciting generalisations
(PDF pp. 11-12); financial applications — the Hawkes diffusion contagion
model of Ait-Sahalia et al. and the Filimonov-Sornette mid-price-change
stylisation with its branching-ratio trend and the Lorenzen timestamp
critique (PDF pp. 12-14); MLE with the O(k) recursive log-likelihood
(remark that (N, lambda*) is then Markov), small-sample bias, local optima,
kernel sensitivity and the GMM alternative's "rather arbitrary" smoothing
(PDF pp. 14-17); goodness of fit via the random time change theorem mapping
the fitted compensator to a unit-rate Poisson process, tested as iid Exp(1)
interarrivals (QQ, KS/AD, Lewis, Brownian-approximation tests, PDF pp. 18-20);
and three exact simulation algorithms (inverse compensator, Ogata's
modified thinning, immigration-birth clusters, PDF pp. 20-24). The empirical
content is zero throughout: every figure is simulated, and the survey itself
flags that its estimation section is tested "over simulated data, for the
sake of simplicity and lack of relevant data", quoting the caution that
"calibrating the Hawkes process is akin to an excursion within a minefield"
(PDF pp. 14-15).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] Branching-ratio arithmetic in its cleanest
   form: n = integral of mu = alpha/beta for the exponential kernel, the
   stationarity condition is 0 < n < 1, and for n >= 1 the intensity
   diverges exponentially and the process explodes a.s. (PDF pp. 7-8);
   under stationarity a uniformly random arrival is endogenous (a child)
   with probability exactly n and exogenous (an immigrant) with probability
   1 - n (PDF p. 8). This is the definition-level statement of what the
   branching-ratio discipline already demands of any future fit on L2
   event data: an estimated n is interpretable as an endogeneity fraction
   ONLY inside a stationary, non-exploding fit, and an n drifting across
   1 is not a regime shift to report, it is a model whose stationary moment
   has ceased to exist. Votes for the existing branching-ratio /
   self-excitation stability family; no queue change.
2. [reinforcing, no new item] The Lorenzen critique is printed in the
   survey's own financial section: Filimonov-Sornette worked on
   second-resolution timestamps with simultaneous arrivals (impossible for
   a simple point process), added Unif(0,1) second fractions, and the
   randomisation "added an element of smoothing" that fit the model better
   than the true millisecond data and biased the alpha and beta estimates
   (PDF p. 13). This is a textbook instance of precisely two already-queued
   rules: the timestamp-unit/arrival-convention discipline (the intake
   audit asserts units on arrival; simultaneity must be handled by declared
   convention, never by jitter) and the estimator-configuration freeze
   (deep-read 63). Nothing here tightens either beyond what they already
   say; no queue change.
3. [interpretation caution] The Markov/recursion bargain: the O(k)
   recursive likelihood (eq. 20-21, PDF pp. 16-17) exists because the
   exponential kernel makes the joint process (N, lambda*) Markov; the
   survey notes the same efficiency disappears for any other kernel,
   where the next arrival must be solved numerically (PDF pp. 21-22).
   A future C8-style Hawkes arm therefore faces a declared trade, not a
   free choice: switching the excitation family away from exponential
   (e.g. to a power-law kernel, which the survey lists, PDF p. 6) invalidates
   the recursive likelihood and its cheap Hessian, and every
   effective-configuration statement (what is fitted, at what cost, with
   which derivatives) changes with it. Feeds the estimator-mode freeze
   already queued; no queue change.
4. [interpretation caution] MLE's printed failure modes: significant bias
   in small samples, many local optima, and high sensitivity to the
   selection of the excitation function (PDF p. 17, citing Filimonov's own
   findings); the GMM escape route runs on sample moments and sample
   autocorrelations "smoothed via a (rather arbitrary) user-selected
   procedure" (PDF p. 17); the minefield quote (PDF pp. 14-15). The
   estimator-mode register (estimator-mode is queued) and the
   noise-model pre-declaration already cover the substance: a future fit
   must pre-declare the optimiser, the kernel family, and the smoothing,
   because different choices of each yield materially different (alpha,
   beta, n). No queue change.
5. [reinforcing, no new item] The stated goodness-of-fit loop is exactly
   the compensator-null discipline the programme already requires:
   random time change theorem — transform arrivals by the FITTED
   compensator and the result must be a unit-rate Poisson process
   (Theorems 4-5, PDF p. 18), then test interarrivals for iid Exp(1)
   (QQ, KS/AD, Lewis, Brownian-approximation tests, PDF pp. 18-20).
   The relevance for the placebo family is direct: a Hawkes placebo or a
   generative-null arm earns nothing from "the fitted process looks
   clustered"; the pass condition is already available in closed form and
   is explored-data-free. The theorem also says the test is only as good
   as the compensator, i.e. as the configuration chosen in finding 4 —
   reinforcing, no queue change.
6. [cost-survival ammunition] The survey's financial applications carry
   the overfitting arithmetic any K7-style cost-survival layer must
   quote before adopting a Hawkes component: the constant-volatility
   Hawkes diffusion needs 5m + 3m^2 parameters for m assets (plus 3m for
   stochastic volatility), was fitted only for market PAIRS even after
   simplifying assumptions, with no AIC/BIC comparisons offered against
   the nested Merton model, and the survey's own verdict is the von
   Neumann elephant line (PDF pp. 12-13). A never-operationalised
   execution-strategy application; assumptions it must carry if ever
   cited: GMM on daily returns, timezone-conversion handling, and the
   unmeasured overfit margin of a many-parameter jump component
   (PDF pp. 12-13). No queue change.
7. [source-quality note] arXiv v1, "Last edited: July 13, 2015", authored
   as a survey ("provides background, introduces the field", PDF p. 1);
   a textbook-grade secondary source, not a primary result — its value
   here is codification (the exact formulas for n, R(tau), the recursion,
   the residual tests) rather than new empirical or theoretical
   information. Published-version caution applies unevenly: this survey
   appears to exist as an arXiv note (v1) — check for a journal version
   before formal citation; the text carries minor typographical slips
   ("natually", "moest", PDF pp. 1, 12) confirming early-draft status.
   No queue change.

## What this paper would have killed if we had done it wrong

Without the timestamp discipline, a future L2 event arm could have
inherited the Filimonov-Sornette path wholesale: second-resolution data,
simultaneous arrivals jittered by Unif(0,1) fractions, and a branching
ratio "trend" that is partly the smoothing artifact the survey prints
(PDF p. 13) — the exact class of elegant, wrong, much-cited result the
programme's estimator-configuration freeze exists to prevent. Without the
branching-ratio stationarity condition, a fit whose n crosses 1 could be
read as an exciting regime discovery rather than the detonation of the
model's own moment conditions (PDF pp. 7-8). Without the residual
(random time change) discipline, a generative-null or placebo arm could
declare success because its simulations "look" clustered, when the
compensator-transform test — available in closed form for the
exponential kernel (eq. 18, PDF p. 16) — would have been decisive either
way. And without the cost-survival ceiling, a contagion-style
many-parameter Hawkes diffusion (5m + 3m^2 parameters, no AIC/BIC
comparisons, PDF pp. 12-13) could have been adopted as a model of a
market whose data had not yet even passed the L0 gate.

## Standing caveat

A pedagogical survey with zero empirical content: every figure simulated,
no data analysis, and the estimation section explicitly bypasses real-data
challenges (PDF pp. 14-15). All financial-application numbers quoted here
(the 30%-to-70% branching-ratio trend, the Lorenzen correlation) are the
cited papers' claims relayed by the survey, banned from the record as
programme evidence under the laundering rule. The financial section is
2015-vintage and does not cover the last decade of microstructure-driven
Hawkes work (the survey itself points to Bacry et al. and the then-new
Parisian school, PDF p. 14). arXiv v1; check for a published version
before formal citation.