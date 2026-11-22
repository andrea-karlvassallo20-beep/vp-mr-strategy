# Knowledge Base Exports (build 2026-11-22)

Complete text exports of the two personal knowledge topics (market-studies and trading-research), built for transfer to another AI.

## Files

- Market-Studies-Knowledge-Export.txt: single file, 987646 bytes, md5 56a8d79256ce03f952f3ec9ae88d8702. 53 source files embedded byte-exact.
- Trading-Research-Knowledge-Export.part00.txt through part07.txt: the trading-research export split into 8 parts, because the whole file (4730469 bytes) exceeds the push limit of the integration used to upload it. Reassemble byte-exact by concatenating in numeric order:

cat Trading-Research-Knowledge-Export.part0*.txt > Trading-Research-Knowledge-Export.txt

md5 of the reassembled file: 4d316a660f3dd09d33db139484479022

Part sizes and md5s:

part00 603383 bytes md5 51e2035eaaadd6c7b8a310d4ff63aa1d
part01 604720 bytes md5 4b27e47ca3280d711401285f6cbad459
part02 600096 bytes md5 77ceda06e72109e4b7837048f413e5a8
part03 600836 bytes md5 ea2e4626ea5beefd4f4a9d49b50b3447
part04 600052 bytes md5 a9e01161271247c62faa673378b638fc
part05 600906 bytes md5 3f9740d3dc7ac46472c188a1f29818cc
part06 600385 bytes md5 2d03a96cf64af299025732ecee46ce32
part07 520091 bytes md5 579790e73ff3b2015a1e25b6cd10ab44

## Format

Each export embeds every source file verbatim (UTF-8, byte-exact, no transliteration, no reflowing) between marker blocks. Each section header carries the source path and SOURCE BYTES. A MANIFEST at the end of each export lists byte offset, length, md5, and path of every embedded section, so files can be sliced back out and verified machine-side.

Scope: all study notes and the master index of market-studies; the master index, four top-level notes, all docs files, and the four research logs of trading-research. Excluded by scope: code, csv/json data, site.html and its .tmp/.new siblings, compiled PDF, pyc caches, and byte-identical duplicate copies of the trading-research master index (one copy embedded).
