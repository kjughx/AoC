import numpy as np
with open(0) as file:
    lines = []
    for line in file.readlines():
        lines.append([int(c) for c in line.strip('\n')])

    lines = np.array(lines)

    count1 = 2*len(lines[0, :]) + 2*len(lines[:, 0]) - 4
    maxc = 0
    for i in range(1, len(lines[:, 0]) - 1):
        for j in range(1, len(lines[0, :]) - 1):
            toedges = [lines[:i, j], lines[i+1:, j], lines[i, :j], lines[i, j+1:]]
            toedges[0] = np.flip(toedges[0])
            toedges[2] = np.flip(toedges[2])
            edges1 = [max(path) < lines[i,j] for path in toedges]
            if any(edges1):
                count1 += 1
            cost = []
            for edge in toedges:
                # print(edge)
                count = 0
                for tree in edge:
                    count += 1
                    if tree >= lines[i,j]:
                        break
                cost.append(count)
            # print(cost)
            # print('-------')
            if np.array(cost).prod() > maxc:
                maxc = np.array(cost).prod()

    # print(count1)
    print(maxc)
