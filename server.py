import socket

class Server:
    server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.connect(("8.8.8.8",80))
    ip=server.getsockname()[0]
    server.close()
    server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(('0.0.0.0',8989))
    hosts=['192.168.99.132','192.168.137.29']
    hosts.remove(ip)
    target=(hosts[0],8989)
    def send(self,data:str):
        self.server.sendto(data.encode(),self.target)
    def recv(self):
        data,ipport=self.server.recvfrom(10240).decode()
        return data.encode()