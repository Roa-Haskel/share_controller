import socket
import threading

from common import RemoveCallbackSet,methodForLoop

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
    HEART_TYPE_LOGO=-1111111
    def __init__(self,port):
        super().__init__(port)
        self.__msageContainer=[]
    def recvfrom(self):
        while True:
            data,addr=super().recvfrom()
            if self.MSAGE_SEP in data:
                return data,addr



    def msageParaser(self,dataTuple:tuple):
        msageType, message = dataTuple[0].split(self.MSAGE_SEP)
        msageType = int(msageType)
        return msageType,message,dataTuple[1]

    def getMsage(self,inputMsageType:int)->tuple:
        for index in range(len(self.__msageContainer)):
            msgType,msage,addr=self.__msageContainer[index]
            if msgType==inputMsageType:
                del self.__msageContainer[index]
                return msage,addr

        while True:
            msgType,msage,addr=self.msageParaser(self.recvfrom())
            if msgType==inputMsageType:
                return msage,addr
            self.__msageContainer.append((msgType, msage, addr))

    def sendMsage(self,data:str,target:tuple,msgType:int=0):
        assert isinstance(msgType,int)
        if not isinstance(data,bytes):
            data=str(data).encode()
        data=str(msgType).encode()+self.MSAGE_SEP+data
        super().sendTo(data,target)

class ManageServer(CommonServer):

    def __init__(self,port=19999):
        super().__init__(port)
        self.clients=RemoveCallbackSet([],13)
        for method in [self._chickHeatBeat,self._sendHeatBeat,self._sendToAllLan]:
            threading.Thread(target=method).start()

    @methodForLoop(50,10)
    def _sendToAllLan(self):
        ip=self.getLocalAddr()[0]
        while not self.clients:
            splitIp = ip.split(".")
            topThree='.'.join(splitIp[:-1])
            allIps=[topThree+"."+str(i) for i in range(1,255) if str(i)!=splitIp[-1]]
            for i in allIps:
                try:
                    self.sendMsage('', (i,self._port), self.HEART_TYPE_LOGO)
                except:
                    print('send to %s error'%(str((ip,self._port))))
    @methodForLoop(0)
    def _chickHeatBeat(self):
        _, addr = self.getMsage(self.HEART_TYPE_LOGO)
        self.clients.add(addr)
    @methodForLoop(8,3)
    def _sendHeatBeat(self):
        for i in self.clients:
            self.sendMsage('',i,self.HEART_TYPE_LOGO)
class ControllerServer(CommonServer):
    pass



if __name__ == '__main__':
    i = 100
