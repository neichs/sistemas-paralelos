from __future__ import annotations

import argparse
import multiprocessing as mp
from time import perf_counter

from factorial_lib import DEFAULT_NUMBERS, factorial, mean_serial, print_result


def main() -> None:
    parser = argparse.ArgumentParser(description="Factoriales en paralelo con multiprocessing.Pool")
    parser.add_argument("--numbers", type=str, default=None, help="Lista separada por comas. Ejemplo: 5,7,10")
    parser.add_argument("--workers", type=int, default=4, help="Cantidad de workers")
    args = parser.parse_args()

    if args.numbers is None:
        numbers = list(DEFAULT_NUMBERS)
    else:
        numbers = [int(item.strip()) for item in args.numbers.split(",") if item.strip()]

    start = perf_counter()
    with mp.Pool(processes=args.workers) as pool:
        factorials = pool.map(factorial, numbers)
    mean_value = mean_serial(factorials)
    elapsed = perf_counter() - start

    print_result("multiprocessing.Pool", numbers, args.workers, mean_value, elapsed)


if __name__ == "__main__":
    main()
