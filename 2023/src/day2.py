#!/bin/env python3
import re
RED = 12
GREEN = 13
BLUE = 14

with open(0) as file:
    imps = 0
    pwrs = 0
    for line in file.readlines():
        line = line.strip('\n')
        id = int(re.findall("Game ([0-9]*)", line)[0])
        _, line = line.split(": ")
        imp = False
        mred = 0
        mgreen = 0
        mblue = 0
        for s in line.split("; "):
            for cube in s.split(", "):
                cnt, clr = cube.split(" ")
                cnt = int(cnt)
                match clr:
                    case "blue":
                        if cnt > BLUE:
                            imp = True
                        if cnt > mblue:
                            mblue = cnt
                    case "green":
                        if cnt > GREEN:
                            imp = True
                        if cnt > mgreen:
                            mgreen = cnt
                    case "red":
                        if cnt > RED:
                            imp = True
                        if cnt > mred:
                            mred = cnt
                    case _:
                        exit(1)
        if not imp:
            imps = imps + id
        pwrs = pwrs + mred * mgreen * mblue
    print(imps)  # part 1
    print(pwrs)  # part 2
