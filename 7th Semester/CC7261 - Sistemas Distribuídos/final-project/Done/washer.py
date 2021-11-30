import socket

class Washer:
    def __init__(self):
        self.total = 0.0
        self.time = 0.0
        self.status = "NONE"
        self.deployied = 0.0
        return

    def getInfo(self):
        return self.total

    def receive(self, value):
        self.total += value
        self.total = round(self.total, 6)
        return

    def deploy(self):
        self.status = "DEPLOY"
        return

    def run(self):
        #time.sleep(0.01)
        self.time += 0.01

        self.time = round(self.time, 2)

        if(self.status == "DEPLOY"):
            if(self.total == 0):
                self.deployied = 0.0
            
            elif(self.total - 0.015 <= 0):
                self.deployied = self.total
                self
                self.total = 0.0

            else:
                self.total -= 0.015
                self.total = round(self.total, 6)
                self.deployied = 0.015

            self.deployied = self.deployied*0.905
            self.deployied = round(self.deployied, 6)

            self.status == "NONE"
            
            return self.deployied

        else:
            return 0.0

def main():
    washer1 = Washer()
    washer2 = Washer()
    washer3 = Washer()

    host = 'localhost'
    port = 50008
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

            if(msg == "[1] RUN"):
                value = washer1.run()
                conn.sendall(str(value).encode())

            elif(msg == "[2] RUN"):
                value = washer2.run()
                conn.sendall(str(value).encode())

            elif(msg == "[3] RUN"):
                value = washer3.run()
                conn.sendall(str(value).encode())
            
            elif(msg == "[1] DEPLOY"):
                washer1.deploy()
                conn.sendall("DONE".encode())

            elif(msg == "[2] DEPLOY"):
                washer2.deploy()
                conn.sendall("DONE".encode())

            elif(msg == "[3] DEPLOY"):
                washer3.deploy()
                conn.sendall("DONE".encode())

            elif(msg == "[1] INFO"):
                value = washer1.getInfo()
                conn.sendall(str(value).encode())

            elif(msg == "[2] INFO"):
                value = washer2.getInfo()
                conn.sendall(str(value).encode())

            elif(msg == "[3] INFO"):
                value = washer3.getInfo()
                conn.sendall(str(value).encode())

            elif(msg.find("[1] SEND") > -1):
                msg = msg.split(" ")
                washer1.receive(float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg.find("[2] SEND") > -1):
                msg = msg.split(" ")
                washer2.receive(float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg.find("[3] SEND") > -1):
                msg = msg.split(" ")
                washer3.receive(float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg == "END"):
                conn.sendall("OK".encode())
                conn.close()
                break

main()