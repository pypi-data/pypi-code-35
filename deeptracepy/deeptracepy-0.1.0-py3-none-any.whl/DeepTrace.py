import os
from .Trace import Trace
from .DeepTraceClient import DeepTraceClient

class DeepTrace():
    def __init__(self, config):
        self.__config = config

    def handle(self, req, resp):
        trace = Trace(self.__config, req, resp).factory()
        if not self.__config['DEEP_TRACE_URL']:
            return
        client = DeepTraceClient(self.__config['DEEP_TRACE_URL'])
        client.createTrace(trace.data)

        return req, resp