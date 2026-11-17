import sys, html
sys.path.insert(0, 'src')
import pandas as pd, numpy as np

import os
_dorm = 'paper/research/clue_scan/mega_dormancy_table.csv'
if not os.path.exists(_dorm):
    _dorm = 'paper/research/clue_scan/dormancy_table.csv'
dorm = pd.read_csv(_dorm)
miss = pd.read_csv('paper/research/clue_scan/missed_moves.csv')
stats = pd.read_csv('paper/research/clue_scan/missed_moves_stats.csv')

def heat_color(days):
    # 0 days -> hot red; 400+ -> deep blue (cold/dormant)
    t = min(days, 400) / 400.0
    r = int(255 * (1 - t) + 30 * t)
    g = int(90 * (1 - t) + 60 * t)
    b = int(60 * (1 - t) + 220 * t)
    return f"rgb({r},{g},{b})"

def cell(series, days, primed, cls):
    ring = "border:2px solid #35ff9e;" if primed else "border:1px solid rgba(255,255,255,.12);"
    return (f'<div class="hm-cell" style="background:{heat_color(days)};{ring}" '
            f'title="{html.escape(str(series))} — {int(days)} days since last ≥4σ day'
            f'{" — PRIMED (coiled)" if primed else ""}">'
            f'<span class="hm-name">{html.escape(str(series))[:14]}</span>'
            f'<span class="hm-days">{int(days)}d</span></div>')

blocks = []
for cls, g in dorm.groupby('class'):
    g = g.sort_values('dormancy_score', ascending=False)
    n_primed = int(g['primed'].sum())
    cells = "\n".join(cell(r.series, r.last_4sigma_days_ago, r.primed, cls) for r in g.itertuples())
    blocks.append(f"""
<section class="hm-class">
  <h3>{cls} <span class="hm-count">{len(g)} series · {n_primed} primed</span></h3>
  <div class="hm-grid">{cells}</div>
</section>""")

# stats table
stat_rows = "\n".join(
    f"<tr><td>{r['class']}</td><td>{int(r['n_moves'])}</td><td>{int(r['n_detected_primed'])}</td>"
    f"<td>{int(r['n_missed'])}</td><td>{r['detection_rate']*100:.1f}%</td>"
    f"<td>{r['miss_median_comp_days']:.0f}</td><td>{r['miss_median_rvol_pct']:.1f}</td>"
    f"<td>{r['miss_median_range_pos']:.2f}</td><td>{r['miss_median_stretch_z']:.2f}</td></tr>"
    for r in stats.to_dict('records'))

# top missed moves per class (the curriculum)
miss_rows = []
for cls in ('crypto', 'commodity', 'index', 'equity'):
    g = miss[miss['class'] == cls].head(12)
    for r in g.itertuples():
        miss_rows.append(
            f"<tr><td>{r.series}</td><td>{r.class_ if hasattr(r,'class_') else cls}</td>"
            f"<td>{'up' if r.direction=='up' else 'down'}</td>"
            f"<td>{r.move30d*100:+.0f}%</td><td>{r.move_end_date}</td>"
            f"<td>{r.comp_days:.0f}</td><td>{r.rvol_pct:.1f}</td><td>{r.range_pos:.2f}</td>"
            f"<td>{r.stretch_z:.2f}</td></tr>")
miss_rows = "\n".join(miss_rows)

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from site_nav import render as _render_nav
NAV = _render_nav("dormancy.html").replace("{", "{{").replace("}", "}}")

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The dormancy heat map — vp-mr-strategy</title>
<meta name="description" content="The dormancy map: 1,300+ series tracked by how long they have been quiet, with primed coils ringed.">
<link rel="stylesheet" href="site.css">
<style>
body{{background:#0b0e14;color:#c9d1d9;font-family:Georgia,serif;margin:0;padding:2rem;max-width:1200px;margin:auto}}
h1{{color:#fff;font-size:2.2rem;letter-spacing:.02em}}
h2{{color:#35ff9e;border-bottom:1px solid #24304a;padding-bottom:.3rem;margin-top:2.8rem}}
h3{{color:#fff;margin-bottom:.6rem}}
.hm-count{{color:#8b949e;font-weight:normal;font-size:.95rem;margin-left:.6rem}}
.hm-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(108px,1fr));gap:6px}}
.hm-cell{{border-radius:6px;padding:6px 4px;text-align:center;display:flex;flex-direction:column;gap:2px}}
.hm-name{{font-size:.62rem;color:rgba(255,255,255,.92);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.hm-days{{font-size:.7rem;color:rgba(255,255,255,.75)}}
table{{border-collapse:collapse;width:100%;font-size:.85rem;margin:1rem 0}}
th,td{{border:1px solid #24304a;padding:.35rem .55rem;text-align:left}}
th{{background:#161b26;color:#35ff9e}}
tr:nth-child(even) td{{background:#11151f}}
.note{{color:#8b949e;font-size:.9rem;font-style:italic}}
.legend{{display:flex;gap:1rem;align-items:center;margin:.8rem 0;font-size:.85rem}}
.swatch{{display:inline-block;width:36px;height:14px;border-radius:3px;margin-right:4px;vertical-align:middle}}
</style>
</head>
<body>
{NAV}

<div class="epigraph"><p>"You will not find the lion by looking where the noise is. You will find him by noticing where he has been quiet too long."</p></div>

<h1>The Dormancy Heat Map</h1>
<p class="note">Every asset we watch, colored by how long it has been since its last ≥4σ day — the quiet ones burn blue. Green rings mark the primed coil state (compression ≥ 20 days, realized vol in the bottom third, price at the bottom of its range). Descriptive only: scanning hundreds of series for silence finds silence by construction; nothing here is a claim, an edge, or a prediction. The 0.505 direction boundary remains in force.</p>

<div class="legend">
<span><span class="swatch" style="background:rgb(255,90,60)"></span> moved today</span>
<span><span class="swatch" style="background:rgb(140,75,140)"></span> ~200 days quiet</span>
<span><span class="swatch" style="background:rgb(30,60,220)"></span> 400+ days silent</span>
<span><span class="swatch" style="background:transparent;border:2px solid #35ff9e"></span> primed coil</span>
</div>

<h2>1 · The quiet ones, by class</h2>
{''.join(blocks)}

<h2>2 · The misses — moves our score did not flag</h2>
<p class="note">Of the {int(stats['n_moves'].sum())} census episodes, our priming score flagged only {int(stats['n_detected_primed'].sum())} beforehand. The rest happened without the textbook coil — these are the moves that got away, and they are the curriculum: we study them precisely because the score was blind to them. Median pre-move state of the misses: no compression (comp_days ≈ 0), mid-range volatility, no stretch. The coil is a clue, not the law.</p>

<table>
<tr><th>class</th><th>moves</th><th>flagged primed</th><th>missed</th><th>detection rate</th><th>miss med comp_days</th><th>miss med rvol_pct</th><th>miss med range_pos</th><th>miss med stretch_z</th></tr>
{stat_rows}
</table>

<h3>The biggest moves the score did not see (study list)</h3>
<table>
<tr><th>series</th><th>class</th><th>dir</th><th>30d move</th><th>ended</th><th>comp_days</th><th>rvol_pct</th><th>range_pos</th><th>stretch_z</th></tr>
{miss_rows}
</table>
<p class="note">KMD's +2,094% with no coil at all lives in this table's family — the honest momentum boundary. The misses are recorded, not explained away.</p>

<h2>3 · What this page cannot tell you</h2>
<p class="note">Whether any quiet series will move, which way, or when. The heat map is a watchlist, not a forecast. The forward test on the 2026-11-12 watchlist (KAVA, HOLO, GENIUS, SOL) already showed the coil fires without promising direction — three of four broke downward within two days. When a blue cell moves, it goes into the misses table above and gets studied.</p>

</body>
</html>"""
open('docs/dormancy.html','w').write(page)
print('docs/dormancy.html written,', len(page), 'bytes')
