#!/usr/bin/env python3

lines = [line.strip() for line in open(0).readlines()]

c = 1
class Block:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, xs, ys, zs, xe, ye, ze):
        global c
        self._cubes = set()
        self._aboves = []
        self._belows = []
        self.z = zs
        self.name = c
        c = c + 1

        for x in range(xs, xe + 1):
            for y in range(ys, ye + 1):
                for z in range(zs, ze + 1):
                    self._cubes.add((x, y, z))

    def __repr__(self):
        s = f"{self.name}: " + "{"
        for (x, y, z) in self._cubes:
            s += f"({x}, {y}, {z}), "
        s += '}'
        return s

    def cubes(self):
        return self._cubes

    def try_fall(self):
        return self.z-1, tuple((x, y, z-1) for x, y, z in self.cubes())

    def fall(self):
        self._cubes = set((x, y, z-1) for x, y, z in self.cubes())
        self.z -= 1
        return self

    def __hash__(self):
        return self._cubes


blocks = []
for line in lines:
    s, e = line.split('~')
    xs, ys, zs = list(map(int, s.split(',')))
    xe, ye, ze = list(map(int, e.split(',')))
    blocks.append(Block(xs, ys, zs, xe, ye, ze))

blocks = sorted(blocks, key=lambda block: block.z)

cubes = set()
for block in blocks:
    cubes |= block.cubes()

for block in blocks:
    fall = True
    while fall:
        fall = False
        z, tfall = block.try_fall()

        for c in block.cubes():
            cubes.remove(c)

        if z > 0 and not any([c in cubes for c in tfall]):
            block.fall()
            fall = True
        cubes |= block.cubes()

for i, b1 in enumerate(blocks):
    for b2 in blocks[i + 1:]:
        if any([(x, y, z - 1) in b1.cubes() for x, y, z in b2.cubes()]):
            # print(f"{b1.name} supports {b2.name}")
            b2._belows.append(b1)
            b1._aboves.append(b2)


# a block can be removed if its aboves are supported by more than 1
t = 0
fall = []
for block in blocks:
    if all([len(b._belows) > 1 for b in block._aboves]) or len(block._aboves) == 0:
        t += 1
    else:
        fall.append(block)
print(t)


from collections import deque

t = 0
for block in fall:
    q = deque([b for b in block._aboves if len(b._belows) == 1])
    fallen = set([b.name for b in q])
    while q:
        b = q.popleft()
        for a in b._aboves:
            if all([s.name in fallen for s in a._belows]):
                q.append(a)
                fallen.add(a.name)
    t += len(fallen)
print(t)
