# Deep-read session 46 (null-time session 50, 2026-11-19): McGillivray & Swishchuk — "Variance-Hawkes Process and its Application to Energy Markets"

Authors: Joshua McGillivray, Anatoliy Swishchuk (University of Calgary). arXiv:2410.08420v1
[q-fin.MF], 14 October 2024. A construction paper: Brownian motion subordinated by a
Hawkes process (Vt := B(Nt)), with a generator derivation, an Itô formula for B²(Nt),
and hand-fitted distribution overlaps on 2018-2019 crude oil and natural gas front-month
futures log returns.

Read 2026-11-19, against ONE question: what here would kill C1-L2 or C8 faster, or
change their kill lines? Source: legally acquired OA copy
(docs/library/text/x618573_variance_hawkes_process_and_its_application_to_ene.txt,
24 pp., page-marked). Next UNREAD triage-rank entry (score 29).

## The paper in one paragraph

The authors subordinate a standard Brownian motion by a simple exponential-kernel
Hawkes counting process (Definition 1, PDF pp. 6-7), note that the price of an asset
depends on trade arrivals rather than calendar time and that continuous subordinators
approximate a discontinuous arrival process (PDF pp. 5-6), and fit ln(S_{t+1}/S_t) =
a + bσ̂B(Nt) to one year each of 2018 and 2019 WTI and NYMEX front-month futures by
hand, trial and error, with visually overlapping distributions (Figs. 2-5, PDF pp.
7-9). Q-Q plots of 2024 per-minute trade volume against exponential quantiles plus
intraday volume profiles are offered as evidence that arrivals are not Poisson (Figs.
6-9, PDF pp. 10-11). They derive the generator of (λt, Nt, B(Nt)) from second-moment
ODEs of Cui-Hawkes-Yi with the assumptions E(NtB(Nt)) = E(λtB(Nt)) = 0 and Var(B(Nt))
= E(Nt) (PDF pp. 12-14, Eqs. (15)-(22)), give the Itô formula dB²(Nt) =
2B(Nt)dB(Nt) + dNt (Theorem 1, PDF p. 14), simulate both sides with Euler-Maruyama
(error mostly within ±20% with spikes they attribute to discretization, Figs. 15-17,
PDF pp. 14-15, 21-23), and leave the marginal distribution B(Nt) ~d √Nt·N(0,1) as an
unproven conjecture (Conjecture 1, PDF p. 15). They explicitly say the Hawkes
α < β stationarity condition "may not be necessary" in their setting (PDF p. 3) and
that calibration techniques for B(Nt) are not yet vetted (PDF p. 7).

## Findings, graded (does any kill line move?)

NO kill line changes. NO new candidate sharpening. Default grade: the paper is a
construction-and-conjecture exhibit; nothing in it is validated to the standard the
programme would need before any of it could bind, and the standing rules already cover
its hazards.

1. [reinforcing, no new item] The event-clock reading is the paper's only live idea:
   price depends on trade arrivals, so a jump subordinator is a defensible
   construction and Var(B(Nt)) = E(Nt) makes volatility mechanical in the arrival
   count (PDF pp. 13-14). This is the same business-time/event-time family the
   flow-clock scale-constant sharpening (already in the ratification queue) covers;
   the paper's version adds no new mechanism and nothing is licensed into any spec.

2. [interpretation caution] The α/β stationarity remark is wrong-direction comfort:
   the authors say α < β "may not be necessary" (PDF p. 3), but α ≥ β drives the
   branching ratio to ≥ 1 and the intensity to a non-stationary or explosive regime
   in which long-horizon B(Nt) is ill-behaved; any future subordination-style
   construction the programme ever entertained must keep the stationarity condition
   live, never relaxed on the strength of a simulation-year horizon.

3. [interpretation caution] The Poisson-rejection evidence conflates two channels:
   the Q-Q plots (Figs. 6-7) reject exponential inter-arrivals, which rejects
   memorylessness, but the intraday volume profiles (Figs. 8-9) show midday/late-
   afternoon concentration, which is diurnal seasonality captured equally by a
   non-homogeneous Poisson process. Diurnal clustering is not self-excitation; a
   future arrival-process test must separate periodic intensity from genuine
   endogenous feedback or it will book seasonality as reflexivity.

4. [reinforcing, no new item] The fit evidence is eyeball-graded and uncosted: hand
   calibration by trial and error on in-sample distributions, no goodness-of-fit
   statistic, no out-of-sample window, a distributional form left as a conjecture,
   and simulation checks with systematic ±20% discrepancies the authors attribute to
   discretization (PDF pp. 7-9, 14-15). This corroborates the standing
   ammunition-not-evidence discipline: nothing here clears the floor, and the paper
   says nothing about any C1-L2 or C8 claim.

5. Vsource-quality note] arXiv v1 preprint, single-venue energy futures, daily
   closing prices (Marketwatch) for the fit years and 2024 minute bars only for the
   Q-Q plots, three-parameter hand fits across four one-year samples, generator
   derived under asserted (not proven) vanishing cross moments
   E(NtB(Nt)) = E(L݉Ф¡9Ф¤􀀰¥͑ɥՑ¥½¹°½ɴ½¹©ѕɕ°±¥Ʌѥ½¸(ѕ¡¹¥ŕၱ¥¥ѱ䁕¹ٕё쁩½Չ¹°ٕɍ¥½¸չ¡­Ёɕ¥¹¡չɑ¥¸°(±¤¸(§r## What this paper would have killed if we had done it wrong

Had the subordination idea been read forward as a working alternative clock for the
programme, an unvetted hand-calibrated fit with a conjectured distribution and a
relaxed stationarity condition would have been laundered into a validated
event-time instrument; had the Q-Q plots been booked as proof of self-excitation, a
diurnal seasonality pattern that any non-homogeneous Poisson model reproduces would
have entered the record as reflexivity evidence; and had the ±20% simulation
discrepancies been dropped, an Itô identity verified only to eyeball tolerance would
have been quoted as exact. Ammunition-not-evidence and the standing venue-transfer
ban prevented all three. Laundering directions named: INTO — nothing; no α, β, v
value, generator term, Itô identity or conjectured marginal from this paper enters
any spec, default, calibration, tolerance or null, and the variance-Hawkes process
may not serve as a simulator or null for any C1-L2 or C8 arm without an
owner-ratified pre-declared derivation of its assumptions on the programme's venue
and fields; OUT — never quote this paper as "energy futures are proved to follow a
Hawkes clock", and never cite the Q-Q figures as self-excitation evidence without
the diurnal-seasonality caveat.

## Standing caveat

Front-month energy futures only, one-year daily samples, hand fits without any
goodness-of-fit statistic, the key distributional claim unproven, generator cross
moments asserted rather than derived, simulations showing non-accumulating but
persistent percent errors, and the entire construction calibrated to nothing in the
programme's venue. Nothing measured here constrains any programme instrument.
