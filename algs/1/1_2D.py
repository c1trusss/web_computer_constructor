t0, t1 = map(int, input().split())
mode = input()

match mode:
    case "fan":
        print(t0)
    case "auto":
        print(t1)
    case "heat":
        print(max(t0, t1))
    case "freeze":
        print(min(t0, t1))