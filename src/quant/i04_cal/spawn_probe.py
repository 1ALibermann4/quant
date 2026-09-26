"""Spawn probe for Windows multiprocessing testing.

This module contains module-level functions that can be imported
by spawned processes on Windows.
"""

import multiprocessing
from typing import Any


def spawn_worker_primitive(x: int) -> int:
    """Simple worker function that accepts and returns primitives."""
    return x * 2


def spawn_worker_dict(x: int, data: dict[str, Any]) -> int:
    """Worker function that accepts dict argument."""
    return x + len(data)


def spawn_worker_task(task: dict[str, Any]) -> dict[str, Any]:
    """Worker function that accepts and returns dict (task-like)."""
    return {
        "input": task["value"],
        "result": task["value"] * 3,
        "worker_id": multiprocessing.current_process().name,
    }
