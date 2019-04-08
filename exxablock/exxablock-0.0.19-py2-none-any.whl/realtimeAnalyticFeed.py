from socketIO_client_nexus import SocketIO, BaseNamespace
import sys, json, urllib2
import pandas as pd

#
# Analytic classes
# A -- price and price returns:
#   * price, return, cumulative return
# B -- moments:
#   * mean, var, skew, and kurtosis
# C -- similarity matrix measures:
#   * colinear, covariance, and correlation matrices
# D -- intraday volatility estimation:
#   * Average True Range(ATR), Parkinson(PK), Garman-Klass(GK), and Rogers-Satchell(RS)
# E -- intraday momentum indicators:
#   * Relative Strength Index (RSI)
anlClass = ['A1', 'B1', 'B2', 'C1', 'C2', 'C3', 'D1', 'E1']

anlAlias = {
    'A1': 'anlrtns',
    'B1': 'anlcmntincr',
    'B2': 'anlcmntwin',
    'C1': 'anlcolm',
    'C2': 'anlcovm',
    'C3': 'anlcorm',
    'D1': 'anlatr',   
    'E1': 'anlrsi',   
}

alias2Class = {
    'anlrtns' : 'A1',
    'anlcmntincr' : 'B1',
    'anlcmntwin' : 'B2',
    'anlcolm' : 'C1',
    'anlcovm' : 'C2',
    'anlcorm' : 'C3',
    'anlatr'  : 'D1',
    'anlrsi'  : 'E1',
}

resSuffix = {
    'timeseries': 'ts',
    'event': 'evt',
    'minute': 'min'
}


class AnalyticBaseNamespace(BaseNamespace):
    def __init__(self, io, path):
        super(AnalyticBaseNamespace, self).__init__(io, path)


# define Socket.io channel handler class
class AnalyticNamespace(AnalyticBaseNamespace):
    def on_admin(self, *args):  # administration news channel
        print('on_admin :: ' + ''.join(args))

    def on_update(self, *args):  # analytic value push channel
        print('on_update :: ' + ''.join(args))
    def on_reconnect(self):
        print('on_reconnect')

    def on_disconnect(self):
        print('on_disconnect')


class RealtimeAnalyticFeed(object):
    host = None
    port = None
    socketIO = None
    anlChnl = None

    def __init__(self, host='analytic-rt.exxablock.io', port=80):
        self.host = host
        self.port = port

    def connect(self, cls, res, handler=AnalyticNamespace, verbose = False):
        self.socketIO = SocketIO(self.host, self.port)
        #
        if not res in resSuffix.keys():
            raise Exception('unknown data resolution :' + res)
        #
        if cls in anlClass:
            schnl = '/' + anlAlias[cls] + resSuffix[res]
        elif cls in anlAlias.values():
            schnl = '/' + cls + resSuffix[res]
        else:
            raise Exception('unknown analytic name :' + cls)
        #
        if verbose:
            print ('host:', self.host, 'port:', self.port)
            print ('schnl:', schnl)
        #
        self.anlChnl = self.socketIO.define(handler, schnl)
        print ('connected to an analytic channel ' + schnl)

    def disconnect(self, path=''):
        self.socketIO.disconnect(path)

    def close (self):
        self.socketIO._close()

    def wait(self, **kw):
        self.socketIO.wait(kw)

    def getSecurityMaster(self):
        url = 'http://' + self.host + ':' + str(self.port) + '/realtime/meta/analytic/secmaster'
        return pd.DataFrame(json.loads(urllib2.urlopen(url).read())[0])[['symbol', 'name']]


if __name__ == '__main__':
    rtfeed = RealtimeAnalyticFeed('localhost', '23456')
    rtfeed.connect('anlrtns', 'timeseries')
    rtfeed.wait()
    #

    class AltAnalyticNamespace(BaseNamespace):
        msgcnt = 1

        def on_admin(self, *args):  # administration news channel
            print('on_admin  :: ' + ''.join(args))

        def on_update(self, *args):  # analytic value push channel
            print('on_update :: ' + str(self.msgcnt) + ' :: ' + ''.join(args))
            self.msgcnt += 1

        def on_reconnect(self):
            print('on_reconnect')

        def on_disconnect(self):
            print('on_disconnect')

    rtfeed.connect('anlrtns', 'timeseries', AltAnalyticNamespace)
    rtfeed.wait()
