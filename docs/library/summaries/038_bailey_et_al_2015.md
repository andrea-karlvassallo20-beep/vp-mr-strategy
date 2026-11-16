# 038 — The Backtest Overfitting Problem (Bailey, Borwein, Lopez de Prado & Zhu, 2015)

**Venue:** working paper (journal: Journal of Computational Finance) | **Category:** Backtesting & FML
**Status:** Downloaded legally (arXiv:1502.03562); full text: `docs/library/text/038_bailey_borwezi_lopez_de_prado_zhu.txt`.

## Summary
The paper that named the problem: given enough strategy
configurations tried on one history, the best backtest is expected
to look good even when all configurations are worthless. Proves
that under broad conditions the maximum Sharpe over $N$ trials
grows like $\sqrt{2\ln N}$, quantifies how few independent bets
most backtests contain, and motivates CPCV and PBO as correctives.
The practical upshot: a backtest is evidence about the search
process, not about the strategy.

## The math that matters
$E[\max_{n\le N} SR_n] \approx \sqrt{2\ln N}$ for independent
trials; minimum backtest length (MinBTL) needed for a Sharpe to be
statistically distinguishable from zero; PBO via rank overlap
across CPCV paths (with 009).

## Why it matters for the L2 project
The C8 kill lines inherit this paper's arithmetic: the number of
(macro x micro x threshold) cells tried is the tax on the one
reading reported. The DSR line in the cheatsheet implements its
formula.

**Caveat:** Verify page numbers against the extracted text before
production.
