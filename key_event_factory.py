

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
        
"""

    keyChars={i[0]:i[1] for i in keyChars}
    def __init__(self):
        self.shiftRelease=True
    def input(self,key):
        if 'name' in dir(key):
            if 'shift' in key.name:
                self.shiftRelease=not self.shiftRelease
            data=("name",key.name)
        elif 'char' in dir(key):
            keyChar=key.char
            if not self.shiftRelease:
                keyChar=self.keyChars.get(keyChar,keyChar)
            data=("char",key.char)
        else:
            data=("vk",key.vk)

