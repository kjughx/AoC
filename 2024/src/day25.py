#!/bin/env python3
import numpy as np
from timer import profiler

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

lines = open(0).read()[:-1]


@profiler
def solve(lines):
    keys = []
    locks = []

    for t in lines.split('\n\n'):
        t = np.array([[1 if c == '#' else 0 for c in row]
                     for row in t.split('\n')])
        if np.all(t[0, :] == 1):
            locks.append(t)
        else:
            keys.append(t)

    p = 0
    for lock in locks:
        for key in keys:
            fit = lock + key
            if np.all(fit <= 1):
                p += 1

    print(p)


solve(lines)
