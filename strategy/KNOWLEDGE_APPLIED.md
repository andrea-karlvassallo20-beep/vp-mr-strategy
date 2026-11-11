# Knowledge applied — from the Market Studies Knowledge Base to this system

Mapping of each knowledge layer (see `KNOWLEDGE.md`) to concrete design
decisions in VP-MR-ETF-D1-001. Where a layer produced a *candidate
improvement*, it was implemented as a research variant (`vol_models.py`)
and handed to the edge-seeker for honest walk-forward evaluation — the
deployed strategy remains frozen (Gate 3).

| Knowledge layer | Concept | Where it lives in this system |
|---|---|---|
| Elliott Wave (Balan) | Regimes: impulse vs corrective phases; mean revention works in ranges, fails in impulses | Motivates the z-score mean-reversion hypothesis AND its known failure mode; the walk-forward and deployment-envelope studies quantify when the edge exists |
| VSA — Master the Markets (Williams) | "Effort vs results"; weak-volume stretches lack real pressure | `VariantStrategy` volume filter: entries only when the stretch bar's volume is below its trailing mean — a research candidate, evaluated nightly |
| Harris, Trading & Exchanges | Microstructure frictions are a first-class cost | Module 4 friction model: half-spread, latency, commission in every backtest and paper fill |
| Hasbrouck / Biais-Glosten-Spatt | Efficient price vs microstructure noise | The MTM equity reconstruction separates position PnL from noise; the SPI audit verifies decision-time data |
| Bouchaud et al. | Square-root impact law | Our impact model is exactly sqrt-impact (`impact_coeff * sqrt(qty)`), aligned with the econophysics evidence |
| Stoll (2002) | Five sources of the spread; temporary vs permanent impact; effective vs realized spread | The expected-cost model charges the informed-flow tax explicitly; the paper sessions will compare expected vs realized costs (future refinement: asymmetric impact) |
| Madhavan (2000) | Information effects permanent, inventory effects transitory | Grounds the VSA filter: a low-volume stretch is more likely transitory (inventory/noise), a high-volume one more likely informed |
| Foucault-Pagano-Roell | Liquidity provision, fragmentation, transparency | Informs venue/broker assumptions in the run card; maker-taker economics noted for future live routing |
| Dark Pools (Patterson) | Feedback loops, quote withdrawal, HFT latency races | Latency modeled at 5ms; kill-switch and flatten-at-close exist precisely because mechanical markets can gap through stops |
| The Quants (Patterson) | Kelly genealogy; 1987 fat tails; funding spirals; model risk | 0.25x fractional Kelly haircut, 0.5% per-trade risk cap, 2% daily kill-switch, 1.0x gross exposure ceiling — all conservative by design |
| Bjork | Martingales; falsification over curve-fitting; stops as hitting-probability bets | The walk-forward and Monte Carlo studies are falsification tests; the ATR trailing stop is treated as a hitting-probability exit, sized via the ATR-risk cap |
| Javaheri | Identification hierarchy: at daily frequency, noise params nearly unestimable | Justifies EWMA/GARCH(1,1) over Heston/3/2 in `vol_models.py`; no over-parameterized vol model at daily bars |
| Levy, Computational Finance | GARCH(1,1), persistence Sigma(alpha+beta)<1, EWMA lambda=0.97 (RiskMetrics), vol clustering | `ewma_vol_ann` (lambda=0.97) and `garch_vol_ann` (alpha=0.05, beta=0.90, persistence 0.95) as sizing-vol candidates in the edge-seeker grid |

## First honest evaluation (real data, 502 bars)

The edge-seeker's expanded 54-candidate grid (z x lookback x vol model x
VSA filter) was run on the fetched real data: the knowledge variants did
NOT beat the selected candidate on this window (selected: z=1.5,
lookback=60, realized vol, no VSA filter; OOS Sharpe -0.52 vs production
-1.16). Both negative in the current adverse regime. The candidates stay
in the nightly research space — the edge-seeker will re-evaluate them as
the live data window grows. Absence of immediate improvement is a result,
not a failure: it is exactly how falsification is supposed to work.
