def getKeysByLine(filename):
    f = open(filename, "r")
    arr = []

    for i in f.readlines():
        key = i.replace("\n", "").replace("'", "")
        if (key != ""):
            arr.append(key)

    f.close()

    return arr