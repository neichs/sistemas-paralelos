import numpy as np
from time import time
import concurrent.futures


def sum_elements(v: np.ndarray) -> float:
    """Calcula la suma de los elementos de un array de NumPy de forma secuencial."""
    res: float = 0.0
    for e in v:
        res += float(e)
    return res


if __name__ == "__main__":
    # ==============================================================
    # Parámetros (Fácilmente modificables)
    # ==============================================================
    c = 100_000_000  # Complejidad: tamaño del vector
    p = 4  # Cantidad de workers (hilos)

    print(f"Generando vector de tamaño {c}...")
    arr = np.random.rand(c)

    print(f"Iniciando suma con {p} hilos (Threading)...")
    init = time()

    # Dividimos el vector en `p` partes (chunks) equitativas.
    # En threading, al compartir la misma memoria, np.array_split devuelve subvistas (views)
    # del array original en memoria, evitando copias costosas de información.
    chunks = np.array_split(arr, p)

    total_sum: float = 0.0

    # Utilizamos ThreadPoolExecutor para gestionar los hilos
    with concurrent.futures.ThreadPoolExecutor(max_workers=p) as executor:
        # submit pasa la función y sus argumentos, de manera asíncrona a ejecutar.
        # map() devuelve un iterador a los resultados parciales garantizando orden.
        # Al sumar el bloque, estamos haciendo que el hilo principal (main thread) sume los retornos.
        resultados_parciales = executor.map(sum_elements, chunks)

        # El hilo principal suma los resultados parciales obtenidos de los workers
        total_sum = sum(resultados_parciales)

    end = time() - init
    print(f"Result: {total_sum} | Time: {end:.4f}s | With c={c}, p={p}")
