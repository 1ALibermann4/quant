"""Test basic multiprocessing on Windows."""

from concurrent.futures import ProcessPoolExecutor
import time


def square(x):
    return x * x


if __name__ == "__main__":
    print("Testing ProcessPoolExecutor...")
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(square, i) for i in range(5)]
        results = [f.result() for f in futures]
    print(f"Results: {results}")
