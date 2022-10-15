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
        if not isinstance(data,bytes):
            data=str(data).encode()
        self.__server.sendto(data,self.target)
    def recvfrom(self):
        return self.__server.recvfrom(1024)


class CommonServer(AbsServer):
    MSAGE_SEP=bytes(bytearray([i+10 for i in 'common_server_msage_sep'.encode()]))

    @classmethod
    class msageList:
        def __init__(self):
            self.msageContainer = []

        def putMsage(self,dataTuple:tuple):

            dataTuple(0).split()
            self.msageContainer.append(dataTuple)

    def __init__(self):
        self.msageContainer=[]



    def msageParaser(self,dataTuple:tuple):
        msageType, message = dataTuple[0].split(self.MSAGE_SEP)
        msageType = int(msageType)
        return msageType,message,dataTuple[1]

    def getMsage(self,inputMsageType:int):
        for index in range(len(self.msageContainer)):
            msgType,msage,addr=self.msageContainer[index]
            if msgType==inputMsageType:
                del self.msageContainer[index]
                return msage,addr

        while True:
            msgType,msage,addr=self.msageParaser(self.recvfrom())
            if msgType==inputMsageType:
                return msage,addr
            self.msageContainer.append((msgType,msage,addr))

    def sendMsage(self,msgType:int,data:str):
        data=str(msgType).encode()+self.MSAGE_SEP+data
        super().sendTo(data)


