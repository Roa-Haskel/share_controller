from pynput.keyboard import Key,KeyCode
import pynput
import sys
import time

class KeyEventFactory:
    keyChars="""
1!
2@
3#
4$
5%
6^
7&
8*
9(
0)
-_
=+
[{
]}
\|
/?
,<
.>
""".strip().split("\n")

    keyNames="""
cmd:alt
alt_l:cmd
""".strip().split("\n")
    keyNames={i.split(":")[0]:i.split(":")[1] for i in keyNames}

    keyChars={i[0]:i[1] for i in keyChars}
    def __init__(self):
        self.shiftRelease=True
    def input(self,key):
        if 'name' in dir(key):
            if 'shift' in key.name:
                self.shiftRelease=not self.shiftRelease
            data=("name",self.keyNames.get(key.name,key.name))
        elif 'char' in dir(key) and key.char is not None:
            keyChar=key.char
            if not self.shiftRelease:
                keyChar=self.keyChars.get(keyChar,keyChar)
            data=("char",keyChar)
        else:
            data=("vk",key.vk)
        return data
    def outPut(self,data):
        tp,dt=data
        if tp=="name":
            key=Key[dt]
        elif tp=='char':
            key=dt
        elif tp=='vk':
            key=KeyCode.from_vk(dt)
        else:
            raise TypeError(str(data))
        return key

class MouseEventFactory:
    def __init__(self):
        self.mouse=pynput.mouse.Controller()
        self.lastPressTime=0
    def mouseEventExec(self,**kwargs):
        if kwargs['type']=='move':
            if sys.platform=='darwin':
                mx,my=kwargs['params']['dx'],kwargs['params']['dy']
                fx,fy=self.correctMove(self.mouse.position,(mx,my),self.getScreenSize())
                self.mouse.move(fx,fy)
            else:
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
    def onMove(self,nx,ny):
        x,y=self.mouse.position
        data={'type':'move','params':{'dx':nx-x,'dy':ny-y}}
        # print(data)
        self.sendEvent(data)
        if self.conrolled or not self.clients:
            self.conrolled=True
            return False
    def onClick(self,x, y, button, pressed):
        button=str(button).split(".")[-1]
        data={'type':'click','button':str(button).split(".")[-1],'pressed':pressed}
        if not pressed:
            if not self.lastPressTime:
                self.lastPressTime=time.time()
            else:
                if self.lastPressTime-time.time()<1:
                    data={'type':'double_click','button':button}
                self.lastPressTime=0


        self.sendEvent(data)
    def onScroll(self,x,y,dx,dy):
        data={'type':'scroll','params':{'dx':dx*5,'dy':dy*5}}
        self.sendEvent(data)