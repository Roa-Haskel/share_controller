from server import CommonServer
import pynput
import time

con=CommonServer()

mouse = pynput.mouse.Controller()
while True:
    if con.clients:
        break
    time.sleep(1)
while True:
    xy=mouse.position
    con.sendMsage(xy,con.clients[0])
