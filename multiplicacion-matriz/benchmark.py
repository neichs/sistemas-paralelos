"""
benchmark.py — Ejecuta todos los métodos de multiplicación de matrices y compara resultados.

Uso:
    python benchmark.py [--seed 2026] [--methods sequential threading multiprocessing numba]

    Modo combinaciones (default): itera sobre todos los workers y complexidades predefinidos.
    Modo manual:  python benchmark.py --complexity 512 --workers 4

Métodos disponibles:
    sequential, threading, multiprocessing, numba

Salida: tabla con N, workers, método, tiempo (s), checksum, speed-up y eficiencia (%).
"""

import argparse
import csv
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

ALL_WORKERS = [1, 4, 10, 24]
ALL_COMPLEXITIES = [512, 1024]
DEFAULT_SEED = 2026


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark de multiplicación de matrices")
    parser.add_argument("--complexity", type=int, default=None,
                        help="Tamaño N de la matriz. Si se omite, corre todas las combinaciones.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--workers", type=int, default=None,
                        help="Número de workers. Si se omite, corre todas las combinaciones.")
    parser.add_argument(
        "--methods",
        nargs="+",
        default=["sequential", "threading", "multiprocessing", "numba"],
        help="Métodos a ejecutar (default: todos los disponibles)",
    )
    return parser.parse_args()


def generate_matrices_list(n: int, seed: int):
    import random
    random.seed(seed)
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    return A, B


def generate_matrices_numpy(n: int, seed: int):
    import random
    import numpy as np
    random.seed(seed)
    flat_a = [random.random() for _ in range(n * n)]
    flat_b = [random.random() for _ in range(n * n)]
    A = np.array(flat_a, dtype=np.float64).reshape(n, n)
    B = np.array(flat_b, dtype=np.float64).reshape(n, n)
    return A, B


def compute_checksum(C, decimals: int = 6) -> float:
    try:
        return round(float(C.sum()), decimals)
    except AttributeError:
        return round(sum(sum(row) for row in C), decimals)


def run_method(name: str, matrices_list, matrices_numpy, n: int, workers: int):
    A_list, B_list = matrices_list
    A_np, B_np = matrices_numpy

    if name == "sequential":
        from mat_sequential import matmul_sequential
        t = time.perf_counter()
        C = matmul_sequential(A_list, B_list, n)
        elapsed = time.perf_counter() - t

    elif name == "threading":
        from mat_threading import matmul_threading
        t = time.perf_counter()
        C = matmul_threading(A_list, B_list, n, workers)
        elapsed = time.perf_counter() - t

    elif name == "multiprocessing":
        from mat_multiprocessing import matmul_multiprocessing
        t = time.perf_counter()
        C = matmul_multiprocessing(A_list, B_list, n, workers)
        elapsed = time.perf_counter() - t

    elif name == "numba":
        try:
            from mat_numba import matmul_numba, _warm_up
            print("    (calentando JIT numba...)", flush=True)
            _warm_up(workers)
            t = time.perf_counter()
            C = matmul_numba(A_np, B_np, n, workers)
            elapsed = time.perf_counter() - t
        except ImportError as e:
            print(f"  [SKIP] numba no disponible: {e}")
            return None

    else:
        print(f"  [SKIP] Método '{name}' no implementado todavía.")
        return None

    checksum = compute_checksum(C)
    return elapsed, checksum


def run_combination(n: int, workers_list: list, seed: int, methods: list) -> list:
    """Runs all methods for a given N. Returns list of result dicts."""
    print(f"\n  Generando matrices N={n}...")
    matrices_list = generate_matrices_list(n, seed)
    matrices_numpy = generate_matrices_numpy(n, seed)

    rows = []

    # Run sequential once (no workers)
    if "sequential" in methods:
        print(f"    [{n}] sequential...", flush=True)
        result = run_method("sequential", matrices_list, matrices_numpy, n, 1)
        if result is not None:
            elapsed, checksum = result
            rows.append({"n": n, "workers": "-", "method": "sequential", "elapsed": elapsed, "checksum": checksum})

    # Run worker-dependent methods (threading, multiprocessing, numba) for each worker count
    worker_methods = [m for m in methods if m in ("threading", "multiprocessing", "numba")]
    for w in workers_list:
        for method in worker_methods:
            print(f"    [{n}] {method} workers={w}...", flush=True)
            result = run_method(method, matrices_list, matrices_numpy, n, w)
            if result is not None:
                elapsed, checksum = result
                rows.append({"n": n, "workers": w, "method": method, "elapsed": elapsed, "checksum": checksum})

    return rows


def compute_baselines(all_rows: list) -> dict:
    baselines = {}
    for row in all_rows:
        if row["method"] == "sequential":
            baselines[row["n"]] = row["elapsed"]
    for row in all_rows:
        n = row["n"]
        if n not in baselines:
            baselines[n] = max(r["elapsed"] for r in all_rows if r["n"] == n)
    return baselines


def print_table(all_rows: list, baselines: dict):
    print()
    header = f"  {'N':>6}  {'Workers':>8}  {'Método':<22} {'Tiempo (s)':>12} {'Checksum':>14} {'Speed-up':>10} {'Eficiencia':>12}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    last_n = None
    for row in all_rows:
        n = row["n"]
        w = row["workers"]
        method = row["method"]
        elapsed = row["elapsed"]
        checksum = row["checksum"]

        speedup = baselines[n] / elapsed
        effective_w = 1 if method == "sequential" else (w if isinstance(w, int) else 1)
        efficiency = (speedup / effective_w) * 100

        sep = "  " if n == last_n else "\n  "
        last_n = n

        w_str = str(w) if isinstance(w, int) else w
        print(f"{sep}{n:>6}  {w_str:>8}  {method:<22} {elapsed:>12.6f} {checksum:>14.6f} {speedup:>10.4f}x {efficiency:>11.2f}%")

    print()


def write_csv(all_rows: list, path: str, baselines: dict):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "workers", "method", "elapsed_s", "checksum", "speedup", "efficiency_pct"])
        for row in all_rows:
            n, w, method = row["n"], row["workers"], row["method"]
            elapsed, checksum = row["elapsed"], row["checksum"]
            speedup = baselines[n] / elapsed
            effective_w = 1 if method == "sequential" else (w if isinstance(w, int) else 1)
            efficiency = (speedup / effective_w) * 100
            writer.writerow([n, w, method, f"{elapsed:.6f}", f"{checksum:.6f}", f"{speedup:.4f}", f"{efficiency:.2f}"])
    print(f"  Resultados guardados en: {path}")


def validate_checksums(all_rows: list):
    from collections import defaultdict
    by_n = defaultdict(dict)
    for row in all_rows:
        key = f"{row['method']}(w={row['workers']})"
        by_n[row["n"]][key] = row["checksum"]

    for n, checksums in sorted(by_n.items()):
        unique = set(checksums.values())
        if len(unique) == 1:
            print(f"  Checksum N={n}: OK — todos los métodos coinciden ({next(iter(unique))}).")
        else:
            print(f"  ADVERTENCIA N={n}: checksums distintos entre métodos:")
            for m, c in checksums.items():
                print(f"    {m}: {c}")
    print()


def main():
    args = parse_args()
    seed = args.seed
    methods = args.methods

    # Decide whether to run all combinations or a single one
    if args.complexity is None and args.workers is None:
        complexities = ALL_COMPLEXITIES
        workers_list = ALL_WORKERS
        print(f"\nBenchmark completo — N={complexities}, workers={workers_list}, seed={seed}")
    else:
        complexities = [args.complexity or ALL_COMPLEXITIES[0]]
        workers_list = [args.workers or ALL_WORKERS[1]]
        print(f"\nBenchmark — N={complexities}, workers={workers_list}, seed={seed}")

    print("=" * 80)

    all_rows = []
    for n in complexities:
        rows = run_combination(n, workers_list, seed, methods)
        all_rows.extend(rows)

    baselines = compute_baselines(all_rows)
    print_table(all_rows, baselines)
    validate_checksums(all_rows)

    csv_path = os.path.join(os.path.dirname(__file__), "resultados_benchmark.csv")
    write_csv(all_rows, csv_path, baselines)


if __name__ == "__main__":
    main()
