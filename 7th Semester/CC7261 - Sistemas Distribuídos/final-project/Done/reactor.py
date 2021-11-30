import socket

class Reactor:
    def __init__(self):
        self.oil = 0.0
        self.naOH = 0.0
        self.etOH = 0.0
        self.processed = 0.0
        self.time = 0.0
        self.cooldown = 0.0
        self.status = "NONE"
        self.deployied = 0.0
        self.cycles = 0
        return

    def getInfo(self):
        return self.oil, self.naOH, self.etOH, self.processed, self.status, self.cycles

    def deploy(self):
        self.status = "DEPLOYING"
        return
    
    def process(self):
        self.status = "PROCESSING"
        return

    def receive(self, item, value):
        if (self.processed == 0.0):
            if ( item == "Oil" and self.oil + value <= 1.25 ):
                self.oil += value
                self.oil = round(self.oil, 3)

            elif ( item == "NaOH" and self.naOH + value <= 1.25 ):
                self.naOH += value
                self.naOH = round(self.naOH, 3)

            elif ( item == "EtOH" and self.etOH + value <= 2.5 ):
                self.etOH += value
                self.etOH = round(self.etOH, 3)

        return

    def run(self):
        #time.sleep(0.01)
        self.time += 0.01

        self.time = round(self.time, 2)
        
        if ( self.oil + self.naOH + self.etOH == 5.0 ):
            self.process()

        elif ( self.processed == 5.0 ):
            self.deploy()

        if ( self.status == "PROCESSING" ):
            self.processed += 0.05
            self.oil -= 0.0125
            self.naOH -= 0.0125
            self.etOH -= 0.0250

            self.processed = round(self.processed, 2)
            self.oil = round(self.oil, 4)
            self.naOH = round(self.naOH, 4)
            self.etOH = round(self.etOH, 4)

            if(self.processed == 5.0):
                self.status = "NONE"
                self.cycles += 1

            self.deployied = 0.0
            return self.deployied

        elif ( self.status == "DEPLOYING" ):

            if (round(self.processed - 0.06, 3) <= 0):
                self.deployied = self.processed
                self.processed = 0.0
            
            else:
                self.processed -= 0.06
                self.deployied = 0.06

            self.deployied = round(self.deployied, 2)
            self.processed = round(self.processed, 2)

            self.status = "NONE"

            return self.deployied

        else:
            self.deployied = 0.0
            return self.deployied

def main():
    reactor = Reactor()

    host = 'localhost'
    port = 50004
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
                value = reactor.run()
                conn.sendall(str(value).encode())

            elif(msg == "DEPLOY"):
                reactor.deploy()
                conn.sendall("DONE".encode())

            elif(msg == "PROCESS"):
                reactor.process()
                conn.sendall("DONE".encode())

            elif(msg == "INFO"):
                value = list(reactor.getInfo())

                for i in range(0, len(value)):
                    value[i] = str(value[i])

                conn.sendall(str(";".join(value)).encode())

            elif(msg.find("SEND") > -1):
                msg = msg.split(" ")
                reactor.receive(msg[-2], float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg == "END"):
                conn.sendall("OK".encode())
                conn.close()
                break

main()