import os
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox


ui_path = os.path.dirname(__file__)
ui_path = ui_path[:-11] + 'ui_files/subwindow.ui'

Ui_SubWindow, QMainWindow = loadUiType(ui_path)

class SubWindow(QMainWindow, Ui_SubWindow):
    def __init__(self, MainWindow, 
                mainleft,
                maintop,
                mainwidth,
                mainheight):
        
        super(SubWindow, self).__init__()
        self.setupUi(self)

        self.main = MainWindow

        panelselect = self.main.panelselect

        nrow = self.main.nrow
        ncolumn = self.main.ncolumn

        global width0, height0
        width0 = 500; height0 = 400

        # panel button matrix: i: row, j: column
        i = (panelselect-1)/ncolumn
        j = np.mod((panelselect-1),ncolumn)

        top = maintop+mainheight/(nrow+1)*i+j*40
        left = mainleft+mainwidth+j*100+i*40

        self.setGeometry(QtCore.QRect(left, top, width0, height0))

        self.setWindowTitle('subpanel %d'%(panelselect))

        self.LayoutWidget = QWidget(self.centralwidget)
        self.LayoutWidget.setGeometry(QtCore.QRect(10, 10, width0-10, height0-20))
        self.plotwidget_layout = QVBoxLayout(self.LayoutWidget)
        self.plotwidget_layout.setContentsMargins(0, 0, 0, 0)

        self.figure = Figure()
        self.canvas = Canvas(self.figure)
        self.plotwidget_layout.addWidget(self.canvas)


    def resizeEvent(self,  event):

        width = event.size().width()
        height = event.size().height()
        wratio=1.*width/width0
        hratio=1.*height/height0
        self.LayoutWidget.setGeometry(QtCore.QRect(10, 10, (width0-10)*wratio, (height0-20)*hratio))
 

    