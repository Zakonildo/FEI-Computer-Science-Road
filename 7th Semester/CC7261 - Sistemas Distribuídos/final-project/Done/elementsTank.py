import socket

class ElementsTank:
    def __init__(self):
        self.naOH = 0.0
        self.etOH = 0.0
        self.time = 0.0
        self.status = "NONE"
        self.naOH_Deployied = 0.0
        self.etOH_Deployied = 0.0
        return

    def getInfo(self):
        return self.naOH, self.etOH

    def receiveEtOH(self, value):
        self.etOH += value
        self.etOH = round(self.etOH, 3)
        return

    def deployEtOH(self):
        self.status = "DEPLOYING EtOH"
        return

    def deployNaOH(self):
        self.status = "DEPLOYING NaOH"
        return

    def deployBoth(self):
        self.status = "DEPLOYING BOTH"
        return

    def run(self):
        self.time += 0.01

        self.time = round(self.time, 2)
        
        if ( self.time % 1.0 == 0 ):
            self.naOH += 0.250
            self.naOH = round(self.naOH, 3)

            self.etOH += 0.125
            self.etOH = round(self.etOH, 3)

        if(self.status == "DEPLOYING BOTH"):
            if ( self.naOH == 0.0 ):
                self.status = "DEPLOYING EtOH"

            elif ( self.etOH == 0.0 ):
                self.status = "DEPLOYING NaOH"

            else:

                if (self.naOH < 0.005):
                    self.naOH_Deployied = 0.0
                    
                else:
                    self.naOH -= 0.005
                    self.naOH_Deployied = 0.005

                if (self.etOH < 0.005):
                    self.etOH_Deployied = 0.0

                else:
                    self.etOH -= 0.005
                    self.etOH_Deployied = 0.005
                
                self.naOH = round(self.naOH, 3)
                self.etOH = round(self.etOH, 3)
                self.naOH_Deployied = round(self.naOH_Deployied, 3)
                self.etOH_Deployied = round(self.etOH_Deployied, 3)

                self.status = "NONE"

                return self.naOH_Deployied, self.etOH_Deployied
        


        if ( self.status == "DEPLOYING EtOH" ):
            if( self.etOH < 0.005 ):
                self.etOH_Deployied = 0.0

            elif( self.etOH < 0.010 and self.etOH >= 0.005):
                self.etOH_Deployied = 0.005
                self.etOH -= 0.005

            else:
                self.etOH_Deployied = 0.010
                self.etOH -= 0.010

            self.etOH = round(self.etOH, 3)
            self.etOH_Deployied = round(self.etOH_Deployied, 3)

            self.naOH_Deployied = 0.0

            self.status = "NONE"

            return self.naOH_Deployied, self.etOH_Deployied
        


        elif ( self.status == "DEPLOYING NaOH" ):
            if( round(self.naOH - 0.010, 3) <= 0):
                self.naOH_Deployied = self.naOH
                self.naOH = 0

            else:
                self.naOH_Deployied = 0.010
                self.naOH -= 0.010

            self.naOH = round(self.naOH, 3)
            self.naOH_Deployied = round(self.naOH_Deployied, 3)

            self.etOH_Deployied = 0.0
            
            self.status = "NONE"

            return self.naOH_Deployied, self.etOH_Deployied

        else:
            self.naOH_Deployied = 0.0
            self.etOH_Deployied = 0.0

            return self.naOH_Deployied, self.etOH_Deployied

def main():
    elementsTank = ElementsTank()

    host = 'localhost'
    port = 50001
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
                value = list(elementsTank.run())

                for i in range(0, len(value)):
                    value[i] = str(value[i])

                conn.sendall(str(";".join(value)).encode())

            elif(msg == "DEPLOY BOTH"):
                elementsTank.deployBoth()
                conn.sendall("DONE".encode())

            elif(msg == "DEPLOY EtOH"):
                elementsTank.deployEtOH()
                conn.sendall("DONE".encode())

            elif(msg == "DEPLOY NaOH"):
                elementsTank.deployNaOH()
                conn.sendall("DONE".encode())

            elif(msg == "INFO"):
                value = list(elementsTank.getInfo())

                for i in range(0, len(value)):
                    value[i] = str(value[i])

                conn.sendall(str(";".join(value)).encode())

            elif(msg.find("SEND") > -1):
                msg = msg.split(" ")
                elementsTank.receiveEtOH(float(msg[-1]))
                conn.sendall("DONE".encode())

            elif(msg == "END"):
                conn.sendall("OK".encode())
                conn.close()
                break

main()