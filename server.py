import socket

class AbsServer:
    PORT=8989
    __server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    __server.bind(('0.0.0.0', PORT))
    @staticmethod
    def getLocalIp():
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.connect(("8.8.8.8", 80))
        ip = server.getsockname()[0]
        server.close()
        return ip
    @classmethod
    def scanWlan(self):
        #TODO 扫描局域网内某个端口处于开放状态的所有ip，用于客户端链接，返回值为[('192.168.0.2',8989),('192.168.0.3',8989)]
        hosts = ['192.168.99.132', '192.168.137.29']
        hosts.remove(self.getLocalIp())
        return [(i,self.PORT) for i in hosts]
    def __init__(self):
        self.target=('0.0.0.0',self.PORT)

    def sendTo(self,data:str):
        self.__server.sendto(data,self.target)
    def recv(self,black:bool=True):
        if not black:
            try:
                return self.__server.recvfrom(1024,0x40)
            except:
                return '',''
        else:
            return self.__server.recvfrom(1024)