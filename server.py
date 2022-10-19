import socket
import threading

class AbsServer:
    def __init__(self,port=19999):
        self._port=port
        self.__server=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__localAddr=None
        self.__server.bind(('0.0.0.0',self._port))
    def getLocalAddr(self):
        if not self.__localAddr:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.connect(("8.8.8.8", 80))
            addr = server.getsockname()
            self.__localAddr=addr[0],self._port
            server.close()
        return self.__localAddr
    def sendTo(self,data:bytes,target:tuple):
        self.__server.sendto(data,target)
    def recvfrom(self):
        return self.__server.recvfrom(1024)

class CommonServer(AbsServer):
    MSAGE_SEP=bytes(bytearray([i+10 for i in 'common_server_msage_sep'.encode()]))
    def __init__(self,port):
        super().__init__(port)
        self.__lock=threading.Lock()
    def recvfrom(self):
        while True:
            data,addr=super().recvfrom()
            if self.MSAGE_SEP in data:
                return data,addr

    def getMsage(self):
        dataTuple=self.recvfrom()
        msageType, message,addr = dataTuple[0].split(self.MSAGE_SEP)
        msageType = int(msageType)
        return msageType, message, eval(addr)


    def sendMsage(self,data:str,target:tuple,msgType:int=0):
        assert isinstance(msgType,int)
        if not isinstance(data,bytes):
            data=str(data).encode()
        data=str(msgType).encode()+self.MSAGE_SEP+data+self.MSAGE_SEP+str(self.getLocalAddr()).encode()
        super().sendTo(data,target)





if __name__ == '__main__':
    i = 100
