# Deep-read session 67 (null-time session 78, log ## 86) — the Clinet-Potiron doubly stochastic Hawkes-inference paper; the naive block-MLE's bias shown to sit at the magnitude of its own standard deviation, and the Gaussian limit shown to exclude diffusive parameter variation; queue-pointer discrepancy honestly recorded; nothing sharpened

Simon Clinet (University of Tokyo / CREST) and Yoann Potiron (Keio
University), "Statistical inference for the doubly stochastic self-
exciting process" (arXiv:1607.05831v3 [q-fin.ST], v3 stamp 27 Jun 2017,
"This version: September 19, 2018"). A statistics paper: the Hawkes
process with exponentially-decaying kernel is extended to a doubly
stochastic version whose three parameters (baseline ν, excitation a,
decay b) are themselves stochastic time-varying processes, the target
becomes the time-integrated parameter, and the paper derives the local
central limit theorem, the bias expansion and the bias-corrected global
central limit theorem for a blockwise local-MLE estimator, then checks
both on Monte Carlo simulations and on 2015 AAPL trade times.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change its kill lines? Source: legally acquired OA copy
(docs/library/text/xbe4d91_statistical_inference_for_the_doubly_stochastic_se.txt,
~47 pp., page-marked). Next UNREAD triage-rank entry (score 26) — with
an honest reconciliation: the recorded ## 85 queue pointer named the
score-25 entry x8f729f, but recomputing the score-sorted triage queue
against the notes on the file state this session shows this score-26
entry carries no note and no log mention; the ## 82 entry's claim that
"the score-26 tier is fully consumed" was off by this one entry. The
score rule orders the 26 above the 25, so this paper is consumed first;
x8f729f remains the next UNREAD after this session.

## The paper in one paragraph

The quantity of interest is the integrated parameter Θ = T^-1 ∫₀ᵀ θ*ₜdt
(eq. 1.1, PDF p. 2), where θ*ₜ = (ν*ₜ, a*ₜ, b*ₜ) is a stochastic process
and the event intensity is a doubly stochastic Hawkes process
λ(t) = nν*ₜ + ∫₀ᵗ na*ₛ e^(−nb*ₛ(t−s)) dNₛ (eq. 4.2, PDF p. 6; existence
by a fixed-point construction under supₜ aₜ/bₜ < 1, condition [E] and
Theorem 5.1, PDF pp. 6-7). The naive estimator chops the day into B_n
blocks and averages blockwise local MLEs (Riemann sum, eq. 1.2, PDF
p. 2); the local CLT forces small blocks (h_n = o(√n), eq. 1.3, PDF
p. 2), killing asymptotic bias forces large blocks (√n = o(h_n),
eq. 1.4, PDF pp. 2-3), and no h_n satisfies both (PDF p. 3), so a
first-order bias-corrected local MLE is constructed (eqs. 1.5, 5.18,
PDF pp. 3, 10) whose bias function b(θ*) is built from Fisher
information and its derivatives (eq. 10.14, PDF pp. 21-22; expansion
Theorem 10.17, PDF p. 41), and the global CLT holds under the smoothness
condition γ ∈ (3/4, 1] — with Itô-process (diffusive) parameter paths
explicitly excluded (condition [BC], PDF p. 10); higher-order
correction extends admissibility only to γ > 1/2, and at γ ≤ 1/2 no bias
correction works without distributional assumptions on the parameter
(p. 11). Monte Carlo: the naive estimator's finite-sample bias is of
the same magnitude as its standard deviation (Table 1, PDF pp. 14-15),
correction removes it (Table 2, PDF p. 17), and the global
constant-parameter MLE and the seasonal-baseline CH competitor are both
badly biased under time variation — CH failing to outperform the local
approach even inside its own well-specified model (Table 3 + text,
PDF pp. 14, 18). Empirics on 251 days of 2015 AAPL trades
(NASDAQ, ~15,000 trades/day, 9:30-15:30, PDF pp. 15-17): the fitted
excitation parameters wander intraday far beyond any seasonal pattern —
a*ₜ oscillating day-specifically, b*ₜ "go[ing] far off from one side or
the other with no specific pattern" (PDF p. 17) — with daily integrated
estimates ≈ (0.56, 11, 40) and dispersion (0.24, 2, 8), robust across
five block-size choices, and the uncorrected MLE/CH very different from
the corrected local estimates (Table 4 + text, PDF pp. 17-21).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening — default grade; every
mechanism found is a page-cited instance of a discipline the queue
already carries (the estimator-identity and estimator-configuration
freeze family), recorded as reinforcement, not as a new axis.

1. [reinforcing, no new item] The naive block-MLE of Hawkes parameters
   carries a finite-sample bias of the same magnitude as its own
   standard deviation (Table 1: naive Z-statistic means 0.69-1.62
   against unit sd across four simulation models, PDF pp. 14-15), and
   the global constant-parameter MLE and the seasonal-baseline CH are
   badly biased under genuine time variation, CH not outperforming the
   local approach even in Model III where CH is exactly well specified
   (Table 3 + text, PDF pp. 14, 18). This is the estimator-discipline
   lesson with the strongest finite-sample demonstration on this shelf
   so far: the dispersion of an uncorrected blockwise Hawkes fit is
   substantially bias, not information. Reinforces the
   named-estimator-identity rule and the estimator-configuration freeze
   (#37) — WHICH estimator, in WHICH exact configuration, now with the
   bias-correction status of that configuration explicitly part of the
   identity. No queue change.

2. [reinforcing, no new item] The block-size squeeze is a theorem, not
   an implementation wart: the local CLT needs h_n = o(√n) (eq. 1.3,
   PDF p. 2), absence of asymptotic bias needs √n = o(h_n) (eq. 1.4,
   PDF pp. 2-3), and the two are incompatible, so no admissible default
   block size exists for the naive estimator (PDF p. 3). For any future
   C1-L2/C8-adjacent partitioned estimator this means the partition is
   a load-bearing configuration choice that must be frozen before the
   data; reported robustness across several block sizes (the paper's own
   Table 4, PDF p. 21) is a robustness report, never a post-hoc
   permission to pick the best-performing partition. Reinforces the
   estimator-configuration freeze (#37) and the stability-is-robustness-
   reporting-never-retuning rule. No queue change.

3. [interpretation caution] The Gaussian limit is not available by
   right: the global CLT requires parameter-path smoothness
   γ ∈ (3/4, 1] and explicitly excludes Itô-process (diffusive)
   parameter variation (condition [BC], PDF p. 10); q-th-order bias
   correction extends admissibility only to γ > 1/2, and for γ ≤ 1/2 no
   correction is possible without assumptions on the parameter's
   distribution (PDF p. 11). Any future statement that a fitted Hawkes
   parameter (say a C8 excitation level) "is" somewhere with a Gaussian
   error band must pre-declare the assumed smoothness class of the time
   variation its inference covers; under diffusive variation the
   estimator remains consistent but has no CLT to normalize against
   (Proposition 5.8, PDF p. 12). No queue change.

4. [interpretation caution] Even inside the admissible class, the
   asymptotic variance is the path-integral T^-2 ∫ Γ(θ*ₛ)^-1 ds
   (Theorem 5.4, eq. 5.23, PDF p. 11), estimated blockwise from
   inverted local Hessians (eqs. 6.1-6.3, PDF pp. 12), and the paper's
   own studentized statistics underestimate tail mass for the excitation
   parameters a* and b* in finite samples (PDF p. 14). A fitted
   parameter's error band is itself an estimated, path-dependent
   object; error-band-as-evidence readings are prohibited. No queue
   change.

5. [interpretation caution] The empirical section documents that
   fitted excitation parameters wander intraday far beyond any seasonal
   template, b*ₜ with no pattern at all, the seasonal model "decent"
   only for ν*ₜ and unsatisfactory overall (PDF p. 17, Figures 2-4,
   PDF p. 19): a constant-parameter or seasonal-only Hawkes fit on
   intraday data is misspecified by construction, and the day-specific
   wander of fitted (a, b) is exactly the pattern that would be laundered
   as "regime signal" if read naively. Single equity name, one year,
   trade times only — no magnitude may be transplanted; the mechanism
   (fitted-parameter wander under misspecification) is the transferable
   content. No queue change.

6. [source-quality note] arXiv v3; the acknowledgments name an Editor,
   an Associate Editor and two anonymous referees (PDF p. 45), so a
   journal version likely exists — check the published version before
   formal citation; the index records zero citations. Single instrument
   (AAPL, NASDAQ 2015, 251 days), trade timestamps only — although the
   model's "market event" language spans orders and cancellations too
   (PDF p. 3), nothing is fitted on that richer event set; the empirical
   bias correction is computed from 100,000 Monte Carlo paths per node
   of a (θ, Δ) grid (PDF p. 13), so the correction inherits the
   parametric model's assumptions.

## What this paper would have killed if we had done it wrong

Had a future C8-adjacent arm fitted blockwise Hawkes parameters naively
and read the dispersion of fitted excitation levels as regime
structure, this paper is the counterfactual: the naive estimator's
finite-sample bias sits at the magnitude of its own standard deviation
on the paper's own simulations (Table 1, PDF pp. 14-15) — the
"regimes" would have been partly the estimator's bias wearing the
costume of market state, precisely the laundering the
named-estimator-identity rule exists to kill, demonstrated here on a
single estimator axis. Had a Gaussian confidence interval been attached
to a fitted parameter by right, the paper's own exclusion of diffusive
parameter paths from the CLT (PDF pp. 10-11) would have been laundered
around — the admissibility of the inference itself depends on an
assumed smoothness class nobody gets to assume silently. Had the
reported robustness across five block sizes (Table 4, PDF p. 21) been
read as license to choose the best block size after seeing results, the
pre-declared-configuration discipline would have been inverted into its
opposite. And had the AAPL intraday parameter wander (PDF p. 17) been
transplanted to a crypto L2 spec as empirical support, the
library-is-ammunition rule would have been broken: single name, single
year, trade prints only.

## Standing caveat

Everything empirical is one equity instrument (AAPL on NASDAQ, 2015,
251 days, 9:30-15:30, ~15,000 trades/day; PDF pp. 15-17) on trade
timestamps only, with the bias function Monte-Carlo-estimated under the
paper's own parametric recursion (PDF p. 13); the theory is for the
exponential kernel only, and the authors themselves flag that fatter
tails (polynomial kernels) are uninvestigated even in the parametric
case (PDF p. 20). The smoothness conditions that license the CLT
(γ ∈ (3/4, 1], PDF p. 10) are assumptions on an unobservable parameter
path, not verifiable from a fit. Applicability of any of this to a
24/7 crypto venue at L2 tick grain is asserted nowhere and proven
nowhere; the arXiv-v3 (referee-acknowledged) status requires the
published version be checked before formal citation. This note records
the bias and admissibility mechanisms only; no empirical claim from
this paper enters the record as support for any program claim.

---

Log entry: ## 86 (null-time session 78, deep-read session 67),
2026-11-20. Nothing measured during null time; no kill line moved;
nothing armed; nothing trades live. No candidate sharpening queued —
the default grade; DECISIONS_PENDING.md not touched. Queue-pointer
discrepancy recorded honestly in the log: the score-26 entry xbe4d91
was UNREAD on the file state; the ## 82 "tier fully consumed" claim was
off by this one entry. Guard clean: python3 src/integrity_guard.py run
this session exits zero on the assembled tree.
