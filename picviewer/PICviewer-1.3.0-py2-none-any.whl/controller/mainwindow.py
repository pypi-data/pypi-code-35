import sys, os, glob
import numpy as np
import matplotlib
#matplotlib.rcParams['backend.qt4']='PySide'
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.patches as patches
#from picviewer.ui_files.base import Ui_MainWindow
import threading
import csv

import picviewer
from picviewer.dataplotter.prepare_localplot import PrepareLocalPlot

from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox



ui_path = os.path.dirname(__file__)
ui_path = ui_path[:-10] + 'ui_files/base.ui'

Ui_MainWindow, QMainWindow = loadUiType(ui_path)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
         initialize GUI
         
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)
         
        # coordiates
        self.coordLabel.setText('(x1,x2)=(%d,%d)'%(0,0))
        # default number of panels
        self.rowpanelSpinBox.setValue(2)
        self.rowpanelSpinBox.setMinimum(1)
        self.rowpanelSpinBox.setMaximum(6)
        self.columnpanelSpinBox.setValue(1)
        self.columnpanelSpinBox.setMinimum(1)
        self.columnpanelSpinBox.setMaximum(5)
        # time step stride
        self.stepSpinBox.setValue(1)
        self.stepSpinBox.setMinimum(1)
        
        # logo icon
        logo_path = os.path.dirname(__file__)
        logo_path = logo_path[:-10] + 'images/logo.png'
        self.imageButton = QPushButton(self.centralwidget)
        self.imageButton.setIcon(QtGui.QIcon(logo_path))
        self.imageButton.setIconSize(QtCore.QSize(80, 68))
        self.imageButton.setGeometry(QtCore.QRect(10, 230, 80, 68))   
        self.imageButton.clicked.connect(self.imagebutton)     

        # field button
        self.fieldButton.setChecked(True)

        # 2D slice for 3D data
        self.xzButton.setChecked(True)

        # space slider
        self.x1minSlider.setValue(0)
        self.x1minSlider.setRange(0,100)
        self.x1maxSlider.setValue(100)
        self.x1maxSlider.setRange(0,100)
        self.x2minSlider.setValue(0)
        self.x2minSlider.setRange(0,100)
        self.x2maxSlider.setValue(100)
        self.x2maxSlider.setRange(0,100)

        # slice value slider
        self.slicevalueSlider.setRange(1,50)
        self.slicevalueSlider.setValue(25)
        self.slicevalueSlider.setMinimum(2)
        self.slicevalueSlider.setMaximum(48)
        self.strideSlider.setRange(1,50) 
        self.strideSlider.setValue(10)
        

        # contrast sliders
        self.contrastSlider.setRange(1,100)
        self.contrastSlider.setValue(100)
        self.contrastLabel.setText(str("%d%%" %100))


        # aspect ratio checkbox
        self.aspectCheckBox.setChecked(False)

        # line selection checkbox
        self.lineCheckBox.setChecked(False)

        # rectangle selection checkbox
        self.rectangleCheckBox.setChecked(False)

        # sync time checkbox
        self.synctimeBox.setChecked(False)


        # AMR level buttons    
        self.amrSpinBox.setValue(0)
        self.amrSpinBox.setMinimum(0)
        
        # initial gui size
        self.width0 = self.geometry().width()
        self.height0 = self.geometry().height()
        # default panel arrays
        self.nrow=2
        self.ncolumn=1
        self.panelselect = 1

        # Save parameters in each window panel
        # Each panal can work independently by setting these parameters.
        # When you click a window panel, the paramaeter saved in each panel is loaded.

        # tstep panel [10, 5, 3, ...]
        self.tstep_panel = []
        # field  i.e., ['Bx', 'By', ...]
        self.field_panel = []
        # field AMR level panel
        self.amrlevel_panel = []
        # species i.e., ['elec', 'ions', ...]
        self.species_panel = []
        # phase for particles i.e., [('px','x'),('py','x'), ...]
        self.phase_panel = []
        # field select i.e., ['True', 'False', ...], 
        # to check whether field or particle is selected in a panel.
        self.field_select_panel = []
        # local line selection i.e., ['True', 'False', ...]
        self.line_panel = []
        # local rectangle selection i.e., ['True', 'False', ...]
        self.rectangle_panel = []
        # aspect ratio selection  i.e., ['auto', 'equal', ...]
        self.aspect_panel = []
        # 2D slice plane in 3D i.e., ['xy', 'yz', ...]
        self.sliceplane_panel = []
        # 3rd axis coordinate: i.e., [15, 15, ...]  <-- range between (0,30)
        self.slicevalue_panel = []
        # 3rd axis particle stride: i.e., [1, 20, ...]  <-- range between (0,30)
        self.stride_panel = []
        # contrast 
        self.contrast_panel = []
        # xmin and xmax location in 2D slice: i.e., [10, 30, ...]  <-- range between (0,100)
        self.xminloc_panel = []
        self.xmaxloc_panel = []
        # ymin and ymax location in 2D slice: i.e., [10, 10, ...]  <-- range between (0,100)
        self.yminloc_panel = []
        self.ymaxloc_panel = []
        # zmin and zmax location in 2D slice: i.e., [10, 20, ...]  <-- range between (0,100)
        self.zminloc_panel = []
        self.zmaxloc_panel = []

        # local panel
        self.localfield_panel = []
        self.localphase_panel = []

        # field data container has multiple key words, i.e.,
        # {('Bx', tstep) : data, ..... }
        self.fdata_container = {}

        # particle data container has multiple key words, i.e.,
        # {('elec', 'px', tstep) : data, ..... }
        self.pdata_container = {}

        # subpanel window
        #self.subplot = {}
        #self.subfieldplot = {}
        self.existingLocalplot = False
        
        # Navigation toolbar home
        self.home = False
    
        # create Matplotlib window
        self.figure = Figure()
        self.canvas = Canvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
    
         # create plotwidget
        self.LayoutWidget = QWidget(self.centralwidget)
        self.LayoutWidget.setGeometry(QtCore.QRect(430, 10, 550, 770))
        self.plotwidget_layout = QVBoxLayout(self.LayoutWidget)
        self.plotwidget_layout.setContentsMargins(0, 0, 0, 0)

        self.plotwidget_layout.addWidget(self.canvas)
        self.plotwidget_layout.addWidget(self.toolbar)

 
    def resizeEvent(self,  event):

        width = event.size().width()
        height = event.size().height()
        wratio=1.*(width-400)/(self.width0-400)
        hratio=1.*height/self.height0
        self.LayoutWidget.setGeometry(QtCore.QRect(430, 10, 550*wratio, 770*hratio))

    def imagebutton(self):

        logo_path = os.path.dirname(__file__)
        logo_path = logo_path[:-10] + 'images/logo.png'

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setIconPixmap(QtGui.QPixmap(logo_path))
        version = picviewer.__version__
        #msg.setWindowTitle("Visualization toolkit for PIC simulations")
        msg.setText( "<br><br><br>" 
		               + 'PICViewer' + " v" + version+ "<br>" 
		               + "(c) 10/2018 LBNL <br><br>")
		               #+ "<a href='{0}'>{0}</a><br><br>".format(website)
		               #+ "<a href='mailto:{0}'>{0}</a><br><br>".format(email) 
		               #+ "License: <a href='{0}'>{1}</a>".format(license_link, 
                       #license_name) )
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        #msg.buttonClicked.connect(msgbtn)  
        msg.exec_()


    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Escape:
            sys.exit(0)

        if self.rectangleCheckBox.isChecked():
            if not self.toolbar.actions()[4].isChecked() and not self.toolbar.actions()[5].isChecked():

                distance = 0.05
                x1min = float(self.x1minLabel.text())
                x1max = float(self.x1maxLabel.text())
                x2min = float(self.x2minLabel.text())
                x2max = float(self.x2maxLabel.text())

                panelselect = self.panelselect
                # check if a rectangle selection tool is already made
                if self.resize[panelselect-1] == 2: 
                    #print(key)
                    if key == 76:
                        #print('Left')
                        xtrans = -(x1max-x1min)*distance
                        ytrans = 0
                        self.xc[panelselect-1] = self.xc[panelselect-1] + xtrans
                        self.yc[panelselect-1] = self.yc[panelselect-1] + ytrans
                        rect = patches.Rectangle((self.xc[panelselect-1]-self.rectw[panelselect-1]*.5, 
                                    self.yc[panelselect-1]-self.recth[panelselect-1]*.5),
                                    self.rectw[panelselect-1],self.recth[panelselect-1],
                                    linewidth=0.8,edgecolor='black',facecolor='none')
                        [p.remove() for p in reversed(self.axes[panelselect-1].patches)]
                        self.axes[panelselect-1].add_patch(rect)
                        self.canvas.draw_idle()

                    if key == 39:
                        #print('Right')
                        xtrans = (x1max-x1min)*distance
                        ytrans = 0
                        self.xc[panelselect-1] = self.xc[panelselect-1] + xtrans
                        self.yc[panelselect-1] = self.yc[panelselect-1] + ytrans
                        rect = patches.Rectangle((self.xc[panelselect-1]-self.rectw[panelselect-1]*.5, 
                                    self.yc[panelselect-1]-self.recth[panelselect-1]*.5),
                                    self.rectw[panelselect-1],self.recth[panelselect-1],
                                    linewidth=0.8,edgecolor='black',facecolor='none')

                        [p.remove() for p in reversed(self.axes[panelselect-1].patches)]
                        self.axes[panelselect-1].add_patch(rect)
                        self.canvas.draw_idle()

                    if key == 80:
                        #print('Up')
                        xtrans = 0
                        ytrans = (x2max-x2min)*distance
                        self.xc[panelselect-1] = self.xc[panelselect-1] + xtrans
                        self.yc[panelselect-1] = self.yc[panelselect-1] + ytrans
                        rect = patches.Rectangle((self.xc[panelselect-1]-self.rectw[panelselect-1]*.5, 
                                    self.yc[panelselect-1]-self.recth[panelselect-1]*.5),
                                    self.rectw[panelselect-1],self.recth[panelselect-1],
                                    linewidth=0.8,edgecolor='black',facecolor='none')

                        [p.remove() for p in reversed(self.axes[panelselect-1].patches)]
                        self.axes[panelselect-1].add_patch(rect)
                        self.canvas.draw_idle()
                    if key == 59:
                        #print('Down')
                        xtrans = 0
                        ytrans = -(x2max-x2min)*distance
                        self.xc[panelselect-1] = self.xc[panelselect-1] + xtrans
                        self.yc[panelselect-1] = self.yc[panelselect-1] + ytrans
                        rect = patches.Rectangle((self.xc[panelselect-1]-self.rectw[panelselect-1]*.5,
                                    self.yc[panelselect-1]-self.recth[panelselect-1]*.5),
                                    self.rectw[panelselect-1],self.recth[panelselect-1],
                                    linewidth=0.8,edgecolor='black',facecolor='none')

                        [p.remove() for p in reversed(self.axes[panelselect-1].patches)]
                        self.axes[panelselect-1].add_patch(rect)
                        self.canvas.draw_idle()

                    # Here make a local plot
                    self.x1localmin = self.xc[panelselect-1] - abs(self.rectw[panelselect-1])*.5
                    self.x1localmax = self.xc[panelselect-1] + abs(self.rectw[panelselect-1])*.5
                    self.x2localmin = self.yc[panelselect-1] - abs(self.recth[panelselect-1])*.5
                    self.x2localmax = self.yc[panelselect-1] + abs(self.recth[panelselect-1])*.5

                    if self.field_select_panel[self.panelselect-1]:
                        PrepareLocalPlot(self).plotfield()
                                            
                    else:
                        PrepareLocalPlot(self).plotparticle()
