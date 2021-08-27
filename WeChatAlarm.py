from PyWeChatSpy import WeChatSpy
from PyWeChatSpy.command import *
from lxml import etree
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from PyWeChatSpy.proto import spy_pb2
import os
import shutil
from queue import Queue
import threading
import conf

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
fh = TimedRotatingFileHandler("spy.log", when="midnight")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

# alarm_room = ["24467106791"]
# 21012194292

WECHAT_PROFILE = rf"C:\Users\{os.environ['USERNAME']}\Documents\WeChat Files"
PATCH_PATH = rf"C:\Users\{os.environ['USERNAME']}\AppData\Roaming\Tencent\WeChat\patch"
if not os.path.exists(WECHAT_PROFILE):
    logger.error("请先设置计算机用户名，并完善WECHAT_PROFILE和PATCH_PATH")
    exit()
if os.path.isdir(PATCH_PATH):
    shutil.rmtree(PATCH_PATH)
if not os.path.exists(PATCH_PATH):
    with open(PATCH_PATH, "a") as wf:
        wf.write("")
my_response_queue = Queue()
spy = WeChatSpy(response_queue=my_response_queue, key="ab28d8c4768ab3bc2ba86841313f6e32", logger=logger)

def pop_response():
    while True:
        data = my_response_queue.get()
        handle_response(data)


def handle_response(data):
    if data.type == PROFESSIONAL_KEY:
        if not data.code:
            logger.warning(data.message)
    elif data.type == WECHAT_CONNECTED:  # 微信接入
        print(f"微信客户端已接入 port:{data.port}")
        time.sleep(1)
        # spy.get_login_qrcode()  # 获取登录二维码
    elif data.type == HEART_BEAT:  # 心跳
        pass
    elif data.type == WECHAT_LOGIN:  # 微信登录
        print("微信登录")
        spy.get_account_details()  # 获取登录账号详情
    elif data.type == WECHAT_LOGOUT:  # 微信登出
        print("微信登出")
    elif data.type == CHAT_MESSAGE:  # 微信消息
        chat_message = spy_pb2.ChatMessage()
        chat_message.ParseFromString(data.bytes)
        for message in chat_message.message:
            _type = message.type  
            _from = message.wxidFrom.str  # 消息发送方
            _to = message.wxidTo.str  # 消息接收方
            content = message.content.str  # 消息内容
            _from_group_member = ""
            if _from.endswith("@chatroom"):
                _from_group_member = message.content.str.split(':\n', 1)[0]
                content = message.content.str.split(':\n', 1)[-1] 
            if _type == 1:  # 文本消息
                print(_from, _to, _from_group_member, content)
                roomid = _from.split("@")
                if roomid[0] not in conf.CONF_DATA.get("ALARM_ROOM")::
                    continue
                check_list = content.split(' ')
                if len(check_list) != 2:
                    continue
                if check_list[0] == conf.CONF_DATA.get("USER_NAME") and check_list[1] == conf.CONF_DATA.get("TEST_REQUEST"):
                    spy.send_text(_from, check_list[0] + "is online")
                    time.sleep(2)
    elif data.type == ACCOUNT_DETAILS:  # 登录账号详情
        if data.code:
            account_details = spy_pb2.AccountDetails()
            account_details.ParseFromString(data.bytes)
            print(account_details)
            # spy.get_contacts()  # 获取联系人列表
        else:
            logger.warning(data.message)
    elif data.type == SEND_TEXT_CALLBACK:
        print("发送文本回调")
        print(data)
        print(data.code)
    elif data.type == SEND_XML_CALLBACK:
        print("发送xml回调")
        print(data)
        print(data.code)
    elif data.type == SEND_IMAGE_CALLBACK:
        print("发送图片回调")
        print(data)
        print(data.code)
    elif data.type == SEND_FILE:
        if os.path.exists("alarm.png"):
            os.remove("alarm.png")        


def start_wechat():
    wechat_path = conf.CONF_DATA.get("WECHAT_PATH")
    pid = spy.run(wechat_path)
    pop_response()

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("开始线程：" + self.name)
        start_wechat()

def start():    
    thread1 = myThread(1, "Thread-1", 1)
    thread1.start()


def alarm_text(word):
    for i in conf.CONF_DATA.get("ALARM_ROOM"):
        spy.send_text(i+"@chatroom", word)

def alarm_pic(img_path):
    for i in conf.CONF_DATA.get("ALARM_ROOM"):
        spy.send_file(i+"@chatroom", img_path)
