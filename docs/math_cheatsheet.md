# Math cheatsheet: the library as code

The formula from the paper, immediately followed by the optimized
Python function that executes it. No PDFs required. All functions are
numpy-vectorized and depend only on `numpy`.

---

## 1. Cont, Kukanov, Stoikov (2014) — "The Price Impact of Order Book Events"

### 1a. Order flow imbalance at the best quotes (OFI)

EXTRACTED VERBATIM FROM THE arXiv LATEX SOURCE (arXiv:1011.6402v3,
Sec. 2.1, verified 2026-11-16 against the rendered source). Let
$P^B_n, q^B_n$ be the best bid price and size after the $n$-th book
event, $P^A_n, q^A_n$ the best ask. The paper defines the contribution
of the $n$-th event to the size of the bid and ask queues:

$$e_n = \mathbb{1}\{P^B_n \geq P^B_{n-1}\}\, q^B_n
       - \mathbb{1}\{P^B_n \leq P^B_{n-1}\}\, q^B_{n-1}
       - \mathbb{1}\{P^A_n \leq P^A_{n-1}\}\, q^A_n
       + \mathbb{1}\{P^A_n \geq P^A_{n-1}\}\, q^A_{n-1}$$

The indicators are NON-STRICT, and this matters: when the price is
unchanged both indicators fire and the event contributes the queue
change $q_n - q_{n-1}$ (added liquidity positive, removed negative).
When the bid improves the event contributes the FULL new queue $q^B_n$
(a price-improving limit order); when the bid drops it contributes
$-q^B_{n-1}$ (the withdrawn old queue, whether by market order or
cancel); the ask side is symmetric with signs reversed. Earlier versions
of this cheatsheet restated $e_n$ as a $\Delta q$-decomposition that
differs from the source on price-changing branches; that restatement is
retired. The order flow imbalance over $[t_{k-1}, t_k]$ aggregates the
event contributions:

$$OFI_k = \sum_{n=N(t_{k-1})+1}^{N(t_k)} e_n$$

and the linear impact relation (their Eq. 2) is
$\Delta P_k = \beta\, OFI_k + \epsilon_k$.

```python
import numpy as np

def ofi_top_level(pb, qb, pa, qa):
    """Cont-Kukanov-Stoikov OFI at the best quotes, the EXACT source
    formula (arXiv:1011.6402v3, Sec. 2.1). Matches features.top_of_book_ofi.

    pb, qb: (T,) best bid price and size after each book event
    pa, qa: (T,) best ask price and size after each book event
    Returns e: (T,) order flow per event, e[0] = 0.
    """
    d_pb, d_pa = np.diff(pb, prepend=pb[0]), np.diff(pa, prepend=pa[0])
    return (np.where(d_pb >= 0, qb, 0.0)
            - np.where(d_pb <= 0, np.concatenate([[qb[0]], qb[:-1]]), 0.0)
            - np.where(d_pa <= 0, qa, 0.0)
            + np.where(d_pa >= 0, np.concatenate([[qa[0]], qa[:-1]]), 0.0))
```

Verified literally against the arXiv source by `src/verify_math_library.py`
(25 randomized books x 2000 events, max abs diff 0.0), which found and fixed
two defects in the prior implementation: sign-flipped ask-side branches and
dropped same-price queue changes.

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

## Library status

The three critical papers are now executable. The library task is
closed; see `docs/library/manifest.md`. Active work: L2 Codespaces
deployment (`CLOUD_DEPLOY.md`, `.devcontainer`).
