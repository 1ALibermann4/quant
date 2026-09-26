"""Geometry / representation adapters for I04-CAL (numpy-only)."""

from __future__ import annotations

import math
from typing import Any, Callable

import numpy as np

from quant.i04_cal.params import (
    G1_GAMMAS,
    G2_DS,
    G2_L,
    G3_MS,
    G5_LAMBDA,
    G5_PS,
    GORD_DS,
    GORD_TAU,
    geometry_aux_seed,
)
from quant.i04_cal.types import GeometrySpec, GeometryStatus


def standardize_window(w: np.ndarray) -> np.ndarray:
    w = np.asarray(w, dtype=np.float64)
    mu = w.mean()
    sd = w.std(ddof=1)
    if not np.isfinite(sd) or sd <= 0:
        return np.zeros_like(w)
    return (w - mu) / sd


def window_at(r: np.ndarray, t: int, W: int) -> np.ndarray:
    return np.asarray(r[t - W + 1 : t + 1], dtype=np.float64)


# ----- G0 -----


def g0_embed(r: np.ndarray, t: int, W: int) -> np.ndarray:
    return standardize_window(window_at(r, t, W))


def g0_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


# ----- Soft-DTW divergence (Cuturi-style softmin) -----


def _softmin(x: np.ndarray, gamma: float) -> float:
    # numerically stable softmin
    m = float(np.min(x))
    return float(-gamma * math.log(np.sum(np.exp(-(x - m) / gamma))) - m)


def soft_dtw(x: np.ndarray, y: np.ndarray, gamma: float, band: int | None = None) -> float:
    """Soft-DTW with optional Sakoe-Chiba band (preregistered for I04-CAL G1)."""
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    n, m = x.size, y.size
    if band is None:
        band = max(2, max(n, m) // 4)
    R = np.full((n + 2, m + 2), np.inf, dtype=np.float64)
    R[0, 0] = 0.0
    for i in range(1, n + 1):
        j0 = max(1, i - band)
        j1 = min(m, i + band)
        xi = x[i - 1]
        for j in range(j0, j1 + 1):
            cost = (xi - y[j - 1]) ** 2
            r0, r1, r2 = R[i - 1, j], R[i, j - 1], R[i - 1, j - 1]
            # softmin of three
            vals = np.array([r0, r1, r2], dtype=np.float64)
            R[i, j] = cost + _softmin(vals, gamma)
    return float(R[n, m])


def soft_dtw_divergence(x: np.ndarray, y: np.ndarray, gamma: float) -> float:
    return soft_dtw(x, y, gamma) - 0.5 * soft_dtw(x, x, gamma) - 0.5 * soft_dtw(y, y, gamma)


def g1_embed(r: np.ndarray, t: int, W: int) -> np.ndarray:
    return standardize_window(window_at(r, t, W))


def g1_distance(a: np.ndarray, b: np.ndarray, gamma: float) -> float:
    return float(soft_dtw_divergence(a, b, gamma))


# ----- Sliced Wasserstein on delay measures -----


def _delay_cloud(w: np.ndarray, d: int) -> np.ndarray:
    # points y_k = (w_k,...,w_{k+d-1})
    n = w.size - d + 1
    if n <= 0:
        return w.reshape(-1, 1)
    return np.ascontiguousarray(
        np.lib.stride_tricks.sliding_window_view(w, d)
    )


def _sw_dirs(d: int, L: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    U = rng.normal(size=(L, d))
    U /= np.linalg.norm(U, axis=1, keepdims=True) + 1e-12
    return U


_SW_DIR_CACHE: dict[tuple[int, int, int], np.ndarray] = {}


def sliced_wasserstein(w1: np.ndarray, w2: np.ndarray, d: int, L: int, seed: int) -> float:
    key = (d, L, seed)
    if key not in _SW_DIR_CACHE:
        _SW_DIR_CACHE[key] = _sw_dirs(d, L, seed)
    U = _SW_DIR_CACHE[key]
    A = _delay_cloud(w1, d)
    B = _delay_cloud(w2, d)
    if A.size == 0 or B.size == 0:
        return float("nan")
    acc = 0.0
    for ell in range(L):
        u = U[ell]
        pa = np.sort(A @ u)
        pb = np.sort(B @ u)
        # interpolate to common length via quantiles
        q = np.linspace(0.0, 1.0, num=max(pa.size, pb.size), dtype=np.float64)
        qa = np.quantile(pa, q)
        qb = np.quantile(pb, q)
        acc += float(np.mean(np.abs(qa - qb)))
    return acc / L


def g2_embed(r: np.ndarray, t: int, W: int) -> np.ndarray:
    return standardize_window(window_at(r, t, W))


def g2_distance(a: np.ndarray, b: np.ndarray, d: int, L: int = G2_L) -> float:
    return sliced_wasserstein(a, b, d=d, L=L, seed=geometry_aux_seed(2))


# ----- Path signatures (truncated, time-augmented) -----


def _time_aug_path(w: np.ndarray) -> np.ndarray:
    t = np.linspace(0.0, 1.0, w.size, dtype=np.float64)
    return np.stack([t, w], axis=1)


def truncated_signature(path: np.ndarray, M: int) -> np.ndarray:
    """Very small truncated signature for 2D path (levels 1..M)."""
    # Incremental path
    dX = np.diff(path, axis=0)
    feats: list[np.ndarray] = []
    # level 1
    s1 = dX.sum(axis=0)
    feats.append(s1)
    # level 2: sum_{i<=j} dX_i ⊗ dX_j via running
    if M >= 2:
        # Chen: S^2 = sum_{i<j} dX_i ⊗ dX_j + 0.5 sum_i dX_i ⊗ dX_i
        run = np.zeros(path.shape[1], dtype=np.float64)
        s2 = np.zeros((path.shape[1], path.shape[1]), dtype=np.float64)
        for dx in dX:
            s2 += np.outer(run, dx)
            s2 += 0.5 * np.outer(dx, dx)
            run += dx
        feats.append(s2.ravel())
    if M >= 3:
        # crude level-3: outer of level2 increments — limited but deterministic
        run2 = np.zeros_like(s2)
        s3 = np.zeros((path.shape[1],) * 3, dtype=np.float64)
        run = np.zeros(path.shape[1], dtype=np.float64)
        for dx in dX:
            # S^3 increment approx
            for a in range(path.shape[1]):
                for b in range(path.shape[1]):
                    for c in range(path.shape[1]):
                        s3[a, b, c] += run2[a, b] * dx[c]
            run2 += np.outer(run, dx) + 0.5 * np.outer(dx, dx)
            run += dx
        feats.append(s3.ravel())
    return np.concatenate(feats)


def g3_embed(r: np.ndarray, t: int, W: int, M: int) -> np.ndarray:
    w = standardize_window(window_at(r, t, W))
    return truncated_signature(_time_aug_path(w), M)


def g3_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


# ----- MMD (RBF, within-window delays) -----


def _rbf_mmd(cloud_a: np.ndarray, cloud_b: np.ndarray, bandwidth: float) -> float:
    def k(X, Y):
        # ||x-y||^2
        xx = np.sum(X * X, axis=1)[:, None]
        yy = np.sum(Y * Y, axis=1)[None, :]
        d2 = xx + yy - 2.0 * (X @ Y.T)
        return np.exp(-d2 / (2.0 * bandwidth * bandwidth + 1e-12))

    m = cloud_a.shape[0]
    n = cloud_b.shape[0]
    Kaa = k(cloud_a, cloud_a)
    Kbb = k(cloud_b, cloud_b)
    Kab = k(cloud_a, cloud_b)
    # unbiased-ish with diag zeroed for XX/YY
    np.fill_diagonal(Kaa, 0.0)
    np.fill_diagonal(Kbb, 0.0)
    term_a = Kaa.sum() / max(m * (m - 1), 1)
    term_b = Kbb.sum() / max(n * (n - 1), 1)
    term_ab = Kab.mean()
    return float(term_a + term_b - 2.0 * term_ab)


def _median_bandwidth(cloud: np.ndarray) -> float:
    if cloud.shape[0] < 2:
        return 1.0
    # subsample pairs
    n = min(cloud.shape[0], 64)
    X = cloud[:n]
    xx = np.sum(X * X, axis=1)[:, None]
    d2 = xx + xx.T - 2.0 * (X @ X.T)
    iu = np.triu_indices(n, 1)
    med = float(np.median(np.sqrt(np.maximum(d2[iu], 0.0))))
    return med if med > 1e-8 else 1.0


def g4_embed(r: np.ndarray, t: int, W: int) -> np.ndarray:
    return standardize_window(window_at(r, t, W))


def g4_distance(a: np.ndarray, b: np.ndarray, delay: int = 2) -> float:
    ca = _delay_cloud(a, delay)
    cb = _delay_cloud(b, delay)
    bw = _median_bandwidth(np.vstack([ca, cb]))
    return _rbf_mmd(ca, cb, bw)


# ----- SPD / AIRM -----


def _cov_reg(w: np.ndarray, p: int, lam: float) -> np.ndarray:
    # lag vectors
    Z = _delay_cloud(w, p)
    if Z.shape[0] < 2:
        return np.eye(p) * lam
    C = np.cov(Z, rowvar=False)
    if C.ndim == 0:
        C = np.array([[float(C)]])
    return C + lam * np.eye(C.shape[0])


def airm_distance(C: np.ndarray, D: np.ndarray) -> float:
    # ||log(C^{-1/2} D C^{-1/2})||_F
    # via generalized eigenvalues
    try:
        w = np.linalg.eigvalsh(C, D) if False else None
    except Exception:
        w = None
    # standard: eig of C^{-1}D
    try:
        vals = np.linalg.eigvals(np.linalg.solve(C, D))
        vals = np.real(vals)
        vals = np.clip(vals, 1e-12, None)
        return float(np.sqrt(np.sum(np.log(vals) ** 2)))
    except np.linalg.LinAlgError:
        return float("nan")


def g5_embed(r: np.ndarray, t: int, W: int, p: int, lam: float = G5_LAMBDA) -> np.ndarray:
    w = standardize_window(window_at(r, t, W))
    return _cov_reg(w, p, lam)


def g5_distance(A: np.ndarray, B: np.ndarray) -> float:
    return airm_distance(A, B)


# ----- G7 minimal TDA (0-dim persistence bottleneck on delay points) -----


def _persistence_0d(points: np.ndarray) -> np.ndarray:
    """0-dim persistence death times via MST edge lengths (sorted)."""
    n = points.shape[0]
    if n < 2:
        return np.zeros(0, dtype=np.float64)
    # pairwise
    d = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
    # Prim MST edges
    in_tree = np.zeros(n, dtype=bool)
    in_tree[0] = True
    deaths: list[float] = []
    for _ in range(n - 1):
        mask = in_tree
        # min edge from tree to outside
        sub = d[mask][:, ~mask]
        if sub.size == 0:
            break
        deaths.append(float(np.min(sub)))
        # add closest outside point
        flat = np.argmin(sub)
        # map back
        outs = np.where(~mask)[0]
        j = outs[flat % outs.size]
        # better indexing:
        ii, jj = np.unravel_index(np.argmin(d[mask][:, ~mask]), sub.shape)
        outs = np.where(~mask)[0]
        in_tree[outs[jj]] = True
    return np.sort(np.asarray(deaths, dtype=np.float64))


def _bottleneck_0d(a: np.ndarray, b: np.ndarray) -> float:
    # pad with diagonal (death=0 birth=0) conceptually — use L_inf matching of death times
    aa = list(a)
    bb = list(b)
    while len(aa) < len(bb):
        aa.append(0.0)
    while len(bb) < len(aa):
        bb.append(0.0)
    aa.sort()
    bb.sort()
    if not aa:
        return 0.0
    return float(np.max(np.abs(np.asarray(aa) - np.asarray(bb))))


def g7_embed(r: np.ndarray, t: int, W: int) -> np.ndarray:
    w = standardize_window(window_at(r, t, W))
    cloud = _delay_cloud(w, 2)
    return _persistence_0d(cloud)


def g7_distance(a: np.ndarray, b: np.ndarray) -> float:
    return _bottleneck_0d(a, b)


# ----- Ordinal / Bandt-Pompe -----


def _ordinal_hist(w: np.ndarray, D: int, tau: int) -> np.ndarray:
    n = w.size - (D - 1) * tau
    n_pat = math.factorial(D)
    hist = np.zeros(n_pat, dtype=np.float64)
    if n <= 0:
        return hist
    # map permutation to lehmer code
    from itertools import permutations

    patterns = list(permutations(range(D)))
    pmap = {p: i for i, p in enumerate(patterns)}
    for i in range(n):
        idx = [i + k * tau for k in range(D)]
        vals = w[idx]
        order = tuple(int(x) for x in np.argsort(vals, kind="mergesort"))
        hist[pmap[order]] += 1.0
    s = hist.sum()
    if s > 0:
        hist /= s
    return hist


def _js_distance(p: np.ndarray, q: np.ndarray) -> float:
    m = 0.5 * (p + q)

    def _kl(a, b):
        mask = a > 0
        return float(np.sum(a[mask] * np.log(a[mask] / (b[mask] + 1e-300))))

    jsd = 0.5 * _kl(p, m) + 0.5 * _kl(q, m)
    return float(math.sqrt(max(jsd, 0.0)))


def gord_embed(r: np.ndarray, t: int, W: int, D: int, tau: int = GORD_TAU) -> np.ndarray:
    w = standardize_window(window_at(r, t, W))
    return _ordinal_hist(w, D, tau)


def gord_distance(a: np.ndarray, b: np.ndarray) -> float:
    return _js_distance(a, b)


# ----- G_VOL nuisance -----


def log_rv(r: np.ndarray, t: int, W: int) -> float:
    w = window_at(r, t, W)
    return float(np.log(np.mean(w * w) + 1e-12))


def gvol_distance(t_val: float, s_val: float) -> float:
    return float(abs(t_val - s_val))


# ----- Registry -----


def iter_geometry_specs(include_hold: bool = False) -> list[GeometrySpec]:
    specs: list[GeometrySpec] = [
        GeometrySpec("G0", "default", {}),
    ]
    for g in G1_GAMMAS:
        specs.append(GeometrySpec("G1", f"gamma={g}", {"gamma": g}))
    for d in G2_DS:
        specs.append(GeometrySpec("G2", f"d={d},L={G2_L}", {"d": d, "L": G2_L}))
    for M in G3_MS:
        specs.append(GeometrySpec("G3", f"M={M}", {"M": M}))
    specs.append(GeometrySpec("G4", "rbf_median", {"delay": 2}))
    for p in G5_PS:
        specs.append(GeometrySpec("G5", f"p={p},lam={G5_LAMBDA}", {"p": p, "lam": G5_LAMBDA}))
    specs.append(GeometrySpec("G7", "rips0_delay2", {}))
    for D in GORD_DS:
        specs.append(GeometrySpec("GORD", f"D={D},tau={GORD_TAU}", {"D": D, "tau": GORD_TAU}))
    if include_hold:
        specs.append(
            GeometrySpec("G6", "HOLD", {}, status=GeometryStatus.HOLD)
        )
    return specs


def embed_and_distance_fns(
    spec: GeometrySpec,
) -> tuple[Callable[..., Any], Callable[..., float]]:
    gid = spec.geometry_id
    p = spec.params
    if gid == "G0":
        return g0_embed, g0_distance
    if gid == "G1":
        g = float(p["gamma"])
        return g1_embed, lambda a, b, gamma=g: g1_distance(a, b, gamma)
    if gid == "G2":
        d = int(p["d"])
        L = int(p["L"])
        return g2_embed, lambda a, b, d=d, L=L: g2_distance(a, b, d, L)
    if gid == "G3":
        M = int(p["M"])
        return (lambda r, t, W, M=M: g3_embed(r, t, W, M)), g3_distance
    if gid == "G4":
        return g4_embed, g4_distance
    if gid == "G5":
        pp = int(p["p"])
        lam = float(p["lam"])
        return (
            lambda r, t, W, pp=pp, lam=lam: g5_embed(r, t, W, pp, lam),
            g5_distance,
        )
    if gid == "G7":
        return g7_embed, g7_distance
    if gid == "GORD":
        D = int(p["D"])
        tau = int(p["tau"])
        return (
            lambda r, t, W, D=D, tau=tau: gord_embed(r, t, W, D, tau),
            gord_distance,
        )
    raise KeyError(gid)
