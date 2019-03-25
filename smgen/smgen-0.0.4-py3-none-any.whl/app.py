from .parser import Parser
from .generator import CodeGener
from .writer import Writer
import argparse


class CLI:
    def __init__(self):
        self.cli = argparse.ArgumentParser()
        self.cli.add_argument('--states', dest='states')
        self.cli.add_argument('--init', dest='init')
        self.cli.add_argument('--app', dest='app')

if __name__ == "__main__":
    cli = CLI().cli
    cfg = vars(cli.parse_args())
    stateConf, initConf, app = cfg["states"], cfg["init"], cfg["app"]
    info = Parser(stateConf, initConf).info
    codeinfo = CodeGener(info).genCode()
    w = Writer(app)
    w.create(codeinfo)
