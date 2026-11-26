#!/usr/bin/env python3

import random
import sys

def tabular_lcs(x, y):
    n = len(x)
    m = len(y)
    L = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    lcs = ""
    i = n
    j = m
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            lcs = x[i - 1] + lcs
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return lcs


def generate(n, alphabet="ACGT"):
    return "".join(random.choices(alphabet, k=n))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        subsequence1 = generate(int(sys.argv[2]))
        subsequence2 = generate(int(sys.argv[2]))
        print("Generated subsequence 1:", subsequence1)
        print("Generated subsequence 2:", subsequence2)
        lcs = tabular_lcs(subsequence1, subsequence2)
        print("LCS is", lcs, "with length", len(lcs))
    elif len(sys.argv) != 3:
        print("Usage: python3 act1-pd_tabular.py <string1> <string2>, or run without arguments to use default strings (aka 'autotest').")
        x = "AGGTAB"
        y = "GXTXAYB"
        lcs = tabular_lcs(x, y)
        print("LCS is", lcs, "with length", len(lcs))
    else:
        x = sys.argv[1]
        y = sys.argv[2]
        lcs = tabular_lcs(x, y)
        print("LCS is", lcs, "with length", len(lcs))
