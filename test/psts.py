import pystray
from PIL import Image

image=Image.open('../resources/icon/img.png')

def onClick(ico,item):
    print(item)
    print('----')

def close(ico,item):
    ico.stop()

icon=pystray.Icon(
    "xxx",image,menu=pystray.Menu(pystray.MenuItem('say',onClick),pystray.MenuItem('close',close))
)




icon.run()



