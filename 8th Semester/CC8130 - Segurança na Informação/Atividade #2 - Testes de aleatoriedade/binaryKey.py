def HexToBinary(hexKey):
    binaryKey = int(hexKey, base=16)

    binaryKey = str(bin(binaryKey))[2:]

    if(len(binaryKey) < 20000):
        binaryKey = "0" + binaryKey

    return binaryKey