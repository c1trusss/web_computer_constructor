arr = list(map(int, input().split()))

max1pos, max2pos = 0, 0
min1neg, min2neg = 0, 0
for n in arr:
    if n < 0:
        if n < min1neg:
            min1neg, min2neg = n, min1neg
        elif n < min2neg:
            min2neg = n
    else:
        if n > max1pos:
            max1pos, max2pos = n, max1pos
        elif n > max2pos:
            max2pos = n

if len(arr) == 2:
    print(*sorted(arr))
elif min1neg * min2neg > max1pos * max2pos:
    print(min1neg, min2neg)
else:
    print(max2pos, max1pos)