# Deep-read session 45 (null-time session 49, log entry 53): Lipton, Pesavento, Sotiropoulos, "Trade arrival dynamics and quote imbalance in a limit order book"

Authors: Alexander Lipton (Bank of America Merrill Lynch and Imperial College),
Umberto Pesavento, Michael G Sotiropoulos (Bank of America Merrill Lynch).
Full title: "Trade arrival dynamics and quote imbalance in a limit order book".
Venue: arXiv:1312.0514v1 [q-fin.TR], 2 December 2013. A diffusion model of the
top-of-book queues plus an unobservable trade-arrival process, jointly
calibrated to event probabilities and passive-fill expectations on one liquid
equity.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8
faster, or change their kill lines? Source: legally acquired OA copy
(docs/library/text/x5f04ef_trade_arrival_dynamics_and_quote_imbalance_in_a_li.txt,
15 pp., page-marked). Next UNREAD triage-rank entry (score 29).

## The paper in one paragraph

The authors study the bid/ask queue imbalance at the top of the book,
I = (qb - qa)/(qb + qa), and its relationship to trade-arrival intensity on
VOD.L over Q1 2012 (PDF pp. 1-2). Empirically, the average mid-price move
until the next quote change grows roughly linearly with imbalance, up to
about a third of the spread in a highly imbalanced book, while the waiting
time to the next move shortens (Fig. 1, PDF pp. 3-5); the authors state
explicitly that imbalance "does not by itself offer an opportunity for a
straightforward statistical arbitrage" (PDF p. 4). Conditioning on the side
of the stopping trade, average mid-price moves until the next matching
(sell) trade shift upward relative to next buy trades, read as an
information/timing advantage of aggressive traders over passive quotes
(Fig. 2, PDF pp. 5-6), and event probabilities (favourable move, adverse
move, passive fill) are bucketed by imbalance (Fig. 3, PDF p. 7). To capture
this, they extend the Cont-de Larrard two-dimensional queue diffusion with a
third, unobservable process phi for near-side trade arrival -- making the
model non-Markovian, reset by draws from a calibrated phi_0 -- and solve the
hitting-probability PDE semi-analytically via correlation-removing and
spherical coordinate transforms plus a Fourier series on a transformed domain
(PDF pp. 6-11, Eqs. 2-25). Joint calibration to the empirical curves yields
rho_xz = -rho_yz = 0.8, rho_xy = -0.1, phi_0 = 3.5 s^(1/2) (Fig. 6, PDF
pp. 12-13); the model reproduces the buy/sell shift and the gross shapes of
event probabilities, and queue/trade interaction alone is reported
responsible for the loss of about 60 per cent of the theoretical spread
capture of a passive fill, with favourable-move probability falling to near
10 per cent at high near-side imbalance (Fig. 7, PDF pp. 13-14). Execution
applications (spread-crossing policies) are left for future work (PDF pp. 12,
14).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening.

1. [reinforcing, no new item] The paper's own headline discipline: quote
   imbalance at the top of the book predicts the direction and rough size of
   the average next mid-price move (up to about a third of the spread,
   Fig. 1, PDF pp. 3-5), and the authors themselves state it does not offer a
   straightforward statistical arbitrage (PDF p. 4). This is another worked
   exhibit for the programme's direction-versus-magnitude discipline and for
   the economic-gate requirement that a predicted move must be sized against
   spread and costs before it is worth anything. No rule moves; nothing is
   licensed beyond what kill lines already encode.

2. [interpretation caution] Every empirical quantity here is
   event-conditional: the stopping times are the next mid-price change, or
   the next arrival of a trade of a given side, conditioned on the state at a
   quote update (PDF pp. 4-5, Table 1, PDF p. 5). This is next-event
   predictability at book-update grain, the same category the Dixon LOB-RNN
   session graded; it licenses nothing about any time-horizon clock, and a
   future feature built from imbalance statistics may never be read as
   supporting a coarser-grain compression-clock claim without its own
   horizon-explicit test. No queue change; a reading mode.

3. [interpretation caution] The calibrated model is a four-parameter joint
   fit (three correlations plus phi_0) to the same empirical curves it is
   compared against, in-sample, on one stock (Figs. 6-7, PDF pp. 12-14),
   with the symmetry rho_xz = -rho_yz imposed (Fig. 6 caption, PDF p. 13)
   and with "calibrations against other liquid stocks displayed qualitatively
   similar results" asserted but not exhibited (PDF p. 12). The calibrated
   values are in-sample outputs of one equity venue, not venue-regular
   properties. Any future fitted microstructure model in the programme must
   disclose parameter count against held-out validation, and these numbers
   may not enter any spec table as if they were measured venue constants.
   No queue change; a reading mode.

4. [cost-survival ammunition] The paper's economically load-bearing number
   -- passive fills lose about 60 per cent of their theoretical spread
   capture to the interaction of queue depletion and trade flow, before any
   adverse-selection story (PDF pp. 12-13) -- is an LSE equity,
   tick-constrained, maker-taker calibration on one stock in one quarter. If
   a future K7-style cost-survival layer ever exists for passive-fill claims
   on the programme venue, it must carry queue-depletion/trade-flow slippage
   as an axis distinct from adverse selection, and must re-estimate, not
   import, the 60 per cent figure: its magnitude is venue
   microstructure-specific. Relevance is conditional on that future layer;
   nothing is armed here.

5. [source-quality note] Single instrument (VOD.L), single quarter (Q1
   2012), restricted to top-of-book observables; error bars from treating
   daily averages as independent (PDF pp. 3, 7); trade side inferred from
   price versus prevailing quotes (PDF p. 5), which misclassifies executions
   inside the spread and biases side-conditioned quantities; the trade-side
   register concern interacts with the already-queued sign-register
   sharpening family. ArXiv v1 read as-is; a later journal version was NOT
   checked at reading (uncertain, flagged for verification).

## What this paper would have killed if we had done it wrong

Had the Fig. 1 imbalance predictability been laundered into "C1-L2 is
pre-confirmed, the top of the book already predicts price", a
to-a-third-of-the-spread next-event effect on one LSE equity, with no cost
model and the authors' own no-arbitrage sentence on the same page, would have
been passed off as support for a compression-clock claim it never makes; the
first costed firing would have killed the claim and taken the programme's
credibility with it. Had the 60 per cent passive-slippage loss been imported
as a transferable constant, an LSE-equity calibration carrying an imposed
symmetry assumption would have inflated a future cost-survival margin on a
materially different venue, exactly the cross-venue import the house rules
forbid. Had the non-Markovian phi model been treated as a validated
generator rather than a four-parameter in-sample fit, semi-analytic elegance
would have smuggled venue-inapplicable parameters into a spec table. Had the
price-versus-quote side inference been adopted as ground truth, mislabeled
mid-book executions would have contaminated any future trade-side register
from the first row.

## Standing caveat

One liquid LSE equity, one quarter, top-of-book observables only, an
unobservable time-to-fill surrogate process calibrated jointly and in
sample, side labels inferred rather than published, and an agency-broker
execution framing that per house rules is never operationalized. The
library is ammunition, not evidence: nothing in this paper enters any spec,
default, kill line, threshold, or generative null; it charges warnings
only.
