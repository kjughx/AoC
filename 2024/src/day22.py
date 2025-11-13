#!/bin/env python3
from collections import deque
from timer import profiler

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

lines = open(0).readlines()


@profiler
def part1():
    def evolve(x, t):
        while t:
            x = (x ^ (x * 2 ** 6)) & (2 ** 24 - 1)
            x = (x ^ (x // 32)) & (2 ** 24 - 1)
            x = (x ^ (x * 2 ** 11)) & (2 ** 24 - 1)
            t -= 1

        return x

    p = 0
    for line in lines:
        p += evolve(int(line.strip()), 2000)

    print(p)


@profiler
def part2():

    seqs = set()

    def evolve(x, T):
        changes = deque([])
        t = T
        y = int(str(x)[-1])
        prices = {}

        while t:
            x = (x ^ (x * 2 ** 6)) & (2 ** 24 - 1)
            x = (x ^ (x // 32)) & (2 ** 24 - 1)
            x = (x ^ (x * 2 ** 11)) & (2 ** 24 - 1)

            ny = int(str(x)[-1])
            if len(changes) == 4:
                if tuple(changes) not in prices:
                    prices[tuple(changes)] = y
                seqs.add(tuple(changes))
                changes.popleft()

            changes.append(ny - y)

            y = ny

            t -= 1

        return prices

    monkeys = [evolve(int(line.strip()), 2000) for line in lines]
    m = 0
    for i, seq in enumerate(seqs):
        p = 0
        for monkey in monkeys:
            try:
                p += monkey[seq]
            except:
                pass
        m = max(m, p)
    print(m)


part1()
part2()
