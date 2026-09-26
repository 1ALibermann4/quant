"""Simple test of caching benefit."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.gates import build_embeddings
from quant.i04_cal.geometries import g0_embed
import numpy as np


def test_cache_benefit():
    """Test caching benefit on repeated calls."""
    r = np.random.default_rng(0).normal(size=8192)
    W = 20
    indices = np.arange(W - 1, 1000, 8)  # ~120 indices
    cache_key = ("test", 0, W, "G0", "default")

    # First call (cold)
    t0 = time.perf_counter()
    emb1 = build_embeddings(r, indices, W, g0_embed, cache_key=cache_key)
    t1 = time.perf_counter()
    cold_time = t1 - t0

    # Second call (warm)
    t0 = time.perf_counter()
    emb2 = build_embeddings(r, indices, W, g0_embed, cache_key=cache_key)
    t1 = time.perf_counter()
    warm_time = t1 - t0

    print(f"Cold: {cold_time:.6f}s")
    print(f"Warm: {warm_time:.6f}s")
    print(f"Speedup: {cold_time / warm_time:.0f}x")

    # Verify identical
    assert emb1 == emb2
    print("✓ Results identical")


if __name__ == "__main__":
    test_cache_benefit()
