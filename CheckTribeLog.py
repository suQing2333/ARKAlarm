import io
from aip import AipOcr
from PIL import ImageGrab
from PIL import Image
import time
import cv2
import numpy as np
import conf
import WeChatAlarm
import os

last_alarm = ""

def ImageDetection():
    # 截取屏幕并裁剪
    img = Image.open("TribeLog.png")
    # img = ImageGrab.grab()
    original_img = img
    # begin_x = conf.CONF_DATA.get("BEGIN_X")
    # begin_y = conf.CONF_DATA.get("BEGIN_Y")
    # end_x = conf.CONF_DATA.get("END_X")
    # end_y = conf.CONF_DATA.get("END_Y")
    begin_x = 1300
    begin_y = 80
    end_x = 1600
    end_y = 180
    cropped = img.crop((begin_x, begin_y, end_x, end_y))

    

    # 将格式转换到适用opencv
    cropped = cv2.cvtColor(np.asarray(cropped),cv2.COLOR_RGB2BGR)

    # 转换为hsv
    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

    # cv2.imshow("Image", hsv)
    # 二值化处理
    # low_hsv = conf.CONF_DATA.get("LOW_HSV")
    # high_hsv = conf.CONF_DATA.get("HIGH_HSV")
    low_hsv = [95,118,217]
    high_hsv = [100,130,255]
    low_hsv = np.array(low_hsv)
    high_hsv = np.array(high_hsv)

    mask = cv2.inRange(hsv,lowerb=low_hsv,upperb=high_hsv)
    cv2.imshow("Image", mask)
    cv2.waitKey(0)
    # 检测占比
    # x,y= mask.shape
    # bk = 0
    # wt = 0
    # for i in range(x):
    #     for j in range(y):
    #         if mask[i,j]==0:
    #             bk+=1
    #         else:
    #             wt+=1
    # rate1 = wt/(x*y) * 100
    # rate2 = bk/(x*y) * 100
    # print(rate1)

    # if rate1 >= conf.CONF_DATA.get("RATE"):
    #     image = Image.fromarray(cv2.cvtColor(mask,cv2.COLOR_BGR2RGB))
    #     baiduOCR(original_img,image)

def baiduOCR(original_img,img):
    #百度文字识别
    APP_ID = "24750544"
    API_KEY = "cZ4bIjsE0eEkRo8TBTcb8xAZ"
    SECRECT_KEY = "rT8wyMFlag7f0368hZBvhTXoto6zMlIj"
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

    img_b = io.BytesIO()
    #image转换为png
    img.save(img_b, format='PNG')
    #存入容器
    img_b = img_b.getvalue()
    # 调用百度aip文字识别
    message = client.basicAccurate(img_b)
    # 匹配关键字,匹配到应该调用微信发送
    print(message)

# ImageDetection()

def get_hsv():
    image=cv2.imread('TribeLog.png')
    HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    def getpos(event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN: #定义一个鼠标左键按下去的事件
            print(HSV[y,x])

    cv2.imshow("imageHSV",HSV)
    cv2.imshow('image',image)
    cv2.setMouseCallback("imageHSV",getpos)
    cv2.waitKey(0)

get_hsv()