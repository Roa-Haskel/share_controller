import time
import threading

class StagingSet(set):
    TIME_OUT=10
    def __init__(self, iterable):
        super().__init__(iterable)
        self.timer={i:self.TIME_OUT for i in self}
        threading.Thread(target=self.chick).start()
    def chick(self):
        while True:
            removed=[]
            for i in self:
                if i not in self.timer:
                    self.timer[i]=self.TIME_OUT
                else:
                    self.timer[i]-=1
                    if self.timer[i]<1:
                        removed.append(i)
            if removed:
                for i in removed:
                    self.remove(i)
            time.sleep(1)
    def add(self, element) -> None:
        self.timer[element]=10
        super().add(element)
    def remove(self, element) -> None:
        if element in self.timer:
            self.timer.pop(element)
        super().remove(element)