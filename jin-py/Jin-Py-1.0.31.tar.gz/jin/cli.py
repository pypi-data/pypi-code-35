import sys

from jin.makeconfig import Maker
from jin.parseconfig import Parser
from jin.composer import Composer
from jin.runner import Runner

VERSION = "Jin Simplified Warp (1.0.31) (Beta)"
USAGE = """usage: jin [--version] [--help] <command> [<args>]

Commands:

starting a new project
    init                Creates a new Jin project in the current directory

testing changes
    [push|empty] dry    Simulates a commit (dry run) and shows a log of the changes

managing a project
    push                Updates remote (remote_location) with host (host_location) changes
        + match-host    Deletes any files and folders in the remote that are not in the host
        + watch         Watches the project directory for changes and pushes to remote automatically

    empty               Removes all files and folders from remote (remote_location)

    status              Shows the most recent action in the project"""

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
