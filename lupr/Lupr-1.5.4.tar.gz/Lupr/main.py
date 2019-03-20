import sys
from PyQt5.QtWidgets import QApplication

from Lupr.model.model import Model
from Lupr.controllers.controller import Controller
from Lupr.views.main_view import MainView


class Lupr(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.model = Model()
        self.controller = Controller(self.model)
        self.main_view = MainView(self.model, self.controller)


def main():
    lupr = Lupr(sys.argv)
    lupr.setQuitOnLastWindowClosed(False)
    sys.exit(lupr.exec_())


if __name__ == "__main__":
    main()
