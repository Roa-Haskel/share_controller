
class Screen:
    def __init__(self,width:int,height:int,leftTop:tuple):
        self.width=width
        self.height=height
        self.leftTop=leftTop
    def isInscreen(self,coordinate:tuple):
        return coordinate[0]>self.leftTop[0] and coordinate[0]<self.leftTop[0]+self.width \
            and coordinate[1]>self.leftTop[1] and coordinate[1]<self.leftTop[1]+self.height
    def reLeftTop(self,leftTop:tuple):
        self.leftTop=leftTop

class ScreenManage:
    def __int__(self,addr,width:int,height:int):
        screen=Screen(width,height,(0,0))
        self.screens={addr:screen}
    def addClient(self,target:tuple,width:int,height:int):
        self.screens[target]=Screen(width,height,(0,0))
        screenkeysSort=sorted(self.screens.keys())
        for screenKey,index in zip(screenkeysSort,range(len(self.screens))):
            if index>0:
                lastSc=self.screens[screenkeysSort[index-1]]
                self.screens[screenKey].reLeftTop((lastSc.width+lastSc.leftTop[0],0))
