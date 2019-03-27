from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from pandasgui.functions import flatten_multiindex
import sys

# List of column names and multiple lists (as QTreeWidgets) to drag them to
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set up widgets and layout
        layout1 = QtWidgets.QVBoxLayout()

        self.setLayout(layout1)

        for x in range(3):
            layout1.addWidget(QtWidgets.QTreeWidget(self))

        # layout1.addLayout(layout2)


def main():
    s = time.time()
    print('a', time.time()-s)
    app = QtWidgets.QApplication(sys.argv)

    win = MyWidget()
    print('b',time.time()-s)
    win.show()
    print('c', time.time()-s)
    app.exec_()

if __name__ == '__main__':
    import time
    main()

