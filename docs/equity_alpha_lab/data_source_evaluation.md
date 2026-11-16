# Data source evaluation — the Month-1 gate decision

The roadmap's critical data requirement, restated as a gate: **no factor
code is written until a source is chosen and its survivorship and
point-in-time characteristics are audited against this checklist.** A
convenient downloadable dataset is not necessarily historically unbiased.

## Hard requirements

1. Historical prices for the full research window, including **delisted
   securities** (survivorship-free).
2. **Corporate actions**: splits AND cash dividends, with adjustment
   factors delivered separately from unadjusted prices (the lab schema
   requires exactly this).
3. **Point-in-time fundamentals**: each record must carry a publication
   (announce/restatement) date, not just a fiscal period end. Restatement
   history (as-first-reported vs as-restated) must be a declared choice.
4. A **security master** that maps stable IDs across ticker changes and
   records listing/delisting dates and delisting returns.
5. Reproducible access: bulk download or stable API, no scraping.

## Candidate evaluation (to be completed with actual coverage checks)

| Source | Prices | PIT fundamentals | Delistings | Cost | Verdict |
|---|---|---|---|---|---|
| CRSP (via WRDS) | Survivorship-free, the academic standard; delisting returns included | No (pair with Compustat) | Yes, with delisting returns | Institutional/academic license | Gold standard for prices; the delisting-return field is exactly what `schema.py` expects |
| Compustat (via WRDS) | — | Point-in-time via `rdq` (report date); as-first-reported via Compustat PIT | — | Institutional/academic license | The `rdq` column is the announce_date this lab requires; verify restatement policy |
| Sharadar (Core US, via Nasdaq Data Link) | SEP equities + actions table | SF1/SF2 fundamentals with `calendardate`/`datekey` (dimension + report date) | Yes (delisted tickers retained) | Paid, moderate | Strong single-vendor candidate; verify delisting-return availability and depth of history |
| Norgate Data | Survivorship-back-adjusted, delisted included | Fundamentals limited | Yes | Paid, moderate | Good for price-based factors; weak for PIT fundamentals |
| yfinance / stooq / other free EOD | Current listings dominate; delisted tickers vanish | None | Mostly no | Free | **Rejected for research**: survivorship-biased by construction; acceptable only for pipeline smoke tests on recent, still-listed names |
| Simulated/synthetic | Full control | Full control | Full control | Free | Used for the lab's own tests; never for claims |

## Audit checklist (run on the chosen source BEFORE Month 2)

- [ ] Delisted names present: count securities with a member_end in the
      research window; must be nonzero and plausible (US listings churn).
- [ ] Survivorship number: run `universe.survivorship_audit` on a mid-window
      date and record members/exited counts in the findings ledger.
- [ ] Corporate actions: pick 5 known split events; confirm unadjusted close
      halves and adj_factor doubles on the ex-date (the lab's continuity
      report must show zero flags for them).
- [ ] Dividends: confirm adj_factor grows across ex-dividend dates and the
      total-return series is continuous.
- [ ] PIT fundamentals: pick 5 known earnings announcements; confirm the
      announce_date column matches the historical press-release date, not
      the period end (this is the exact trap `pit.py` is built to catch).
- [ ] Restatements: determine whether fundamentals are as-first-reported
      or as-restated, and record the choice in the spec BEFORE any factor
      uses them.
- [ ] Coverage: min/max date, name count over time, missingness via
      `quality.missingness_report`.

## Standing rule

The source decision and the audit results are recorded here and dated,
before the first factor is implemented — the same spec-before-data rule
the rest of this repository runs under. Never commit licensed datasets, API
keys, or credentials.
