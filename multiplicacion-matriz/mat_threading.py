"""
mat_threading.py — Multiplicación de matrices NxN con threading.

Uso:
    python mat_threading.py --complexity 512 --seed 2026 --workers 4

Cada thread calcula un bloque contiguo de filas de la matriz resultado C.
Por el GIL de Python, el paralelismo real en trabajo CPU-bound es limitado.
"""

import argparse
import time
import threading


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multiplicación de matrices con threading"
    )
    parser.add_argument("--complexity", type=int, default=512)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--workers", type=int, default=4)
    return parser.parse_args()


def generate_matrices(n: int, seed: int):
    import random
    random.seed(seed)
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    return A, B


def _worker(A, B, C, row_start: int, row_end: int, n: int) -> None:
    """Calcula las filas [row_start, row_end) de C = A × B."""
    for i in range(row_start, row_end):
        for k in range(n):
            a_ik = A[i][k]
            for j in range(n):
                C[i][j] += a_ik * B[k][j]


def matmul_threading(A, B, n: int, num_workers: int):
    C = [[0.0] * n for _ in range(n)]
    chunk = (n + num_workers - 1) // num_workers  # ceil division
    threads = []
    for w in range(num_workers):
        row_start = w * chunk
        row_end = min(row_start + chunk, n)
        if row_start >= n:
            break
        t = threading.Thread(target=_worker, args=(A, B, C, row_start, row_end, n))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return C


def compute_checksum(C, decimals: int = 6) -> float:
    total = sum(sum(row) for row in C)
    return round(total, decimals)


def main():
    args = parse_args()
    n = args.complexity
    seed = args.seed
    workers = args.workers

    print(f"[mat_threading] N={n}  seed={seed}  workers={workers}")

    print("  Generando matrices...")
    A, B = generate_matrices(n, seed)

    print("  Multiplicando...")
    t_start = time.perf_counter()
    C = matmul_threading(A, B, n, workers)
    elapsed = time.perf_counter() - t_start

    checksum = compute_checksum(C)

    print(f"  Tiempo   : {elapsed:.6f} s")
    print(f"  Checksum : {checksum}")
    print(f"  Workers  : {workers}")


if __name__ == "__main__":
    main()
