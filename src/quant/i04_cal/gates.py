"""Neighborhood engine and structural gates for I04-CAL."""

from __future__ import annotations

from typing import Any, Callable

import numpy as np

from quant.i04_cal.geometries import embed_and_distance_fns, gvol_distance, log_rv
from quant.i04_cal.params import (
    CANDIDATE_STRIDE,
    EXPENSIVE_CANDIDATE_STRIDE,
    EXPENSIVE_GEOMETRIES,
    EXPENSIVE_QUERY_STRIDE,
    K_NEIGHBORS,
    PERTURB_CS,
    QUERY_STRIDE,
    RECURRENCE_H_MULT,
)
from quant.i04_cal.types import GeometrySpec, WorldBundle
from quant.i04_cal.worlds import _spearman


def admissible_indices(T: int, W: int) -> np.ndarray:
    return np.arange(W - 1, T, dtype=np.int64)


def query_indices(T: int, W: int, stride: int = QUERY_STRIDE) -> np.ndarray:
    return admissible_indices(T, W)[::stride]


def candidate_indices(T: int, W: int, stride: int = CANDIDATE_STRIDE) -> np.ndarray:
    return admissible_indices(T, W)[::stride]


def embargo_ok(t: int, s: int, W: int) -> bool:
    return abs(int(t) - int(s)) >= int(W)


def _is_vector_embed(x: Any) -> bool:
    return isinstance(x, np.ndarray) and x.ndim == 1


def _vector_knn_batch(
    q_idx: np.ndarray,
    c_idx: np.ndarray,
    emb: dict[int, np.ndarray],
    W: int,
    k_max: int,
    rng: np.random.Generator,
) -> dict[int, tuple[list[int], list[float], list[int], list[float]]]:
    """Vectorized L2 kNN for 1-D embeddings."""
    c_list = [int(s) for s in c_idx if int(s) in emb]
    if not c_list:
        return {}
    C = np.stack([emb[s] for s in c_list], axis=0)  # nC x D
    c_arr = np.asarray(c_list, dtype=np.int64)
    out: dict[int, tuple[list[int], list[float], list[int], list[float]]] = {}
    for t in q_idx:
        t = int(t)
        if t not in emb:
            continue
        v = emb[t]
        # distances
        d = np.linalg.norm(C - v[None, :], axis=1)
        # mask embargo / self
        mask = np.abs(c_arr - t) >= W
        mask &= c_arr != t
        d2 = np.where(mask, d, np.inf)
        order = np.argsort(d2, kind="mergesort")
        nn_i = []
        nn_d = []
        for j in order:
            if not np.isfinite(d2[j]):
                break
            nn_i.append(int(c_arr[j]))
            nn_d.append(float(d2[j]))
            if len(nn_i) >= k_max:
                break
        pool = [int(c_arr[j]) for j in range(len(c_arr)) if mask[j]]
        if len(pool) >= k_max:
            choice = rng.choice(len(pool), size=k_max, replace=False)
            rand_idx = [pool[int(i)] for i in choice]
        else:
            rand_idx = pool
        dmap = {int(c_arr[j]): float(d[j]) for j in range(len(c_arr)) if mask[j]}
        rand_dist = [dmap[s] for s in rand_idx]
        out[t] = (nn_i, nn_d, rand_idx, rand_dist)
    return out


def knn_for_query(
    t: int,
    emb: dict[int, Any],
    dist_fn: Callable[[Any, Any], float],
    candidates: np.ndarray,
    W: int,
    k: int,
    rng: np.random.Generator,
) -> tuple[list[int], list[float], list[int], list[float]]:
    dlist: list[tuple[float, int]] = []
    for s in candidates:
        s = int(s)
        if s == t or not embargo_ok(t, s, W):
            continue
        if s not in emb or t not in emb:
            continue
        d = dist_fn(emb[t], emb[s])
        if not np.isfinite(d):
            continue
        dlist.append((float(d), s))
    dlist.sort(key=lambda x: (x[0], x[1]))
    nn = dlist[:k]
    pool = [s for _, s in dlist]
    if len(pool) < k:
        rand_idx = pool
    else:
        choice = rng.choice(len(pool), size=k, replace=False)
        rand_idx = [pool[int(i)] for i in choice]
    dmap = {s: d for d, s in dlist}
    rand_dist = [dmap[s] for s in rand_idx]
    return [s for _, s in nn], [d for d, _ in nn], rand_idx, rand_dist


def build_embeddings(
    r: np.ndarray,
    indices: np.ndarray,
    W: int,
    embed_fn: Callable[..., Any],
) -> dict[int, Any]:
    out: dict[int, Any] = {}
    for t in indices:
        out[int(t)] = embed_fn(r, int(t), W)
    return out


def compute_gates_for_spec(
    world: WorldBundle,
    spec: GeometrySpec,
    W: int,
    *,
    seed: int,
) -> dict[str, Any]:
    r = world.returns
    T = int(r.shape[0])
    embed_fn, dist_fn = embed_and_distance_fns(spec)
    q_stride = (
        EXPENSIVE_QUERY_STRIDE
        if spec.geometry_id in EXPENSIVE_GEOMETRIES
        else QUERY_STRIDE
    )
    c_stride = (
        EXPENSIVE_CANDIDATE_STRIDE
        if spec.geometry_id in EXPENSIVE_GEOMETRIES
        else CANDIDATE_STRIDE
    )
    q_idx = query_indices(T, W, stride=q_stride)
    c_idx = candidate_indices(T, W, stride=c_stride)
    union_idx = np.unique(np.concatenate([q_idx, c_idx]))
    emb = build_embeddings(r, union_idx, W, embed_fn)
    rng = np.random.default_rng(seed)

    results: dict[str, Any] = {
        "geometry_id": spec.geometry_id,
        "variant_id": spec.variant_id,
        "W": W,
        "n_queries": int(q_idx.size),
        "k": {},
        "CAL_G3": {},
        "CAL_G4": {},
        "CAL_G5": {},
        "CAL_6": {},
    }

    k_max = max(K_NEIGHBORS)
    sample = next(iter(emb.values())) if emb else None
    if _is_vector_embed(sample) and spec.geometry_id in {"G0", "G3", "G7", "GORD", "G4"}:
        # G4 embed is window vector but distance is MMD on delays — not pure L2 on embed
        if spec.geometry_id in {"G0", "G3", "G7", "GORD"}:
            nn_cache = _vector_knn_batch(q_idx, c_idx, emb, W, k_max, rng)
        else:
            nn_cache = {
                int(t): knn_for_query(int(t), emb, dist_fn, c_idx, W, k_max, rng)
                for t in q_idx
            }
    else:
        nn_cache = {
            int(t): knn_for_query(int(t), emb, dist_fn, c_idx, W, k_max, rng)
            for t in q_idx
        }

    for k in K_NEIGHBORS:
        contrasts = []
        jacc_obs = []
        jacc_null = []
        prev_set: set[int] | None = None
        prev_t: int | None = None
        for t in q_idx:
            t = int(t)
            if t not in nn_cache:
                continue
            nn_idx, nn_d, rand_idx, rand_d = nn_cache[t]
            nn_k = nn_idx[:k]
            nn_dk = nn_d[:k]
            rd = rand_d[:k]
            if not nn_dk or not rd:
                continue
            med_nn = float(np.median(nn_dk))
            med_r = float(np.median(rd))
            if med_r > 0:
                contrasts.append(med_nn / med_r)
            cur = set(nn_k)
            if prev_set is not None and prev_t is not None and abs(t - prev_t) <= W:
                inter = len(cur & prev_set)
                uni = len(cur | prev_set)
                j_obs = inter / uni if uni else 0.0
                pool = [int(s) for s in c_idx if embargo_ok(t, int(s), W) and int(s) != t]
                if len(pool) >= k:
                    a = set(int(x) for x in rng.choice(pool, size=k, replace=False))
                    b = set(int(x) for x in rng.choice(pool, size=k, replace=False))
                    j_null = len(a & b) / len(a | b) if (a | b) else 0.0
                else:
                    j_null = 0.0
                jacc_obs.append(j_obs)
                jacc_null.append(j_null)
            prev_set = cur
            prev_t = t

        results["k"][str(k)] = {
            "CAL_G1_contrast_median": float(np.median(contrasts)) if contrasts else None,
            "CAL_G1_contrast_q10": float(np.quantile(contrasts, 0.1)) if contrasts else None,
            "CAL_G1_contrast_q90": float(np.quantile(contrasts, 0.9)) if contrasts else None,
            "CAL_G2_EP": (
                float(np.mean(jacc_obs) - np.mean(jacc_null))
                if jacc_obs and jacc_null
                else None
            ),
            "n_contrast": len(contrasts),
        }

    for mult in RECURRENCE_H_MULT:
        H = mult * W
        rates = []
        for t in q_idx:
            t = int(t)
            if t not in nn_cache:
                continue
            nn_idx = nn_cache[t][0]
            if not nn_idx:
                continue
            kk = min(10, len(nn_idx))
            rates.append(np.mean([1.0 if abs(t - s) > H else 0.0 for s in nn_idx[:kk]]))
        results["CAL_G3"][f"H={H}"] = {
            "R_mean": float(np.mean(rates)) if rates else None,
            "n": len(rates),
        }

    # CAL-G4: lighter probe set
    for c in PERTURB_CS:
        rng_p = np.random.default_rng(seed + int(1000 * c))
        sigma = float(np.std(r)) + 1e-12
        r_p = r + c * sigma * rng_p.normal(size=r.shape)
        emb_p = build_embeddings(r_p, union_idx, W, embed_fn)
        probes = q_idx[:: max(1, len(q_idx) // 16)][:16]
        ranks_o: list[float] = []
        ranks_p: list[float] = []
        cans = c_idx[:: max(1, len(c_idx) // 32)][:32]
        for t in probes:
            t = int(t)
            d0 = []
            d1 = []
            for s in cans:
                s = int(s)
                if not embargo_ok(t, s, W) or s == t:
                    continue
                if t not in emb or s not in emb or t not in emb_p or s not in emb_p:
                    continue
                d0.append(dist_fn(emb[t], emb[s]))
                d1.append(dist_fn(emb_p[t], emb_p[s]))
            if len(d0) < 5:
                continue
            ranks_o.extend(np.argsort(np.argsort(d0)).tolist())
            ranks_p.extend(np.argsort(np.argsort(d1)).tolist())
        results["CAL_G4"][f"c={c}"] = {
            "spearman_rank": (
                _spearman(np.asarray(ranks_o, float), np.asarray(ranks_p, float))
                if ranks_o
                else None
            )
        }

    pair_n = 120
    ts = rng.choice(q_idx, size=min(pair_n, q_idx.size), replace=False)
    nuisance = {k: [] for k in ("dG", "dRV", "dMean", "dTrend", "dSkew", "dKurt", "dGVOL")}
    for t in ts:
        t = int(t)
        pool = [int(s) for s in c_idx if embargo_ok(t, int(s), W) and int(s) != t]
        if not pool or t not in emb:
            continue
        s = int(rng.choice(pool))
        if s not in emb:
            continue
        wt = r[t - W + 1 : t + 1]
        ws = r[s - W + 1 : s + 1]
        nuisance["dG"].append(dist_fn(emb[t], emb[s]))
        nuisance["dRV"].append(abs(np.mean(wt * wt) - np.mean(ws * ws)))
        nuisance["dMean"].append(abs(wt.mean() - ws.mean()))
        nuisance["dTrend"].append(abs((wt[-1] - wt[0]) - (ws[-1] - ws[0])))
        nuisance["dSkew"].append(abs(_skew(wt) - _skew(ws)))
        nuisance["dKurt"].append(abs(_kurt(wt) - _kurt(ws)))
        nuisance["dGVOL"].append(gvol_distance(log_rv(r, t, W), log_rv(r, s, W)))
    dG = np.asarray(nuisance["dG"], float)
    results["CAL_G5"] = {
        key: _spearman(dG, np.asarray(val, float))
        for key, val in nuisance.items()
        if key != "dG" and len(val) == len(dG) and len(dG) >= 5
    }
    results["CAL_G5"]["n_pairs"] = int(len(dG))
    results["CAL_6"] = compute_cal6(world, nn_cache, q_idx, W, K_NEIGHBORS[1])
    return results


def _skew(w: np.ndarray) -> float:
    w = w - w.mean()
    s = w.std()
    if s <= 0:
        return 0.0
    return float(np.mean((w / s) ** 3))


def _kurt(w: np.ndarray) -> float:
    w = w - w.mean()
    s = w.std()
    if s <= 0:
        return 0.0
    return float(np.mean((w / s) ** 4) - 3.0)


def compute_cal6(
    world: WorldBundle,
    nn_cache: dict[int, tuple],
    q_idx: np.ndarray,
    W: int,
    k: int,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "oracle_status": world.oracle_status.value,
        "kind": world.oracle_meta.get("kind"),
    }
    if world.oracle_status.value == "NOT_APPLICABLE":
        out["note"] = "S0-class: no positive oracle; structure => false positive audit"
        return out
    if world.oracle_status.value == "INVALID":
        out["note"] = "oracle INVALID — CAL-6 NOT INTERPRETABLE"
        out["interpretable"] = False
        return out

    kind = world.oracle_meta.get("kind")
    if kind == "categorical" and world.oracle_labels is not None:
        labels = world.oracle_labels
        exclude = set(world.oracle_meta.get("exclude_labels", []))
        hits = []
        for t in q_idx:
            t = int(t)
            if t not in nn_cache:
                continue
            zt = int(labels[t])
            if zt in exclude:
                continue
            nn_idx = nn_cache[t][0][:k]
            if not nn_idx:
                continue
            same = [
                1.0
                for s in nn_idx
                if int(labels[int(s)]) == zt and int(labels[int(s)]) not in exclude
            ]
            hits.append(len(same) / len(nn_idx))
        n_cls = len(world.oracle_meta.get("classes", {})) or 3
        out["P_mean"] = float(np.mean(hits)) if hits else None
        out["chance"] = 1.0 / n_cls
        out["n"] = len(hits)
        out["interpretable"] = True
        return out

    if kind == "volatility" and "h" in world.latent:
        h = world.latent["h"]
        dG = []
        dH = []
        for t in q_idx[::2]:
            t = int(t)
            if t not in nn_cache:
                continue
            nn_idx, nn_d, _, _ = nn_cache[t]
            for s, d in zip(nn_idx[:k], nn_d[:k]):
                dG.append(d)
                dH.append(abs(float(h[t] - h[int(s)])))
        out["OR_VOL_spearman"] = (
            _spearman(np.asarray(dG), np.asarray(dH)) if dG else None
        )
        out["n"] = len(dG)
        out["interpretable"] = True
        return out

    if kind == "latent_distance" and "z" in world.latent:
        z = world.latent["z"]
        dG = []
        dZ = []
        for t in q_idx[::2]:
            t = int(t)
            if t not in nn_cache:
                continue
            nn_idx, nn_d, _, _ = nn_cache[t]
            for s, d in zip(nn_idx[:k], nn_d[:k]):
                dG.append(d)
                dZ.append(float(np.linalg.norm(z[t] - z[int(s)])))
        out["OR_spearman"] = _spearman(np.asarray(dG), np.asarray(dZ)) if dG else None
        out["n"] = len(dG)
        out["interpretable"] = True
        return out

    out["interpretable"] = False
    out["note"] = "unhandled oracle kind"
    return out
