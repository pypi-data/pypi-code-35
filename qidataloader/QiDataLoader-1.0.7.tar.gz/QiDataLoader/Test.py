import datetime
import pandas as pd
import sys
import os
sys.path.append(os.getcwd())
from MqDataLoader import *
import datetime

def CombineTick(instrumentIdA, instrumentIdB, beginDate, endDate):
    dataLoader = MqDataLoader("//172.16.10.200/MqData/futuretick/Future")
    tickSeriesA = dataLoader.GetTickSeries(instrumentIdA, beginDate, endDate)
    tickSeriesB = dataLoader.GetTickSeries(instrumentIdB, beginDate, endDate)
    lstA = []
    for tick in tickSeriesA:
        lstA.append([tick.DateTime, tick.LastPrice, tick.AskPrice1, tick.BidPrice1, tick.AskVolume1, tick.BidVolume1])
    dfA = pd.DataFrame(lstA, columns=['DateTime', 'LastPrice', 'AskPrice1', 'BidPrice1', 'AskVolume1', 'BidVolume1'])

    lstB = []
    for tick in tickSeriesB:
        lstB.append([tick.DateTime, tick.LastPrice, tick.AskPrice1, tick.BidPrice1, tick.AskVolume1, tick.BidVolume1])
    dfB = pd.DataFrame(lstB, columns=['DateTime', 'LastPrice', 'AskPrice1', 'BidPrice1', 'AskVolume1', 'BidVolume1'])

    result = pd.merge(dfA, dfB, how='outer', on='DateTime')
    result = result.sort_values(by=['DateTime'], ascending=[True])
    result.fillna(method='ffill', axis=0, inplace=True)

    lstStdSpread = []
    lstBuySpread = []
    lstSellSpread = []
    for index, row in result.iterrows():
        lastPriceA = row['LastPrice_x']
        lastPriceB = row['LastPrice_y']
        askPriceA = row['AskPrice1_x']
        askPriceB = row['AskPrice1_y']
        bidPriceA = row['BidPrice1_x']
        bidPriceB = row['BidPrice1_y']

        stdSpread = lastPriceA - lastPriceB
        buySpread = askPriceA - bidPriceB
        sellSpread = bidPriceA - askPriceB

        lstStdSpread.append(stdSpread)
        lstBuySpread.append(buySpread)
        lstSellSpread.append(sellSpread)

    result['StdSpread'] = lstStdSpread
    result['BuySpread'] = lstBuySpread
    result['SellSpread'] = lstSellSpread
    return result


def IntersectTick(instrumentIdA, instrumentIdB, beginDate, endDate):
    dataLoader = MqDataLoader("//172.16.10.200/MqData/futuretick/Future")
    tickSeriesA = dataLoader.GetTickSeries(instrumentIdA, beginDate, endDate)
    tickSeriesB = dataLoader.GetTickSeries(instrumentIdB, beginDate, endDate)
    lstA = []
    for tick in tickSeriesA:
        lstA.append([tick.DateTime, tick.LastPrice, tick.AskPrice1, tick.BidPrice1, tick.AskVolume1, tick.BidVolume1])
    dfA = pd.DataFrame(lstA, columns=['DateTime', 'LastPrice', 'AskPrice1', 'BidPrice1', 'AskVolume1', 'BidVolume1'])

    lstB = []
    for tick in tickSeriesB:
        lstB.append([tick.DateTime, tick.LastPrice, tick.AskPrice1, tick.BidPrice1, tick.AskVolume1, tick.BidVolume1])
    dfB = pd.DataFrame(lstB, columns=['DateTime', 'LastPrice', 'AskPrice1', 'BidPrice1', 'AskVolume1', 'BidVolume1'])

    result = pd.merge(dfA, dfB, how='inner', on='DateTime')
    result = result.sort_values(by=['DateTime'], ascending=[True])
    result.fillna(method='ffill', axis=0, inplace=True)

    lstStdSpread = []
    lstBuySpread = []
    lstSellSpread = []
    for index, row in result.iterrows():
        lastPriceA = row['LastPrice_x']
        lastPriceB = row['LastPrice_y']
        askPriceA = row['AskPrice1_x']
        askPriceB = row['AskPrice1_y']
        bidPriceA = row['BidPrice1_x']
        bidPriceB = row['BidPrice1_y']

        stdSpread = lastPriceA - lastPriceB
        buySpread = askPriceA - bidPriceB
        sellSpread = bidPriceA - askPriceB

        lstStdSpread.append(stdSpread)
        lstBuySpread.append(buySpread)
        lstSellSpread.append(sellSpread)

    result['StdSpread'] = lstStdSpread
    result['BuySpread'] = lstBuySpread
    result['SellSpread'] = lstSellSpread
    return result


def CreateTickCsv(instrumentIdA, instrumentIdB, beginDate, endDate, filePath):
    dfTick = IntersectTick(instrumentIdA, instrumentIdB, beginDate, endDate)
    print(dfTick)
    # path = 'D:/SpreadAnalysis/' + instrumentIdA[0:2] + beginDate.strftime('%Y%m%d')+'-' + endDate.strftime('%Y%m%d') + 'IntersectTick.csv'
    # dfTick.to_csv(filePath)


view = 3
if view == 1:
    instrumentIdA = "IC1812"
    instrumentIdB = "IC1903"
elif view == 2:
    instrumentIdA = "IH1812"
    instrumentIdB = "IH1903"
else:
    instrumentIdA = "IF1812"
    instrumentIdB = "IF1901"

beginDate = datetime.date(2018, 12, 12)
endDate = datetime.date(2018, 12, 12)
path = 'D:/SpreadAnalysis/' + instrumentIdA[0:2] + beginDate.strftime('%Y%m%d')+'-' + endDate.strftime('%Y%m%d') + 'IntersectTick.csv'
CreateTickCsv(instrumentIdA, instrumentIdB, beginDate, endDate, path)