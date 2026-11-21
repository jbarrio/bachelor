#!/usr/bin/env python3

import random
import sys

def recursive_lcs(x, y):
    if not x or not y:
        return 0
    if x[-1] == y[-1]:
        return 1 + recursive_lcs(x[:-1], y[:-1])
    
    return max(recursive_lcs(x[:-1], y), recursive_lcs(x, y[:-1]))


def generate(n, alphabet="ACGT"):
    return "".join(random.choices(alphabet, k=n))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        subsequence1 = generate(int(sys.argv[2]))
        subsequence2 = generate(int(sys.argv[2]))
        print("Generated subsequence 1:", subsequence1)
        print("Generated subsequence 2:", subsequence2)
        print("Length of LCS is", recursive_lcs(subsequence1, subsequence2))
    elif len(sys.argv) != 3:
        print("Usage: python3 act1-lcs.py <string1> <string2>, or run without arguments to use default strings (aka 'autotest').")
        x = "AGGTAB"
        y = "GXTXAYB"
        print("Length of LCS is", recursive_lcs(x, y))
    else:
        x = sys.argv[1]
        y = sys.argv[2]
        print("Length of LCS is", recursive_lcs(x, y))