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
        ((width,height),leftTop)=screen
        return coordinate[0] > leftTop[0] and coordinate[0] < leftTop[0] + width \
               and coordinate[1] > leftTop[1] and coordinate[1] < leftTop[1] + height

    def __init__(self,selfAddr:tuple):
        self.selfAddr=selfAddr
        win=tkinter.Tk()
        self.screens={selfAddr:((win.winfo_screenwidth(),win.winfo_screenheight()),(0,0))}
        win.destroy()

    def addClient(self,target:tuple,screen:tuple):
        self.screens[target]=screen
        screenkeysSort = sorted(self.screens.keys())
        for screenKey, index in zip(screenkeysSort, range(len(self.screens))):
            if index>0:
                lastSc=self.screens[screenkeysSort[index-1]]
                # self.screens[screenKey].reLeftTop((lastSc.width+lastSc.leftTop[0],0))
                screen=self.screens[screenKey]
                self.screens[screenKey]=(screen[0],(lastSc[0][0]+lastSc[1][0],0))
    def update(self,screens:dict=None):
        if screens:
            self.screens=screens
        #以当前显示器左上角为原点重置所有显示器坐标
        if self.screens[self.selfAddr][1]!=(0,0):
            left,top=self.screens[self.selfAddr][1]
            for key,screen in self.screens.items():
                ((w,h),(l,t))=screen
                self.screens[key]=((w,h),(l-left,top-top))
    def coordinateIsInTarget(self,x:int,y:int):
        if not self.isInscreen(self.screens[self.selfAddr],(x,y)):
            for target,screen in self.screens.items():
                if self.isInscreen(screen,(x,y)):
                    ((_,_),(left,top))=screen
                    return target,(x-left,y-top)
        return None,None

    def setting(self):
        """
        打开gui设置窗口，可视化方式拖动各个窗口位置
        Returns:

        """
        pass


