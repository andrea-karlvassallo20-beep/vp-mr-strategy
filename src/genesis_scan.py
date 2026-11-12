"""Genesis scan — the earliest charts of the TVC USD pairs.

Directive (Andrea, Nov 2026): the START affects the future. Look at the
earliest charts of the USD pairs — those who knew the WHAT were there from
the start, and the start may hold the clue.

Honest data boundary: all panel CSVs share a common export window starting
2021-11-12, so pairs that existed before it have no true listing-era data
here. Pairs whose first bar falls AFTER the window start do have their real
earliest charts — those are the genesis set. DESRIPTIVE ONLY: no claim is
tested; the null used for comparison (a random 90-day window contains the
all-time extreme with probability ~ window/history) is stated, not fitted.

Genesis metrics (per launched pair):
  genesis window = first 90 days of available history
  ath_in_genesis / atl_in_genesis : does the all-time high / low of the
      whole available history still sit inside the first 90 days?
  genesis_ret : return over the first 90 days
  now_vs_genesis : current close's position within the genesis range
"""

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("paper/research/data")
WINDOW_START = pd.Timestamp("2021-11-12")
GENESIS_DAYS = 90


def scan():
    rows = []
    for f in sorted(DATA.glob("*.csv")):
        name = f.stem
        if not (name.endswith("usd") or name.endswith("usdt")):
            continue
        df = pd.read_csv(f).dropna(subset=["close"]).reset_index(drop=True)
        if len(df) < 200:
            continue
        first = pd.Timestamp(df["date"].iloc[0])
        if first <= WINDOW_START + pd.Timedelta(days=45):
            continue  # no true listing-era data; shared window start
        close = df["close"].to_numpy(float)
        g = close[:GENESIS_DAYS]
        ath = close.max()
        atl = close.min()
        rows.append({
            "pair": name,
            "first_bar": str(first.date()),
            "n_days": len(close),
            "genesis_ret": round(float(g[-1] / g[0] - 1.0), 3),
            "ath_in_genesis": bool(g.max() >= ath * 0.999),
            "atl_in_genesis": bool(g.min() <= atl * 1.001),
            "now_vs_genesis": round(
                float((close[-1] - g.min()) / max(g.max() - g.min(), 1e-9)), 3),
            "ath_vs_now": round(float(close[-1] / ath), 3),
        })
    out = pd.DataFrame(rows).sort_values("first_bar").reset_index(drop=True)
    n = len(out)
    ath_rate = float(out["ath_in_genesis"].mean()) if n else float("nan")
    atl_rate = float(out["atl_in_genesis"].mean()) if n else float("nan")
    # null: probability a random 90-day window contains the extreme
    nulls = [GENESIS_DAYS / r["n_days"] for _, r in out.iterrows()]
    print(f"genesis set: {n} pairs with true launch-era data")
    print(f"ATH still in the first {GENESIS_DAYS} days: {ath_rate:.1%} "
          f"(random-window null: {np.mean(nulls):.1%})")
    print(f"ATL still in the first {GENESIS_DAYS} days: {atl_rate:.1%}")
    print(out.to_string(index=False))
    out.to_csv(Path("paper/research/clue_scan") / "genesis_scan.csv", index=False)
    return out


if __name__ == "__main__":
    scan()
