#!/bin/env python3
import numpy as np

def sy(c):
    return not (c.isdigit() or c == '.' or c == ' ')

mat=[]
with open(0) as file:
    for line in file.readlines():
        line = line.strip('\n')
        mat.append([c for c in line])
mat = np.array(mat)
s = mat.shape
t=0
gr = {}
for i in range(s[0]):
    gs = set()
    isp = False
    n=""
    for j in range(s[1]+1):
        if j < s[1] and mat[i,j].isdigit():
            n += mat[i,j]
            for ii in [-1,0,1]:
                for jj in [-1,0,1]:
                    if 0<= i + ii < s[0] and 0 <= j + jj < s[1]:
                        c = mat[i + ii, j + jj]
                        cc = (i + ii, j + jj)
                        isp |= sy(c)
                        if c == "*":
                            gs.add(cc)
        elif len(n) > 0:
            if isp:
                t += int(n)
            for g in gs:
                if g not in gr:
                    gr[g] = [int(n)]
                else:
                    gr[g].append(int(n))
            n = ""
            isp = False
            gs = set()

t2 = 0
for g in gr.values():
    if len(g) == 2:
        t2 += g[0] * g[1]

print(t)
print(t2)
