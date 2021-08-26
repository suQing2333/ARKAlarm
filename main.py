#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import win32gui as w
import time
import ImageDetection
import WeChatAlarm
import conf

def 

def main():
    WeChatAlarm.start()
    title_find = conf.CONF_DATA.get("TITLE_FIND")
    while True:
        title = w.GetWindowText (w.GetForegroundWindow())
        if title.find("ARK") != -1:
            print(title)
            ImageDetection.ImageDetection()
        time.sleep(1)

if __name__ == "__main__":
    main()