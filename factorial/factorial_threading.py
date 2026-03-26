from __future__ import annotations

import argparse
import threading
from queue import Queue
from time import perf_counter

from factorial_lib import DEFAULT_NUMBERS, factorial, mean_serial, print_result


def worker(task_queue: Queue, results: list[int]) -> None:
    while True:
        item = task_queue.get()
        if item is None:
            break

        index, number = item
        results[index] = factorial(number)
        task_queue.task_done()


def main() -> None:
    parser = argparse.ArgumentParser(description="Factoriales en paralelo con threading")
    parser.add_argument("--numbers", type=str, default=None, help="Lista separada por comas. Ejemplo: 5,7,10")
    parser.add_argument("--workers", type=int, default=4, help="Cantidad de hilos")
    args = parser.parse_args()

    if args.numbers is None:
        numbers = list(DEFAULT_NUMBERS)
    else:
        numbers = [int(item.strip()) for item in args.numbers.split(",") if item.strip()]

    task_queue: Queue = Queue()
    results: list[int] = [0] * len(numbers)

    threads: list[threading.Thread] = []
    for _ in range(args.workers):
        thread = threading.Thread(target=worker, args=(task_queue, results))
        thread.start()
        threads.append(thread)

    start = perf_counter()
    for index, number in enumerate(numbers):
        task_queue.put((index, number))

    task_queue.join()

    for _ in threads:
        task_queue.put(None)

    for thread in threads:
        thread.join()

    mean_value = mean_serial(results)
    elapsed = perf_counter() - start

    print_result("threading", numbers, args.workers, mean_value, elapsed)


if __name__ == "__main__":
    main()
