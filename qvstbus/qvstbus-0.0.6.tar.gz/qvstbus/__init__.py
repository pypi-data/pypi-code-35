import websocket
import json
import time
import random
try:
	import _thread as thread
except:
	import thread
class QvstBus:		
	@staticmethod
	def register(hubIp, myName, callback=None, port=2019):	
		obj = QvstBus()	
		websocket.enableTrace(True)
		obj.ws = websocket.WebSocketApp('ws://{0}:{1}'.format(hubIp, port))	
		thread.start_new_thread(obj.ws.run_forever,())	
		obj.hubIp = hubIp
		obj.myName = myName		
		obj.requestMap = {}
		obj.methodMap = {}
		def on_open(ws):
			ws.send(myName)		
			if (callback is not None):
				callback(obj)				
		def on_message(ws, msg):
			msg = json.loads(msg)			
			data = msg['data']
			if ('method' in data):
				error = None
				result = None
				try:
					result = obj.methodMap.get(data['method'])(data['params'])
				except Exception:
					error = 'method execution error'
				obj._response(msg['from'], data['id'], result, error)
			else:
				if (data['error'] is not None):
					obj._log('request error: {}'.format(data['error']))
				else:
					try:
						obj.requestMap.get(data['id'])(data['result'])
						del obj.requestMap[data['id']]
					except Exception:
						obj._log('response error')
		def help(stupid_arg):
			return list(filter(lambda x: x is not 'help', obj.methodMap.keys()))		

		def on_error(ws, err):
			raise Exception('websocket connection error {}'.format(err))		
		obj.ws.on_open = on_open
		obj.ws.on_message = on_message
		obj.ws.on_error = on_error		
		obj.on('help', help)		

	def on(self, methodName, callback):
		self.methodMap[methodName] = callback

	def call(self, to, method, params, callback):
		id = self._uuid()
		msg = {
			'from': self.myName,
			'to': to,
			'data': {
				'id': id,
				'method': method,
				'params': params
			}
		}
		self.requestMap[id] = callback
		self._send(msg)

	def _log(self, msg):
		print(msg)

	def _send(self, msg):		
		msg = json.dumps(msg)
		self.ws.send(msg)

	def _uuid(self):
		return '{0}{1}'.format(round(time.time() * 1000), str(random.random())[2:])

	def _response(self, to, id, result, error):
		msg = {
			'from': self.myName,
			'to': to,
			'data': {
				'id': id,
				'result': result,
				'error': error
			}
		}
		self._send(msg)		
register = QvstBus.register
