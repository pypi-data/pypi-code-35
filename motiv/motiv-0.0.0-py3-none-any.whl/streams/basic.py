 queue

from ensure import ensure_annotations
from motiv.channel import BasicChannelIn, BasicChannelOut
from motiv.straems.mixin import (Emitter, Subscriber,
        Ventilator, Worker)

class BasicEmitter(Emitter):

    @ensure_annotations
    def __init__(self, name: str, q: queue.Queue):
        self.name = name
        cout = BasicChannelOut(q)
        Emitter.__init__(self, cout)

    def connect(self):
        pass

class BasicSubscriber(Subscriber):

    @ensure_annotations
    def __init__(self, name: str, q: queue.Queue):
        self.name = name
        cin = BasicChannelIn(q)
        self.subscriptions = []
        Subscriber.__init__(self, cout)

    def subscribe(self, event_type: int):
        ensure(event_type).is_an(int)
        self.subscriptions.append(event_type)

    def connect(self):
        pass
