"""Shared types for I04-CAL."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import numpy as np


class WorldStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    INCONCLUSIVE = "INCONCLUSIVE"


class OracleStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ExecStatus(str, Enum):
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    FAILED_TECHNICAL = "FAILED_TECHNICAL"


class GeometryStatus(str, Enum):
    EXECUTABLE = "EXECUTABLE"
    DEGENERATE = "DEGENERATE"
    PARAMETER_FRAGILE = "PARAMETER_FRAGILE"
    HOLD = "HOLD"
    INVALID_UNDER_CONTRACT = "INVALID_UNDER_CONTRACT"


@dataclass(slots=True)
class WorldBundle:
    """One synthetic realization."""

    world_id: str
    b: int
    seed: int
    returns: np.ndarray  # float64 length N (post burn-in unless noted)
    latent: dict[str, Any] = field(default_factory=dict)
    oracle_labels: np.ndarray | None = None  # categorical int codes or None
    oracle_meta: dict[str, Any] = field(default_factory=dict)
    world_status: WorldStatus = WorldStatus.VALID
    oracle_status: OracleStatus = OracleStatus.NOT_APPLICABLE
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class GeometrySpec:
    geometry_id: str
    variant_id: str
    params: dict[str, Any]
    status: GeometryStatus = GeometryStatus.EXECUTABLE
