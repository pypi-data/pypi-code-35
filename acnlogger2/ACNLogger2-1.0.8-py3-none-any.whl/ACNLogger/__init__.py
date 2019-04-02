#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import os
import sys
import inspect
from html import escape

class ACNLogger:

        def check(self, message):
                newstr = message.replace("./", "")
                newstr = newstr.replace("..", "")
                return escape(newstr)

        def debug(self, message):
                self.logger.debug("["+os.path.basename(inspect.stack()[1].filename)+"]  ["+self.ENV+"]  ["+self.oid+"]  ["+self.session+"]  ["+self.correlationId+"]  " + self.check(message))

        def info(self, message):
                self.logger.info("["+os.path.basename(inspect.stack()[1].filename)+"]  ["+self.ENV+"]  ["+self.oid+"]  ["+self.session+"]  ["+self.correlationId+"]  " + self.check(message))

        def warning(self, message):
                self.logger.warning("["+os.path.basename(inspect.stack()[1].filename)+"]  ["+self.ENV+"]  ["+self.oid+"]  ["+self.session+"]  ["+self.correlationId+"]  " + self.check(message))

        def error(self, e):
                self.logger.error("["+os.path.basename(inspect.stack()[1].filename)+"]  ["+self.ENV+"]  ["+self.oid+"]  ["+self.session+"]  ["+self.correlationId+"]  " + self.check(str(e)))

        def critical(self, e):
                self.logger.critical("["+os.path.basename(inspect.stack()[1].filename)+"]  ["+self.ENV+"]  ["+self.oid+"]  ["+self.session+"]  ["+self.correlationId+"]  " + self.check(str(e)))

        def exception(self, e):
                if self.ENV != "PRO":
                        self.logger.exception("["+os.path.basename(inspect.stack()[1].filename)+"]  ["+self.ENV+"]  ["+self.oid+"]  ["+self.session+"]  ["+self.correlationId+"]  " + self.check(str(e)))
                else:
                        self.error(e)

        def setSession(self, session):
                self.session = session

        def setCorrelationId(self, correlationId):
                self.correlationId = correlationId

        def setOId(self, oid):
                self.oid = oid


        def __init__(self,name,file=None,console_level="debug",logfile_level="debug"):

                #file = file or name+".log"
                _logLevelMap = {
                        "debug": logging.DEBUG,
                        "info": logging.INFO,
                        "warning": logging.WARNING,
                        "error": logging.ERROR,
                        "critical":logging.CRITICAL
                }

                acn_logger=logging.getLogger(name) # Creating the new logger
                acn_logger.setLevel(logging.DEBUG) # Setting new logger level to INFO or above
                acn_logger.propagate = False


                console_handler=logging.StreamHandler()
                console_handler.setLevel(_logLevelMap[console_level])


                #file_handler=logging.FileHandler(file)
                #file_handler.setLevel(_logLevelMap[logfile_level])


                #acn_logger.addHandler(file_handler) #Adding file handler to the new logger
                acn_logger.addHandler(console_handler)

                formatter=logging.Formatter('[%(asctime)s]  [%(levelname)s]  [%(process)d]  %(message)s') #Creating a formatter

                #file_handler.setFormatter(formatter) #Setting handler format
                console_handler.setFormatter(formatter)

                self.session = "UNDEFINED"
                self.correlationId = "UNDEFINED"
                self.oid = "UNDEFINED"

                self.logger=acn_logger

                try:
                        self.ENV = os.environ["ENV"]
                except:
                        self.ENV = "ENV NOT SET"
                        self.warning("Environment variable ENV not set")

                self.info("STARTING MICROSERVICE")