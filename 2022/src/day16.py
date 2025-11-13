#!/bin/env python3 

with open('inputs/day16') as file:
    tunnels = {}
    valves = {'AA': 0}
    for line in file.readlines():
        line = line.strip('\n')
        valve = line.split(' ')[1]
        rate = int(line.split(' ')[4].split('=')[1].strip(';'))
        targets = [target.split(' ')[-1] for target in line.split('to')[1].split(',')]
        if rate > 0:
            valves[valve] = rate
        tunnels[valve] = targets

    vis = {}
    def f(valve, time, opened, elephant):
        if time == 0:
            if elephant:
                return f('AA', 26, opened, False)
            else:
                return 0
        
        if (valve, time, opened, elephant) in vis:
            return vis[(valve, time, opened, elephant)]

        ans = 0
        if valve in valves: 
            bit = 1 << list(valves).index(valve)
            if not (bit & opened):
                ans = max(ans, valves[valve]*(time-1) + f(valve, time - 1, opened | bit, elephant)) # open the valve

        for target in tunnels[valve]:
            ans = max(ans, f(target, time - 1, opened, elephant)) # go to neighbor

        vis[(valve, time, opened, elephant)] = ans 

        return ans

    maxtime = 30
    # print(f('AA', maxtime, 0, False))
    print(f('AA', 26, 0, True))
