import socket
import threading
import queue
import json

#定义基本的tcp和udp服务器

class AbsUdpServer:
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
    def close(self):
        self.__server.close()

class CommonUdpServer(AbsUdpServer):
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


class TcpServer:
    __MSG_SEP=bytes(bytearray([i+10 for i in 'event_server_msage_sep'.encode()]))

    def __init__(self,port=20000):
        self.__port=port
        self.__client=None
        self.conrolled=True
        self.msageQueue=queue.Queue(100)
        threading.Thread(target=self.recvLoop).start()
        self.activate=True
    def getTcpPort(self):
        return self.__port

    def createClient(self,addr):
        self.__client=socket.socket()
        try:
            self.__client.connect(addr)
        except:
            self.__client=None
    def sendEvent(self, data: dict):
        try:
            self.__client.send(json.dumps(data).encode()+self.__MSG_SEP)
        except ConnectionResetError as e:
            self.__client=None
            print("-----------------")
        except ConnectionAbortedError as e:
            self.__client=None
        except Exception as e:
            print(type(e))
            print(e)

    def recvLoop(self):
        server = socket.socket()
        server.bind(("0.0.0.0", self.__port))
        server.listen(1)
        while self.activate:
            tcp, addr = server.accept()
            tail=b''
            while True:
                recv = tcp.recv(1024)
                if not recv:
                    break
                messages = (tail+recv).split(self.__MSG_SEP)
                tail = messages[-1]
                for msg in messages[:-1]:
                    self.msageQueue.put(msg)
        server.close()
    def closeClient(self):
        if self.__client:
            self.__client.close()
            self.__client=None
    def connectedServer(self):
        return self.__client is not None

    def close(self):
        try:
            self.__client.close()
        except:
            pass
        self.activate=False




if __name__ == '__main__':
    i = 100
