from random import randint


def equal_case(A, B, C, D):
    if A == B and C == D:
        return min(A, C) + 1, 1
    elif A == B:
        return A + 1, 1
    elif C == D:
        return 1, C + 1


def solution(A, B, C, D):
    variants = []
    if A == B or C == D:
        variants.append(equal_case(A, B, C, D))
    if A + C > B + D or (B == 0 or D == 0):
        variants.append((B + 1, D + 1))
    else:
        variants.append((A + 1, C + 1))

    if A and B:
        variants.append((A + B, 1))
    if C and D:
        variants.append((1, C + D))

    return min(variants, key=sum)


print(*solution(*(int(input()) for _ in range(4))))


for i in range(10):
    a, b, c, d = (randint(0, 10) for _ in range(4))
    sol = solution(a, b, c, d)

    print(a, b, ' ', c, d, '|', sol)