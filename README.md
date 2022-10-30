# 多设备控制器共享

## 概述
该程序旨在以简单的方式实现跨操作系统的鼠标键盘共享功能，核心基于python pynput库实现鼠标键盘控制，基于udp协议实现局域网内设备之间的信息数据传输，基于tcp协议传输鼠标键盘控制事件，主要用于解决作者pc机和mac电脑的控制器共享功能。
当前支持鼠标键盘共享，剪贴板文本内容共享，未来将考虑支持设备间文件复制粘贴功能。

安装方法：

1、git clone https://gitee.com/Roa-Haskel/share_controller.git
2、cd share_controller
3、pip install -r requirements.txt

运行

python main.py
