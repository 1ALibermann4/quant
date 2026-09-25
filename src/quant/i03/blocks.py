"""Deterministic temporal blocks (I03-PREREG-v0.1 §5)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i03.params import I03Config


@dataclass(frozen=True, slots=True)
class TemporalBlock:
    """One contiguous block ``B_p`` (1-based ``period`` label)."""

    period: int  # 1..P
    start: int  # inclusive index into returns calendar
    end: int  # inclusive
    indices: np.ndarray  # intp array of member indices


def build_blocks(T: int, cfg: I03Config) -> tuple[TemporalBlock, ...]:
    """Split analysis indices ``{0..T-1}`` per prereg §5.

    Scientific calendar for returns uses the I02 convention that scientific
    observations live at indices ``1..T-1`` with ``returns[0]`` padding, but
    **block cuts are on the full length-``T`` index set**
    ``{t_0,...,t_{T-1}} = {0,...,T-1}`` as written in the prereg. Pool
    membership still requires ``X_s`` defined (which excludes index 0).
    """

    if T < 1:
        raise ValueError("T must be positive")
    P = cfg.P
    L = T // P
    R = T % P
    blocks: list[TemporalBlock] = []
    # B1, B2 exact length L; B3 gets L+R
    boundaries = [0, L, 2 * L, 3 * L + R]
    if boundaries[-1] != T:
        raise RuntimeError("block construction invariant failed")
    for p in range(1, P + 1):
        start = boundaries[p - 1]
        end = boundaries[p] - 1
        idx = np.arange(start, end + 1, dtype=np.intp)
        blocks.append(TemporalBlock(period=p, start=start, end=end, indices=idx))
    return tuple(blocks)


def block_membership(blocks: tuple[TemporalBlock, ...], t: int) -> int:
    """Return 1-based period containing ``t``, or 0 if none."""

    for b in blocks:
        if b.start <= t <= b.end:
            return b.period
    return 0
