import os
import time
import re
import sys
import subprocess

from jin.watcher import Watcher

class Runner():
    """Executes commands given by Composer and stores the output in jin.log"""

    def __init__(self, composer):
        self.config = composer.config
        self.command = composer.command
        self.minToWatch = composer.minToWatch
        self.dryRun = composer.isDryRun
        self.isHot = composer.isHot

    def run(self):
        if self.isHot:
            watcher = Watcher(self, self.execute)
            watcher.watch()
        else:
            self.execute(self.command)

    def execute(self, command):
        cmd = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        out, err = cmd.communicate()
        if cmd.returncode != 0:
            print("An error has occured!\n\n", err.decode("utf-8"))
            sys.exit(1)

        out_final = []
        out_formatted = out.decode("utf-8").split("\n")[1:]
        out_formatted = out_formatted[0:len(out_formatted)-3]

        with open(".jin/jin.log", "w+") as log:
            log.write(f"Command: {' '.join(command)} \n\n")

            for line in out_formatted:
                if re.search("^(\t|\s)+?", line):
                    continue
                else:
                    out_final.append(line)

            log.write("\n".join(out_final))

        if self.dryRun:
            print("Changes (DRY RUN):\n")
        else:
            print("Changes:\n")

        print("\n".join(out_final))
