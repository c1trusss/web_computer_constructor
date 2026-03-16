from math import ceil

k1, m, k2, p2, n2 = map(int, input().split())

flats_on_floor = ceil(k2 / n2)
p1 = ceil(k1 / (flats_on_floor * m))
n1 = ceil((k1 % (flats_on_floor * m)) / flats_on_floor)


if n2 > m or k2 < n2:
    print(-1, -1)
elif n2 == 1 and p2 == 1:
    print(0, n2)
else:
    print(p1, n1)