import random 
for i in range(2000):
    x = random.randint(1, 3)
    if x == 3:
        day = random.randint(1, 7)
        if day == 1 or day == 2 or day == 5: #sun, mon, fri 
            if random.randint(0,1) == 0:
                time = 10
            else:
                time = 11
        else:
            time = 3
    elif x == 2:
        day = random.randint(1, 7)
        if day == 3 or day == 5 or day == 6: #tue, fri, sat 
            if random.randint(0,1) == 0:
                time = 5
            else:
                time = 6
        else: 
            time = 12
    else:
        day = random.randint(1, 7)
        if day == 2 or day == 1 or day == 4: #sun, mon, th
            if random.randint(0,1) == 0:
                time = 2
            else:
                time = 4
        else: 
            time = 22

    print(f'{day},{time},{x}')


def merge(a, start1, start2, end):
    index1 = start1
    index2 = start2
    length = end - start1
    aux = [None] * length
    for i in range(length):
        if ((index1 == start2) or
            ((index2 != end) and (a[index1] > a[index2]))):
            aux[i] = a[index2]
            index2 += 1
        else:
            aux[i] = a[index1]
            index1 += 1
    for i in range(start1, end):
        a[i] = aux[i - start1]

def mergeSort(a):
    n = len(a)
    step = 1
    while (step < n):
        for start1 in range(0, n, 2*step):
            start2 = min(start1 + step, n)
            end = min(start1 + 2*step, n)
            merge(a, start1, start2, end)
        step *= 2
