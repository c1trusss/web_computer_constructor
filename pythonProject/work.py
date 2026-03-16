a = input()

index = 0
for i in range(len(a)):
    x = a[:i - 1] + a[i:]
    if x == x[::-1]:
        index = i

print(index)
