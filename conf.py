#!/usr/bin/python
# -*- coding: UTF-8 -*-

CONF_DATA = {
	"USER_NAME":"TC",

	# OCR所需参数
	"APP_ID":"24750544",
	"API_KEY":"cZ4bIjsE0eEkRo8TBTcb8xAZ",
	"SECRECT_KEY":"rT8wyMFlag7f0368hZBvhTXoto6zMlIj",

	# 识别的屏幕区间
	"BEGIN_X":0,
	"BEGIN_Y":0,
	"END_X":1920,
	"END_Y":200,

	# 识别的颜色区间 HSV格式
	"LOW_HSV":[0,200,200],
	"HIGH_HSV":[10,255,255],
	# 文字识别阈值
	"RATE":10,

	# 报警匹配的字符串 
	"ALARM_KEY":"",
	# 报警的 群聊roomid
	"ALARM_ROOM":[],
	# 是否需要报警截图
	"NEED_SCREENSHOT":1,
	# 是否需要报警时间
	"NEED_TIME":1,
	# 报警文字
	"ALARM_STRING":"微信报警",
	# 检测报警系统在线,在报警群发送对应文本
	"TEXT_REQUEST":"check_alarm_online",

	# 微信路径
	"WECHAT_PATH":r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
}


def _init():
    global _global_dict
    _global_dict = {}


def set_value(key,value):
    _global_dict[key] = value


def get_value(key,defValue=None):
	return _global_dict.get(key)