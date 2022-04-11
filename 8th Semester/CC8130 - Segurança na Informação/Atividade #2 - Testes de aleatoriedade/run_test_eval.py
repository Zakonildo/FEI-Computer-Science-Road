import binaryKey as bk

def evalRange(num, less, greater):
    if(num > less and num < greater):
        return True
    else:
        return False

def solve(key):

    binKey = bk.HexToBinary(key)
    last = binKey[0]

    index = 0

    count0 = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
    }

    count1 = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
    }

    for i in binKey:
        if i == last:
            index += 1
        else:
            if(last == "0"):
                if (index > 6):
                    count0[6] += 1
                else:
                    count0[index] += 1
            
            elif (last == "1"):
                if (index > 6):
                    count1[6] += 1
                else:
                    count1[index] += 1

            last = i
            
            index = 1

    if(index > 1 and last == "0"):
        if (index > 6):
            count0[6] += 1
        else:
            count0[index] += 1

    elif(index > 1 and last == "1"):
        if (index > 6):
            count1[6] += 1
        else:
            count1[index] += 1

    if (
        evalRange(count0[1], 2267, 2773) and
        evalRange(count0[2], 1079, 1421) and
        evalRange(count0[3], 502, 748) and
        evalRange(count0[4], 223, 402) and
        evalRange(count0[5], 90, 223) and
        evalRange(count0[6], 90, 223) and
        evalRange(count1[1], 2267, 2773) and
        evalRange(count1[2], 1079, 1421) and
        evalRange(count1[3], 502, 748) and
        evalRange(count1[4], 223, 402) and
        evalRange(count1[5], 90, 223) and
        evalRange(count1[6], 90, 223)
    ):
        return count0, count1, True
    
    else:
        return count0, count1, False