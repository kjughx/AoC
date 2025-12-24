#!/usr/bin/env python3
import sys
import re
import numpy as np

def main(data):
    parcels = []
    trees = []
    lines = data.splitlines()
    i = 0
    while i < len(lines):
        if re.search(r"\d+x\d+:", lines[i]):
            ns = list(map(int, re.findall(r"\d+", lines[i])))
            size, counts = ns[:2], ns[2:]
            trees.append((tuple(size), np.array(counts)))
            i += 1
        else:
            i += 1
            parcel = list(map(lambda line: re.sub('#', '1,', re.sub(r'\.', '0,', line)), lines[i:i+3]))
            parcel = [eval(p) for p in parcel]
            parcels.append(np.array(parcel))
            i += 4

    areas = np.array([sum(sum(parcel)) for parcel in parcels])
    n = 0
    for (w,h), counts in trees:
        if np.dot(areas, counts) <= w * h:
            n += 1
    print(n)


if __name__ == "__main__":
    main(sys.stdin.read())
