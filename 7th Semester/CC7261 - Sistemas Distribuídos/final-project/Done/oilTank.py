import random
import socket

class OilTank:
    def __init__(self):
        self.total = 0.0
        self.time = 0.0
        self.status = "NONE"
        self.deployied = 0.0
        return

    def getInfo(self):
        return self.total

    def deploy(self):
        self.status = "DEPLOYING"
        return
    
    def run(self):
        self.time += 0.01

        self.time = round(self.time, 2)
        
        if ( self.time % 10 == 0 ):
            totalTemp = self.total
            self.total = random.randrange(1000, 2000, 5)
            self.total /= 1000.0
            self.total += totalTemp
            self.total = round(self.total, 3)

        if(self.status == "DEPLOYING"):
            if( self.total - 0.005 < 0):
                self.deployied = 0.0
                self.total = 0.0
            
            else:
                self.total -= 0.005
                self.deployied = 0.005
            
            self.total = round(self.total, 3)
            self.deployied = round(self.deployied, 3)

            self.status = "NONE"

        else:
            self.deployied = 0
        
        return self.deployied

def main():
    oilTank = OilTank()

    host = 'localhost'
    port = 50000
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

            if(msg == "RUN"):
                value = oilTank.run()
                conn.sendall(str(value).encode())

            elif(msg == "DEPLOY"):
                oilTank.deploy()
                conn.sendall("DONE".encode())

            elif(msg == "INFO"):
                value = oilTank.getInfo()
                conn.sendall(str(value).encode())

            elif(msg == "END"):
                conn.sendall("OK".encode())
                conn.close()
                break

main()