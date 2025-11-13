#!/bin/env python3
import functools
import numpy as np

cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J',]

hands = []
with open(0) as file:
    for i, line in enumerate(file.readlines()):
        line = line.strip('\n')

        h, bid = line.split(" ")

        hand = {c:0 for _,c in enumerate(cards)}
        for c in h:
            hand[c] += 1

        hands.append((hand, h, int(bid)))

def rank(h):
    ks,vs = h.keys(), list(h.values())[:-1]
    j = h['J']

    if j == 5:
        return 7

    vs[np.min(np.where(np.array(vs) == max(vs)))] += j
    if 5 in vs:
        return 7
    if 4 in vs:
        return 6
    if 3 in vs and 2 in vs:
        return 5
    if 3 in vs:
        return 4

    if 2 in vs:
        if vs.count(2) == 2:
            return 3
        return 2
    return 1

def cmp(h1, h2):
    c1 = h1[1]
    c2 = h2[1]
    t1,t2 = rank(h1[0]), rank(h2[0])
    if t1 != t2:
        return t1 - t2

    for i,c in enumerate(c1):
        if cards.index(c) > cards.index(c2[i]):
            return -1
        if cards.index(c) < cards.index(c2[i]):
            return 1
    return 0

t=0
print(hands[0], rank(hands[0][0]))
print((sorted(hands, key=functools.cmp_to_key(cmp))))
for i,h in enumerate(sorted(hands, key=functools.cmp_to_key(cmp))):
    t += (i + 1) * h[2]
    print(i + 1 , h[1], h[2])
#

print(t)
