import __init__ as qvstbus
ip = '127.0.0.1'
def test(o):
	return ''
def result(x):
	print(x)
def fa(a):	
	a.on('test a', test)
	a.call(to='a', method='help', params={}, callback=result)

qvstbus.register(hubIp=ip, myName='a', port=80, callback=fa)
input()