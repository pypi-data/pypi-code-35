import sys

from PyQt5.QtWidgets import QApplication

from Lupv.models.main import MainModel
from Lupv.controllers.main import MainController
from Lupv.views.main import MainView


class Lupv(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.main_model = MainModel()
        self.main_ctrl = MainController(self.main_model)
        self.main_view = MainView(self.main_ctrl, self.main_model)
        self.main_view.show()


def main():
    lupv = Lupv(sys.argv)
    sys.exit(lupv.exec_())


if __name__ == "__main__":
    main()
