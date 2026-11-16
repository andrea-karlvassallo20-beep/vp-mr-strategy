# Math cheatsheet: the library as code

The formula from the paper, immediately followed by the optimized
Python function that executes it. No PDFs required. All functions are
numpy-vectorized and depend only on `numpy`.

---

## 1. Cont, Kukanov, Stoikov (2014) — "The Price Impact of Order Book Events"

### 1a. Order flow imbalance at the best quotes (OFI)

Let $P^b_n, q^b_n$ be the best bid price and size after the $n$-th book
event, $P^a_n, q^a_n$ the best ask. Define $\Delta P^b_n = P^b_n - P^b_{n-1}$,
$\Delta q^b_n = q^b_n - q^b_{n-1}$, and likewise for the ask. The paper
(Eq. 2.2-2.4) defines the order flow at the top of book:

$$e^b_n = \Delta q^b_n \cdot \mathbb{1}\{\Delta P^b_n > 0\}
       + (\Delta q^b_n)^{+} \cdot \mathbb{1}\{\Delta P^b_n = 0\}
       - q^b_{n-1} \cdot \mathbb{1}\{\Delta P^b_n < 0\}$$

$$e^a_n = -q^a_{n-1} \cdot \mathbb{1}\{\Delta P^a_n > 0\}
       + (-\Delta q^a_n)^{+} \cdot \mathbb{1}\{\Delta P^a_n = 0\}
       + \Delta q^a_n \cdot \mathbb{1}\{\Delta P^a_n < 0\}$$

$$e_n = e^b_n - e^a_n$$

```python
import numpy as np

def ofi_top_level(pb, qb, pa, qa):
    """Cont-Kukanov-Stoikov OFI at the best quotes.

    pb, qb: (T,) best bid price and size after each book event
    pa, qa: (T,) best ask price and size after each book event
    Returns e: (T-1,) order flow per event.
    """
    d_pb, d_qb = np.diff(pb), np.diff(qb)
    d_pa, d_qa = np.diff(pa), np.diff(qa)
    qb_prev, qa_prev = qb[:-1], qa[:-1]

    e_b = (np.where(d_pb > 0, d_qb, 0.0)          # bid price improved: size change
           + np.where(d_pb == 0, np.maximum(d_qb, 0.0), 0.0)  # same price: added liquidity
           - np.where(d_pb < 0, qb_prev, 0.0))     # bid price dropped: old size withdrawn
    e_a = (- np.where(d_pa > 0, qa_prev, 0.0)      # ask price up: old size withdrawn
           + np.where(d_pa == 0, np.maximum(-d_qa, 0.0), 0.0)  # same price: added liquidity
           + np.where(d_pa < 0, d_qa, 0.0))        # ask price down: size change
    return e_b - e_a
```

### 1b. Integrated OFI and the linear impact regression

The paper aggregates OFI over a window $W$ and regresses the
mid-price change on it (Eq. 2.6 and Sec. 3.1):

$$e_W = \sum_{n \in W} e_n, \qquad
\delta P_W = \lambda \, e_W + \varepsilon_W, \qquad
\hat\lambda = \frac{\sum_W e_n \, \delta P_n}{\sum_W e_n^2}$$

```python
def integrated_ofi_impact(e, mid, window):
    """Integrated OFI per window and the OLS impact coefficient lambda.

    e: (T,) per-event OFI; mid: (T,) mid-price; window: int events per window.
    Returns (e_W, delta_P, lambda_hat): integrated OFI, mid-price change,
    and impact coefficient per window.
    """
    n_win = len(e) // window
    e_w = e[:n_win * window].reshape(n_win, window).sum(axis=1)
    d_mid = mid[window::window][:n_win] - mid[:n_win * window:window]
    lambda_hat = (e_w * d_mid).sum() / (e_w ** 2).sum()
    return e_w, d_mid, lambda_hat
```

### 1c. Multi-level OFI (the Q-matrix projection)

In Appendix B3 the paper extends OFI to $K$ deeper levels: apply the
same event decomposition at each level to get per-level imbalances
$e^{(i)}_n$, then regress the mid-price change on all of them
simultaneously (their regressions 8a-8c):

$$\delta P_n = \sum_{i=1}^{K} \beta_i \, e^{(i)}_n + \varepsilon_n, \qquad
\hat\beta = (E^\top E)^{-1} E^\top \, \delta P$$

where $E$ is the $(T \times K)$ matrix of per-level OFIs. The fitted
$\hat\beta$ are the level weights; the scalar multi-level OFI is
$\tilde e_n = \sum_i \hat\beta_i e^{(i)}_n$. The paper's finding:
deeper levels add only marginal explanatory power beyond the best
quotes.

```python
def multi_level_ofi_weights(e_levels, d_mid):
    """OLS weights of per-level OFIs for mid-price change (CKS App. B3).

    e_levels: (T, K) OFI at each of K book levels (level 1 = best).
    d_mid: (T,) contemporaneous mid-price changes.
    Returns beta: (K,) level weights.
    """
    return np.linalg.lstsq(e_levels, d_mid, rcond=None)[0]

def multi_level_ofi(e_levels, beta):
    """Scalar multi-level OFI: weighted sum of per-level OFIs.

    e_levels: (T, K) per-level OFI; beta: (K,) OLS weights.
    Returns tilde_e: (T,) scalar multi-level OFI.
    """
    return e_levels @ beta
```

---

## 2. Filimonov, Sornette (2012, 2014) — Hawkes endogeneity of markets

### 2a. The Hawkes intensity with exponential kernel

Events $\{t_i\}$ arrive with conditional intensity (their Eq. 1-2):

$$\lambda(t) = \mu + \sum_{t_i < t} \varphi(t - t_i), \qquad
\varphi(t) = n_c \, \beta \, e^{-\beta t}, \qquad n_c \in [0, 1)$$

$n_c$ is the branching ratio: the average number of offspring events
per event, i.e. the fraction of endogenously triggered activity. The
stationary (mean) intensity is:

$$\bar\lambda = \frac{\mu}{1 - n_c}$$

so the branching ratio is recovered from the fitted parameters as
$n_c = 1 - \mu / \bar\lambda$. $n_c \to 1$ means the market is almost
entirely self-exciting (reflexive).

### 2b. Maximum-likelihood estimation

The log-likelihood of the observed points on $[0, T]$

$$\log L = \sum_{i=1}^{N} \log \lambda(t_i) - \int_0^T \lambda(t)\, dt
= \sum_{i=1}^{N} \log \lambda(t_i) - \mu T - n_c \sum_{i=1}^{N} \big(1 - e^{-\beta (T - t_i)}\big)$$

is computed in $O(N)$ with the Ozaki-style recursion instead of the
naive $O(N^2)$ double sum:

$$R_i = e^{-\beta (t_i - t_{i-1})} (1 + R_{i-1}), \qquad
\lambda(t_i) = \mu + n_c \beta R_i, \qquad R_0 = 0$$

```python
import numpy as np

def _hawkes_ll(theta, t):
    """Negative log-likelihood of a 1D Hawkes process, exponential kernel.

    theta: (mu, n_c, beta); t: (N,) sorted event times on [0, T].
        lambda(t) = mu + sum_{t_i<t} n_c * beta * exp(-beta (t - t_i))
    """
    mu, n_c, beta = theta
    if mu <= 0 or not 0 <= n_c < 1 or beta <= 0:
        return np.inf
    dt = np.diff(t)
    R = np.empty(len(t))
    R[0] = 0.0
    decay = np.exp(-beta * dt)
    for i in range(1, len(t)):          # O(N) Ozaki recursion
        R[i] = decay[i - 1] * (1.0 + R[i - 1])
    lam = mu + n_c * beta * R
    T = t[-1]
    integral = mu * T + n_c * np.sum(1.0 - np.exp(-beta * (T - t)))
    return -(np.sum(np.log(lam)) - integral)

def fit_hawkes(t, x0=(1.0, 0.5, 1.0)):
    """MLE fit of (mu, n_c, beta) via scipy; returns theta and branching ratio.

    t: (N,) sorted event times (e.g. trade times in seconds).
    """
    from scipy.optimize import minimize
    res = minimize(_hawkes_ll, x0, args=(t,), method="Nelder-Mead",
                   options={"xatol": 1e-8, "fatol": 1e-8, "maxiter": 5000})
    mu, n_c, beta = res.x
    lam_bar = mu / (1.0 - n_c)           # stationary intensity
    return res.x, 1.0 - mu / lam_bar     # == n_c by construction
```

The branching ratio `n_c` is the Filimonov-Sornette endogeneity
metric: fit it on trade times in a window and track it over time.

---

## 3. Lopez de Prado (2018) — Combinatorial Purged Cross-Validation (CPCV)

*Advances in Financial Machine Learning*, ch. 7. Walk-forward tests a
single path; CPCV builds many backtest paths from one history.

### 3a. The combinatorial split

Partition $T$ observations into $N$ groups **without shuffling**;
choose $k$ of them as the test set. The number of train/test
combinations is:

$$\phi = \binom{N}{k}$$

Each combination trains on $T(1 - k/N)$ observations and tests on
$Tk/N$. Each group is tested in exactly $\binom{N-1}{k-1}$
combinations, and the per-group test predictions can be stitched into

$$\text{paths} = \frac{k}{N} \binom{N}{k}$$

full backtest paths over the whole dataset.

### 3b. Purging and embargo

Let each training label $y_j$ depend on information over
$[t_j, t_j^{end}]$ (e.g. a forward-return label). Purging removes from
the train set every observation whose label span overlaps the test
label span; the embargo additionally removes training observations in
the window of length $h$ **following** the test set, because of
leakage from serial correlation:

$$\text{train} = \{j : [t_j, t_j^{end}] \cap [t^{test}_{start}, t^{test}_{end}] = \emptyset\}
\setminus \{j : t_j \in (t^{test}_{end}, t^{test}_{end} + h]\}$$

```python
import numpy as np
from itertools import combinations

def cpcv_splits(n_groups, k_test):
    """All CPCV combinations: phi = C(N, k) splits.

    Returns a list of (test_groups, train_groups) index tuples.
    """
    phi = list(combinations(range(n_groups), k_test))
    return [(test, tuple(g for g in range(n_groups) if g not in test))
            for test in phi]

def purge_and_embargo(test_idx, label_start, label_end, embargo_h):
    """Purged, embargoed train mask for one CPCV test fold.

    test_idx: (m,) observation indices in the test group.
    label_start, label_end: (T,) start/end times of each label's span.
    embargo_h: embargo duration (same time units as the label spans).
    Returns a boolean (T,) mask: True = keep in training set.
    """
    T = len(label_start)
    ts_min, te_max = label_start[test_idx].min(), label_end[test_idx].max()
    keep = np.ones(T, dtype=bool)
    keep[test_idx] = False
    # a train label overlaps the test span if its interval intersects it
    overlaps_test = (label_start <= te_max) & (label_end >= ts_min)
    keep &= ~overlaps_test
    embargoed = (label_start > te_max) & (label_start <= te_max + embargo_h)
    keep &= ~embargoed
    return keep
```

Usage for the C1-L2 pipeline: build label spans from the holding period,
partition the era timeline into $N$ groups (no shuffling), enumerate the
$\binom{N}{k}$ splits, purge + embargo each train set, fit per split,
stitch the $k\binom{N-1}{k-1}$ test predictions into
$\frac{k}{N}\binom{N}{k}$ full backtest paths, and take the distribution
of per-path performance as the honest answer.

---

## 4. Kyle's Lambda (market depth / price impact)

Kyle (1985), "Continuous Auctions and Insider Trading": in
equilibrium, the market maker sets price as a linear function of
aggregate order flow, and the coefficient is the market's depth
parameter. The price impact regression form used empirically (and
the bridge to CKS's OFI slope) is:

$$\Delta P_t = \lambda\, q_t + \epsilon_t, \qquad
\hat\lambda = \frac{\operatorname{Cov}(\Delta P, q)}{\operatorname{Var}(q)}
= \frac{\sum_t q_t\, \Delta P_t}{\sum_t q_t^2}, \qquad
\text{depth} \propto \frac{1}{\lambda}$$

where $q_t$ is signed order flow (signed volume, or signed OFI).
Kyle's equilibrium value for a Gaussian setup is
$\lambda = \frac{2\sigma_u}{\Sigma}$ ($\sigma_u$ noise-trade rate,
$\Sigma$ informed-trader precision), tying depth to adverse
selection: the more private information, the steeper the impact.
Amihud's illiquidity $|r_t|/\text{volume}_t$ is its per-period cousin.

**Verify against library source before production** (paywalled;
synthesized from LLM internal knowledge).

```python
def kyle_lambda(d_mid, signed_flow):
    """Kyle's lambda: OLS slope of mid-price change on signed flow.

    d_mid: (T,) mid-price changes per interval.
    signed_flow: (T,) signed volume or signed OFI over the same intervals.
    Returns lambda_hat: price impact per unit of flow (depth ~ 1/lambda).
    """
    denom = (signed_flow ** 2).sum()
    if denom == 0:
        return np.nan
    return (signed_flow * d_mid).sum() / denom
```

---

## 5. VPIN (Volume-Synchronized Probability of Informed Trading)

Easley, Lopez de Prado & O'Hara (2012), "Flow Toxicity and
Liquidity in a High-Frequency World": sample trades in the volume
clock; each fixed-size volume bucket $i$ is split into buy/sell
fractions by **bulk volume classification** — the standardized
price change over the bucket, passed through the normal CDF, gives
the buy proportion. VPIN is the mean absolute imbalance over the
last $n$ buckets:

$$z_i = \frac{P_i - P_{i-1}}{\sigma_P}, \qquad
V^{buy}_i = V_i\, \Phi(z_i), \qquad
V^{sell}_i = V_i\, \big(1 - \Phi(z_i)\big)$$

$$OI_i = \frac{\big|V^{buy}_i - V^{sell}_i\big|}{V_i}, \qquad
\text{VPIN} = \frac{1}{n}\sum_{i=1}^{n} OI_i$$

The theoretical target is the sequential-trade probability of
informed trading (order flow toxicity):

$$\Pi = \frac{\alpha\,\mu}{\alpha\,\mu + 2\epsilon}$$

with $\mu$ the informed-arrival rate, $\epsilon$ the uninformed rate
per bucket, and $\alpha$ the event probability. Andersen-Bondarenko
later contested VPIN's predictive claims — treat as a candidate
signal, not established fact.

**Verify against library source before production** (paywalled;
synthesized from LLM internal knowledge).

```python
def vpin(prices, volumes, bucket_v, n_buckets=50):
    """VPIN via volume buckets and bulk volume classification.

    prices: (T,) trade prices; volumes: (T,) trade sizes (same units).
    bucket_v: volume per bucket (e.g. 1/50 of average daily volume).
    n_buckets: window length in buckets for the VPIN average.
    Returns vpin_series: one value per completed bucket window
    (aligned to the last bucket of each window).
    """
    from math import erf, sqrt
    total = np.cumsum(volumes)
    edges = np.searchsorted(total, np.arange(1, np.floor(total[-1] / bucket_v) + 1) * bucket_v)
    edges = np.unique(edges[edges < len(prices)])
    if len(edges) < 2:
        return np.array([])
    bounds = np.concatenate(([0], edges))          # bucket boundaries (index space)
    p_start = prices[bounds[:-1]]
    p_end = prices[np.minimum(bounds[1:], len(prices) - 1)]
    d_p = p_end - p_start
    sigma_p = d_p.std()
    if sigma_p == 0:
        return np.array([])
    z = d_p / sigma_p
    phi = 0.5 * (1.0 + np.vectorize(erf)(z / sqrt(2.0)))   # standard normal CDF
    oi = np.abs(2.0 * phi - 1.0)                          # |Vb - Vs| / V
    if len(oi) < n_buckets:
        return np.array([])
    kernel = np.ones(n_buckets) / n_buckets
    return np.convolve(oi, kernel, mode="valid")
```

---

## Library status

The five critical formulas (OFI, Hawkes, CPCV, Kyle's lambda, VPIN)
are executable above. The full 68-paper catalogue is synthesized in
`docs/library/summaries/`; acquisition status is in
`docs/library/acquisition_log.json`; see
`docs/library/manifest.md`. Active work: L2 Codespaces deployment
(`CLOUD_DEPLOY.md`, `.devcontainer`).
