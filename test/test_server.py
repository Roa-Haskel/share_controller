from server import CommonServer
import pynput
import time

con=CommonServer()

mouse = pynput.mouse.Controller()
while True:
    if con.clients:
        break
    time.sleep(1)
x,y=mouse.position
with pynput.mouse.Events() as events:
    # print(con.clients,111111111111111111111)
    for event in events:
        con.sendMsage((event.x-x,event.y-y),list(con.clients)[0],2)
        x,y=event.x,event.y
