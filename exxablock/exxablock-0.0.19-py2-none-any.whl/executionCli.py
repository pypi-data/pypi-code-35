from redisCli import *

defaultRtExecutionCon = {
    'host': 'localhost',
    'port': 15486
}

defaultHistExecutionCon = {
    'host': 'localhost',
    'port': 15487
}

class ExecutionCli  (RedisCli):
    # execution classes
    xqnClass = ['A1', 'B1', 'C1', 'D1', 'E1']

    xqnAlias = {
        'A1': 'xqnbbo',
        'B1': 'xqngbbo',
        'C1': 'xqnobk',
        'D1': 'xqngobk',   
        'E1': 'xqngxng',   
    }

    cols = {
        'A1': ['timestamp', 'exch', 'nts', 'ets', 'bbp',	'bbs', 'bap', 'bas', 'sd', 'mp', 'wp', 'dp', 'bd', 'ad'],
        'B1': ['gbts', 'gbbp', 'gbbs', 'gbbx', 'gbap', 'gbas', 'gbax', 'sd', 'mp', 'wp'],
        'C1': ['timestamp', 'cbv', 'bv',	'bs', 'bp', 'ap', 'as',	'av', 'cav'],
        'D1': ['timestamp', 'gbs', 'gbp', 'gap',	'gas'],
        'E1': ['timestamp', 'xbs', 'xbp', 'xap',	'xas']
    }

    pair = None

    def __init__(self, host, port):
        super(ExecutionCli, self).__init__(host, port)

    def connect(self, host=None, port=None):
        return super(ExecutionCli, self).connect(host, port)

    def prodClass(self, pair, res = 'timeseries'):
        rsfx   = resSuffix[res] + '-' + pair
        return [k[:k.rfind(rsfx)] for k in super(ExecutionCli, self).keys() if k.endswith(rsfx)]

    def count(self, cls, pair, res = 'timeseries'):
        xqntc  = self.xqnAlias[cls] if cls in self.xqnClass else cls
        return super(ExecutionCli, self).count(xqntc + resSuffix[res] + '-' + pair)

    def head(self, cls, pair,  n = -1, res = 'timeseries', withTimestamp=True):
        xqntc  = self.xqnAlias[cls] if cls in self.xqnClass else cls
        return super(ExecutionCli, self).head(cls + resSuffix[res] + '-' + pair, n, withTimestamp)

    def tail(self, cls, pair,  n = -1, res = 'timeseries', withTimestamp=True):
        xqntc  = self.xqnAlias[cls] if cls in self.xqnClass else cls
        return super(ExecutionCli, self).tail(xqntc + resSuffix[res] + '-' + pair, n, withTimestamp)

    def minTime(self, cls, pair, start=0, res = 'timeseries'):
        rsfx        = resSuffix[res] + '-' + pair
        if isinstance(cls, list):
            xqntc  = [(self.xqnAlias[nm] if nm in self.xqnClass else nm) for nm in cls]
            xqnts   = map(lambda k: k + rsfx, xqntc)
        else:
            xqnts   = (self.xqnAlias[cls]
                     if cls in self.xqnClass else cls) + rsfx
        return datetime.fromtimestamp(super(ExecutionCli, self).minTime(xqnts, start)/1000)

    def maxTime(self, cls, pair, end=-1, res = 'timeseries'):
        rsfx        = resSuffix[res] + '-' + pair
        if isinstance(cls, list):
            xqntc  = [(self.xqnAlias[nm] if nm in self.xqnClass else nm) for nm in cls]
            xqnts   = map(lambda k: k + rsfx, xqntc)
        else:
            xqnts   = (self.xqnAlias[cls] if cls in self.xqnClass else cls) + rsfx
        return datetime.fromtimestamp(super(ExecutionCli, self).maxTime(xqnts, end)/1000)

    def getCurrencyMaster(self):
        jobj = json.loads(self.cli.zrange('crncyaster', -1, -1))
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


    def getData(self, cls, pair, n = 10, dtype = 'object', opts = {}, res = 'timeseries'):
        if cls == 'C1':
            print ('Cache does not support the product class', cls)
            return
        #
        if not cls in self.xqnClass:
            print (cls + ' should be one of ', self.xqnClass)
            return
        #
        if n == 0:
            st = 0
            ed = -1
        else:
            st = 0 if n > 0 else n
            ed = -1 if n < 0 else n - 1 
        #
        prd = self.xqnAlias[cls] if cls in self.xqnClass else cls
        tsdata = self.cli.zrange(prd + resSuffix[res] + '-' + pair, st, ed, withscores=True)
        #
        if dtype == 'object':
            robj = []
            for ts in tsdata:
                robj.append(cbor.loads(ts[0]))
            return robj
        #
        rdf = None
        for ts in tsdata:
            cobj = cbor.loads(ts[0])
            rtns = cobj['value']
            ts = cobj['timestamp']
            #
            if 'stats' in rtns.keys():
                del rtns['stats']
            #
            if cls == 'B1':
                df = pd.DataFrame(rtns, index=[0])
            elif cls == 'D1':
                gbdepth = rtns['gbdepth']
                gbp = [0] * len(gbdepth)
                gbs = [0] * len(gbdepth)
                for ix in range(len(gbdepth)):
                    gbp[ix] = gbdepth[ix][0]
                    gbs[ix] = gbdepth[ix][1]
                bdf = pd.DataFrame({ 'gbp': gbp, 'gbs': gbs})
                #
                gadepth = rtns['gadepth']
                gap = [0] * len(gadepth)
                gas = [0] * len(gadepth)
                for ix in range(len(gadepth)):
                    gap[ix] = gadepth[ix][0]
                    gas[ix] = gadepth[ix][1]
                adf = pd.DataFrame({ 'gap': gap, 'gas': gas})
                #
                if bdf.shape[0] > adf.shape[0]:
                    df = pd.concat([bdf.reset_index(), adf], axis=1)
                else:
                    df = pd.concat([adf.reset_index(), bdf], axis=1)
                df['timestamp'] = ts
            elif cls == 'E1':
                xbdepth = rtns['xbdepth']
                xbp = [0] * len(xbdepth)
                xbs = [0] * len(xbdepth)
                for ix in range(len(xbdepth)):
                    xbp[ix] = xbdepth[ix][0]
                    xbs[ix] = xbdepth[ix][1]
                bdf = pd.DataFrame({ 'xbp': xbp, 'xbs': xbs})
                #
                xadepth = rtns['xadepth']
                xap = [0] * len(xadepth)
                xas = [0] * len(xadepth)
                for ix in range(len(xadepth)):
                    xap[ix] = xadepth[ix][0]
                    xas[ix] = xadepth[ix][1]
                adf = pd.DataFrame({ 'xap': xap, 'xas': xas})
                #
                if bdf.shape[0] > adf.shape[0]:
                    df = pd.concat([bdf.reset_index(), adf], axis=1)
                else:
                    df = pd.concat([adf.reset_index(), bdf], axis=1)
                df['timestamp'] = ts
            else:
                df = pd.DataFrame(rtns)
            #
            lts = pd.to_datetime(cobj['timestamp'], unit='ms')
            df['timestamp'] = lts
            rdf = df if rdf is None else rdf.append(df)
            rdf.index = range(rdf.shape[0])
        #
        return rdf[self.cols[cls]]


    def getDataByTimeRange(self, cls, pair, start='-Inf', end='+Inf', dtype = 'object', opts = {}, res = 'timeseries'):
        if cls == 'C1':
            print ('Cache does not support the product class', cls)
            return
        #
        if not cls in self.xqnClass:
            print (cls + ' should be one of ', self.xqnClass)
            return
        #
        mnt = self.minTime (cls, pair)
        mxt = self.maxTime (cls, pair)
        #
        st = mnt if start == '-Inf' else start
        ed = mxt if end == '+Inf' else end
        #
        if st != mnt and type(st) == str:
            if st[0] in "sSmMhHdD":
                dlt  = int(st[1:])
                tp = st[0].lower()
                if tp == 's':
                    st = (mxt if dlt < 0 else mnt) + timedelta (seconds=dlt)
                elif tp == 'm':
                    st = (mxt if dlt < 0 else mnt) + timedelta (minutes=dlt)
                elif tp == 'h':
                    st = (mxt if dlt < 0 else mnt) + timedelta (hours=dlt)
                elif tp == 'd':
                    st = (mxt if dlt < 0 else mnt) + timedelta (days=dlt)
        #
        if ed != mxt and type(ed) == str:
            if ed[0] in "sSmMhHdD":
                dlt  = int(ed[1:])
                tp = ed[0].lower()
                if tp == 's':
                    ed = (mxt if dlt < 0 else mnt) + timedelta (seconds=dlt)
                elif tp == 'm':
                    ed = (mxt if dlt < 0 else mnt) + timedelta (minutes=dlt)
                elif tp == 'h':
                    ed = (mxt if dlt < 0 else mnt) + timedelta (hours=dlt)
                elif tp == 'd':
                    ed = (mxt if dlt < 0 else mnt) + timedelta (days=dlt)
        #
        utcstart, utcend = self.timeRange2Offsets(res, st, ed)
        #
        prd = self.xqnAlias[cls] if cls in self.xqnClass else cls
        tsdata = self.cli.zrangebyscore(prd + resSuffix[res] + '-' + pair, utcstart, utcend, withscores=True)
        #
        if dtype == 'object':
            robj = []
            for ts in tsdata:
                robj.append(cbor.loads(ts[0]))
            return robj
        #
        rdf = None
        for ts in tsdata:
            cobj = cbor.loads(ts[0])
            rtns = cobj['value']
            ts = cobj['timestamp']
            #
            if 'stats' in rtns.keys():
                del rtns['stats']
            #
            if cls == 'B1':
                df = pd.DataFrame(rtns, index=[0])
            elif cls == 'D1':
                gbdepth = rtns['gbdepth']
                gbp = [0] * len(gbdepth)
                gbs = [0] * len(gbdepth)
                for ix in range(len(gbdepth)):
                    gbp[ix] = gbdepth[ix][0]
                    gbs[ix] = gbdepth[ix][1]
                bdf = pd.DataFrame({ 'gbp': gbp, 'gbs': gbs})
                #
                gadepth = rtns['gadepth']
                gap = [0] * len(gadepth)
                gas = [0] * len(gadepth)
                for ix in range(len(gadepth)):
                    gap[ix] = gadepth[ix][0]
                    gas[ix] = gadepth[ix][1]
                adf = pd.DataFrame({ 'gap': gap, 'gas': gas})
                #
                if bdf.shape[0] > adf.shape[0]:
                    df = pd.concat([bdf.reset_index(), adf], axis=1)
                else:
                    df = pd.concat([adf.reset_index(), bdf], axis=1)
                df['timestamp'] = ts
            elif cls == 'E1':
                xbdepth = rtns['xbdepth']
                xbp = [0] * len(xbdepth)
                xbs = [0] * len(xbdepth)
                for ix in range(len(xbdepth)):
                    xbp[ix] = xbdepth[ix][0]
                    xbs[ix] = xbdepth[ix][1]
                bdf = pd.DataFrame({ 'xbp': xbp, 'xbs': xbs})
                #
                xadepth = rtns['xadepth']
                xap = [0] * len(xadepth)
                xas = [0] * len(xadepth)
                for ix in range(len(xadepth)):
                    xap[ix] = xadepth[ix][0]
                    xas[ix] = xadepth[ix][1]
                adf = pd.DataFrame({ 'xap': xap, 'xas': xas})
                #
                if bdf.shape[0] > adf.shape[0]:
                    df = pd.concat([bdf.reset_index(), adf], axis=1)
                else:
                    df = pd.concat([adf.reset_index(), bdf], axis=1)
                df['timestamp'] = ts
            else:
                df = pd.DataFrame(rtns)
            #
            lts = pd.to_datetime(cobj['timestamp'], unit='ms')
            df['timestamp'] = lts
            rdf = df if rdf is None else rdf.append(df)
            rdf.index = range(rdf.shape[0])
        #
        return rdf[self.cols[cls]]



if __name__ == '__main__':
    cli = ExecutionCli('localhost', 15487)
    cli.connect()
    #
    pair = 'BTC/USD'
    #
    print "cli.xqnClass::", cli.xqnClass
    print "cli.xqnAlias::", cli.xqnAlias
    print 'available product class: ', cli.prodClass(pair)
    for cl in cli.xqnClass:
        print cl, ':: ', pair, ' :: cnt ==> ', cli.count(cl, pair)
    #
    print "cli.count('xqnbbo', pair)::", cli.count('xqnbbo', pair)
    print "cli.minTime('A1', pair) :: ", cli.minTime('A1', pair)
    print "cli.maxTime('A1', pair) :: ", cli.maxTime('A1', pair)
    print "cli.getData('A1', pair) :: ", cli.getData('A1', pair)
    print "cli.getData('A1', pair) :: ", cli.getData('A1', pair)
    #print "cli.getDataByTimeRange('A1', pair) :: ", cli.getDataByTimeRange('A1', pair, start = '2019-04-06 03:25:00.000')
