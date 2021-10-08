import socket

maxInitNumber = 0
allPrimeNumbers = []
primeCheckpoints = {}

# Escuta os clientes
def listening():

    # Cria um Socket de cliente que se conectará com P3
    conSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conSocket.connect(('localhost', 1500))

    # Cria um Socket de servidor para atender P1
    host = 'localhost'
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( (host, port) )
    s.listen()

    # Aguarda o chamado
    while True:
        print("AGUARDANDO CONEXÃO...")

        conn, ender = s.accept()

        print("CONEXÃO RECEBIDA DE", ender)

        # Atende
        while True:
            # Captura a mensagem
            data = conn.recv(200)

            # Se a mensagem for para finalizar, ele solicita o fechamento de P3 e encerra o processo
            if(data.decode() == "END"):
                print("FINALIZANDO...")
                conSocket.sendall(str("END").encode())
                conn.close()
                return

            # Separa os parâmetros
            param = data.decode().split(" ")

            # Captura a chave através da função solve (Veja a solve).
            key = solve(int(param[0]), int(param[1]), param[2], conSocket)

            # Retorna a chave para o cliente
            conn.sendall(str(key).encode())

# Se conecta com P3 para pegar a chave.
def connect(n1, n2, primeCheckpoint, conSocket, thread):

    conSocket.sendall((str(n1) + " " + str(n2) + " " + str(primeCheckpoint) + " " + thread).encode())

    data = conSocket.recv(200).decode()

    return data

# Pega todos os números primos e os checkpoints de primos (O dicionário que salva o total de primos até aqule número)
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

# Pega o maior n1 no arquivo file.csv
def getMaxInitNumber():
    maxInitNumber = 0

    fNums = open("file.csv", "r")

    for i in fNums.readlines():
            i = i.split(",")
            if(int(i[0]) > maxInitNumber):
                maxInitNumber = int(i[0])

    fNums.close()

    return maxInitNumber

# Realiza as obrigações necessárias para enncontrar a chave
def solve(n1, n2, thread, conSocket):
    global primeCheckpoints, allPrimeNumbers

    # Validação se existe chave
    if(n1 >= 1000000):

        # Pega o checkpoint mais próximo do número
        checkpoint = int(n1/100000) * 100000

        if(primeCheckpoints[checkpoint] >= 2*n2):

            # Chama a função connect para chamar P3 para resolver a chave.
            key = connect(n1, n2, primeCheckpoints[checkpoint], conSocket, thread)
    
    return key

# Inicializa o servidor
def initialize():
    global maxInitNumber, primeCheckpoints, allPrimeNumbers

    print("INICIANDO SERVIDOR P2...")

    maxInitNumber = getMaxInitNumber()
    primeCheckpoints, allPrimeNumbers = getAllPrimes(maxInitNumber + 1000000)

    listening()

    return

initialize()