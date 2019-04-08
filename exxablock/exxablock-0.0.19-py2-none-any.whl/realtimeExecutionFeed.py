from socketIO_client_nexus import SocketIO, BaseNamespace
import sys, json, urllib2
import pandas as pd

#
# Execution classes
# A -- Best Bid and Offer of individual exchanges
# B -- Global Best Bid and Offer  from BBOs 
# C -- Order book of individual exchanges
# D -- Global order book aggregated from order books of all cryptocurrency exchanges
# E -- Global bid-ask crossing in the global order book
xqnClass = ['A1', 'B1', 'C1', 'D1', 'E1']

xqnAlias = {
    'A1': 'xqnbbo',
    'B1': 'xqngbbo',
    'C1': 'xqnobk',
    'D1': 'xqngobk',   
    'E1': 'xqngxng',   
}

alias2Class = {
    'xqnbbo' : 'A1',
    'xqngbbo' : 'B1',
    'xqnobk' : 'C1',
    'xqngobk'  : 'D1',
    'xqngxng'  : 'E1',
}

resSuffix = {
    'timeseries': 'ts',
    'event': 'evt',
    'minute': 'min'
}


class ExecutionBaseNamespace(BaseNamespace):
    pair = None

    def __init__(self, io, path):
        super(ExecutionBaseNamespace, self).__init__(io, path)


# define Socket.io channel handler class
class ExecutionNamespace(ExecutionBaseNamespace):
    def on_admin(self, *args):  # administration news channel
        print('on_admin :: ' + ''.join(args))

    def on_update(self, *args):  # execution value push channel
        print('on_update :: ' + ''.join(args))
    def on_reconnect(self):
        print('on_reconnect')

    def on_disconnect(self):
        print('on_disconnect')


class RealtimeExecutionFeed(object):
    host = None
    port = None
    socketIO = None
    xqnChnl = None

    def __init__(self, host='execution-rt.exxablock.io', port=80):
        self.host = host
        self.port = port

    def connect(self, cls, pair, res = 'timeseries', handler=ExecutionNamespace, verbose = False):
        self.socketIO = SocketIO(self.host, self.port)
        self.pair = pair
        #
        if not res in resSuffix.keys():
            raise Exception('unknown data resolution :' + res)
        #
        if cls in xqnClass:
            schnl = '/' + xqnAlias[cls] + resSuffix[res] + '-' + pair
        elif cls in xqnAlias.values():
            schnl = '/' + cls + resSuffix[res]  + '-' + pair
        else:
            raise Exception('unknown execution name :' + cls)
        #
        if verbose:
            print ('host:', self.host, 'port:', self.port, 'pair:', self.pair)
            print ('schnl:', schnl)
        #
        self.xqnChnl = self.socketIO.define(handler, schnl)
        print ('connected to an execution channel ' + schnl)

    def disconnect(self, path=''):
        self.socketIO.disconnect(path)

    def close (self):
        self.socketIO._close()

    def wait(self, **kw):
        self.socketIO.wait(kw)

    def getCurrencyMaster(self):
        url = 'http://' + self.host + ':' + str(self.port) + '/api/realtime/execution/crncymaster'
        jobj = json.loads (urllib2.urlopen(url).read())
        #
        pdf = pd.DataFrame(jobj['plst'])
        pdf.columns = ['pair']
        #
        edf = pd.DataFrame(jobj['elst'])
        edf.columns = ['exch']
        #
        tdf = pd.DataFrame(jobj['tlst'])
        tdf.columns = ['type']
        #
        return pdf, edf, tdf


if __name__ == '__main__':
    rtfeed = RealtimeExecutionFeed('localhost', '25486')
    rtfeed.connect('xqnbbo', 'BTC/USD')
    #rtfeed.getCurrencyMaster()
    rtfeed.wait()
    #

    class AltExecutionNamespace(BaseNamespace):
        msgcnt = 1

        def on_admin(self, *args):  # administration news channel
            print('on_admin  :: ' + ''.join(args))

        def on_update(self, *args):  # execution value push channel
            self.msgcnt += 1
            print('on_update :: ' + str(self.msgcnt) + ' :: ' + ''.join(args))

        def on_reconnect(self):
            print('on_reconnect')

        def on_disconnect(self):
            print('on_disconnect')

    rtfeed.connect('xqnbbo', 'BTC/USD', 'timeseries', AltExecutionNamespace)
    rtfeed.wait()
