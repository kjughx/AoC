#!/bin/env python3

maps = [{} for _ in range(7)]

lines = [line.strip('\n') for line in open(0).readlines()]
seeds = list(map(int, lines[0].split(": ")[1].split(" ")))

id = 0
for line in lines[2::]:
    if len(line) == 0:
        id += 1
        continue
    elif line[0].isalpha():
        continue
    dst, src, r = map(int, line.split(" "))
    maps[id][src] = (dst, r)

locations = []
for seed in seeds:
    found = True
    for i, m in enumerate(maps):
        for (src, (dst, r)) in m.items():
            if seed < src or seed >= src + r:
                continue
            if src <= seed < src + r - 1:
                seed = seed - src + dst
                found = True
                break

    locations.append(seed)
print(min(locations))

seeds = set([(seeds[2*i], seeds[2*i] + seeds[2*i+1] - 1) for i in range(int(len(seeds)/2))])

# split the ranges in seeds into posssibly three ranges
for m in maps:
    mseeds = set()  # seeds that were mapped by a range
    for (src, (dst, r)) in m.items():
        nseeds = set()  # seeds that were not mapped, these need to be checked again
        while (len(seeds) > 0):
            ss, se = seeds.pop()

            # how to find seeds in [src, src + r]?
            # the seed range in the source range: [srs, sre)
            srs = max(ss, src)
            sre = min(src + r, se)

            if ss < src:  # before source
                nseeds.add((ss, min(src-1, se)))  # All seeds that are before src

            if se >= src + r:  # after source
                nseeds.add((max(src + r, ss), se))  # All seeds that are after (and including) src + r

            if srs <= sre:  # then there are seeds in the source range
                mseeds.add((dst + (srs - src), dst + (sre - src)))

        seeds = nseeds  # Check the seeds that were not already mapped again

    seeds |= mseeds  # Add the mapped seeds back to seeds

print(min(seeds)[0])
