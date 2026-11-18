"""Compound Hawkes order-flow engine (synthetic, demonstration grade).

A 12-dimensional compound Hawkes point process driving a top-of-book
limit order book simulator, modelled on Jain, Firoozye, Kochems and
Treleaven, "Limit Order Book Dynamics and Order Size Modelling Using
Compound Hawkes Process" (arXiv:2312.08927v5). Differences from the
paper are deliberate and disclosed:

- Kernels are single exponentials phi_ji(t) = a_ji * exp(-b_ji * t),
  with b_ji heterogeneous across the 144 (j -> i) pairs (the paper
  fits power laws; exponential kernels keep the excitation bank exact
  under the discrete-time simulator).
- Stability is enforced by DISCLOSURE, not by silent repair. If the
  kernel-norm matrix violates the stationarity constraint the builder
  either raises (refuse=True) or rescales to a target and returns a
  disclosure record with the raw eigenvalue, the scaled eigenvalue and
  the applied factor. Nothing is capped quietly.
- Simulation is a discrete-time Bernoulli grid (dt), an Euler-type
  approximation of the continuous point process. The approximation
  requires peak intensity * dt < 1; simulate_day asserts this.

This module generates synthetic data only. It never touches programme
datasets and produces no evidence for any programme claim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Event dimensions (paper section 3.1 ordering, ask side first)
# ---------------------------------------------------------------------------

DIM_NAMES: Tuple[str, ...] = (
    "LO_ask_deep",   # 0  limit order, ask +1 tick
    "CO_ask_deep",   # 1  cancel, ask +1 tick
    "LO_ask_top",    # 2  limit order, best ask
    "CO_ask_top",    # 3  cancel, best ask
    "MO_ask_top",    # 4  market order, best ask
    "LO_ask_is",     # 5  limit order inside the spread (ask side)
    "LO_bid_is",     # 6  limit order inside the spread (bid side)
    "LO_bid_top",    # 7  limit order, best bid
    "CO_bid_top",    # 8  cancel, best bid
    "MO_bid_top",    # 9  market order, best bid
    "LO_bid_deep",   # 10 limit order, bid -1 tick
    "CO_bid_deep",   # 11 cancel, bid -1 tick
)

NDIM = 12
ASK_IS = 5   # dim indices whose intensity scales with the spread state
BID_IS = 6
MAX_LEVEL_JUMPS = 5  # deepest depletion a single market order can cause


# ---------------------------------------------------------------------------
# Stability with disclosure (the boundary-solution lesson as code)
# ---------------------------------------------------------------------------

def spectral_radius(M: np.ndarray) -> float:
    """Spectral radius of the kernel-norm matrix (assumed non-negative
    diagonal-dominant usage aside, this is max |eig|)."""
    eig = np.linalg.eigvals(np.asarray(M, dtype=float))
    return float(np.max(np.abs(eig)))


@dataclass
class StabilityDisclosure:
    """Record of any stability intervention. No silent capping, ever."""
    raw_rho: float
    threshold: float          # 1 / max TOD factor
    scaled_rho: Optional[float]
    factor: Optional[float]    # multiplicative factor applied to M (None if refused)
    action: str                # "none" | "rescaled_with_disclosure" | "refused"

    def as_dict(self) -> Dict:
        return {
            "raw_rho": self.raw_rho,
            "threshold": self.threshold,
            "scaled_rho": self.scaled_rho,
            "factor": self.factor,
            "action": self.action,
        }


def stabilize_norm_matrix(
    M: np.ndarray,
    max_tod_factor: float,
    target_rho: float = 0.85,
    refuse: bool = False,
) -> Tuple[np.ndarray, StabilityDisclosure]:
    """Return a stationary kernel-norm matrix plus a disclosure record.

    The stationary condition for the intensity system (paper eq. 21) is
    rho(M) < 1 / max_tod_factor. If M already satisfies it, it is
    returned unchanged (action "none"). Otherwise either raise
    (refuse=True) or rescale every kernel by a single factor so the
    constraint holds with margin, and record exactly what happened.
    """
    M = np.asarray(M, dtype=float)
    threshold = 1.0 / max_tod_factor
    raw_rho = spectral_radius(M)
    if raw_rho < threshold:
        return M.copy(), StabilityDisclosure(raw_rho, threshold, raw_rho, 1.0, "none")
    if refuse:
        raise ValueError(
            "kernel-norm matrix violates the stationarity constraint "
            f"(rho={raw_rho:.4f} >= {threshold:.4f}) and refuse=True; "
            "no silent rescale is permitted"
        )
    if not 0.0 < target_rho < 1.0:
        raise ValueError("target_rho must be in (0, 1)")
    factor = (target_rho * threshold) / raw_rho
    scaled = M * factor
    scaled_rho = spectral_radius(scaled)
    d = StabilityDisclosure(raw_rho, threshold, scaled_rho, factor, "rescaled_with_disclosure")
    assert scaled_rho < threshold, "rescale failed to stabilize"
    return scaled, d


# ---------------------------------------------------------------------------
# Time of day (paper Prop 2): separable U-shape multiplier, 13 bins
# ---------------------------------------------------------------------------

def u_shape(n_bins: int = 13) -> np.ndarray:
    """Classic U shape over the trading day, mean 1 by normalisation."""
    x = np.linspace(0.0, 1.0, n_bins)
    u = 0.55 + 1.9 * (x - 0.5) ** 2 * 4.0  # strong open/close lift
    return u / u.mean()


def build_tod_matrix(rng: np.random.Generator, n_bins: int = 13) -> np.ndarray:
    """Per-dimension time-of-day factors f_i(Qt), each mean 1, peak bounded."""
    base = np.tile(u_shape(n_bins), (NDIM, 1))
    noise = rng.uniform(0.85, 1.15, size=(NDIM, 1))
    F = base * noise
    F *= NDIM * 13.0 / F.sum() * 1.0  # keep overall scale sane
    # renormalise each row to mean 1 so the day average matches baselines
    F = (F.T / F.mean(axis=1)).T
    return F


# ---------------------------------------------------------------------------
# Order sizes (compound marks): geometric body + round-number spikes
# ---------------------------------------------------------------------------

ROUND_SIZES: Tuple[int, ...] = (1, 10, 50, 100, 200, 500)


@dataclass
class SizeSampler:
    """Order-size distribution: geometric body, Dirac spikes at round
    numbers (paper section 4.3, following Lu & Abergel 2018a)."""

    p_body: float                       # geometric success parameter
    spike_weight: float                 # total probability mass on round sizes
    spike_probs: np.ndarray             # per-round-number weights (sums to 1)
    max_size: int = 5000
    rng: np.random.Generator = field(default_factory=lambda: np.random.default_rng(0))

    def __post_init__(self) -> None:
        if not (0.0 < self.p_body <= 1.0):
            raise ValueError("p_body must be in (0, 1]")
        if not 0.0 <= self.spike_weight < 1.0:
            raise ValueError("spike_weight must be in [0, 1)")
        if not np.isclose(self.spike_probs.sum(), 1.0, atol=1e-9):
            raise ValueError("spike_probs must sum to 1")

    def sample(self, n: int) -> np.ndarray:
        if n <= 0:
            return np.empty(0, dtype=int)
        rng = self.rng
        use_spike = rng.random(n) < self.spike_weight
        body = rng.geometric(self.p_body, size=n)
        body = np.minimum(body, self.max_size)
        which = rng.choice(len(ROUND_SIZES), size=n, p=self.spike_probs)
        spikes = np.asarray(ROUND_SIZES, dtype=int)[which]
        out = np.where(use_spike, spikes, body)
        return out.astype(int)

    def mean(self) -> float:
        body_mean = min(1.0 / self.p_body, self.max_size)
        spike_mean = float(np.dot(self.spike_probs, np.asarray(ROUND_SIZES, dtype=float)))
        return (1 - self.spike_weight) * body_mean + self.spike_weight * spike_mean


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class BookState:
    """Top-of-book state; prices in integer ticks."""
    ask: int
    bid: int
    q_ask_top: int
    q_ask_deep: int
    q_bid_top: int
    q_bid_deep: int

    def spread(self) -> int:
        return self.ask - self.bid


@dataclass
class Config:
    mu: np.ndarray                       # (12,) exogenous intensities, /s
    amp: np.ndarray                      # (12,12) kernel amplitudes a_ji (signed)
    dec: np.ndarray                       # (12,12) kernel decays b_ji > 0
    tod: np.ndarray                       # (12,13) time-of-day factors, mean 1
    beta_spread: float                    # in-spread intensity exponent on (s-1)
    size_samplers: Sequence[SizeSampler]  # one per dim
    replenish_sampler: SizeSampler       # unknown queues revealed on widening
    init_book: BookState
    horizon_s: float = 6.5 * 3600.0
    dt: float = 0.05                      # simulation grid, seconds
    seed: int = 7
    max_intensity_per_dt: float = 0.9     # Bernoulli-grid validity cap

    def __post_init__(self) -> None:
        self.mu = np.asarray(self.mu, dtype=float)
        self.amp = np.asarray(self.amp, dtype=float)
        self.dec = np.asarray(self.dec, dtype=float)
        self.tod = np.asarray(self.tod, dtype=float)
        if self.mu.shape != (NDIM,):
            raise ValueError(f"mu must be ({NDIM},)")
        if self.amp.shape != (NDIM, NDIM) or self.dec.shape != (NDIM, NDIM):
            raise ValueError(f"amp/dec must be ({NDIM},{NDIM})")
        if np.any(self.dec <= 0):
            raise ValueError("all kernel decays must be positive")
        if np.any(np.diagonal(self.amp) < 0):
            raise ValueError("self-excitation diagonals must be >= 0 (signed kernels)")
        if self.beta_spread <= 0:
            raise ValueError("beta_spread must be > 0")

    def norm_matrix(self) -> np.ndarray:
        """Kernel-norm matrix M_ij = integral of phi_ji = a_ji / b_ji."""
        return self.amp / self.dec

    def max_tod_factor(self) -> float:
        return float(self.tod.max())


# ---------------------------------------------------------------------------
# Limit order book with mechanical constraints (paper Prop 1)
# ---------------------------------------------------------------------------

class OrderBook:
    """Six-queue top-of-book with paper-style mechanical transitions.

    Invariants, asserted after every event:
    - spread >= 1 tick, always;
    - all queue sizes >= 0;
    - in-spread levels carry no queue (orders there create a new best).
    """

    def __init__(self, state: BookState, replenish: SizeSampler,
                 rng: np.random.Generator) -> None:
        self.ask = state.ask
        self.bid = state.bid
        self.q_ask_top = int(state.q_ask_top)
        self.q_ask_deep = int(state.q_ask_deep)
        self.q_bid_top = int(state.q_bid_top)
        self.q_bid_deep = int(state.q_bid_deep)
        self._replenish = replenish
        self._rng = rng

    # -- helpers ------------------------------------------------------------

    def spread(self) -> int:
        return self.ask - self.bid

    def mid(self) -> float:
        return (self.ask + self.bid) / 2.0

    def _replenish_queue(self) -> int:
        return max(int(self._replenish.sample(1)[0]), 1)

    def _check_invariants(self) -> None:
        assert self.ask - self.bid >= 1, "spread below one tick"
        assert min(self.q_ask_top, self.q_ask_deep, self.q_bid_top,
                   self.q_bid_deep) >= 0, "negative queue"

    # -- events -------------------------------------------------------------

    def apply(self, dim: int, size: int) -> int:
        """Apply one event; return the mid-price change in ticks (signed)."""
        mid0 = self.mid()
        if dim == 0:    # LO ask deep
            self.q_ask_deep += size
        elif dim == 1:  # CO ask deep
            self.q_ask_deep -= min(size, self.q_ask_deep)
        elif dim == 2:  # LO ask top
            self.q_ask_top += size
        elif dim == 3:  # CO ask top
            self.q_ask_top -= min(size, self.q_ask_top)
            if self.q_ask_top == 0:
                self._walk_ask()
        elif dim == 4:  # MO ask top: consume, possibly multiple levels
            rem = size
            for _ in range(MAX_LEVEL_JUMPS):
                take = min(rem, self.q_ask_top)
                self.q_ask_top -= take
                rem -= take
                if self.q_ask_top == 0:
                    # queue-depletion: the best ask quote is empty, walk up
                    self._walk_ask()
                if rem <= 0:
                    break
        elif dim == 5:  # LO ask in-spread: new best ask one tick lower
            assert self.spread() >= 2, "in-spread event at one-tick spread"
            self.ask -= 1
            self.q_ask_deep = self.q_ask_top
            self.q_ask_top = max(size, 1)
        elif dim == 6:  # LO bid in-spread: new best bid one tick higher
            assert self.spread() >= 2, "in-spread event at one-tick spread"
            self.bid += 1
            self.q_bid_deep = self.q_bid_top
            self.q_bid_top = max(size, 1)
        elif dim == 7:  # LO bid top
            self.q_bid_top += size
        elif dim == 8:  # CO bid top
            self.q_bid_top -= min(size, self.q_bid_top)
            if self.q_bid_top == 0:
                self._walk_bid()
        elif dim == 9:  # MO bid top
            rem = size
            for _ in range(MAX_LEVEL_JUMPS):
                take = min(rem, self.q_bid_top)
                self.q_bid_top -= take
                rem -= take
                if self.q_bid_top == 0:
                    self._walk_bid()
                if rem <= 0:
                    break
        elif dim == 10:  # LO bid deep
            self.q_bid_deep += size
        elif dim == 11:  # CO bid deep
            self.q_bid_deep -= min(size, self.q_bid_deep)
        else:
            raise ValueError(f"unknown dim {dim}")
        self._check_invariants()
        return int(round((self.mid() - mid0) * 2))  # half-tick units as ints

    def _walk_ask(self) -> None:
        # best ask queue depleted: ask moves up one tick; the old deep
        # level (possibly empty) is revealed and a new deep queue sampled
        self.ask += 1
        self.q_ask_top = self.q_ask_deep
        self.q_ask_deep = self._replenish_queue()
        while self.q_ask_top == 0:
            self.ask += 1
            self.q_ask_top = self.q_ask_deep
            self.q_ask_deep = self._replenish_queue()

    def _walk_bid(self) -> None:
        self.bid -= 1
        self.q_bid_top = self.q_bid_deep
        self.q_bid_deep = self._replenish_queue()
        while self.q_bid_top == 0:
            self.bid -= 1
            self.q_bid_top = self.q_bid_deep
            self.q_bid_deep = self._replenish_queue()


# ---------------------------------------------------------------------------
# Simulator
# ---------------------------------------------------------------------------

@dataclass
class DayResult:
    events_t: np.ndarray        # (N,) seconds
    events_dim: np.ndarray      # (N,) dimension index
    events_size: np.ndarray     # (N,) order size in shares
    mid_t: np.ndarray           # (T,) sampled mid, 1 per second
    mid: np.ndarray              # (T,) mid in half-ticks (ints)
    spread_t: np.ndarray
    spread: np.ndarray
    book_t: np.ndarray          # sample times for the book snapshot
    q_ask_top: np.ndarray
    q_ask_deep: np.ndarray
    q_bid_top: np.ndarray
    q_bid_deep: np.ndarray
    exog_mass: np.ndarray        # sampled intensity decomposition (share)
    endog_share: np.ndarray
    peak_intensity: float
    gross_exog: float
    gross_total: float


def simulate_day(cfg: Config, day_index: int = 0) -> DayResult:
    """One trading day on the Bernoulli grid with an exact excitation bank.

    The excitation bank A[j, i] holds the surviving excitation of dim j's
    past events on dim i: between grid steps A *= exp(-b_ji * dt), and an
    event in dim j adds amp[j, :] to A[j, :]. Intensity uses max(0, mu +
    sum_j A[j, :]) so inhibitory kernels floor at zero, per paper Prop 3.
    """
    rng = np.random.default_rng(cfg.seed * 100003 + day_index)
    n_steps = int(round(cfg.horizon_s / cfg.dt))
    decay = np.exp(-cfg.dec * cfg.dt)                # (12,12)
    A = np.zeros((NDIM, NDIM))
    book = OrderBook(cfg.init_book, cfg.replenish_sampler,
                    np.random.default_rng(cfg.seed * 7 + day_index + 1))

    # samplers get their own streams for reproducibility
    samplers = []
    for s in cfg.size_samplers:
        ss = SizeSampler(s.p_body, s.spike_weight, s.spike_probs, s.max_size)
        ss.rng = np.random.default_rng(cfg.seed * 31 + hash(str(s.p_body)) % 997 + day_index)
        samplers.append(ss)

    ev_t: List[float] = []
    ev_dim: List[int] = []
    ev_size: List[int] = []

    # sampled outputs
    sec_steps = int(round(1.0 / cfg.dt))
    n_sec = int(cfg.horizon_s)
    mid_out = np.empty(n_sec)
    spread_out = np.empty(n_sec)
    book_every = 5                                   # seconds between book snapshots
    n_book = n_sec // book_every + 1
    qat = np.empty(n_book); qad = np.empty(n_book)
    qbt = np.empty(n_book); qbd = np.empty(n_book)
    book_t_out = np.arange(n_book) * book_every
    share_every = 30                                 # seconds between intensity share samples
    n_share = n_sec // share_every + 1
    exog_mass = np.empty(n_share); endog_share = np.empty(n_share)

    peak_intensity = 0.0
    tot_exog = 0.0
    tot_total = 0.0
    fires = np.empty(NDIM)
    sizes_buf: Dict[int, List[int]] = {d: [] for d in range(NDIM)}

    t = cfg.dt
    sec_idx = 0
    book_idx = 0
    share_idx = 0
    b_sq = float(cfg.beta_spread)

    for step in range(n_steps):
        # time-of-day bin (13 x 30 min)
        frac = t / cfg.horizon_s
        bin_ = min(int(frac * 13), 12)
        f = cfg.tod[:, bin_]

        A *= decay
        raw = cfg.mu + A.sum(axis=0)          # (12,) excitation bank sums
        lam = f * np.maximum(raw, 0.0)
        s = book.spread()
        spread_fac = (s - 1) ** b_sq if s > 1 else 0.0
        lam[ASK_IS] *= spread_fac
        lam[BID_IS] *= spread_fac

        haz = lam * cfg.dt
        peak_intensity = max(peak_intensity, float(lam.max()))
        if float(haz.max()) > cfg.max_intensity_per_dt:
            raise RuntimeError(
                f"Bernoulli grid violated: peak hazard {haz.max():.3f} > "
                f"{cfg.max_intensity_per_dt}; reduce dt or intensities"
            )

        u = rng.random(NDIM)
        fires = u < haz
        if fires.any():
            for d in np.flatnonzero(fires):
                size = int(samplers[d].sample(1)[0])
                # rejection guard: in-spread orders cannot fire at one-tick spread
                if (d == ASK_IS or d == BID_IS) and book.spread() < 2:
                    continue
                ev_t.append(t)
                ev_dim.append(int(d))
                ev_size.append(size)
                book.apply(int(d), size)
                A[d, :] += cfg.amp[d, :]
        # endogenous-share accounting: each dim's floored intensity is
        # attributed between exogenous base and excitation PROPORTIONALLY
        # (mu/raw, clipped to [0,1]); under zero excitation the share is
        # exactly zero. This is the declared attribution convention.
        frac_ex = np.clip(np.divide(cfg.mu, raw, out=np.zeros(NDIM), where=raw > 0),
                          0.0, 1.0)
        ex_step = float(np.dot(lam, frac_ex))
        tot_exog += ex_step * cfg.dt
        tot_total += float(lam.sum()) * cfg.dt

        # sampled outputs at second boundaries
        if (step + 1) % sec_steps == 0 and sec_idx < n_sec:
            mid_out[sec_idx] = book.mid()
            spread_out[sec_idx] = book.spread()
            sec_idx += 1
        if book_idx < n_book and (step + 1) * cfg.dt >= float(book_t_out[book_idx]):
            qat[book_idx] = book.q_ask_top
            qad[book_idx] = book.q_ask_deep
            qbt[book_idx] = book.q_bid_top
            qbd[book_idx] = book.q_bid_deep
            book_idx += 1
        if share_idx < n_share and (step + 1) * cfg.dt >= float(share_idx * share_every):
            tot_now = float(lam.sum())
            exog_mass[share_idx] = ex_step
            endog_share[share_idx] = 0.0 if tot_now <= 0 else 1.0 - ex_step / tot_now
            share_idx += 1
        t += cfg.dt

    # flush any unsampled book slots with final state
    if book_idx < n_book:
        qat[book_idx:] = book.q_ask_top
        qad[book_idx:] = book.q_ask_deep
        qbt[book_idx:] = book.q_bid_top
        qbd[book_idx:] = book.q_bid_deep
    if share_idx < n_share:
        exog_mass[share_idx:] = exog_mass[share_idx - 1] if share_idx > 0 else 0.0
        endog_share[share_idx:] = 0.0

    return DayResult(
        events_t=np.asarray(ev_t),
        events_dim=np.asarray(ev_dim, dtype=np.int16),
        events_size=np.asarray(ev_size, dtype=np.int32),
        mid_t=np.arange(n_sec, dtype=float),
        mid=np.round(mid_out * 2).astype(np.int32),
        spread_t=np.arange(n_sec, dtype=float),
        spread=spread_out.astype(np.int16),
        book_t=book_t_out,
        q_ask_top=qat.astype(np.int32),
        q_ask_deep=qad.astype(np.int32),
        q_bid_top=qbt.astype(np.int32),
        q_bid_deep=qbd.astype(np.int32),
        exog_mass=exog_mass,
        endog_share=endog_share,
        peak_intensity=peak_intensity,
        gross_exog=tot_exog,
        gross_total=tot_total,
    )


# ---------------------------------------------------------------------------
# Baseline: same book mechanics, no self-excitation (Poisson control)
# ---------------------------------------------------------------------------

def simulate_poisson_day(cfg: Config, day_index: int = 0) -> DayResult:
    """Poisson control: identical seeds, book, sizes and TOD conditioning,
    zero excitation. Used to show what the Hawkes memory contributes."""
    zero = Config(
        mu=cfg.mu.copy(),
        amp=np.zeros_like(cfg.amp),
        dec=cfg.dec.copy(),
        tod=cfg.tod.copy(),
        beta_spread=cfg.beta_spread,
        size_samplers=cfg.size_samplers,
        replenish_sampler=cfg.replenish_sampler,
        init_book=cfg.init_book,
        horizon_s=cfg.horizon_s,
        dt=cfg.dt,
        seed=cfg.seed,
    )
    return simulate_day(zero, day_index)


# ---------------------------------------------------------------------------
# Builder: a realistic, intentionally self-exciting configuration
# ---------------------------------------------------------------------------

def build_config(seed: int = 20261118, target_rho: float = 0.82,
                 horizon_s: float = 6.5 * 3600.0) -> Tuple[Config, StabilityDisclosure]:
    """Construct a medium-tick-style configuration with named structure.

    Mechanisms planted (each motivates its kernel sign):
    - MO -> MO same side: trades cluster (momentum bursts).
    - MO -> LO same side: liquidity reacts to trades, with a lag.
    - LO -> CO same queue: resting liquidity attracts cancels.
    - LO in-spread both sides: competition to improve price is mutual.
    - CO top -> LO in-spread same side: vanishing best invites improvement.
    - MO ask -> CO bid top (inhibition): one side's aggression quiets
      the other's cancel flow (inventory caution).
    """
    rng = np.random.default_rng(seed)
    mu = np.zeros(NDIM)
    mu[0] = 0.35   # LO ask deep
    mu[1] = 0.22   # CO ask deep
    mu[2] = 1.20   # LO ask top
    mu[3] = 0.85   # CO ask top
    mu[4] = 0.55   # MO ask top
    mu[5] = 0.30   # LO ask in-spread
    mu[6] = 0.30   # LO bid in-spread
    mu[7] = 1.20   # LO bid top
    mu[8] = 0.85   # CO bid top
    mu[9] = 0.55   # MO bid top
    mu[10] = 0.35  # LO bid deep
    mu[11] = 0.22  # CO bid deep

    # decays b_ji: heterogeneous multi-timescale memory (per second)
    dec = rng.uniform(0.6, 6.0, size=(NDIM, NDIM))
    np.fill_diagonal(dec, rng.uniform(1.5, 3.0, size=NDIM))

    amp = np.zeros((NDIM, NDIM))
    def set_a(j: int, i: int, val: float) -> None:
        amp[j, i] = val

    # market orders self-excite and excite same-side top liquidity and cancels
    for mo, lo_top, co_top, lo_is, other_co in ((4, 2, 3, 5, 8), (9, 7, 8, 6, 3)):
        set_a(mo, mo, 1.05)      # trade clustering
        set_a(mo, lo_top, 0.55)  # liquidity replenishment after trades
        set_a(mo, co_top, 0.30)  # cancels follow trades
        set_a(mo, lo_is, 0.42)   # price improvement attempts after trades
        set_a(mo, other_co, -0.22)  # inhibition: quiets the other side's cancels
    # resting liquidity attracts cancels; top flow draws deep flow
    for lo_top, co_top, lo_deep, co_deep, is_ in ((2, 3, 0, 1, 5), (7, 8, 10, 11, 6)):
        set_a(lo_top, co_top, 0.50)
        set_a(co_top, lo_is, 0.45)   # empty best invites improvement
        set_a(lo_top, lo_deep, 0.25)
        set_a(lo_deep, co_deep, 0.18)
        set_a(lo_top, lo_top, 0.30)
    # in-spread competition is mutual on both sides (cross-talk)
    set_a(5, 6, 0.35)
    set_a(6, 5, 0.35)
    # deep cancels inhibit deep liquidity arrival (adverse selection)
    set_a(1, 0, -0.12)
    set_a(11, 10, -0.12)

    M = amp / dec
    tod = build_tod_matrix(rng)
    max_f = float(tod.max())
    M, disc = stabilize_norm_matrix(M, max_f, target_rho=target_rho, refuse=False)
    # rescale amps to match the (disclosed) norm matrix adjustment
    amp = M * dec

    # order sizes
    def mk(body_p: float, spike_w: float, sseed: int) -> SizeSampler:
        w = np.array([0.42, 0.18, 0.14, 0.16, 0.07, 0.03])
        return SizeSampler(p_body=body_p, spike_weight=spike_w,
                           spike_probs=w / w.sum(),
                           rng=np.random.default_rng(sseed))

    samplers = [
        mk(0.010, 0.34, 101),  # LO ask deep  (avg body ~100 with cap)
        mk(0.020, 0.30, 102),  # CO ask deep
        mk(0.014, 0.36, 103),  # LO ask top
        mk(0.025, 0.32, 104),  # CO ask top
        mk(0.006, 0.42, 105),  # MO ask top (bigger)
        mk(0.020, 0.35, 106),  # LO ask in-spread
        mk(0.020, 0.35, 107),  # LO bid in-spread
        mk(0.014, 0.36, 108),  # LO bid top
        mk(0.025, 0.32, 109),  # CO bid top
        mk(0.006, 0.42, 110),  # MO bid top
        mk(0.010, 0.34, 111),  # LO bid deep
        mk(0.020, 0.30, 112),  # CO bid deep
    ]
    replenish = mk(0.012, 0.30, 999)

    init = BookState(ask=1_000_000, bid=999_998, q_ask_top=480, q_ask_deep=950,
                     q_bid_top=450, q_bid_deep=900)
    cfg = Config(mu=mu, amp=amp, dec=dec, tod=tod, beta_spread=0.75,
                size_samplers=samplers, replenish_sampler=replenish,
                init_book=init, horizon_s=horizon_s, dt=0.05, seed=seed)
    return cfg, disc


# ---------------------------------------------------------------------------
# Analytics (descriptive statistics of the synthetic stream)
# ---------------------------------------------------------------------------

def signature_plot(mid_half_ticks: np.ndarray, day_id: List[np.ndarray],
                   scales: Sequence[int] = (1, 2, 5, 10, 30, 60, 120, 300)
                   ) -> Tuple[List[int], List[float]]:
    """Realised volatility (per sqrt-second) at each sampling scale, with
    day boundaries respected (no cross-day returns)."""
    vols: List[float] = []
    for k in scales:
        sq_sum = 0.0
        n_ret = 0
        for seg in day_id:
            arr = mid_half_ticks[seg].astype(float) / 2.0
            r = np.diff(arr[::k])
            sq_sum += float(np.dot(r, r))
            n_ret += len(r)
        vols.append(math.sqrt(sq_sum / max(n_ret, 1)))
    return list(scales), vols


def abs_returns_acf(mid_half_ticks: np.ndarray, max_lag: int = 120) -> np.ndarray:
    r = np.abs(np.diff(mid_half_ticks.astype(float) / 2.0))
    r = r - r.mean()
    n = len(r)
    denom = float(np.dot(r, r))
    acf = np.array([np.dot(r[: n - k], r[k:]) / denom for k in range(1, max_lag + 1)])
    return acf


def interarrival_histograms(day: DayResult, dims: Sequence[int],
                             n_bins: int = 50) -> Dict[int, Dict]:
    out: Dict[int, Dict] = {}
    for d in dims:
        t = day.events_t[day.events_dim == d]
        if len(t) < 20:
            continue
        gaps = np.diff(np.sort(t))
        gaps = gaps[gaps > 0]
        if len(gaps) == 0:
            continue
        lo, hi = np.log10(gaps.min()), np.log10(gaps.max()) if gaps.max() > gaps.min() else np.log10(gaps.min() + 1e-6)
        if hi <= lo:
            hi = lo + 0.1
        bins = np.logspace(lo, hi, n_bins + 1)
        counts, edges = np.histogram(gaps, bins=bins)
        out[d] = {
            "rate": float(len(gaps) / (day.events_t.max() - day.events_t.min() or 1.0)),
            "counts": counts.tolist(),
            "edges": edges.tolist(),
        }
    return out


def size_histograms(days: Sequence[DayResult], groups: Dict[str, Sequence[int]],
                    max_size: int = 600) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    for name, dims in groups.items():
        sizes = np.concatenate([d.events_size[np.isin(d.events_dim, list(dims))]
                                for d in days]) if days else np.empty(0)
        counts, edges = np.histogram(sizes, bins=np.arange(1, max_size + 2))
        out[name] = {
            "counts": counts.tolist(),
            "mean": float(sizes.mean()) if len(sizes) else 0.0,
            "n": int(len(sizes)),
            "spike_mass": float(np.mean(np.isin(sizes, ROUND_SIZES))) if len(sizes) else 0.0,
        }
    return out
