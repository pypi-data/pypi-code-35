#!/usr/bin/env python3
#-*- coding: utf-8 -*-


#====#====#====#====
#file: lead
#time: 5/29/18
#====#====#====#====

#from cython.parallel import funcname, linenum
import logging
import json
import time
import hashlib

_logger = logging.getLogger(__name__)

def funcname():
	return 1

def linenum():
	return 1


class BaseDeviceCallback(object):

	def callService(self, name, input):
		'''
			:param name[string]: method name
			:param input[dict]: , eg:
				{
					"args1": xxx,
					"args2": yyy
					...
				}
			:return:
				code[int]: 若获取成功则返回LEDA_SUCCESS, 失败则返回错误码（参考错误码定义:ledaException.py）
				output[dict]: , eg:
					{
						"key1": xxx,
						"key2": yyy,
						 ...
					}
		'''
		raise Exception("callService is empty")

	def getProperties(self, input):
		'''
			:param input[list]: ,eg:[property1,property2 ...]
			:return:
				code[int]: 若获取成功则返回LEDA_SUCCESS, 失败则返回错误码（参考错误码定义:ledaException.py）
				output[dict]: , eg:
					{
						'property1':xxx,
						'property2':yyy,
						 ...
					}
		'''
		raise Exception("getProperties is empty")

	def setProperties(self, input):
		'''
			:param input[dict]:, eg:
				{
					'property1':xxx,
					'property2':yyy,
					...
				}
			:return:
				code[int]: 若获取成功则返回LEDA_SUCCESS, 失败则返回错误码（参考错误码定义:ledaException.py）
				output[dict]: 数据内容自定义，若无返回数据，则值空:{}
		'''
		raise Exception("setProperties is empty")

class LedaModule(object):
	def __init__(self):
		pass

	

	def moduleInit(self, moduleName):
		'''模块初始化

			:param moduleName[string]: 模块名称
			:return:
		'''
		pass

	def moduleRelease(self):
		'''模块退出
		:return:
		'''
		pass

	def feedDog(self, thread_name, count_down_seconds):
		'''喂看门狗.
			:param thread_name: 需要保活的线程名称.
			:param count_down_seconds: 倒计时时间, -1表示停止保活, 单位:秒.
			:return:
		'''

		pass

	def getConfig(self):
		pass

	def getTSL(self, productKey):
		pass

	def getTSLConfig(self, productKey):
		pass

	def getPdInfo(self, productKey = ''):
		'''获取配置相关信息

			:param productKey[string]: 如果为空，则默认获取lead module 的配置信息
			:return: info[string]:输出信息内容
		'''
		pass

	def subConfig(self, key, type = 1):
		'''
			:param key: config name
			:param type: 0: Owner, 1: observer
			:return:
		'''
		pass
		

	def registerDeviceConfigCallback(self, callbackObj):
		'''注册设备配置变更回调.

		:param callbackObj: 设备变更通知回调接口对象
		:return:
		'''
		pass

	def driver_register_device(self, device_name, product_key, product_md5, profile, bus_callback_object):

		''' register a device
			:param device_name: 由设备特征值组成的唯一描述信息,只能由字母和数字组成
			:param product_key: 通过productConfig获取产品唯一描述信息
			:param product_md5: productConfig算出md5
			:param profile    : profile 设备三要素模型
			:param bus_callback_object: callback object
			:return: cloud_id
		'''
		pass

	def deviceUnregister(self, subDevice):
		''' unregister device

			:param subDevice: device obj
			:return:
		'''
		pass

	def deviceRegister(self, deviceName, productKey, productTsl, deviceCallBack):
		'''注册设备并上线设备(设备默认注册后即上线)
			:param deviceName[string]: 由设备特征值组成的唯一描述信息, 必须保证每个待接入设备名称不同.
			:param productKey[string]: 产品唯一描述信息, 由阿里提供, 在设备 tsl 里也可以查得到.
			:param productTsl[string]: 设备tsl, 由阿里提供描述规范, 描述了设备的能力
			:param deviceCallBack[obj]: 设备回调方法
			:return:ledaSubDev[obj]
		'''
		pass

