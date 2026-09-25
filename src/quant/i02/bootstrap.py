"""Bootstrap block-length constants and contract-gap gate.

Frozen scientific parameters ``b*`` and sensitivity set are available.
The unique moving/block bootstrap **inference algorithm** is not fully
specified — calling :func:`moving_block_bootstrap` raises
:class:`ImplementationContractGap`.
"""

from __future__ import annotations

from quant.i02.contract_gaps import (
    BOOTSTRAP_ALGORITHM_GAP,
    ImplementationContractGap,
)
from quant.i02.params import DEFAULT_PARAMS, I02Params


def frozen_block_lengths(params: I02Params = DEFAULT_PARAMS) -> tuple[int, tuple[int, ...]]:
    """Return ``(b_star, b_sensitivity)`` without inventing an algorithm."""

    return params.b_star, params.b_sensitivity


def moving_block_bootstrap(*_args, **_kwargs):
    """Intentionally unimplemented — see ``BOOTSTRAP_ALGORITHM_GAP``."""

    raise ImplementationContractGap(BOOTSTRAP_ALGORITHM_GAP)
