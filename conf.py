#!/usr/bin/python
# -*- coding: UTF-8 -*-

CONF_DATA = {
	"USER_NAME":"",

	# OCR所需参数
	"APP_ID":"",
	"API_KEY":"",
	"SECRECT_KEY":"",

	# 识别的屏幕区间
	"BEGIN_X":600,
	"BEGIN_Y":20,
	"END_X":1320,
	"END_Y":70,

	# 识别的颜色区间 HSV格式
	"LOW_HSV":[0,200,200],
	"HIGH_HSV":[10,255,255],
	# 文字识别阈值
	"RATE":4,

	# 如果匹配到对应字符串不会报警
	"ALARM_SHIELD":["baby"],
	# 报警匹配的字符串 
	"ALARM_KEY":"killed",
	# 报警的 群聊roomid
	"ALARM_ROOM":[],
	# 是否需要报警截图
	"NEED_SCREENSHOT":1,
	# 是否需要报警时间
	"NEED_TIME":1,
	# 是否需要默认报警
	"NEED_DEFAULT":1,
	# 报警文字
	"ALARM_STRING":"微信报警",
	# 检测报警系统在线,在报警群发送对应文本
	"TEST_REQUEST":"check_alarm_online",

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

def reload_conf():
	for line in open("conf.txt","r"):
		line_list = line.split(':',1)
		key = line_list[0]
		value = line_list[1]
		if type(CONF_DATA.get(key)) == int:
			if type(eval(value)) == int:
				value = int(value)
			else:
				print("%s conf error",key)
				continue
		elif type(CONF_DATA.get(key)) == list:
			value = value.split(',')
			if len(CONF_DATA.get(key)) != 0 and type(CONF_DATA.get(key)[0]) == int:
				for i in range(len(value)):
					if type(eval(value[i])) == int:
						value[i] = int(value[i])
					else:
						print("%s conf error",key)
						continue
		# if key == "WECHAT_PATH":
		# 	print(value)
		# 	CONF_DATA[key] = repr(value)
		# else:
		CONF_DATA[key] = value

print(CONF_DATA)
reload_conf()
print(CONF_DATA)
