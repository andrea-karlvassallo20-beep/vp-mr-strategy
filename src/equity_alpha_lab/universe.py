"""Point-in-time universe membership.

universe_asof returns the securities that were members of the research
universe on a given date, using the membership INTERVALS in the security
master — not a current constituent list. A security that delisted before
`asof` is not a member; a security that joined after `asof` is not a member.

survivorship_audit quantifies the bias a current-list snapshot would have
introduced: how many members on `asof` are no longer alive at the audit
date, and how many ever-members exited before `asof`.
"""

from __future__ import annotations

import pandas as pd


def universe_asof(security_master: pd.DataFrame, asof: pd.Timestamp) -> pd.DataFrame:
    """Return security_master rows active on `asof` (half-open [start, end))."""
    asof = pd.Timestamp(asof).normalize()
    sm = security_master
    active = sm["member_start"] <= asof
    ended = sm["member_end"].notna() & (sm["member_end"] <= asof)
    out = sm[active & ~ended].copy()
    return out


def survivorship_audit(
    security_master: pd.DataFrame,
    asof: pd.Timestamp,
    audit_date: pd.Timestamp | None = None,
) -> dict:
    """Quantify survivorship characteristics of the master.

    Returns a dict with:
    - members_asof: members active on `asof`.
    - exited_before_asof: ever-members whose interval ended before `asof`
      (these are the names a current-ticker snapshot silently drops).
    - exited_between: members active on `asof` that exited by `audit_date`
      (bias of evaluating `asof` members with today's list).
    """
    asof = pd.Timestamp(asof).normalize()
    audit = pd.Timestamp(audit_date).normalize() if audit_date is not None else None
    sm = security_master
    members = universe_asof(sm, asof)
    exited_before = sm[sm["member_end"].notna() & (sm["member_end"] <= asof)]
    out = {
        "asof": asof,
        "members_asof": len(members),
        "exited_before_asof": len(exited_before),
    }
    if audit is not None and audit > asof:
        still = members["member_end"].isna() | (members["member_end"] > audit)
        out["audit_date"] = audit
        out["exited_between"] = int((~still).sum())
    return out
