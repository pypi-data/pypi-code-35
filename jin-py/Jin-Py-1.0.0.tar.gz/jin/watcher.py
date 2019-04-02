import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

class Watcher():
    """Watches Jin project directory for changes and runs given command"""

    def __init__(self, runner, exfunc):
        self.config = runner.config
        self.path = os.path.abspath(".")
        self.exfunc = exfunc
        self.command = runner.command
        self.minToWatch = runner.minToWatch

    def watch(self):
        observer = Observer()
        eventHandler = EventHandler(self)
        observer.schedule(eventHandler, self.path, recursive=True)
        observer.start()

        print("Watching for changes...")

        try:
            while True:
                if eventHandler.SHOULD_RUN_CMD:
                    eventHandler.run()
                    eventHandler.SHOULD_RUN_CMD = False
                time.sleep(3)
        except KeyboardInterrupt:
            print("Stopping...")
            observer.stop()
            sys.exit(0)
        except:
            observer.stop()
            print("Jin watcher encountered an error!")
            sys.exit(1)

        observer.join()

class EventHandler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.CONFIG = watcher.config
        self.EXECUTE = watcher.exfunc
        self.COMMAND = watcher.command
        self.WATCHER_MIN = watcher.minToWatch
        self.WATCHER_CHANGES = 0
        self.SHOULD_RUN_CMD = False

    def run(self):
        self.EXECUTE(self.COMMAND)

    def on_modified(self, event):
        if self.CONFIG.get("igspec") != None:
            isIgnoredFile = False

            for ignore in self.CONFIG.get("igspec"):
                if ignore in event.src_path:
                    print(f"{event.src_path} is ignored by rule {ignore}")
                    isIgnoredFile = True
            if not isIgnoredFile:
                self.WATCHER_CHANGES += 1

        if self.CONFIG.get("igtype") != None:
            isIgnoredType = False

            for ignore in self.CONFIG.get("igtype"):
                if ignore in event.src_path:
                    print(f"{event.src_path} is ignored by rule {ignore}")
                    isIgnoredType = True
            if not isIgnoredType:
                self.WATCHER_CHANGES += 1

        # fix issue with command being run multiple times
        if self.WATCHER_CHANGES > self.WATCHER_MIN:
            self.SHOULD_RUN_CMD = True
            self.WATCHER_CHANGES = 0
