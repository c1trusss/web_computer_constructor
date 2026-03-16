houses = list(map(int, input().split()))

max_dist = 0
last_shop = None
for i, h in enumerate(houses):
    if h == 2:
        last_shop = i
        continue
    if h == 1:
        left_shop, right_shop = last_shop, i
        while houses[right_shop] != 2 and right_shop < 9:
            right_shop += 1
        if houses[right_shop] != 2:
            right_shop = None

        if left_shop is None:
            max_dist = max(max_dist, right_shop - i)
        elif right_shop is None:
            max_dist = max(max_dist, i - left_shop)
        else:
            max_dist = max(max_dist, min(right_shop - i, i - left_shop))

print(max_dist)
