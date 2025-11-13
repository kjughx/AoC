#!/bin/env python3 
from itertools import cycle

shifts = cycle(open('inputs/day17').readlines()[0].strip())
shifti = -1
shapes = cycle(['-', '+', 'L', '|', 'x'])
shapei = -1

rocks = set([(i,-1) for i in range(7)])
h = 0

ptop = (0,0, tuple([-1 for _ in range(7)]))
tops =  {ptop: (0, 0)}

def hash(h, ptop, rock):
    ntop = list(ptop)
    for px, py in enumerate(ptop):
        for x, y in rock:
            if x == px:
                ntop[x] = max(py, h - y)
    return tuple(ntop)

nshifts = len(open('inputs/day17').readlines()[0].strip())
i = 0
repeated = False
maxrock = 1_000_000_000_000
while i < maxrock:
    h = h + 3
    shape = next(shapes)
    shapei = (shapei + 1) % 5
    match shape:
        case '-':
            rock = set([(2, h), (3, h), (4, h), (5,h)])
        case '+':
            rock = set([(2,h+1), (3,h+1), (4,h+1), (3,h), (3,h+2)])
        case 'L':
            rock = set([(2, h), (3, h), (4,h), (4,h+1), (4,h+2)])
        case '|':
            rock = set([(2,h),(2,h+1), (2,h+2),(2,h+3)])
        case 'x':
            rock = set([(2,h), (3,h), (2,h+1),(3,h+1)])
        case _:
            assert(False)

    falling = True
    while falling:
        shift = next(shifts)
        shifti = (shifti + 1) % nshifts
        if shift ==  '<':
            nrock = set([(x-1,y) for x,y, in rock])
            if all(x >= 0 for x, _ in nrock) and not(nrock & rocks):
                rock = nrock
        else:
            nrock = set([(x+1,y) for x,y, in rock])
            if all(x < 7 for x, _ in nrock) and not(nrock & rocks):
                rock = nrock
       
        rock = set([(x, y-1) for x,y in rock])
        if rock & rocks:
            rock = set([(x,y+1) for x,y in rock])
            rocks |= rock
            h = max([y for _, y in rocks]) + 1

            top = (shapei, shifti, hash(h, ptop[2], rock))
            if top in tops and not repeated:
                # Then it repeats, grab the state from the tops dictionary 
                # and fast forward to 1_000_000_000_000 % rock_count
                pi, ph = tops[top]
                repeat_count = (maxrock - i) // (i - pi) # (i - pi): how many rocks are in the repeat window
                height = (h - ph) * repeat_count # (h - ph) is how tall the repeat window is
                i += repeat_count * (i - pi)
                repeated = True

            ptop = top
            tops[top] = (i, h) #type: ignore

            falling = False
    i += 1

print(h + height)
