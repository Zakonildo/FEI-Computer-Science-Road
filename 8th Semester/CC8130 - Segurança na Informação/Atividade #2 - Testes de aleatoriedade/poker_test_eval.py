import binaryKey as bk

def solve(key):

    count = {
        '0' : 0,
        '1' : 0,
        '2' : 0,
        '3' : 0,
        '4' : 0,
        '5' : 0,
        '6' : 0,
        '7' : 0,
        '8' : 0,
        '9' : 0,
        'A' : 0,
        'B' : 0,
        'C' : 0,
        'D' : 0,
        'E' : 0,
        'F' : 0
    }

    for i in key:
        count[i] += 1

    countSum = 0

    for i in count.items():
        countSum += i[1]*i[1]
    
    result = ((16/5000) * countSum) - 5000

    if (result > 1.03 and result < 57.4):
        return result, count, True
    
    else:
        return result, count, False