#!/usr/bin/env python
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# For handle args and watchmysass
from utils import handleArgs, searchNestedDirectories
from WatchMySASS import WatchMySASS

paths = []
rules = []
ARG_DICT = {}

# Create a pausable observer to avoid infinite loop
# https://github.com/gorakhargosh/watchdog/issues/181
class PausingObserver(Observer):
    def dispatch_events(self, *args, **kwargs):
        if not getattr(self, '_is_paused', False):
            super(PausingObserver, self).dispatch_events(*args, **kwargs)

    def pause(self):
        self._is_paused = True

    def resume(self):
        time.sleep(1)  # allow interim events to be queued
        self.event_queue.queue.clear()
        self._is_paused = False

# Create a handler class for the event_handler
# event_handler needs to call a dispatch method with self & event args
class Handler:
    def __init__(self, observer, arg_dict):
        self = self
        self.arg_dict = arg_dict
        self.rules = arg_dict["rules"]
        self.observer = observer

    def dispatch(self, event):
        path, filename = os.path.split(os.path.abspath(event.src_path))
        if self.shouldUpdate(path, filename) == True:
            self.observer.pause()
            # Only compile the changed file
            self.arg_dict["rules"] = [{path: filename}]
            WatchMySASS(self.arg_dict)
            self.observer.resume()

    def shouldUpdate(self, path, filename):
        for rule in self.rules:
            key = rule.keys()[0]
            if key == path and rule[path] == '*':
                return True
            elif key == path and rule[path] == filename:
                if filename.split('.')[-1] == 'html' and filename.split('-')[-1] != 'compiled.html':
                    return True
        return False

###################### Main Function #############################
def observe(argDict):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    ARG_DICT = argDict
    paths = argDict["paths"]
    rules = argDict["rules"]

    # Grab files from nested directories
    files = []
    for path in paths:
        files = list(set(searchNestedDirectories(path, '*.html')))

    # Add nested files to rules
    for file in files:
        _path, _filename = os.path.split(file)
        rules.append({_path: _filename})

    # Set observer args
    observer = PausingObserver()
    event_handler = Handler(observer, ARG_DICT)

    # Loop through paths and add to the observer
    for path in paths:
        print('\nListening for HTML/SCSS changes in %s...' % path)
        observer.schedule(event_handler, path, recursive=True)

    # Listen for changes
    observer.start()
    try:
        while True:
            time.sleep(1)
    # Kill on ctrl + c
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
