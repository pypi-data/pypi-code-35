import itertools
from collections import OrderedDict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication


class MyDict(OrderedDict):
    def __missing__(self, key):
        val = self[key] = MyDict()
        return val


class MyComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(MyComboBox, self).showPopup()


def bold(item):
    bold = QFont()
    bold.setWeight(QFont.Bold)
    item.setFont(0, bold)


def resize_column(widget):
    widget.header().setSectionResizeMode(QHeaderView.ResizeToContents)


def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)


def icon_style(icon_name):
    style = QApplication.instance().style()
    return style.standardIcon(icon_name)
