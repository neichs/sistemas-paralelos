import numpy as np
from time import time
import concurrent.futures


def sum_elements(v: np.ndarray) -> float:
    """Calcula la suma de los elementos de un array de NumPy."""
    res: float = 0.0
    for e in v:
        res += float(e)
    return res


if __name__ == "__main__":
    c = 100_000_000  # Complejidad: tamaño del vector
    p = 4  # Cantidad de workers (procesos)

    print(f"Generando vector de tamaño {c}...")
    arr = np.random.rand(c)

    print(f"Iniciando suma con {p} procesos (Multiprocessing)...")
    init = time()

    # Dividimos el vector en `p` partes utilizando chunks.
    # NOTA SOBRE PICKLING Y MEMORIA:
    # Cuando pasamos argumentos a otro proceso, Python debe serializarlos (Pickling).
    # Si le pasamos a multiprocessing una sub-vista (view) de un ndarray gigante, en muchas versiones
    # de Python/NumPy, pickle terminará serializando el array BASE COMPLETO.
    # Para EVITAR copiar todo el array original múltiples veces y minimizar el overhead de red/memoria,
    # forzamos copias en memoria (.copy()) que limitan la estructura enviada estrictamente al chunk.
    chunks = [chunk.copy() for chunk in np.array_split(arr, p)]

    total_sum: float = 0.0

    # Utilizamos ProcessPoolExecutor para la paralelización real en CPU, evadiendo el GIL
    with concurrent.futures.ProcessPoolExecutor(max_workers=p) as executor:
        # Repartimos el trabajo entre N procesos distintos
        resultados_parciales = executor.map(sum_elements, chunks)

        # El proceso principal recolecta y suma los resultados parciales iterables
        total_sum = sum(resultados_parciales)

    end = time() - init
    print(f"Result: {total_sum} | Time: {end:.4f}s | With c={c}, p={p}")
