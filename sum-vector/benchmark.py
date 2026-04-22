import csv
import numpy as np
from time import time
import concurrent.futures


def sum_elements_seq(v: np.ndarray) -> float:
    """Calcula la suma de los elementos de un array de NumPy."""
    res: float = 0.0
    for e in v:
        res += float(e)
    return res


def run_sequential(arr: np.ndarray) -> float:
    init = time()
    result = sum_elements_seq(arr)
    end = time() - init
    return end


def run_threading(arr: np.ndarray, p: int) -> float:
    init = time()
    chunks = np.array_split(arr, p)
    with concurrent.futures.ThreadPoolExecutor(max_workers=p) as executor:
        total_sum = sum(executor.map(sum_elements_seq, chunks))
    end = time() - init
    return end


def run_multiprocessing(arr: np.ndarray, p: int) -> float:
    init = time()
    # Para evitar copiar todo el array original múltiples veces por el overhead de pickle
    chunks = [chunk.copy() for chunk in np.array_split(arr, p)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=p) as executor:
        total_sum = sum(executor.map(sum_elements_seq, chunks))
    end = time() - init
    return end


def main():
    complexities = [12, 1_000_000, 100_000_000]
    workers = [1, 2, 4, 8, 16]
    cores = 32

    results = []

    for c in complexities:
        print(f"\n========================================")
        print(f"Evaluando complejidad C = {c}")
        print(f"========================================")
        print("Generando vector aleatorio...")
        arr = np.random.rand(c)

        # 1. Secuencial
        print("-> Ejecutando algoritmo SECUENCIAL...")
        t_seq = run_sequential(arr)
        results.append(
            {
                "Algoritmo": "secuencial",
                "complejidad": c,
                "procesos(workers)": 1,
                "tiempo": t_seq,
                "speed-up": 1.0,
                "eficiencia": 100.0,
                "hardware (cantidad cores)": cores,
            }
        )
        print(f"   Tiempo secuencial: {t_seq:.4f}s")

        # 2. Multiprocessing
        print("\n-> Ejecutando algoritmo MULTIPROCESSING...")
        for p in workers:
            t_mp = run_multiprocessing(arr, p)
            speed_up = t_seq / t_mp if t_mp > 0 else 0
            eficiencia = (speed_up / p) * 100
            results.append(
                {
                    "Algoritmo": "multiprocessing",
                    "complejidad": c,
                    "procesos(workers)": p,
                    "tiempo": t_mp,
                    "speed-up": speed_up,
                    "eficiencia": eficiencia,
                    "hardware (cantidad cores)": cores,
                }
            )
            print(
                f"   Workers: {p:2d} | Tiempo: {t_mp:.4f}s | Speed-up: {speed_up:.4f} | Eficiencia: {eficiencia:.2f}%"
            )

        # 3. Threading
        print("\n-> Ejecutando algoritmo THREADING...")
        for p in workers:
            t_th = run_threading(arr, p)
            speed_up = t_seq / t_th if t_th > 0 else 0
            eficiencia = (speed_up / p) * 100
            results.append(
                {
                    "Algoritmo": "threading",
                    "complejidad": c,
                    "procesos(workers)": p,
                    "tiempo": t_th,
                    "speed-up": speed_up,
                    "eficiencia": eficiencia,
                    "hardware (cantidad cores)": cores,
                }
            )
            print(
                f"   Workers: {p:2d} | Tiempo: {t_th:.4f}s | Speed-up: {speed_up:.4f} | Eficiencia: {eficiencia:.2f}%"
            )

    # Guardar en CSV
    csv_filename = "resultados_benchmark.csv"
    print(f"\nGuardando resultados en {csv_filename}...")
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = [
            "Algoritmo",
            "complejidad",
            "procesos(workers)",
            "tiempo",
            "speed-up",
            "eficiencia",
            "hardware (cantidad cores)",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print("¡Finalizado con éxito!")


if __name__ == "__main__":
    main()
