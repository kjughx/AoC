import numpy as np

def isclose(x1, y1, x2, y2):
    return (abs(x1-x2) <= 1 and abs(y1 - y2) <= 1)

with open(0) as file:
    startx, starty = 0,0
    xtyt = [[startx, starty] for _ in range(10)]
    xh, yh = startx,starty
    xt, yt = startx,starty
    map = {(xt, yt)}
    for line in file.readlines()[:]:
        dir, step = line.strip('\n').split(' ')
        step = int(step)
        for i in range(step):
            xh,yh = xtyt[0]
            if dir == 'R': yh += 1
            if dir == 'L': yh -= 1
            if dir == 'U': xh -= 1
            if dir == 'D': xh += 1
            xtyt[0] = [xh, yh]
            for i in range(1, len(xtyt)):
                xh,yh = xtyt[i-1]
                xt,yt = xtyt[i]
                if not isclose(xh, yh, xt, yt):
                    xt += np.sign(xh-xt)
                    yt += np.sign(yh-yt)
                        
                    xtyt[i] = [xt, yt]
            xt,yt = xtyt[-1]
            map |= {(xt, yt)}
    print(len(map))
