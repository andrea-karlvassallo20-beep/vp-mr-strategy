# Deep-read session 40 — Filimonov, Wheatley and Sornette, "Effective measure of endogeneity for the Autoregressive Conditional Duration point processes via mapping to the self-excited Hawkes process"

Library deep-read session 40 (null-time session 44, log entry
## 48; drafted as deep-read 39 / null-time 43 / log entry ## 47
and renumbered at landing time after the parallel nonlinear-
Hawkes classification landing (x20bdef) merged first as ## 47,
per the declared append-time rule; the renumber is recorded in
log entry ## 48's session-state note). Vladimir Filimonov, Spencer
Wheatley and Didier Sornette (Department of Management, Technology
and Economics, ETH Zürich), arXiv:1306.2245v2 [q-fin.ST], v2
stamped 19 Jun 2014, "(Dated: October 31, 2018)" header line at
PDF p. 1; 37 pp. text extract, page-marked, complete (references
PDF pp. 23-32, figures PDF pp. 33-37). A simulation-only methods
paper: it defines the composite ACD parameter
ζ = Σαj + Σβk as an "effective degree of endogeneity",
maps it by numerical calibration onto the Hawkes branching ratio
η, and reads the large ζ values reported in the ACD
econometrics literature as support for dominant market
endogeneity. Read 2026-11-19, against ONE question: what here
would kill C1-L2 or C8 faster, or change their kill lines?
Source: legally acquired OA copy
(docs/library/text/xa4ac36_effective_measure_of_endogeneity_for_the_autoregre.txt).
Assigned triage-rank entry (score 30, xa4ac36; consumed after
two declared skips: the landed ## 45's closing pointer named
x36082b as the next UNREAD, but x36082b is already read on main as
deep-read session 2 — stale pointer, defect declared; and x20bdef,
the next entry behind it, was claimed in flight at read time by
branch deep-read/session-39-nlhawkes-classification — honored, not
consumed — and has since LANDED on main as log entry ## 47
(deep-read session 39, the nonlinear-Hawkes steady-state
classification paper) while this session was reading, its closing
pointer already naming xa4ac36 as the next unclaimed UNREAD, so
this consumption is consistent with the landed chain). Next UNREAD
triage-rank entry: "Stochastic Optimal Control of Hawkes
Jump-Diffusion Systems" (score 30, xd02283); behind it "Critical
reflexivity in financial markets: a Hawkes process analysis"
(score 30, xdc14f4). A successor session must re-read the live
main tail and the branch/PR set first.

## The paper in one paragraph

The paper introduces, for the Autoregressive Conditional Duration
ACD(p,q) model (δti = ψi·εi with
ψi = ω + Σαj·δti-j + Σβk·ψi-k,
Eqs. (9)-(13), PDF pp. 7-8, stationarity ζ = Σαj + Σβk < 1,
Eq. (12)), a composite control parameter ζ intended to play the
role the branching ratio η plays for the exponential-kernel Hawkes
process (Eq. (7), PDF p. 7; branching-ratio definitions and the
endo/exo fraction identity Rendo/R = n, Eq. (17) and Eq. (18),
PDF p. 10). The ACD cannot be mapped exactly onto a branching
structure, because each past event's contribution to the
conditional intensity depends on the realized durations of all
later events, violating branch independence (PDF pp. 11-12), and
ζ shares only the divergence structure of the mean duration
E[δt] = ω/(1-ζ) with the Hawkes rate R = µ/(1-η)
(Eqs. (16), (21), PDF pp. 10, 12). The mapping ζ→η is therefore
established numerically: 40 values of ζ, 100 realizations of 3500
synthetic ACD(1,1) events each (first 500 discarded), exponential
Hawkes fitted by MLE, KS goodness-of-fit on the residual process
(PDF pp. 12-14). The result is a monotone but decomposition-
dependent η(ζ) curve: α and β enter with different weights, all
branches converge to η̂ ≈ 0.9-1 at ζ = 1, and the α = 0 branch
gives η̂ = 0 for every ζ (Figs. 3-5, PDF pp. 14-15, 33-35). A
finite-sample study of the Hawkes MLE (Appendix B, PDF pp. 21-22,
Fig. 7, PDF p. 37) shows positive bias near η = 0 and large
sample-length-dependent negative bias for η > 0.9. The conclusion
reads the large ζ values (up to 0.95) reported in the ACD
econometrics literature as strong support for a dominant
endogenous component, and proposes extending the ζ-interpretation
to GARCH models (PDF pp. 18-19).

## Findings, graded (does any kill line move?)

NO kill line changed. NO new candidate sharpening. Default grade;
the paper is a simulation-only worked exhibit for rules already
standing (the estimator-mode register with its no-single-mode
rule from the landed ## 45, the near-critical regime-disclosure
rule of deep-read 17, the kernel-family register of the Hardiman-
Bouchaud session-2 note and the session-32 aggregation cautions,
and the featureless-process placebo family), and the burden of
proof for a sharpening was not met.

1. **[reinforcing, no new item]** ζ is a model-family statistic,
   not an identity with the branching ratio: the mapping η(ζ) is
   monotone but not one-to-one in the decomposition. The paper's
   own cases (B) α = 0.38, β = 0.13 and (C) α = 0.13, β = 0.38
   share ζ = 0.51 yet give η̂ = 0.52 versus η̂ = 0.22 (PDF p. 14,
   Fig. 2); and the α = 0 branch yields η̂ = 0 for every ζ,
   because with α = 0 the conditional-duration recursion is
   purely deterministic and the realized durations are carried
   entirely by the iid noise (Eqs. (9), (13), (23), PDF pp. 14-15,
   Fig. 3(B), PDF p. 33). This is a second-model-family worked
   exhibit for the estimator-mode register and the landed ## 45's
   no-single-mode rule: a duration-based GARCH-family fit of the
   same data yields an "endogeneity" number that is family-
   relative, decomposition-dependent, and can be exactly zero
   under one member of the same family. No ACD-fitted ζ from the
   econometrics record may enter any programme spec, default,
   tolerance or expected value; nothing added, the standing
   register already governs.

2. **[interpretation caution]** The mapping is goodness-of-fit-
   conditioned, and the KS rejection band sits exactly on the
   region the conclusion relies on: for most combinations
   0.6 ≲ α+β ≲ 0.95 the calibrating Hawkes model is rejected by
   the KS residual test at the 5% level (PDF p. 15; Fig. 5 dashed
   region, PDF p. 35), yet the conclusion reads empirical ζ values
   "often larger than 0.5, and up to 0.95" as strong support for
   dominant endogeneity (PDF p. 18). A future imported
   endogeneity reading of duration-model lineage is admissible
   only with the calibrating model's fit test disclosed and
   passing in the claimed region; where the fit is rejected, both
   ζ and the mapped η̂ are model-relative artifacts, not
   measurements of the venue. Read discipline only; the
   estimator-mode register already stands and no new amendment is
   needed for a family the programme does not currently use.

3. **[reinforcing, no new item]** The paper's own Appendix B is a
   seventh worked exhibit for the near-critical
   regime-disclosure rule: the Hawkes MLE of η carries positive
   bias near 0 (kernel positivity forces η ≥ 0), and a large
   sample-length-dependent negative bias for η > 0.9, with 90%
   quantile error at most 0.1 for η ≤ 0.9 on 3000-event
   realizations (Appendix B, PDF pp. 21-22, Fig. 7, PDF p. 37).
   Any near-critical branching claim must disclose sample length
   and bias direction; an η̂ close to 1 on a limited sample is a
   downward-biased, length-dependent statistic, not a measured
   criticality. Same governance as the ## 46 and ## 47
   exhibits; nothing added.

4. **[reinforcing, no new item]** Appendix A states the paper's
   own placebo discipline as a general recommendation: "always
   consider one or several well-known processes (such as the
   uncorrelated random walk) and apply first the new method to
   these known processes to check if the event defining procedure
   might not introduce some spurious endogeneity", together with
   the warning that trend/turning-point event definitions are
   mostly non-causal (unsuitable for forecasting) and that
   conditional-statistics event definitions can create spurious
   phenomena even in featureless processes (PDF pp. 20-21). An
   external worked precedent, from the same ETH line as the
   landed ## 45's Poissonization placebo, for the programme's
   featureless-process placebo family and the label-conditioning
   declaration family; cited as design precedent only, never as
   evidence about any venue.

5. **[reinforcing, no new item]** The kernel-robustness result is
   a short-memory statement, not a kernel-invariance license: the
   exponential and power-law calibrations agree (Table 1, PDF
   pp. 16-17) because the fitted power law collapses to an
   exponential-like shape (φ̂ ≈ 105, ĉ ≈ 816, PDF p. 17; Fig. 6,
   PDF p. 36) on ACD(1,1) data whose autocorrelation decays
   exponentially by construction (PDF p. 16). Worked exhibit for
   the kernel-family register: kernel-shape agreement is a
   property of the data's memory class; no kernel shape from any
   single fit is ever citable as expected behavior (per-branch
   rule, session-2 note).

## What this paper would have killed if we had done it wrong

If the conclusion's headline reading had been imported as
"duration-based econometrics proves markets are up to 95%
endogenous", a simulation-only, fit-test-conditioned, model-family
mapping would have been laundered into a market-truth claim, and
its own Fig. 5 rejection band shows the calibrating model fails
exactly in the ζ range the headline relies on. If ζ had been
treated as interchangeable with η, the paper's own α = 0
counterexample (ζ anything, η̂ = 0) would have smuggled a
meaningless endogeneity number into a spec under a familiar name.
If the finite-sample bias had been ignored, an η̂ near 1 would have
been booked as measured criticality rather than a downward-biased,
sample-length-dependent statistic. Library-is-ammunition, the
estimator-mode register, the near-critical disclosure rule and
nothing-measured prevented all three.

## Standing caveat

No market, no sample, no period, no costs: every number in the
paper is generated by simulating ACD(1,1) processes and calibrating
Hawkes models to them (PDF pp. 12-13, 21-22); nothing is measured
on any venue, and the "empirical" reading of past ACD studies is
a reinterpretation of other people's ζ estimates, not new data.
The ACD admits no clean exo/endo decoupling, ω is not the only
factor embodying exogenous activity (PDF pp. 15-16), and its
conditional intensity is constant between events where the Hawkes
decays exponentially (PDF p. 14), so ζ-like numbers are never read
as ν-style breakdowns here. arXiv v2, journal record NOT checked
at reading, published version to be checked before formal
citation. Laundering directions named. INTO — nothing: no ζ, no
η(ζ) curve, no α/β decomposition, no kernel, no bias numbers
enter any spec, default, calibration, tolerance or generative
null. OUT — never read backwards as "duration-based econometrics
proves dominant endogeneity" (model-relative and fit-test-
conditioned), "ζ is the branching ratio" (non-injective and void
at α = 0), or "kernel choice does not matter" (a short-memory
artifact of this construction).
