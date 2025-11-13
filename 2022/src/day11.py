class Monkey:
    def __init__(self, items, op, test, to):
        self.items = items
        self.lop = op
        self.to = to
        self.ltest = test
        self.c = 0

    def op(self, x):
        self.c += 1
        match self.lop[0]:
            case '*':
                if len(self.lop) == 1:
                    return x * x
                else:
                    return  x * self.lop[1]
            case '+':
                if len(self.lop) == 1:
                    return x + x
                else:
                    return x + self.lop[1]

    def test(self, x):
        if x % self.ltest == 0:
            return self.to[0]
        else:
            return self.to[1]

from collections import deque
with open(0) as file:
    mks = []
    mkline = [[]]
    lines = [line.strip('\n') for line in file.readlines()]
    mkid = 0
    for line in lines:
        if line != '':
            mkline[mkid].append(line)
        else:
            mkline.append([])
            mkid+=1

    mkid = 0
    for monkey in mkline:
        stitems = deque([int(item) for item in monkey[1].split(':')[1].strip().split(', ')])
        op = monkey[2].split(':')[1].strip().split(' ')
        match op[3:]:
            case ['*', x]:
                op = ['*']
                if x.isdigit(): op.append(int(x))
            case ['+', x]:
                op = ['+']
                if x.isdigit(): op.append(int(x))

        test = int(monkey[3].strip().split(' ')[3])
        truto = int(monkey[4].strip().split(' ')[-1])
        falto = int(monkey[5].strip().split(' ')[-1])
        mks.append(Monkey(stitems, op, test, [truto,falto]))

    # part 1
    # for _ in range(20):
    #     for monkey in mks:
    #         for item in monkey.items.copy():
    #             item = int(monkey.op(item) / 3)
    #             monkey.items.popleft()
    #             id = monkey.test(item)
    #             # print(id, item)
    #             mks[id].items.append(item)
    #         # print('---')
    #     break
    # # for monkey in mks:
    #     # print(monkey.items)
    # act = [monkey.c for monkey in mks]
    # act.sort()
    # print(act[-1] * act[-2])


    # # part 2
    for monkey in mks:
        items = monkey.items.copy()
        monkey.items = deque([[item % mks[id].ltest for id in range(len(mks))] for item in items])

    for _ in range(10000):
        mkid = 0
        for mkid in range(len(mks)):
            monkey = mks[mkid]
            for item in monkey.items.copy():
                nitem = [monkey.op(item[id]) % mks[id].ltest for id in range(len(mks))]
                id = monkey.test(nitem[mkid])
                mks[id].items.append(nitem)

                monkey.items.popleft()
            mkid += 1

    act = [monkey.c/len(mks) for monkey in mks]
    act.sort()
    print(act[-1] * act[-2])
