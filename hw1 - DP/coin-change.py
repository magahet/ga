import numpy as np
import sys


def solve(X, B, k):
    N = len(X)
    T = np.ones((N + 1, B + 1)) * np.inf
    T[:, 0] = 0

    for i in xrange(1, N + 1):
        for j in xrange(1, B + 1):
            print X[i - 1], j, X[i - 1] > j
            if X[i - 1] > j:
                T[i, j] = T[i - 1, j]
            else:
                print 'blah'
                print T[i - 1, j], T[i - 1, j - X[i - 1]] + 1
                T[i, j] = min(T[i - 1, j], T[i - 1, j - X[i - 1]] + 1)
    return T[N][B]


print solve([int(d) for d in sys.argv[1].strip()],
            int(sys.argv[2]),
            int(sys.argv[3]))
