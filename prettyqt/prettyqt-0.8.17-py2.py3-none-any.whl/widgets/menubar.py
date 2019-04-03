# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class MenuBar(QtWidgets.QMenuBar):
    """
    Customized MenuBar class
    """

    def add_action(self, action):
        self.addAction(action)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = MenuBar()
    widget.show()
    app.exec_()
