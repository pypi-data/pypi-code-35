'''
Created on Feb 14, 2019

@author: reynolds
'''

import time
import numpy as np

from PyQt5.QtCore import pyqtSignal

from wrtdk.io.streamer.streamer import LoggingStreamer

class fieldfox_streamer(LoggingStreamer):
    '''
    classdocs
    '''
    
    new_d = pyqtSignal(list,str,int,int)
    new_ascan = pyqtSignal(list,str,int,int)

    def __init__(self,port=[]):
        '''  constructor  '''
        super().__init__()
        self.port = port
        self._logging = False
        
    def run(self):
        ''' the aux sensor thread '''
        if len(self.port) > 1: self._running = True
        
        while self._running:
            try:
                if self.port[0].measure():
                    self.new_ascan.emit(self.port[0].getData(),
                                        'AG',0,0)
                    line = ''
                    try:
                        line,_ = self.port[1].readLast()
                        d = float(line.decode().strip())
                        self.new_d.emit([d],'AG',0,1)
                    except:
                        d = np.NaN
                        print('MototCountError. Unable to parse motor count.',line)
                        self.new_d.emit([d],'ND',0,1)
                    
                
                    if self._logging: self.port[0].write(self._file,'data',d,time.time())
            except Exception as e:
                print(str(e),'Error in aux streamer.')
                
        for p in self.port:
            try:
                p.close()
            except Exception as e:
                print('Error.',str(e))
        
    def startLog(self, filename, ftype='w+'):
        ''' starts the log '''
        try:
            self._file = filename
            self.port[0].header(fn=self._file,odir='data')
            self._logging = True
        except Exception as e:
            print('Error starting aux log file.',str(e))
            
    def isLogging(self):
        ''' returns whether the device is logging '''
        return self._logging
            
    def stopLog(self):
        ''' stops the aux log '''
        self._logging = False
        