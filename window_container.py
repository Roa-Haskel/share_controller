import tkinter as tk
from server import Server
import platform


class WindowContainer(Server):
    def __init__(self):
        self.windowID=1 if platform.platform().startswith("Windows") else 2

        if platform.platform().startswith("Windows"):
            self.windowID=1
            self.targetX,self.targetY=self.targetWidth,0
        else:
            self.windowID=2
            self.targetX,self.targetY=0,0

        win=tk.Tk()
        self.width,self.hight=win.winfo_screenwidth(),win.winfo_screenheight()
        win.destroy()
        self.send(str((self.width,self.hight)))
        self.targetWidth,self.targetHight = eval(self.recv())

        self.targetX,self.targetY=0,0

    def move(self,x,y):
        if(self.windowID==1):
            self.targetX+=x
            self.targetY=y-self.width -self.targetWidth
        else:
            self.targetX=x-self.width+self.targetX
            self.targetY=self.targetHight-self.hight+y

        if self.targetX<=self.targetWidth and self.targetY>=0 and self.targetY<=self.targetHight:
            return False,self.targetX,self.targetY
        else:
            return True,x,y


