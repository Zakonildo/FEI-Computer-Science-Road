import socket

class Dryer:
    def __init__(self):
        self.total = 0.0
        self.totalNotDryied = 0.0
        self.time = 0.0
        self.cooldown = 0.0
        self.status = "NONE"
        self.deployied = 0.0
        return

    def getInfo(self):
        return self.totalNotDryied, self.status

    def receive(self, value):
        if (value != 0.0):
            self.totalNotDryied += value*0.975
            self.totalNotDryied = round(self.totalNotDryied, 6)
            self.status = "RECEIVING"
        return

    def run(self):
        #time.sleep(0.01)
        self.time += 0.01

        self.time = round(self.time, 2)

        if(self.totalNotDryied != 0.0):
            if(self.totalNotDryied - 0.002 <= 0):
                self.total += self.totalNotDryied
                self.totalNotDryied = 0.0

            else:
                self.total += 0.002
                self.totalNotDryied -= 0.002

            if (self.total - 0.015 <= 0):
                self.deployied = self.total
                self.total = 0.0

            else:
                self.deployied = 0.015
                self.total -= 0.015
            
            self.total = round(self.total, 6)
            self.deployied = round(self.deployied, 6)
            self.totalNotDryied = round(self.totalNotDryied, 6)

            return self.deployied

        else:
            return 0.0

def main():
    dryer = Dryer()

    host = 'localhost'
    port = 50007
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
                value = dryer.run()
                conn.sendall(str(value).encode())

            elif(msg == "INFO"):
                value = list(dryer.getInfo())

                for i in range(0, len(value)):
                    value[i] = str(value[i])

                conn.sendall(str(";".join(value)).encode())

            elif(msg.find("SEND") > -1):
                msg = msg.split(" ")
                dryer.receive(float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg == "END"):
                conn.sendall("OK".encode())
                conn.close()
                break

main()