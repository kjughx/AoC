import numpy as np

with open(0) as file:
    sensors = []
    row = set()
    nrow = 2_000_000
    for line in file.readlines():
        line = line.strip('\n').split(' ')
        sx, sy = int(line[2].split('=')[1].strip(',')), int(line[3].split('=')[1].strip(':'))
        bx, by = int(line[-2].split('=')[1].strip(',')), int(line[-1].split('=')[1].strip(':'))

        d = abs(sx - bx) + abs(sy - by)
        sensors.append((sx, sy, d))

        if nrow in range(sy-d,sy+d+1):
            n = abs(nrow - sy)
            for x in range(sx - (d-n), sx + (d-n) + 1):
                if x not in row:
                    row.add(x)

    print(len(row)-1)

    N = 4_000_000
    for y in range(N+1):
        intervals = []
        for sx, sy, d in sensors:
            n = d - abs(y - sy)
            if n < 0:
                continue

            intervals.append([sx-n, sx+n+1])

        # if this list doesn't cover the entire row, it's golden
        # so stitch together the intervals
        intervals.sort()
        low, high = None, None
        for xb, xe in intervals:
            if low == None: low = xb if xb > 0 else 0
            if high == None: high = xe if xb < N else N
            if xb < low: low = xb if xb > 0 else 0
            if xe > high and xb <= high:
                high = xe if xe < N else N
        if (high - low) != N:
            print(high * 4000000 + y)
