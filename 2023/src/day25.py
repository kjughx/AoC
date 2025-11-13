#!/usr/bin/env python3
import networkx as nx

lines = [line.strip() for line in open(0).readlines()]

cables = {}
for line in lines:
    c1, rest = line.split(':')
    if c1 not in cables:
        cables[c1] = set()
    for cable in rest.strip().split(' '):
        if cable not in cables:
            cables[cable] = set()
        cables[c1].add(cable)
        cables[cable].add(c1)

g = nx.Graph()

for key, val in cables.items():
    for v in val:
        g.add_edge(key, v, capacity=1)


for c1 in cables.keys():
    for c2 in cables.keys():
        if c1 != c2:
            n, (g1, g2) = nx.minimum_cut(g, c1, c2)
            if n == 3:
                print(len(g1) * len(g2))
                exit(0)
