with open(0) as file:
    lines = [line.strip('\n') for line in file.readlines()]

    nstacks = 9 # CHANGE TO 9

    stacks = []
    for i in range(nstacks):
        stacks.append([line[1 + i*4] for line in lines[0:nstacks] if line[1 + i*4] != ' '])

    for stack in stacks:
        stack.reverse()

    # part1
    # for line in lines[nstacks+1::]:
    #     n, fr, to = [int(el) for el in line.split(' ')[1::2]]
    #     for _ in range(n):
    #         stacks[to -1].append(stacks[fr-1].pop())

    for line in lines[nstacks+1::]:
        n, fr, to = [int(el) for el in line.split(' ')[1::2]]
        print(n, stacks[fr-1][-1-n+1::])
        stacks[to-1].extend(stacks[fr-1][-1-n+1::])
        for _ in range(n):
            stacks[fr-1].pop()

    for stack in stacks:
        print(stack.pop())
