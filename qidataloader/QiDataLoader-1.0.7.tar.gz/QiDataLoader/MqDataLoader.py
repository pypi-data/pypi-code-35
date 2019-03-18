from MqTickReader import *
import datetime
import os

class MqDataLoader: 
    def __init__(self, futureTickPath):
        self._futureTickPath = futureTickPath

    def GetTickSeries(self, instrumentId, beginTime, endTime):
        tickSeries = []
        tradingDate = beginTime
        while(tradingDate <= endTime):  
            filePath = self._futureTickPath+"/"+ tradingDate.strftime('%Y%m%d')+"/"+instrumentId + ".tk"
            if(os.path.exists(filePath)):
                if (instrumentId != "index"):        
                    mqTickReader = MqTickReader("", instrumentId, filePath)
                    mqTickReader.Read(tickSeries, 0, 10000000000)       
            tradingDate = tradingDate + datetime.timedelta(days=1)
   
        return tickSeries
