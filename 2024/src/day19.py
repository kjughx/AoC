#!/bin/env python3
from collections import deque
from timer import profiler

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001


@profiler
def part1(patterns):
    p = 0
    for pattern in patterns:
        q = deque([])
        for e in range(len(pattern) + 1):
            if pattern[:e] in towels:
                q.append((pattern[:e]))

        vis = set()
        while q:
            pat = q.popleft()
            if pat == pattern:
                p += 1
                break

            if pat in vis:
                continue
            vis.add(pat)

            e = len(pat)
            for towel in towels:
                if pattern[e:].startswith(towel):
                    q.append(pat + towel)
    print(p)


@profiler
def part2(patterns):
    vis = {}

    def build(towels, p):
        if p in vis:
            return vis[p]

        pp = 0
        if len(p) == 0:
            pp = 1

        for towel in towels:
            if p.startswith(towel):
                pp += build(towels, p[len(towel):])
        vis[p] = pp

        return pp

    p = 0
    for pattern in patterns:
        p += build(towels, pattern)
    print(p)


lines = open(0).read()

towels, patterns = lines.split('\n\n')
towels = set(towels.split(', '))
patterns = patterns.split('\n')[:-1]

part1(patterns)
part2(patterns)
