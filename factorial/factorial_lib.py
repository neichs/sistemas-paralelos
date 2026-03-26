"""Funciones compartidas para el ejercicio de factorial en paralelo."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Iterable, List, Sequence


DEFAULT_SEED = 2026
_rng = random.Random(DEFAULT_SEED)
DEFAULT_NUMBERS: List[int] = [_rng.randint(0, 50) for _ in range(10000000)]


def factorial(n: int) -> int:
    """Calcula factorial de n con una implementacion simple en Python."""
    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


def mean_serial(values: Iterable[int]) -> Fraction:
    """Calcula el promedio en forma secuencial."""
    count = 0
    total = 0
    for value in values:
        total += value
        count += 1

    if count == 0:
        raise ValueError("No se puede calcular promedio de una lista vacia")

    return Fraction(total, count)


def print_result(title: str, numbers: Sequence[int], workers: int, mean_value: Fraction, elapsed: float) -> None:
    """Imprime un resumen simple para comparar variantes."""
    print(f"Implementacion: {title}")
    print(f"Cantidad de numeros: {len(numbers)}")
    print(f"Workers: {workers}")
    print(f"Tiempo (segundos): {elapsed:.6f}")

    # Redondeo a 2 decimales sin usar float para evitar overflow con enteros muy grandes.
    scaled = (mean_value.numerator * 100 + mean_value.denominator // 2) // mean_value.denominator
    integer_part = scaled // 100
    decimal_part = scaled % 100
    print(f"Promedio final (2 decimales): {integer_part}.{decimal_part:02d}")
