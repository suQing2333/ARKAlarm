#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import win32gui as w
import time
import WeChatAlarm
import ImageDetection
import conf

def main():
    conf.reload_conf()
    WeChatAlarm.start()
    title_find = conf.CONF_DATA.get("TITLE_FIND")
    while True:
        title = w.GetWindowText (w.GetForegroundWindow())
        if title.find("ARK") != -1:
            ImageDetection.ImageDetection()
        time.sleep(4)

if __name__ == "__main__":
    main()