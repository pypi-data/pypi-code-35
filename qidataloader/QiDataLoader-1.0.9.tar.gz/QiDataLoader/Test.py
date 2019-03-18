import datetime
import pandas as pd
import sys
import os
from QiDataLoader.MqDataLoader import MqDataLoader
import datetime

instrumentIdA = "IF1812"
instrumentIdB = "IF1901"
beginDate = datetime.date(2018, 12, 12)
endDate = datetime.date(2018, 12, 12)
dataLoader = MqDataLoader("//172.16.10.200/MqData/futuretick/Future")
tickSeriesA = dataLoader.GetTickSeries(instrumentIdA, beginDate, endDate)
lstA = []
for tick in tickSeriesA:
    lstA.append([tick.DateTime, tick.LastPrice, tick.AskPrice1, tick.BidPrice1, tick.AskVolume1, tick.BidVolume1])
dfA = pd.DataFrame(lstA, columns=['DateTime', 'LastPrice', 'AskPrice1', 'BidPrice1', 'AskVolume1', 'BidVolume1'])

print(dfA)