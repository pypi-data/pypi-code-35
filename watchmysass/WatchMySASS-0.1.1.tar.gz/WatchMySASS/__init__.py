#!/usr/bin/env python
import observer
from WatchMySASS import WatchMySASS
from utils import stripNewLines, handleArgs

def main():
    # Paths tells the observer what directories to listen to
    # Rules tells the observer what files to react to within those directories
    handler = handleArgs()
    args = handler[0]
    rules = handler[1]
    watch = args.watch
    paths = args.relpath
    destructive = args.destructive
    uncompressed = args.uncompressed

    argDict = {
        "paths": args.relpath,
        "rules": rules,
        "watch": args.watch,
        "destructive": args.destructive,
        "uncompressed": args.uncompressed
    }

    if watch == True:
        # Call observer.py with args
        observer.observe(argDict)
    else:
        # Directly compile files
        WatchMySASS(argDict)

if __name__ == "__main__":
    main()
