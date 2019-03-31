import qvstbus
def register(hubIp, myName, callback=None):
	return qvstbus.QvstBus.register(hubIp, myName, callback)