"""Point-in-time snapshots of fundamentals and the leakage tripwire.

pit_fundamentals(asof) returns, for each (sid, field), the value from the
record with the LATEST announce_date <= asof. This is the only legal way a
fundamental enters a feature. A record announced exactly on `asof` is
included (public at the close of the announcement day is a declared
convention — documented, not hidden).

assert_no_future_information is the tripwire: given a snapshot and the raw
frame it came from, it fails if any value in the snapshot could only be
explained by a record announced after the as-of date.
"""

from __future__ import annotations

import pandas as pd


def pit_fundamentals(
    fundamentals: pd.DataFrame,
    asof: pd.Timestamp,
    max_lag_days: int | None = None,
) -> pd.DataFrame:
    """Latest announced value per (sid, field) as of `asof`.

    max_lag_days, if set, drops records whose announce_date is more than
    max_lag_days after period_end (stale-but-unusable or error rows).
    """
    asof = pd.Timestamp(asof).normalize()
    fd = fundamentals
    if not fd["announce_date"].dtype.kind in "M":
        raise TypeError("announce_date must be datetime64")
    usable = fd[fd["announce_date"] <= asof]
    if max_lag_days is not None:
        lag = (fd["announce_date"] - fd["period_end"]).dt.days
        usable = usable.loc[usable.index.intersection(fd.index[lag <= max_lag_days])]
    if usable.empty:
        return usable.assign(asof=asof).iloc[0:0]
    idx = usable.groupby(["sid", "field"])["announce_date"].idxmax()
    snap = usable.loc[idx].copy()
    snap["asof"] = asof
    return snap.reset_index(drop=True)


def assert_no_future_information(
    snapshot: pd.DataFrame,
    fundamentals: pd.DataFrame,
    asof: pd.Timestamp,
    tol: float = 1e-12,
) -> None:
    """Fail if snapshot values cannot be reproduced from announced records.

    For each (sid, field) in the snapshot, the snapshot value must equal the
    value of the latest record with announce_date <= asof. If it instead
    matches a record announced LATER, the snapshot was built with lookahead
    and this raises LeakageError.
    """
    from .quality import LeakageError

    asof = pd.Timestamp(asof).normalize()
    legal = pit_fundamentals(fundamentals, asof)
    keys = ["sid", "field"]
    merged = snapshot.merge(
        legal, on=keys, how="left", suffixes=("", "_legal")
    )
    bad_value = merged["value"].notna() & (
        (merged["value_legal"].isna())
        | ((merged["value"] - merged["value_legal"]).abs() > tol)
    )
    if bad_value.any():
        offenders = merged.loc[bad_value, keys + ["value", "value_legal"]]
        raise LeakageError(
            f"snapshot contains values not reproducible from information "
            f"available at {asof.date()}; {len(offenders)} offending rows, "
            f"first: {offenders.iloc[0].to_dict()}"
        )
    future = fundamentals.merge(snapshot[keys].drop_duplicates(), on=keys)
    future = future[future["announce_date"] > asof]
    if len(future):
        latest_legal = legal.set_index(keys)["value"]
        collided = snapshot.set_index(keys)["value"]
        for key, row in future.iterrows():
            if key in collided.index and latest_legal.get(key) != collided.loc[key]:
                raise LeakageError(
                    f"snapshot value for {key} matches a record announced "
                    f"{row['announce_date'].date()}, after as-of {asof.date()}"
                )
