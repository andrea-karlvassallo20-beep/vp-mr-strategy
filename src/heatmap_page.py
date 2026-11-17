"""The heat map page — the board as a market treemap.

Directive (Andrea, Nov 2026): the page should LOOK like the market
heat maps posted on Reddit/X — the finviz-style treemap: every series a
tile, tile AREA sized by how big the market is, tile COLOR the day's
move (the sea-of-green melt-up, the wall-of-red crash). The priming
research rides along on every tile (hover), but the first read is the
picture: green or red, big or small.

Design (honest and fixed):
  - AREA: trailing 60-day average daily dollar volume (close x volume)
    — one consistent liquidity weight computable for every class from
    the same cached klines. Series with no volume on Yahoo (FX, some
    indexes) get the class-median weight, never zero: they stay
    visible, and the substitution is stated in the legend, not hidden.
  - COLOR: last daily % change. Green up, red down, intensity by
    |change| capped at 5% (the finviz convention): 0% = neutral gray.
  - LAYOUT: the squarified treemap (Bruls, Huizing & van Wijk) per
    class — one map per section, exactly like the posted maps that are
    one map per universe.
  - HOVER: every tile carries the priming state (dormancy score,
    primed flag, coil days) — the research is the tooltip; the picture
    is the move.

The board source is the living board (mega_dormancy_table.csv), falling
back to board_table.csv. Sections are data-driven: every class present
gets a map; no class is silently dropped.

DESCRIPTIVE ONLY. The color is the past day's move — it is a picture of
what already happened, not a prediction; the priming score ranks
candidates and tests nothing. WHICH WAY is refused by measurement.
C7 stays sealed.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import surprise_ledger as sl  # noqa: E402

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import render as _render_nav

CLUE = Path("paper/research/clue_scan")
MEGA_CSV = CLUE / "mega_dormancy_table.csv"
BOARD_CSV = CLUE / "board_table.csv"
PAGE = Path("docs/heatmap.html")

MAP_W = 1000
CAP_PCT = 5.0

CLASS_TITLES = {
    "commodity": "Commodities",
    "index": "Indexes",
    "world_index": "World indexes",
    "rate": "Rates",
    "fx": "FX",
    "equity": "Large-cap equities",
    "global_equity": "Global mega-caps (non-US)",
    "sp500": "S&P 500",
    "sp400": "S&P 400 (mid caps)",
    "sp600": "S&P 600 (small caps)",
    "etf": "ETFs",
    "crypto": "Crypto (every Binance USDT market)",
}

CLASS_ORDER = ["commodity", "index", "world_index", "rate", "fx",
               "equity", "global_equity", "sp500", "sp400", "sp600",
               "etf", "crypto"]

NAV = _render_nav("heatmap.html")


def load_board(mega_csv=MEGA_CSV, board_csv=BOARD_CSV):
    """The living board, normalized (same contract as before)."""
    if Path(mega_csv).exists():
        df = pd.read_csv(mega_csv)
        score = df["dormancy_score"].astype(float)
        span = float(score.max()) or 1.0
        out = pd.DataFrame({
            "series": df["series"], "class": df["class"],
            "venue": df.get("venue", ""),
            "score": score / span,
            "comp_days": df["comp_days"], "rvol_pct": df["rvol_pct"],
            "eligible": df["primed"].astype(bool),
            "source": "mega_dormancy_table.csv",
        })
    elif Path(board_csv).exists():
        df = pd.read_csv(board_csv)
        out = pd.DataFrame({
            "series": df["series"], "class": df["class"],
            "venue": df.get("venue", ""),
            "score": df["primed_score"].astype(float),
            "comp_days": df["comp_days"], "rvol_pct": df["rvol_pct"],
            "eligible": df["eligible"].astype(bool),
            "source": "board_table.csv",
        })
    else:
        raise SystemExit("no board found - run the board refresh first")
    return out


def _day_stats(data_file):
    """(daily % change, trailing 60d avg dollar volume) from cached
    klines, or (None, None)."""
    if not data_file:
        return None, None
    try:
        df = pd.read_csv(data_file)
    except Exception:
        return None, None
    if "close" not in df.columns or len(df) < 2:
        return None, None
    close = df["close"].to_numpy(float)
    ret1 = close[-1] / close[-2] - 1.0
    vol = (df["volume"].to_numpy(float)
           if "volume" in df.columns else np.zeros(len(df)))
    dvol = close * vol
    tail = dvol[-60:]
    w = float(np.mean(tail[tail > 0])) if (tail > 0).any() else 0.0
    return float(ret1), w


def _color(chg):
    """finviz convention: green up, red down, intensity capped at CAP_PCT."""
    if chg is None or not np.isfinite(chg) or chg == 0:
        return "#5c6b80", "#e8eef7"
    c = max(-CAP_PCT, min(CAP_PCT, chg * 100.0)) / CAP_PCT
    if c > 0:
        r, g, b = int(46 + (0 - 46) * c), int(204 + (32 - 204) * c), \
            int(80 + (17 - 80) * c)
    else:
        t = -c
        r, g, b = int(248 - (248 - 183) * 0) , int(113 - (113 - 21) * t), \
            int(113 - (113 - 35) * t)
        r = 248
    return f"rgb({r},{g},{b})", "#070b12"


def _worst_row(rows):
    """The squarify row-split decision (Bruls et al.): worst aspect
    ratio of the candidate row, given the current remainder side."""
    s = sum(r["area"] for r in rows)
    side = rows[0]["side"]
    h = s / side
    return max(max(r["area"] / (h * h), h * h / r["area"]) for r in rows)


def _squarify(items, x, y, w, h):
    """Squarified treemap (Bruls, Huizing & van Wijk, 2000)."""
    rects = []
    items = sorted(items, key=lambda r: -r["area"])
    total = sum(r["area"] for r in items)
    scale = (w * h) / total if total else 1.0
    items = [{"series": r["series"], "area": r["area"] * scale}
             for r in items]
    while items:
        side = min(w, h)
        row = []
        while items:
            cand = row + [dict(items[0], side=side)]
            if not row or _worst_row(cand) <= _worst_row(row):
                row = cand
                items.pop(0)
            else:
                break
        s = sum(r["area"] for r in row)
        if w >= h:
            rw = s / h
            cx, cy, cw, ch = x, y, rw, h
            x += rw
            w -= rw
        else:
            rh = s / w
            cx, cy, cw, ch = x, y, w, rh
            y += rh
            h -= rh
        # place each item in the row
        if cw >= ch:  # row is vertical strip: stack along ch
            off = cy
            for r in row:
                ih = ch * r["area"] / s
                rects.append((r["series"], cx, off, cw, max(ih, 1.0)))
                off += ih
        else:
            off = cx
            for r in row:
                iw = cw * r["area"] / s
                rects.append((r["series"], off, cy, max(iw, 1.0), ch))
                off += iw
    return rects


def _tile_html(series, x, y, w_, h_, chg, weight, row, color, ink):
    pct = "" if chg is None else f"{chg * 100:+.1f}%"
    big = w_ >= 78 and h_ >= 40
    mid = w_ >= 46 and h_ >= 22
    name_font = max(9, min(17, int(w_ / 9)))
    label = f'<span class="tname">{series}</span>'
    if big:
        label = (f'<span class="tname" style="font-size:{name_font}px">'
                 f"{series}</span>"
                 f'<span class="tpct">{pct}</span>'
                 f'<span class="tmeta">{int(row["comp_days"])}d coil</span>')
    elif mid:
        label = (f'<span class="tname" style="font-size:{name_font}px">'
                 f"{series}</span>")
    else:
        label = ""
    border = "box-shadow:inset 0 0 0 1px rgba(7,11,18,.55);"
    dim = "" if row["eligible"] else "opacity:.45;"
    tip = (f'{series} {pct} · dormancy {row["score"]:.2f} · '
           f'{int(row["comp_days"])}d coil · rvol_pct {row["rvol_pct"]:.1f}'
           + (" · PRIMED" if row["eligible"] else ""))
    return (f'<div class="tile" style="left:{x:.1f}px;top:{y:.1f}px;'
            f'width:{w_:.1f}px;height:{h_:.1f}px;'
            f'background:{color};color:{ink};{border}{dim}" '
            f'title="{tip}">{label}</div>')


def _class_map(cls, sub, stats):
    n = len(sub)
    height = max(220, min(980, int(0.95 * n)))
    items = [{"series": r["series"], "area": stats[r["series"]][1]}
             for _, r in sub.iterrows()]
    rects = _squarify(items, 0, 0, MAP_W, height)
    tiles = []
    lookup = {r["series"]: r for _, r in sub.iterrows()}
    for series, x, y, w_, h_ in rects:
        w_ = min(w_, MAP_W - x)
        h_ = min(h_, height - y)
        chg, weight = stats.get(series, (None, None))
        color, ink = _color(chg)
        tiles.append(_tile_html(series, x, y, w_, h_, chg, weight,
                                lookup[series], color, ink))
    up = sum(1 for s in stats if stats[s][0] and stats[s][0] > 0)
    down = sum(1 for s in stats if stats[s][0] and stats[s][0] < 0)
    n_primed = int(sub["eligible"].sum())
    return f"""<section>
<h2>{CLASS_TITLES.get(cls, cls)}<span class="dot">.</span></h2>
<p class="dim">n={n} &middot; up {up} / down {down} &middot; primed
{n_primed} &middot; tile area = trailing 60d dollar volume (no-volume
series: class-median weight) &middot; color = daily change, capped at
&plusmn;{CAP_PCT:.0f}%</p>
<div class="treemap" style="position:relative;width:{MAP_W}px;height:{height}px;max-width:100%">
{"".join(tiles)}
</div>
</section>"""


def _surprise_section(ledger_path):
    records = sl.read_ledger(ledger_path)
    snaps = [r for r in records if r["type"] == sl.SNAPSHOT_RECORD]
    res = [r for r in records if r["type"] == sl.RESOLUTION_RECORD]
    head = (f"<p class=\"dim\">Snapshots sealed: <b>{len(snaps)}</b> &middot; "
            f"resolutions past horizon: <b>{len(res)}</b> &middot; "
            f"ledger: hash-chained, append-only, verify-before-write</p>")
    if not res:
        return (head + "<p>No horizon has passed yet. The priming states on "
                "this page are sealed nightly; reality gets its turn in 10 "
                "bars. Come back and study what surprised.</p>")
    s = sl.study(ledger_path)
    rows = []
    for cls, b in s["per_class"].items():
        rho = b["spearman_rho"]
        rho_s = "n/a" if rho is None else f"{rho:.3f}"
        p_s = "n/a" if b["p_value"] is None else f"{b['p_value']:.3f}"
        top5_s = ("n/a" if b["mean_jump_top5"] is None
                  else f"{b['mean_jump_top5']:.4f}")
        rest_s = ("n/a" if b["mean_jump_rest"] is None
                  else f"{b['mean_jump_rest']:.4f}")
        rows.append(
            f"<tr><td>{cls}</td><td>{b['n']}</td><td>{rho_s} (p={p_s})</td>"
            f"<td>{b['median_jump']:.4f}</td><td>{top5_s}</td>"
            f"<td>{rest_s}</td></tr>")
    surprises = "\n".join(
        f"<tr><td>{r['series']}</td><td>{r['class']}</td>"
        f"<td>{r['primed_score']:.3f}</td>"
        f"<td>{r['realized_jump']:.4f}</td><td>{r['jump_direction']}</td></tr>"
        for r in s["biggest_surprises"])
    o = s["overall"]
    return f"""{head}
<p>Descriptive only: the sealed top-k are extremes by construction, so
the study asks whether the <b>ranking</b> carried information - Spearman
rho between the sealed score and the realized 10-bar max |move| - never
whether one winner proves anything.</p>
<table>
<tr><th>Class</th><th>Resolved</th><th>Spearman rho (score vs jump)</th>
<th>Median jump</th><th>Mean jump, top-5 sealed</th>
<th>Mean jump, rest</th></tr>
{"".join(rows)}
</table>
<h3>The biggest surprises so far</h3>
<table>
<tr><th>Series</th><th>Class</th><th>Sealed score</th>
<th>Realized 10-bar jump</th><th>Direction</th></tr>
{surprises}
</table>
<p class="dim">Whole board: n={o['n']} rho={o['spearman_rho']:.3f}
(p={o['p_value']:.4f}). Full report:
<code>paper/research/clue_scan/surprise_study.md</code></p>"""


def build_page(mega_csv=MEGA_CSV, board_csv=BOARD_CSV,
               ledger_path=sl.LEDGER, page=PAGE):
    board = load_board(mega_csv, board_csv)
    source = board["source"].iloc[0]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # day stats per series (change + dollar-volume weight)
    stats = {}
    for _, r in board.iterrows():
        f = sl._mega_data_file(r["series"], r.get("venue", ""))
        chg, w = _day_stats(f)
        stats[r["series"]] = (chg, w or 0.0)
    # no-volume classes get the class-median weight (stated, not hidden)
    for cls, sub in board.groupby("class"):
        ws = [stats[s][1] for s in sub["series"] if stats[s][1] > 0]
        med = float(np.median(ws)) if ws else 1.0
        for s in sub["series"]:
            if stats[s][1] <= 0:
                stats[s] = (stats[s][0], med)

    n_up = sum(1 for s in stats if stats[s][0] and stats[s][0] > 0)
    n_down = sum(1 for s in stats if stats[s][0] and stats[s][0] < 0)

    sections = []
    present = [c for c in CLASS_ORDER if (board["class"] == c).any()]
    extras = [c for c in board["class"].dropna().unique()
              if c not in CLASS_ORDER]
    for cls in present + extras:
        sub = board[board["class"] == cls]
        if len(sub):
            sections.append(_class_map(cls, sub, stats))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Salient &mdash; The heat map</title>
<meta name="description" content="The heat map: every series on the board colored by days since its last >=4-sigma move, refreshed nightly.">
<link rel="stylesheet" href="site.css">
<style>
.treemap {{ position: relative; max-width: 100%; }}
.tile {{ position: absolute; overflow: hidden; display: flex;
  flex-direction: column; justify-content: center; align-items: center;
  gap: 1px; padding: 2px; text-align: center; }}
.tile .tname {{ font-family: var(--mono); font-weight: 700;
  line-height: 1.1; white-space: nowrap; }}
.tile .tpct {{ font-weight: 700; font-size: 12px; }}
.tile .tmeta {{ font-size: 9px; opacity: .75; }}
.legend {{ display: flex; gap: 0; border-radius: 6px; overflow: hidden;
  height: 12px; max-width: 420px; }}
.legend i {{ flex: 1; }}
</style>
</head>
<body>
{NAV}
<main>

<div class="kicker">Everything on one board &middot; the day&rsquo;s
move, tile by tile</div>
<h1>The heat map<span class="dot">.</span></h1>

<div class="epigraph">
The market heat map, Reddit-style: every series a tile, area by
liquidity, color by the day&rsquo;s move &mdash; the sea of green on
melt-up days, the wall of red on crash days. Zoom out and you see the
whole market breathe. Hover any tile for its priming state: the
research rides the tooltip; the picture is the move.
</div>

<p><span class="big">Descriptive only.</span> The color is yesterday&rsquo;s
move &mdash; a picture of what already happened, never a prediction.
The priming score (on hover) ranks candidates; it tests nothing, and
WHICH WAY is refused by measurement. The multiplicity warning binds on
a ~1,300-series board. The only path from this page to knowledge is
C7&rsquo;s kill lines.</p>

<div class="grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0">
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Series on the board</div><div style="font-size:22px;font-weight:700">{len(board)}</div></div>
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Up / down today</div><div style="font-size:22px;font-weight:700"><span style="color:var(--good)">{n_up}</span> / <span style="color:var(--bad)">{n_down}</span></div></div>
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Primed candidates</div><div style="font-size:22px;font-weight:700">{int(board["eligible"].sum())}</div></div>
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Board built</div><div style="font-size:22px;font-weight:700">{now}</div></div>
</div>

<div class="legend" aria-hidden="true">
<i style="background:rgb(183,21,35)"></i><i style="background:rgb(216,70,74)"></i><i style="background:rgb(248,113,113)"></i><i style="background:#5c6b80"></i><i style="background:rgb(46,204,80)"></i><i style="background:rgb(32,158,62)"></i><i style="background:rgb(0,32,17)"></i>
</div>
<p class="dim" style="margin-top:4px">&minus;5% &rarr; 0 &rarr; +5%
(daily change, capped) &middot; dimmed tiles: not primed &middot; board
source: <code>{source}</code></p>

{"".join(sections)}

<section>
<h2>The surprise ledger &mdash; what jumped, vs what we sealed<span class="dot">.</span></h2>
{_surprise_section(ledger_path)}
</section>

</main>
<footer style="font-size:12px;color:var(--faint);padding:0 32px 32px">
Generated by src/heatmap_page.py from {source}
and logs/board_surprise_ledger.jsonl, regenerated by the nightly
src/board_refresh.py cycle. Descriptive only - candidates, not claims;
C7 stays sealed.
</footer>
</body>
</html>
"""
    Path(page).parent.mkdir(parents=True, exist_ok=True)
    Path(page).write_text(html)
    return {"page": str(page), "n_series": len(board),
            "n_up": n_up, "n_down": n_down,
            "source": source, "generated_utc": now}


def main():
    print(build_page())


if __name__ == "__main__":
    main()
