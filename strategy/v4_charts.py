"""THE V4 CHART PAGES: AVFI v4 top/bottom marking across the
whole universe, and the portfolio equity curve of the
philosopher's long rule.

Two outputs:

  docs/v4_charts.html - every series in the extended universe
  (15 indexes, 29 commodity futures, 156 crypto; the ones with
  enough bars) rendered as a compact SVG chart: the price line,
  the AVFI v4 CONFIRMED bottoms (green up-markers: deep stretch
  z <= -2 with bull-side confirmation within 3 bars) and tops
  (red down-markers: z >= +2, bear-side), plus the causal
  stretch-z sparkline beneath. The points of significant change,
  marked, per market.

  paper/research/v4_charts.json - the portfolio equity curve of
  the crash-zone long rule on the anchored set: equal-weight
  concurrent positions (capped), 4-week holds, 5 bps costs both
  sides, the honest daily-grain simulation - plus the equity
  stats (total return, max drawdown, n trades) the front page
  renders.

Usage (nightly, after tops_bottoms_backtest):
    python3 v4_charts.py --data-dir ../paper/research/data \\
        --research-dir ../paper/research --docs-dir ../docs
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent))
from market_philosopher import ANCHORED, HOLD_WEEKS, WEEK, \
    ZONE_HI, ZONE_LO, COST_BPS
from smh_proof import _series
from tops_bottoms_backtest import NEW_INDEXES, _class_of, \
    detect_events
from v4_study import causal_z

N_POINTS = 160          # downsampled points per chart
MAX_CONCURRENT = 10
MIN_BARS = 400


def _downsample(n, target=N_POINTS):
    if n <= target:
        return np.arange(n)
    step = n // target
    idx = np.arange(0, n - 1, step)
    return np.append(idx, n - 1)


def _series_svg(name, c, z, bottoms, tops, cls):
    """One compact SVG: price line + v4 markers + z sparkline."""
    n = len(c)
    keep = _downsample(n)
    kset = set(keep.tolist())
    lo, hi = float(np.min(c)), float(np.max(c))
    rng_ = hi - lo if hi > lo else 1.0
    W, H, HZ = 300, 90, 26
    pts = " ".join(
        f"{i * W / max(1, len(keep) - 1):.1f},"
        f"{H - (float(c[k]) - lo) / rng_ * (H - 8) - 4:.1f}"
        for i, k in enumerate(keep))
    zl, zh = float(np.min(z[keep])), float(np.max(z[keep]))
    zr = zh - zl if zh > zl else 1.0
    zpts = " ".join(
        f"{i * W / max(1, len(keep) - 1):.1f},"
        f"{HZ - (float(z[k]) - zl) / zr * (HZ - 6) - 3:.1f}"
        for i, k in enumerate(keep))

    def marker(t, up):
        if t not in kset:
            # snap to the nearest kept point
            i = int(np.argmin(np.abs(keep - t)))
            k = int(keep[i])
        else:
            k = t
        x = list(keep).index(k) * W / max(1, len(keep) - 1)
        y = H - (float(c[k]) - lo) / rng_ * (H - 8) - 4
        col = "#4ade80" if up else "#f87171"
        tri = (f'{x - 4:.1f},{y + 7:.1f} '
               f'{x + 4:.1f},{y + 7:.1f} {x:.1f},{y - 2:.1f}'
               if up else
               f'{x - 4:.1f},{y - 7:.1f} '
               f'{x + 4:.1f},{y - 7:.1f} {x:.1f},{y + 2:.1f}')
        return (f'<polygon points="{tri}" fill="{col}" '
                f'opacity="0.9"/>')

    marks = "".join(marker(t, True) for t in bottoms
                    if 0 <= t < n) \
        + "".join(marker(t, False) for t in tops if 0 <= t < n)
    return (f'<div class="chart"><div class="ch">'
            f'<span class="ct">{name}</span>'
            f'<span class="cc">{cls}</span></div>'
            f'<svg viewBox="0 0 {W} {H + HZ}" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<polyline points="{pts}" fill="none" '
            f'stroke="#8fa0b5" stroke-width="1.2"/>{marks}'
            f'<polyline points="{zpts}" fill="none" '
            f'stroke="#22d3ee" stroke-width="0.8" '
            f'opacity="0.55" transform="translate(0,{H})"/>'
            f'</svg></div>')


def build_charts(data_dir: Path) -> tuple:
    """All series charts (HTML fragment) + the per-class counts."""
    frags = []
    counts = {}
    for name, c, v in _series(data_dir):
        if len(c) < MIN_BARS:
            continue
        z = causal_z(c)
        b, t_, ub, ut = detect_events(c, v)
        cls = _class_of(name)
        counts[cls] = counts.get(cls, 0) + 1
        frags.append(_series_svg(name, c, z, b, t_, cls))
    return frags, counts


def portfolio_equity(data_dir: Path) -> dict:
    """The crash-zone long portfolio on the anchored set, on a
    CALENDAR-DATE grid (assets have different histories - bar
    indices would mix timelines). Entries at the zone cross,
    4-week holds, equal-weight concurrent positions capped at
    MAX_CONCURRENT, 5 bps costs both sides."""
    from papertrading_runner import load_bars
    from pathlib import Path as _P
    positions = []          # (start_date, end_date, per-date rets)
    per_asset = {}
    for f in sorted((_P(data_dir)).glob("*.csv")):
        name = f.stem.upper()
        if name not in ANCHORED:
            continue
        bars = load_bars(f)
        if len(bars) < MIN_BARS:
            continue
        c = np.array([b["close"] for b in bars], dtype=float)
        dates = [b["date"] for b in bars]
        logc = np.log(c)
        n = len(logc)
        last_entry = -10 ** 9
        for t in range(60, n - WEEK * HOLD_WEEKS):
            if t < WEEK:
                continue
            wr = float(logc[t] - logc[t - WEEK])
            prev = float(logc[t - 1] - logc[t - 1 - WEEK])
            if (ZONE_LO <= wr < ZONE_HI
                    and not ZONE_LO <= prev < ZONE_HI
                    and t >= last_entry + WEEK * HOLD_WEEKS):
                last_entry = t
                daily = np.diff(
                    logc[t:t + WEEK * HOLD_WEEKS + 1])
                per_date = {
                    dates[t + 1 + j]: float(daily[j])
                    for j in range(len(daily))}
                positions.append((dates[t],
                                  dates[t + WEEK * HOLD_WEEKS],
                                  per_date, name))
                a = per_asset.setdefault(name, {
                    "n": 0, "fwd": []})
                a["n"] += 1
                a["fwd"].append(float(
                    logc[t + WEEK * HOLD_WEEKS] - logc[t]))
    if not positions:
        return {"status": "NO_TRADES"}
    positions.sort(key=lambda p: p[0])
    all_dates = sorted({d for p in positions
                        for d in p[2]})
    eq = 1.0
    curve = []
    max_dd = 0.0
    peak = 1.0
    cost = 2 * COST_BPS / 1e4 / (WEEK * HOLD_WEEKS)
    for d in all_dates:
        # dated correction (12 Nov 2026, doctrine rule 6):
        # the pool is rebuilt from positions whose window
        # COVERS the date, capped by entry order - the old
        # code silently dropped positions whose entry date was
        # not covered by another position's window (caught by
        # the cap-sensitivity suite; both simulators fixed;
        # numbers re-measured and re-recorded)
        active = [p for p in positions if p[0] <= d < p[1]]
        open_pool = active[:MAX_CONCURRENT]
        rets = [p[2][d] for p in open_pool if d in p[2]]
        r = (float(np.mean(rets)) - cost) if rets else 0.0
        eq *= np.exp(r)
        peak = max(peak, eq)
        max_dd = max(max_dd, (peak - eq) / peak)
        curve.append(round(float(eq), 4))
    # monthly sampling for the rendered curve
    monthly = curve[::21] if len(curve) > 42 else curve
    years = len(all_dates) / 252.0
    cagr = (eq ** (1 / years) - 1) if years > 0 and eq > 0 \
        else None
    breakdown = {
        nm: {
            "n_trades": a["n"],
            "median_fwd": round(float(np.median(a["fwd"])), 4),
            "positive": bool(np.median(a["fwd"]) > 0),
        } for nm, a in sorted(per_asset.items())}
    return {
        "status": "OK",
        "n_trades": len(positions),
        "total_return": round(float(eq - 1.0), 4),
        "cagr": round(float(cagr), 4) if cagr is not None
        else None,
        "max_drawdown": round(float(max_dd), 4),
        "years": round(years, 2),
        "equity_curve_monthly": monthly,
        "concurrent_cap": MAX_CONCURRENT,
        "per_asset": breakdown,
        "note": "equal-weight concurrent positions on a "
                "calendar-date grid, 4-week holds, 5 bps costs "
                "both sides; the honest simulation of the "
                "philosopher's long rule on the anchored set - "
                "design sample, forward-scored or it stays "
                "flagged. The per-asset breakdown is the honest "
                "part the pooled median hides: the edge is "
                "concentrated, and negative cells are flagged",
    }


def run(data_dir: Path, research_dir: Path,
        docs_dir: Path) -> dict:
    frags, counts = build_charts(data_dir)
    eq = portfolio_equity(data_dir)
    css = """
<style>
.v4wrap { max-width:1280px; margin:0 auto; padding:24px 48px;
  color:#e8eef7; font-family:-apple-system,'Segoe UI',sans-serif;
  background:#070b12; }
.v4wrap h1 { font-size:28px; letter-spacing:-.02em; }
.v4wrap p { color:#8fa0b5; max-width:760px; line-height:1.6; }
.grid { display:grid; grid-template-columns:repeat(4,1fr);
  gap:14px; margin-top:18px; }
.chart { background:#0d1420; border:1px solid #1c2637;
  border-radius:10px; padding:8px 10px; }
.chart svg { width:100%; height:auto; display:block; }
.ch { display:flex; justify-content:space-between;
  font-size:11px; margin-bottom:4px; }
.ct { font-weight:700; }
.cc { color:#5c6b80; }
.eq { color:#8fa0b5; font-size:13px; margin-top:10px;
  line-height:1.7; }
.eq strong { color:#e8eef7; }
@media (max-width:900px){ .grid { grid-template-columns:1fr; } }
</style>"""
    body = (f'<div class="v4wrap"><h1>Salient &mdash; the '
            f'universe, marked</h1>'
            f'<p>AVFI v4 detection on every market with enough '
            f'history: green marks CONFIRMED bottoms (deep '
            f'stretch z &le; &minus;2 with bull-side '
            f'confirmation within 3 bars), red marks CONFIRMED '
            f'tops (z &ge; +2, bear-side); the cyan sparkline '
            f'is the causal stretch-z. '
            f'{sum(counts.values())} charts across '
            f'{", ".join(f"{k}: {v}" for k, v in counts.items())}'
            f'.</p>')
    if eq.get("status") == "OK":
        body += (f'<p class="eq">The philosopher&rsquo;s long '
                 f'rule on the anchored set, simulated: '
                 f'<strong>{eq["n_trades"]} trades over '
                 f'{eq["years"]} years</strong>, total return '
                 f'<strong>{eq["total_return"] * 100:.1f}%'
                 f'</strong>' 
                 + (f' (CAGR {eq["cagr"] * 100:.1f}%)'
                    if eq.get("cagr") is not None else "")
                 + f', max drawdown '
                 f'<strong>{eq["max_drawdown"] * 100:.1f}%'
                 f'</strong>, concurrent cap '
                 f'{eq["concurrent_cap"]}. Design sample - '
                 f'forward-scored or it stays flagged.</p>')
        pts = eq["equity_curve_monthly"]
        n = len(pts)
        lo, hi = min(pts), max(pts)
        rng_ = (hi - lo) if hi > lo else 1.0
        W, H = 900, 160
        poly = " ".join(
            f"{i * W / max(1, n - 1):.1f},"
            f"{H - (p - lo) / rng_ * (H - 20) - 10:.1f}"
            for i, p in enumerate(pts))
        body += (f'<svg viewBox="0 0 {W} {H}" '
                 f'xmlns="http://www.w3.org/2000/svg" '
                 f'style="background:#0d1420;border-radius:10px">'
                 f'<polyline points="{poly}" fill="none" '
                 f'stroke="#22d3ee" stroke-width="1.6"/></svg>')
    body += ('<div class="grid">' + "".join(frags)
             + '</div></div>')
    html = ("<!DOCTYPE html><html lang=\"en\"><head>"
            "<meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-"
            "width, initial-scale=1\">"
            "<title>Salient — the universe, marked</title>"
            + css + "</head><body>" + body + "</body></html>")
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "v4_charts.html").write_text(html)

    result = {
        "status": "OK",
        "generated_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "n_charts": len(frags),
        "per_class": counts,
        "equity": eq,
        "page": "docs/v4_charts.html",
    }
    dest = research_dir / "v4_charts.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2))

    frags_dest = research_dir / "v4_chart_frags.json"
    frags_dest.write_text(json.dumps({
        "status": "OK",
        "generated_utc": result["generated_utc"],
        "n_charts": len(frags),
        "per_class": counts,
        "charts": frags,
    }))
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="V4 chart pages + portfolio equity")
    ap.add_argument("--data-dir", type=Path,
                    default=Path("../paper/research/data"))
    ap.add_argument("--research-dir", type=Path,
                    default=Path("../paper/research"))
    ap.add_argument("--docs-dir", type=Path,
                    default=Path("../docs"))
    args = ap.parse_args()
    r = run(args.data_dir, args.research_dir, args.docs_dir)
    eq = r["equity"]
    print(f"v4 charts -> {r['page']} ({r['n_charts']} charts; "
          f"equity: {eq.get('n_trades')} trades, total "
          f"{eq.get('total_return')}, maxDD "
          f"{eq.get('max_drawdown')})")


if __name__ == "__main__":
    main()
