n = int(input())
companies = tuple(map(int, input().split()))

dp = [0 for _ in range(n)]  # dp[i] = максимальная сумма i-й компании вместе с собой
dp_need = [0 for _ in range(n)]     # dp_need[i] - сколько нужно i-й компании иметь после поглощения младших на старте,
                                    # чтобы суметь победить
dp_potential = [0 for _ in range(n)]  # может победить или нет

dp[0] = companies[0]
if n > 1:
    dp_need[-1] = companies[-2] + 1
for i in range(n - 2, -1, -1):
    dp_need[i] = max(dp_need[i + 1] - companies[i], companies[i + 1] - companies[i] + 1)

for i in range(1, n):
    dp[i] = dp[i - 1] + companies[i]
    if dp[i] - companies[i] >= dp_need[i]:
        dp_potential[i] = 1

for i in dp_potential:
    print(i)

print(companies)
print(dp)
print(dp_need)
print(dp_potential)
