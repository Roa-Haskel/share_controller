from pynput.keyboard import Key,KeyCode
import sys
keyChars = r"1!2@3#4$5%6^7&8*9(0)-_=+[{]}\|/?,<.>".strip()
_keyChars = {keyChars[i]: keyChars[i + 1] for i in range(0, len(keyChars), 2)}
class KeyEventFactory:
    keyChars=_keyChars
    keyNames="""
cmd:alt
alt_l:cmd
""".strip().split("\n")
    keyNames={i.split(":")[0]:i.split(":")[1] for i in keyNames}

    # keyChars={i[0]:i[1] for i in keyChars}
    def __init__(self):
        self.shiftRelease=True
    def input(self,key):
        if 'name' in dir(key):
            if 'shift' in key.name:
                self.shiftRelease=not self.shiftRelease
            data=("name",key.name)
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
            if sys.platform == 'darwin':
                name=self.keyNames.get(dt,dt)
            else:
                name=dt
            try:
                key=Key[name]
            except:
                key=None
        elif tp=='char':
            key=dt
        elif tp=='vk':
            key=KeyCode.from_vk(dt)
        else:
            raise TypeError(str(data))
        return key

if __name__ == '__main__':
    pass