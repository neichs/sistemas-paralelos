from __future__ import annotations

import argparse
from time import perf_counter

from factorial_lib import DEFAULT_NUMBERS, factorial, mean_serial, print_result


def main() -> None:
    parser = argparse.ArgumentParser(description="Factoriales en forma secuencial")
    parser.add_argument("--numbers", type=str, default=None, help="Lista separada por comas. Ejemplo: 5,7,10")
    parser.add_argument("--workers", type=int, default=1, help="Parametro informativo para mantener misma interfaz")
    args = parser.parse_args()

    if args.numbers is None:
        numbers = list(DEFAULT_NUMBERS)
    else:
        numbers = [int(item.strip()) for item in args.numbers.split(",") if item.strip()]

    start = perf_counter()
    factorials = [factorial(number) for number in numbers]
    mean_value = mean_serial(factorials)
    elapsed = perf_counter() - start

    print_result("secuencial", numbers, args.workers, mean_value, elapsed)


if __name__ == "__main__":
    main()
