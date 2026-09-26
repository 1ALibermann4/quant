"""Frozen I04-CAL configuration and seed map (SPEC v0.2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


SPEC_ID = "I04-CAL-SPEC-v0.2"
B_WORLD = 32
WINDOWS: tuple[int, ...] = (20, 40, 60)
QUERY_STRIDE = 8
CANDIDATE_STRIDE = 4
# Expensive O(W^2) geometries: coarser preregistered strides (frozen before CAL)
EXPENSIVE_QUERY_STRIDE = 32
EXPENSIVE_CANDIDATE_STRIDE = 32
EXPENSIVE_GEOMETRIES: frozenset[str] = frozenset({"G1"})
K_NEIGHBORS: tuple[int, ...] = (5, 10, 20)
N_POST_BURNIN = 8192

WORLD_INDEX: dict[str, int] = {
    "S0a": 0,
    "S0b": 1,
    "S1": 2,
    "S2": 3,
    "S3": 4,
    "S4": 5,
    "S5": 6,
    "S6": 7,
    "S7": 8,
}

# Soft-DTW gamma grid
G1_GAMMAS: tuple[float, ...] = (0.1, 1.0, 10.0)
# Sliced-Wasserstein
G2_DS: tuple[int, ...] = (2, 3)
G2_L = 32
# Signatures
G3_MS: tuple[int, ...] = (2, 3)
# AIRM
G5_PS: tuple[int, ...] = (2, 3)
G5_LAMBDA = 1e-3
# Ordinal
GORD_DS: tuple[int, ...] = (3, 4)
GORD_TAU = 1
# Perturbation
PERTURB_CS: tuple[float, ...] = (0.05, 0.1, 0.2)
# Recurrence horizons as multiples of W
RECURRENCE_H_MULT: tuple[int, ...] = (2, 5, 10)
# Observability diagnostic threshold (OPEN GOVERNANCE documented)
OBSERVABILITY_SPEARMAN_MIN = 0.25
# S7 noise fractions of sigma_x
S7_NOISE_FRAC: tuple[float, ...] = (0.0, 0.05, 0.1)
# S1 SV
S1_PHI = 0.98
S1_SIGMA_H = 0.15
S1_BURNIN = 2000


def world_seed(world: str, b: int) -> int:
    if world not in WORLD_INDEX:
        raise KeyError(f"unknown world {world}")
    if not (0 <= int(b) < B_WORLD):
        raise ValueError("b out of range")
    return 100_000 * WORLD_INDEX[world] + int(b)


def variant_seed(tag: str, b: int) -> int:
    """Secondary variants (e.g. S7 logistic)."""
    tags = {"S7_logistic": 80}
    if tag not in tags:
        raise KeyError(tag)
    return 100_000 * tags[tag] + int(b)


def geometry_aux_seed(geometry_id: int) -> int:
    return 100_000 * 900 + int(geometry_id)


@dataclass(frozen=True, slots=True)
class CalConfig:
    """Operational run config (not a scientific retune surface)."""

    spec_id: str = SPEC_ID
    B: int = B_WORLD
    windows: tuple[int, ...] = WINDOWS
    query_stride: int = QUERY_STRIDE
    k_neighbors: tuple[int, ...] = K_NEIGHBORS
    workers: int = 1
    include_hold_geometries: bool = False  # G6 never in CAL-qualified path
    worlds: tuple[str, ...] = tuple(WORLD_INDEX.keys())
    geometries: tuple[str, ...] = (
        "G0",
        "G1",
        "G2",
        "G3",
        "G4",
        "G5",
        "G7",
        "GORD",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_id": self.spec_id,
            "B": self.B,
            "windows": list(self.windows),
            "query_stride": self.query_stride,
            "k_neighbors": list(self.k_neighbors),
            "workers": self.workers,
            "worlds": list(self.worlds),
            "geometries": list(self.geometries),
        }


DEFAULT_CAL_CONFIG = CalConfig()
