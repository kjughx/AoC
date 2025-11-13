#!/bin/env python3

from collections import deque

lines = [deque(map(int, line.strip().split())) for line in open(0).readlines()]


def diffs(lst):
    diffs = []
    for i in range(len(lst) - 1):
        diffs.append(lst[i + 1] - lst[i])
    return diffs


t1 = 0
t2 = 0
for line in lines:
    nxt = 0
    ds = [deque(diffs(line))]
    while not all([d == 0 for d in ds[-1]]):
        ds.append(deque(diffs(ds[-1])))

    for i in reversed(range(1, len(ds))):
        ds[i - 1].append(ds[i - 1][-1] + ds[i][-1])
        ds[i - 1].appendleft(ds[i - 1][0] - ds[i][0])

    line.append(line[-1] + ds[0][-1])
    line.appendleft(line[0] - ds[0][0])
    t1 += line[-1]
    t2 += line[0]

print(t1, t2)
