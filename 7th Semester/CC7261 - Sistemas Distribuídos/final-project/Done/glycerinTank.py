import socket

class GlycerinTank:
    def __init__(self):
        self.total = 0.0
        self.time = 0.0
        return

    def getInfo(self):
        return self.total

    def receive(self, value):
        self.total += value
        self.total = round(self.total, 3)
        return

def main():
    glycerinTank = GlycerinTank()

    host = 'localhost'
    port = 50003
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind( (host, port) )
    s.listen()

    while True:
        conn, ender = s.accept()

        print(ender)

        while True:
            data = conn.recv(200)

            msg = data.decode()

            if(msg == "INFO"):
                value = glycerinTank.getInfo()
                conn.sendall(str(value).encode())

            elif(msg.find("SEND") > -1):
                msg = msg.split(" ")
                glycerinTank.receive(float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg == "END"):
                conn.sendall("OK".encode())
                conn.close()
                break

main()