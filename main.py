import pystray
from PIL import Image
from share_control_server import ShareControlServer
import sys

#程序入口
if __name__ == '__main__':
    con = ShareControlServer()
    #windows 可运行系统托盘程序
    if sys.platform=='win32':
        image=Image.open('resources/icon/img.png')
        def onClick(ico,item):
            con.setting()
            con.broadcastScreens()

        def close(ico,item):
            con.close()
            ico.stop()

        icon=pystray.Icon(
            "xxx",image,menu=pystray.Menu(pystray.MenuItem('screen_manage',onClick),pystray.MenuItem('close',close))
        )

        icon.run()
    #mac系统使用系统托盘图标无法正常运行，请自行测试
    elif sys.platform=='darwin':
        for i in con.threads:
            i.join()


