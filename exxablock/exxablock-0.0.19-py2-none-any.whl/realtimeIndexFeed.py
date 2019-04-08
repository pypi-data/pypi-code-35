from socketIO_client_nexus import SocketIO, BaseNamespace
import sys, json, urllib2
import pandas as pd

idxClass = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'X1', 'X2', 'ZZ']
idxMetaClass = ['M1', 'M2']

idxAlias = {
    'A1': 'idxmktcap',
    'A2': 'idxprice',
    'A3': 'idxadjprice',
    'B1': 'idxpricertn',
    'B2': 'idxsupplyrtn',
    'B3': 'idxvolumertn',
    'X1': 'idxcompositemp',
    'X2': 'idxcompositempv',
    'ZZ': 'idxall'
} 

idxMetaAlias = {
    'M1': 'idxconstituent',
    'M2': 'idxmktdfactor',
}


alias2Class = {
    'idxmktcap': 'A1',
    'idxprice': 'A2',
    'idxadjprice': 'A3',
    'idxpricertn': 'B1',
    'idxsupplyrtn': 'B2',
    'idxvolumertn': 'B3',
    'idxcompositemp': 'X1',
    'idxcompositempv': 'X2',
    'idxall': 'ZZ' 
} 

resSuffix = { 
    'timeseries' : 'ts',
    'event'      : 'evt',
    'minute'     : 'min'
}

class IndexBaseNamespace(BaseNamespace):
    def __init__(self, io, path):
        super(IndexBaseNamespace, self).__init__(io, path)


# define Socket.io channel handler class
class IndexNamespace(IndexBaseNamespace):
    def on_admin(self, *args):  # administration news channel
        print('on_admin :: ' + ''.join(args))

    def on_update(self, *args):  # index value push channel
        print('on_update :: ' + ''.join(args))
    
    def on_reconnect(self):
        print('on_reconnect')

    def on_disconnect(self):
        print('on_disconnect')


class RealtimeIndexFeed(object):
    host = None
    port = None
    socketIO = None
    idxChnl = None

    def __init__(self, host='index-rt.exxablock.io', port=80):
        self.host = host
        self.port = port

    def connect (self, cls, res, handler = IndexNamespace, verbose = False):
        self.socketIO = SocketIO(self.host, self.port)
        #
        if not res in resSuffix.keys():
            raise Exception('unknown data resolution :' + res)
        #
        if cls in idxMetaClass:
            schnl = '/' + idxMetaAlias[cls] + resSuffix[res]
        elif cls in idxMetaAlias.values():
            schnl = '/' + cls + resSuffix[res]
        elif cls in idxClass:
            schnl = '/' +  idxAlias[cls] + resSuffix[res]
        elif cls in idxAlias.values():
            schnl = '/' + cls + resSuffix[res]
        else:
            raise Exception('unknown index :' + cls)      
        #
        if verbose:
            print ('host:', host, 'port:', port)
            print ('schnl:', schnl)
        #
        self.idxChnl = self.socketIO.define(handler, schnl)
        print ('connected to an index channel ' + schnl)

    def disconnect (self, path=''):
        self.socketIO.disconnect(path)

    def close (self):
        self.socketIO._close()
        
    def wait(self, **kw):
        self.socketIO.wait(kw)
    
    def getSecurityMaster(self):
        url = 'http://' + self.host + ':' + str(self.port) + '/realtime/meta/index/secmaster'
        return pd.DataFrame(json.loads(urllib2.urlopen(url).read())[0])[['symbol', 'name']]


if __name__ == '__main__':
    rtfeed = RealtimeIndexFeed('localhost', '12345')
    #rtfeed.connect('idxmktcap', 'timeseries')
    #rtfeed.wait()
    #
    class AltIndexNamespace(BaseNamespace):
        msgcnt = 1
        def on_admin(self, *args):  # administration news channel
            print('on_admin  :: ' + ''.join(args))

        def on_update(self, *args):  # index value push channel
            print('on_update :: ' +  str(self.msgcnt) + ' :: ' +  ''.join(args))
            self.msgcnt += 1
    
        def on_reconnect(self):
            print('on_reconnect')

        def on_disconnect(self):
            print('on_disconnect')

    rtfeed.connect('idxmktcap', 'timeseries', AltIndexNamespace)
    rtfeed.wait()
