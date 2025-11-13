file = open(0)

priorities1 = 0
lines=[]
for line in file.readlines():
    lines.append(line.strip('\n'))
    line = line.strip('\n')
    n = int(len(line)/2)
    first,second = line[0:n], line[n::]
    for let in first:
        if let in second:
            if let.isupper():
                priorities1 += ord(let) - 38 # A == 65 - 38 == 27
            else:
                priorities1 += ord(let) - 96 # a == 97 - 96 == 1
            break
print(priorities1)

priorities2 = 0
for i in range(0, len(lines), 3):
    m1 = {c for c in lines[i]}
    m2 = {c for c in lines[i+1]}
    m3 = {c for c in lines[i+2]}
    let = m1.intersection(m2.intersection(m3)).pop()
    print('=========')
    print(let)
    print(m1)
    print(m2)
    print(m3)
    print('=========')
    if let.isupper():
        priorities2 += ord(let) - 38 # A == 65 - 38 == 27
    else:
        priorities2 += ord(let) - 96 # a == 97 - 96 == 1
print(priorities2)

