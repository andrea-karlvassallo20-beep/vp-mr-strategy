# CLOUD_DEPLOY.md - GitHub Codespaces instructions

Purpose: run the L2 gate and the C1-L2 pipeline on real Tardis data in a cloud dev container, instead of a local machine. Codespaces gives you a real Python environment (pandas, pyarrow, scipy, lifelines) with enough disk for the tick files, which the sandbox used for the gating and dry-run work could not provide.

## 1. Provision the codespace

1. Open the repo on GitHub, click the green Code button, then the Codespaces tab, then "Create codespace on main".
2. Machine type: 4-core / 16 GB RAM minimum. 8-core / 32 GB recommended; the tick processing is mostly I/O, but the uncompressed incremental_book_L2 CSVs are large (145.2M rows for one day on 2026-10-01).
3. Disk: the default disk is 32 GB. One day of incremental_book_L2 (BTCUSDT, binance-futures) is ~796 MB compressed; a 10-day window is roughly 8-12 GB compressed and several times that uncompressed. If you plan to keep both raw CSVs and parquet for 2-4 weeks, stop the codespace and recreate with a larger disk, or convert and delete raw files day by day.
4. Costs: Codespaces bills per core-hour while running. Stop the codespace when not in use; idle shutdown is on by default.

## 2. Environment

The default image ships Python 3.12. In the codespace terminal:

```bash
python3 --version
pip install pandas pyarrow scipy numpy lifelines
```

## 3. API key handling

1. Add the Tardis key as a Codespaces secret: repo Settings, Codespaces, Secrets, New secret, name it TARDIS_API_KEY, paste the key value. Codespaces injects it into every new codespace for this repo as the environment variable $TARDIS_API_KEY.
2. Never paste the key into a file, a commit, a notebook, or a command line that is logged. Never echo it. The trial key pasted in chat history should be rotated regardless; it is quota-dead (Tardis code 278) but still a credential.
3. First-of-month files are free and need no key at all. Everything else needs a paid plan or a fresh trial.

## 4. Download the data

Free day (verified, no key needed; byte sizes are the ones reproduced by a correct pull):

```bash
mkdir -p data/raw && cd data/raw
curl -o incremental_book_L2_BTCUSDT_2026-10-01.csv.gz \
  "https://datasets.tardis.dev/v1/binance-futures/incremental_book_L2/BTCUSDT/2026-10-01.csv.gz"
# expect 796,135,847 bytes
```

Paid window (auth header; NEVER use -L together with the header, the redirect forwards Authorization to a third party):

```bash
curl -H "Authorization: Bearer $TARDIS_API_KEY" \
  -o "incremental_book_L2_BTCUSDT_${D}.csv.gz" \
  "https://datasets.tardis.dev/v1/binance-futures/incremental_book_L2/BTCUSDT/${D}.csv.gz"
```

Loop over your window one day at a time. Also pull book_snapshot_25 and trades for the same days if you need the snapshot cross-check and the trade labels. Check the byte size of every file against a first successful pull; a truncated download fails the gate later and wastes quota.

## 5. Critical schema warning

src/verify_l2_gate.py expects seq_u/seq_pu or sequence_number/operation schemas. The Tardis datasets CSV (exchange, symbol, timestamp, local_timestamp, is_snapshot, side, price, amount) matches NEITHER, so verify_l2_gate.py refuses it by design. This is correct behavior, not a bug.

For Tardis CSVs use the repo-native gate:

```bash
python3 src/gate_tardis_sample.py data/raw/incremental_book_L2_BTCUSDT_2026-10-01.csv.gz
```

It checks criteria 2 and 3 (mid and depth agreement against book_snapshot_25); criterion 1 (sequence continuity) is structurally N/A on Tardis CSVs because the feed carries no sequence numbers.

Parity anchors your gate run must reproduce (independently verified by the streaming mawk gate, session 81, and the repo's own committed validation):

- 2026-10-01: 145,203,455 rows, mid 100/100, depth 100/100, 4 snapshot blocks (initial + 3 mid-day resyncs, pre-resync gaps 0.476/0.512/2.497 s are the INVALIDATED windows for any later event clock), exit 0.
- 2026-10-10: 78,904,284 rows, 1 block, max update gap 0.052 s, mid 100/100, depth 100/100, exit 0.

## 6. Parquet conversion

The repo gates stream and does not need parquet. The C1-L2 pipeline reads data frame style, so convert chunked after the gate passes:

```python
import pandas as pd

def convert_day(src, dst, chunksize=2_000_000):
    header = True
    for chunk in pd.read_csv(src, compression="gzip", chunksize=chunksize):
        chunk.to_parquet(dst, index=False, append=not header)
        header = False
```

The convert_to_parquet.py copy from the sandbox has never been executed (no pandas there); its first real run happens here, so verify the row counts of one parquet against its CSV before batch-converting.

## 7. Run the C1-L2 pipeline

The spec is paper/research/c1_l2_test_spec.md; the runner is src/c1_l2_test.py; the diagnostics and the five kill lines are in src/cox_diagnostics.py. Requirements proven by the dry run on 2026-10-01:

- The primary spec needs 2-4 weeks of data. On a 1-day window the H=24h purge plus embargo empties every training fold (6/6 folds, train rows 0, leakage violations 0). That is correct machinery behavior, not a bug: do not shorten the horizon to force folds on a short window and do not read a shortened run as the spec.
- Macro censor before labeling: src/macro_censor.py with data/macro_timeline.csv. Note NFP lands 2026-10-02 12:30 UTC inside the October window.
- Run order: gate first, then convert, then label, then fit. Nothing is evaluated before the gate passes.

Dry-run reproducibility reference (2026-10-01, H=2h machinery config): 57,498 BBBA touch events, 19,551 compression events, 74 decision rows, 47 H=2h events, pooled out-of-fold concordance 0.5657 on the labeled 1-day harness. The harness adaptations are documented in its docstring; full-window runs follow the repo spec, not the dry-run shortcuts.

## 8. Persistence and hygiene

- Codespace files survive stop/restart but not deletion. Anything valuable must be committed; raw data and the key are never committed (.gitignore keeps data/ paths out by design, the directories are .gitkeep placeholders).
- Commit gate logs and parquet-adjacent small outputs, not tick data. Store gate exit codes with the logs; a gate claim without a committed log is not evidence.
- Stop the codespace when done. Delete it only after everything needed is pushed.

## 9. Order of operations

1. Provision the codespace (section 1).
2. pip install (section 2).
3. Add the key as a Codespaces secret (section 3), or skip for free first-of-month days.
4. Download one day; verify the byte size (section 4).
5. Gate it with src/gate_tardis_sample.py; check the parity anchors (section 5).
6. Convert to parquet; verify row counts (section 6).
7. Repeat 4-6 for the full 2-4 week window, one day at a time.
8. Macro censor, then run the C1-L2 pipeline per spec (section 7).
9. Commit logs and outputs; stop the codespace (section 8).
