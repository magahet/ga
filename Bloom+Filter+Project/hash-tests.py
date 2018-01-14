import bloom
import numpy.random as random
import matplotlib.pyplot as plt


def plot(x, y):
    plt.figure()
    plt.scatter(x, y)

    plt.figure()
    plt.hist(y)


config = {
    'N': 2147483647,
    'n': 1000,
    'k': 1,
    'genSeed': 877623067,
    'seeds': [],
}
h = bloom.HashType2(config, True)
hashes = h.getHashList(10)

x = [random.randint(100000) for _ in xrange(1000)]
#x = [2 * i for i in xrange(1000)]

y = [h.getHashList(i)[0] for i in x]

plot(x, y)
