from pynput.keyboard import Key,KeyCode

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
""".strip().split(":")
    keyNames={i[0]:i[1] for i in keyChars}

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

