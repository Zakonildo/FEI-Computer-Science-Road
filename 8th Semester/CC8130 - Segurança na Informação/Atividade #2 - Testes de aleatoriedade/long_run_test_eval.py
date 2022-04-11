import binaryKey as bk

def solve(key):

    binKey = bk.HexToBinary(key)
    last = binKey[0]
    index = 0

    for i in binKey:
        if i == last:
            index += 1
            if(index >= 34):
                return [False]
        else:
            last = i
            index = 1

    return [True]