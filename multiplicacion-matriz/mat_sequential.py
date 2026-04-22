"""
mat_sequential.py — Multiplicación de matrices NxN (método secuencial tradicional).

Uso:
    python mat_sequential.py --complexity 512 --seed 2026

El parámetro --workers se acepta por compatibilidad con el benchmark pero se ignora
(este script es puramente secuencial, workers=1 siempre).

Checksum: suma de todos los elementos de la matriz resultado redondeada a 6 decimales.
El checksum debe ser idéntico al producido por todos los demás métodos para la misma
combinación de --complexity y --seed.
"""

import argparse
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multiplicación de matrices secuencial (método tradicional)"
    )
    parser.add_argument(
        "--complexity",
        type=int,
        default=512,
        help="Tamaño N de las matrices NxN (default: 512)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="Semilla para la generación aleatoria (default: 2026)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="(Ignorado en modo secuencial, incluido por compatibilidad)",
    )
    return parser.parse_args()


def generate_matrices(n: int, seed: int):
    """Genera dos matrices NxN de floats usando la semilla dada."""
    import random

    random.seed(seed)

    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    return A, B


def matmul_sequential(A, B, n: int):
    """
    Multiplicación de matrices cuadradas NxN mediante el algoritmo triple bucle
    (método tradicional îˆ C[i][j] += A[i][k] * B[k][j]).
    """
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            a_ik = A[i][k]
            for j in range(n):
                C[i][j] += a_ik * B[k][j]
    return C


def compute_checksum(C, decimals: int = 6) -> float:
    """
    Checksum reproducible: suma total de todos los elementos de C,
    redondeada a `decimals` posiciones decimales.
    """
    total = sum(sum(row) for row in C)
    return round(total, decimals)


def main():
    args = parse_args()
    n = args.complexity
    seed = args.seed

    print(f"[mat_sequential] N={n}  seed={seed}  workers=1 (secuencial)")

    print("  Generando matrices...")
    A, B = generate_matrices(n, seed)

    print("  Multiplicando...")
    t_start = time.perf_counter()
    C = matmul_sequential(A, B, n)
    elapsed = time.perf_counter() - t_start

    checksum = compute_checksum(C)

    print(f"  Tiempo   : {elapsed:.6f} s")
    print(f"  Checksum : {checksum}")
    print(f"  Speed-up : 1.0 (baseline)")
    print(f"  Eficiencia: 100.00 %")


if __name__ == "__main__":
    main()
