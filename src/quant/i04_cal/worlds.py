"""Synthetic world generators for I04-CAL (SPEC v0.2)."""

from __future__ import annotations

import math
from typing import Callable

import numpy as np

from quant.i04_cal.params import (
    N_POST_BURNIN,
    OBSERVABILITY_SPEARMAN_MIN,
    S1_BURNIN,
    S1_PHI,
    S1_SIGMA_H,
    S7_NOISE_FRAC,
    world_seed,
)
from quant.i04_cal.types import OracleStatus, WorldBundle, WorldStatus


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(int(seed))


# ----- S0 -----


def gen_s0a(b: int) -> WorldBundle:
    seed = world_seed("S0a", b)
    r = _rng(seed).normal(0.0, 1.0, size=N_POST_BURNIN).astype(np.float64)
    return WorldBundle(
        world_id="S0a",
        b=b,
        seed=seed,
        returns=r,
        oracle_status=OracleStatus.NOT_APPLICABLE,
        notes=["IID Gaussian null — no structural recurrence"],
    )


def gen_s0b(b: int) -> WorldBundle:
    seed = world_seed("S0b", b)
    # t_5 / sqrt(5/3) => variance 1
    x = _rng(seed).standard_t(5, size=N_POST_BURNIN).astype(np.float64)
    r = x / math.sqrt(5.0 / 3.0)
    return WorldBundle(
        world_id="S0b",
        b=b,
        seed=seed,
        returns=r,
        oracle_status=OracleStatus.NOT_APPLICABLE,
        notes=["IID heavy-tail null — no structural recurrence"],
    )


# ----- S1 SV -----


def gen_s1(b: int) -> WorldBundle:
    seed = world_seed("S1", b)
    rng = _rng(seed)
    T = N_POST_BURNIN + S1_BURNIN
    h = np.zeros(T, dtype=np.float64)
    for t in range(1, T):
        h[t] = S1_PHI * h[t - 1] + S1_SIGMA_H * rng.normal()
    eps = rng.normal(size=T)
    r_full = np.exp(0.5 * h) * eps
    r = r_full[S1_BURNIN:].astype(np.float64)
    h_keep = h[S1_BURNIN:].astype(np.float64)
    return WorldBundle(
        world_id="S1",
        b=b,
        seed=seed,
        returns=r,
        latent={"h": h_keep},
        oracle_status=OracleStatus.VALID,
        oracle_meta={"kind": "volatility", "d_star": "abs_h"},
        notes=["SV only — expected VOLATILITY-DOMINATED"],
    )


# ----- S2 motifs -----

# Frozen prototype coefficients (sums of sines) — NOT redrawn per run
_S2_PROTOS: tuple[tuple[tuple[float, float, float], ...], ...] = (
    ((1.0, 1.0, 0.0), (0.35, 3.0, 0.2), (0.15, 5.0, -0.4)),
    ((1.0, 2.0, 0.5), (0.4, 4.0, 0.0), (0.2, 6.0, 1.0)),
    ((0.8, 1.5, -0.3), (0.5, 3.5, 0.7), (0.25, 7.0, 0.1)),
)


def _proto_m(j: int, u: np.ndarray) -> np.ndarray:
    out = np.zeros_like(u, dtype=np.float64)
    for amp, freq, phase in _S2_PROTOS[j]:
        out += amp * np.sin(2.0 * math.pi * freq * u + phase)
    return out


def _psi_alpha(u: np.ndarray, alpha: float) -> np.ndarray:
    # u^a / (u^a + (1-u)^a); endpoints fixed
    ua = np.power(np.clip(u, 0.0, 1.0), alpha)
    va = np.power(np.clip(1.0 - u, 0.0, 1.0), alpha)
    den = ua + va
    out = np.divide(ua, den, out=np.zeros_like(ua), where=den > 0)
    out[0] = 0.0
    out[-1] = 1.0
    return out


def gen_s2(b: int, W: int = 60) -> WorldBundle:
    """Concatenate warped motif windows; oracle class = prototype j."""
    seed = world_seed("S2", b)
    rng = _rng(seed)
    alphas = (0.65, 1.0, 1.55)
    # Fill series with successive motifs of length W
    n_blocks = N_POST_BURNIN // W
    r = np.zeros(N_POST_BURNIN, dtype=np.float64)
    labels = np.full(N_POST_BURNIN, -1, dtype=np.int32)
    u = np.linspace(0.0, 1.0, W, dtype=np.float64)
    # Frozen distractor: mix frequencies of proto0/1 without being class 0 or 1
    distractor_coefs = ((0.7, 1.2, 0.1), (0.45, 3.7, -0.5), (0.2, 8.0, 0.3))

    for blk in range(n_blocks):
        if rng.random() < 0.15:
            # distractor — label -2 (excluded from primary oracle)
            m = np.zeros(W, dtype=np.float64)
            for amp, freq, phase in distractor_coefs:
                m += amp * np.sin(2.0 * math.pi * freq * u + phase)
            j = -2
        else:
            j = int(rng.integers(0, 3))
            alpha = float(alphas[int(rng.integers(0, 3))])
            a = float(rng.uniform(0.9, 1.1))
            uw = _psi_alpha(u, alpha)
            m = a * _proto_m(j, uw)
        sd = float(np.std(m)) + 1e-12
        eps = rng.normal(0.0, 0.20 * sd, size=W)
        seg = m + eps
        start = blk * W
        r[start : start + W] = seg
        labels[start : start + W] = j

    # pad remainder
    rem = N_POST_BURNIN - n_blocks * W
    if rem:
        r[-rem:] = rng.normal(size=rem)
        labels[-rem:] = -1

    return WorldBundle(
        world_id="S2",
        b=b,
        seed=seed,
        returns=r,
        oracle_labels=labels,
        oracle_status=OracleStatus.VALID,
        oracle_meta={
            "kind": "categorical",
            "classes": {0: "m1", 1: "m2", 2: "m3"},
            "exclude_labels": [-1, -2],
            "window_hint": W,
        },
        notes=["Time-warped motifs; alpha/a not part of class"],
    )


# ----- S3 regimes -----


def _skew_normal_std(rng: np.random.Generator, n: int, shape: float = 5.0) -> np.ndarray:
    """Approximate skew-normal then standardize empirically per draw block."""
    # Azzalini construction via half-normal + gaussian
    u0 = rng.normal(size=n)
    v = rng.normal(size=n)
    z = shape * np.abs(u0) + v  # crude; then standardize
    z = (z - z.mean()) / (z.std() + 1e-12)
    return z.astype(np.float64)


def gen_s3(b: int) -> WorldBundle:
    seed = world_seed("S3", b)
    rng = _rng(seed)
    r = np.empty(N_POST_BURNIN, dtype=np.float64)
    labels = np.empty(N_POST_BURNIN, dtype=np.int32)
    t = 0
    prev = -1
    # 0=GAUSSIAN, 1=STUDENT, 2=SKEWED
    while t < N_POST_BURNIN:
        choices = [0, 1, 2]
        if prev in choices:
            choices.remove(prev)
        reg = int(rng.choice(choices))
        L = int(rng.integers(120, 301))
        end = min(N_POST_BURNIN, t + L)
        n = end - t
        if reg == 0:
            seg = rng.normal(size=n)
        elif reg == 1:
            seg = rng.standard_t(5, size=n) / math.sqrt(5.0 / 3.0)
        else:
            seg = _skew_normal_std(rng, n, shape=5.0)
        r[t:end] = seg
        labels[t:end] = reg
        prev = reg
        t = end
    return WorldBundle(
        world_id="S3",
        b=b,
        seed=seed,
        returns=r,
        oracle_labels=labels,
        oracle_status=OracleStatus.VALID,
        oracle_meta={
            "kind": "categorical",
            "classes": {0: "GAUSSIAN", 1: "STUDENT", 2: "SKEWED"},
        },
        notes=["Distributional regimes; empirical moments reported downstream"],
    )


# ----- S4 ordering -----


def gen_s4(b: int, W: int = 64) -> WorldBundle:
    seed = world_seed("S4", b)
    rng = _rng(seed)
    n_blocks = N_POST_BURNIN // W
    r = np.zeros(N_POST_BURNIN, dtype=np.float64)
    labels = np.full(N_POST_BURNIN, -1, dtype=np.int32)
    for blk in range(n_blocks):
        base = rng.normal(size=W)
        # shared multiset: sort then permute into orderings
        vals = np.sort(base)
        order = int(rng.integers(0, 3))
        if order == 0:  # alternating high-low from ends
            out = np.empty(W, dtype=np.float64)
            lo, hi = 0, W - 1
            for i in range(W):
                if i % 2 == 0:
                    out[i] = vals[hi]
                    hi -= 1
                else:
                    out[i] = vals[lo]
                    lo += 1
        elif order == 1:  # persistent runs: low then high
            mid = W // 2
            out = np.concatenate([vals[:mid], vals[mid:]])
        else:  # shuffled
            out = vals.copy()
            rng.shuffle(out)
        start = blk * W
        r[start : start + W] = out
        # interior oracle: exclude edges of width 4
        labels[start : start + W] = order
        labels[start : start + 4] = -1
        labels[start + W - 4 : start + W] = -1
    rem = N_POST_BURNIN - n_blocks * W
    if rem:
        r[-rem:] = rng.normal(size=rem)
    return WorldBundle(
        world_id="S4",
        b=b,
        seed=seed,
        returns=r,
        oracle_labels=labels,
        oracle_status=OracleStatus.VALID,
        oracle_meta={
            "kind": "categorical",
            "classes": {0: "O1_alt", 1: "O2_persist", 2: "O3_shuf"},
            "exclude_labels": [-1],
        },
        notes=["Same multiset / different ordering; interior windows only"],
    )


# ----- S5 dependence -----


def gen_s5(b: int) -> WorldBundle:
    seed = world_seed("S5", b)
    rng = _rng(seed)
    phis = (-0.6, 0.0, 0.6)
    r = np.zeros(N_POST_BURNIN, dtype=np.float64)
    labels = np.empty(N_POST_BURNIN, dtype=np.int32)
    phi_t = np.empty(N_POST_BURNIN, dtype=np.float64)
    t = 0
    prev_phi_idx = -1
    r_prev = 0.0
    while t < N_POST_BURNIN:
        choices = [0, 1, 2]
        if prev_phi_idx in choices:
            choices.remove(prev_phi_idx)
        idx = int(rng.choice(choices))
        phi = phis[idx]
        L = int(rng.integers(150, 351))
        end = min(N_POST_BURNIN, t + L)
        # transition exclusion width
        trans = 20
        for s in range(t, end):
            eps = rng.normal()
            r_prev = phi * r_prev + math.sqrt(max(0.0, 1.0 - phi * phi)) * eps
            r[s] = r_prev
            phi_t[s] = phi
            labels[s] = idx if (s - t) >= trans and (end - s) > trans else -1
        prev_phi_idx = idx
        t = end
    return WorldBundle(
        world_id="S5",
        b=b,
        seed=seed,
        returns=r,
        latent={"phi": phi_t},
        oracle_labels=labels,
        oracle_status=OracleStatus.VALID,
        oracle_meta={
            "kind": "categorical",
            "classes": {0: "phi_-0.6", 1: "phi_0", 2: "phi_+0.6"},
            "exclude_labels": [-1],
        },
        notes=["AR(1) regimes continuous; variance theoretically 1"],
    )


# ----- S6 manifold -----


def gen_s6(b: int) -> WorldBundle:
    seed = world_seed("S6", b)
    rng = _rng(seed)
    # slow latent random walk with reflecting boundaries on [-1,1]^2
    u = np.zeros(N_POST_BURNIN, dtype=np.float64)
    v = np.zeros(N_POST_BURNIN, dtype=np.float64)
    u[0], v[0] = 0.0, 0.0
    step = 0.02
    for t in range(1, N_POST_BURNIN):
        u[t] = u[t - 1] + step * rng.normal()
        v[t] = v[t - 1] + step * rng.normal()
        if u[t] > 1.0 or u[t] < -1.0:
            u[t] = np.clip(u[t], -1.0, 1.0)
            step_u = -1  # reflect by negating next increments via clip only
        if v[t] > 1.0 or v[t] < -1.0:
            v[t] = np.clip(v[t], -1.0, 1.0)
    c = 1.5
    # frozen projection q
    q = np.array([0.6, 0.3, 0.1], dtype=np.float64)
    q = q / np.linalg.norm(q)
    Phi = np.stack(
        [(u + c) * np.cos(u), v, (u + c) * np.sin(u)], axis=1
    )
    eta = 0.05 * rng.normal(size=N_POST_BURNIN)
    r = (Phi @ q) + eta
    z = np.stack([u, v], axis=1)
    # observability diagnostic vs delay L2 (W=40)
    obs = _observability_spearman(r, z, W=40, seed=seed + 999)
    ostat = (
        OracleStatus.VALID
        if obs >= OBSERVABILITY_SPEARMAN_MIN
        else OracleStatus.INVALID
    )
    return WorldBundle(
        world_id="S6",
        b=b,
        seed=seed,
        returns=r.astype(np.float64),
        latent={"z": z, "observability_spearman": obs},
        oracle_status=ostat,
        oracle_meta={"kind": "latent_distance", "d_star": "euclidean_z"},
        notes=[f"observability_spearman={obs:.4f}"],
    )


def _observability_spearman(
    r: np.ndarray, z: np.ndarray, *, W: int, seed: int, n_pairs: int = 400
) -> float:
    rng = _rng(seed)
    T = r.shape[0]
    # delay vectors
    idx = np.arange(W - 1, T)
    if idx.size < 10:
        return 0.0
    # sample pairs
    n = min(n_pairs, idx.size * (idx.size - 1) // 2)
    i = rng.choice(idx, size=n, replace=True)
    j = rng.choice(idx, size=n, replace=True)
    mask = np.abs(i - j) >= W
    i, j = i[mask], j[mask]
    if i.size < 20:
        return 0.0
    # distances
    d_delay = np.empty(i.size, dtype=np.float64)
    d_z = np.empty(i.size, dtype=np.float64)
    for k in range(i.size):
        wi = r[i[k] - W + 1 : i[k] + 1]
        wj = r[j[k] - W + 1 : j[k] + 1]
        d_delay[k] = float(np.linalg.norm(wi - wj))
        d_z[k] = float(np.linalg.norm(z[i[k]] - z[j[k]]))
    return float(_spearman(d_delay, d_z))


def _spearman(a: np.ndarray, b: np.ndarray) -> float:
    if a.size < 3:
        return 0.0
    ra = a.argsort().argsort().astype(np.float64)
    rb = b.argsort().argsort().astype(np.float64)
    ra -= ra.mean()
    rb -= rb.mean()
    den = float(np.sqrt((ra * ra).sum() * (rb * rb).sum()))
    if den <= 0:
        return 0.0
    return float((ra * rb).sum() / den)


# ----- S7 Lorenz -----


def _lorenz_rk4(n: int, dt: float, seed: int) -> np.ndarray:
    rng = _rng(seed)
    sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
    # burn-in integrate
    x = y = z = 1.0
    burn = 5000
    states = np.empty((n, 3), dtype=np.float64)

    def f(xx, yy, zz):
        return (
            sigma * (yy - xx),
            xx * (rho - zz) - yy,
            xx * yy - beta * zz,
        )

    def step(xx, yy, zz):
        k1 = f(xx, yy, zz)
        k2 = f(xx + 0.5 * dt * k1[0], yy + 0.5 * dt * k1[1], zz + 0.5 * dt * k1[2])
        k3 = f(xx + 0.5 * dt * k2[0], yy + 0.5 * dt * k2[1], zz + 0.5 * dt * k2[2])
        k4 = f(xx + dt * k3[0], yy + dt * k3[1], zz + dt * k3[2])
        return (
            xx + (dt / 6.0) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            yy + (dt / 6.0) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]),
            zz + (dt / 6.0) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]),
        )

    for _ in range(burn):
        x, y, z = step(x, y, z)
    # subsample every 10 steps for series length
    sub = 10
    k = 0
    while k < n:
        for _ in range(sub):
            x, y, z = step(x, y, z)
        states[k] = (x, y, z)
        k += 1
    # tiny jitter unused — keep deterministic trajectory
    _ = rng
    return states


def gen_s7(b: int, noise_frac: float = 0.05) -> WorldBundle:
    seed = world_seed("S7", b)
    states = _lorenz_rk4(N_POST_BURNIN, dt=0.01, seed=seed)
    x = states[:, 0]
    sigma_x = float(np.std(x)) + 1e-12
    rng = _rng(seed + 17)
    r = x + noise_frac * sigma_x * rng.normal(size=N_POST_BURNIN)
    obs = _observability_spearman(r, states, W=40, seed=seed + 777)
    ostat = (
        OracleStatus.VALID
        if obs >= OBSERVABILITY_SPEARMAN_MIN
        else OracleStatus.INVALID
    )
    return WorldBundle(
        world_id="S7",
        b=b,
        seed=seed,
        returns=r.astype(np.float64),
        latent={
            "z": states,
            "observability_spearman": obs,
            "noise_frac": noise_frac,
            "sigma_x": sigma_x,
        },
        oracle_status=ostat,
        oracle_meta={"kind": "latent_distance", "d_star": "euclidean_xyz"},
        notes=[f"Lorenz univariate x; noise_frac={noise_frac}; obs={obs:.4f}"],
    )


GENERATORS: dict[str, Callable[[int], WorldBundle]] = {
    "S0a": gen_s0a,
    "S0b": gen_s0b,
    "S1": gen_s1,
    "S2": gen_s2,
    "S3": gen_s3,
    "S4": gen_s4,
    "S5": gen_s5,
    "S6": gen_s6,
    "S7": lambda b: gen_s7(b, noise_frac=0.05),
}


def generate_world(world_id: str, b: int) -> WorldBundle:
    if world_id not in GENERATORS:
        raise KeyError(world_id)
    return GENERATORS[world_id](int(b))
