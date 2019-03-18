import time
import logging


class NodeModule(object):
    active = False

    def __init__(self, mbus, queue, active, stop, cache):
        """Create the module, receives the message bus and queue"""
        self.id = self.__class__.__name__
        self.__mbus = mbus
        self.__queue = queue
        self.__active = active
        self.__stop = stop
        self.cache = cache

    def worker(self):
        while True:
            if self.__stop.is_set():
                self.cleanup()
                break
            if self.__active.is_set() and not self.active:
                self.active = True
            elif self.active:
                self.active = False
            try:
                if not self.__queue.empty():
                    self.__processQueue(self.__queue.get())
                    self.__queue.task_done()
                self.tick()
            except Exception as e:
                logging.exception("Exception in worker")
                time.sleep(5)

    def cleanup(self):
        pass

    def __processQueue(self, data):

        callback = getattr(self, "callback_" + data["type"], None)

        if data["type"] == "shutdown":
            exit()

        elif data["type"] == "__icache":
            self.cache = data["data"]

        elif callable(callback):
            callback(data)

        else:
            self.processMessage(data)

    def add_to_menu(self, title):
        self.push({'type': 'menu_add', 'title': title})

    def store(self, key, value):
        data = {"type": "store", "key": key, "value": value}
        self.__mbus.put(data)

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        return None

    def push(self, data):
        if "type" not in data:
            data = {"type": "unspecified", "data": data, }
        data['_source'] = self.id
        self.__mbus.put(data)

    def pushToModule(self, name, data):
        data["target"] = name
        self.__send(data)

    def wait(self, wait=None):
        if self.__queue.empty():
            if self.active:
                if callable(getattr(self, "draw", None)):
                    self.draw()
            if wait:
                time.sleep(wait)
            else:
                if self.active:
                    time.sleep(0.2)
                else:
                    self.__processQueue(self.__queue.get(True))
                    self.__queue.task_done()

    def tick(self):
        self.wait()

    def processMessage(self, data):
        pass
