from executionCli import *

class ExecutionCache  (ExecutionCli):

    def __init__(self, host='localhost', port=15487, res='timeseries'):
        super(ExecutionCache, self).__init__(host, port)


if __name__ == '__main__':
    host    = 'localhost'
    cache   = ExecutionCache(host, 15487)
    cache.connect()
    #
    pair = 'BTC/USD'
    #
    print "cache.xqnClass::", cache.xqnClass
    print "cache.xqnAlias::", cache.xqnAlias
    print 'available product class: ', cache.prodClass(pair)
    #
    for cl in cache.xqnClass:
        print cl, ':: ', pair, ' :: cnt ==> ', cache.count(cl, pair)
    #
    print "cache.count('xqnbbo', pair)::", cache.count('xqnbbo', pair)
    #
    print "cache.getData('A1', pair) :: ", cache.getData('A1', pair, 'M-2')

