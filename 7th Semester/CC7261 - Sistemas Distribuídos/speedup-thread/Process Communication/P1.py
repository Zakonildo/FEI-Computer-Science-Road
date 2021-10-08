import time
import socket

# Funçaõ que busca pela solução, recebe algumas opções e trabalha para buscar servidores para resolver o problema.
def startSolution(timeToRun, filename, thread):

    # Criando o Socket do Cliente
    host = 'localhost'
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Se conectando ao servidor
    s.connect((host, port))

    # Captura o tempo inicial
    start_time = time.time()

    # Abre os arquivos (Leitura do números e escrita das chaves)
    fNums = open("file.csv", "r")
    fKeys = open(filename, "a")

    print("ESCREVENDO ARQUIVO...")

    # Começa a trabalhar
    for line in fNums.readlines():

        # Trata a linha do arquivo
        line = line.split(",")
        n1 = int(line[0])
        n2 = int(line[1])

        # Solicita que o servidor atenda a solicitação
        # Mensagem no padrão <n1> <n2> <estadoThread>
        s.sendall((str(n1) + " " + str(n2) + " " + thread).encode())

        # Captura a mensagem retornada pelo servidor (Chave)
        data = s.recv(200).decode()

        # Escreve a chave do arquivo
        fKeys.write(" KEY: " + data + "\n")
        
        # Pega a diferença de tempo
        timeDiff = time.time() - start_time

        # Se passou do tempo, ele quebra
        if(timeDiff >= timeToRun and timeToRun > 0):
            break
    
    print("ARQUIVO PRONTO!")

    # Agradece o atendimento e pede para encerrar as atividades dos servidores
    s.sendall(str("END").encode())

    # Fecha os arquivos
    fNums.close()
    fKeys.close()

# Aqui é a limpeza do documento no qual será trabalhado
def clearKeysDocument(filename):
    f = open(filename, "w").close()
    return

# Main, aqui é o menu de P1, configurações iniciais
def main():
    timeLimit = int(input("DIGITE QUANTO TEMPO VOCÊ QUER RODAR (Segundos): "))
    thread = int(input("QUER UTILIZAR THREAD (0 = Não | 1 = Sim)?: "))
    if(thread == 1):
        clearKeysDocument("myKeysThread.txt")
        startSolution(timeLimit, "myKeysThread.txt", "On")
    else:
        clearKeysDocument("myKeys.txt")
        startSolution(timeLimit, "myKeys.txt", "Off")

main()