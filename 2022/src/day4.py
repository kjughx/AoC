with open(0) as file:
    count1 = 0
    count2 = 0
    for line in file.readlines():
        range1,range2 = line.strip('\n').split(',')
        start1,end1 = range1.split('-')
        start1,end1 = int(start1), int(end1)
        range1 = range(start1, end1+1)
        start2,end2 = range2.split('-')
        start2,end2 = int(start2), int(end2)
        range2 = range(start2, end2+1)


        if (start2 <= start1 and end1 <= end2) or (start1 <= start2 and end2 <= end1):
            count1 += 1

        if (start1 in range2 or end1 in range2 or start2 in range1 or end2 in range1):
            count2 += 1

    print(count1)
    print(count2)
