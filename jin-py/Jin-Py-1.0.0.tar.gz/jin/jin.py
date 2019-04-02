import sys
import cli
from shutil import which

def main():
    if which("rsync") is None:
        print("Installation of rsync not found. Please install rsync and try again")
        sys.exit(1)
    else:
        cli.checkArgs()

if __name__ == "__main__":
    main()
