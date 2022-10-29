from server import CommonUdpServer
import pynput

con=CommonUdpServer()

mouse = pynput.mouse.Controller()

while True:
    msg,addr = con.getMsage(2)
    xy=(int[i] for i in eval(msg))
    mouse.move(*xy)

