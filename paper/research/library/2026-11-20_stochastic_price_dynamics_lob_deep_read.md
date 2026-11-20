# Deep-read session 66 (null-time session 77, log ## 85) — the Langnau-Punchev LOB-implied price-dynamics paper; the price-process family shown to manufacture or erase the book statistic's meaning; ONE sharpening queued

Alex Langnau (Allianz Investment Management) and Yanko Punchev (LMU
Munich), "Stochastic Price Dynamics Implied By the Limit Order Book"
(arXiv:1105.4789v1 [q-fin.TR], 24 May 2011 stamp). Rosu's equilibrium
impatience rate is extracted from a reconstructed DAX-futures limit
order book (June-August 2010, ~450,000 updates/day, depth six levels,
PDF pp. 6, 33-35) and tested for level-independence first under a
geometric Brownian motion and then under Kou's double-exponential
jump-diffusion.

Read 2026-11-20, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x074d5c_stochastic_price_dynamics_implied_by_the_limit_ord.txt,
~41 pp., page-marked). Next UNREAD triage-rank entry (score 25).

## The paper in one paragraph

A distance-to-fill expected utility UD(r) = |D| E[exp(-r τ)] (eq. 2,
PDF p. 3) is defined, where τ is the first passage time of the best
offer to the limit-order level D; the impatience rate r is fitted on
30-second reconstructed LOB grids of the FDAX, holding U stepwise
constant under the assumption that an equilibrium book supports one
level-independent r (Algorithm 1, PDF pp. 6-7). Under GBM the
impatience rate is NOT level-independent: it follows a power law in
the risk-adjusted distance z (Figures 1-2, PDF pp. 7-9), and holding
r and U constant instead forces an implied volatility that rises with
distance-to-fill — a "volatility smile" implied by the book (Figure 5,
PDF p. 12), which the authors read as far-out limit orders being
underweighted by continuous dynamics. Augmenting the price process to
Kou's DEJD, with first-passage Laplace transforms (Theorem 6.3, PDF
pp. 13-16) and a bipower-variation split of diffusive from jump
variance (PDF pp. 17-18), makes r approximately level-independent
within established market regimes (Figures 7-8, PDF pp. 21-22). In
both settings the authors' own regression finds no significant
relationship between the impatience rate and future mid-price
returns (PDF pp. 9, 20).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING
OWNER RATIFICATION — the price-process-family invariance rule (the
thirty-eighth): the same market, the same reconstructed book, the same
equilibrium assumption, and one analyst choice — the price-process
family — converts the headline book statistic from unstable and
meaningless to stable and meaningful. Under GBM the day-level dispersion
of the fitted impatience rate is enormous (σr up to 43.3, 50.7, 83.9
and 88.3 across the ~48 days, Figures 12-13, PDF pp. 30-31) and r is
an explicit function of distance-to-fill AND of estimated volatility
(eq. 13 and the power law, PDF pp. 7-9); under DEJD on the same data
σr collapses by an order of magnitude (most days ~0.003 to ~2.7, same
pages) and r is a function of neither (PDF pp. 21-22). The level
structure the statistic is supposed to measure is therefore
manufactured or erased by the assumed family, not measured from the
book. Pre-declaration text: any C1-L2/C8-adjacent book-defined
statistic that prices time through an assumed price process — expected
fill, first-passage or hitting-time discounting, impatience or utility
weighting of book levels — must, BEFORE the data, pre-declare the
price-process family entering its definition from a declared generic
default, and must carry the killed-if-wrong counterfactual: a
statistic whose level-dependence, stability, or sign exists under one
family and dissolves under another fails by rule instead of surviving
as a modeling choice; the declared default may only be changed by a
dated amendment before the data is touched. Harder to pass because a
family-dependent book statistic that only behaves under the analyst's
preferred family now fails at the gate rather than arriving as a
tuning freedom; tightens the same axis the named-estimator-identity
rule and the estimator-configuration freeze already tightened (WHICH
estimator, in WHICH exact configuration, and now under WHICH assumed
price-process family), and hardens rule 1 of the pre-registration
discipline. Full draft with the counterfactual in this note.

2. [reinforcing, no new item] The "volatility smile" implied by the
book (implied σ rising with distance-to-fill, Figure 5, PDF p. 12) is
a derived artifact of the GBM family and dissolves once jumps are
added (PDF pp. 19-22): the tempting anticipatory reading — far-out
limit orders "betting on a sharp price change" (the authors' own
intuition, PDF p. 11) — is a property of the assumed dynamics, not an
observation about traders. Reinforces the magnitudes-never-transfer
rule and the pre-declaration family; no empirical claim from this
paper enters the record as support for any program claim. No queue
change.

3. [reinforcing, no new item] The paper's own regression shows the
impatience rate carries no significant relationship to future
mid-price returns in either the GBM or the DEJD setting, with false
outbreaks documented (PDF pp. 9, 20) — a headline book-derived
statistic honestly reported as failing its own directional null.
Reinforces the two-null admission rule: any future C1-L2
urgency/fill-discount feature must beat free nulls in the subsample
where its claimed information lives. No queue change.

4. [interpretation caution] The DEJD calibration is under-identified:
five parameters against two moment constraints, drift assumed away by
fiat (PDF p. 18), the symmetry constraint η1 ≈ η2 abandoned because
off-the-shelf optimizers would not converge with it (PDF pp. 18-19),
and the bipower-variation estimate capped by realized variance to
avoid negative jump variance (eq. 33, PDF p. 17). The celebrated flat
r regime therefore passes partly under a fitting procedure that drops
the constraints it cannot converge under. Any future passage-time
discounting of book levels must treat its fitted parameters as
optimizer-conditioned objects, not identified structure.

5. [source-quality note] arXiv v1 only, zero citations recorded, no
published version found; first author industry-affiliated (Allianz
Investment Management, PDF p. 1); single instrument (FDAX), three
months of 2010 data, depth restricted to five or six levels, results
illustrated on "a representative day" (PDF p. 7) with descriptive
per-day statistics (PDF pp. 30-31); the raw data lacks order flags so
cancellations cannot be reliably reconstructed (PDF pp. 33-34); no
significance testing anywhere in the paper. Check the published
version before formal citation.

## What this paper would have killed if we had done it wrong

Had the LOB-implied smile been read as evidence that deep-book
positioning anticipates sharp moves — the reading the paper's own
intuition invites (PDF p. 11) — a C1-L2 motivation could have carried
"far orders imply coming jumps" into the spec while the paper itself
proves the smile is exactly what a wrong price family manufactures:
under the jump-augmented family the same book shows no smile (PDF
pp. 19-22). That is the academic-degree-of-freedom failure the
pre-declaration family exists to kill, demonstrated on a single
analyst axis. Had the flat DEJD impatience rate been read as
directional information, the authors' own null regression (PDF
pp. 9, 20) would have been laundered around — the same laundering the
two-null admission rule forbids. And had the DEJD parameterization
been treated as identified market structure, an under-identified fit
whose constraints were dropped for convergence (PDF pp. 18-19) would
have entered the record wearing the costume of measurement.

## Standing caveat

Everything here is single-venue (Eurex FDAX), single-instrument,
2010, 30-second grid with 30-observation rolling windows (~25
minutes of history per estimate, PDF pp. 5-7), five-to-six-level
depth, tick-size spreads, cancellations unreconstructible from the
data (PDF pp. 33-34), and no significance testing. Applicability of
passage-time-discounted book statistics to a 24/7 crypto venue at L2
tick grain is asserted nowhere and proven nowhere; the arXiv v1
status and acknowledged optimizer instability (PDF pp. 18-19) are
additional reasons no magnitude, rate, or smile shape from this
paper may be transplanted. This note records the family-dependence
mechanism only; it enters no spec as empirical support.

---

Log entry: ## 85 (null-time session 77, deep-read session 66), 2026-11-20.
Nothing measured during null time; no kill line moved; nothing armed;
nothing trades live. Sharpening hardening rule 1 of the
pre-registration discipline, harder-to-pass only, PENDING OWNER
RATIFICATION.
