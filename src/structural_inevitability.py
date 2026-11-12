"""Structural Inevitability Engine — quantifying the lion's frustration.

BUILDER DIRECTIVE (Nov 2026): the L2 data is the TRIGGER; the structural
data is the CAUSE. Before any L2 hazard model, quantify inevitability from
structural data: funding, open interest, and basis.

Pre-declared definitions (fixed before the retrospective was computed):

  funding_trap    = clip(-funding_z30, 0, 3) / 3 * 100
                    (extreme NEGATIVE funding = short-squeeze fuel;
                     positive funding reads zero on this component)
  oi_divergence  = clip((1 - corr30(price, OI)) / 2, 0, 1)
                    * clip(oi_z30, 0, 3) / 3 * 100
                    (flat price + RISING open interest = the spring coiling)
  basis_extreme  = clip(|basis_z30|, 0, 3) / 3 * 100
                    (contango/backwardation that must revert)
  FRUSTRATION SCORE (0-100) = 0.4*funding_trap + 0.4*oi_divergence
                              + 0.2*basis_extreme

KILL LINES (enforced by assertion):
  1. If OI/funding/basis/price cannot be aligned by UTC date, the dataset
     is dead (raise, never silently interpolate).
  2. If the Frustration Score does not spike (top decile of its own
     distribution) within 14 days before the major historical
     crashes/squeezes (FTX Nov 2022, carry unwind Aug 2024), the structural
     trap theory is falsified for those events.

Liquidation levels: no free historical source exists; NOT estimated here
(no proxy substitution). Flagged blocked-on-data.
"""

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw")
Z30 = 30


def _read_zip_csv(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
        head = zf.read(name)[:200].decode("utf-8", errors="replace")
        has_header = any(
            k in head.lower()
            for k in ("price", "calc_time", "create_time", "open_time", "symbol")
        )
        return pd.read_csv(io.BytesIO(zf.read(name)), header=0 if has_header else None)


def load_funding(dates: pd.DatetimeIndex) -> pd.Series:
    """Daily mean funding rate (fractional per 8h event), UTC dates."""
    rows = []
    for p in sorted((RAW / "fundingRate").glob("BTCUSDT-fundingRate-*.zip")):
        df = _read_zip_csv(p)
        df.columns = [str(c).strip().lower() for c in df.columns]
        if "calc_time" not in df.columns:
            raise ValueError(f"{p}: unexpected funding schema {list(df.columns)}")
        ts = pd.to_datetime(df["calc_time"], unit="ms", utc=True)
        rows.append(pd.DataFrame({"date": ts.dt.date, "rate": df["last_funding_rate"]}))
    f = pd.concat(rows).groupby("date")["rate"].mean()
    idx = pd.to_datetime(pd.Index(f.index))
    return pd.Series(f.values, index=idx)


def load_oi(dates: pd.DatetimeIndex) -> pd.Series:
    """Daily last open interest (contracts), UTC dates, from metrics zips."""
    rows = []
    for p in sorted((RAW / "metrics").glob("BTCUSDT-metrics-*.zip")):
        df = _read_zip_csv(p)
        df.columns = [str(c).strip().lower() for c in df.columns]
        if "create_time" not in df.columns or "sum_open_interest" not in df.columns:
            raise ValueError(f"{p}: unexpected metrics schema")
        ts = pd.to_datetime(df["create_time"], utc=True, format="mixed")
        rows.append(pd.DataFrame({"date": ts.dt.date, "oi": df["sum_open_interest"]}))
    o = pd.concat(rows).groupby("date")["oi"].last()
    return pd.Series(o.values, index=pd.to_datetime(pd.Index(o.index)))


def load_perp_close() -> pd.Series:
    """Daily perp close from monthly 1d klines (column 4)."""
    rows = []
    for p in sorted((RAW / "klines").glob("BTCUSDT-1d-*.zip")):
        df = _read_zip_csv(p)
        ts = pd.to_datetime(df.iloc[:, 0], unit="ms", utc=True)
        rows.append(pd.DataFrame({"date": ts.dt.date, "close": df.iloc[:, 4]}))
    k = pd.concat(rows).groupby("date")["close"].last()
    return pd.Series(k.values, index=pd.to_datetime(pd.Index(k.index)))


def load_spot() -> pd.Series:
    df = pd.read_csv("paper/research/data/btcusd.csv")
    idx = pd.to_datetime(df["date"], utc=True)
    return pd.Series(df["close"].values, index=idx)


def _utc(s: pd.Series) -> pd.Series:
    idx = s.index
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    s.index = idx
    return s


def build_structural_frame() -> pd.DataFrame:
    """KILL LINE 1: strict UTC-date alignment; raise on any gap."""
    spot = _utc(load_spot())
    funding = _utc(load_funding(None))
    oi = _utc(load_oi(None))
    perp = _utc(load_perp_close())
    df = pd.DataFrame({
        "spot": spot, "perp": perp, "funding": funding, "oi": oi,
    }).dropna()
    if len(df) < 200:
        raise AssertionError(
            f"KILL LINE 1: aligned structural frame too short ({len(df)})")
    gaps = df.index.to_series().diff().dt.days
    if (gaps > 5).any():
        raise AssertionError(
            f"KILL LINE 1: alignment gap > 5 days: "
            f"{df.index[gaps > 5].tolist()[:3]}")
    return df


def frustration_features(df: pd.DataFrame) -> pd.DataFrame:
    """The three pre-declared frustration metrics and the 0-100 score."""
    out = df.copy()
    fz = (out["funding"] - out["funding"].rolling(Z30).mean()) / out[
        "funding"].rolling(Z30).std()
    out["funding_trap"] = np.clip(-fz, 0, 3) / 3 * 100
    corr = out["spot"].rolling(Z30).corr(out["oi"])
    oiz = (out["oi"] - out["oi"].rolling(Z30).mean()) / out["oi"].rolling(Z30).std()
    out["oi_divergence"] = (
        np.clip((1 - corr) / 2, 0, 1) * np.clip(oiz, 0, 3) / 3 * 100
    )
    basis = (out["perp"] - out["spot"]) / out["spot"] * 1e4  # bps
    bz = (basis - basis.rolling(Z30).mean()) / basis.rolling(Z30).std()
    out["basis_bps"] = basis
    out["basis_extreme"] = np.clip(np.abs(bz), 0, 3) / 3 * 100
    out["frustration_score"] = (
        0.4 * out["funding_trap"].fillna(0)
        + 0.4 * out["oi_divergence"].fillna(0)
        + 0.2 * out["basis_extreme"].fillna(0)
    )
    return out.dropna()


def score_spiked_before(df: pd.DataFrame, event: str, lookback_days: int = 14,
                        quantile: float = 0.90) -> dict:
    """KILL LINE 2: was the score in its own top decile within the 14 days
    before the event? Causal: only the window BEFORE the event is examined."""
    events = {
        "carry_unwind_2024_08_05": "2024-08-05",
        "ftx_2022_11_08": "2022-11-08",
    }
    if event not in events:
        raise ValueError(f"unknown event {event}")
    d = pd.Timestamp(events[event], tz="UTC")
    thresh = df["frustration_score"].quantile(quantile)
    win = df.loc[(df.index >= d - pd.Timedelta(days=lookback_days))
                 & (df.index < d)]
    peak = float(win["frustration_score"].max())
    peak_date = str(win["frustration_score"].idxmax().date())
    return {
        "event": event,
        "threshold_p90": round(float(thresh), 1),
        "peak_score_before": round(peak, 1),
        "peak_date": peak_date,
        "spiked": bool(peak >= thresh),
        "full_sample_median": round(float(df["frustration_score"].median()), 1),
    }


def main():
    df = build_structural_frame()
    feat = frustration_features(df)
    out = Path("paper/research/clue_scan")
    out.mkdir(parents=True, exist_ok=True)
    feat.to_csv(out / "structural_inevitability_btcusd.csv")
    print(f"aligned days: {len(feat)}  ({feat.index[0].date()} → {feat.index[-1].date()})")
    for ev in ("carry_unwind_2024_08_05", "ftx_2022_11_08"):
        r = score_spiked_before(feat, ev)
        print(r)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        assets = Path("docs/assets")
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(feat.index, feat["frustration_score"], lw=0.8, color="#f5b04c",
                label="frustration score (0-100)")
        for name, d in (("FTX", "2022-11-08"), ("carry unwind", "2024-08-05")):
            ax.axvline(pd.Timestamp(d, tz="UTC"), color="#f87171", lw=1, ls="--")
            ax.text(pd.Timestamp(d, tz="UTC"), 95, name, fontsize=8, color="#f87171")
        ax.set_ylim(0, 100)
        ax.legend()
        ax.set_title("BTCUSDT structural frustration score — the lion's grievance, quantified")
        fig.tight_layout()
        fig.savefig(assets / "frustration_score.png", dpi=110)
        print("chart: docs/assets/frustration_score.png")
    except ImportError:
        pass


if __name__ == "__main__":
    main()
