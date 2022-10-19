import socket
import threading
import time
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

class ManageServer(CommonServer):

    class MsageType:
        #心跳事件
        HEART_TYPE_LOGO = -1111111
        #控制器事件
        CONTROLLER_EVENTS=1
        #屏幕管理器事件
        SCREEN_MANAGER_EVENTS=2
    def __init__(self,port=19999):
        super().__init__(port)
        self.clients=RemoveCallbackSet([],13)
        for method in [self._eventMainLoop, self._sendHeatBeat, self._sendToAllLan]:
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
                    self.sendMsage('', (i,self._port), self.MsageType.HEART_TYPE_LOGO)
                except Exception as e:
                    print(e)
                    print('send to %s error'%(str((i,self._port))))
                    pass
            time.sleep(1)
    @methodForLoop(8,3)
    def _sendHeatBeat(self):
        for i in self.clients:
            try:
                self.sendMsage('',i,self.MsageType.HEART_TYPE_LOGO)
            except:
                pass
    @methodForLoop(0)
    def _eventMainLoop(self):
        msgType, msg, addr = self.getMsage()
        if msgType == self.MsageType.HEART_TYPE_LOGO:
            self.clients.add(addr)
        elif msgType == self.MsageType.CONTROLLER_EVENTS:
            pass
        elif msgType == self.MsageType.SCREEN_MANAGER_EVENTS:
            pass
        else:
            print("unknow msage type %s"%msgType)

class ControllerServer(CommonServer):
    pass



if __name__ == '__main__':
    i = 100
