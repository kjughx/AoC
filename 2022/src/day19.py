#!/bin/env python3

import re
from collections import deque

with open('inputs/day19') as file:
    blueprints = [line.strip('\n') for line in file.readlines()]
    quality = 0

    materials = ['ore', 'clay', 'obsidian', 'geode']
    for bpi, blueprint in enumerate(blueprints):
        costs = [re.findall(r"\d+ \w+", line) for line in blueprint.split('. ')]
        bp = []
        maxcost = [0,0,0]
        for cost in costs:
            c = [0,0,0,0]
            for m in cost:
                ci, m = m.split(' ')
                c[materials.index(m)] = int(ci)
                maxcost[materials.index(m)] = max(int(ci), maxcost[materials.index(m)])
            bp.append(c)

        costs = bp
        print(maxcost)

        vis = set()
        maxtime = 24
        q = deque([(maxtime, [1, 0, 0, 0], [0, 0, 0, 0])])
        maxg = 0

        while q:
            time, bots, resources = q.popleft()
            assert(all(x >= 0 for x in bots))
            assert(all(x >= 0 for x in resources))

            maxg = max(maxg, resources[3])

            if time == 0:
                continue

            key = (time, *bots, *resources)
            if key in vis:
                continue
            vis.add(key)

            resources_ = resources[:]
            for i in range(4):
                resources_[i] += bots[i]
            q.append([time - 1, bots, resources_])

            for i in range(4):
                if i != 3 and resources[i] > maxcost[i]:
                    continue
                bots_, resources_ = bots[:], resources[:]
                if all(resources[j] >= cost for j, cost in enumerate(costs[i])):
                    for j, cost in enumerate(costs[i]):
                        resources_[j] += (bots_[j] - cost)

                    bots_[i] += 1
                    q.append([time - 1, bots_, resources_])
        print(maxg)
        quality += (bpi+1) * maxg
    print(quality)
