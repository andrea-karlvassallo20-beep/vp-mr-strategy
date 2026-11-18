# Deep-read session 27 — Barzykin, Boyce, Neuman and Tuschmann, "Optimal Execution with Passive Market Impact"

Library deep-read session 27 (null-time session 31, log entry ## 35).
Alexander Barzykin (HSBC), Robert Boyce, Eyal Neuman and Sturmius
Tuschmann (Department of Mathematics, Imperial College London),
arXiv:2607.28323v1 [q-fin.TR], 30 Jul 2026, 31 pp. text extract,
page-marked. Read 2026-11-18, against ONE question: what here would
kill C1-L2 or C8 faster, or change their kill lines? Source: legally
acquired OA copy
(docs/library/text/x28ad86_optimal_execution_with_passive_market_impact.txt).
Assigned triage-rank entry (score 33, x28ad86). Next UNREAD
triage-rank entry (score 32, x947263, "State-dependent Hawkes
processes and their application to limit order book modelling").

## The paper in one paragraph

A mesoscopic optimal-execution model in which a liquidating trader
posts unit sell limit orders at a controlled distance delta from the
midprice: fills arrive with an Avellaneda-Stoikov intensity
lambda·e^(−k·delta), and each passive fill carries permanent impact at
rate eta·e^(−m·delta), derived by combining the fill intensity with
the Cont-Kukanov-Stoikov / Xu-Gould-Howison linear response of
mid-price changes to (multi-level) order flow imbalance whose impact
coefficient beta(delta) is assumed to decay exponentially with
distance (PDF pp. 4-5, eqs. (2.1)-(2.8)). With m = k the HJB system
is linearised and the optimal quote is explicit (PDF p. 7, Theorem
3.1); with m ≠ k a Lambert-W semi-explicit solution holds (PDF pp.
17-18, Theorem 6.1); extensions cover transient impact and TWAP-style
targets (PDF pp. 19-22). Calibration: fill-intensity decay k estimated
from LOBSTER NASDAQ order records (six stocks, 2016) and from LSEG FX
public quote and trade data (five pairs, 100 business days of 2026);
impact decay l fitted to the published MLOFI ridge coefficients of
Xu, Gould and Howison; headline finding l ≪ k for equities, so
m ≈ k there, with a visible gap in FX (PDF pp. 11-17, Tables 4-5).

## Findings, graded

NO kill line changed. NO new candidate sharpening queued. This is the
default grade: nothing here earns a rule.

1. **[reinforcing, no new item]** An independent, page-cited second
   mechanism for the queue-state conditioning rule queued through
   deep-read session 26 (still PENDING OWNER RATIFICATION, unchanged
   in scope). For the large-tick NASDAQ stocks (ORCL, CSCO, MU) the
   exponential distance-decay fit of MLOFI impact coefficients fails,
   returning slightly negative l, and the authors state their own
   preferred interpretation: "MLOFI price impact may depend more
   directly on the volume queued ahead of an order than on its
   distance from the midprice" (PDF p. 15). A different author team,
   different data (LOBSTER, 2016), same direction as the queued rule's
   premise: passive impact is conditioned on the queue state, not on
   distance alone. Corroboration only; the rule's text, scope and
   ratification status are untouched.

2. **[interpretation caution]** The paper sidesteps, and does not
   test, the passive-impact sign paradox recorded through deep-read
   session 26. The adverse direction of the passive term in the price
   dynamics (a passive sell depresses the impacted midprice, PDF p. 6,
   eq. (3.4)) is inherited from the OFI regression identity — the
   beta of the contemporaneous mid-price-change-on-OFI regression
   (PDF pp. 4-5, eqs. (2.2), (2.6)) — not derived from book state,
   and the authors' own limitations section concedes the estimates
   "measure contemporaneous price responses to aggregate order-book
   events", with a stronger test requiring trader-tagged or
   order-level data (PDF p. 24). This paper is therefore never cited
   as evidence about the sign of passive impact at the level the
   queued rule governs, and never as counter-evidence to the sign
   paradox.

3. **[reinforcing, no new item]** Depth carries information without
   fills: fill probabilities decay exponentially with distance (k in
   the range 0.48-3.72 across the six stocks) while the MLOFI impact
   coefficients persist across book levels (l approximately 0.01-0.02
   for the small-tick stocks), because "limit orders deeper in the
   book still reveal information, thereby moving the price without
   being filled" (PDF p. 14, Table 4). Mechanism-level corroboration
   of C1-L2's standing premise — full-depth L2 carries what taker
   prints cannot see — and consistent with the standing "aggTrades is
   taker prints only" constraint and the replay-days passive-cancel
   context. No number, level count, or decay rate transfers.

4. **[interpretation caution]** Empirical provenance is thin in both
   samples. The equity evidence does not re-estimate impact: it reuses
   the ridge coefficients published in Table 8 of Xu, Gould and
   Howison (PDF p. 13), LOBSTER data, six NASDAQ names, 2016,
   10:00-15:30 windows. The FX evidence is built on conflated L2
   snapshots of at least 5 ms with no event detail, fills proxied
   synthetically by next-bucket aggressor trades reaching a
   hypothetical passive quote (PDF p. 15). No magnitude from either
   sample transfers, ever; the m ≈ k equity headline is a
   paper-sample property.

5. **[source-quality note]** Four authors, one HSBC practitioner and
   three Imperial College mathematicians; arXiv v1 stamped 30 Jul
   2026, roughly four months old at reading; zero indexed citations
   found; unpublished v1, published version to be checked before any
   formal citation. The paper cites deep-read session 26's paper
   (Ouazzani Chahdi et al. [34]) as contemporaneous complementary
   work — the queue-based microscopic foundation beside this
   mesoscopic form (PDF pp. 23-24) — a useful library cross-link.
   The text extract is lightly degraded (some formula glyphs lost in
   the HJB and proof regions), but the model structure follows from
   the prose and numbered equations, and the load-bearing content for
   the ONE question sits in pages 4-17, which are clean.

## Killed if wrong

If the large-tick negative-l fit is later shown to be an estimation
artifact — the authors themselves warn it may "partly reflect this
limitation of the model specification rather than genuine
amplification" (PDF p. 15) — then finding 1's corroboration weakens
to nothing, and the queued queue-state conditioning rule stands alone
on deep-read session 26's mechanism, which is where it already
stands. The corroboration is recorded so it is never cited as
independent proof of the rule; it is one author team's interpretation
of its own anomalous fit.

## Standing caveat

NASDAQ 2016 equities via LOBSTER and borrowed 2018 ridge
coefficients; LSEG FX 2026 public conflated L2 with synthetic fill
proxies; no crypto, no BTCUSDT, no futures, measuring-window
conventions unlike the programme's. Transferable content is
mechanism only: the queue-volume-over-distance conditioning
interpretation and the fills-may-be-absent depth-information point.
Laundering directions named. INTO: no decay rate (k, l, m), impact
coefficient (eta, xi, beta), fill intensity (lambda), or
quote-distance form enters any spec, default, or calibration, and
the passive-impact direction in the record's L2 arm remains governed
by the pending rules and the pre-registered sign guard, never by this
paper's assumed sign; the model is not adopted anywhere without its
own pre-registration. OUT: the m ≈ k equity headline, the
fill-versus-impact decay gap, and the FX estimates are never cited as
evidence about any real market the programme measures, and the deep-
level MLOFI persistence is never cited as expected BTCUSDT depth
behavior.
