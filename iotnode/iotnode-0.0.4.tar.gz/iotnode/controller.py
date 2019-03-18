import threading
import logging
import queue
import time


class Controller:
    modules = {}
    event_handlers = {}
    mbus = queue.Queue()
    stop = threading.Event()

    # The local database stores key value pairs
    cache = {}

    def __init__(self, modules=None):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(threadName)s %(message)s')

        for module in modules:
            try:
                self.__add_module(module)
            except Exception as e:
                logging.exception(
                    "Error loading module: " + str(module[0]))

    def __add_module(self, module):
        """Load a module class object and start the worker as a thread"""
        ref = module[0]
        self.modules[ref] = {}
        self.modules[ref]["queue"] = queue.Queue()
        self.modules[ref]["active"] = threading.Event()
        self.modules[ref]["object"] = getattr(
            __import__("nodemodules." + module[1],
                       fromlist=[ref]), ref)(
                           self.mbus,
                           self.modules[ref]["queue"],
                           self.modules[ref]["active"],
                           self.stop,
                           self.cache,)
        self.modules[ref]["thread"] = threading.Thread(
            target=self.modules[ref]["object"].worker, name=ref)
        self.modules[ref]["thread"].start()
        logging.info("Started " + ref)

    def __worker(self):
        while True:
            if self.stop.is_set():
                break
            try:
                if not self.mbus.empty():
                    self.__processMBus(self.mbus.get())
                    self.mbus.task_done()
                else:
                    time.sleep(0.01)
            except Exception as e:
                logging.exception("Exception in main worker")
                time.sleep(5)

    def __processMBus(self, data):
        if data["type"] != "render_data":
            logging.debug("MBUS: " + str(data))

        if "type" not in data:
            logging.error("Invalid message passed to bus: " + str(data))
            return

        if type(data["type"]) is not str:
            logging.error("Type value must be a string")
            return

        if "__" in data["type"]:
            logging.error("Internal __types cannot be broadcast from mbus")
            return

        if data["type"] == "shutdown":
            self.__shutdown()

        elif data["type"] == "store":
            self.__handleStore(data)

        elif data["type"] == "input":
            self.__handleInput(data)

        elif "target" in data:
            if data["target"] in self.modules:
                self.modules[data["target"]]["queue"].put(data)
            else:
                logging.error("Invalid module targeted: " + str(data))

        else:
            self.__sendAll(data)

    def __sendAll(self, data):
        for m in self.modules:
            self.modules[m]["queue"].put(data)

    def start(self):
        thread = threading.Thread(target=self.__worker, name="Controller")
        thread.start()
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            self.__shutdown()
        thread.join()

    def __shutdown(self):
        self.stop.set()
        self.__sendAll({"type": "shutdown", })
        logging.warning("Shutting down")
        logging.shutdown()
        exit()

    def __handleStore(self, data):
        if "key" not in data or "value" not in data:
            logging.error("Set key/value for store operations: " + str(data))
            return

        if "__" in data["key"]:
            logging.error("Cannot set __keys outside controller")
            return

        self.cache[data["key"]] = data["value"]
        self.__sendAll({"type": "__cache", "data": self.cache})

    def __handleInput(self, data):
        if "__target" not in self.cache:
            self.cache["__target"] = None
        if "switch" in data:
            if data["switch"] in self.modules:
                if self.cache["__target"]:
                    self.modules[self.cache["__target"]]["active"].clear()
                self.cache["__target"] = data["switch"]
                self.modules[self.cache["__target"]]["active"].set()
            else:
                logging.error("Invalid target for input switch: " + str(data))

        if self.cache["__target"]:
            self.modules[self.cache["__target"]]["queue"].put(data)
        else:
            logging.debug("No target for input: " + str(data))
