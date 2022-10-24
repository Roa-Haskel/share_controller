import pystray
from PIL import Image
from control_manage import ControlManageServer

image=Image.open('resources/icon/img.png')


con=ControlManageServer()

def onClick(ico,item):
    con.setting()

    con.sendEvent(con.getScreens(),con.MsageType.SCREEN_UPDATE_EVENTS)

def close(ico,item):
    ico.stop()

icon=pystray.Icon(
    "xxx",image,menu=pystray.Menu(pystray.MenuItem('screen_manage',onClick),pystray.MenuItem('close',close))
)

icon.run()



