#!/usr/bin/env python3

import random
import sys

def lcs_last_row(x, y):
    m = len(y)
    prev = [0] * (m + 1)

    for xi in x:
        curr = [0] * (m + 1)
        for j in range(1, m + 1):
            if xi == y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr

    return prev


def hirschberg_lcs(x, y):
    if not x or not y:
        return ""
    if len(x) == 1:
        return x if x in y else ""

    mid = len(x) // 2
    top = lcs_last_row(x[:mid], y)
    bottom = lcs_last_row(x[mid:][::-1], y[::-1])[::-1]
    k = max(range(len(y) + 1), key=lambda k: top[k] + bottom[k])

    return hirschberg_lcs(x[:mid], y[:k]) + hirschberg_lcs(x[mid:], y[k:])


def generate(n, alphabet="ACGT"):
    return "".join(random.choices(alphabet, k=n))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        subsequence1 = generate(int(sys.argv[2]))
        subsequence2 = generate(int(sys.argv[2]))
        print("Generated subsequence 1:", subsequence1)
        print("Generated subsequence 2:", subsequence2)
        lcs = hirschberg_lcs(subsequence1, subsequence2)
        print("LCS is", lcs, "with length", len(lcs))
    elif len(sys.argv) != 3:
        print("Usage: python3 act1-hirschberg.py <string1> <string2>, or run without arguments to use default strings (aka 'autotest').")
        x = "AGGTAB"
        y = "GXTXAYB"
        lcs = hirschberg_lcs(x, y)
        print("LCS is", lcs, "with length", len(lcs))
    else:
        x = sys.argv[1]
        y = sys.argv[2]
        lcs = hirschberg_lcs(x, y)
        print("LCS is", lcs, "with length", len(lcs))
