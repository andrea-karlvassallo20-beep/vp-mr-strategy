"""Knowledge-grounded candidate extensions for VP-MR-ETF-D1-001.

Derived from the Market Studies Knowledge Base (KNOWLEDGE.md):

- EWMA volatility (Levy, Computational Finance: IGARCH/EWMA with
  lambda = 0.97, the RiskMetrics special case of GARCH(1,1)) — vol
  clustering is a stylized fact; a flat 60-day realized window ignores it.
- GARCH(1,1) canonical forecast (alpha=0.05, beta=0.90, persistence
  0.95 < 1 per the Levy persistence condition) with long-run variance
  anchored to the trailing sample.
- VSA volume filter (Williams, Master the Markets: "effort vs results" /
  "no demand") — a z-score stretch on weak volume suggests absence of
  real pressure rather than informed flow (Stoll/Madhavan: information
  effects are permanent; a low-volume stretch is more likely transitory).

All estimates use strictly trailing windows (Gate 1). These are RESEARCH
CANDIDATES evaluated by the edge-seeker; the deployed strategy remains
frozen (Gate 3). Javaheri's identification hierarchy justifies simple
(GARCH/EWMA) over rich stochastic-vol models at daily frequency: noise
parameters are nearly unestimable daily.
"""
import math
from collections import deque
from typing import Deque, Dict, Optional

import numpy as np

from vp_mr_strategy import (StrategyParameters,
                            VolatilityParityMeanReversionStrategy)

EWMA_LAMBDA = 0.97          # RiskMetrics / Levy IGARCH special case
GARCH_ALPHA = 0.05          # canonical persistence 0.95 < 1
GARCH_BETA = 0.90
VOLUME_LOOKBACK = 20        # VSA effort baseline


def ewma_vol_ann(closes: np.ndarray, bars_per_year: float) -> Optional[float]:
    if len(closes) < 30:
        return None
    r = np.diff(np.log(closes))
    var = float(np.var(r))          # seed with sample variance
    for x in r:
        var = EWMA_LAMBDA * var + (1 - EWMA_LAMBDA) * x * x
    return float(math.sqrt(var * bars_per_year))


def garch_vol_ann(closes: np.ndarray, bars_per_year: float) -> Optional[float]:
    if len(closes) < 30:
        return None
    r = np.diff(np.log(closes))
    long_run = float(np.var(r))
    var = long_run
    for x in r:
        var = (GARCH_ALPHA * x * x + GARCH_BETA * var
               + (1 - GARCH_ALPHA - GARCH_BETA) * long_run)
    return float(math.sqrt(var * bars_per_year))


class VariantStrategy(VolatilityParityMeanReversionStrategy):
    """Research variant: selectable vol model (for vol-parity sizing) and an
    optional VSA volume filter on entries. Strictly trailing state."""

    def __init__(self, params: StrategyParameters, universe, initial_equity,
                 vol_model: str = "realized",
                 volume_filter: bool = False) -> None:
        super().__init__(params, universe, initial_equity)
        self.vol_model = vol_model
        self.volume_filter = volume_filter
        self._vol_buf: Dict[str, Deque[float]] = {
            s: deque(maxlen=VOLUME_LOOKBACK + 5) for s in universe}

    def _realized_vol_ann(self, s: str) -> Optional[float]:
        if self.vol_model == "ewma":
            return ewma_vol_ann(np.asarray(self._close[s]),
                                self.p.bars_per_year)
        if self.vol_model == "garch":
            return garch_vol_ann(np.asarray(self._close[s]),
                                 self.p.bars_per_year)
        return super()._realized_vol_ann(s)

    def _signals(self, s: str):
        if not self.volume_filter:
            return super()._signals(s)
        z = self._zscore(s) if self._warm(s) else None
        le, se, lx, sx = super()._signals(s)
        if z is None:
            return le, se, lx, sx
        buf = self._vol_buf[s]
        # VSA effort check at decision time: the bar that produced the
        # z-score stretch must show WEAK volume vs its trailing mean
        # (absence of real pressure -> stretch more likely transitory)
        if buf and len(buf) >= VOLUME_LOOKBACK and (le or se):
            recent = list(buf)[-VOLUME_LOOKBACK:]
            baseline = float(np.mean(recent[:-1]))
            weak_effort = recent[-1] < baseline
            return (le and weak_effort, se and weak_effort, lx, sx)
        return le, se, lx, sx

    def on_bar_close(self, s, ts, o, h, l, c, v):
        super().on_bar_close(s, ts, o, h, l, c, v)
        # append AFTER the decision so signals use only t-1 volumes
        if math.isfinite(v) and v >= 0:
            self._vol_buf[s].append(float(v))
