import time
import queue

from ensure import ensure_annotations, ensure

from motiv.sync import SystemEvent
from motiv.channel.mixin import Channel, ChannelIn, ChannelOut

class BasicChannelOut(ChannelOut):

    @ensure_annotations
    def __init__(self, event_queue: queue.Queue):

        self.event_queue = event_queue

    def send(self, body):
        self.event_queue.put(body)

    def close(self):
        self.event_queue = None

class BasicChannelIn(ChannelIn):

    @ensure_annotations
    def __init__(self, event_queue: queue.Queue):
        self.event_queue = event_queue

    def receive(self):
        return self.event_queue.get()

    def poll(self, exit_condition: SystemEvent, poll_interval=50):
        ensure(exit_condition).is_a(SystemEvent)

        while not exit_condition.is_set():
            qsize = self.event_queue.qsize()
            if qsize > 0:
                return self.receive()
            time.sleep(poll_interval)

        return None

    def close(self):
        self.event_queue = None

class BasicChannel(Channel):

    @ensure_annotations
    def __init__(self, channel_in: BasicChannelIn, channel_out: BasicChannelOut):
        self.cin = channel_in
        self.cout = channel_out

    def proxy(self):
        while True:
            payload = self.cin.receive()
            self.cout.send(payload)

    def send(self, body):
        return self.cout.send(body)

    def receive(self):
        return self.cin.receive()

    def poll(self, exit_condition, poll_interval=50):
        return self.cin.poll(exit_condition, poll_interval)

    def close(self):
        self.cin.close()
        self.cout.close()

__all__ = ['BasicChannel', 'BasicChannelIn', 'BasicChannelOut']
