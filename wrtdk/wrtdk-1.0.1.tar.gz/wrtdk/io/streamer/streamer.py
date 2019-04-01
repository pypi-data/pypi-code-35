'''
Created on Feb 14, 2019

@author: reynolds
'''
from PyQt5.Qt import QThread
from wrtdk.io.writer import FileLogger

class LoggingStreamer(QThread):
    
    def __init__(self,running=False,debug=False):
        ''' constructor '''
        super().__init__()
        self._running = running
        self._debug = debug
        self.writer = FileLogger()
    
    def stop(self):
        '''  stops the thread  '''
        self._running = False
        self._debug = False
    
    def startLog(self,filename,ftype='w+'):
        '''  starts the log  '''
        self.writer.open(filename,ftype=ftype)

    def stopLog(self):
        '''  stops logging  '''
        self.writer.close()
        
    def isLogging(self):
        ''' returns whether the file writer is currently logging '''
        return self.writer.isLogging()
        