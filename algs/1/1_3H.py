a, b, c = (int(input()) for _ in range(3))

if c < 0:
    print("NO SOLUTION")
elif a == 0:
    if b == c ** 2:
        print("MANY SOLUTIONS")
    else:
        print("NO SOLUTION")
else:
    solution = (c ** 2 - b) / a
    if int(solution) == solution:
        print(int(solution))
    else:
        print("NO SOLUTION")