p, v = map(int, input().split())
q, m = map(int, input().split())

left1, right1 = p - v, p + v
left2, right2 = q - m, q + m

if left1 > left2:
    left1, right1, left2, right2 = left2, right2, left1, right1

if left2 > right1:
    print((right1 - left1 + 1) + (right2 - left2 + 1))
else:
    print(max(right1, right2) - left1 + 1)
