#!/bin/env python3
import numpy as np
from collections import deque
from functools import cache
from timer import profiler

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

codes = list(map(str.strip, open(0).readlines()))

keypad = np.array([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [' ', '0', 'A']
])

dpad = np.array([
    [' ', '^', 'A'],
    ['<', 'v', '>']
])

ds = {
    (-1, 0): '^',
    (1, 0): 'v',
    (0, 1): '>',
    (0, -1): '<',
    (0, 0): 'A',
}
dds = {
    v: k for k, v in ds.items()
}


def get_turns(path):
    if not path:
        return 0

    n = 0
    pd = path[0]
    for p in path[1:]:
        n += (p != pd)
        pd = p
    return n


def distance_from_A(path, pad):
    if not path:
        return 0

    n = 0
    rc = np.where(pad == 'A')
    fr, fc = rc[0][0], rc[1][0]
    for p in path:
        r, c = dds[p]
        n += abs(r - fr) + abs(c - fc)

    return n


def prime(pad):
    R, C = np.shape(pad)

    def dfs(sr, sc, fr, fc):
        q = deque([(sr, sc, '', set())])
        paths = []
        d = float('inf')

        while q:
            r, c, path, vis = q.popleft()
            if (r, c) == (fr, fc):
                path += 'A'
                if len(path) < d:
                    d = len(path)
                    paths = [path]
                elif len(path) == d:
                    paths.append(path)

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in vis:
                    continue
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                if pad[nr, nc] == ' ':
                    continue

                q.append((nr, nc, path + ds[(dr, dc)], vis | {(nr, nc)}))
        return paths

    fastest = {}
    for i in map(str, pad.reshape(-1)):
        for j in map(str, pad.reshape(-1)):
            if i == ' ' or j == ' ':
                continue

            if i == j:
                fastest[(i, j)] = ['A']
                continue

            rc = np.where(pad == i)
            sr, sc = rc[0][0], rc[1][0]
            rc = np.where(pad == j)
            fr, fc = rc[0][0], rc[1][0]

            paths = dfs(sr, sc, fr, fc)

            fastest[(i, j)] = paths
            paths = []
    return fastest


dpaths = prime(dpad)
dlens = {k: len(v[0]) for k, v in dpaths.items()}
kpaths = prime(keypad)
klens = {k: len(v[0]) for k, v in kpaths.items()}


def find_sequence(code, pad):
    R, C = np.shape(pad)
    paths = set()
    dist = float('inf')

    fastest = prime(pad)

    @cache
    def dfs(i, path):
        nonlocal paths, dist
        if i == len(code):
            if len(path) < dist:
                dist = len(path)
                paths = {path}
            elif len(path) == dist:
                paths.add(path)
            return

        if len(path) >= dist:
            return

        if not fastest[(code[i - 1], code[i])]:
            dfs(i + 1, path)
        else:
            for p in fastest[(code[i - 1], code[i])]:
                dfs(i + 1, path + p)

    for p in fastest[('A', code[0])]:
        dfs(1, p)

    return paths


"""
what's the shortest way to do a single button press 25 levels deep?

"""


@cache
def find_length(seq, depth):
    if depth == 1:
        return sum(dlens[(pc, c)] for pc, c in zip('A' + seq, seq))

    length = 0
    for pc, c in zip('A' + seq, seq):
        length += min(find_length(seq, depth - 1) for seq in dpaths[(pc, c)])

    return length


@profiler
def solve(dep):
    p = 0
    for code in codes:
        paths = find_sequence(code, keypad)
        m = float('inf')
        for path in paths:
            m = min(m, find_length(path, dep))
        p += m * \
            int("".join([c for c in code if c.isdigit()]))

    print(p)


solve(2)
solve(25)
