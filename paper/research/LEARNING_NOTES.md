# Learning Notes — The Market Research Database, Explained Simply

A plain-language guide to what lives in this repository, how the research
knowledge is organised, and where the program currently stands. Written for
study, not for execution. Separate from the medical education project.

---

## 1. What this repository IS

A research knowledge base for one question:

> Can order-flow and liquidity structure predict WHEN and WHICH WAY a major
> price move happens — first in crypto, then possibly across a panel?

It is built on TWO pillars:

1. **The book knowledge base** ("Market Studies", `KNOWLEDGE.md`) — the
   accumulated market research from the work sessions: 13 books studied
   one at a time, from Elliott Wave as the base framework through the full
   microstructure stack to the mathematical-finance core. This is where the
   ideas come from.
2. **The falsification lab** (`paper/research/`) — where those ideas are turned
   into claims that can die, with kill lines declared before testing. This
   is where the ideas face the data.

It is run like a lab, not like a trading desk. The core discipline is
**falsification**: every idea is written down as a claim that CAN fail, with
the exact result that would kill it ("kill line") declared BEFORE it is
tested. An idea that cannot fail is marketing, not research.

Three questions are kept strictly separate, and no single model may answer
two of them:

| Question | Name | Status on current data |
|---|---|---|
| WHEN does a move happen? | Hazard (timing) | The only one testable so far |
| WHICH WAY does it go? | Direction | Blocked — no order-flow data yet |
| HOW MUCH to size? | Sizing | Blocked — needs a direction posterior first |

## 2. The map — what lives where

```
KNOWLEDGE.md, KNOWLEDGE_SMH.md   <-- THE BOOK KNOWLEDGE BASE ("Market Studies")
   Study notes distilled book-by-book from Andrea's trading/markets book
   collection: 13 books fully studied + 1 partial, with a reading queue.
   The FOUNDATION of all market research in this repo (see section 2b).

paper/research/                 <-- THE RESEARCH KNOWLEDGE BASE (the lab)
  orderflow_program.md          The constitution: data inventory, claims, kill
                                lines, what is blocked and why
  c1_hazard_report.md           The C1 experiment and its verdict (FAILED)
  c1_hazard_btc.json / _eth.json  Raw results, machine-readable
  c1_l2_test_spec.md            The NEXT experiment, drafted but NOT run
  l2_data_acquisition_spec.md   Exactly what data must be bought/recorded next
  LEARNING_NOTES.md             This file
  (older files: the daily-bar studies that came before this program)
  data/                         ~156 crypto pairs, DAILY bars (no order flow)
strategy/                       The code (backtests, tests, the C1 experiment)
paper/data/                     5 US ETFs, daily bars
docs/, DASHBOARD.md             Presentation layer (thesis, live instrument)
```

Reading order for a newcomer: `KNOWLEDGE.md` (the accumulated book research) →
`orderflow_program.md` (the rules and claims) → `c1_hazard_report.md` (what was
tested and what died) → `c1_l2_test_spec.md` (what happens next and why).

### 2b. The book knowledge base — the market research from the work sessions

The market research did not start with the falsification program. It was
built book by book, and every later decision rests on it. Current state:
13 books fully studied and noted, 1 partial, with a queue behind them.

**The base framework:** Elliott Wave Principle (Balan, 1989) — the founding
layer that everything else links back to. Important honest caveat: in this
lab, wave counts are treated as a descriptive language, NOT as evidence —
directional claims from price patterns are bounded by the measured coin-flip
result (P(up) = 0.505) and Elliott labels may only be used if they are given
a deterministic, reproducible operationalization first.

**The microstructure stack** (why order flow is the research frontier):

| Book | Layer | The durable idea in one line |
|---|---|---|
| Harris, Trading and Exchanges (2002) | Microstructure | How the limit order book actually works: orders, queues, and who trades with whom |
| Hasbrouck, Empirical Market Microstructure (2004) | Statistical | Prices as conditional expectations; how to measure what flow reveals (Roll, VAR) |
| Biais, Glosten & Spatt survey (~2005) | Unified theory | One synthetic model unifying the classic microstructure papers |
| Bouchaud et al., Trades, Quotes and Prices (2018) | Econophysics (PARTIAL — only Ch. 1–2.1.4 studied) | Bottom-up: queue models, Hawkes processes, price impact laws. Resume when full text uploaded |
| Foucault, Pagano & Röell, Market Liquidity (2013) | Theory/policy | Kyle's lambda, PIN, liquidity measurement and market design |
| Stoll survey (2002) | Founder's retrospective | The five sources of the spread and their time-series fingerprints |
| Madhavan survey (2000) | Information economics | Information effects are permanent, inventory effects transitory; transparency redistributes |

**The practitioner/indicator layer:** Tom Williams, Master the Markets
(VSA, 2009) — the signal dictionary (tests, up-thrusts, climaxes, shake-outs,
no demand, absorption) and "effort vs result". This is where the C2 and C3
claims came from — and why they had to be operationalized (breach-and-recover
with parameters) before they could even be declared as claims.

**The history/model-risk layer:** Dark Pools and The Quants (Patterson) —
how HFT and the quant era rose, the Flash Crash anatomy (quote withdrawal +
feedback loops), 1987 and August 2007 as feedback-loop warnings, fat tails
(Mandelbrot vindicated), and the Financial Modelers' Manifesto. These books
are why the lab refuses untested models and demands kill lines.

**The mathematical-finance core:** Björk, Arbitrage Theory in Continuous
Time (complete: both Fundamental Theorems, Black-Scholes, martingale
pricing, HJB/Merton, term structure, forward measures); Javaheri, Inside
Volatility Arbitrage (the volatility-model zoo and the identification
hierarchy — which parameters can actually be estimated at daily frequency:
almost none of the noise ones); Levy, Computational Finance (numerical
pricing and GARCH econometrics — the persistence condition, why fat tails
appear even from Gaussian inputs, and the S&P 500 identification result).

**The reading queue (still open):** Applied Quantitative Finance, then
Analysis of Financial Time Series, Mathematics of Financial Markets, the
algorithmic/HFT books, then Nonlinear Optimization. The end goal, set in
Nov 2026: after all books are studied, use the accumulated knowledge to
build a trading strategy and run the next research phase — which is exactly
what the falsification program now is.

**How the books connect to the claims ledger (the bridge):**

- VSA "effort vs result" → operationalized as accumulated volume per unit
  price change → became claim C2 (now dead by dependency).
- VSA springs/up-thrusts → operationalized as breach-and-recover → C3
  (closed with the daily program, never run).
- Harris/Hasbrouck/Foucault order-flow economics (Kyle's lambda, PIN,
  spread decomposition) → the entire L2 layer: C5 (absorption asymmetry)
  and C6 (depth OFI), both blocked on the Tardis data.
- Bouchaud's Hawkes-process chapters (unstudied yet) → the Hawkes
  excitation matrix in Layer 2; the cancellation-fraction kill switch in
  the acquisition spec exists because a book-frozen book makes Hawkes
  meaningless.
- The Quants/1987/2007 → the CVaR/drawdown constraint and the refusal to
  size on a wide posterior (Layer 4), and the refusal to trust simulated
  profitability.
- Stoll/Madhavan "information effects are permanent, inventory effects
  transitory" → the design rule that direction, if it ever exists, must
  come from flow, not price.
- Björk/Javaheri/Levy → the estimation discipline: knowing which parameters
  are identifiable at which frequency is why the lab refuses to fit noise.

## 3. The claims ledger — a scoreboard where ideas die

Each claim is recorded in a fixed format so nothing can quietly morph:

- **CLAIM** — one sentence that can be false.
- **MECHANISM** — WHY it should be true (liquidity, flow toxicity, duration).
  "Because the backtest says so" is not a mechanism.
- **TEST** — the exact statistic and the exact data.
- **KILL LINE** — declared in advance: the result that ends the claim.
- **STATUS** — untested / tested-pass / tested-fail / blocked-on-data.
- **WHAT IT CANNOT TELL YOU** — the honest boundary.

Current scoreboard:

| Claim | One-line idea | Status |
|---|---|---|
| C1 | Compression (quiet range) raises breakout hazard | **tested-fail** (BTC & ETH) |
| C2 | Volume dry-up conditions the hazard | **dead by dependency** (base died; never tested) |
| C3 | Spring/upthrust raises breakout hazard | closed with the daily program (never run) |
| C4 | Hazard differs by market phase | closed with the daily program (never run) |
| C5 | Absorption asymmetry predicts break direction/timing | blocked-on-data (needs L2) |
| C6 | Depth order-flow adds timing information | blocked-on-data (needs L2) |

## 4. What we learned from C1 — the one completed experiment

We asked: after the market goes quiet (a compressed range), does time-in-range
predict when it breaks out? Mechanism: resting orders at the range edges age,
so the market should break sooner as time passes.

**Answer: no — and we know why.** Four independent kill lines all fired:

1. **Vol-tautology:** once you know the CURRENT volatility level, the
   "compression" flag adds nothing. Compression was volatility wearing a costume.
2. **Placebo:** shuffling the timeline while preserving volatility clustering
   reproduced the whole "effect." The alignment was mechanical.
3. **Scale-invariance null:** a synthetic market that has volatility clustering
   but NO liquidity mechanism reproduced the same numbers.
4. Same result on BOTH instruments (BTC and ETH), so it is not instrument luck.

The honest demotion: the daily data can only give you a **"volatility clock"**
— high volatility means barriers get hit sooner, which is close to trivial —
and a volatility clock is not a timing edge. The daily-resolution program is
CLOSED. No further daily tests will be run, by pre-commitment.

## 5. Why the program is blocked — and on what

The original question is about ORDER FLOW: the actual sequence of bids, asks,
cancellations, and trades. Daily bars contain NONE of that. We hold:

- Daily OHLCV bars only (5 US ETFs + ~156 crypto pairs).
- No order book, no trade-by-trade data, no intraday, no cancellations.

So Layers 0–2 of the research architecture (book reconstruction,
microstructure features, order-flow signals) cannot even be started —
not "hard", but **impossible without new data**. That is why the next task
is data acquisition: full-depth order-book updates + signed trades for ONE
instrument (Binance BTCUSDT perpetual, 2–4 weeks, purchased from Tardis.dev),
which must pass a verification gate (rebuild the book, compare against 100
exchange snapshots, one-tick tolerance) before ANY modelling.

## 6. The rules that make this trustworthy (the epistemic contract)

1. Never say "prove." Every result is an estimate with a confidence interval
   and a sample size.
2. Declare the kill line BEFORE testing — no moving goalposts afterwards.
3. Never label an event using information from after the event.
4. Direction cannot come from price patterns — a prior study of 15,386
   episodes measured P(up) = 0.505, a coin flip. Direction must come from
   order-flow data we don't yet have.
5. When a test fails, NAME the mechanism that died. No pivoting to a nearby
   idea that happens to survive.
6. If you cannot test something, say so and stop. No silent proxy substitution.
7. One instrument must survive before any panel of pairs is attempted.

## 7. Where the program stands right now (the one-paragraph state)

The daily-resolution program is closed: C1 failed on both instruments and the
whole daily hazard layer was demoted to a descriptive volatility clock; C2
died by dependency; C3/C4 were never run; C5/C6 remain blocked because the
order-flow data does not exist in the database yet. The next experiment
(C1 re-run at L2 resolution — does the compression effect exist when the
state is measured from the order book instead of daily bars?) is fully
specified with pre-declared kill lines and is waiting on one thing only:
procurement of the Tardis.dev dataset and its verification. Nothing runs
until that data passes the gate.

In parallel, the book programme continues: Bouchaud is paused on a partial
upload, and the queue (Applied Quantitative Finance, Analysis of Financial
Time Series, the algorithmic/HFT books, Nonlinear Optimization) feeds the
same lab — each new book is another candidate source of claims, and the
Bouchaud Hawkes/queue chapters in particular are required reading before
C5/C6 ever run.
