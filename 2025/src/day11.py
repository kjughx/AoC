#!/usr/bin/env python3
import sys
import re
from collections import deque
from functools import lru_cache

devices = {}
devicesb = {}

""" From 'out', how many can reach `node` backwards? """
def traverse(path, target):
    def can_reach(node):
        reachable = {node}
        q = deque([node])
        while q:
            node = q.popleft()
            if node not in devicesb:
                continue

            for d in devicesb[node]:
                if d in reachable:
                    continue
                reachable.add(d)
                q.append(d)

        return reachable

    reachable = can_reach(target)
    cache = set()

    paths = set()
    q = deque([path])
    while q:
        path = q.popleft()
        node = path[-3:]
        if node not in reachable:
            continue

        cache.add(path)

        if node == target:
            paths.add(path)
            continue

        for d in devices[node]:
            if path + d in cache:
                continue
            q.append(path + d)

    return paths

def main(data):
    global n, cache, PATHS
    for line in data.splitlines():
        data = re.findall(r"([a-z]{3})", line)
        if data[0] not in devices:
            devices[data[0]] = []
        devices[data[0]] += data[1:]
        for d in data[1:]:
            if d not in devicesb:
                devicesb[d] = []
            devicesb[d].append(data[0])

    print(f"part1 = {len(traverse('you', 'out'))}")

    fft = traverse("svr", "fft")
    dac = traverse("fft", "dac")
    out = traverse("dac", "out")
    print(f"part2 = {len(fft) * len(dac) * len(out)}")

if __name__ == "__main__":
    main(sys.stdin.read())
