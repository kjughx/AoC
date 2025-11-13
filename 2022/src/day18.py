from collections import deque
with open(0) as file:
    airs = set()
    cubes = set(tuple(map(int, line.strip('\n').split(','))) for line in file.readlines())

    count1 = 0
    for cube in cubes:
        cx, cy, cz = cube
        for dx, dy, dz in [(0, 0, 1), (0, 0, -1),
                           (0, 1, 0), (0, -1, 0),
                           (1, 0, 0), (-1, 0, 0)]:
            ax, ay, az = (cx + dx, cy + dy, cz + dz)
            if (ax, ay, az) not in cubes: # then it is air
                count1 += 1

    # find a bounding box of the lava drop
    minx, maxx = min(cubes, key=lambda x: x[0])[0] - 1, max(cubes, key=lambda x: x[0])[0] + 2
    miny, maxy = min(cubes, key=lambda x: x[1])[1] - 1, max(cubes, key=lambda x: x[1])[1] + 2
    minz, maxz = min(cubes, key=lambda x: x[2])[2] - 1, max(cubes, key=lambda x: x[2])[2] + 2

    # Make a queue of points to explore
    q = deque([(minx, miny, minz)])
    nvis = set((x,y,z) for x in range(minx, maxx) for y in range(miny,maxy) for z in range(minz, maxz))
    vis = set()
    count2 = 0
    # while there are points to explore
    while q:
        ax,ay,az = q.popleft()
        # check if neighbors are cubes
        vis.add((ax,ay,az))
        for dx, dy, dz in [(0, 0, 1), (0, 0, -1),
                           (0, 1, 0), (0, -1, 0),
                           (1, 0, 0), (-1, 0, 0)]:
            nx, ny, nz = (ax + dx, ay + dy, az + dz)
            if (nx, ny, nz) in cubes:
                count2 += 1
                continue
            # print((nx,ny,nz))
            if nx in range(minx, maxx) and ny in range(miny, maxy) and nz in range(minz,maxz):
                if (nx, ny, nz) not in vis and (nx, ny, nz) in nvis:
                    q.append((nx,ny,nz))
                    nvis.remove((nx,ny,nz))
    print(count2)
