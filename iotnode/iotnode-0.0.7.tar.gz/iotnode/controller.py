from multiprocessing import Process, Queue, Value
import logging
import time


class Controller:
    modules = {}
    event_handlers = {}
    mbus = Queue()
    stop = Value('u', 'R')

    # The local database stores key value pairs
    cache = {}

    def __init__(self, modules=None):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(processName)s %(message)s')

        for module in modules:
            try:
                self.add_module(module)
            except Exception as e:
                del self.modules[module[0]]
                logging.exception(
                    "Error loading module: " + str(module[0]))

    def add_module(self, module):
        """Load a module class object and start the worker as a process"""
        ref = module[0]
        self.modules[ref] = {}
        self.modules[ref]["queue"] = Queue()
        self.modules[ref]["state"] = Value('u', 'R')
        self.modules[ref]["object"] = getattr(
            __import__("nodemodules." + module[1],
                       fromlist=[ref]), ref)(
                           self.mbus,
                           self.modules[ref]["queue"],
                           self.modules[ref]["state"],
                           self.cache,)
        self.modules[ref]["callbacks"] = self.modules[ref]["object"].get_callbacks()
        self.modules[ref]["process"] = Process(
            target=self.modules[ref]["object"].worker, name=ref)
        self.modules[ref]["process"].daemon = True
        self.modules[ref]["process"].start()
        logging.info("Started " + ref)

    def worker(self):
        while True:
            try:
                if self.stop.value == 'S':
                    break
                self.processMBus(self.mbus.get(True))
            except Exception as e:
                logging.exception("Exception in main worker")
                time.sleep(5)

    def processMBus(self, data):
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
            self.shutdown()

        elif data["type"] == "store":
            self.handleStore(data)

        elif data["type"] == "input":
            self.handleInput(data)

        elif "target" in data:
            if data["target"] in self.modules:
                self.modules[data["target"]]["queue"].put(data)
            else:
                logging.error("Invalid module targeted: " + str(data))

        else:
            self.handleCallback(data)

    def start(self):
        process = Process(target=self.worker, name="Controller")
        process.daemon = True
        process.start()
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            self.shutdown()
        process.join()

    def shutdown(self):
        for ref in self.modules:
            self.modules[ref]["state"] = 'S'
        logging.warning("Shutting down")
        logging.shutdown()
        self.stop.value = 'S'
        exit()

    def handleStore(self, data):
        if "key" not in data or "value" not in data:
            logging.error("Set key/value for store operations: " + str(data))
            return

        if "__" in data["key"]:
            logging.error("Cannot set __keys outside controller")
            return

        self.cache[data["key"]] = data["value"]
        self.sendAll({"type": "__cache", "data": self.cache})

    def handleCallback(self, data):
        for m in self.modules:
            if data["type"] in self.modules[m]["callbacks"]:
                self.modules[m]["queue"].put(data)

    def handleInput(self, data):
        if "__target" not in self.cache:
            self.cache["__target"] = None
        if "switch" in data:
            if data["switch"] in self.modules:
                target = self.cache.get("__target")
                if target:
                    self.modules[target]["state"].value = "R"
                self.cache["__target"] = data["switch"]
                self.modules[self.cache["__target"]]["state"].value = "A"
            else:
                logging.error("Invalid target for input switch: " + str(data))

        if self.cache["__target"]:
            self.modules[self.cache["__target"]]["queue"].put(data)
        else:
            logging.debug("No target for input: " + str(data))

    def sendAll(self, data):
        for m in self.modules:
            self.modules[m]["queue"].put(data)
