import time
import threading

class StagingSet(set):
    def __init__(self, iterable,timeout=10):
        super().__init__(iterable)
        self.__destroyed=False
        self.timeout=timeout
        self.timer={i:self.timeout for i in self}
        threading.Thread(target=self.__chick).start()
    def __chick(self):
        while not self.__destroyed:
            removed=[]
            for i in self:
                if i not in self.timer:
                    self.timer[i]=self.timeout
                else:
                    self.timer[i]-=1
                    if self.timer[i]<1:
                        removed.append(i)
            if removed:
                for i in removed:
                    self.remove(i)
            time.sleep(1)
    def add(self, element) -> None:
        super().add(element)
        self.timer[element]=self.timeout

    def remove(self, element) -> None:
        if element in self.timer:
            self.timer.pop(element)
        super().remove(element)
    def safeRemove(self,element):
        try:
            self.remove(element)
        except KeyError as e:
            pass
    def destroy(self):
        self.__destroyed=True


class RemoveCallbackSet(StagingSet):
    def __init__(self,iterable,timeout=10,removeCallback:'function'=None):
        super().__init__(iterable,timeout)
        self.removeCallback=removeCallback
    def remove(self, element) -> None:
        super().remove(element)
        if self.removeCallback:
            threading.Thread(target=self.removeCallback,args=(element,)).start()
