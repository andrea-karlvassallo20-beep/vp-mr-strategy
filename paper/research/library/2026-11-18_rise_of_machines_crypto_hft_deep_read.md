# Library deep-read session 22 — Petukhina, Reule & Härdle, "Rise of
# the Machines? Intraday High-Frequency Trading Patterns of
# Cryptocurrencies" (arXiv:2009.04200v1, 2020; Humboldt zu Berlin /
# SMU; post-peer-review version of a European Journal of Finance
# article; GAM seasonality of 5-minute crypto data, the
# "Proof-Of-Human" argument)

Read 2026-11-18, against ONE question: **what here would kill C1-L2
or C8 faster, or change their kill lines?** Source: legally acquired
OA copy (`docs/library/text/x2a7ad5_rise_of_the_machines_intraday_high_frequency_tradi.txt`,
~20 pp., page-marked). Next UNREAD triage-rank entry (score 33;
the session-27 queue pointer's "next score-34/33 entry, verify
against the shelf" — verified unread against the note shelf by the
read-slug mapping, not by title).

## The paper in one paragraph

The authors take 5-minute interval data (CRIX index family plus a
dyos solutions GmbH European feed) for eleven major cryptocurrencies
over July-August 2018 — deliberately a European corporate-vacation
period — compute returns, absolute-return volatility, and volume,
and fit Generalized Additive Models (cubic splines for daily, P-
splines for weekly seasonality) to each (PDF pp. 6-8, 15). Summary
statistics: first-order return autocorrelations are near zero and
mostly slightly negative; squared/absolute-return autocorrelations
are positive (volatility clustering); excess kurtosis is extreme
(BTC 49.4, all coins > 8; Jarque-Bera rejects normality everywhere;
PDF p. 12, Table 1); pairwise return correlations cluster around
BTC/ETH/XRP, the market drivers (PDF pp. 13-14, Tables 2-3). The
headline "Proof-Of-Human" finding: the GAM smooths show clear daily
and weekly seasonal structure — volatility and volume trough during
European sleep hours, lunch-break flattening, peaks at 17:00-20:00
when routine jobs end, weekend declines for both volatility and
volume — a human/corporate activity signature that a 24/7 algorithm-
driven market "should not" produce; the authors conclude that in
2018 the crypto market's activity was shaped predominantly by human
agents, with algorithmic trading's overall impact "negligible"
(PDF pp. 15-19). Notably they also report the seasonality's
explanatory power is tiny (R^2 around 1%) even though the smooth
terms are highly significant (PDF p. 15).

## Findings, graded (does any kill line move?)

**NO kill line changed. NO new candidate sharpening.** All five
C1-L2 lines, C8's eleven, and C5's four stand:

1. **[reinforcing, no new item] Measured intraday and weekly
   seasonality in crypto — the queued drift item's second seasonality
   citation.** The paper measures, at a 5-minute grain, exactly the
   calendar structure the drift-reporting item (extended by session
   15's Barzykin seasonality read) exists to handle: time-of-day
   and day-of-week components in volatility AND volume, toward the
   trough-peak pattern of the human/corporate clock (PDF pp. 16-17,
   Figures 7-10). Two layers of reinforcement: (a) calendar
   structure is REAL in crypto even in a hypertechnical venue-
   agnostic index — any drift statistic computed over gated BTCUSDT
   windows without declaring calendar composition would fold
   seasonality into "drift" silently, an artifact no label placebo
   could catch; the queued drift item already forces the calendar
   declaration, and this read adds a measured precedent at a
   neighboring grain; (b) the same R^2-around-1% observation is a
   caveat the item already carries implicitly but which this paper
   states cleanly: the seasonality is highly significant and small —
   it is a measurement-contamination concern (drift reporting),
   NOT an exploitable-effect claim. Nothing about the queued item's
   legal content changes; it is not re-armed or re-worded here.

2. **[interpretation caution] Agent composition is a REGIME
   VARIABLE, and its measurement is vintage- and venue-local.**
   The "Proof-Of-Human" conclusion is built on 2018 European-spot
   vacation data and explicitly framed against media hype about
   algorithmic trading (PDF pp. 5-6, 15). For the program this is
   a two-sided warning: (a) any structural claim about WHO trades
   (humans vs. algorithms) decays — agent composition drifts with
   market maturity, venue, and period, and an inference about
   composition on one vintage tells you nothing about another
   (2018 vacation Europe vs. CME's engine-transaction races in
   session 19's 2025 feed study are the same asset class at
   different maturity: the composition is not portable); (b) any
   future market-structure narrative in the record cites its
   vintage and venue before its conclusion. This extends the
   venue-freeze warrant (session 14) and the regressed-process
   caution (session 21) into a new dimension: composition drift.

3. **[reinforcing, no new item] The stylized facts line up with the
   program's priors, quoting nothing new.** Near-zero first-order
   return autocorrelation with strongly positive absolute/squared-
   return autocorrelation (volatility clustering) and extreme
   leptokurtosis at the 5-minute grain (PDF p. 12, Table 1) are the
   same stylized facts the program has already recorded from other
   crypto reads — one more citation in the "the grain's moments are
   the grain's own" family; readings from different grains are
   different objects (the estimator-mode and aggregation-endogeneity
   lines), and nothing here licenses a statement about any other
   grain or venue.

## What this paper would have killed if we had done it wrong

If the drift-reporting discipline had been written as "drift is a
nuisance parameter, report it as a single number per window," this
paper's measured calendar structure means those numbers would have
been mixtures of window calendar composition and actual drift — a
confound that changes sign across sessions and weekends. And if any
line of the record had carried a "crypto is algorithm-dominated,
therefore calendar effects are dead" narrative — the exact media
narrative the paper debunks for its vintage — every downstream
calendar logic built on it would have been resting on an unmeasured
assumption. The program's existing grain- and calendar-declaration
discipline keeps both failures off the table.

## Standing caveat

Five-minute European-sourced index/spot data from a single two-month
2018 window — not a perpetual-futures order book; the GAM R^2 ~ 1%
means seasonality is a real but SMALL component, and the
significance is partly a sample-size artifact of 5-minute frequency;
the PoH argument assumes absence of algorithms that mimic human
calendars (news-driven bots); "negligible algorithmic impact" is the
authors' inference from seasonality, not a direct observation of
agent identity; published version exists (European Journal of
Finance, DOI 10.1080/1351847X.2020.1789684) — the shelf copy is the
pre-copyedit arXiv v1, check the published version before formal
citation. Execution content: none — a descriptive study; nothing to
operationalize; cost-survival relevance: none.
