import socket

class Decanter:
    def __init__(self):
        self.glycerin = 0.0
        self.solution = 0.0
        self.etOH = 0.0
        self.total = 0.0
        self.time = 0.0
        self.cooldown = 0.0
        self.status = "NONE"
        self.deployiedGlycerin = 0.0
        self.deployiedSolution = 0.0
        self.deployiedEtOH = 0.0
        return

    def getInfo(self):
        return self.etOH, self.solution, self.glycerin, self.total, self.status

    def deploy(self):
        self.status = "DEPLOYING"
        return

    def rest(self):
        self.status = "REST"
        return

    def receive(self, value):
        if (self.total + value <= 10.0 and value != 0.0):
            self.total += value
            self.total = round(self.total, 3)
            self.cooldown += round(( (value * 5.0) / 3.0 ), 2)
            self.cooldown = round(self.cooldown, 2)
            self.status = "RECEIVING"
        return

    def run(self):
        self.time += 0.01

        self.time = round(self.time, 2)
        
        if (self.status == "REST"):
            self.cooldown -= 0.01

            self.cooldown = round(self.cooldown, 3)

            if(self.cooldown == 0):
                self.glycerin = self.total*0.03
                self.solution = self.total*0.88
                self.etOH = self.total*0.09

                self.glycerin = round(self.glycerin, 3)
                self.solution = round(self.solution, 3)
                self.etOH = round(self.etOH, 3)

                self.status = "NONE"

            return 0.0, 0.0, 0.0

        elif (self.status == "DEPLOYING"):
            if (self.glycerin - 0.015 <= 0):
                deployGlycerin = self.glycerin
                self.glycerin = 0.0

            else:
                deployGlycerin = 0.015
                self.glycerin -= 0.015
                self.glycerin = round(self.glycerin, 3)

            if (self.solution - 0.015 <= 0):
                deploySolution = self.solution
                self.solution = 0.0

            else:
                deploySolution = 0.015
                self.solution -= 0.015
                self.solution = round(self.solution, 3)

            if (self.etOH - 0.015 <= 0):
                deployEtOH = self.etOH
                self.etOH = 0.0

            else:
                deployEtOH = 0.015
                self.etOH -= 0.015
                self.etOH = round(self.etOH, 3)

            self.total -= deployEtOH + deploySolution + deployGlycerin
            self.total = round(self.total, 3)

            if (self.glycerin == 0.0 and self.solution == 0.0 and self.etOH == 0.0):
                self.status = "NONE"

            return deployEtOH, deploySolution, deployGlycerin
            
        else:
            self.status = "NONE"
            return 0.0, 0.0, 0.0

def main():
    decanter = Decanter()

    host = 'localhost'
    port = 50005
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
                value = list(decanter.run())

                for i in range(0, len(value)):
                    value[i] = str(value[i])

                conn.sendall(str(";".join(value)).encode())

            elif(msg == "DEPLOY"):
                decanter.deploy()
                conn.sendall("DONE".encode())

            elif(msg == "REST"):
                decanter.rest()
                conn.sendall("DONE".encode())

            elif(msg == "INFO"):
                value = list(decanter.getInfo())

                for i in range(0, len(value)):
                    value[i] = str(value[i])

                conn.sendall(str(";".join(value)).encode())

            elif(msg.find("SEND") > -1):
                msg = msg.split(" ")
                decanter.receive(float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg == "END"):
                conn.sendall("OK".encode())
                conn.close()
                break

main()