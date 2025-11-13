from collections import deque
with open(0) as file:
    line = file.readlines()[0].strip('\n')
    count1 = 0
    dq = deque()
    for c in line:
        count1 += 1
        if len(dq) < 14:
            dq.append(c)
        else:
            dq.append(c)
            dq.popleft()

        if len(set(dq)) == 14:
            break
    print(count1)
