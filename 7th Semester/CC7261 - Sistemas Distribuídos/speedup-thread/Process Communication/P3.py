import socket
import threading

maxInitNumber = 0
allPrimeNumbers = []
primeCheckpoints = {}

# Ouve o cliente P2
def listening():

    # Cria o Socket para ouvir P2.
    host = 'localhost'
    port = 1500
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( (host, port) )
    s.listen()

    # Aguarda chamdo de P2
    while True:
        print("AGUARDANDO CONEXÃO...")

        conn, ender = s.accept()

        print("ATENDENDO SERVIDOR P2 EM", ender)

        # Atende
        while True:
            data = conn.recv(200)

            if(data.decode() == "END"):
                print("FINALIZANDO...")
                conn.close()
                return

            param = data.decode().split(" ")

            var = [0, 0, 0, 0, 0, 0, 0, 0]

            key = 0

            # Se ele pedir para usar Thread, a chave será calculada com thread
            if(param[3] == "On"):
                t0 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2]), var, 0))
                t1 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2])+1, var, 1))
                t2 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2])+2, var, 2))
                t3 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2])+3, var, 3))
                t4 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2])+4, var, 4))
                t5 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2])+5, var, 5))
                t6 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2])+6, var, 6))
                t7 = threading.Thread(target=findKey, args=(int(param[0]), int(param[1]), int(param[2])+7, var, 7))

                t0.start()
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
                t6.start()
                t7.start()

                t0.join()
                t1.join()
                t2.join()
                t3.join()
                t4.join()
                t5.join()
                t6.join()
                t7.join()

                for i in var:
                    if i != 0:
                        key = i

            # Caso contrário, busca a chave de forma sequêncial
            else:
                key = findKeySingle(int(param[0]), int(param[1]), int(param[2]))

            # Retorna a chave para P2
            conn.sendall(str(key).encode())

# Mesma coisa que P2
def getAllPrimes(n):

    # Populate prime array.
    prime = [True for i in range(n + 1)]
    p = 2

    # Classify all n numbers into primes and
    # non-primes.
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1

    totalPrimes = 0
    allPrimeNumbers = []
    primeCheckpoint = {}

    # Get all prime numbers splited into an array
    # and get primes checkpoints.
    for number in range(2, n + 1):
        if prime[number] and number != n:
            totalPrimes += 1
            allPrimeNumbers.append(number)

        if(number % 100000 == 0):
            primeCheckpoint[number] = totalPrimes


    return primeCheckpoint, allPrimeNumbers

# Mesma coisa que P2
def getMaxInitNumber():
    maxInitNumber = 0

    fNums = open("file.csv", "r")

    for i in fNums.readlines():
            i = i.split(",")
            if(int(i[0]) > maxInitNumber):
                maxInitNumber = int(i[0])

    fNums.close()

    return maxInitNumber

# Mesma coisa, só que com Thread
def findKey(n1, n2, total, var, i):
    global allPrimeNumbers
    before = 0
    after = 0

    while(True):
        if (allPrimeNumbers[total-1] < n1):
            total += 8
        else:
            if (allPrimeNumbers[total - 2] >= n1):
                var[i] = 0
                return

            before = allPrimeNumbers[total - 1 - n2]

            if(allPrimeNumbers[total-1] == n1):
                after = allPrimeNumbers[total - 1 + n2]
            else:
                after = allPrimeNumbers[total - 2 + n2]

            break
    
    var[i] = (before*after)
    return

# Encontra a chave
def findKeySingle(n1, n2, total):
    global allPrimeNumbers
    before = 0
    after = 0

    while(True):
        # Se o primo atual for menor que n1, avança para o próximo primo
        if (allPrimeNumbers[total-1] < n1):
            total += 1

        # Se for maior, ele volta n2 indíces para encontra o anterior e avança n2 - 1 indíces para
        # achar o posterior. Caso o primo atual seja o próprio n1, o posterior só deve avançar n2
        # indíces.
        else:
            before = allPrimeNumbers[total - 1 - n2]

            if(allPrimeNumbers[total-1] == n1):
                after = allPrimeNumbers[total - 1 + n2]
            else:
                after = allPrimeNumbers[total - 2 + n2]

            break
    
    # Calcula a chave e retornna ela
    return(before*after)

# Mesma coisa que P2
def initialize():
    global maxInitNumber, primeCheckpoints, allPrimeNumbers

    print("INICIANDO SERVIDOR P3...")

    maxInitNumber = getMaxInitNumber()
    primeCheckpoints, allPrimeNumbers = getAllPrimes(maxInitNumber + 1000000)

    listening()

    return

initialize()