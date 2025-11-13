import numpy as np
def draw(crt, opc, regx):
    if opc in range(regx-1, regx+2):
        return crt + '#'
    else:
        return crt + '.'

with open(0) as file:
    poss = [20, 60, 100, 140, 180, 220]
    posi = 0
    regx = 1
    total = 0
    opc = 1
    file = file.readlines()
    crt = ""
    did = 0
    pid = regx

    for line in file:
        line = line.strip('\n').split(' ')
        print(line, regx)
        if posi != len(poss):
            if opc == poss[posi] or abs(opc - poss[posi]) == 1:
                total += poss[posi]*regx
                posi += 1
        if line[0] == 'addx':
            crt = draw(crt, (opc-1)%40, regx)
            opc += 1
            crt = draw(crt, (opc-1)%40, regx)
            opc += 1
            regx += int(line[1])
        else:
            crt = draw(crt, (opc-1)%40, regx)
            opc += 1
    print(total)

    crt = np.array([c for c in crt]).reshape(int(len(crt)/40), 40)
    for row in crt:
        print("".join(row))
