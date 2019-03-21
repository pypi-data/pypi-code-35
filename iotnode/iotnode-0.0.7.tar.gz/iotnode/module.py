import time
import logging


class NodeModule:
    active = False

    def __init__(self, mbus, queue, state, cache):
        """Create the module, receives the message bus and queue"""
        self.id = self.__class__.__name__
        self.mbus = mbus
        self.queue = queue
        self.state = state
        self.changed = True
        self.cache = cache

    def worker(self):
        while True:
            try:
                if self.state.value == 'S':
                    self.cleanup()
                    break
                if self.state.value == 'A' and not self.active:
                    self.active = True
                    self.changed = True
                elif self.active and self.state.value != 'A':
                    self.active = False
                if not self.queue.empty():
                    self.processQueue(self.queue.get())
                else:
                    self.tick()
            except Exception as e:
                logging.exception("Exception in worker")
                time.sleep(5)

    def cleanup(self):
        pass

    def get_callbacks(self):
        callbacks = []
        names = dir(self)
        for name in names:
            if "callback_" in name:
                if callable(getattr(self, name, None)):
                    callbacks.append(name.replace("callback_", ""))
        return callbacks

    def processQueue(self, data):
        callback = getattr(self, "callback_" + data["type"], None)

        if data["type"] == "__icache":
            self.cache = data["data"]

        elif callable(callback):
            callback(data)

        else:
            self.processMessage(data)

    def add_to_menu(self, title):
        self.push({'type': 'menu_add', 'title': title})

    def update(self):
        self.changed = True

    def store(self, key, value):
        data = {"type": "store", "key": key, "value": value}
        self.mbus.put(data)

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        return None

    def push(self, data):
        if "type" not in data:
            data = {"type": "unspecified", "data": data, }
        data['_source'] = self.id
        self.mbus.put(data)

    def pushToModule(self, name, data):
        data["target"] = name
        self.send(data)

    def wait(self, wait=None):
        if self.active and self.changed:
            if callable(getattr(self, "draw", None)):
                self.changed = False
                self.draw()
        if wait:
            time.sleep(wait)
        elif self.active:
            time.sleep(0.1)
        else:
            self.processQueue(self.queue.get(True))

    def tick(self):
        self.wait()

    def processMessage(self, data):
        pass
