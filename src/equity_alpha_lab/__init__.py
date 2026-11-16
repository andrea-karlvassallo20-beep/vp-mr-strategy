"""equity-alpha-lab: Month-1 point-in-time equity data pipeline.

DEScriptive infrastructure only. No factor, model, or claim is tested by
this package; it exists so that every later feature and target can be
traced to information available at decision time.

Submodules:
- schema: canonical panel schemas and column validators.
- universe: point-in-time universe membership (survivorship-aware).
- pit: point-in-time snapshots of fundamentals (announce-date discipline).
- returns: forward returns with entry delay, delisting handling, and
  no-lookahead construction.
- quality: data-quality checks (adjustment continuity, missingness,
  calendar alignment) and the leakage tripwire.
"""

from .schema import (
    SECURITY_MASTER_COLUMNS,
    PRICE_COLUMNS,
    FUNDAMENTALS_COLUMNS,
    validate_security_master,
    validate_prices,
    validate_fundamentals,
)
from .universe import universe_asof, survivorship_audit
from .pit import pit_fundamentals, assert_no_future_information
from .returns import forward_returns, total_return_series
from .quality import (
    adjustment_continuity_report,
    missingness_report,
    check_panel,
    LeakageError,
)
from .factors import PRICE_FACTORS, compute_all, momentum, reversal, volatility, range_position, amihud_illiquidity, dollar_volume
from .evaluation import ic_series, ic_summary, quantile_returns, top_bucket_turnover
from .inference import (
    newey_west_tstat,
    ic_inference,
    fama_macbeth,
    bonferroni_threshold,
    bonferroni_t_threshold,
)

__all__ = [
    "SECURITY_MASTER_COLUMNS",
    "PRICE_COLUMNS",
    "FUNDAMENTALS_COLUMNS",
    "validate_security_master",
    "validate_prices",
    "validate_fundamentals",
    "universe_asof",
    "survivorship_audit",
    "pit_fundamentals",
    "assert_no_future_information",
    "forward_returns",
    "total_return_series",
    "adjustment_continuity_report",
    "missingness_report",
    "check_panel",
    "LeakageError",
    "PRICE_FACTORS",
    "compute_all",
    "momentum",
    "reversal",
    "volatility",
    "range_position",
    "amihud_illiquidity",
    "dollar_volume",
    "ic_series",
    "ic_summary",
    "quantile_returns",
    "top_bucket_turnover",
    "newey_west_tstat",
    "ic_inference",
    "fama_macbeth",
    "bonferroni_threshold",
    "bonferroni_t_threshold",
]
