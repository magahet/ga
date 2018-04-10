import heapq
import operator


def top10(f):
    a = [float(i) for i in f.readlines()]
    return zip(*heapq.nlargest(20, enumerate(a), key=operator.itemgetter(1)))[0]


t = ['SL', 'T3']
a = [75, 85, 95]

d = {}
l = set([])
for i in t:
    d[i] = {}
    for j in a:
        with open('large_{}_0.{}-outputPR.txt'.format(i, j)) as f:
            d[i][j] = top10(f)
            l.update(d[i][j])

r = []
for k in l:
    s = {}
    for i in t:
        s[i] = {}
        for j in a:
            if k in d[i][j]:
                s[i][j] = d[i][j].index(k)
    r.append(s)
