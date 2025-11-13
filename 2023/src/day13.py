#!/bin/env python3
import numpy as np

lines = [line.strip('\n') for line in open(0).readlines()]

patterns = []
p = []
for i, line in enumerate(lines):
    if len(line) == 0:
        patterns.append(np.array(p))
        p = []
        continue

    p.append([c for c in line])

patterns.append(np.array(p))

t = 0
t2 = 0
for p in patterns:
    R = p.shape[0]
    C = p.shape[1]

    i = 1
    while (i < R or i < C):
        if i < C:
            d = min(i, C - i)
            if np.all(p[:, i - d:i] == np.flip(p[:, i: i + d], axis=1)):
                t += i
            if np.sum(p[:, i - d:i] != np.flip(p[:, i: i + d], axis=1)) == 1:
                t2 += i

        if i < R:
            d = min(i, R - i)
            if np.all(p[i - d:i, :] == np.flip(p[i: i + d, :], axis=0)):
                t += 100 * i
            if np.sum(p[i - d:i, :] != np.flip(p[i: i + d, :], axis=0)) == 1:
                t2 += 100 * i
        i += 1
print(t, t2)
