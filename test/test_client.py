from server import CommonServer
import pynput

con=CommonServer()

mouse = pynput.mouse.Controller()

while True:
    msg,addr = con.getMsage(2)
    xy=(int[i] for i in eval(msg))
    mouse.move(*xy)

