# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta


class ProgressDialog(QtWidgets.QProgressDialog):
    """
    simple Progressdialog
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setRange(0, 0)
        progress_bar.setTextVisible(False)
        self.setBar(progress_bar)

        self.setWindowIcon(qta.icon("mdi.timer-sand-empty", color="lightgray"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setCancelButton(None)
        self.cancel()

    def open(self, message=None):
        if not message:
            message = "Processing..."
        self.setLabelText(message)
        self.show()
