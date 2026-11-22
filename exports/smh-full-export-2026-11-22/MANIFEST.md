# SMH / AVFI Research Programme - Full Export, 2026-11-22

Owner-directed snapshot of the complete durable state of the Research project
(the "Salient Market Hypothesis" / AVFI weekly market-research programme),
generated 2026-11-22 at programme session 230.

## The original single file

- Name: SMH-research-programme-full-export-2026-11-22.txt
- Size: 14,610,844 bytes
- MD5:  fc83d7686e114d7df1cde47cf5bf33a5
- UTF-8 text, newline-terminated lines
- Contents: 333 text files (trading-research bundle: record, mirrors,
  progress ledger, governance and frontier documents, signed and unsigned
  amendments, thesis text source, research scripts and reports, data CSVs,
  site source; plus the market-studies knowledge base entrypoint and all 52
  study notes) with a per-file manifest header (bytes / md5 / path) and
  ##FILE-BEGIN## / ##FILE-END## delimiters.
- Binary exclusions, listed honestly inside the export header: bytecode
  caches only, plus the frozen thesis PDF; the thesis text source is included.

## Why it is split

The upload channel imposes a hard memory ceiling near 2 MB per operation,
so the single 14.6 MB file is stored as 20 exact byte-range parts. The parts
are arbitrary byte splits: each part may begin and end mid-line. Concatenate
in order to recover the original file byte for byte.

## Reassembly

    cat part-01.txt part-02.txt part-03.txt part-04.txt part-05.txt \
        part-06.txt part-07.txt part-08.txt part-09.txt part-10.txt \
        part-11.txt part-12.txt part-13.txt part-14.txt part-15.txt \
        part-16.txt part-17.txt part-18.txt part-19.txt part-20.txt \
        > SMH-research-programme-full-export-2026-11-22.txt

Verify after reassembly:

    wc -c SMH-research-programme-full-export-2026-11-22.txt
    # 14610844
    md5sum SMH-research-programme-full-export-2026-11-22.txt
    # fc83d7686e114d7df1cde47cf5bf33a5

Or, since the names sort in order: cat part-*.txt > the same result.

## Parts (1-based inclusive byte ranges of the original file)

| part | byte range | bytes | md5 | git blob sha |
|---|---|---|---|---|
| part-01.txt | 1 - 1400000 | 1400000 | 45f509cf902c6bc930e958d0a273b35f | 283e849cb449f242ae9270cff4e0b39c848182e9 |
| part-02.txt | 1400001 - 2100000 | 700000 | 9e19fefd27b554fa97efb87e810a0e8b | 88fed7607b42b667d1707df7767d4be3c17ecfa8 |
| part-03.txt | 2100001 - 2800000 | 700000 | 069c108e3dd18b342cf4871a06966a37 | 86445987ed18806f7ebb2562c0851dfe5afec76d |
| part-04.txt | 2800001 - 3500000 | 700000 | 2d5dcbe21379c0b09ca322f221701c04 | be28e5b293e746172c3e0f4c02ef2a01c2c99b6d |
| part-05.txt | 3500001 - 4200000 | 700000 | d4e874f2a5f9a74e709c85ec4041fbf0 | 20e136463caa4b6bb020dc665a17c67b0a6354c2 |
| part-06.txt | 4200001 - 4900000 | 700000 | 1a73483819358ed537f3f0a0a7e73661 | 04faccf6f1ca7367e3ea9f4519407cfc472ce364 |
| part-07.txt | 4900001 - 5600000 | 700000 | d074e2d36f2cb78324b57fdccbe4adc9 | cda08534fd2b4af997f9b94f6148cb6cbba0d106 |
| part-08.txt | 5600001 - 6300000 | 700000 | 74c9dece18b787099c38d3c2fd967e4c | 4d2035fea3f17a508499d0ffc5884fddeea25537 |
| part-09.txt | 6300001 - 7000000 | 700000 | 3cb4f1d2be3dbd2d5b1b1555679e06c2 | cd83e70e5613c2fe85afdfaa788d528ecca52636 |
| part-10.txt | 7000001 - 7700000 | 700000 | 4d045f9d36bf95d5128e0cd49a267d9d | 4f0fe872a8b6a3c6920610df5a7b7da2baf655ad |
| part-11.txt | 7700001 - 8400000 | 700000 | 238a10563d35d1759cff9e4edaf26fe8 | 108ba3c2cb3019e2a764f66e2547bb2b5426f6a8 |
| part-12.txt | 8400001 - 9100000 | 700000 | 7b82f300c3a36f7648f856be341c6452 | f8c581e9f85913622f6ce854586ce8468cf4c7c7 |
| part-13.txt | 9100001 - 9800000 | 700000 | c33a667ea721fe18dcc4118ccd9151d0 | 4c271c253d09c5c6a9a4e3f879dc60b68e0b1d78 |
| part-14.txt | 9800001 - 10500000 | 700000 | 55ede2ce3c1d341c56cc0d1056c3fe68 | 262ab8cc0d299c46c9e8134dc50386bfaa18e368 |
| part-15.txt | 10500001 - 11200000 | 700000 | 5f4c52b73558fa4bfb6b6477f6d9302a | a3fd608d10a6d1350a49d377c94904a813095c46 |
| part-16.txt | 11200001 - 11900000 | 700000 | b4d8c67372eb45eb4283d216485f1622 | e27dabe952bd0497602393b55e4ae7fedaea078c |
| part-17.txt | 11900001 - 12600000 | 700000 | efce786e70b462bdbbe920654497226d | 36ecde04cb2fdbb94c4789adae880fcff4188f1e |
| part-18.txt | 12600001 - 13300000 | 700000 | 42475e2778cbd0ecf9e35782345a157e | b7abbc5ea48727d933fd515b6eb6c546a70a138a |
| part-19.txt | 13300001 - 14000000 | 700000 | e4d19ff00fe273f2c9104f11b60cf97c | a40aed07805852a59a452b4a8e31a0efbe8d581c |
| part-20.txt | 14000001 - 14610844 | 610844 | cfdd618ede427b1cf0f729b522940285 | 2e54c60aee03578c1fb0a8a80fc3cb1b2b65ebbd |

All 20 blob shas were computed from the local export BEFORE upload and the
uploaded blobs were verified to match, so each part is byte-identical to its
local counterpart. Independent verification does not require this manifest:
recover the blob sha of any part with `git hash-object` and compare.

## Landing commits on main (in order)

part-01 122b9ceff2a7ee3e5a6fbd1c7d40b64a2acf81c7
part-02 0fefb6609d6658b25e891cef79467446a86dc55d
part-03 bea89e5169f6e45fd140fa20e9655f613a3b22d9
part-04 72f2348a81821fdaa3de46e556b0547c35c4e76e
part-05 687c6b93c184ee5de9728a76f00942a286d2c246
part-06 3616d1df44dfda18ebab20ee323c142147776c4e
part-07 64fd0ec35a6c59b2246de381ccaf62d4bcc8d3a2
part-08 87d6e93c3c6945feff2e26f371b0d5b71307217d
part-09 21f5b84be288e6bf5afe0f3b5a5e16e30a67ba75
part-10 a1c293631d586569a14456216d69a78634a181c3
part-11 068a663252f6387fb0c92be8c173a6cf2cf18759
part-12 42537c5cdafb9d1ca40e6a6ff289adc88f0a2a79
part-13 7e4c70ce7177145965ba154c6e85ef40cf5d85dc
part-14 2d432b4ca1954a1a5ea7ac7f48a27fe3b5773212
part-15 99c2519cf6734835ec6c0abc58b9b9bf393e217c
part-16 be55c6a7b915606b52d9a4e231aa7f2fb35a2233
part-17 53a620d7352f42106ac2b251000f219fcdeac4a2
part-18 6d7eb22ac3ff8a3eaf04f14ef3964f571401fb0f
part-19 5d7a50cd9965fc9595121162ca66c4ccd47bfd83
part-20 11c180fd1f9161115e945a43809a4e87971050b6

## Standing status lines of the programme at snapshot time

- Default assumption: there is no edge; the burden of proof is on every signal.
- NQ 2021+ holdout: SPENT, never re-evaluated.
- Frozen constants never re-tuned; closed verdicts stand.
- Paper trading only; unsigned drafts have zero status until the owner's dated word.
- Snapshot only: nothing here was evaluated, booked, armed or ratified by this upload.
