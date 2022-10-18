import socket
import requests
import urllib
from common import RemoveCallbackSet
import time
import threading


class AbsServer:

    PORT=19999
    remoteServerBaseUrl="http://120.48.68.8"
    # remoteServerBaseUrl="http://127.0.0.1"

    __localAddr=None
    @classmethod
    def getLocalAddr(cls):
        if not cls.__localAddr:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.connect(("8.8.8.8", 80))
            addr = server.getsockname()
            cls.__localAddr=addr[0],cls.PORT
            server.close()
        return cls.__localAddr
    def __init__(self):
        self.__server=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server.bind(self.getLocalAddr())
    def register(self):
        url=urllib.parse.urljoin(self.remoteServerBaseUrl,'register/'+str(self.getLocalAddr()))
        try:
            htm=requests.get(url)
            htm.raise_for_status()
        except:
            return False
        return not htm.text
    def deleteFromRemote(self,lanAddr:tuple):
        url=urllib.parse.urljoin(self.remoteServerBaseUrl,'register/'+str(lanAddr))
        htm=requests.get(url)
        return not htm.text
    def logout(self):
        self.deleteFromRemote(self.getLocalAddr())
    def sendTo(self,data:bytes,target:tuple):
        self.__server.sendto(data,target)
    def recvfrom(self):
        return self.__server.recvfrom(1024)

class CommonServer(AbsServer):
    MSAGE_SEP=bytes(bytearray([i+10 for i in 'common_server_msage_sep'.encode()]))
    HEART_TYPE_LOGO=-1111111
    def __init__(self):
        super().__init__()
        self.register()
        self.msageContainer=[]
        self.clients=RemoveCallbackSet([])
        threading.Thread(target=self.updateClients).start()
        threading.Thread(target=self.sendHeartbeat).start()
        threading.Thread(target=self.registerLoop).start()
    def registerLoop(self):
        while True:
            if self.register():
                time.sleep(16)
    def updateClients(self):
        index=0
        while True:
            if index%10==0:
                self.getClientsFromRemote()
            self.chickHeartbeat()
            time.sleep(1)
            index+=1
    def getClientsFromRemote(self):
        url=urllib.parse.urljoin(self.remoteServerBaseUrl,'clients')
        htm=requests.get(url)
        localAddr=self.getLocalAddr()
        clients=[i for i in eval(htm.text) if i[0]!=localAddr[0]]
        self.clients.update(clients)

    def chickHeartbeat(self):
        _,addr = self.getMsage(self.HEART_TYPE_LOGO)
        self.clients.add(addr)

    def sendHeartbeat(self):
        while True:
            for i in self.clients:
                self.sendMsage('',i,self.HEART_TYPE_LOGO)
            time.sleep(1)

    def msageParaser(self,dataTuple:tuple):
        msageType, message = dataTuple[0].split(self.MSAGE_SEP)
        msageType = int(msageType)
        return msageType,message,dataTuple[1]

    def getMsage(self,inputMsageType:int)->tuple:
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

    def sendMsage(self,data:str,target:tuple,msgType:int=0):
        if not isinstance(data,bytes):
            data=str(data).encode()
        data=str(msgType).encode()+self.MSAGE_SEP+data
        super().sendTo(data,target)

if __name__ == '__main__':
    i = 100
