import re
import logging

class Mangler(object):
    def __init__(self, patterns, sender):
        self.patterns = []
        for pattern in patterns:
            self.patterns.append(
                {
                    "search": re.compile(pattern["search"]),
                    "replace": pattern["replace"]
                }
            )
        self.sender = sender

    def mangle(self, metrics):
        logging.debug("Mangling")
        for metric in metrics.split("\n"):
            for pattern in self.patterns:
                metric = pattern["search"].sub(pattern["replace"], metric)
            logging.debug("Sending metric %s", metric)
            self.sender.send(metric)
