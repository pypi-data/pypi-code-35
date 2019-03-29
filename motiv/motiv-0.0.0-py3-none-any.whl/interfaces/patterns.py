"""
Module:
    motiv.interfaces.patterns

Description:
    boilerplate design patterns.
"""

import abc

from motiv.interfaces.events import Event
from motiv.exceptions import OrphanActorError
from ensure import ensure_annotations

class Registry(abc.ABC):

    @abc.abstractmethod
    def notify_observers(self, event):
        pass

    @abc.abstractmethod
    def add_observer(self, observer):
        pass

    @abc.abstractmethod
    def remove_observer(self, observer):
        pass

class Observable(abc.ABC):

    @ensure_annotations
    def __init__(self, registry: Registry, *args, **kwargs):
        self.registry = registry

    def notify_observers(self, event_type, *args, **kwargs):
        event = Event(self, event_type, *args, **kwargs)
        return self.registry.notify_observers(event)

class Observer(abc.ABC):

    SUBSCRIBES_TO = []
    def __init__(self, registry, *args, **kwargs):

        if len(self.SUBSCRIBES_TO) is 0:
            raise OrphanActorError("Observer {self.__class__.__name__}"\
                    "doesn't subscribe to any events, set SUBSCRIBES_TO")

        self.registry = registry

    def observe(self, event_type):
        registry.add_observer(self, event_type)

    @abc.abstractmethod
    def notify(self, event):
        self.events.put(event)

class Middleware(Observer, Observable):
    def __init__(self, *args, **kwargs):
        Observer.__init__(self, *args, **kwargs)
        Observable.__init__(self, *args, **kwargs)

class SingletonType(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

