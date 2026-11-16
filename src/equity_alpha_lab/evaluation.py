"""Factor evaluation machinery: rank IC, quantile spreads, turnover.

DESCRIPTIVE ONLY. These are the measuring instruments, not verdicts. The
inference rules (what IC counts as a signal, which quantile spread counts
as monotonic, how multiple testing is handled) belong to a pre-registered
spec, not to this module.

Conventions (frozen):
- IC is the per-date Spearman rank correlation between the factor value and
  the forward return over the declared horizon, computed on the
  intersection of available names per date.
- Quantile buckets are assigned by per-date factor rank into `n_buckets`
  equal-sized groups (largest factor value = top bucket).
- Turnover is the per-date fraction of the top-bucket membership that
  changed versus the previous date.

Limitations stated up front: the IC t-stat here is naive (i.i.d. across
dates). Serial dependence in IC and cross-sectional correlation are real;
the honest inference layer (Newey-West, Fama-MacBeth, multiple-testing
control) is Month-2 follow-up work and must precede any claim.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _merge(factor: pd.DataFrame, fwd: pd.DataFrame) -> pd.DataFrame:
    """Inner-join a factor long frame with a forward-returns frame on (sid, date)."""
    f = factor[["sid", "date", "value"]].rename(columns={"value": "factor"})
    m = f.merge(
        fwd[["sid", "decision_date", "fwd_ret"]],
        left_on=["sid", "date"],
        right_on=["sid", "decision_date"],
        how="inner",
    ).drop(columns=["decision_date"])
    return m.dropna(subset=["factor", "fwd_ret"])


def ic_series(factor: pd.DataFrame, fwd: pd.DataFrame) -> pd.Series:
    """Per-date Spearman rank IC between factor and forward return."""
    m = _merge(factor, fwd)
    if m.empty:
        return pd.Series(dtype="float64", name="ic")
    ranked = m.groupby("date")[["factor", "fwd_ret"]].rank()
    ranked["date"] = m["date"]
    ic = ranked.groupby("date").apply(
        lambda g: g["factor"].corr(g["fwd_ret"]), include_groups=False
    )
    return ic.rename("ic")


def ic_summary(factor: pd.DataFrame, fwd: pd.DataFrame) -> dict:
    """Mean IC, std, naive t-stat, ICIR, hit rate, n dates, n names per date."""
    ic = ic_series(factor, fwd)
    n = len(ic)
    if n == 0:
        return {"n_dates": 0, "mean_ic": float("nan"), "ic_ir": float("nan")}
    mean = float(ic.mean())
    std = float(ic.std(ddof=1)) if n > 1 else float("nan")
    return {
        "n_dates": n,
        "mean_ic": mean,
        "std_ic": std,
        "t_stat_naive": float(mean / std * np.sqrt(n)) if std and std > 0 else float("nan"),
        "ic_ir": float(mean / std) if std and std > 0 else float("nan"),
        "hit_rate": float((ic > 0).mean()),
        "min_names_per_date": int(_merge(factor, fwd).groupby("date").size().min()),
    }


def quantile_returns(
    factor: pd.DataFrame, fwd: pd.DataFrame, n_buckets: int = 5
) -> pd.DataFrame:
    """Per-date mean forward return per factor quantile bucket.

    Output: wide frame indexed by date, one column per bucket
    (bucket 1 = lowest factor value, bucket n = highest), plus `spread` =
    top minus bottom.
    """
    m = _merge(factor, fwd)
    if m.empty:
        return pd.DataFrame()
    m["bucket"] = m.groupby("date")["factor"].rank(
        method="first", pct=True
    ).apply(lambda p: min(int(p * n_buckets) + 1, n_buckets))
    wide = m.pivot_table(index="date", columns="bucket", values="fwd_ret", aggfunc="mean")
    wide.columns = [f"q{c}" for c in wide.columns]
    wide["spread"] = wide[f"q{n_buckets}"] - wide["q1"]
    return wide


def top_bucket_turnover(
    factor: pd.DataFrame, fwd: pd.DataFrame, n_buckets: int = 5
) -> pd.Series:
    """Per-date fraction of top-bucket membership that changed vs prior date."""
    m = _merge(factor, fwd)
    if m.empty:
        return pd.Series(dtype="float64", name="turnover")
    m["bucket"] = m.groupby("date")["factor"].rank(
        method="first", pct=True
    ).apply(lambda p: min(int(p * n_buckets) + 1, n_buckets))
    top = m[m["bucket"] == n_buckets]
    memberships = top.groupby("date")["sid"].apply(set)
    dates = sorted(memberships.index)
    out = {}
    for prev, cur in zip(dates, dates[1:]):
        a, b = memberships[prev], memberships[cur]
        union = a | b
        out[cur] = len(b - a) / len(union) if union else float("nan")
    return pd.Series(out, name="turnover").sort_index()
