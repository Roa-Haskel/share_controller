from server import CommonServer
import json
import pynput
import time
from common import RemoveCallbackSet,methodForLoop
from screen_manage import ScreenManage
import threading
import os
import socket
from event_server import EventServer


class ControlManageServer(CommonServer,ScreenManage,EventServer):
    BUTTONS = {"left": pynput.mouse.Button.left, "right": pynput.mouse.Button.right,
               "middle": pynput.mouse.Button.middle}
    class MsageType:
        #心跳事件
        HEART_TYPE_LOGO = -1111111
        #键盘事件
        KEYBOARD_EVENTS=442
        #鼠标事件
        MOUSE_EVENTS=2324
        #屏幕管理器更新事件
        SCREEN_UPDATE_EVENTS=211
        #注册屏幕信息事件
        ADD_SCREEN_EVENTS=4324
        #控制器状态变更事件，用于控制是否抑制当前输入，发送到其他屏幕
        CONTROL_STATUS_CHANGE=24234
    def __init__(self,port=19999,tcpPort=20000):
        CommonServer.__init__(self,port)
        ScreenManage.__init__(self,self.getLocalAddr())
        EventServer.__init__(self,tcpPort)
        self.__client=None
        self.mouse = pynput.mouse.Controller()
        self.dx,self.dy=self.mouse.position
        self.conrolled=True
        self.keyboard = pynput.keyboard.Controller()
        self.target = None
        self.clients=RemoveCallbackSet([],13,removeCallback=lambda x:None if str(x) not in self.screens or str(x)==self.selfAddr else self.screens.pop(str(x)))
        for method in [self._eventLoop, self._sendHeatBeat, self.scanLanLoop,self.mainLoop,self.controllerEventLoop]:
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
    def _eventLoop(self):
        msgType, msg, addr = self.getMsage()
        if msgType == self.MsageType.HEART_TYPE_LOGO:
            #如果没有给该客户端发送过屏幕信息，则发送一下
            if addr not in self.clients:
                self.sendMsage(self.getScreenSize(), addr, self.MsageType.ADD_SCREEN_EVENTS)
            self.clients.add(addr)

        elif msgType==self.MsageType.ADD_SCREEN_EVENTS:
            self.addClient(addr,eval(msg))
        elif msgType == self.MsageType.MOUSE_EVENTS:
            self.mouseEvent(**json.loads(msg))
        elif msgType == self.MsageType.SCREEN_UPDATE_EVENTS:
            data=json.loads(msg)
            self.update(data)
        elif msgType==self.MsageType.KEYBOARD_EVENTS:
            data=json.loads(msg)
            self.keyboardEvent(**data)
        elif msgType==self.MsageType.CONTROL_STATUS_CHANGE:
            self.conrolled=eval(msg)
        else:
            print("unknow msage type %s"%msgType)
    @methodForLoop(0)
    def controllerEventLoop(self):
        event=json.loads(self.msageQueue.get())
        if event['type'] in ['move','click','button','move_to','scroll']:
            self.mouseEvent(**event)
        elif event['type'] in ['release','press']:
            self.keyboardEvent(**event)
        else:
            print("error")
    def mouseEvent(self,**kwargs):
        if kwargs['type']=='move':
            self.mouse.move(**kwargs['params'])
        elif kwargs['type']=='click':
            button=kwargs['button']
            if kwargs['pressed']:
                self.mouse.press(self.BUTTONS[button])
            else:
                self.mouse.release(self.BUTTONS[button])
        elif kwargs['type']=='move_to':
            toX,toY=kwargs['params']['x'],kwargs['params']['y']
            dx,dy=toX-self.mouse.position[0],toY-self.mouse.position[1]
            self.mouse.move(dx,dy)

        elif kwargs['type']=='scroll':
            self.mouse.scroll(**kwargs['params'])

    def sendEvent(self,data:dict):
        self.__client.send(json.dumps(data).encode())
    def onMove(self,nx,ny):
        x,y=self.mouse.position
        data={'type':'move','params':{'dx':nx-x,'dy':ny-y}}
        # print(data)
        self.sendEvent(data)
        if self.conrolled or not self.clients:
            self.conrolled=True
            return False
    def onClick(self,x, y, button, pressed):
        data={'type':'click','button':str(button).split(".")[-1],'pressed':pressed}
        self.sendEvent(data)
    def onScroll(self,x,y,dx,dy):
        data={'type':'scroll','params':{'dx':dx*5,'dy':dy*5}}
        self.sendEvent(data)

    def keyboardEvent(self,**kwargs):
        try:
            key=pynput.keyboard.Key[kwargs['key']]
        except:
            key=kwargs['key']
        if kwargs['type']=='press':
            self.keyboard.press(key)
        else:
            self.keyboard.release(key)

    def onPress(self,key):
        try:
            name=key.name
        except:
            name=key.char
        data={'type':'press','key':name}
        self.sendEvent(data,self.MsageType.KEYBOARD_EVENTS)


    def onRelease(self,key):
        try:
            name=key.name
        except:
            name=key.char
        data={'type':"release",'key':name}
        self.sendEvent(data,self.MsageType.KEYBOARD_EVENTS)


    def broadcastEvent(self,data,msgType:int):
        for target in self.clients:
            self.sendMsage(json.dumps(data),target,msgType)
    def broadcastScreens(self):
        self.broadcastEvent(self.getScreens(),self.MsageType.SCREEN_UPDATE_EVENTS)
    def setTarget(self,target):
        self.target=target
    def setting(self):
        super().setting()
        self.broadcastScreens()
    @methodForLoop(0)
    def mainLoop(self):
        while not self.clients:
            time.sleep(3)
        with pynput.mouse.Events() as events:
            for event in events:
                if isinstance(event,pynput.mouse.Events.Move):
                    x,y=event.x,event.y
                    target,xy=self.coordinateIsInTarget(x,y)
                    self.target=target
                    if target:
                        self.conrolled=False
                        self.sendMsage(True,self.target,self.MsageType.CONTROL_STATUS_CHANGE)
                        self.__client=socket.socket()
                        self.__client.connect((target[0],self.getTcpPort()))
                        self.sendEvent({"type":"move_to","params":{"x":xy[0],'y':xy[1]}})
                        break
        if not self.conrolled:
            mouseListen=pynput.mouse.Listener(
                    suppress=True,
                    on_move=self.onMove,
                    on_click=self.onClick,
                    on_scroll=self.onScroll)
            keyboardListen=pynput.keyboard.Listener(
                suppress=True,
                on_press=self.onPress,
                on_release=self.onRelease
            )
            mouseListen.start()
            keyboardListen.start()
            mouseListen.join()
            self.__client.close()
            keyboardListen.stop()
    def close(self):
        super().close()
        os._exit(0)



if __name__ == '__main__':
    con=ControlManageServer()
    con.mainLoop()

