import sys

from makeconfig import Maker
from parseconfig import Parser
from composer import Composer
from runner import Runner

VERSION = "Jin Simplified Warp (1.0.0) (Beta)"
USAGE = """
usage: jin [--version] [--help] <command> [<args>]

Common commands:

starting a new project
    init                Creates a new Jin project in the current directory

managing a project
    push                Updates destination with source changes
        + dry           Simulates the changes first before committing to destionation
        + match-host    Deletes any files and folders in the destination that are not in the source
        + watch         Watches project directory for changes and pushes automatically

    empty               Removes all files and folders from the destination
        + dry           Simulates the changes first before committing to destionation

    status              Shows the most recent change to the directory

tips
    1) Commands like 'push' and 'empty' have the option to use the 'dry' command
    after to simulate the changes first before committing them.
"""

def checkArgs():
    arguments = sys.argv[1:]

    if len(arguments) <= 0:
        print(USAGE)
        sys.exit(0)

    for arg in arguments:
        if arg in ("-h", "--help"):
            print(USAGE)
        elif arg in ("-v", "--version"):
            print(VERSION)
        elif arg in ("init"):
            maker = Maker(arguments)
            maker.createNewConfig()
            return
        elif arg in ("push", "empty"):
            parser = Parser()
            composer = Composer(arguments, parser.config)
            runner = Runner(composer).run()
            return
        elif arg in ("status"):
            try:
                with open(".jin/jin.log", "r") as log:
                    print(f"Jin Log (most recent action):\n\n{log.read()}")
            except:
                print("No actions have been commited yet.")
        else:
            print(USAGE)
            sys.exit(1)
