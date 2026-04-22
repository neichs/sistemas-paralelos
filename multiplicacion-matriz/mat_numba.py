"""
mat_numba.py — Multiplicación de matrices NxN con Numba JIT (njit).

Uso:
    python mat_numba.py --complexity 512 --seed 2026

El parámetro --workers se acepta por compatibilidad con el benchmark pero se ignora
(este script usa numba.njit sin paralelismo explícito de threads/procesos).

La primera llamada incluye el tiempo de compilación JIT; se informa por separado.
Checksum: debe coincidir con el de los demás métodos para la misma --complexity y --seed.
"""

import argparse
import time
import random

import numpy as np
import numba
from numba import njit, prange


@njit(parallel=True, cache=True)
def _matmul_njit(A, B, C, n):
    """Triple bucle compilado a código nativo por numba.njit con paralelismo en filas."""
    for i in prange(n):
        for k in range(n):
            a_ik = A[i, k]
            for j in range(n):
                C[i, j] += a_ik * B[k, j]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multiplicación de matrices con Numba JIT (njit)"
    )
    parser.add_argument("--complexity", type=int, default=512,
                        help="Tamaño N de las matrices NxN (default: 512)")
    parser.add_argument("--seed", type=int, default=2026,
                        help="Semilla para la generación aleatoria (default: 2026)")
    parser.add_argument("--workers", type=int, default=1,
                        help="(Ignorado en modo numba njit, incluido por compatibilidad)")
    return parser.parse_args()


def generate_matrices(n: int, seed: int):
    """Genera dos matrices NxN numpy usando el mismo RNG que el resto de métodos."""
    random.seed(seed)
    flat_a = [random.random() for _ in range(n * n)]
    flat_b = [random.random() for _ in range(n * n)]
    A = np.array(flat_a, dtype=np.float64).reshape(n, n)
    B = np.array(flat_b, dtype=np.float64).reshape(n, n)
    return A, B


def matmul_numba(A: np.ndarray, B: np.ndarray, n: int, workers: int = 1) -> np.ndarray:
    numba.set_num_threads(workers)
    C = np.zeros((n, n), dtype=np.float64)
    _matmul_njit(A, B, C, n)
    return C


def compute_checksum(C: np.ndarray, decimals: int = 6) -> float:
    return round(float(C.sum()), decimals)


def _warm_up(workers: int = 1):
    """Fuerza la compilación JIT con matrices 2x2 para no contaminar el benchmark."""
    numba.set_num_threads(workers)
    a = np.ones((2, 2), dtype=np.float64)
    b = np.ones((2, 2), dtype=np.float64)
    c = np.zeros((2, 2), dtype=np.float64)
    _matmul_njit(a, b, c, 2)


def main():
    args = parse_args()
    n = args.complexity
    seed = args.seed

    print(f"[mat_numba] N={n}  seed={seed}  workers=1 (numba njit)")

    print("  Calentando JIT (compilación numba)...")
    t_jit = time.perf_counter()
    _warm_up()
    t_jit = time.perf_counter() - t_jit
    print(f"  Tiempo JIT warm-up: {t_jit:.4f} s")

    print("  Generando matrices...")
    A, B = generate_matrices(n, seed)

    print("  Multiplicando...")
    t_start = time.perf_counter()
    C = matmul_numba(A, B, n)
    elapsed = time.perf_counter() - t_start

    checksum = compute_checksum(C)

    print(f"  Tiempo   : {elapsed:.6f} s")
    print(f"  Checksum : {checksum}")
    print(f"  Speed-up : (ejecutar benchmark.py para comparar con baseline)")


if __name__ == "__main__":
    main()
