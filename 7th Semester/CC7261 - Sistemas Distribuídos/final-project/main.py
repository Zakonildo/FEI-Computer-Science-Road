import socket
import time

timer = 0
decReceived = 0
dryReceived = 0
dry2Received = 0

oilSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
oilSocket.connect(('localhost', 50000))
oilSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

elementsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
elementsSocket.connect(('localhost', 50001))
elementsSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

biodieselSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
biodieselSocket.connect(('localhost', 50002))
biodieselSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

glycerinSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
glycerinSocket.connect(('localhost', 50003))
glycerinSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

reactorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
reactorSocket.connect(('localhost', 50004))
reactorSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

decanterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
decanterSocket.connect(('localhost', 50005))
decanterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

dryerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dryerSocket.connect(('localhost', 50006))
dryerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

dryer2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dryer2Socket.connect(('localhost', 50007))
dryer2Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

washerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
washerSocket.connect(('localhost', 50008))
washerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


f = open("Data.txt" ,"w")

while(True):
    # GET INFO
    oilSocket.sendall("INFO".encode())
    oilInfo = float(oilSocket.recv(200).decode())

    elementsSocket.sendall("INFO".encode())
    elementsInfo = list(elementsSocket.recv(200).decode().split(";"))

    for i in range(0, len(elementsInfo)):
        elementsInfo[i] = float(elementsInfo[i])

    biodieselSocket.sendall("INFO".encode())
    biodieselInfo = float(biodieselSocket.recv(200).decode())

    glycerinSocket.sendall("INFO".encode())
    glycerinInfo = float(glycerinSocket.recv(200).decode())

    reactorSocket.sendall("INFO".encode())
    reactorInfo = list(reactorSocket.recv(200).decode().split(";"))

    for i in range(0, len(reactorInfo)):
        if(i < 4):
            reactorInfo[i] = float(reactorInfo[i])
        elif(i == 5):
            reactorInfo[i] = int(reactorInfo[i])

    decanterSocket.sendall("INFO".encode())
    decanterInfo = list(decanterSocket.recv(200).decode().split(";"))

    for i in range(0, len(decanterInfo)):
        if(i < 4):
            decanterInfo[i] = float(decanterInfo[i])

    dryerSocket.sendall("INFO".encode())
    dryerInfo = list(dryerSocket.recv(200).decode().split(";"))

    for i in range(0, len(dryerInfo)):
        if(i < 1):
            dryerInfo[i] = float(dryerInfo[i])

    dryer2Socket.sendall("INFO".encode())
    dryer2Info = list(dryer2Socket.recv(200).decode().split(";"))

    for i in range(0, len(dryer2Info)):
        if(i < 1):
            dryer2Info[i] = float(dryer2Info[i])

    washersInfo = []

    washerSocket.sendall("[1] INFO".encode())
    washersInfo.append(washerSocket.recv(200).decode())

    washerSocket.sendall("[2] INFO".encode())
    washersInfo.append(washerSocket.recv(200).decode())

    washerSocket.sendall("[3] INFO".encode())
    washersInfo.append(washerSocket.recv(200).decode())

    for i in range(0, len(washersInfo)):
        if(i < 1):
            washersInfo[i] = float(washersInfo[i])

    #print(oilInfo)
    #print(elementsInfo)
    #print(reactorInfo)
    #print(decanterInfo)
    #print(dryerInfo)
    #print(washersInfo)
    #print(dryer2Info)
    #print(biodieselInfo)
    #print(glycerinInfo)

    # WRITE FILE
    if (timer % 10 == 0):
        f.write("\n")

        f.write("TIMER: %.2fs\n" % (timer/100))

        f.write(("GLICERINA PRODUZIDA: %.3f L\n" % glycerinInfo))

        f.write(("BIODIESEL PRODUZIDO: %.3f L\n" % biodieselInfo))

        f.write(("""VOLUME DOS TANQUES: [OLEO]   |   [NaOH]   |   [EtOH]
                    %4.4f L | %4.4f L | %4.4f L\n""" % (oilInfo, elementsInfo[0], elementsInfo[1]) ))

        f.write(("CICLOS REALIZADOS PELO REATOR: %d\n" % (reactorInfo[5])))
        
        f.write("\n")

    # REACTOR NEEDS
    if ( reactorInfo[0] < 1.25 and oilInfo > 0 and reactorInfo[3] == 0.0):
        oilSocket.sendall("DEPLOY".encode())
        oilSocket.recv(200).decode()

    if ( reactorInfo[1] < 1.25 and reactorInfo[2] < 2.5 and reactorInfo[3] == 0.0 and 
         elementsInfo[0] > 0 and elementsInfo[1] > 0):
        elementsSocket.sendall("DEPLOY BOTH".encode())
        elementsSocket.recv(200).decode()

    elif ( reactorInfo[1] < 1.25 and reactorInfo[3] == 0.0 and elementsInfo[0] > 0 ):
        elementsSocket.sendall("DEPLOY NaOH".encode())
        elementsSocket.recv(200).decode()

    elif ( reactorInfo[2] < 2.5 and reactorInfo[3] == 0.0 and elementsInfo[1] > 0 ):
        elementsSocket.sendall("DEPLOY EtOH".encode())
        elementsSocket.recv(200).decode()

    # RUN TANKS
    oilSocket.sendall("RUN".encode())
    oilDeploy = float(oilSocket.recv(200).decode())

    elementsSocket.sendall("RUN".encode())
    elementsDeploy = list(elementsSocket.recv(200).decode().split(";"))

    for i in range(0, len(elementsDeploy)):
        elementsDeploy[i] = float(elementsDeploy[i])

    oilSocket.sendall("INFO".encode())
    oilInfo = float(oilSocket.recv(200).decode())

    elementsSocket.sendall("INFO".encode())
    elementsInfo = list(elementsSocket.recv(200).decode().split(";"))

    for i in range(0, len(elementsInfo)):
        elementsInfo[i] = float(elementsInfo[i])

    # RECEIVE FROM TANKS
    reactorSocket.sendall(("SEND Oil " + str(oilDeploy)).encode())
    reactorSocket.recv(200).decode()
    reactorSocket.sendall(("SEND NaOH " + str(elementsDeploy[0])).encode())
    reactorSocket.recv(200).decode()
    reactorSocket.sendall(("SEND EtOH " + str(elementsDeploy[1])).encode())
    reactorSocket.recv(200).decode()

    # REACTOR DECISION
    if(reactorInfo[0] + reactorInfo[1] + reactorInfo[2] == 5.0):
        reactorSocket.sendall(("PROCESS").encode())
        reactorSocket.recv(200).decode()

    if(reactorInfo[3] > 0 and reactorInfo[4] == "NONE" and decanterInfo[4] != "REST" ):
        reactorSocket.sendall(("DEPLOY").encode())
        reactorSocket.recv(200).decode()

    # RUN REACTOR
    reactorSocket.sendall(("RUN").encode())
    reactorDeploy = float(reactorSocket.recv(200).decode())

    reactorSocket.sendall("INFO".encode())
    reactorInfo = list(reactorSocket.recv(200).decode().split(";"))

    for i in range(0, len(reactorInfo)):
        if(i < 4):
            reactorInfo[i] = float(reactorInfo[i])
        elif(i == 5):
            reactorInfo[i] = int(reactorInfo[i])


    # DECANTER DECISION

    if(decanterInfo[4] != "REST" and decanterInfo[4] != "DEPLOYING"):

        if(reactorDeploy != 0.0):
            # RECEIVE FROM REACTOR
            decanterSocket.sendall(("SEND " + str(reactorDeploy)).encode())
            decanterSocket.recv(200).decode()
            decReceived += reactorDeploy
            decReceived = round(decReceived, 2)

        if ( ( reactorDeploy == 0.0 and decReceived != 0.0 ) or decReceived == 3.0):
            decReceived = 0.0
            decanterSocket.sendall(("REST").encode())
            decanterSocket.recv(200).decode()

        elif ( reactorDeploy == 0.0 and decReceived == 0.0 and (decanterInfo[0] != 0 or decanterInfo[1] != 0 or decanterInfo[2] != 0) ):
            decanterSocket.sendall(("DEPLOY").encode())
            decanterSocket.recv(200).decode()

    # RUN DECANTER
    decanterSocket.sendall(("RUN").encode())
    decanterDeploy = list(decanterSocket.recv(200).decode().split(";"))

    for i in range(0, len(decanterDeploy)):
        decanterDeploy[i] = float(decanterDeploy[i])
    
    decanterSocket.sendall("INFO".encode())
    decanterInfo = list(decanterSocket.recv(200).decode().split(";"))

    for i in range(0, len(decanterInfo)):
        if(i < 4):
            decanterInfo[i] = float(decanterInfo[i])

    if(decanterInfo[4] == "DEPLOYING"):

        # RECEIVE GLYCERIN
        glycerinSocket.sendall(("SEND " + str(decanterDeploy[2])).encode())
        glycerinSocket.recv(200).decode()

        # RECEIVE SOLUTION
        washerSocket.sendall(("[1] SEND " + str(decanterDeploy[1])).encode())
        washerSocket.recv(200).decode()

    washerSocket.sendall(("[1] DEPLOY").encode())
    washerSocket.recv(200).decode()

    washerSocket.sendall(("[1] RUN").encode())
    washer01Deploy = float(washerSocket.recv(200).decode())

    washerSocket.sendall(("[1] INFO").encode())
    washer01Info = float(washerSocket.recv(200).decode())

    washerSocket.sendall(("[2] SEND " + str(washer01Deploy)).encode())
    washerSocket.recv(200).decode()

    washerSocket.sendall(("[2] DEPLOY").encode())
    washerSocket.recv(200).decode()

    washerSocket.sendall(("[2] RUN").encode())
    washer02Deploy = float(washerSocket.recv(200).decode())

    washerSocket.sendall(("[2] INFO").encode())
    washer02Info = float(washerSocket.recv(200).decode())

    washerSocket.sendall(("[3] SEND " + str(washer02Deploy)).encode())
    washerSocket.recv(200).decode()

    washerSocket.sendall(("[3] DEPLOY").encode())
    washerSocket.recv(200).decode()

    washerSocket.sendall(("[3] RUN").encode())
    washer03Deploy = float(washerSocket.recv(200).decode())

    washerSocket.sendall(("[3] INFO").encode())
    washer03Info = float(washerSocket.recv(200).decode())


    dryerSocket.sendall(("SEND " + str(washer03Deploy)).encode())
    dryerSocket.recv(200).decode()

    dryerSocket.sendall(("RUN").encode())
    dryerDeploy = float(dryerSocket.recv(200).decode())

    dryerSocket.sendall(("INFO").encode())
    dryerInfo = list(dryerSocket.recv(200).decode().split(";"))

    for i in range(0, len(dryerInfo)):
        if(i < 1):
            dryerInfo[i] = float(dryerInfo[i])
    
    biodieselSocket.sendall(("SEND " + str(dryerDeploy)).encode())
    biodieselSocket.recv(200).decode()

    dryer2Socket.sendall(("SEND " + str(decanterDeploy[0])).encode())
    dryer2Socket.recv(200).decode()

    dryer2Socket.sendall(("RUN").encode())
    dryer2Deploy = float(dryer2Socket.recv(200).decode())

    dryer2Socket.sendall(("INFO").encode())
    dryer2Info = list(dryer2Socket.recv(200).decode().split(";"))

    for i in range(0, len(dryer2Info)):
        if(i < 1):
            dryer2Info[i] = float(dryer2Info[i])
    
    elementsSocket.sendall(("SEND " + str(dryer2Deploy)).encode())
    elementsSocket.recv(200).decode()

    timer += 1

    if(timer > (360000)):
        oilSocket.sendall(("END").encode())
        oilSocket.recv(200).decode()

        elementsSocket.sendall(("END").encode())
        elementsSocket.recv(200).decode()

        reactorSocket.sendall(("END").encode())
        reactorSocket.recv(200).decode()

        decanterSocket.sendall(("END").encode())
        decanterSocket.recv(200).decode()

        washerSocket.sendall(("END").encode())
        washerSocket.recv(200).decode()

        dryerSocket.sendall(("END").encode())
        dryerSocket.recv(200).decode()

        dryer2Socket.sendall(("END").encode())
        dryer2Socket.recv(200).decode()

        biodieselSocket.sendall(("END").encode())
        biodieselSocket.recv(200).decode()

        glycerinSocket.sendall(("END").encode())
        glycerinSocket.recv(200).decode()
        break

f.close()