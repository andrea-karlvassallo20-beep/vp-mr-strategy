# Library deep-read session 84 — Liquidity-adjusted Return and Volatility, and Autoregressive Models

- **Authors:** Qi Deng (Hubei University of Automotive Technology; Cofintelligence Financial Technology), Zhong-guo Zhou (California State University Northridge)
- **Title:** Liquidity-adjusted Return and Volatility, and Autoregressive Models
- **Venue:** arXiv:2503.08693v1 [q-fin], 2025 (JEL C32, C51, C53, G11, G12)
- **What it is:** a financial-econometrics paper that rescales minute-level returns by
  Amihud-style same-day liquidity factors to build "liquidity-adjusted" returns and
  volatilities, derives a liquidity beta pair (jump and diffusion), folds the
  liquidity-induced jump term of ARMA-GARCH into a deterministic rescaling, and
  claims better ARMA-GARCH fit and mean-variance portfolio Sharpe for illiquid
  cryptocurrencies but not for US stocks or BTC.

Read 2026-11-22, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x0acf9d_liquidity_adjusted_return_and_volatility_and_autor.txt,
~49 pp., page-marked). Next UNREAD triage-rank entry (score 22).

## The paper in one paragraph

The authors model a risk-averse investor's "perceived volatility" as a
minute-level liquidity-adjusted variance: each minute return is rescaled by a
factor built from an Amihud-style illiquidity ratio times a same-day
normalization constant (Eq. 1, with the day-T normalization factor defined by
the constraint summing to T over all minutes of the day, and using the day's
arithmetic-mean dollar volume, PDF p. 11; Eqs. 2-3, PDF p. 12), the daily
adjusted return aggregates these minute-level adjusted returns (Eqs. 4a-4b,
5, PDF p. 12), and a "liquidity beta pair" is built as ratios of same-period
aggregates: liquidity jump |r_t / r_t^l| (footnote 4; Eq. 6) and liquidity
diffusion sigma_t / sigma_t^l (Eq. 7, PDF p. 13). The derivation reinterprets
the stochastic liquidity-induced jump innovation of an ARMA-GARCH-Jump model
(Eq. 10, PDF p. 19) as a deterministic function of the beta pair and the
expected return (Eqs. 11-12, PDF p. 19), declared "no longer stochastic"
because it is the "deterministic daily-level manifestation" of minute-level
stochastic jumps, and substitutes it into the conditional mean to yield a
liquidity-adjusted ARMA-GARCH on r_t^l directly (Eqs. 13-16, PDF
pp. 19-21). The empirics fit ARMA(p,q<=4)-GARCH(1,1) on 242-day (stocks) and
365-day (cryptos) rolling windows to regular and adjusted returns for 15 US
stocks (Polygon.io minute data, Jul 2014-Feb 2025; PDF pp. 13-14) and 10
cryptocurrencies (Binance data, Oct 2020-Feb 2025; PDF p. 14), with both
liquidity betas silently capped at 10 before every statistic (footnote 6,
PDF p. 13): pairwise t-tests on log-likelihoods show the regular model fits
better for all 15 stocks at 1% (Table 5, Panel A, PDF p. 39) and the
adjusted model fits better for 7 of 10 cryptos (BTC declines; AVAX, LTC
nonsignificant; Table 6, Panel A, PDF p. 42), with the shock coefficient
rising under adjustment for 9 of 10 cryptos (Table 6, Panel B, PDF p. 43)
and persistence falling for the 7 significant ones (Table 6, Panel C, PDF
p. 44). "Validation" is two-asset mean-variance portfolios (one risky asset
plus a 0% risk-free one) on one-day-ahead forecasts (Eqs. 17-18, PDF
pp. 27-28; realized t versus forecast t+1, footnote 12, PDF p. 26): the
adjusted-input portfolios show higher annualized Sharpe ratios for 9 of 10
cryptos (all but BTC) and mixed results for stocks (9 up, 5 down, 1 flat;
Table 7, PDF p. 45).

## Findings, graded (does any kill line move?)

NO kill line changed; ONE new candidate sharpening queued, PENDING OWNER
RATIFICATION.

1. [reinforcing, no new item] Every headline magnitude in this paper is a
   paired-family self-comparison with no market null anywhere: the fit
   "improvements" are pairwise t-tests between the authors' own two nested
   model families on log-likelihoods (Tables 5-6, PDF pp. 39-44), and the
   Sharpe "validation" is the authors' own adjusted-input portfolio against
   their own regular-input portfolio, on two-asset toy portfolios, with a
   0% risk-free rate and zero transaction costs (Eq. 19, PDF p. 29; Table 7,
   PDF p. 45). The abstract's "validated by the empirical evidence that the
   liquidity-adjusted (LAMV) portfolios outperform" (PDF p. 1) is
   policy-family-indexed, not market-null-survived. The laundering ban
   binds: nothing in this paper may enter the record as support for any
   programme claim, and the portfolio-optimization layer is cost-survival
   context, never operationalized. No queue change.

2. [candidate sharpening, PENDING OWNER RATIFICATION] The
   same-period-aggregate feature availability rule, queued as the
   FORTY-FIFTH candidate: BEFORE the L0 gate, any C1-L2/C8-adjacent spec
   using a signal or feature computed from aggregates over its own
   aggregation period — a period mean or total (dollar volume, volume,
   trade count), a period return, a period volatility, or any ratio,
   rescaling or weighting built from them (an Amihud-style illiquidity
   weighting, a within-day normalized or "liquidity-adjusted" return, a
   period-aggregate liquidity factor) — must pre-declare, in the same
   frozen signal definition, that the feature's availability timestamp is
   the CLOSE of its aggregation period, and may evaluate only at points at
   or after that close; a feature evaluated at any finer grain inside its
   own aggregation window is forward-looking and fails by rule, regardless
   of whether it is labeled a normalization statistic, a liquidity factor
   or something else, with the availability declaration counted as frozen
   signal configuration and every deviation a dated amendment before any
   data is touched. Earned by the paper's own mechanism: every
   liquidity-adjusted quantity in the paper is a function of same-period
   aggregates — the minute-level factor uses the whole day's mean dollar
   volume and the day-level normalization constant inside every minute's
   rescaling (Eq. 1 with its summation-to-T normalization, PDF p. 11;
   Eqs. 2-3, PDF p. 12), the daily adjusted return aggregates all of day
   t (Eqs. 4a-4b, 5, PDF p. 12), and the liquidity beta pair is a ratio of
   same-period aggregates (|r_t/r_t^l|, footnote 4, PDF p. 12; Eq. 7,
   PDF p. 13) — and the paper's own use is lawful precisely because its
   forecasts are strictly one-period-ahead after the day closes (footnote
   12, realized t versus forecast t+1, PDF p. 26), which proves the
   availability discipline is what keeps this feature family honest; a
   C1-L2/C8 spec adopting any such liquidity-weighted feature at intraday
   evaluation grain would silently import the rest of the day, exactly as
   a full-sample normalization window does, and the queued
   feature-normalization pre-declaration (deep-read 83) does not catch it
   because that rule binds only signals defined through rolling or
   windowed normalisation statistics (min-max, z-score, rolling-mean,
   rolling-vol), not through aggregate-weighted liquidity factors.
   Harder-to-pass because a spec whose feature aggregates its own
   evaluation period, evaluated before that period closes, now fails at
   the gate instead of surviving as a clever liquidity adjustment; it
   tightens the feature-normalization pre-declaration (deep-read 83) by
   extending the availability discipline from the normalization-statistic
   class to ANY same-period aggregate-derived feature, joining the
   spread-convention declaration rule (deep-read 56) and the
   estimator-configuration freeze (deep-read 63) on the frozen-configuration
   axis. Full draft with the killed-if-wrong counterfactual below and in
   the session log.

3. [interpretation caution] The paper's own cross-asset contrast is
   liquidity-regime-indexed: the adjustment degrades fit for all 15
   liquid stocks at 1% (Table 5, Panel A, PDF p. 39), improves it for 7 of
   10 cryptos and DEGRADES it for BTC, whose liquidity profile the
   authors themselves read as stock-like (PDF pp. 24-25), and the same
   asymmetry appears in the Sharpe table (9 of 10 cryptos up, BTC down;
   Table 7, Panel B, PDF p. 45). Reading discipline for any C1-L2/C8
   cross-sectional or cross-asset read: a compressive or anticipatory
   association measured on one baseline-liquidity regime (BTC-like majors)
   cannot be generalized to another (illiquid alts) or across regimes
   without the replication the programme already requires; microstructure
   associations may be liquidity-regime-conditioned, and a pooled-market
   claim that silently mixes regimes inherits exactly this confounder.
   No queue change.

4. [interpretation caution] Both liquidity betas are silently capped at 10
   before every statistic (footnote 6, PDF p. 13), and the cap binds
   visibly: the maximum of the liquidity jump is exactly 10 for every
   stock and crypto (Tables 1, 3, PDF pp. 35, 37) and every histogram is
   described by its "higher bar at" the cap (Figs. 1-4, PDF
   pp. 46-49), so the reported means, medians and day-counts are
   clip-indexed numbers. Reading discipline for any future registered
   descriptive statistic of a liquidity-type quantity: winsorization or
   clipping constants must be pre-declared as frozen configuration, else
   the measured moments are functions of an undisclosed analyst choice —
   the existing frozen-configuration discipline owns this; the paper
   demonstrates the degrees of freedom are real and load-bearing. No
   queue change.

5. [reinforcing, no new item] The derivation abolishes its own stochastic
   jump term by assertion: the liquidity-induced innovation of
   Eq. 10 (PDF p. 19) is declared "no longer stochastic" once rewritten
   as a deterministic function of the beta pair (Eqs. 11-12, PDF p. 19),
   with the gamma and lambda of Eq. 11 never estimated or tested, and the
   conditional variance of the adjusted return then being nothing but
   the regular variance rescaled by the liquidity jump (Eqs. 13-15,
   PDF pp. 19-20). This is exactly the move the programme's generative-null
   and admission-null discipline refuses: a refutation instrument may not
   be converted mid-derivation into a deterministic relabelling of the
   quantity it was supposed to test. Reinforces the standing discipline
   (the dynamics-identification rule for generative nulls, the
   two-null admission family); no queue change.

6. [reinforcing, no new item] The crypto results are consistent with
   volatility persistence on unadjusted returns of illiquid assets
   partly reflecting liquidity-shock clustering rather than genuine
   temporal memory: persistence falls under adjustment for the 7
   significant cryptos (Table 6, Panel C, PDF p. 44) while shock
   sensitivity rises (Table 6, Panel B, PDF p. 43). As observation this
   only sharpens the reading discipline already owned by the queued
   level-versus-memory disambiguation (deep-read 59): count-based or
   persistence-type evidence in illiquid regimes must be shown to
   survive a liquidity-regime or level control before it is read as
   memory. Ammunition, never evidence; no queue change.

7. [source-quality note] arXiv v1 preprint (2025), zero citations at
   cataloguing, funded by two Hubei provincial grants (PDF p. 1); the
   source equations extract as partially corrupted Unicode, and the
   derivation carries loose steps (gamma/lambda never estimated;
   "first order approximation" declared and moved past, footnote 3,
   PDF p. 12); the supporting tests are withheld as "available upon
   request" (ANOVA, footnote 9, PDF p. 16; ADF called "Adam-Fuller",
   footnote 10, PDF p. 17; AIC/BIC, footnote 11, PDF p. 22); two
   paragraphs are duplicated verbatim across PDF pp. 23-24; and the
   conclusions say the LAMV "does not offer improved performance" for
   stocks (PDF pp. 30-31) while the body calls the same Panel A results
   "mixed" (9 up, 5 down, 1 flat, PDF p. 29; Table 7, PDF p. 45); the
   crypto Sharpe ratios are mostly negative annualized values over the
   2021-2025 window (Table 7, Panel B, PDF p. 45). All magnitudes are
   asset-, period- and family-indexed, none-of-our-support. Check the
   published version before any formal citation. Read, graded,
   recorded.

## What this paper would have killed if we had done it wrong

If a future C8-adjacent spec had adopted a liquidity-weighted or
"liquidity-adjusted" feature family modeled on this paper — which is a
natural temptation for a spec already carrying a market-book first-PC
factor and VPIN-style flow clocks — without the availability rule of
finding 2, the feature would have entered at intraday evaluation grain
carrying its own aggregation period's future inside it: day-level mean
volume, normalization constants and period returns all computed over a
window that includes the evaluation point's own future, invisible to the
timestamp audits (which police raw-data arrival, not derived-feature
availability) and outside the letter of the feature-normalization
pre-declaration (which binds normalization statistics, not
aggregate-weighted factors). An L2-phase compression claim could then have
passed on lookahead alone, and defended itself by re-choosing the
aggregation window after every kill attempt — the exact post-hoc re-tuning
loop the freeze family exists to close. Equally, had the log-likelihood
t-tests or the Sharpe table been cited as evidence that liquidity
adjustment "works" in crypto, a paired-family self-comparison with no
market null would have been laundered into the record — the failure class
the library-is-ammunition rule forbids, and the reason this note records
no empirical claim from the paper as programme support.

## Standing caveat

Everything here is 15 US stocks from Polygon.io minute data and 10
Binance pairs over one 2020-2025 window, with every fit and portfolio
result a comparison between two members of the authors' own nested model
family: no market null, no transaction costs, a 0% risk-free rate,
two-asset portfolios, liquidity betas clipped at 10, supporting tests
withheld, and the derivation's stochastic-to-deterministic conversion
asserted rather than tested. The within-day normalization inside the
minute-level factor is lawful for the paper's own strictly
one-day-ahead use and the Sharpe figures cannot be audited from the text
beyond what is printed. The extract is the arXiv v1 version — check the
published version before any formal citation. Nothing here licenses a
measurement, an arming or a kill-line move; it licenses one
harder-to-pass pre-declaration rule, pending the owner's ratification.
