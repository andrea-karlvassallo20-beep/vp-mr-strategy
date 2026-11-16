# Open-source math verification — Task 1 report (2026-11-16)

Status: **VERIFIED** (with three defects found and fixed in the repo's own
implementations — the point of verification is that the formula is
authoritative, not the code).

Machine-checkable evidence: `src/verify_math_library.py` (re-runnable),
`paper/research/math_verification.json` (its output), hermetic regression
tests in `tests/test_math_exactness.py`.

## A. OFI — the exact formula extracted from the arXiv LaTeX source

Paper: Cont, Kukanov & Stoikov, "The Price Impact of Order Book Events",
arXiv:1011.6402v3 (q-fin.TR), Sec. 2.1. The exact event-contribution
formula from the source:

    e_n = I{P^B_n >= P^B_{n-1}} q^B_n - I{P^B_n <= P^B_{n-1}} q^B_{n-1}
          - I{P^A_n <= P^A_{n-1}} q^A_n + I{P^A_n >= P^A_{n-1}} q^A_{n-1}

with aggregation OFI_k = sum_{n in (t_{k-1}, t_k]} e_n and the linear
impact relation Delta P_k = beta * OFI_k + eps_k (their Eq. 2), with
beta_i = c / AD_i^lambda (their Eq. 3; the stylized model is lambda = 1,
i.e. impact inversely proportional to depth).

Two properties of the source formula that earlier restatements got wrong:

1. The indicators are NON-STRICT (>=, <=). When a price is unchanged,
   both indicators fire and the event contributes the queue change
   q_n - q_{n-1}. A restatement using strict inequalities drops all
   same-price queue changes — the majority of book events.
2. On price-changing events the contribution is the FULL level size
   (q^B_n on a bid improvement, -q^B_{n-1} on a bid drop), not the
   queue delta across price levels.

Found and fixed in `src/features.py::top_of_book_ofi` (descriptive-only
consumer; no claim ever drew on the buggy version):

- D1 (sign): both ask-side branches were sign-flipped relative to the
  source (+q^A_n on ask-drop instead of -q^A_n; -q^A_{n-1} on ask-rise
  instead of +q^A_{n-1}). The code contradicted its own docstring.
- D2 (missing branch): same-price queue changes contributed 0.

Verification: the implementation is compared event-by-event against a
literal transcription of the source formula on 25 randomized synthetic
books x 2000 events covering every branch — max abs diff **0.0**
(`math_verification.json: ofi`). The cheatsheet
(`docs/math_cheatsheet.md` §1a) now carries the exact source formula and
a matching implementation; the earlier Delta-q restatement is retired
with an explicit note.

## B. Hawkes — verified against the `tick` library (v0.8.0.2)

Convention bridge (this matters and was previously unwritten): the repo
uses the amplitude convention phi_mn(t) = alpha_mn exp(-beta t) with
branching matrix G = alpha / beta; tick uses phi_mn(t) = G_mn beta
exp(-beta t), i.e. tick's `adjacency` parameter IS the branching matrix.
All comparisons convert through G.

Checks and results (10 randomized paths each):

- **B1 — log-likelihood exactness.** The repo's O(N) recursive
  `hawkes_loglik` vs an independent O(N^2) oracle written directly from
  the intensity definition, on tick-simulated 2D data (exact ground-truth
  generation): max relative diff **1.6e-14**. Found and fixed in
  `hawkes_loglik`:
  - D3 (phantom event): the recursion seeded `prev = ones(d)`, which is
    equivalent to a phantom event at t_0 in EVERY dimension, inflating
    every early intensity;
  - D4 (orientation): the intensity used the column alpha[:, y_k] while
    the compensator uses rows alpha[m, :] — internally inconsistent.
- **B2 — 2D branching recovery.** Planted G (tick simulator, exact),
  repo MLE `fit_hawkes` (fixed true beta) and tick's `HawkesExpKern`
  fit, spectral radius rho(G) vs planted: repo max abs err **0.086**,
  tick **0.033**. Found and fixed in `fit_hawkes`:
  - D5 (metric): `branching_ratio` reported rho(alpha) instead of
    rho(alpha / beta) — an overstatement by the factor beta (= 2.0 in
    the default configuration). With the C8 trigger threshold at
    branching > 0.8, this defect alone could have manufactured the
    trigger. The upgraded T2 estimator (`fit_hawkes2`) was already
    correct (G = alpha/beta, row convention consistent, verified
    recursion-vs-brute by its own unit tests).
- **B3 — 1D Filimonov-Sornette branching ratio.** The cheatsheet's
  `fit_hawkes` (docs/math_cheatsheet.md §2b, executed verbatim from the
  markdown by the verify script) vs tick's `HawkesExpKern` on
  tick-simulated 1D data: cheatsheet max abs err **0.036**, tick
  **0.040**, both against the planted n_c. The cheatsheet's Ozaki
  recursion was already correct.

Environment notes (reproducibility):

- tick's `Base` metaclass builds its attribute registry from docstrings
  via `numpydoc`; without `numpydoc` installed, every tick learner raises
  `AttributeError` on `__init__`.
- tick's `HawkesExpKern` requires `penalty="none"` (string) in this
  build, not `penalty=0.0`.
- tick 0.8.0.2's `ModelHawkesExpKernLogLik.loss` was probed on
  handcrafted Poisson data (loss = 0 where the documented formula gives
  -loglik = mu*T; inconsistent values in 2D) and does not expose an
  interpretable absolute log-likelihood. The sharp likelihood check
  (B1) therefore runs against the independent brute-force oracle; tick
  enters the verification through its simulator (ground truth) and its
  `HawkesExpKern` estimator (independent estimator agreeing on branching
  recovery). This limitation is recorded rather than papered over.

## Verdict

The public math is now verified end-to-end in this repo: OFI is
byte-exact to the arXiv source across all four indicator branches, the
Hawkes likelihood is exact against an independent oracle, and the
branching ratio — the C8 trigger metric — is now the correct spectral
radius of G, cross-validated against tick on exact simulations. Five
defects (D1-D5) were found and fixed; none of them had been consumed by
a tested claim. The L2 trigger layer can now be built on flawless math.
