#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import base64
import json
import sys
import JsonDecoder
import Message
import logging
import HttpServerWrapper
import HttpClientWrapper
from DefaultHttpWrapper import DefaultHttpClientWrapper, DefaultHttpServerWrapper,DefaultMsgHandler, DefaultResponseHandler
import httplib
from NBException import OAuthException

LogLevel = { "INFO":logging.INFO, "DEBUG":logging.DEBUG}


class MavNBClient:
	def __init__(self):
		logFormat = '<%(asctime)s %(funcName)s %(name)s:%(lineno)d %(levelname)s> %(message)s'
		logFileName = 'MavNBClient.log'
		logLevel = 'INFO'

	def initialize(self, 
		client_class=DefaultHttpClientWrapper, server_class=DefaultHttpServerWrapper, 
		handler_class=DefaultMsgHandler, response_handler = DefaultResponseHandler,webHook = "",
		logLevel = logging.INFO, logFileName = 'MavNBClient.log',
		cbpServerIP = "", cbpServerPort = "", userName = "", password = "", chatBotId = "", serverPort = 0):

		logFormat = '<%(asctime)s %(funcName)s %(name)s:%(lineno)d %(levelname)s> %(message)s'
		logging.basicConfig(filename = logFileName, format = logFormat, level = logLevel)
		self.logger = logging.getLogger(__name__)
		self.logger.info("Creating MavNBClient")
		self.username = userName
		self.password = password
		self.ip = cbpServerIP
		self.port = cbpServerPort
		self.listenPort = serverPort
		self.useHttps = False
		self.url = "http://"+self.ip + ":"+str(self.port)
		self.botId = chatBotId
		self.access_token = ""
		self.refresh_token = ""
		self.tokenExpiry = 3600
		self.aSyncClient = client_class(response_handler)
		self.server = server_class(handler_class)
		self.UrlValidity = None
		self.webHook = webHook

	def getLogger():
		return self.logger

	def start(self):
		self.server.startHttpServer(self.listenPort,self.webHook)

	def setUrl(self, callbackUrl):
		self.url = "http://" + callbackUrl

	def setUrlValidity(self, callbackUrlValidity):
		self.urlValidity = callbackUrlValidity

	def setAccessToken(self, username, password):
		base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		self.access_token = base64string

	def doOAuth(self, *args):
		try:
			URL = self.url+"/oauth2/v1/token"
			payload ="scope=botmessage&grant_type=client_credentials"
			base64string = "Basic " + base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
		
			conn = httplib.HTTPConnection(self.ip + ":"+str(self.port), timeout=10)
			headers = {'Connection':'keep-alive', 'Authorization':base64string}
			conn.request("POST", URL, body=payload, headers=headers)

			response = conn.getresponse()
			print response.reason
			if response.status == 200:
				authDic = json.load(response)
				print authDic
				self.access_token = authDic["access_token"]
				self.refresh_token = authDic["refresh_token"]
				self.tokenExpiry =  authDic["expires_in"]
			else:
				raise OAuthException("error response received for OAuth", "check the OAuth request", response)
			self.registerCallBack(self.doOAuth, self.tokenExpiry)
		except:
			raise

	def sendTextMessage(self, textMessage = "", userId = "", isDeliveredNeeded = True, isDisplayedNeeded = True, isAliased = True, jsonFile = ""):
		URL = self.url + "/bot/v1/" + self.botId + "/messages"
		self.logger.info( "Sending msg to {}".format(URL))
		chipListJson =""
		if jsonFile != "":
			chipListFile = open(jsonFile, "r")
			chipListJson = chipListFile.read()
			chipListJson = chipListJson.replace("\n", "")
			chipListFile.close()

		message = Message.Message(messageText = textMessage, recipient = userId, suggestedChipList = chipListJson)
		payload = JsonDecoder.encodeMessageObj(message)
		self.aSyncClient.sendRequest(url = URL, body= payload, headers = {'Connection':'keep-alive', "content-type":"application/json", 'Authorization':'Bearer %s' % self.access_token})


	def sendFileMessage(self, textMessage = "", userId = "", isDeliveredNeeded = True, isDisplayedNeeded = True, isAliased = True, jsonFile = ""):
		URL = self.url + "/bot/v1/" + self.botId + "/messages"
		self.logger.info( "Sending msg to {}".format(URL))
		fileJson =""
		if jsonFile != "":
			fileJsonFile = open(jsonFile, "r")
			fileJson = fileJsonFile.read()
			fileJson = fileJson.replace("\n", "")
			fileJsonFile.close()
		message = Message.Message(messageType = "File", messageText = textMessage, recipient = userId, fileJson = fileJson)
		payload = JsonDecoder.encodeMessageObj(message)
		self.aSyncClient.sendRequest(url = URL, body= payload, headers = {'Connection':'keep-alive', "content-type":"application/json", 'Authorization':'Bearer %s' % self.access_token})
		
	def sendRichCard(self, textMessage = "", userId = "", jsonFile = "", user = ""):
		richCardFile = open(jsonFile, "r")
		richCardFileJson = richCardFile.read()
		richCardFileJson = richCardFileJson.replace("\n", "")
		richCardFileJson = richCardFileJson.replace("	", "")
		richCardFile.close()
		URL = self.url + "/bot/v1/" + self.botId + "/messages"
		self.logger.info("Sending msg to {}".format(URL))
		message = Message.Message(messageText = textMessage, messageType = "RichCard", recipient = userId, richCard = richCardFileJson)
		payload = JsonDecoder.encodeMessageObj(message)
		self.aSyncClient.sendRequest(url = URL, body= payload, headers = {'Connection':'keep-alive', "content-type":"application/json", 'Authorization':'Bearer %s' % self.access_token})

	def sendStatus(self, msgId, status):
		URL = self.url + "/bot/v1/" + self.botId + "/messages/" + msgId + "/status"
		self.logger.info("Sending msg to {}".format(URL))
		message = Message.Message(messageType = "Status", )
		payload = JsonDecoder.encodeStatusObj(message, status)
		self.aSyncClient.sendRequest(url = URL, body= payload, headers = {'Connection':'keep-alive', "content-type":"application/json", 'Authorization':'Bearer %s' % self.access_token})

	def sendSuggestedChipList(self, textMessage = "", userId = "", jsonFile = "", user = ""):
		chipListFile = open(jsonFile, "r")
		chipListJson = chipListFile.read()
		chipListJson = chipListJson.replace("\n", "")
		chipListFile.close()
		URL = self.url + "/bot/v1/" + self.botId + "/messages"
		self.logger.info("Sending msg to {}".format(URL))
		message = Message.Message(messageText = textMessage, recipient = userId, suggestedChipList = chipListJson)
		payload = JsonDecoder.encodeMessageObj(message)
		self.aSyncClient.sendRequest(url = URL, body= payload, headers = {'Connection':'keep-alive', 'content-type':'application/json', 'Authorization':'Bearer %s' % self.access_token})
		self.logger.info(message.toString())
		return message.msgId

	def sendIsComposing(self, userId = ""):
		URL = self.url + "/bot/v1/" + self.botId + "/messages"
		self.logger.info("Sending msg to {}".format(URL))
		message = Message.Message(messageType = "IsTyping", recipient = userId)
		payload = JsonDecoder.encodeMessageObj(message)
		self.aSyncClient.sendRequest(url = URL, body= payload, headers = {'Connection':'keep-alive', "content-type":"application/json", 'Authorization':'Bearer %s' % self.access_token})
		
	def getCapability(self, userId = ""):
		URL = self.url + "/bot/v1/" + self.botId + "/contactCapabilities?userContact=%2B"+userId
		self.logger.info("Sending msg to {}".format(URL))
		self.aSyncClient.sendRequest(url = URL, headers = {'Connection':'keep-alive', 'Authorization':'Bearer %s' % self.access_token, "id":"1234"})

	def registerCallBack(self, callBack, timer, *args, **kwargs):
		self.aSyncClient.registerCallBack(callBack, timer, *args, **kwargs)
	def startTimer(self, callBack, timer, *args, **kwargs):
		self.aSyncClient.startTimer(callBack, timer, *args, **kwargs)

'''
	def registerKwCallBack(self, callBack, timer , **kargs):
		print kargs
		self.aSyncClient.registerCallBack(callBack, timer, **kargs)

	def startTimer(self, callBack, timer, *args):
		self.aSyncClient.registerCallBack(callBack, timer, args)

	def startTimer(self, callBack, timer, **kargs):
		self.aSyncClient.registerCallBack(callBack, timer, kargs)
'''

if __name__ == "__main__":
	print "MavNBClient Class"
	username = "C4BU91524137293@botplatform.lab.t-mobile.com"
	password = "monica"
	client = MavNBClient()#password=password, username=username, cbpIp = "10.10.161.205", cbpPort = 8081)
	client.initialize()
	#print client.aSyncClient
	#client.sendTextMessage(userId = "19843033304", textMessage = "Plz select one of the option")
	client.doOAuth()
	client.start()
	#client.waitForMessage()
	#hdl = DefaultHttpMessageHandler()
	time.sleep(100)
	sys.exit()
	#client.doOAuth()
	#try:
		#client.sendMessage()
	#except:
		#print "closing"
	#client.shutdown()
