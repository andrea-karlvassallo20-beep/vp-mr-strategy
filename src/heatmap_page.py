"""The heat map page - EVERYTHING, scored, sealed, studied.

Directive (Andrea, Nov 2026): a heat map on the website of EVERYTHING -
all commodities, all indexes, crypto, the main 500 stocks - scored by
what is most likely to make the next significant jump, then tracked
over time to study what surprises.

Generates docs/heatmap.html from the LIVING board: mega_dormancy_table.csv
(the table the nightly board_refresh cycle maintains) when it exists,
falling back to board_table.csv. The page reads whichever board is
current - it can no longer silently render a stale universe while the
refresh cycle moves on (the bug that once left the page at 817 tiles
while the living board held 1,299).

Two board schemas are normalized to one internal frame:
  - the mega dormancy table: dormancy_score (higher = deeper coil,
    min-max normalized within the board for color), primed flag,
    artifact derived from |ret30| > 20%, genesis from n_days < 90.
  - the clue-scan board table: primed_score, eligible, artifact_flag,
    genesis_flag as committed.

Sections are data-driven: every class present on the board gets a
section, in CLASS_ORDER plus first-appearance order for unknown classes.
No class is ever silently dropped again (the etf class was invisible
until this became data-driven).

DESCRIPTIVE ONLY. The multiplicity warning is binding at its worst on a
1,300-series board: extremes are found by construction. The score
ranks candidates; it tests nothing, and WHICH WAY is refused. The only
path from this page to knowledge is C7's kill lines - the surprise
ledger exists precisely so the ranking is judged against sealed
reality, not against memory.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import surprise_ledger as sl  # noqa: E402

CLUE = Path("paper/research/clue_scan")
MEGA_CSV = CLUE / "mega_dormancy_table.csv"
BOARD_CSV = CLUE / "board_table.csv"
PAGE = Path("docs/heatmap.html")

CLASS_TITLES = {
    "commodity": "Commodities",
    "index": "Indexes",
    "world_index": "World indexes (frontier and war-adjacent included)",
    "rate": "Rates",
    "fx": "FX (majors, EM, the Iranian rial)",
    "equity": "Large-cap equities",
    "global_equity": "Global mega-caps (non-US)",
    "sp500": "S&P 500 (full constituents)",
    "sp400": "S&P 400 (mid caps)",
    "sp600": "S&P 600 (small caps)",
    "etf": "ETFs",
    "crypto": "Crypto",
}

# Section order when known; any class not listed here is appended after,
# in first-appearance order - the page can never silently drop a class.
CLASS_ORDER = ["commodity", "index", "world_index", "rate", "fx",
               "equity", "global_equity", "sp500", "sp400", "sp600",
               "etf", "crypto"]

NAV = """<nav>
  <a href="index.html">Thesis</a>
  <a href="manual.html">The working manual</a>
  <a href="causal.html">Causal chains</a>
  <a href="books.html">The books, taught</a>
  <a href="clues.html">The clue dossier</a>
  <a href="criteria.html">The night-before sauce move</a>
  <a href="v4_charts.html">The board, colored</a>
  <a href="heatmap.html" aria-current="page">The heat map</a>
  <a href="dormancy.html">The dormancy map</a>
  <a href="resources.html">The library</a>
  <a href="ledger.html">The claims ledger</a>
  <a href="instrument.html">The instrument (live)</a>
</nav>"""


def load_board(mega_csv=MEGA_CSV, board_csv=BOARD_CSV):
    """The living board, normalized: one frame, one score column, flags."""
    if Path(mega_csv).exists():
        df = pd.read_csv(mega_csv)
        score = df["dormancy_score"].astype(float)
        span = float(score.max()) or 1.0
        out = pd.DataFrame({
            "series": df["series"],
            "class": df["class"],
            "score": score / span,
            "score_label": "dormancy score (normalized)",
            "comp_days": df["comp_days"],
            "rvol_pct": df["rvol_pct"],
            "range_pos": df["range_pos"],
            "ret30": df.get("ret30", np.nan),
            "eligible": df["primed"].astype(bool),
            "artifact_flag": (df.get("ret30", 0).abs() > 0.20),
            "genesis_flag": df["n_days"] < 90,
            "last_date": "",
            "vol_ratio": np.nan,
            "source": "mega_dormancy_table.csv",
        })
    elif Path(board_csv).exists():
        df = pd.read_csv(board_csv)
        out = pd.DataFrame({
            "series": df["series"],
            "class": df["class"],
            "score": df["primed_score"].astype(float),
            "score_label": "priming score",
            "comp_days": df["comp_days"],
            "rvol_pct": df["rvol_pct"],
            "range_pos": df["range_pos"],
            "ret30": df.get("ret30", np.nan),
            "eligible": df["eligible"].astype(bool),
            "artifact_flag": df["artifact_flag"].astype(bool),
            "genesis_flag": df["genesis_flag"].astype(bool),
            "last_date": df.get("last_date", ""),
            "vol_ratio": df.get("vol_ratio", np.nan),
            "source": "board_table.csv",
        })
    else:
        raise SystemExit("no board found - run the board refresh first")
    out["artifact_flag"] = out["artifact_flag"].fillna(False).astype(bool)
    out["genesis_flag"] = out["genesis_flag"].fillna(False).astype(bool)
    return out.sort_values("score", ascending=False).reset_index(drop=True)


def _tile_color(score):
    """Dark -> amber -> red interpolation on the observatory palette."""
    s = max(0.0, min(1.0, float(score)))
    if s < 0.5:
        t = s / 0.5
        rgb = [int(13 + (245 - 13) * t), int(20 + (176 - 20) * t),
               int(32 + (76 - 32) * t)]
    else:
        t = (s - 0.5) / 0.5
        rgb = [int(245 + (248 - 245) * t), int(176 + (113 - 176) * t),
               int(76 + (113 - 76) * t)]
    return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"


def _tile(row):
    score = float(row["score"])
    color = _tile_color(score)
    dim = "" if row["eligible"] else " opacity:.38;"
    flag = ""
    if row["artifact_flag"]:
        flag = '<span class="tflag">moved</span>'
    elif row["genesis_flag"]:
        flag = '<span class="tflag">new</span>'
    return (f'<div class="tile" style="background:{color};{dim}" '
            f'title="{row["series"]} score {score:.3f} comp_days '
            f'{row["comp_days"]} rvol_pct {row["rvol_pct"]}">'
            f'<span class="tname">{row["series"]}</span>'
            f'<span class="tscore">{score:.2f}</span>'
            f'<span class="tmeta">{int(row["comp_days"])}d coil</span>'
            f"{flag}</div>")


def _class_section(cls, sub):
    tiles = "\n".join(_tile(r) for _, r in sub.iterrows())
    n_elig = int(sub["eligible"].sum())
    deep = int((sub["comp_days"] >= 20).sum())
    top = sub.iloc[0] if len(sub) else None
    top_s = (f'{top["series"]} ({top["score"]:.2f})'
             if top is not None else "-")
    return f"""<section>
<h2>{CLASS_TITLES.get(cls, cls)}<span class="dot">.</span></h2>
<p class="dim">n={len(sub)} &middot; primed={n_elig} &middot;
deep coils (20d+)={deep} &middot; hottest: <b>{top_s}</b></p>
<div class="tilegrid">
{tiles}
</div>
</section>"""


def _top_table(board, k=20):
    rows = []
    for i, (_, r) in enumerate(
            board[board["eligible"]].head(k).iterrows(), start=1):
        rows.append(
            f"<tr><td>{i}</td><td>{r['series']}</td>"
            f"<td>{r['class']}</td><td>{r['score']:.3f}</td>"
            f"<td>{int(r['comp_days'])}</td><td>{r['rvol_pct']:.1f}</td>"
            f"<td>{r['range_pos']:.2f}</td></tr>")
    return """<table>
<tr><th>Rank</th><th>Series</th><th>Class</th><th>Score</th>
<th>Coil days</th><th>RVol pct</th><th>Range pos</th></tr>
""" + "\n".join(rows) + "</table>"


def _surprise_section(ledger_path):
    records = sl.read_ledger(ledger_path)
    snaps = [r for r in records if r["type"] == sl.SNAPSHOT_RECORD]
    res = [r for r in records if r["type"] == sl.RESOLUTION_RECORD]
    head = (f"<p class=\"dim\">Snapshots sealed: <b>{len(snaps)}</b> &middot; "
            f"resolutions past horizon: <b>{len(res)}</b> &middot; "
            f"ledger: hash-chained, append-only, verify-before-write</p>")
    if not res:
        return (head + "<p>No horizon has passed yet. The scores above are "
                "sealed; reality gets its turn in 10 bars. Come back and "
                "study what surprised.</p>")
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
rho between the sealed priming score and the realized 10-bar max
|move| - never whether one winner proves anything.</p>
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
    score_label = board["score_label"].iloc[0]
    source = board["source"].iloc[0]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    n_elig = int(board["eligible"].sum())
    top = board[board["eligible"]].iloc[0] if n_elig else board.iloc[0]

    sections = []
    present = [c for c in CLASS_ORDER if (board["class"] == c).any()]
    extras = [c for c in board["class"].dropna().unique()
              if c not in CLASS_ORDER]
    for cls in present + extras:
        sub = board[board["class"] == cls]
        if len(sub):
            sections.append(_class_section(cls, sub))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Salient &mdash; The heat map</title>
<link rel="stylesheet" href="site.css">
<style>
.tilegrid {{ display: flex; flex-wrap: wrap; gap: 3px; }}
.tile {{ display: inline-flex; flex-direction: row; align-items: center;
  gap: 5px; height: 21px; padding: 1px 7px; border-radius: 4px;
  color: #070b12; position: relative; white-space: nowrap; }}
.tile .tname {{ font-family: var(--mono); font-size: 9.5px; font-weight: 700;
  max-width: 110px; overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; }}
.tile .tscore {{ font-size: 10px; font-weight: 700; opacity: .85; }}
.tile .tmeta {{ display: none; }}
.tile .tflag {{ font-size: 8px; text-transform: uppercase;
  letter-spacing: .5px; opacity: .6; }}
.legend {{ display: flex; gap: 0; border-radius: 6px; overflow: hidden;
  height: 12px; max-width: 420px; }}
.legend i {{ flex: 1; }}
</style>
</head>
<body>
{NAV}
<main>

<div class="kicker">Everything on one board &middot; scored &middot; sealed
&middot; studied</div>
<h1>The heat map<span class="dot">.</span></h1>

<div class="epigraph">
"Look at EVERYTHING." So the board holds everything: all commodities, all
indexes - world, frontier and war-adjacent included - rates, FX down to
the Iranian rial, the full S&amp;P 500, non-US mega-caps, ETFs, crypto.
Zoom out: the board reads as a checkerboard - color first, one flat cell
per series, dark = nothing coiled, amber = compression building, red =
the deepest coils alive tonight. Hover any cell for its name and
grievance.
</div>

<p><span class="big">Descriptive only.</span> The score ranks
candidates; it tests nothing. Scanning ~1,300 series for extremes finds
extremes by construction - the multiplicity warning is binding. WHICH WAY
is refused by measurement: priming is directionless, on purpose. The only
path from this page to knowledge is C7's kill lines. What this page adds
is time: the top candidates are <b>sealed</b> into a hash-chained ledger
with their scores, and once the 10-bar horizon passes, the realized jump
is resolved against the same data - so "what surprised" is studied
against sealed predictions, never against memory.</p>

<div class="grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0">
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Series on the board</div><div style="font-size:22px;font-weight:700">{len(board)}</div></div>
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Primed candidates</div><div style="font-size:22px;font-weight:700">{n_elig}</div></div>
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Hottest tile</div><div style="font-size:22px;font-weight:700">{top["series"]} <span style="color:var(--accent2)">{top["score"]:.2f}</span></div></div>
<div class="card" style="background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)">Board built</div><div style="font-size:22px;font-weight:700">{now}</div></div>
</div>

<div class="legend" aria-hidden="true">
<i style="background:{_tile_color(0)}"></i><i style="background:{_tile_color(.25)}"></i><i style="background:{_tile_color(.5)}"></i><i style="background:{_tile_color(.75)}"></i><i style="background:{_tile_color(1)}"></i>
</div>
<p class="dim" style="margin-top:4px">{score_label} 0 &rarr; 1 &middot;
dimmed tiles: move-already-happened (artifact) or too new (genesis filter,
&lt;90d listing) &middot; board source:
<code>{source}</code></p>

{"".join(sections)}

<section>
<h2>The top-20 primed candidates on the whole board<span class="dot">.</span></h2>
{_top_table(board)}
</section>

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
            "n_eligible": n_elig, "source": source,
            "generated_utc": now}


def main():
    print(build_page())


if __name__ == "__main__":
    main()
