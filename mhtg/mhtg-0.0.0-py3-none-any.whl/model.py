import abc
import os

import h11


class HTTPEvent(metaclass=abc.ABCMeta):
    pass


HTTPEvent.register(h11.Request)
HTTPEvent.register(h11.InformationalResponse)
HTTPEvent.register(h11.Response)
HTTPEvent.register(h11.Data)
HTTPEvent.register(h11.EndOfMessage)
HTTPEvent.register(h11.ConnectionClosed)


class FilePlaceholder:
    def __init__(self, factory, size):
        self.factory = factory
        self.size = size

    def __len__(self):
        return self.size
