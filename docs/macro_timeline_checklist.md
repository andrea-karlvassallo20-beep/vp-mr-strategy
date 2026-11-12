# Macro Timeline Population Checklist — 2021-2024

Purpose: the exact rows needed to populate `data/macro_timeline.csv` for the
dataset span (2021-11 → present; 2021-2024 requested). Fill in manually.
Confidence flags are pre-set: `confirmed` = date verified against the
Federal Reserve calendar / public record; `expected` = month known, exact
day to be verified from the cited source before entering.

## FOMC (decision day = second day, statement 19:00 UTC; `confirmed`)

2021: Jan 26-27 | Mar 16-17 | Apr 27-28 | Jun 15-16 | Jul 27-28 | Sep 21-22 | Nov 2-3 | Dec 14-15
2022: Jan 25-26 | Mar 15-16 | May 3-4 | Jun 14-15 | Jul 26-27 | Sep 20-21 | Nov 1-2 | Dec 13-14
2023: Jan 31-Feb 1 | Mar 21-22 | May 2-3 | Jun 13-14 | Jul 25-26 | Sep 19-20 | Oct 31-Nov 1 | Dec 12-13
2024: Jan 30-31 | Mar 19-20 | Apr 30-May 1 | Jun 11-12 | Jul 30-31 | Sep 17-18 | Nov 6-7 | Dec 17-18

32 rows. `event_type=FOMC`, `asset_scope=ALL`, `event_time_utc=19:00`,
`expected_resolution_utc` = decision date 19:00 UTC.
Source: federalreserve.gov/monetarypolicy/fomccalendars.htm.

## CPI (`expected` — month-level here; take exact 13:30 UTC dates from BLS)

CPI releases ~monthly, mid-month, 13:30 UTC. 48 releases 2021-2024.
Exact dates: bls.gov/schedule/news_release/cpi.htm (BLS release schedule).
Enter one row per release: `event_type=CPI`, `asset_scope=ALL`,
`event_time_utc=13:30`. Do NOT enter from memory — copy from the BLS
schedule; a wrong CPI date is worse than a missing one because it poisons
event-window censoring.

## Major crypto events (`confirmed` dates; verify any you are unsure of)

| Date (UTC) | Event | Suggested row |
|---|---|---|
| 2021-02-08 | Tesla $1.5B BTC purchase disclosed in 10-K/SEC filing | ETF_FLOW_REPORT / OTHER, scope BTC |
| 2021-04-14 | Coinbase (COIN) direct listing | OTHER, scope CRYPTO |
| 2021-05-12 | Tesla halts BTC payments (Musk statement) | CRYPTO_REGULATORY, BTC |
| 2021-05-19 | China crackdown selloff (largest daily liquidation wave to that date) | EXCHANGE_EVENT, CRYPTO |
| 2021-09-07 | El Salvador BTC legal tender takes effect | CRYPTO_REGULATORY, BTC |
| 2021-09-24 | PBOC declares all crypto transactions illegal | CRYPTO_REGULATORY, CRYPTO |
| 2022-02-24 | Russia invades Ukraine (risk-off; crypto donation flows) | OTHER, ALL |
| 2022-05-09 | Terra/UST collapse begins (death spiral through May 12) | OTHER, CRYPTO |
| 2022-06-12 | Celsius freezes withdrawals | EXCHANGE_EVENT, CRYPTO |
| 2022-07-01 | Three Arrows Capital insolvency; Voyager freeze | EXCHANGE_EVENT, CRYPTO |
| 2022-11-08 | FTX withdrawal halt; bankruptcy Nov 11 | EXCHANGE_EVENT, CRYPTO |
| 2023-03-10 | Silicon Valley Bank failure; USDC depeg Mar 11, Signature Mar 12 | OTHER, ALL |
| 2023-06-05 | SEC sues Binance; Jun 06 SEC sues Coinbase | CRYPTO_REGULATORY, CRYPTO |
| 2023-08-29 | Grayscale wins DC Circuit case (ETF catalyst) | CRYPTO_REGULATORY, BTC |
| 2023-10-16 | False spot-ETF-approval post from SEC's hacked X account | CRYPTO_REGULATORY, BTC |
| 2024-01-10 | SEC approves 11 spot BTC ETFs; trading from Jan 11 | ETF_FLOW_REPORT, BTC |
| 2024-04-20 | 4th BTC halving | HALVING, BTC |
| 2024-05-23 | ETH spot ETF 19b-4 approvals | ETF_FLOW_REPORT, ETH |
| 2024-07-23 | ETH spot ETFs begin trading | ETF_FLOW_REPORT, ETH |
| 2024-11-05 | US presidential election (crypto rallied on the result) | OTHER, ALL |
| 2024-12-04 | BTC first closes above $100k | OTHER, BTC |

## Rules for filling (from docs/data_dictionary.md)

- `event_id` = `YYYYMMDD-HHMM-<slug>`, stable forever.
- Times UTC only. `all_day=1` for events with no single decision moment.
- `surprise_note` is filled AFTER the event and is NEVER a model input.
- Empty strings, never invented placeholders.
