"""
Module:
    motiv.interfaces.events

Description:
    contains wrapper class for events
"""

class Event(object):
    def __init__(self, emitter, event_type, **kwargs):
        self.emitter = emitter
        self.event_type = event_type
        self.params = kwargs

