import numpy as np
import sys


def solve(digits, k):
    if k == 0:
        return int(digits)

    N = len(digits)
    T = np.zeros((N, k + 1))
    for i in xrange(N):
        T[i][0] = int(digits[:i+1])
        for j in xrange(1, min(k, i)):
            max_ = 0
            for a in xrange(i):
                l = int(digits[a + 1:i + 1])
                prod = l * T[a][j-1]
                max_ = max(max_, prod)
            T[i][j] = max_
    return T[N - 1][k]


print solve(sys.argv[1].strip(), int(sys.argv[2]))
