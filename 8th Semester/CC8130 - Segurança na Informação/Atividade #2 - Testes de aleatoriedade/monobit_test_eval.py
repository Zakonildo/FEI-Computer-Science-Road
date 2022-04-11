import binaryKey as bk

def solve(key):
    binKey = bk.HexToBinary(key)

    count1 = 0
    for i in binKey:
        if (i == "1"):
            count1 += 1

    if (count1 > 9654 and count1 < 10346):
        return count1, True
    else:
        return count1, False
