import socket
import json
import queue
import threading

class EventServer:
    __MSG_SEP=bytes(bytearray([i+10 for i in 'event_server_msage_sep'.encode()]))
    __MSG_SEP=b"111111111111111111111111111111111111111111111111111111111"
    def __init__(self,port=20000):
        self.__port=port
        self.__client=None
        self.conrolled=True
        self.msageQueue=queue.Queue(100)
        threading.Thread(target=self.recvLoop).start()
    def getTcpPort(self):
        return self.__port

    def createClient(self,addr):
        self.__client=socket.socket()
        self.__client.connect(addr)
    def sendEvent(self, data: dict):
        self.__client.send(json.dumps(data).encode()+self.__MSG_SEP)

    def recvLoop(self):
        server = socket.socket()
        server.bind(("0.0.0.0", self.__port))
        server.listen(1)
        while True:
            tcp, addr = server.accept()
            tail=b''
            while True:
                recv = tcp.recv(1024)
                if not recv:
                    break
                messages = (recv+tail).split(self.__MSG_SEP)
                tail = messages[-1]
                for msg in messages[:-1]:
                    self.msageQueue.put(msg)




