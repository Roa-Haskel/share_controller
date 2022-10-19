from server import CommonServer
import json
import pynput
import time
from common import RemoveCallbackSet,methodForLoop
import threading

class ControlManageServer(CommonServer):
    BUTTONS = {"left": pynput.mouse.Button.left, "right": pynput.mouse.Button.right,
               "middle": pynput.mouse.Button.middle}
    class MsageType:
        #心跳事件
        HEART_TYPE_LOGO = -1111111
        #键盘事件
        KEYBOARD_EVENTS=442
        #鼠标事件
        MOUSE_EVENTS=2324
        #屏幕管理器事件
        SCREEN_MANAGER_EVENTS=211
    def __init__(self,port=19999):
        super().__init__(port)
        self.mouse = pynput.mouse.Controller()
        self.keyboard = pynput.keyboard.Controller()
        self.target = None
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
        elif msgType == self.MsageType.MOUSE_EVENTS:
            self.mouseEvent(json.loads(msg))
        elif msgType == self.MsageType.SCREEN_MANAGER_EVENTS:
            print("screen manage set------")
            pass
        elif msgType==self.MsageType.KEYBOARD_EVENTS:
            print("keyboard event")
            pass
        else:
            print("unknow msage type %s"%msgType)


    def mouseEvent(self,**kwargs):
        if kwargs['type']=='move':
            self.mouse.move(**kwargs['params'])
        elif kwargs['type']=='click':
            button=kwargs['button']
            if kwargs['pressed']:
                self.mouse.press(self.BUTTONS[button])
            else:
                self.mouse.release(self.BUTTONS[button])
        elif kwargs['type']=='scroll':
            self.mouse.scroll(**kwargs['params'])

    def sendEvent(self,data:dict):
        self.sendMsage(json.dumps(data),self.target,self.MsageType.MOUSE_EVENTS)
    def onMove(self,x,y):
        data={'type':'move','params':{'x':x,'y':y}}
        self.sendMsage(data)
    def onClick(self,x, y, button, pressed):
        data={'type':'click','button':str(button).split(".")[-1],'pressed':pressed}
        self.sendMsage(data)
    def onScroll(self,x,y,dx,dy):
        data={'type':'scroll','params':{'dx':dx,'dy':dy}}
        self.sendMsage(data)

    def keyboardEvent(self,**kwargs):
        if kwargs['type']=='press':
            self.keyboard.press(kwargs['key'])
        else:
            self.keyboard.release(kwargs['key'])

    def onPress(self,key):
        data={'type':'press','key':key}
        self.sendMsage(data,self.target,self.MsageType.MOUSE_EVENTS)

    def onRelease(self,key):
        data={'type':"release",'key':key}
        self.sendMsage(data,self.target,self.MsageType.KEYBOARD_EVENTS)

    def setTarget(self,target):
        self.target=target

    def mainLoop(self):
        with pynput.mouse.Events() as events:
            for event in events:
                if isinstance(event,pynput.mouse.Events.Move):
                    if event.x<0:
                        break
        print('--------------------------')
        with pynput.mouse.Listener(
                # suppress=True,
                on_move=self.onMove,
                on_click=self.onClick,
                on_scroll=self.onScroll) as listener:
            listener.join()


if __name__ == '__main__':
    con=ControlManageServer()
    con.mainLoop()

