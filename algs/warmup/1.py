from string import ascii_lowercase


def decode(s):
    i = 0
    result = ''
    while i < len(s):
        ch = s[i]
        if i + 2 < len(s) and s[i + 2] == "#":
            result += ascii_lowercase[int(s[i:i + 2]) - 1]
            i += 3
        else:
            result += ascii_lowercase[int(ch) - 1]
            i += 1

    return result


print(decode(input()))