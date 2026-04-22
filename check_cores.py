import os
import multiprocessing


def detectar_nucleos():
    print("========================================")
    print("   DETECCIÓN DE CÚCLEOS DEL SISTEMA")
    print("========================================")

    # Detección de núcleos usando multiprocessing
    try:
        logical_cores = multiprocessing.cpu_count()
        print(
            f"-> Núcleos lógicos (hilos de ejecución) usando multiprocessing: {logical_cores}"
        )
    except NotImplementedError:
        print("-> No se pudo detectar la cantidad de núcleos con multiprocessing.")

    # Detección usando os (equivalente en py >= 3.4)
    try:
        os_cores = os.cpu_count()
        print(f"-> Núcleos lógicos (hilos de ejecución) usando os: {os_cores}")
    except Exception as e:
        pass

    # Recomendación final
    print(
        "\n[Nota]: Tu sistema tiene por defecto esta cantidad total de hilos o workers lógicos disponibles."
    )
    print(
        "Si el número es 32, entonces establecer ese valor manualmente en tu archivo benchmark para los cálculos está perfecto."
    )
    print("========================================")


if __name__ == "__main__":
    detectar_nucleos()
