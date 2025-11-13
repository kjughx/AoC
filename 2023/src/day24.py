#!/usr/bin/env python3

lines = [line.strip() for line in open(0).readlines()]

ps,vs = [], []
for line in lines:
    p, v = line.split(' @ ')
    ps.append(tuple(map(int, p.split(','))))
    vs.append(tuple(map(int, v.split(','))))


# How to solve system of equations:
"""
k_x2 * t2 + m_x2 = k_x1 * t1 + m_x1
t1 = (m_x2 - m_x1 + k_x2 * t2) / k_x1

k_y1 * t1 + m_y1 = k_y2 * t2 + m_y2
t2 = (m_y1 - m_y2 + k_y1 * t1) / k_y2

=>

t1 = (m_x2 - m_x1 * k_x2 * ((m_y1 - m_y2 + k_y1 * t1) / k_y2)) / k_x1 =
(m_x2 - m_x1 + (k_x2/k_y2) * (m_y1 - m_y2 + k_y1 * t1)) / k_x1 =>

k_x1 * t1 = m_x2 - m_x1 + (k_x2/k_y2)* k_y1 * t1 + (kx_2/k_y2)*(m_y1 - m_y2) =>

t1 *(k_x1 - k_y1*(k_x2/k_y2)) = m_x2 - m_x1 + (k_x2/k_y2) * (m_y1 - m_y2) =>

t1 = (m_x2 - m_x1 + (k_x2/k_y2) * (m_y1 - m_y2)) / (k_x1 - k_y1 * (k_x2 / k_y2))


Then if the intersection is 200000000000000 <= x <= 400000000000000 it's valid.
Then do the same for y

"""

ll = 200000000000000
hl = 400000000000000

t = 0
for i in range(len(ps)):
    for j in range(i + 1, len(ps)):
        k_x1, k_y1 = vs[i][:2]
        m_x1, m_y1 = ps[i][:2]
        k_x2, k_y2 = vs[j][:2]
        m_x2, m_y2 = ps[j][:2]

        if (k_x1 - k_y1 * (k_x2 / k_y2)) == 0:
            continue

        t1 = (m_x2 - m_x1 + (k_x2/k_y2) * (m_y1 - m_y2)) / (k_x1 - k_y1 * (k_x2 / k_y2))
        t2 = (m_y1 - m_y2 + k_y1 * t1) / k_y2
        x = k_x1 * t1 + m_x1
        y = k_y1 * t1 + m_y1

        if t1 > 0 and t2 > 0 and ll <= x <= hl and ll <= y <= hl:
            t += 1
# print(t)



"""

So there is a line: x, y, z @ vx, vy, vz
that intersects all lines at some points (possibly unique to each line)

So what we should solve is:

vx * t + x = kx * t + m
vy * t + y = ky * t + m
vz * t + z = kz * t + m

<=>

0 = (k_x - vx) * t + (m_x - x) => t = (x - m_x) / (k_x - vx)
0 = (k_y - vy) * t + (m_y - y) = (k_y - vy) * (x - m_x) + (k_x - vx) * (m_y - y) (1)
0 = (k_z - vz) * t + (m_z - z) = (k_z - vz) * (x - m_x) + (k_x - vx) * (m_z - z) (2)

where the unknowns are x,y,z and vx,vy,vz

"""
import sympy

x,y,z,vx,vy,vz = sympy.symbols("x, y, z, vx, vy, vz") # unknowns

equations = []

t = 0
for i in range(len(ps)):
    k_x, k_y, k_z = vs[i]
    m_x, m_y, m_z = ps[i]
    equations.append((k_y - vy) * (x - m_x) + (k_x - vx) * (m_y - y))
    equations.append((k_z - vz) * (x - m_x) + (k_x - vx) * (m_z - z))
solution = sympy.solve(equations)[0]

print(solution[x] + solution[y] + solution[z])
