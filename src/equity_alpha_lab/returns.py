"""Forward returns with explicit execution timing and delisting handling.

Convention (declared, fixed for the whole programme):
- Features are computed from information up to and including the close of
  date t (decision time).
- Execution happens at the OPEN of the next trading day t+1 (entry_delay=1).
- The forward return for horizon h is measured from the entry price to the
  total-return equivalent of the close h trading days after the entry date.

Delisting: if a security stops trading inside the horizon, the return is
closed out with the security master's delisting_return applied on the last
available trading date. A security with no price after entry and no
delisting return is dropped with a count, never silently filled.

No function here ever reads a price dated before the entry date to compute
the target, and no function ever needs prices beyond t+h — the target is
allowed to see the future; features are not.
"""

from __future__ import annotations

import pandas as pd


def total_return_series(prices: pd.DataFrame) -> pd.Series:
    """Per-sid total-return index from unadjusted close x adj_factor.

    Returns a Series indexed by (sid, date) — the compounded return proxy
    that treats splits and dividends correctly without back-filling prices.
    """
    px = prices.sort_values(["sid", "date"])
    tr = px["close"] * px["adj_factor"]
    idx = pd.MultiIndex.from_frame(px[["sid", "date"]])
    out = pd.Series(tr.values, index=idx, name="total_return_index")
    return out / out.groupby(level="sid").transform("first")


def forward_returns(
    prices: pd.DataFrame,
    security_master: pd.DataFrame,
    horizon: int = 1,
    entry_delay: int = 1,
) -> pd.DataFrame:
    """Forward total returns for every (sid, decision_date) with a price.

    Output columns: sid, decision_date, entry_date, exit_date, fwd_ret,
    delisted (bool), dropped (bool). Rows where no exit price exists and no
    delisting return is recorded are marked dropped=True and returned so
    the caller can count them (they must never enter a backtest silently).
    """
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    if entry_delay < 1:
        raise ValueError("entry_delay must be >= 1 (no same-close execution)")
    px = prices.sort_values(["sid", "date"]).reset_index(drop=True)
    tr = total_return_series(prices).rename("tr")

    rows = []
    sm = security_master.set_index("sid")
    for sid, grp in px.groupby("sid"):
        dates = grp["date"].to_numpy()
        tr_vals = tr.loc[sid].to_numpy() if sid in tr.index.get_level_values(0) else None
        if tr_vals is None:
            tr_vals = tr.xs(sid, level="sid").to_numpy()
        n = len(grp)
        for i in range(n):
            entry_pos = i + entry_delay
            exit_pos = entry_pos + horizon
            decision = dates[i]
            row = {
                "sid": sid,
                "decision_date": decision,
                "entry_date": pd.NaT,
                "exit_date": pd.NaT,
                "fwd_ret": float("nan"),
                "delisted": False,
                "dropped": False,
            }
            if entry_pos >= n:
                # no next trading day to enter on: either a delisting, or
                # truncated panel at the right edge
                if sid in sm.index and pd.notna(sm.at[sid, "member_end"]):
                    row["delisted"] = True
                    row["entry_date"] = decision
                    row["exit_date"] = decision
                    dr = sm.at[sid, "delisting_return"]
                    if pd.notna(dr):
                        row["fwd_ret"] = float(dr)
                    else:
                        row["dropped"] = True
                else:
                    row["dropped"] = True
                rows.append(row)
                continue
            row["entry_date"] = dates[entry_pos]
            entry_tr = tr_vals[entry_pos]
            if exit_pos < n:
                row["exit_date"] = dates[exit_pos]
                row["fwd_ret"] = float(tr_vals[exit_pos] / entry_tr - 1.0)
            else:
                # ran off the right edge while holding: close at last price
                # or at the delisting return if one exists
                if sid in sm.index and pd.notna(sm.at[sid, "member_end"]):
                    row["delisted"] = True
                    row["exit_date"] = dates[n - 1]
                    dr = sm.at[sid, "delisting_return"]
                    if pd.notna(dr):
                        held = float(tr_vals[n - 1] / entry_tr - 1.0)
                        row["fwd_ret"] = held + float(dr)
                    else:
                        row["dropped"] = True
                else:
                    row["dropped"] = True
            rows.append(row)
    return pd.DataFrame(rows)
