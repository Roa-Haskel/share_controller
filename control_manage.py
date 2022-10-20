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
        #控制器状态变更事件
        CONTROL_STATUS_CHANGE=24234
    def __init__(self,port=19999):
        super().__init__(port)
        self.mouse = pynput.mouse.Controller()
        self.dx,self.dy=self.mouse.position

        self.conrolled=True
        self.keyboard = pynput.keyboard.Controller()
        self.target = None
        self.clients=RemoveCallbackSet([],13)
        for method in [self._eventMainLoop, self._sendHeatBeat, self.scanLanLoop]:
            threading.Thread(target=method).start()

    def scanLanLoop(self):
        ip=self.getLocalAddr()[0]
        splitIp = ip.split(".")
        topThree = '.'.join(splitIp[:-1])
        allIps = [topThree + "." + str(i) for i in range(1, 255) if str(i) != splitIp[-1]]
        index=0
        while True:
            if index%30!=0:
                continue
            # self.sendHeartToAllTargets(allIps)
            while not self.clients:
                self.sendHeartToAllTargets(allIps)
                time.sleep(3)
            time.sleep(1)
    def sendHeartToAllTargets(self,ips:list):
        for i in ips:
            try:
                self.sendMsage('', (i, self._port), self.MsageType.HEART_TYPE_LOGO)
            except Exception as e:
                pass

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
            self.mouseEvent(**json.loads(msg))
        elif msgType == self.MsageType.SCREEN_MANAGER_EVENTS:
            print("screen manage set------")
            pass
        elif msgType==self.MsageType.KEYBOARD_EVENTS:
            print("keyboard event")
            pass
        elif msgType==self.MsageType.CONTROL_STATUS_CHANGE:
            self.conrolled=eval(msg)
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

    def sendEvent(self,data:dict,eventType:int):
        self.sendMsage(json.dumps(data),self.target,eventType)
    def onMove(self,x,y):
        nx,ny=x-self.dx,y-self.dy
        self.dx,self.dy=x,y
        data={'type':'move','params':{'dx':nx,'dy':ny}}
        self.sendEvent(data,self.MsageType.MOUSE_EVENTS)
        if self.conrolled:
            return False
    def onClick(self,x, y, button, pressed):
        data={'type':'click','button':str(button).split(".")[-1],'pressed':pressed}
        self.sendEvent(data,self.MsageType.MOUSE_EVENTS)
    def onScroll(self,x,y,dx,dy):
        data={'type':'scroll','params':{'dx':dx*5,'dy':dy*5}}
        self.sendEvent(data,self.MsageType.MOUSE_EVENTS)

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
                        self.conrolled=False
                        self.sendMsage(True,self.target,self.MsageType.CONTROL_STATUS_CHANGE)
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

