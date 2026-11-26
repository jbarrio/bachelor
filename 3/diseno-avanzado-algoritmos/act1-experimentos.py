#!/usr/bin/env python3

import importlib
import random
import time
import tracemalloc

recursive = importlib.import_module("act1-lcs")
hirschberg = importlib.import_module("act1-hirschberg")
tabular = importlib.import_module("act1-pd_tabular")

SEED = 2026
REPEAT = 3


def measure(f, x, y):
    times = []
    for _ in range(REPEAT):
        start = time.process_time()
        result = f(x, y)
        times.append(time.process_time() - start)

    tracemalloc.start()
    f(x, y)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return result, min(times) * 1000, peak / 1024


if __name__ == "__main__":
    random.seed(SEED)

    print("Hirschberg vs tabular")
    print("| n | LCS | Hirschberg ms | Hirschberg KiB | Tabular ms | Tabular KiB |")
    print("|---|---|---|---|---|---|")
    for n in [10, 100, 250, 500, 1000, 2000]:
        x = recursive.generate(n)
        y = recursive.generate(n)
        lcs_h, t_h, m_h = measure(hirschberg.hirschberg_lcs, x, y)
        lcs_t, t_t, m_t = measure(tabular.tabular_lcs, x, y)
        if len(lcs_h) != len(lcs_t):
            print("ERROR: lengths do not match for n =", n)
        print(f"| {n} | {len(lcs_t)} | {t_h:.3f} | {m_h:.1f} | {t_t:.3f} | {m_t:.1f} |")

    print()
    print("Recursive")
    print("| n | LCS | Recursive ms | Recursive KiB | Tabular ms |")
    print("|---|---|---|---|---|")
    for n in [6, 8, 10, 12, 14, 16, 18, 20]:
        x = recursive.generate(n)
        y = recursive.generate(n)
        lcs_r, t_r, m_r = measure(recursive.recursive_lcs, x, y)
        lcs_t, t_t, m_t = measure(tabular.tabular_lcs, x, y)
        if lcs_r != len(lcs_t):
            print("ERROR: lengths do not match for n =", n)
        print(f"| {n} | {lcs_r} | {t_r:.3f} | {m_r:.1f} | {t_t:.3f} |")
