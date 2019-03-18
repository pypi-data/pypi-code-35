import struct
import time
import datetime
from QiDataLoader.BinaryReader import BinaryReader
from QiDataLoader.Tick import Tick
from QiDataLoader.Quote import Quote

class MqTickReader:  
        CPosTicklen = 32
        # CFileFlag = ('K' << 24) + ('C' << 16) + ('I' << 8) + 'T'
        _filePath = ""
        _instrumentId = ""
        _exchangeId = ""
        _firstRead = False
        _instrumentType = 0
        _tradingDay = datetime.date
        _origDays = []
        _origTickOffset = []
        _origdayoffset= 0
        _quotecount = 0
        _origdays = 1
        _tickoffset = 0
        _multiUnit = 1000
        _preClosePrice = 0.0
        _preSettlementPrice = 0.0
        _upLimit = 0.0
        _downLimit = 0.0
        _openPrice = 0.0
        _preInterest = 0.0
        _tickcount = 0

        def __init__(self, instrumentType, instrumentId, filePath):
            self._filePath = filePath
            self._instrumentId = instrumentId
            self._exchangeId = "CFFEX"
            self._firstRead = False
            self._tradingDay = time.time()
            self._instrumentType = instrumentType
        
        def Read(self, tickSeries, offset, count):       
            data = open(self._filePath,'rb') 
            reader= BinaryReader(data)            
            self.ReadHeader(reader)
            self.ReadOrigDays(reader)    
            pos = self._tickoffset + offset * (self.CPosTicklen + self._quotecount * 2 * 8)
            reader.stream.seek(pos)
            self.ReadTicks1(tickSeries, reader, offset, count)
            return True            
        
        def ReadHeader(self, reader):        
            flag = reader.ReadInt32()    
            self._origDays.clear()
            self._origTickOffset.clear()
            self._origdays = 0
            reader.ReadInt16()
            self._quotecount = reader.ReadByte()
            itmp = 1
            imult = reader.ReadByte()
            for i in range(0,imult):
                itmp = itmp * 10

            self._multiUnit = itmp
            year = reader.ReadInt16()
            month = reader.ReadByte()
            day = reader.ReadByte()
            self._tradingDay = datetime.date(year, month, day)
            self._preClosePrice = reader.ReadInt32() / self._multiUnit
            self._preSettlementPrice = reader.ReadInt32() / self._multiUnit
            self._preInterest = reader.ReadInt32()
            self._upLimit = reader.ReadInt32() / self._multiUnit
            self._downLimit = reader.ReadInt32() / self._multiUnit
            self._openPrice = reader.ReadInt32() / self._multiUnit
            self._tickcount = reader.ReadInt32()
            iorig = reader.ReadInt16()
            self._origdays = (iorig >> 12)
            self._origdayoffset = (iorig & 0x0fff)
            self._tickoffset = reader.ReadInt16()
            return True
        
        def ReadOrigDays(self, reader):
            for i in range(0, self._origdays):        
                year = reader.ReadInt16()
                month = reader.ReadByte()
                day = reader.ReadByte()
                origtickoffset = reader.ReadInt32()
                origday = datetime.date(year, month, day)
                self._origDays.append(origday)
                self._origTickOffset.append(origtickoffset)
                
        def ReadTicks1(self, tickSeries, reader, offset, count):
            for origidx in range(0, len(self._origTickOffset)):        
                if (offset < self._origTickOffset[origidx]):
                    break
                origidx = origidx + 1               
            origidx = origidx - 1
            if (origidx < 0):
                return
            origday = self._origDays[origidx]
            nextorigoffset = 100000000
            if (origidx < len(self._origTickOffset) - 1):      
                nextorigoffset = self._origTickOffset[origidx + 1] - 1            
            leng = self._tickcount - offset
            if(leng < count):
                leng = leng 
            else:
                leng = count
            for i in range(0,leng):         
                tick = Tick()              
                tick.InstrumentType = self._instrumentType,
                tick.OpenPrice = self._openPrice,
                tick.PreClosePrice = self._preClosePrice,
                tick.InstrumentId = self._instrumentId,
                tick.ExchangeId = self._exchangeId,
                tick.PreOpenInterest = self._preInterest,
                tick.PreSettlementPrice = self._preSettlementPrice,
                tick.UpLimit = self._upLimit,
                tick.DropLimit = self._downLimit               
                hour = reader.ReadByte()
                min = reader.ReadByte()
                second = reader.ReadByte()
                msecond = reader.ReadByte()
                msecond *= 10
                tick.DateTime =datetime.datetime(origday.year,origday.month,origday.day,hour, min, second, msecond)
                tick.TradingDay = self._tradingDay
                tick.LastPrice = reader.ReadInt32() / self._multiUnit
                tick.HighPrice = reader.ReadInt32() / self._multiUnit
                tick.LowPrice = reader.ReadInt32() / self._multiUnit
                tick.OpenInterest = reader.ReadInt32()
                tick.Volume = reader.ReadInt32()
                tick.Turnover = reader.ReadDouble()
                # quote = Quote()
                # quote.AskVolume1 = reader.ReadInt32()
                # quote.BidVolume1 = reader.ReadInt32()
                # quote.AskPrice1 = reader.ReadInt32() / self._multiUnit
                # quote.BidPrice1 = reader.ReadInt32() / self._multiUnit
                # tick.Quote = quote
                tick.AskVolume1 = reader.ReadInt32()
                tick.BidVolume1 = reader.ReadInt32()
                tick.AskPrice1 = reader.ReadInt32() / self._multiUnit
                tick.BidPrice1 = reader.ReadInt32() / self._multiUnit
                
                tickSeries.append(tick)
                if (i + offset >= nextorigoffset):          
                    origidx = origidx + 1
                    if (origidx < len(self._origDays)):
                        origday = self._origDays[origidx]
                    nextorigoffset = 10000000
                    if (origidx < len(self._origTickOffset) - 1):               
                        nextorigoffset = self._origTickOffset[origidx + 1] - 1
        
    