# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

BUTTONS = dict(cancel=QtWidgets.QDialogButtonBox.Cancel,
               ok=QtWidgets.QDialogButtonBox.Cancel,
               save=QtWidgets.QDialogButtonBox.Cancel,
               open=QtWidgets.QDialogButtonBox.Open,
               close=QtWidgets.QDialogButtonBox.Close)


class DialogButtonBox(QtWidgets.QDialogButtonBox):

    def set_horizontal(self):
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        self.setOrientation(QtCore.Qt.Vertical)

    def add_buttons(self, buttons):
        for btn in buttons:
            if btn not in BUTTONS:
                raise ValueError("button type not available")
            self.addButton(BUTTONS[btn])

    def add_accept_button(self, button):
        self.addButton(button, QtWidgets.QDialogButtonBox.AcceptRole)

    def add_reject_button(self, button):
        self.addButton(button, QtWidgets.QDialogButtonBox.RejectRole)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = DialogButtonBox()
    widget.set_buttons(["ok"])
    widget.show()
    app.exec_()
