"""Run spawn probe to test Windows multiprocessing.

This script tests whether native Windows spawn works with module-level
functions in a proper package.
"""

import multiprocessing
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"


def test_spawn_primitive():
    """Test spawn with primitive worker."""
    print("Test 1: Primitive worker")
    from quant.i04_cal.spawn_probe import spawn_worker_primitive

    print(f"  Worker module: {spawn_worker_primitive.__module__}")
    print(f"  Worker qualname: {spawn_worker_primitive.__qualname__}")

    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(processes=2) as pool:
        results = pool.map(spawn_worker_primitive, [1, 2, 3])
    print(f"  Results: {results}")
    assert results == [2, 4, 6]
    print("  PASSED")


def test_spawn_dict():
    """Test spawn with dict worker."""
    print("\nTest 2: Dict worker")
    from quant.i04_cal.spawn_probe import spawn_worker_dict

    ctx = multiprocessing.get_context("spawn")
    test_dict = {"a": 1, "b": 2}
    with ctx.Pool(processes=2) as pool:
        results = pool.starmap(
            spawn_worker_dict,
            [(5, test_dict), (10, test_dict)],
        )
    print(f"  Results: {results}")
    assert results == [7, 12]
    print("  PASSED")


def test_spawn_task():
    """Test spawn with task-like worker."""
    print("\nTest 3: Task worker")
    from quant.i04_cal.spawn_probe import spawn_worker_task

    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(processes=2) as pool:
        results = pool.map(
            spawn_worker_task,
            [{"value": 1}, {"value": 2}, {"value": 3}],
        )
    print(f"  Results: {results}")
    assert len(results) == 3
    assert all(r["result"] == r["input"] * 3 for r in results)
    print("  PASSED")


def main():
    """Run all spawn tests."""
    print("Windows Spawn Probe")
    print("=" * 60)
    print("Testing native Windows spawn with module-level workers")
    print("=" * 60)

    try:
        test_spawn_primitive()
    except Exception as e:
        print(f"  FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

    try:
        test_spawn_dict()
    except Exception as e:
        print(f"  FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

    try:
        test_spawn_task()
    except Exception as e:
        print(f"  FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("All tests PASSED - Windows spawn works correctly")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
