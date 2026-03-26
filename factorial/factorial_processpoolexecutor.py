from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from time import perf_counter

from factorial_lib import DEFAULT_NUMBERS, factorial, mean_serial, print_result


def main() -> None:
    parser = argparse.ArgumentParser(description="Factoriales en paralelo con ProcessPoolExecutor")
    parser.add_argument("--numbers", type=str, default=None, help="Lista separada por comas. Ejemplo: 5,7,10")
    parser.add_argument("--workers", type=int, default=4, help="Cantidad de workers")
    args = parser.parse_args()

    if args.numbers is None:
        numbers = list(DEFAULT_NUMBERS)
    else:
        numbers = [int(item.strip()) for item in args.numbers.split(",") if item.strip()]

    start = perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        factorials = list(executor.map(factorial, numbers))
    mean_value = mean_serial(factorials)
    elapsed = perf_counter() - start

    print_result("concurrent.futures.ProcessPoolExecutor", numbers, args.workers, mean_value, elapsed)


if __name__ == "__main__":
    main()
