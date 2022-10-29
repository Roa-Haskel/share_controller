import pystray
from PIL import Image
from share_control_server import ShareControlServer
import sys

if __name__ == '__main__':
    con = ShareControlServer()
    if sys.platform=='win32':
        image=Image.open('resources/icon/img.png')
        def onClick(ico,item):
            con.setting()
            con.broadcastScreens()

        def close(ico,item):
            ico.stop()

        icon=pystray.Icon(
            "xxx",image,menu=pystray.Menu(pystray.MenuItem('screen_manage',onClick),pystray.MenuItem('close',close))
        )

        icon.run()
    elif sys.platform=='darwin':
        for i in con.threads:
            i.join()


