"""
mat_multiprocessing.py — Multiplicación de matrices NxN con multiprocessing.

Uso:
    python mat_multiprocessing.py --complexity 512 --seed 2026 --workers 4

Cada proceso calcula un bloque contiguo de filas de la matriz resultado C.
Al usar procesos separados se evita el GIL, logrando paralelismo real en CPU-bound.
"""

import argparse
import time
import multiprocessing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multiplicación de matrices con multiprocessing"
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


def _worker(args):
    """Calcula las filas [row_start, row_end) de C = A × B y las devuelve."""
    A, B, row_start, row_end, n = args
    rows = []
    for i in range(row_start, row_end):
        row = [0.0] * n
        for k in range(n):
            a_ik = A[i][k]
            for j in range(n):
                row[j] += a_ik * B[k][j]
        rows.append(row)
    return row_start, rows


def matmul_multiprocessing(A, B, n: int, num_workers: int):
    chunk = (n + num_workers - 1) // num_workers
    tasks = []
    for w in range(num_workers):
        row_start = w * chunk
        row_end = min(row_start + chunk, n)
        if row_start >= n:
            break
        tasks.append((A, B, row_start, row_end, n))

    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(_worker, tasks)

    C = [[0.0] * n for _ in range(n)]
    for row_start, rows in results:
        for offset, row in enumerate(rows):
            C[row_start + offset] = row
    return C


def compute_checksum(C, decimals: int = 6) -> float:
    total = sum(sum(row) for row in C)
    return round(total, decimals)


def main():
    args = parse_args()
    n = args.complexity
    seed = args.seed
    workers = args.workers

    print(f"[mat_multiprocessing] N={n}  seed={seed}  workers={workers}")

    print("  Generando matrices...")
    A, B = generate_matrices(n, seed)

    print("  Multiplicando...")
    t_start = time.perf_counter()
    C = matmul_multiprocessing(A, B, n, workers)
    elapsed = time.perf_counter() - t_start

    checksum = compute_checksum(C)

    print(f"  Tiempo   : {elapsed:.6f} s")
    print(f"  Checksum : {checksum}")
    print(f"  Workers  : {workers}")


if __name__ == "__main__":
    main()
