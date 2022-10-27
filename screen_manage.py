import tkinter

class ScreenManage:
    @staticmethod
    def isInscreen(screen:tuple,coordinate):
        """
        Args:
            screen:((width,height),(top,left))
            coordinate: (x,y)
        Returns:
            给定坐标是否在屏幕中
        """
        # ((width,height),leftTop)=screen
        # return coordinate[0] > leftTop[0] and coordinate[0] < leftTop[0] + width \
        #        and coordinate[1] > leftTop[1] and coordinate[1] < leftTop[1] + height
        ((w,h),(l,t))=screen
        x,y=coordinate
        return x>=l and x<=l+w and y>=t and y<=t+h

    def __init__(self,selfAddr:tuple):
        self.selfAddr=str(selfAddr)
        win=tkinter.Tk()
        self.screens={self.selfAddr:((win.winfo_screenwidth(),win.winfo_screenheight()),(0,0))}
        win.destroy()
        self.screensWidget=None

    def addClient(self,target:tuple,screenSize:tuple):
        """
        根据客户端地址，屏幕尺寸添加客户端
        Args:
            target: 地址，ip和端口号
            screenSize: （x,y)

        Returns:

        """
        if str(target) in self.screens:
            return
        self.screens[str(target)]=(screenSize,(0,0))
        screenkeysSort = sorted(self.screens.keys())
        maxHeight=max([hegith for (target,((width,hegith),(left,top))) in self.screens.items()])
        for screenKey, index in zip(screenkeysSort, range(len(self.screens))):
            if index>0:
                lastSc=self.screens[screenkeysSort[index-1]]
                screen=self.screens[screenKey]
                self.screens[screenKey]=(screen[0],(lastSc[0][0]+lastSc[1][0],0))
        #下对齐
        for (target, ((width, hegith), (left, top))) in self.screens.items():
            self.screens[target]=((width,hegith),(left,maxHeight-hegith))
        self.update(None)
    def update(self,screens:dict=None):
        """
        根据输入的调整后的屏幕布局，更新当前屏幕管理状态
        Args:
            screens: {地址1:屏幕1，地址2：屏幕2}

        Returns:

        """
        if screens and len(screens)==len(self.screens):
            self.screens.update(screens)
        #以当前显示器左上角为原点重置所有显示器坐标
        if self.screens[self.selfAddr][1]!=(0,0):
            left,top=self.screens[self.selfAddr][1]
            for key,screen in self.screens.items():
                ((w,h),(l,t))=screen
                self.screens[key]=((w,h),(l-left,t-top))
    def coordinateIsInTarget(self,x:int,y:int):
        """
        判断给定坐标位于哪个客户端屏幕中
        Args:
            x: 坐标x
            y: 坐标y

        Returns:
            目标地址和目标坐标位置
            target,(x,y)
        """
        if not self.isInscreen(self.getScreen(),(x,y)):
            for target,screen in self.screens.items():
                if target!=self.selfAddr and self.isInscreen(screen,(x,y)):
                    ((_,_),(left,top))=screen
                    return eval(target),(x-left,y-top)
        return None,None
    def getScreenSize(self):
        return self.screens[self.selfAddr][0]
    def getScreen(self):
        return self.screens[self.selfAddr]
    def setting(self):
        """
        打开gui设置窗口，可视化方式拖动各个窗口位置
        Returns:

        """
        win=tkinter.Tk()
        win.geometry("640x480+100+100")

        screens=[(k,v) for k,v in self.screens.items()]
        minX=abs(min(min([i[1][0] for _,i in screens]),0))
        minY=abs(min(min([i[1][1] for _,i in screens]),0))


        def mousedown(event):
            widget = event.widget
            widget.startx = event.x  # 开始拖动时, 记录控件位置
            widget.starty = event.y

        def drag(event):
            widget = event.widget
            dx = event.x - widget.startx
            dy = event.y - widget.starty
            widget.place(x=widget.winfo_x() + dx,y=widget.winfo_y() + dy)

        self.screensWidget=dict()
        for index,(target,screen) in zip(range(len(screens)),screens):
            ((width,height),(left,top))=screen
            width,height=int(width/10),int(height/10)
            left,top=int((left+minX)/10),int((top+minY)/10)
            canvas=tkinter.Canvas(win,width=width,height=height,bg='red')
            canvas.place(x=left,y=top)
            canvas.bind("<Button-1>",mousedown)
            canvas.bind("<B1-Motion>",drag)
            canvas.bind("<ButtonRelease-1>",self.resetScrensAndUpdate)
            self.screensWidget[target]=canvas
        win.mainloop()
        self.screensWidget=None

    def resetScrensAndUpdate(self,event):
        if not self.screensWidget:
            return
        #TODO 还需要一个松开鼠标自动调整位置的功能

        newScreens = dict()
        for target,screen in self.screensWidget.items():
            info = screen.place_info()
            left, top = int(info['x']) * 10, int(info['y']) * 10
            (wh, topLeft) = self.screens[target]
            newScreens[target] = (wh, (left, top))
        self.update(newScreens)
    def getScreens(self):
        return {str(key):value for key,value in self.screens.items()}

if __name__ == '__main__':
    sc = ScreenManage(('1', 1999))
    sc.addClient(('2', 1999), (1280, 720))
    # sc.screens[('2',1999)]=((1280,720),(-300,-500))
    for i in range(10):
        sc.setting()
        print(sc.screens)
